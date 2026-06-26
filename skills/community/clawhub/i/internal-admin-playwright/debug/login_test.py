#!/usr/bin/env python3
"""独立登录测试脚本，诊断 staff.bluemv.net 登录问题"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__) + '/../scripts')

from playwright.sync_api import sync_playwright

OTP = sys.argv[1] if len(sys.argv) > 1 else input("请输入验证码: ").strip()

BASE_URL = "https://staff.bluemv.net/d.php"
USERNAME = "wulongcha"
PASSWORD = "wulongcha"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=800)  # 开可视窗口，慢速执行
    ctx = browser.new_context(ignore_https_errors=True)
    page = ctx.new_page()

    print(f"[1] 打开登录页: {BASE_URL}")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    print(f"    当前URL: {page.url}")
    print(f"    页面标题: {page.title()}")

    print("[2] 查找所有 input 字段:")
    inputs = page.locator("input").all()
    for i, inp in enumerate(inputs):
        try:
            name = inp.get_attribute("name") or ""
            typ = inp.get_attribute("type") or ""
            placeholder = inp.get_attribute("placeholder") or ""
            visible = inp.is_visible()
            print(f"    [{i}] name={name!r} type={typ!r} placeholder={placeholder!r} visible={visible}")
        except:
            pass

    print("[3] 填写账号密码和验证码...")
    # 用户名
    page.locator('input[name="username"]').fill(USERNAME)
    page.wait_for_timeout(300)
    # 密码
    page.locator('input[name="password"]').fill(PASSWORD)
    page.wait_for_timeout(300)
    # 标识码
    card_input = page.locator('input[name="card_num"]')
    if card_input.count() > 0 and card_input.is_visible():
        card_input.fill(OTP)
        print(f"    已填标识码: {OTP}")
    else:
        print("    [警告] 未找到 card_num 字段！")
    page.wait_for_timeout(300)

    print("[4] 点击登录按钮...")
    page.locator('button[type="submit"], button:has-text("登")').first.click()
    page.wait_for_timeout(3000)

    print(f"[5] 登录后URL: {page.url}")
    print(f"    页面标题: {page.title()}")

    # 检查是否还在登录页
    if "login" in page.url.lower() or "登录" in page.title():
        print("[结果] ❌ 登录失败，仍在登录页")
        # 截图
        page.screenshot(path="/tmp/login_test.png", full_page=True)
        print("    截图已保存到 /tmp/login_test.png")
        # 打印页面错误文字
        body = page.inner_text("body")
        print(f"    页面内容: {body[:300]}")
    else:
        print("[结果] ✅ 登录成功！")
        print("[6] 查找菜单项 '帖子社区'...")
        try:
            page.get_by_text("帖子社区").first.wait_for(timeout=5000)
            print("    ✅ 找到'帖子社区'菜单！")
        except:
            print("    ❌ 未找到'帖子社区'，打印页面所有文字:")
            print(page.inner_text("body")[:500])

    input("按回车关闭浏览器...")
    browser.close()
