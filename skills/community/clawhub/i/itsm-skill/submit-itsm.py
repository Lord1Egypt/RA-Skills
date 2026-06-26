#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ITSM 工单自动提交 - 严格对应 submit-itsm.js 的操作流程
使用 Selenium + CDP（Chrome DevTools Protocol）
"""

import subprocess
import time
import json
import sys
import os
import re

try:
    import requests
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import TimeoutException
except ImportError as e:
    print(f"❌ 缺少依赖库: {e}")
    print("请运行: pip install selenium requests")
    sys.exit(1)

# 配置（对应 JS 中的 CONFIG）
CONFIG = {
    'url': 'https://itsm.westmonth.com/#/create',
    'username': '500525',
    'password': 'Xy@123456',
    'ticketType': '头程询价',
    'warehouse': '美国15仓',
    'sku': '11',
    'remark': '11',
    'attachmentPath': r'C:\Users\Administrator\Desktop\30d5179fb6468e1643740a153838a9dd (1).jpeg',
    'debug_port': 9222
}

def setup_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"localhost:{CONFIG['debug_port']}")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--force-device-scale-factor=1.0 --disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def take_screenshot(driver, filename):
    screenshot_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
    os.makedirs(screenshot_dir, exist_ok=True)
    filepath = os.path.join(screenshot_dir, filename)
    driver.save_screenshot(filepath)
    print(f"   📸 截图已保存: {filename}")

def convert_windows_to_wsl_path(windows_path):
    """
    将 Windows 路径转换为 WSL 路径
    例如: C:\\Users\\... -> /mnt/c/Users/...
    """
    if not windows_path:
        return None

    # 移除可能的引号
    windows_path = windows_path.strip().strip('"').strip("'")

    # 如果已经是 WSL 路径或相对路径，直接返回
    if windows_path.startswith('/') or windows_path.startswith('./'):
        return windows_path

    # 匹配 Windows 路径格式 (C:\, C:/, \\server\share, 等)
    # 处理盘符路径: C:\path -> /mnt/c/path
    drive_pattern = r'^([A-Za-z]):[/\\](.+)$'
    match = re.match(drive_pattern, windows_path)

    if match:
        drive_letter = match.group(1).lower()
        rest_of_path = match.group(2)
        # 将反斜杠转换为正斜杠
        rest_of_path = rest_of_path.replace('\\', '/')
        wsl_path = f"/mnt/{drive_letter}/{rest_of_path}"
        print(f"   🔄 路径转换: {windows_path} -> {wsl_path}")
        return wsl_path

    # UNC 路径处理 (\\server\share) - WSL 中通过 \\wsl$\ 访问
    unc_pattern = r'^\\\\([^\\]+)\\(.+)$'
    match = re.match(unc_pattern, windows_path)
    if match:
        server = match.group(1)
        share = match.group(2).replace('\\', '/')
        # UNC 路径在 WSL 中需要特殊处理，返回原路径让浏览器处理
        print(f"   ⚠️ 检测到 UNC 路径，使用原路径: {windows_path}")
        return windows_path

    # 无法识别的格式，返回原路径
    print(f"   ⚠️ 无法识别路径格式，使用原路径: {windows_path}")
    return windows_path

def submit_itsm_ticket():
    driver = None
    try:
        print("🚀 开始 ITSM 工单自动化提交...\n")
        driver = setup_driver()
        print("✅ 已连接到浏览器")
        print("📝 访问 ITSM 系统...")
        driver.get(CONFIG['url'])
        time.sleep(2)
        take_screenshot(driver, '01-login.png')

        # 检查登录状态
        print("📝 检查登录状态...")
        already_logged_in = False
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "工作台")]'))
            )
            already_logged_in = True
            print("   ✅ 检测到已登录，跳过登录步骤")
        except TimeoutException:
            print("   📝 需要登录，开始登录流程...")

        if not already_logged_in:
            try:
                username_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"], input[name="username"], input[placeholder*="用户名"]'))
                )
                username_input.send_keys(CONFIG['username'])
                password_input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"], input[name="password"], input[placeholder*="密码"]')
                password_input.send_keys(CONFIG['password'])
                try:
                    login_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], .login-btn')
                    login_btn.click()
                except:
                    password_input.send_keys(Keys.RETURN)
                time.sleep(6)
                take_screenshot(driver, '02-logged-in.png')
                print("✅ 已登录")
            except TimeoutException:
                print("   ⚠️ 登录步骤失败，可能已经登录")
                time.sleep(2)

        # 导航菜单
        print("📝 导航到工单管理...")
        ticket_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "工单管理")]'))
        )
        ticket_menu.click()
        time.sleep(2)
        print("   ✅ 已点击工单管理")

        create_ticket = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "发起工单")]'))
        )
        create_ticket.click()
        time.sleep(2)
        print("   ✅ 已点击发起工单")

        overseas_ticket = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "新海外仓售前售中工单")]'))
        )
        overseas_ticket.click()
        time.sleep(3)
        print("   ✅ 已点击新海外仓售前售中工单")

        take_screenshot(driver, '03-ticket-form.png')

        # 选择工单类型
        print(f"📝 选择工单类型：{CONFIG['ticketType']}")
        try:
            ticket_type_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[contains(text(), "{CONFIG["ticketType"]}") and not(contains(@class, "anticon"))]'))
            )
            ticket_type_btn.click()
            time.sleep(1)
            print(f"   ✅ 已选择工单类型：{CONFIG['ticketType']}")
        except TimeoutException:
            print("   ⚠️ 工单类型选择失败，可能已默认选择")
        time.sleep(2)

        # 需求类别级联选择器
        print("📝 选择需求类别...")
        try:
            cascader_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.ant-cascader-input, .ant-select-selection-search-input'))
            )
            cascader_input.click()
            print("   ✅ 已点击级联选择器输入框")
            time.sleep(1)
            cascader_input.send_keys('头程询价')
            print("   🔍 已输入【头程询价】搜索...")
            time.sleep(3)
            take_screenshot(driver, '04-cascader-search.png')

            js_find_option = '''
const menus = document.querySelectorAll(".ant-cascader-menu, .ant-select-dropdown, [class*=cascader-menu], [class*=dropdown-menu]");
for (let menu of menus) {
    if (menu.offsetParent === null) continue;
    const allElements = menu.querySelectorAll("*");
    for (let elem of allElements) {
        if (elem.textContent && elem.textContent.trim() === "头程询价" && elem.offsetParent !== null) {
            let clickable = elem;
            while (clickable && !clickable.classList.contains("ant-cascader-menu-item") && !clickable.classList.contains("ant-select-item") && clickable !== menu) {
                clickable = clickable.parentElement;
            }
            if (clickable && clickable !== menu) {
                clickable.click();
                return "Clicked";
            }
            elem.click();
            return "Clicked";
        }
    }
}
return "Not found";
'''
            result = driver.execute_script(js_find_option)
            if result and 'Clicked' in result:
                time.sleep(1.5)
                print(f'   ✅ 已点击"头程询价"选项')
                take_screenshot(driver, '05-cascader-selected.png')
            else:
                print(f"   ⚠️ 未找到下拉选项: {result}")
        except Exception as e:
            print(f"   ⚠️ 需求类别选择失败: {e}")
            take_screenshot(driver, '05-cascader-error.png')
        time.sleep(2)
        take_screenshot(driver, '06-form-loaded.png')

        # 填写 SKU
        print(f"📝 填写商品编码：{CONFIG['sku']}")
        try:
            sku_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'requirementProjectForm_tableData_0_sku_id'))
            )
            sku_input.click()
            time.sleep(0.3)
            sku_input.clear()
            sku_input.send_keys(CONFIG['sku'])
            print(f"   ✅ 已填写商品编码：{CONFIG['sku']}")
            take_screenshot(driver, '07-sku-filled.png')
        except TimeoutException as e:
            print(f"   ❌ 商品编码填写失败: {e}")
            take_screenshot(driver, '07-sku-error.png')

        # 步骤8: 滚动表格
        print("📝 滚动表格...")
        try:
            scroll_handle = driver.find_element(By.CSS_SELECTOR, '.vxe-table--scroll-x-handle')
            location = scroll_handle.location
            size = scroll_handle.size

            if location and size:
                print(f"   → 滚动条位置：x={location['x']}, y={location['y']}, width={size['width']}")
                actions = ActionChains(driver)
                actions.move_to_element(scroll_handle).perform()
                time.sleep(0.3)
                actions.click_and_hold(scroll_handle).perform()
                time.sleep(0.3)
                actions.move_by_offset(500, 0).perform()
                time.sleep(0.5)
                actions.release().perform()
                print("   ✅ 已滚动表格到右侧")
                time.sleep(1)
            else:
                print("   ⚠️ 无法获取滚动条位置")
        except Exception as e:
            print(f"   ⚠️ 未找到滚动条，尝试直接滚动... ({e})")
            try:
                driver.execute_script('''
                    const table = document.querySelector(".vxe-table--body-wrapper");
                    if (table) table.scrollLeft = 500;
                ''')
                time.sleep(1)
            except:
                pass
        take_screenshot(driver, '08-scrolled.png')

        # 步骤9: 填写备注
        print("📝 填写备注...")
        try:
            # 直接使用 ID 填写备注
            remark_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'requirementProjectForm_tableData_0_description'))
            )

            # 滚动到输入框
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", remark_input)
            time.sleep(0.5)

            # 点击并清空
            remark_input.click()
            time.sleep(0.3)
            remark_input.clear()
            time.sleep(0.3)

            # 填写备注
            remark_input.send_keys(CONFIG['remark'])
            print(f"   ✅ 备注已填写：{CONFIG['remark']}")
            take_screenshot(driver, '09-remark-filled.png')

        except TimeoutException:
            print(f"   ⚠️ 未找到备注输入框（ID: requirementProjectForm_tableData_0_description）")
            take_screenshot(driver, '09-remark-error.png')
        except Exception as e:
            print(f"   ❌ 备注填写失败: {e}")
            take_screenshot(driver, '09-remark-error.png')

        time.sleep(1)

        # 步骤10: 上传附件（支持 Windows 路径转换）
        print(f"📝 检查附件配置...")
        print(f"   CONFIG['attachmentPath'] = {CONFIG.get('attachmentPath')}")

        if CONFIG.get('attachmentPath'):
            print(f"📝 上传附件：{CONFIG['attachmentPath']}")
            try:
                attachment_path = CONFIG['attachmentPath']

                # 路径转换：Windows -> WSL
                print(f"   → 开始路径转换...")
                wsl_path = convert_windows_to_wsl_path(attachment_path)
                print(f"   → 转换后路径: {wsl_path}")

                # 检查文件是否存在
                if not os.path.exists(wsl_path):
                    print(f"   ⚠️ 附件文件不存在：{wsl_path}")
                    print(f"   原路径：{attachment_path}")
                    print(f"   当前工作目录: {os.getcwd()}")
                else:
                    upload_clicked = False
                    try:
                        upload_btn = driver.find_element(By.XPATH, '//button[contains(text(), "上传")]')
                        if upload_btn.is_displayed():
                            print("   → 找到上传按钮，点击...")
                            upload_btn.click()
                            upload_clicked = True
                            time.sleep(1.5)
                    except:
                        pass

                    if not upload_clicked:
                        try:
                            upload_btn = driver.find_element(By.CSS_SELECTOR, '.upload-btn, i[class*="upload"]')
                            if upload_btn.is_displayed():
                                upload_btn.click()
                                upload_clicked = True
                                time.sleep(1.5)
                        except:
                            pass

                    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                    if file_input:
                        abs_path = os.path.abspath(wsl_path)
                        print(f"   📎 使用路径: {abs_path}")
                        file_input.send_keys(abs_path)
                        print("   ✅ 附件上传成功")
                        time.sleep(3)
                        take_screenshot(driver, '10-uploaded.png')
                    else:
                        print("   ❌ 未找到文件上传输入框")
            except Exception as e:
                print(f"   ❌ 附件上传失败: {e}")
                take_screenshot(driver, '10-upload-error.png')
        else:
            print("📝 跳过附件上传（未配置附件路径）")

        time.sleep(2)

        # 步骤11: 选择发货仓
        print(f"📝 选择发货仓：{CONFIG['warehouse']}")
        try:
            warehouse_label = driver.find_element(By.XPATH, '//*[contains(text(), "发货仓")]')
            if warehouse_label:
                print("   ✅ 已找到发货仓 label")
                dropdown_element = None
                current_parent = warehouse_label.find_element(By.XPATH, '..')
                depth = 0
                max_depth = 10
                while depth < max_depth:
                    try:
                        parent_html = current_parent.get_attribute('innerHTML')
                        if '.ant-select' in parent_html or '.ant-cascader' in parent_html or 'ant-select-selector' in parent_html:
                            dropdown_elements = current_parent.find_elements(By.CSS_SELECTOR, '.ant-select, .ant-cascader, .ant-select-selector, .ant-cascader-input')
                            if dropdown_elements:
                                dropdown_element = dropdown_elements[0]
                                print(f"   ✅ 在第{depth + 1}层找到包含下拉框的父容器")
                                break
                    except:
                        pass
                    try:
                        current_parent = current_parent.find_element(By.XPATH, '..')
                    except:
                        break
                    depth += 1

                if dropdown_element:
                    dropdown_element.click()
                    print("   ✅ 已点击发货仓下拉框")
                    time.sleep(1)
                    dropdown_input = dropdown_element.find_element(By.CSS_SELECTOR, 'input[type="text"], input[type="search"]')
                    dropdown_input.clear()
                    dropdown_input.send_keys(CONFIG['warehouse'])
                    print(f"   🔍 已输入【{CONFIG['warehouse']}】搜索...")
                    time.sleep(3)
                    take_screenshot(driver, '10-warehouse-dropdown.png')
                    first_option = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, f'//*[contains(@class, "ant-select-item-option") or contains(@class, "ant-cascader-menu-item-content") or @role="option"]//*[contains(text(), "{CONFIG["warehouse"]}")]'))
                    )
                    if first_option:
                        first_option.click()
                        time.sleep(1.5)
                        print(f"   ✅ 已选择发货仓：{CONFIG['warehouse']}")
                        take_screenshot(driver, '11-warehouse-selected.png')
                else:
                    print("   ⚠️ 未找到发货仓下拉框")
            else:
                print("   ⚠️ 未找到发货仓 label")
        except Exception as e:
            print(f"   ⚠️ 发货仓选择失败: {e}")
            take_screenshot(driver, '11-warehouse-error.png')

        time.sleep(2)
        take_screenshot(driver, '12-form-all-filled.png')

        # 步骤12: 提交工单
        print("📝 提交工单...")
        try:
            submit_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "提交") or contains(text(), "确定")]'))
            )
            submit_btn.click()
            time.sleep(3)
            print("   ✅ 工单已提交")
            take_screenshot(driver, '13-submitted.png')
        except TimeoutException:
            buttons = driver.find_elements(By.CSS_SELECTOR, 'button')
            for btn in buttons:
                text = btn.text
                if '提交' in text or '确定' in text:
                    btn.click()
                    time.sleep(3)
                    print(f"   ✅ 已点击提交按钮 ({text})")
                    take_screenshot(driver, '13-submitted.png')
                    break

        print("\n✅ ITSM 工单提交完成！")
        print(f"📸 截图已保存到: screenshots/")
        return True

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        if driver:
            try:
                driver.save_screenshot('screenshots/error.png')
                print("📸 错误截图已保存: screenshots/error.png")
            except:
                pass
        return False
    finally:
        if driver:
            print("\n💡 浏览器保持运行，可以继续操作")
            print("   关闭浏览器: pkill -f 'chromium.*--remote-debugging-port=9222'")

if __name__ == '__main__':
    # 解析命令行参数
    print(f"🔍 [DEBUG] 收到的命令行参数: {sys.argv}")
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            print(f"🔍 [DEBUG] 处理参数: {arg}")
            if '=' in arg:
                key, value = arg.split('=', 1)
                print(f"🔍 [DEBUG] 键值对: {key} = {value}")
                if key in ['username', 'password', 'sku', 'remark', 'warehouse', 'ticketType', 'attachmentPath']:
                    CONFIG[key] = value
                    print(f"✅ 已设置 CONFIG['{key}'] = {value}")
                elif key == 'image':
                    # 支持 --image 参数作为附件路径
                    CONFIG['attachmentPath'] = value
                    print(f"✅ 已设置 CONFIG['attachmentPath'] = {value}")

    # 显示最终配置
    print("\n📋 最终配置:")
    print(f"   - username: {CONFIG['username']}")
    print(f"   - sku: {CONFIG['sku']}")
    print(f"   - remark: {CONFIG['remark']}")
    print(f"   - warehouse: {CONFIG['warehouse']}")
    print(f"   - attachmentPath: {CONFIG['attachmentPath']}")
    print("")

    submit_itsm_ticket()
