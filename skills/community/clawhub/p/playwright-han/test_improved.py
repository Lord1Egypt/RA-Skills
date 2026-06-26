#!/usr/bin/env python3
"""
Playwright 测试 - 改进版（直接访问搜索 URL）
"""

from playwright.sync_api import sync_playwright

def test_playwright():
    """测试 Playwright 基本功能"""
    print("[*] 启动 Playwright...")
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 直接访问搜索 URL
        print("[*] 访问百度搜索：毛毛...")
        page.goto('https://www.baidu.com/s?wd=毛毛', wait_until='networkidle')
        
        # 截图
        print("[*] 截图...")
        page.screenshot(path='/tmp/playwright_maomao.png')
        
        # 获取标题
        print(f"[✓] 页面标题：{page.title()}")
        
        # 获取搜索结果
        results = page.query_selector_all('.result h3')
        print(f"[✓] 找到 {len(results)} 个搜索结果")
        
        for i, r in enumerate(results[:5], 1):
            text = r.inner_text()
            print(f"   {i}. {text}")
        
        # 保存完整页面截图
        page.screenshot(path='/tmp/playwright_full.png', full_page=True)
        print("[✓] 完整页面截图已保存")
        
        browser.close()
        print("[✓] Playwright 测试成功！")

if __name__ == '__main__':
    test_playwright()
