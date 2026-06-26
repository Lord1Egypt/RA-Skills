"""
浏览器控制模块 - 提供浏览器启动、导航、点击、输入等自动化功能
支持 Chromium、Firefox、Edge 等浏览器
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from typing import List, Dict, Optional
import base64
import time
import os

_driver = None
_element_map = {}
_element_counter = 0

GECKODRIVER_PATH = r"C:\Users\LukeNcCode\AppData\Local\Microsoft\WinGet\Packages\Mozilla.GeckoDriver_Microsoft.Winget.Source_8wekyb3d8bbwe\geckodriver.exe"


def _get_element_id() -> str:
    global _element_counter
    _element_counter += 1
    return f"elem_{_element_counter}"


def browser_start(browser: str = "chrome", headless: bool = True):
    global _driver, _element_map
    try:
        if browser.lower() == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            service = FirefoxService(executable_path=GECKODRIVER_PATH)
            _driver = webdriver.Firefox(service=service, options=options)
        elif browser.lower() == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=IsolateOrigins,site-per-process")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--ignore-certificate-errors")
            try:
                _driver = webdriver.Edge(options=options)
            except:
                _driver = webdriver.Edge()
        else:
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=IsolateOrigins,site-per-process")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--ignore-certificate-errors")
            try:
                _driver = webdriver.Chrome(options=options)
            except:
                _driver = webdriver.Chrome()
        
        _driver.set_page_load_timeout(30)
        _element_map = {}
        return {"success": True, "data": {"browser": browser, "headless": headless}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_close():
    global _driver, _element_map
    try:
        if _driver:
            _driver.quit()
        _driver = None
        _element_map = {}
        return {"success": True, "data": {"message": "Browser closed"}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_navigate(url: str):
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        _driver.get(url)
        return {"success": True, "data": {"url": url}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_info():
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        return {
            "success": True,
            "data": {"url": _driver.current_url, "title": _driver.title},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_elements():
    global _driver, _element_map
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        
        selectors = [
            (By.TAG_NAME, "a"),
            (By.TAG_NAME, "button"),
            (By.TAG_NAME, "input"),
            (By.TAG_NAME, "select"),
            (By.TAG_NAME, "textarea"),
            (By.CSS_SELECTOR, "[role='button']"),
            (By.CSS_SELECTOR, "[role='link']"),
            (By.TAG_NAME, "img"),
            # 淘宝/天猫购物车按钮 - 扩大扫描范围
            (By.CSS_SELECTOR, "div[class*='Wrapper']"),
            (By.CSS_SELECTOR, "span[class*='Wrapper']"),
            (By.CSS_SELECTOR, "div[class*='button']"),
            (By.CSS_SELECTOR, "span[class*='button']"),
            (By.CSS_SELECTOR, "div[class*='btn']"),
            (By.CSS_SELECTOR, "span[class*='btn']"),
            # 加号按钮 - 包括CSS modules的类名（带--）
            (By.CSS_SELECTOR, "div[class*='addWrapper']"),
            (By.CSS_SELECTOR, "span[class*='addWrapper']"),
            (By.CSS_SELECTOR, "[class*='addWrapper--']"),
            (By.CSS_SELECTOR, "i[class*='add']"),
            (By.CSS_SELECTOR, "span[class*='add']"),
            (By.CSS_SELECTOR, "div[class*='plus']"),
            (By.CSS_SELECTOR, "span[class*='plus']"),
            # 通用点击元素
            (By.TAG_NAME, "div"),
            (By.TAG_NAME, "span"),
        ]
        
        elements = []
        
        for by, sel in selectors:
            try:
                elems = _driver.find_elements(by, sel)
                for elem in elems:
                    try:
                        if not elem.is_displayed():
                            continue
                        
                        location = elem.location
                        size = elem.size
                        
                        if size["width"] < 3 or size["height"] < 3:
                            continue
                        
                        elem_id = _get_element_id()
                        _element_map[elem_id] = elem
                        
                        element_info = {
                            "id": elem_id,
                            "type": elem.tag_name if elem.tag_name in ['a', 'button', 'input', 'select', 'textarea', 'img'] else (sel.split('[')[0] if '[' in sel else sel),
                            "x": int(location["x"]),
                            "y": int(location["y"]),
                            "width": int(size["width"]),
                            "height": int(size["height"])
                        }
                        
                        try:
                            text = elem.text.strip()[:100]
                            if text:
                                element_info["text"] = text
                        except:
                            pass
                        
                        try:
                            if sel == "a":
                                element_info["href"] = elem.get_attribute("href")
                        except:
                            pass
                        
                        try:
                            attr_type = elem.get_attribute("type")
                            if attr_type and elem.tag_name == 'input':
                                element_info["type"] = attr_type
                            element_info["name"] = elem.get_attribute("name")
                            element_info["placeholder"] = elem.get_attribute("placeholder")
                            element_info["value"] = elem.get_attribute("value")
                            # 添加class属性以识别特定按钮
                            element_info["class"] = elem.get_attribute("class")
                        except:
                            pass
                        
                        elements.append(element_info)
                    except:
                        pass
            except:
                pass
        
        return {"success": True, "data": {"elements": elements}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_click(element: str = None, text: str = None, index: int = None, method: str = "auto"):
    global _driver, _element_map
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        
        elem = None
        
        if element and element in _element_map:
            elem = _element_map[element]
        elif text:
            # 首先尝试CSS选择器（用于class选择器等）
            if text.startswith(".") or text.startswith("#") or "[" in text:
                try:
                    elems = _driver.find_elements(By.CSS_SELECTOR, text)
                    if elems:
                        elem = elems[0] if index is None else elems[index] if index < len(elems) else None
                except:
                    pass
            if not elem:
                try:
                    elems = _driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
                    if not elems:
                        elems = _driver.find_elements(By.XPATH, f"//button[contains(@aria-label, '{text}')]")
                    if not elems:
                        elems = _driver.find_elements(By.XPATH, f"//input[@value='{text}']")
                    if not elems:
                        elems = _driver.find_elements(By.CSS_SELECTOR, f"*[contains(@placeholder, '{text}')]")
                    if not elems:
                        elems = _driver.find_elements(By.CSS_SELECTOR, f"a[href*='{text}']")
                    if elems:
                        elem = elems[0] if index is None else elems[index] if index < len(elems) else None
                except:
                    pass
        elif index is not None:
            elems = _driver.find_elements(By.CSS_SELECTOR, "a, button, input, select, textarea, [role='button'], [role='link']")
            elem = elems[index] if index < len(elems) else None
        
        if not elem:
            return {"success": False, "data": None, "error": "Element not found"}
        
        try:
            if method == "js":
                _driver.execute_script("arguments[0].click();", elem)
            elif method == "js_native":
                # 模拟真实鼠标点击 - 触发完整的鼠标事件链 (mousedown -> mouseup -> click)
                # 适用于有复杂事件监听的按钮（如电商网站的加号按钮）
                _driver.execute_script("""
                    var elem = arguments[0];
                    var rect = elem.getBoundingClientRect();
                    var x = rect.left + rect.width / 2;
                    var y = rect.top + rect.height / 2;
                    
                    // 创建鼠标事件
                    var mouseEvent = new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true,
                        view: window,
                        clientX: x,
                        clientY: y
                    });
                    
                    // 尝试多种点击方式
                    try {
                        elem.dispatchEvent(mouseEvent);
                    } catch(e) {
                        try { elem.click(); } catch(e2) {}
                    }
                """, elem)
            elif method == "action":
                from selenium.webdriver.common.action_chains import ActionChains
                ActionChains(_driver).move_to_element(elem).click().perform()
            else:
                try:
                    elem.click()
                except:
                    _driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                    time.sleep(0.2)
                    try:
                        elem.click()
                    except:
                        # 回退到 JS native 点击方式
                        _driver.execute_script("""
                            var elem = arguments[0];
                            var rect = elem.getBoundingClientRect();
                            var x = rect.left + rect.width / 2;
                            var y = rect.top + rect.height / 2;
                            var mouseEvent = new MouseEvent('click', {bubbles: true, cancelable: true, view: window, clientX: x, clientY: y});
                            elem.dispatchEvent(mouseEvent);
                        """, elem)
        except Exception as click_err:
            try:
                _driver.execute_script("arguments[0].click();", elem)
            except:
                return {"success": False, "data": None, "error": str(click_err)}
        
        return {"success": True, "data": {"element": element or text or str(index)}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_input(element: str = None, text: str = None, text_to_input: str = "", index: int = None):
    global _driver, _element_map
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        
        elem = None
        
        if element and element in _element_map:
            elem = _element_map[element]
        elif text:
            try:
                elems = _driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
                if elems:
                    elem = elems[0] if index is None else elems[index] if index < len(elems) else None
            except:
                pass
        elif index is not None:
            elems = _driver.find_elements(By.CSS_SELECTOR, "input, textarea, select")
            elem = elems[index] if index < len(elems) else None
        
        if not elem:
            return {"success": False, "data": None, "error": "Element not found"}
        
        elem.clear()
        elem.send_keys(text_to_input)
        return {"success": True, "data": {"element": element or text or str(index), "text": text_to_input}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_js(script: str):
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        
        result = _driver.execute_script(script)
        return {"success": True, "data": {"result": str(result)}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_screenshot():
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        
        screenshot_bytes = _driver.get_screenshot_as_png()
        base64_image = base64.b64encode(screenshot_bytes).decode("utf-8")
        return {"success": True, "data": {"image": base64_image}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_wait(element: str = None, text: str = None, timeout: int = 5000):
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        
        wait = WebDriverWait(_driver, timeout / 1000)
        
        if text:
            wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]")))
        elif element:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
        
        return {"success": True, "data": {"message": "Element found"}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_back():
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        _driver.back()
        return {"success": True, "data": {"url": _driver.current_url}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_forward():
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        _driver.forward()
        return {"success": True, "data": {"url": _driver.current_url}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_refresh():
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        _driver.refresh()
        return {"success": True, "data": {"url": _driver.current_url}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_scroll(direction: str = "down", amount: int = 500):
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        
        if direction == "up":
            _driver.execute_script(f"window.scrollBy(0, -{amount})")
        else:
            _driver.execute_script(f"window.scrollBy(0, {amount})")
        
        return {"success": True, "data": {"direction": direction, "amount": amount}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}


def browser_execute_script(script: str):
    """Execute custom JavaScript in the browser"""
    global _driver
    try:
        if not _driver:
            return {"success": False, "data": None, "error": "Browser not started"}
        
        result = _driver.execute_script(script)
        return {"success": True, "data": {"result": str(result)}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
