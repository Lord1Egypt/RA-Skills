#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动登录脚本 (支持图形验证码 OCR 识别 + 持久化会话 + 自动定位元素)
【强制使用 Google Chrome 浏览器】
用法: python3 openclaw_login.py <用户名> <密码> [--url <登录页URL>] [--debug] [--window-size WIDTH,HEIGHT]
若未提供 --url，则从环境变量 GJSW_LOGIN_URL 读取
"""

import argparse
import base64
import time
import sys
import os
import re
import subprocess
import socket
import shutil
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import ddddocr

# ========== 配置区域 ==========
USER_DATA_DIR = "./chrome_profile"
REMOTE_DEBUG_PORT = 9222
MAX_LOGIN_RETRIES = 5
AUTO_LOCATE_TIMEOUT = 5000

# 手动选择器配置（留空则使用自动定位）
MANUAL_USERNAME_SELECTOR = ""
MANUAL_PASSWORD_SELECTOR = ""
MANUAL_CAPTCHA_IMG_SELECTOR = ""
MANUAL_CAPTCHA_INPUT_SELECTOR = ""
MANUAL_LOGIN_BUTTON_SELECTOR = "div.form-btn"
# =============================


def find_element_auto(page, role_type, timeout=5000, debug=False):
    """自动定位元素"""
    try:
        if role_type == "username":
            for label in ["账号", "手机号", "用户名", "邮箱", "account", "username", "mobile"]:
                elem = page.get_by_label(label, exact=False).first
                if elem.count() > 0:
                    if debug: print(f"[自动定位] username 通过 label '{label}' 找到")
                    return elem
                elem = page.get_by_placeholder(re.compile(label, re.IGNORECASE)).first
                if elem.count() > 0:
                    if debug: print(f"[自动定位] username 通过 placeholder '{label}' 找到")
                    return elem
            for selector in ['input[name*="user"]', 'input[name*="account"]', 'input[name*="mobile"]', 'input[type="text"]']:
                elem = page.query_selector(selector)
                if elem:
                    if debug: print(f"[自动定位] username 通过 selector '{selector}' 找到")
                    return elem
        elif role_type == "password":
            elem = page.query_selector('input[type="password"]')
            if elem:
                if debug: print("[自动定位] password 通过 input[type=password] 找到")
                return elem
            elem = page.get_by_placeholder(re.compile("密码|password", re.IGNORECASE)).first
            if elem.count() > 0:
                if debug: print("[自动定位] password 通过 placeholder 找到")
                return elem
        elif role_type == "captcha_input":
            for selector in ['input[placeholder*="验证码"]', 'input[placeholder*="验证码"]',
                             'input[name*="captcha"]', 'input[name*="code"]', 'input[name*="verify"]']:
                elem = page.query_selector(selector)
                if elem:
                    if debug: print(f"[自动定位] captcha_input 通过 selector '{selector}' 找到")
                    return elem
        elif role_type == "captcha_img":
            for selector in ['img[alt*="验证码"]', 'img[src*="captcha"]', 'img[src*="verify"]',
                             '.captcha-img', '#captchaImg', 'img[class*="captcha"]']:
                elem = page.query_selector(selector)
                if elem:
                    if debug: print(f"[自动定位] captcha_img 通过 selector '{selector}' 找到")
                    return elem
            imgs = page.query_selector_all('img')
            for img in imgs:
                src = img.get_attribute('src') or ""
                if 'captcha' in src.lower() or 'verify' in src.lower() or 'code' in src.lower():
                    if debug: print("[自动定位] captcha_img 通过 src 关键字找到")
                    return img
                try:
                    box = img.bounding_box()
                    if box and 50 < box['width'] < 300 and 20 < box['height'] < 100:
                        if debug: print("[自动定位] captcha_img 通过尺寸找到")
                        return img
                except:
                    pass
        elif role_type == "login_button":
            for selector in ['div.form-btn', 'button:has-text("登录")', '.form-btn',
                             'form button:has-text("登录")', 'form input[type="submit"]',
                             '.login-form button:has-text("登录")', '.ant-btn-primary',
                             'button:has-text("登录")', 'input[type="submit"]']:
                elem = page.query_selector(selector)
                if elem and elem.is_visible():
                    if debug: print(f"[自动定位] login_button 通过 selector '{selector}' 找到可见元素")
                    return elem
            button = page.get_by_role("button", name="登录").first
            if button.count() > 0 and button.is_visible():
                if debug: print("[自动定位] login_button 通过 role=button name='登录' 找到可见元素")
                return button
            elem = page.get_by_label("登录").first
            if elem.count() > 0 and elem.is_visible():
                if debug: print("[自动定位] login_button 通过 aria-label 找到可见元素")
                return elem
            for tag in ['div', 'button', 'a']:
                elems = page.query_selector_all(f'{tag}:has-text("登录")')
                for elem in elems:
                    if elem.is_visible():
                        if debug: print(f"[自动定位] login_button 通过 {tag}:has-text 找到可见元素")
                        return elem
            return None
    except Exception as e:
        print(f"[自动定位] {role_type} 出错: {e}")
    return None


def get_element(page, manual_selector, auto_role, timeout=5000, debug=False):
    if manual_selector:
        try:
            elem = page.wait_for_selector(manual_selector, timeout=timeout)
            if elem:
                print(f"[定位] 使用手动选择器: {manual_selector}")
                return elem
        except:
            print(f"[定位] 手动选择器无效: {manual_selector}")
    elem = find_element_auto(page, auto_role, timeout, debug)
    if elem:
        print(f"[定位] 自动定位成功 ({auto_role})")
    else:
        print(f"[定位] 自动定位失败 ({auto_role})")
        if auto_role == "login_button" and debug:
            print("[调试] 页面上的按钮文本：")
            buttons = page.query_selector_all('div, button, input[type="button"], input[type="submit"], a')
            for btn in buttons:
                text = btn.text_content() or btn.get_attribute('value') or ""
                if text.strip():
                    print(f"  - {text.strip()}")
    return elem


def click_element_robust(element, page, debug=False):
    if not element:
        return False
    try:
        if hasattr(element, 'scroll_into_view_if_needed'):
            element.scroll_into_view_if_needed()
            time.sleep(0.3)
        elif hasattr(element, 'evaluate'):
            element.evaluate("el => el.scrollIntoView({block: 'center'})")
            time.sleep(0.3)
    except Exception as e:
        if debug: print(f"[点击] 滚动元素失败: {e}")
    try:
        if hasattr(element, 'wait_for'):
            element.wait_for(state="visible", timeout=3000)
        elif hasattr(element, 'is_visible'):
            if not element.is_visible():
                if debug: print("[点击] 元素不可见")
    except Exception as e:
        if debug: print(f"[点击] 等待可见失败: {e}")
    try:
        if hasattr(element, 'click'):
            element.click(timeout=3000)
        else:
            element.click(timeout=3000)
        if debug: print("[点击] 常规点击成功")
        return True
    except Exception as e:
        if debug: print(f"[点击] 常规点击失败: {e}")
    try:
        if hasattr(element, 'click'):
            element.click(force=True, timeout=3000)
        else:
            element.click(force=True, timeout=3000)
        if debug: print("[点击] force点击成功")
        return True
    except Exception as e2:
        if debug: print(f"[点击] force点击失败: {e2}")
    try:
        if hasattr(element, 'evaluate'):
            element.evaluate("el => el.click()")
        else:
            page.evaluate("el => el.click()", element)
        if debug: print("[点击] JS点击成功")
        return True
    except Exception as e3:
        if debug: print(f"[点击] JS点击失败: {e3}")
        return False


def get_captcha_code(page, ocr, debug=False):
    try:
        captcha_element = get_element(page, MANUAL_CAPTCHA_IMG_SELECTOR, "captcha_img", timeout=AUTO_LOCATE_TIMEOUT, debug=debug)
        if not captcha_element:
            print("[错误] 无法定位验证码图片")
            if debug:
                imgs = page.query_selector_all('img')
                print("页面上的img标签src列表：")
                for i, img in enumerate(imgs):
                    src = img.get_attribute('src')
                    if src:
                        print(f"  {i+1}. {src[:200]}")
            return None
        src = captcha_element.get_attribute('src') if hasattr(captcha_element, 'get_attribute') else None
        img_bytes = None
        if src and src.startswith('data:image'):
            base64_str = src.split(',')[1]
            img_bytes = base64.b64decode(base64_str)
        else:
            if hasattr(captcha_element, 'screenshot'):
                img_bytes = captcha_element.screenshot()
            else:
                img_bytes = captcha_element.screenshot()
        if not img_bytes:
            print("[错误] 无法获取验证码图片数据")
            return None
        result = ocr.classification(img_bytes)
        filtered = ''.join(filter(str.isdigit, result))
        if filtered:
            print(f"[识别] 验证码原始: {result}, 过滤后: {filtered}")
            return filtered
        else:
            print(f"[识别] 验证码识别结果无效: {result}")
            return None
    except Exception as e:
        print(f"[错误] 获取验证码失败: {e}")
        return None


def refresh_captcha(page, debug=False):
    try:
        refresh_btn = page.query_selector('a:has-text("换一张"), img[alt*="刷新"], .refresh-captcha')
        if refresh_btn:
            refresh_btn.click()
            if debug: print("[信息] 已点击刷新验证码")
            time.sleep(0.5)
            return True
        else:
            captcha_img = get_element(page, MANUAL_CAPTCHA_IMG_SELECTOR, "captcha_img", timeout=2000, debug=debug)
            if captcha_img:
                src = captcha_img.get_attribute('src')
                if src and '?' in src:
                    new_src = src.split('?')[0] + '?t=' + str(int(time.time()))
                    captcha_img.set_attribute('src', new_src)
                    if debug: print("[信息] 通过修改图片 URL 刷新验证码")
                    return True
            return False
    except Exception as e:
        if debug: print(f"[错误] 刷新验证码失败: {e}")
        return False


def is_login_successful(page, context, debug=False):
    """严格检查是否已登录成功"""
    current_url = page.url.lower()
    
    if "login" in current_url or "auth" in current_url:
        if debug:
            print("[验证] URL 仍包含登录关键字，判定为未登录")
        return False, "URL 仍为登录页"
    
    indicators = [
        ('a:has-text("个人中心")', "个人中心链接"),
        ('a:has-text("退出")', "退出链接"),
        ('span:has-text("欢迎")', "欢迎语"),
        ('.user-info', "用户信息区域"),
        ('.avatar', "头像"),
    ]
    for selector, desc in indicators:
        if page.query_selector(selector):
            if debug:
                print(f"[验证] 检测到成功标识: {desc}")
            return True, desc
    
    try:
        page.wait_for_timeout(2000)
        for selector, desc in indicators:
            if page.query_selector(selector):
                if debug:
                    print(f"[验证] 延迟后检测到成功标识: {desc}")
                return True, desc
    except:
        pass
    
    cookies = context.cookies()
    auth_cookies = ['token', 'sessionid', 'jsessionid', 'sid', 'userid']
    for cookie in cookies:
        if cookie['name'].lower() in auth_cookies:
            if debug:
                print(f"[验证] 存在 Cookie {cookie['name']} 且 URL 已跳转，辅助判定成功")
            return True, f"Cookie {cookie['name']} + URL跳转"
    
    return False, "未检测到登录成功标志"


def detect_error_message(page, debug=False):
    body_text = page.text_content('body')
    if "验证码错误" in body_text or "验证码不正确" in body_text:
        return 'captcha', "验证码错误"
    elif "账号或密码错误" in body_text or "用户名或密码错误" in body_text or "密码错误" in body_text:
        return 'password', "账号或密码错误"
    else:
        error_elem = page.query_selector('.error, .err, .alert-danger, .message-error')
        if error_elem:
            err_text = error_elem.text_content()
            if "验证码" in err_text:
                return 'captcha', err_text
            elif "密码" in err_text or "账号" in err_text:
                return 'password', err_text
        return None, None


def perform_login_attempt(page, context, username, password, ocr, attempt_num, debug=False):
    print(f"\n[尝试 {attempt_num}] 开始登录流程...")
    
    username_elem = get_element(page, MANUAL_USERNAME_SELECTOR, "username", timeout=AUTO_LOCATE_TIMEOUT, debug=debug)
    if not username_elem:
        print("[错误] 无法找到账号输入框")
        return False, False, "no_username_field"
    username_elem.fill(username)
    print("[信息] 已填写账号")
    
    password_elem = get_element(page, MANUAL_PASSWORD_SELECTOR, "password", timeout=AUTO_LOCATE_TIMEOUT, debug=debug)
    if not password_elem:
        print("[错误] 无法找到密码输入框")
        return False, False, "no_password_field"
    password_elem.fill(password)
    print("[信息] 已填写密码")
    
    max_captcha_retries = 3
    captcha_code = None
    for captcha_attempt in range(1, max_captcha_retries + 1):
        print(f"[验证码] 第 {captcha_attempt} 次识别...")
        captcha_code = get_captcha_code(page, ocr, debug=debug)
        if captcha_code:
            break
        else:
            print("[警告] 验证码识别失败，尝试刷新...")
            refresh_captcha(page, debug)
            time.sleep(0.5)
    if not captcha_code:
        print("[错误] 多次识别验证码失败")
        return False, True, "captcha_recognition_failed"
    
    captcha_input = get_element(page, MANUAL_CAPTCHA_INPUT_SELECTOR, "captcha_input", timeout=AUTO_LOCATE_TIMEOUT, debug=debug)
    if not captcha_input:
        print("[错误] 无法找到验证码输入框")
        return False, False, "no_captcha_field"
    captcha_input.fill(captcha_code)
    time.sleep(0.3)
    print(f"[信息] 已填写验证码: {captcha_code}")
    
    login_btn = get_element(page, MANUAL_LOGIN_BUTTON_SELECTOR, "login_button", timeout=AUTO_LOCATE_TIMEOUT, debug=debug)
    if not login_btn:
        print("[错误] 无法找到登录按钮")
        return False, False, "no_login_button"
    
    initial_pages = context.pages
    initial_url = page.url
    
    clicked = click_element_robust(login_btn, page, debug=debug)
    if not clicked:
        print("[错误] 点击登录按钮失败")
        return False, True, "click_failed"
    print("[信息] 已点击登录按钮")
    
    timeout = 15
    start_time = time.time()
    new_page = None
    url_changed = False
    login_success = False
    error_type = None
    
    while time.time() - start_time < timeout:
        if len(context.pages) > len(initial_pages):
            new_page = context.pages[-1]
            print(f"[信息] 检测到新标签页打开: {new_page.url}")
            page = new_page
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except:
                pass
            success, reason = is_login_successful(page, context, debug)
            if success:
                login_success = True
                print(f"[信息] 新页面登录成功: {reason}")
            else:
                err_type, err_msg = detect_error_message(page, debug)
                if err_type:
                    error_type = err_type
                    print(f"[警告] 新页面错误: {err_msg}")
            break
        
        current_url = page.url
        if current_url != initial_url:
            url_changed = True
            print(f"[信息] 当前页面 URL 变化: {current_url}")
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except:
                pass
            success, reason = is_login_successful(page, context, debug)
            if success:
                login_success = True
                print(f"[信息] 页面跳转后登录成功: {reason}")
            else:
                err_type, err_msg = detect_error_message(page, debug)
                if err_type:
                    error_type = err_type
                    print(f"[警告] 跳转后页面错误: {err_msg}")
            break
        
        err_type, err_msg = detect_error_message(page, debug)
        if err_type:
            error_type = err_type
            print(f"[警告] 检测到错误: {err_msg}")
            break
        
        success, reason = is_login_successful(page, context, debug)
        if success:
            login_success = True
            print(f"[信息] 页面内容检测到登录成功: {reason}")
            break
        
        time.sleep(0.5)
    else:
        print("[警告] 等待登录响应超时，未检测到页面变化或错误提示")
        success, reason = is_login_successful(page, context, debug)
        if success:
            login_success = True
            print(f"[信息] 超时后检测到登录成功: {reason}")
        else:
            err_type, err_msg = detect_error_message(page, debug)
            if err_type:
                error_type = err_type
                print(f"[警告] 超时后检测到错误: {err_msg}")
    
    if login_success:
        return True, False, None
    else:
        if error_type == 'captcha':
            print("[信息] 验证码错误，将刷新验证码并重试")
            refresh_captcha(page, debug)
            return False, True, error_type
        elif error_type == 'password':
            print("[错误] 账号或密码错误，停止重试")
            return False, False, error_type
        else:
            print("[警告] 登录失败，原因未知，将重试")
            return False, True, "unknown"


def is_port_open(port, host='127.0.0.1'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        return result == 0


def get_chrome_executable():
    mac_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium"
    ]
    for path in mac_paths:
        if os.path.exists(path):
            return path
    chrome_path = shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chromium-browser")
    if chrome_path:
        return chrome_path
    try:
        with sync_playwright() as p:
            chrome_info = p.chrome.executable_path
            if chrome_info and os.path.exists(chrome_info):
                return chrome_info
    except Exception:
        pass
    raise Exception("未找到 Google Chrome 浏览器！")


def start_chrome_with_debug_port(user_data_dir, debug_port, window_size, debug=False):
    chrome_path = get_chrome_executable()
    if debug:
        print(f"[调试] Chrome 路径: {chrome_path}")
    os.makedirs(user_data_dir, exist_ok=True)
    args = [
        chrome_path,
        f"--user-data-dir={user_data_dir}",
        f"--remote-debugging-port={debug_port}",
        f"--window-size={window_size}",
        "--no-first-run",
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars",
        "--test-type",
    ]
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        creationflags = 0
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            creationflags=creationflags if sys.platform == "win32" else 0,
                            start_new_session=True)
    max_wait = 10
    for _ in range(max_wait * 2):
        if is_port_open(debug_port):
            if debug:
                print(f"[调试] Chrome 已启动，调试端口 {debug_port} 可用")
            return proc
        time.sleep(0.5)
    raise Exception(f"Chrome 启动超时，端口 {debug_port} 未在 {max_wait} 秒内开放")


def connect_to_chrome(debug_port):
    p = sync_playwright().start()
    try:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{debug_port}")
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.pages[0] if context.pages else context.new_page()
        return p, browser, context, page
    except Exception as e:
        p.stop()
        raise e


def auto_login(username, password, login_url, debug=False, window_size="1280,800"):
    print("=" * 50)
    print("国家税务总局 12366 纳税服务平台自动登录")
    print("=" * 50)
    
    # ========== 新增：URL 清洗与有效性检查 ==========
    # 去除首尾空白和可能的引号（单引号/双引号）
    if login_url:
        login_url = login_url.strip()
        # 如果同时以双引号或单引号包裹，则去除外层匹配的引号
        if (login_url.startswith('"') and login_url.endswith('"')) or (login_url.startswith("'") and login_url.endswith("'")):
            login_url = login_url[1:-1]
        # 再次 strip 以防内部有空白
        login_url = login_url.strip()
    
    # 检查 URL 是否有效（必须以 http:// 或 https:// 开头）
    if not login_url or not (login_url.startswith("http://") or login_url.startswith("https://")):
        print(f"[错误] 无效的登录 URL: '{login_url}'")
        print("请确保 URL 以 http:// 或 https:// 开头，且不包含多余引号。")
        return False
    # =============================================
    
    ocr = ddddocr.DdddOcr(show_ad=False)
    
    if is_port_open(REMOTE_DEBUG_PORT):
        print(f"[信息] 检测到已有 Chrome 使用端口 {REMOTE_DEBUG_PORT}，将直接连接")
    else:
        print(f"[信息] 启动独立 Chrome 进程，端口 {REMOTE_DEBUG_PORT}，窗口大小 {window_size}")
        start_chrome_with_debug_port(USER_DATA_DIR, REMOTE_DEBUG_PORT, window_size, debug)
    
    playwright_obj, browser, context, page = connect_to_chrome(REMOTE_DEBUG_PORT)
    print(f"[信息] 已连接到 Chrome，打开登录页: {login_url}")
    
    success = False
    try:
        page.goto(login_url)
        page.wait_for_timeout(2000)
        
        already_logged_in, reason = is_login_successful(page, context, debug)
        if already_logged_in:
            print(f"[信息] 检测到已登录状态 ({reason})，跳过登录流程。")
            success = True
            return success
        else:
            print(f"[信息] 当前未登录（{reason}），开始自动登录流程...")
        
        for attempt in range(1, MAX_LOGIN_RETRIES + 1):
            if "login" not in page.url.lower():
                print("[信息] 当前不在登录页，重新加载登录页...")
                page.goto(login_url)
                page.wait_for_timeout(2000)
            
            login_ok, need_retry, error_type = perform_login_attempt(
                page, context, username, password, ocr, attempt, debug
            )
            
            if login_ok:
                success = True
                print("\n" + "=" * 50)
                print("✅ 登录成功！浏览器将继续保持打开状态。")
                print("=" * 50)
                break
            else:
                if not need_retry:
                    print(f"\n❌ 登录失败，原因: {error_type}，停止重试。")
                    break
                else:
                    print(f"\n🔄 登录失败 ({error_type})，准备第 {attempt+1} 次重试...")
                    refresh_captcha(page, debug)
                    time.sleep(1)
                    continue
        else:
            print(f"\n❌ 已达到最大重试次数 ({MAX_LOGIN_RETRIES})，登录失败。")
            success = False
    
    except KeyboardInterrupt:
        print("\n[信息] 接收到中断信号 (Ctrl+C)，脚本退出，浏览器不受影响继续运行。")
        success = False
    except Exception as e:
        print(f"[错误] 登录过程异常: {e}")
        if debug:
            import traceback
            traceback.print_exc()
        success = False
    finally:
        try:
            playwright_obj.stop()
        except Exception as e:
            if debug:
                print(f"[调试] 停止 Playwright 时出现异常（可忽略）: {e}")
    
    return success


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="自动登录国家税务总局 12366 纳税服务平台")
    parser.add_argument("username", help="登录账号")
    parser.add_argument("password", help="登录密码")
    parser.add_argument("--url", help="登录页面的URL（若未提供则从环境变量 GJSW_LOGIN_URL 读取）")
    parser.add_argument("--debug", action="store_true", help="调试模式（打印更多信息）")
    parser.add_argument("--window-size", default="1280,800", help="浏览器窗口大小，格式: 宽度,高度 (例如 1920,1080)，默认 1280,800")
    args = parser.parse_args()

    # 获取登录 URL：优先使用命令行参数，其次使用环境变量 GJSW_LOGIN_URL
    login_url = args.url
    if not login_url:
        login_url = os.environ.get("GJSW_LOGIN_URL")
    if not login_url:
        print("错误：未提供登录页面 URL。请通过 --url 参数指定，或设置环境变量 GJSW_LOGIN_URL。")
        sys.exit(1)

    # 清洗 URL（去除可能的多余引号和空白）
    login_url = login_url.strip()
    if (login_url.startswith('"') and login_url.endswith('"')) or (login_url.startswith("'") and login_url.endswith("'")):
        login_url = login_url[1:-1]
    login_url = login_url.strip()

    # 简单检查 URL 有效性，提前给出明确错误
    if not (login_url.startswith("http://") or login_url.startswith("https://")):
        print(f"错误：登录 URL 无效，必须以 http:// 或 https:// 开头。当前值: '{login_url}'")
        sys.exit(1)

    success = auto_login(args.username, args.password, login_url, args.debug, args.window_size)
    sys.exit(0 if success else 1)
