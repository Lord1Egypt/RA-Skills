#!/usr/bin/env python3
"""
Playwright 学习笔记 - 第一个脚本
对比 Selenium 和 Playwright 的区别
"""

from playwright.sync_api import sync_playwright
import time

def test_playwright():
    """测试 Playwright 基本功能"""
    print("[*] 启动 Playwright...")
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("[*] 访问百度...")
        page.goto('https://www.baidu.com')
        
        # 截图
        print("[*] 截图...")
        page.screenshot(path='/tmp/playwright_baidu.png')
        
        # 搜索
        print("[*] 搜索'毛毛'...")
        page.fill('#kw', '毛毛')
        page.click('#su')
        
        # 等待结果
        page.wait_for_selector('#content_left')
        
        # 获取结果
        results = page.query_selector_all('.result h3')
        print(f"[✓] 找到 {len(results)} 个搜索结果")
        
        for i, r in enumerate(results[:5], 1):
            print(f"   {i}. {r.inner_text()}")
        
        # 截图
        page.screenshot(path='/tmp/playwright_search.png')
        print("[✓] 截图已保存")
        
        browser.close()
        print("[✓] 完成！")

if __name__ == '__main__':
    try:
        test_playwright()
    except Exception as e:
        print(f"[!] 错误：{e}")
