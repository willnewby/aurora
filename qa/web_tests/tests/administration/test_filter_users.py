from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import unittest
from qa.web_tests import config

class TestFilterUsers(unittest.TestCase):

    def setUp(self):
        self.base_url = config.base_url
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(config.implicitly_wait)

    def test_filter_users(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.base_url + "/")
        driver.find_element_by_name("username").send_keys(config.username)
        driver.find_element_by_name("password").send_keys(config.password)
        driver.find_element_by_css_selector("input.loginSubmit").click()
        Move = ActionChains(driver).move_to_element(driver.find_element_by_link_text("Settings"))
        Move.perform()
        driver.find_element_by_link_text("Users").click()
        #filter
        lst = driver.find_elements_by_xpath("//table[@id='table_OSUserList']/tbody/tr")
        count_before_filter = len(lst)
        if count_before_filter>1:
            name_user = driver.find_element_by_xpath("//table/tbody/tr[1]/td[3]").text
            driver.find_element_by_id("filter").send_keys(name_user)
            lst1 = driver.find_elements_by_xpath("//table[@id='table_OSUserList']/tbody/tr[@style='display: none;']")
            count_after_filter = len(lst1)
            self.assertEquals(count_before_filter-count_after_filter,int(driver.find_elements_by_xpath("//div/label")[1].text))
        else:
            raise('Users are not enough in table')

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def tearDown(self):
        self.driver.save_screenshot(config.screen_path)
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()