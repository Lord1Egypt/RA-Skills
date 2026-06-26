#!/usr/bin/env python3

import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 延迟导入 ddddocr，避免启动时出错
# import ddddocr

# 配置文件
CONFIG_FILE = os.path.join(os.path.dirname(__file__), ".env")

# 是否启用详细日志（调试用）
VERBOSE = os.getenv("KUAIPU_VERBOSE", "0") == "1"

# 临时文件目录
TMP_DIR = os.path.join(os.path.dirname(__file__), "tmp")

# 确保tmp目录存在
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

# 临时文件
CAPTCHA_IMAGE = os.path.join(TMP_DIR, "kuaipu_captcha.png")
COOKIE_FILE = os.path.join(TMP_DIR, "kuaipu_cookies.pkl")
LOGIN_RESULT_HTML = os.path.join(TMP_DIR, "kuaipu_login_result.html")
LOGIN_RESULT_SCREENSHOT = os.path.join(TMP_DIR, "kuaipu_login_result.png")
LOGIN_PAGE_SCREENSHOT = os.path.join(TMP_DIR, "kuaipu_login_page.png")
MAIN_PAGE_SCREENSHOT = os.path.join(TMP_DIR, "kuaipu_main_page.png")
MAIN_PAGE_HTML = os.path.join(TMP_DIR, "kuaipu_main_page.html")
SHENPI_PAGE_SCREENSHOT = os.path.join(TMP_DIR, "kuaipu_shenpi_page.png")
SHENPI_PAGE_HTML = os.path.join(TMP_DIR, "kuaipu_shenpi_page.html")
SHENPI_PAGE_TEXT = os.path.join(TMP_DIR, "kuaipu_shenpi_page_text.txt")
LOGIN_ERROR_SCREENSHOT = os.path.join(TMP_DIR, "kuaipu_login_error.png")
SHENPI_ERROR_SCREENSHOT = os.path.join(TMP_DIR, "kuaipu_shenpi_error.png")


# 清除临时文件夹
def clear_tmp_dir():
    """清除临时文件夹中的所有文件"""
    try:
        if os.path.exists(TMP_DIR):
            files = os.listdir(TMP_DIR)
            for file in files:
                file_path = os.path.join(TMP_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print(f"临时文件夹已清空: {TMP_DIR}")
    except Exception as e:
        print(f"清空临时文件夹失败: {e}")


# 读取配置文件
def read_config():
    """读取配置文件"""
    config = {}
    if not os.path.exists(CONFIG_FILE):
        print(f"错误: 配置文件 {CONFIG_FILE} 不存在")
        return None

    try:
        with open(CONFIG_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    config[key] = value
    except Exception as e:
        print(f"错误: 读取配置文件失败: {e}")
        return None

    # 检查配置是否完整
    required_keys = ["kuaipu_url", "kuaipu_user", "kuaipu_pass"]
    for key in required_keys:
        if key not in config:
            print(f"错误: 配置文件中缺少必要的登录信息: {key}")
            return None

    return config


def login(driver=None, return_driver=False):
    """执行登录流程

    Args:
        driver: 可选，复用已有的浏览器实例
        return_driver: 是否返回浏览器实例（供 shenpi 复用）

    Returns:
        如果 return_driver=True，返回 (success, driver)，否则返回 success
    """
    print("快普系统自动登录技能 (Selenium 版本)")
    print("=============================")

    # 读取配置
    config = read_config()
    if not config:
        if return_driver:
            return False, None
        return False

    kuaipu_url = config["kuaipu_url"]
    kuaipu_user = config["kuaipu_user"]
    kuaipu_pass = config["kuaipu_pass"]

    print(f"登录地址: {kuaipu_url}")
    print(f"用户名: {kuaipu_user}")
    print()

    # 初始化浏览器（如果没有传入）
    should_close_driver = False
    if driver is None:
        should_close_driver = not return_driver
        print("正在初始化浏览器...")
        try:
            # 初始化浏览器
            options = webdriver.ChromeOptions()
            # 无头模式，不显示浏览器窗口
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")  # 设置窗口大小

            # 尝试直接初始化 Chrome 驱动
            try:
                driver = webdriver.Chrome(options=options)
                print("浏览器初始化成功！")
            except Exception as e1:
                print(f"警告: 直接初始化 Chrome 驱动失败: {e1}")
                print("正在尝试使用 webdriver_manager...")
                # 设置 webdriver_manager 的缓存目录
                os.environ["WDM_LOCAL"] = "1"
                os.environ["WDM_CACHE"] = "/tmp/.wdm"
                # 使用 webdriver_manager 自动管理驱动
                from webdriver_manager.chrome import ChromeDriverManager

                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                print("浏览器初始化成功！")
        except Exception as e:
            print(f"错误: 初始化浏览器失败: {e}")
            if return_driver:
                return False, None
            return False

    try:
        # 打开登录页面
        print(f"正在打开快普登录页面: {kuaipu_url}")
        driver.get(kuaipu_url)

        # 等待页面加载
        time.sleep(3)
        print(f"当前页面: {driver.title}")
        print(f"当前URL: {driver.current_url}")

        # 保存登录页面截图（调试用）
        if VERBOSE:
            driver.save_screenshot(LOGIN_PAGE_SCREENSHOT)
            print(f"登录页面截图已保存: {LOGIN_PAGE_SCREENSHOT}")

        # 尝试找到登录表单元素
        print("正在查找登录表单元素...")

        # 尝试通过不同方式查找用户名输入框
        username_input = None
        try:
            username_input = driver.find_element(
                By.XPATH,
                "//input[contains(@placeholder, '用户名') or contains(@name, 'user') or contains(@id, 'user')]",
            )
        except Exception as e:
            print(f"找不到用户名输入框: {e}")
            return False

        # 尝试通过不同方式查找密码输入框
        password_input = None
        try:
            password_input = driver.find_element(
                By.XPATH,
                "//input[contains(@placeholder, '密码') or contains(@name, 'pass') or contains(@id, 'pass') or @type='password']",
            )
        except Exception as e:
            print(f"找不到密码输入框: {e}")
            return False

        # 尝试通过不同方式查找验证码输入框
        captcha_input = None
        try:
            captcha_input = driver.find_element(
                By.XPATH,
                "//input[contains(@placeholder, '验证码') or contains(@name, 'captcha') or contains(@id, 'captcha')]",
            )
        except Exception as e:
            print(f"找不到验证码输入框: {e}")
            return False

        # 尝试通过不同方式查找验证码图片
        captcha_image = None
        try:
            captcha_image = driver.find_element(
                By.XPATH,
                "//img[contains(@src, 'ValidateCodeHandler') or contains(@src, 'captcha') or contains(@src, 'verify') or contains(@src, 'code')]",
            )
        except Exception as e:
            # 尝试其他方式查找
            try:
                # 尝试通过标签名查找所有图片，然后筛选
                images = driver.find_elements(By.TAG_NAME, "img")
                for img in images:
                    try:
                        src = img.get_attribute("src")
                        if src and (
                            "ValidateCodeHandler" in src
                            or "captcha" in src.lower()
                            or "verify" in src.lower()
                            or "code" in src.lower()
                        ):
                            captcha_image = img
                            break
                    except Exception:
                        pass
            except Exception:
                pass

            if not captcha_image:
                print("错误: 找不到验证码图片")
                return False

        # 尝试通过不同方式查找登录按钮
        login_button = None
        try:
            login_button = driver.find_element(
                By.XPATH,
                "//button[contains(text(), '登录') or contains(@type, 'submit')] | //input[contains(@value, '登录') or @type='submit']",
            )
        except Exception as e:
            # 尝试其他方式查找
            try:
                # 尝试查找所有按钮元素
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    try:
                        text = btn.text
                        type_attr = btn.get_attribute("type")
                        if (
                            text
                            and ("登录" in text or "submit" in text.lower())
                            or type_attr == "submit"
                        ):
                            login_button = btn
                            break
                    except Exception:
                        pass
            except Exception:
                pass

            # 如果还是找不到，尝试查找所有输入元素
            if not login_button:
                try:
                    inputs = driver.find_elements(By.TAG_NAME, "input")
                    for input_elem in inputs:
                        try:
                            value = input_elem.get_attribute("value")
                            type_attr = input_elem.get_attribute("type")
                            if (
                                (
                                    value
                                    and ("登录" in value or "submit" in value.lower())
                                )
                                or type_attr == "submit"
                                or type_attr == "image"
                            ):
                                login_button = input_elem
                                break
                        except Exception:
                            pass
                except Exception:
                    pass

            if not login_button:
                print("错误: 找不到登录按钮")
                return False

        # 填写用户名和密码
        print(f"正在填写用户名: {kuaipu_user}")
        username_input.clear()
        username_input.send_keys(kuaipu_user)

        print("正在填写密码: ********")
        password_input.clear()
        password_input.send_keys(kuaipu_pass)

        # 处理验证码
        print("正在处理验证码...")

        # 保存验证码图片
        try:
            captcha_image.screenshot(CAPTCHA_IMAGE)
            print(f"验证码图片已保存到: {CAPTCHA_IMAGE}")
        except Exception as e:
            print(f"错误: 保存验证码图片失败: {e}")
            return False

        # 使用 ddddocr 识别验证码
        print("正在识别验证码...")
        captcha_code = ""
        try:
            # 参考用户提供的示例代码
            import ddddocr
            # 初始化OCR对象
            ocr = ddddocr.DdddOcr()
            # 读取图片
            with open(CAPTCHA_IMAGE, "rb") as f:
                image = f.read()
            # 识别图片
            captcha_code = ocr.classification(image)
            print(f"识别到的验证码: {captcha_code}")
        except Exception as e:
            print(f"错误: 验证码识别失败: {e}")
            import traceback
            traceback.print_exc()
            return False

        if not captcha_code:
            print("错误: 验证码识别结果为空")
            return False

        # 填写验证码
        print(f"正在填写验证码: {captcha_code}")
        captcha_input.clear()
        captcha_input.send_keys(captcha_code)

        # 提交登录表单
        print("正在提交登录表单...")
        # 保存提交前的页面状态
        before_submit_url = driver.current_url
        print(f"提交前URL: {before_submit_url}")

        # 点击登录按钮
        login_button.click()

        # 等待页面跳转
        print("等待页面跳转...")
        time.sleep(5)

        # 检查是否有alert弹窗
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"警告: 出现弹窗: {alert_text}")
            alert.accept()
            print("已关闭弹窗")
        except:
            # 没有弹窗是正常情况，不需要打印
            pass

        # 检查登录状态
        print("正在检查登录状态...")
        print(f"当前页面: {driver.title}")
        print(f"当前URL: {driver.current_url}")

        # 保存登录结果截图（调试用）
        if VERBOSE:
            driver.save_screenshot(LOGIN_RESULT_SCREENSHOT)
            print(f"登录结果截图已保存: {LOGIN_RESULT_SCREENSHOT}")

        # 检查页面源代码，看看是否有登录失败的提示
        try:
            page_source = driver.page_source
            # 保存页面源代码到文件，便于分析
            if VERBOSE:
                with open(LOGIN_RESULT_HTML, "w", encoding="utf-8") as f:
                    f.write(page_source)
                print(f"登录结果页面源代码已保存: {LOGIN_RESULT_HTML}")

            # 检查页面中是否有错误提示
            if (
                "错误" in page_source
                or "失败" in page_source
                or "验证码" in page_source
            ):
                print("页面中可能包含登录失败的提示")
        except Exception as e:
            print(f"获取页面源代码失败: {e}")

        # 统一检查登录状态
        login_success = False
        page_source = driver.page_source

        # 检查是否在 wincheck 页面且包含成功标志
        if "wincheck" in driver.current_url.lower():
            if (
                "successful.png" in page_source
                or "点击进入" in page_source
                or "ChkWin()" in page_source
            ):
                login_success = True
                print("登录成功! 页面显示登录成功标志")
        # 检查是否已经跳转到非登录页面
        elif "login" not in driver.current_url.lower():
            login_success = True
            print("登录成功! 已跳转到新页面")
        else:
            print("登录失败: 仍在登录页面")
            return False

        # 如果登录成功，尝试访问主页面并保存 cookies
        if login_success:
            try:
                main_url = kuaipu_url + "/WebEnterprise/newmain.aspx"
                print(f"正在访问主页面: {main_url}")
                driver.get(main_url)
                time.sleep(3)
                print(f"主页面URL: {driver.current_url}")
                print(f"主页面标题: {driver.title}")

                # 保存主页面截图（调试用）
                if VERBOSE:
                    driver.save_screenshot(MAIN_PAGE_SCREENSHOT)
                    print(f"主页面截图已保存: {MAIN_PAGE_SCREENSHOT}")
            except Exception as e:
                print(f"访问主页面失败: {e}")

            # 保存 cookies（只保存一次）
            try:
                with open(COOKIE_FILE, "wb") as f:
                    pickle.dump(driver.get_cookies(), f)
                print("登录状态已保存")
            except Exception as e:
                print(f"保存登录状态失败: {e}")

            if return_driver:
                return True, driver
            return True

        if return_driver:
            return False, driver
        return False

    except Exception as e:
        print(f"错误: 登录过程中发生异常: {e}")
        # 保存错误截图
        try:
            driver.save_screenshot(LOGIN_ERROR_SCREENSHOT)
            print(f"错误截图已保存到: {LOGIN_ERROR_SCREENSHOT}")
        except:
            pass

        if return_driver:
            return False, driver
        return False
    finally:
        # 只有当不需要返回 driver 时才关闭浏览器
        if should_close_driver and driver:
            print("正在关闭浏览器...")
            driver.quit()


def status():
    """查看登录状态"""
    print("正在检查登录状态...")

    # 检查是否存在 cookies 文件
    if not os.path.exists(COOKIE_FILE):
        print("未找到登录状态文件")
        print("状态: 未登录")
        return

    # 读取配置
    config = read_config()
    if not config:
        print("无法读取配置文件")
        print("状态: 未登录")
        return

    kuaipu_url = config["kuaipu_url"]
    main_url = kuaipu_url + "/WebEnterprise/newmain.aspx"

    # 初始化浏览器
    print("正在初始化浏览器...")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")  # 设置窗口大小

        try:
            driver = webdriver.Chrome(options=options)
            print("浏览器初始化成功！")
        except Exception as e1:
            print(f"警告: 直接初始化 Chrome 驱动失败: {e1}")
            print("正在尝试使用 webdriver_manager...")
            os.environ["WDM_LOCAL"] = "1"
            os.environ["WDM_CACHE"] = "/tmp/.wdm"
            from webdriver_manager.chrome import ChromeDriverManager

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            print("浏览器初始化成功！")
    except Exception as e:
        print(f"错误: 初始化浏览器失败: {e}")
        print("状态: 未登录")
        return

    try:
        # 访问主页面
        print(f"正在访问主页面: {main_url}")
        driver.get(main_url)
        time.sleep(2)

        # 加载 cookies
        print("正在加载登录状态...")
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)

        for cookie in cookies:
            driver.add_cookie(cookie)

        # 重新访问主页面
        driver.get(main_url)
        time.sleep(3)

        print(f"当前页面: {driver.title}")
        print(f"当前URL: {driver.current_url}")

        # 检查是否登录成功
        if "newmain" in driver.current_url or "main" in driver.current_url:
            print("状态: 已登录")
        else:
            print("状态: 未登录")

    except Exception as e:
        print(f"错误: 检查登录状态失败: {e}")
        print("状态: 未登录")
    finally:
        print("正在关闭浏览器...")
        driver.quit()


def logout():
    """退出登录"""
    print("正在退出登录...")

    # 删除 cookies 文件
    if os.path.exists(COOKIE_FILE):
        try:
            os.remove(COOKIE_FILE)
            print(f"已删除登录状态文件: {COOKIE_FILE}")
        except Exception as e:
            print(f"错误: 删除登录状态文件失败: {e}")
    else:
        print("未找到登录状态文件")

    print("已退出登录")


def shenpi():
    """访问审批中心页面并提取业务审批列表"""
    print("快普系统审批中心技能")
    print("=====================")

    # 读取配置
    config = read_config()
    if not config:
        return False

    kuaipu_url = config["kuaipu_url"]
    main_url = kuaipu_url + "/WebEnterprise/newmain.aspx"

    driver = None
    try:
        # 检查是否存在 cookies 文件，如果不存在则先登录
        if not os.path.exists(COOKIE_FILE):
            print("未找到登录状态，正在执行登录...")
            success, driver = login(return_driver=True)
            if not success:
                print("登录失败，无法访问审批中心")
                return False
        else:
            # 初始化浏览器并加载现有 cookies
            print("正在初始化浏览器...")
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")

                try:
                    driver = webdriver.Chrome(options=options)
                except Exception as e1:
                    print(f"警告: 直接初始化 Chrome 驱动失败: {e1}")
                    print("正在尝试使用 webdriver_manager...")
                    os.environ["WDM_LOCAL"] = "1"
                    os.environ["WDM_CACHE"] = "/tmp/.wdm"
                    from webdriver_manager.chrome import ChromeDriverManager

                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                print(f"错误: 初始化浏览器失败: {e}")
                return False

            # 访问主页面并加载 cookies
            print(f"正在访问主页面: {main_url}")
            driver.get(main_url)
            time.sleep(5)  # 增加等待时间

            try:
                with open(COOKIE_FILE, "rb") as f:
                    cookies = pickle.load(f)

                driver.delete_all_cookies()
                for cookie in cookies:
                    if "expiry" in cookie:
                        del cookie["expiry"]
                    driver.add_cookie(cookie)

                driver.get(main_url)
                time.sleep(5)  # 增加等待时间
                print(f"当前页面: {driver.title}")
            except Exception as e:
                print(f"加载登录状态失败: {e}，重新登录...")
                if driver:
                    driver.quit()
                success, driver = login(return_driver=True)
                if not success:
                    print("登录失败，无法访问审批中心")
                    return False

        # 保存主页面截图（调试用）
        if VERBOSE:
            driver.save_screenshot(MAIN_PAGE_SCREENSHOT)
            print(f"主页面截图已保存: {MAIN_PAGE_SCREENSHOT}")

        # 首先查找主页上的"业务催办"方框
        print("\n正在查找主页上的业务催办方框...")
        
        # 保存主页面HTML用于调试
        with open(MAIN_PAGE_HTML, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"主页面HTML已保存到: {MAIN_PAGE_HTML}")

        # 1. 查找包含"业务催办"的元素
        business_reminder_elements = driver.find_elements(
            By.XPATH, "//*[contains(text(), '业务催办')]"
        )
        print(f"找到 {len(business_reminder_elements)} 个包含'业务催办'的元素")

        # 2. 尝试查找业务催办方框（通常是一个包含业务催办标题的容器）
        business_reminder_box = None
        
        # 查找包含"业务催办"的容器元素
        try:
            # 查找包含"业务催办"文本的整个item容器（使用更精确的class选择器）
            business_reminder_box = driver.find_element(
                By.XPATH, "//div[contains(@class, 'item') and @title='业务催办']"
            )
            print("找到业务催办方框")
        except Exception as e:
            print(f"查找业务催办方框失败: {e}")
            
            # 尝试其他方式查找
            try:
                # 查找所有包含item的元素
                items = driver.find_elements(
                    By.XPATH, "//div[contains(@class, 'item')]"
                )
                print(f"找到 {len(items)} 个包含item的元素")
                
                for i, item in enumerate(items):
                    try:
                        title = item.get_attribute('title')
                        if title == "业务催办":
                            business_reminder_box = item
                            print(f"在item {i + 1} 中找到业务催办")
                            break
                    except Exception as e:
                        pass
            except Exception as e:
                print(f"尝试其他方式查找业务催办方框失败: {e}")
            
            # 再尝试一种方式：通过文本内容查找
            if not business_reminder_box:
                try:
                    # 查找包含"业务催办"文本的元素，然后找到其父级的容器
                    title_elem = driver.find_element(
                        By.XPATH, "//*[contains(text(), '业务催办')]"
                    )
                    # 找到包含这个标题的容器
                    business_reminder_box = title_elem.find_element(
                        By.XPATH, "ancestor::div[contains(@class, 'item')]"
                    )
                    print("通过文本内容找到业务催办方框")
                except Exception as e:
                    print(f"通过文本内容查找业务催办方框失败: {e}")
            
            # 最后尝试一种方式：直接查找包含业务催办文本的容器
            if not business_reminder_box:
                try:
                    # 直接查找包含业务催办文本的容器
                    business_reminder_box = driver.find_element(
                        By.XPATH, "//*[contains(text(), '业务催办')]/ancestor::div[contains(@class, 'item')]"
                    )
                    print("通过直接查找找到业务催办方框")
                except Exception as e:
                    print(f"通过直接查找业务催办方框失败: {e}")

        # 提取业务催办信息
        if business_reminder_box:
            print("\n正在提取业务催办信息...")
            
            # 保存业务催办方框的HTML
            business_reminder_html = business_reminder_box.get_attribute('outerHTML')
            with open(os.path.join(TMP_DIR, "business_reminder.html"), "w", encoding="utf-8") as f:
                f.write(business_reminder_html)
            print("业务催办方框HTML已保存到: tmp/business_reminder.html")
            
            # 尝试提取催办项目
            try:
                # 查找催办项目列表（更精确的XPath）
                reminder_items = business_reminder_box.find_elements(
                    By.XPATH, ".//div[@class='content-panel']//li"
                )
                print(f"找到 {len(reminder_items)} 个可能的催办项目")
                
                # 提取催办项目信息
                reminder_list = []
                
                if reminder_items:
                    for item in reminder_items:
                        try:
                            # 提取主题和时间
                            content_elem = item.find_element(By.XPATH, ".//span[@class='contnet']")
                            time_elem = item.find_element(By.XPATH, ".//span[@class='time']")
                            subject = content_elem.text.strip()
                            time_str = time_elem.text.strip()
                            reminder_list.append((subject, time_str))
                        except Exception as e:
                            # 如果无法提取详细信息，尝试直接获取文本
                            try:
                                item_text = item.text.strip()
                                if item_text:
                                    # 尝试从文本中分离主题和时间
                                    lines = item_text.split('\n')
                                    if len(lines) >= 2:
                                        subject = lines[0].strip()
                                        time_str = lines[1].strip()
                                        reminder_list.append((subject, time_str))
                            except:
                                pass
                else:
                    # 尝试直接提取方框内的所有文本
                    box_text = business_reminder_box.text
                    # 处理文本，提取催办项目
                    import re
                    lines = box_text.split('\n')
                    if len(lines) > 1:
                        # 跳过第一行（标题）
                        i = 0
                        while i < len(lines) - 1:
                            i += 1
                            line = lines[i].strip()
                            if line:
                                # 检查是否是主题行
                                if not re.match(r'\d{4}-\d{2}-\d{2}', line):
                                    subject = line
                                    # 查找下一行是否是日期
                                    if i + 1 < len(lines):
                                        next_line = lines[i + 1].strip()
                                        if re.match(r'\d{4}-\d{2}-\d{2}', next_line):
                                            time_str = next_line
                                            i += 1
                                        else:
                                            time_str = ""
                                    else:
                                        time_str = ""
                                    reminder_list.append((subject, time_str))
                
                # 处理并显示催办列表
                if reminder_list:
                    print("\n业务催办列表:")
                    print("=====================")
                    
                    import re
                    for i, (subject, time_str) in enumerate(reminder_list, 1):
                        print(f"{i}. 主题: {subject}")
                        if time_str:
                            print(f"   时间: {time_str}")
                        
                        # 提取最后中文括号内的名字作为当前审批人
                        match = re.search(r'【([^】]+)】$', subject)
                        if match:
                            approver = match.group(1)
                            print(f"   当前审批人: {approver}")
                        print("---")
                else:
                    print("\n业务催办列表:")
                    print("=====================")
                    print("我的所有申请全部通过了")
            except Exception as e:
                print(f"提取业务催办信息失败: {e}")
        else:
            print("未找到业务催办方框，尝试访问审批中心...")
            
            # 尝试访问审批中心
            print("\n正在访问审批中心...")

            # 首先，打印页面中所有的链接，以便我们了解页面结构
            print("\n=== 页面中找到的链接 ===")
            links = driver.find_elements(By.TAG_NAME, "a")
            print(f"找到 {len(links)} 个链接元素")
            shenpi_links = []

            # 专门查找右上角的审批中心图标
            print("\n=== 专门查找右上角的审批中心图标 ===")

            # 1. 查找所有可能的审批中心元素（包括没有文本但有title属性的图标）
            for i, link in enumerate(links):
                try:
                    text = link.text.strip()
                    href = link.get_attribute("href")
                    title = link.get_attribute("title") or link.get_attribute("alt") or ""

                    if text or href or title:
                        print(f"链接 {i + 1}: 文本='{text}', 标题='{title}', href='{href}'")

                        # 收集可能的审批中心链接
                        is_shenpi_link = False

                        # 检查文本是否包含审批相关关键词
                        if text and ("审批" in text or "业务" in text):
                            is_shenpi_link = True
                        # 检查href是否包含审批相关关键词
                        elif href and (
                            "shenpi" in href.lower()
                            or "approve" in href.lower()
                            or "workflow" in href.lower()
                        ):
                            is_shenpi_link = True
                        # 检查title/alt属性是否包含审批相关关键词
                        elif title and ("审批" in title or "业务" in title):
                            is_shenpi_link = True

                        if is_shenpi_link:
                            shenpi_links.append((text or title, href, link))
                            print(f"  -> 标记为审批中心链接")
                except Exception as e:
                    print(f"获取链接 {i + 1} 属性失败: {e}")

            # 2. 尝试通过XPath查找右上角的元素
            try:
                print("\n=== 尝试通过XPath查找右上角元素 ===")

                # 专门查找审批中心图标（根据HTML结构）
                print("\n=== 专门查找审批中心图标 ===")
                # 查找带有title="审批中心"的元素
                approval_center_elements = driver.find_elements(
                    By.XPATH, "//*[@title='审批中心']"
                )
                print(f"找到 {len(approval_center_elements)} 个带有title='审批中心'的元素")

                for i, elem in enumerate(approval_center_elements):
                    try:
                        print(
                            f"审批中心元素 {i + 1}: 标签={elem.tag_name}, id={elem.get_attribute('id')}"
                        )
                        # 检查是否是li元素，并且有nav-action类
                        if elem.tag_name == "li" and "nav-action" in elem.get_attribute(
                            "class"
                        ):
                            # 尝试找到其中的链接或直接点击元素
                            link = None
                            # 检查元素内部是否有链接
                            links_in_elem = elem.find_elements(By.TAG_NAME, "a")
                            if links_in_elem:
                                link = links_in_elem[0]
                                print(f"  -> 找到内部链接: {link.get_attribute('href')}")
                                shenpi_links.append(
                                    ("审批中心", link.get_attribute("href"), link)
                                )
                            else:
                                # 直接添加元素本身（可能需要直接点击）
                                print(f"  -> 直接添加元素本身")
                                shenpi_links.append(("审批中心", "", elem))
                    except Exception as e:
                        print(f"获取审批中心元素 {i + 1} 属性失败: {e}")

                # 查找id="liWorkFlow"的元素（审批中心图标）
                print("\n=== 尝试查找id=liWorkFlow的元素 ===")
                try:
                    li_workflow = driver.find_element(By.ID, "liWorkFlow")
                    print(
                        f"找到id=liWorkFlow的元素: 标签={li_workflow.tag_name}, class={li_workflow.get_attribute('class')}"
                    )
                    shenpi_links.append(("审批中心", "", li_workflow))
                    print(f"  -> 标记为审批中心链接")
                except Exception as e:
                    print(f"查找id=liWorkFlow的元素失败: {e}")

                # 查找可能在右上角的元素
                right_top_elements = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'top') or contains(@class, 'header') or contains(@class, 'nav') or contains(@class, 'menu')]//*[contains(@class, 'icon') or contains(@class, 'btn') or contains(@class, 'button')]",
                )
                print(f"找到 {len(right_top_elements)} 个可能在右上角的元素")

                for i, elem in enumerate(right_top_elements):
                    try:
                        # 检查是否是链接
                        link = None
                        if elem.tag_name == "a":
                            link = elem
                        else:
                            # 使用find_elements避免抛出异常
                            links_in_elem = elem.find_elements(By.XPATH, ".//a")
                            if links_in_elem:
                                link = links_in_elem[0]

                        if link:
                            href = link.get_attribute("href")
                            title = (
                                link.get_attribute("title")
                                or link.get_attribute("alt")
                                or ""
                            )
                            text = link.text.strip()

                            print(
                                f"右上角元素 {i + 1}: 文本='{text}', 标题='{title}', href='{href}'"
                            )

                            # 检查是否包含审批相关关键词
                            is_shenpi_link = False
                            if text and ("审批" in text or "业务" in text):
                                is_shenpi_link = True
                            elif href and (
                                "shenpi" in href.lower()
                                or "approve" in href.lower()
                                or "workflow" in href.lower()
                            ):
                                is_shenpi_link = True
                            elif title and ("审批" in title or "业务" in title):
                                is_shenpi_link = True

                            if is_shenpi_link:
                                shenpi_links.append((text or title, href, link))
                                print(f"  -> 标记为审批中心链接")
                    except Exception as e:
                        print(f"获取右上角元素 {i + 1} 属性失败: {e}")
            except Exception as e:
                print(f"查找右上角元素失败: {e}")

            # 初始化变量
            found_shenpi_page = False

            # 尝试点击审批中心链接
            if shenpi_links:
                print(f"\n找到 {len(shenpi_links)} 个可能的审批中心链接")
                for i, (text, href, elem) in enumerate(shenpi_links):
                    print(f"尝试点击审批中心元素 {i + 1}: {text}")
                    try:
                        # 先滚动到元素位置
                        driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                            elem,
                        )
                        time.sleep(1)

                        # 点击元素
                        elem.click()
                        time.sleep(5)  # 增加等待时间

                        # 检查是否有新窗口打开
                        window_handles = driver.window_handles
                        if len(window_handles) > 1:
                            # 切换到新窗口
                            driver.switch_to.window(window_handles[-1])
                            print("切换到新窗口")

                        # 检查是否有iframe
                        try:
                            iframes = driver.find_elements(By.TAG_NAME, "iframe")
                            if iframes:
                                print(f"找到 {len(iframes)} 个iframe")
                                for i, iframe in enumerate(iframes):
                                    try:
                                        driver.switch_to.frame(iframe)
                                        print(f"切换到iframe {i + 1}")
                                        # 检查是否在审批中心页面
                                        if (
                                            "审批" in driver.title
                                            or "审批" in driver.page_source
                                        ):
                                            break
                                    except:
                                        # iframe 不存在或无法切换是正常情况
                                        driver.switch_to.default_content()
                        except:
                            # 没有 iframe 是正常情况
                            pass

                        print(f"当前页面: {driver.title}")
                        print(f"当前URL: {driver.current_url}")

                        # 检查是否成功进入审批中心
                        if (
                            "审批" in driver.title
                            or "shenpi" in driver.current_url.lower()
                            or "approve" in driver.current_url.lower()
                            or "workflow" in driver.current_url.lower()
                            or "审批" in driver.page_source
                        ):
                            found_shenpi_page = True
                            break
                    except:
                        # 点击失败，尝试通过URL直接访问
                        if href:
                            print(f"尝试通过URL直接访问: {href}")
                            driver.get(href)
                            time.sleep(5)  # 增加等待时间
                            print(f"当前页面: {driver.title}")
                            print(f"当前URL: {driver.current_url}")

                            if (
                                "审批" in driver.title
                                or "shenpi" in driver.current_url.lower()
                                or "approve" in driver.current_url.lower()
                                or "workflow" in driver.current_url.lower()
                            ):
                                found_shenpi_page = True
                                break

                if not found_shenpi_page:
                    print("未成功进入审批中心，尝试使用默认路径")
            else:
                print("未找到可能的审批中心链接，尝试使用默认路径")

            # 尝试一些常见的审批中心路径
            if not found_shenpi_page:
                common_shenpi_paths = [
                    "/WebEnterprise/COM/WorkFlow/OA_V_WorkFlowBusinessApprovalList.aspx",  # 业务审批
                    "/WebEnterprise/COM/WorkFlow/OA_V_WorkFlowBussinessReminderList.aspx",  # 业务催办
                    "/WebEnterprise/workflow.aspx",
                    "/WebEnterprise/shenpi.aspx",
                    "/WebEnterprise/approve.aspx",
                    "/WebEnterprise/business.aspx",
                ]

                for path in common_shenpi_paths:
                    shenpi_url = kuaipu_url + path
                    print(f"尝试访问: {shenpi_url}")
                    try:
                        driver.get(shenpi_url)
                        time.sleep(5)  # 增加等待时间
                        print(f"当前页面: {driver.title}")
                        print(f"当前URL: {driver.current_url}")

                        if (
                            "审批" in driver.title
                            or "shenpi" in driver.current_url.lower()
                            or "approve" in driver.current_url.lower()
                        ):
                            found_shenpi_page = True
                            break
                    except Exception as e:
                        # 路径不存在，尝试下一个
                        print(f"访问路径失败: {path}, 错误: {e}")
                        pass

        # 保存审批中心页面截图
        driver.save_screenshot(SHENPI_PAGE_SCREENSHOT)
        print(f"审批中心页面截图已保存到: {SHENPI_PAGE_SCREENSHOT}")

        # 保存审批中心页面HTML用于调试
        with open(SHENPI_PAGE_HTML, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"审批中心页面HTML已保存到: {SHENPI_PAGE_HTML}")

        # 尝试提取业务审批列表
        print("\n正在提取业务审批列表...")

        # 尝试点击"业务审批"选项卡
        try:
            print("\n=== 尝试点击业务审批选项卡 ===")
            # 查找包含"业务审批"的元素
            business_approval_elements = driver.find_elements(
                By.XPATH, "//*[contains(text(), '业务审批')]"
            )
            print(f"找到 {len(business_approval_elements)} 个包含'业务审批'的元素")

            for i, elem in enumerate(business_approval_elements):
                try:
                    print(f"尝试点击业务审批元素 {i + 1}")
                    # 滚动到元素位置
                    driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                        elem,
                    )
                    time.sleep(1)
                    # 点击元素
                    elem.click()
                    time.sleep(3)  # 等待页面加载
                    print("点击业务审批选项卡成功")
                    break
                except:
                    # 点击失败，尝试下一个元素
                    pass
        except:
            # 没有找到业务审批选项卡
            pass

        # 首先，打印页面中所有的表格，以便我们了解页面结构
        print("\n=== 页面中找到的表格 ===")
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"找到 {len(tables)} 个表格元素")

        table_found = False
        # 遍历所有表格，尝试找到审批列表
        for i, table in enumerate(tables):
            try:
                # 尝试获取表格的所有行
                rows = table.find_elements(By.TAG_NAME, "tr")
                print(f"表格 {i + 1}: {len(rows)} 行")

                # 只处理有足够数据的表格（至少3行：表头、数据行、可能的合计行）
                if len(rows) >= 2:
                    # 尝试获取表头
                    headers = []
                    # 首先尝试 th 作为表头
                    header_cells = rows[0].find_elements(By.TAG_NAME, "th")
                    if header_cells:
                        headers = [h.text.strip() for h in header_cells]
                        print(f"表格 {i + 1} 表头 (th): {headers}")
                    else:
                        # 尝试 td 作为表头
                        header_cells = rows[0].find_elements(By.TAG_NAME, "td")
                        if header_cells:
                            headers = [h.text.strip() for h in header_cells]
                            print(f"表格 {i + 1} 表头 (td): {headers}")

                    # 跳过选项卡表格（表头包含多个选项卡名称）
                    if headers and any(
                        "审批中心" in h or "业务催办" in h or "督查督办" in h
                        for h in headers
                    ):
                        print(f"表格 {i + 1} 是选项卡表格，跳过")
                        continue

                    # 检查是否是审批列表表格
                    # 放宽条件，只要表格有足够的列且包含相关关键词就尝试提取
                    if len(headers) > 1:
                        # 检查表头是否包含审批相关关键词
                        has_approval_keywords = any(
                            "主题" in h
                            or "标题" in h
                            or "业务" in h
                            or "状态" in h
                            or "办理" in h
                            or "审批" in h
                            for h in headers
                        )

                        if has_approval_keywords:
                            print(f"\n找到审批列表表格 (表格 {i + 1})")
                            table_found = True

                            # 提取数据
                            print("\n业务审批列表:")
                            print("=====================")

                            # 遍历数据行
                            data_found = False
                            for j, row in enumerate(rows[1:], 1):
                                try:
                                    cells = row.find_elements(By.TAG_NAME, "td")
                                    if len(cells) > 1:
                                        # 提取主题（第一列）
                                        subject = cells[0].text.strip()
                                        # 尝试找到办理情况列
                                        status = ""

                                        # 优先根据表头查找状态列
                                        if headers:
                                            for k, header in enumerate(headers):
                                                if k < len(cells) and (
                                                    "状态" in header
                                                    or "办理" in header
                                                    or "情况" in header
                                                    or "审批" in header
                                                ):
                                                    status = cells[k].text.strip()
                                                    break

                                        # 如果没有找到，尝试使用最后一列
                                        if not status and len(cells) > 1:
                                            status = cells[-1].text.strip()

                                        # 只有当主题不为空时才打印
                                        if (
                                            subject
                                            and not subject.startswith("合计")
                                            and not subject.startswith("总计")
                                        ):
                                            print(f"{j}. 主题: {subject}")
                                            print(f"   办理情况: {status}")
                                            print("---")
                                            data_found = True
                                except Exception as e:
                                    print(f"提取行 {j} 失败: {e}")

                                # 只显示前 10 条
                                if j >= 10:
                                    print("... 更多数据省略 ...")
                                    break

                            # 如果找到数据，停止查找其他表格
                            if data_found:
                                break
                        else:
                            # 即使表头没有关键词，也尝试提取数据（可能是自定义列名）
                            print(f"\n尝试从表格 {i + 1} 提取数据（表头无关键词）")

                            # 遍历数据行
                            data_found = False
                            for j, row in enumerate(rows[1:], 1):
                                try:
                                    cells = row.find_elements(By.TAG_NAME, "td")
                                    if len(cells) > 1:
                                        # 提取主题（第一列）
                                        subject = cells[0].text.strip()
                                        # 尝试使用第二列作为状态
                                        status = (
                                            cells[1].text.strip()
                                            if len(cells) > 1
                                            else ""
                                        )

                                        # 只有当主题不为空时才打印
                                        if (
                                            subject
                                            and not subject.startswith("合计")
                                            and not subject.startswith("总计")
                                        ):
                                            print(f"{j}. 主题: {subject}")
                                            print(f"   办理情况: {status}")
                                            print("---")
                                            data_found = True
                                except Exception as e:
                                    print(f"提取行 {j} 失败: {e}")

                                # 只显示前 10 条
                                if j >= 10:
                                    print("... 更多数据省略 ...")
                                    break

                            # 如果找到数据，停止查找其他表格
                            if data_found:
                                table_found = True
                                break
            except Exception as e:
                print(f"处理表格 {i + 1} 失败: {e}")

        # 如果没有找到表格，尝试其他方式提取数据
        if not table_found:
            print("\n未找到审批列表表格，尝试其他方式提取数据...")

            # 尝试查找所有可能的审批项
            try:
                # 1. 首先尝试查找所有包含审批信息的元素
                print("1. 尝试查找包含审批信息的元素...")
                items = driver.find_elements(
                    By.XPATH,
                    "//*[contains(@class, 'item') or contains(@class, 'list') or contains(@class, 'row') or contains(@class, '审批') or contains(@class, 'business') or contains(@class, 'workflow')]",
                )
                print(f"找到 {len(items)} 个可能的审批项")

                if items:
                    print("\n业务审批列表:")
                    print("=====================")

                    data_found = False
                    for i, item in enumerate(items, 1):
                        try:
                            # 提取主题
                            subject = ""
                            try:
                                # 尝试多种方式查找主题元素
                                subject_elem = item.find_element(
                                    By.XPATH,
                                    ".//*[contains(@class, 'subject') or contains(@class, 'title') or contains(@class, 'theme') or starts-with(name(), 'h') or contains(@class, 'name')]",
                                )
                                subject = subject_elem.text.strip()
                            except Exception as e:
                                # 尝试获取所有文本
                                item_text = item.text.strip()
                                if item_text:
                                    # 取第一行作为主题
                                    lines = item_text.split("\n")
                                    subject = lines[0].strip() if lines else ""

                            # 提取状态
                            status = ""
                            try:
                                # 尝试多种方式查找状态元素
                                status_elem = item.find_element(
                                    By.XPATH,
                                    ".//*[contains(@class, 'status') or contains(@class, 'state') or contains(@class, 'result') or contains(@class, 'status')]",
                                )
                                status = status_elem.text.strip()
                            except Exception as e:
                                # 尝试从文本中提取
                                item_text = item.text.strip()
                                if item_text:
                                    lines = item_text.split("\n")
                                    for line in lines[1:]:  # 从第二行开始查找状态
                                        line = line.strip()
                                        if (
                                            "状态" in line
                                            or "办理" in line
                                            or "结果" in line
                                            or "审批" in line
                                        ):
                                            status = line
                                            break

                            # 只有当主题不为空时才打印
                            if subject:
                                print(f"{i}. 主题: {subject}")
                                print(f"   办理情况: {status}")
                                print("---")
                                data_found = True
                        except Exception as e:
                            print(f"提取审批项 {i} 失败: {e}")

                        # 只显示前 10 条
                        if i >= 10:
                            print("... 更多数据省略 ...")
                            break

                    if data_found:
                        table_found = True

                # 2. 如果第一种方式失败，尝试查找所有链接元素
                if not table_found:
                    print("\n2. 尝试查找包含审批信息的链接...")
                    links = driver.find_elements(By.TAG_NAME, "a")
                    approval_links = []

                    for link in links:
                        try:
                            text = link.text.strip()
                            href = link.get_attribute("href")
                            if (
                                text
                                and ("审批" in text or "业务" in text or "主题" in text)
                                and href
                            ):
                                approval_links.append((text, href))
                        except:
                            pass

                    print(f"找到 {len(approval_links)} 个可能的审批链接")

                    if approval_links:
                        print("\n业务审批列表:")
                        print("=====================")

                        for i, (text, href) in enumerate(approval_links[:10], 1):
                            print(f"{i}. 主题: {text}")
                            print(f"   链接: {href}")
                            print("---")

                        table_found = True

                # 3. 如果前两种方式都失败，尝试查找所有包含审批相关文本的元素
                if not table_found:
                    print("\n3. 尝试查找包含审批相关文本的所有元素...")
                    # 查找所有包含审批相关文本的元素
                    all_elements = driver.find_elements(
                        By.XPATH,
                        "//*[contains(text(), '审批') or contains(text(), '业务') or contains(text(), '主题')]",
                    )
                    print(f"找到 {len(all_elements)} 个包含审批相关文本的元素")

                    if all_elements:
                        print("\n业务审批列表:")
                        print("=====================")

                        for i, elem in enumerate(all_elements[:10], 1):
                            try:
                                text = elem.text.strip()
                                if text:
                                    print(f"{i}. 内容: {text}")
                                    print("---")
                            except Exception as e:
                                print(f"提取元素 {i} 失败: {e}")

                        table_found = True

                # 4. 如果所有方式都失败，尝试获取整个页面的文本并分析
                if not table_found:
                    print("\n4. 尝试分析整个页面文本...")
                    try:
                        page_text = driver.page_source
                        # 保存页面文本到文件，便于分析
                        with open(SHENPI_PAGE_TEXT, "w", encoding="utf-8") as f:
                            f.write(page_text)
                        print(f"页面文本已保存到: {SHENPI_PAGE_TEXT}")

                        # 简单分析页面文本，查找审批相关内容
                        print("\n页面文本分析完成，请查看保存的文件以了解页面结构")
                        print(
                            "\n提示: 根据实际页面结构，您可能需要修改shenpi函数以适应特定的页面布局"
                        )
                    except Exception as e:
                        print(f"分析页面文本失败: {e}")
            except Exception as e:
                print(f"尝试其他方式提取数据失败: {e}")
                import traceback

                traceback.print_exc()

        print("\n审批中心操作完成！")
        print("\n提示:")
        print("1. 所有页面截图和HTML文件已保存到项目目录")
        print("2. 请查看这些文件以了解实际的页面结构")
        print("3. 根据实际页面结构，您可能需要修改shenpi函数以适应特定的页面布局")
        return True

    except Exception as e:
        print(f"\n错误: 审批中心操作过程中发生异常: {e}")
        import traceback

        traceback.print_exc()
        # 保存错误截图
        try:
            driver.save_screenshot(SHENPI_ERROR_SCREENSHOT)
            print(f"错误截图已保存到: {SHENPI_ERROR_SCREENSHOT}")
        except:
            pass

        return False
    finally:
        print("\n正在关闭浏览器...")
        if driver:
            driver.quit()


def main():
    """主函数"""
    import sys

    # 清除临时文件夹
    clear_tmp_dir()

    if len(sys.argv) < 2:
        print("用法: kuaipu_login_selenium.py [login|status|logout|shenpi]")
        print()
        print("login   - 执行快普系统登录")
        print("status  - 查看登录状态")
        print("logout  - 退出登录")
        print("shenpi  - 访问审批中心并提取业务审批列表")
        return

    command = sys.argv[1]

    if command == "login":
        login()
    elif command == "status":
        status()
    elif command == "logout":
        logout()
    elif command == "shenpi":
        shenpi()
    else:
        print(f"错误: 未知命令: {command}")
        print("用法: kuaipu_login_selenium.py [login|status|logout|shenpi]")


if __name__ == "__main__":
    main()
