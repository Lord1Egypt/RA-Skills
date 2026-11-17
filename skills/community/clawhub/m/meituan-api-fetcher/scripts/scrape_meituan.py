#!/usr/bin/env python3
"""
美团餐饮系统(智能版) 开放平台数据抓取脚本 v4
修复：每个分类展开后点其子菜单中的"API列表"（最后可见的那个）
"""
from playwright.sync_api import sync_playwright
import json, os, sys, time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SOLUTIONS_DIR = SKILL_DIR / "solutions"
REFERENCES_DIR = SKILL_DIR / "references"
SOLUTIONS_DIR.mkdir(exist_ok=True)
REFERENCES_DIR.mkdir(exist_ok=True)

BASE = "https://developer.meituan.com"
START_URL = f"{BASE}/docs/biz/biz_rms_e8a2bfb2-c855-40ff-8565-ee946a5cae2e"
API_URL = f"{BASE}/docs/biz/biz_rms_0ee2d760-3990-405b-9a2a-782d96324870"

def create_page():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True,
        args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        viewport={'width': 1440, 'height': 900}, locale='zh-CN')
    page = context.new_page()
    page.add_init_script('''
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN','zh','en']});
    ''')
    return p, browser, context, page

def expand_submenu(page, text, timeout=2000):
    """展开指定文字的 submenu"""
    titles = page.query_selector_all('.ant-menu-submenu-title')
    for t in titles:
        if t.text_content().strip() == text:
            if not t.evaluate('el => { const p = el.closest(".ant-menu-submenu"); return p ? p.classList.contains("ant-menu-submenu-open") : false; }'):
                t.click()
                page.wait_for_timeout(timeout)
            return True
    return False

def click_last_visible_item(page, text, timeout=4000):
    """点击最后一个可见的指定文字 menu-item（确保点到的不是旧分类的）"""
    items = page.query_selector_all('.ant-menu-item')
    candidates = []
    for item in items:
        if item.text_content().strip() == text and item.evaluate('el => el.offsetParent !== null'):
            candidates.append(item)
    if candidates:
        candidates[-1].click()  # 点最后一个
        page.wait_for_timeout(timeout)
        return True
    return False

def get_page_content(page):
    for sel in ['.doc-content', '.markdown-body', 'main', '[class*="content"]']:
        el = page.query_selector(sel)
        if el:
            text = el.text_content()
            if len(text) > 200:
                return text.strip()
    return page.text_content('body')

def scrape_solutions(page):
    """抓取所有解决方案页面"""
    print("\n=== 阶段1: 解决方案 ===")
    page.goto(START_URL, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(8000)
    
    results = []
    
    # 7个直接解决方案项
    for sol_name in [
        "堂食扫码点餐", "自营外卖下单", "第三方会员CRM对接",
        "第三方财务对接", "第三方数据中台", "第三方供应链对接",
        "供应链旗舰版对接三方系统-说明文档",
    ]:
        print(f"  {sol_name}...", end=" ")
        try:
            if click_last_visible_item(page, sol_name, timeout=4000):
                url = page.url
                content = get_page_content(page)
                fname = sol_name.replace("/", "-").replace(" ", "_") + ".md"
                (SOLUTIONS_DIR / fname).write_text(f"# {sol_name}\n\nURL: {url}\n\n{content}", encoding='utf-8')
                results.append({"name": sol_name, "url": url, "file": fname, "len": len(content)})
                print(f"✅ {len(content)}c")
                time.sleep(2)
            else:
                print("❌")
        except Exception as e:
            print(f"❌ {e}")
    
    # 三方交易子项
    print("\n  三方交易:")
    click_last_visible_item(page, "堂食扫码点餐", timeout=2000)
    page.wait_for_timeout(1000)
    
    if expand_submenu(page, "三方交易"):
        page.wait_for_timeout(1000)
        for item in ["三方交易接口白皮书", "接口对接流程", "三方开台接口", "查询桌台订单接口", "三方下单接口"]:
            print(f"    {item}...", end=" ")
            try:
                if click_last_visible_item(page, item, timeout=4000):
                    url = page.url
                    content = get_page_content(page)
                    fname = f"三方交易_{item.replace('/', '-')}.md"
                    (SOLUTIONS_DIR / fname).write_text(f"# 三方交易 - {item}\n\nURL: {url}\n\n{content}", encoding='utf-8')
                    results.append({"name": f"三方交易/{item}", "url": url, "file": fname, "len": len(content)})
                    print(f"✅ {len(content)}c")
                    time.sleep(2)
                else:
                    print("❌")
            except Exception as e:
                print(f"❌ {e}")
    
    return results

def scrape_api_categories(page):
    """抓取API分类 - 每个分类展开后点最后一个'API列表'"""
    print("\n=== 阶段2: API分类 ===")
    page.goto(API_URL, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(8000)
    
    results = []
    
    categories = {
        "基础档案类": ["API列表", "消息列表"],
        "数据报表类": ["API列表"],
        "订单类": ["API列表", "消息列表"],
        "沽清类": ["API列表", "消息列表"],
        "会员营销类": ["API列表"],
        "供应链旗舰版": ["API列表", "消息列表"],
    }
    
    for cat_name, sub_items in categories.items():
        print(f"  {cat_name}:")
        
        if not expand_submenu(page, cat_name):
            print(f"    ❌ 展开失败")
            continue
        page.wait_for_timeout(1000)
        
        for sub_name in sub_items:
            print(f"    {sub_name}...", end=" ")
            try:
                if click_last_visible_item(page, sub_name, timeout=4000):
                    page.wait_for_timeout(2000)
                    url = page.url
                    content = get_page_content(page)
                    fname = f"{cat_name}_{sub_name}.md"
                    (REFERENCES_DIR / fname).write_text(f"# {cat_name} - {sub_name}\n\nURL: {url}\n\n{content}", encoding='utf-8')
                    results.append({"category": cat_name, "type": sub_name, "url": url, "file": fname, "len": len(content)})
                    print(f"✅ {len(content)}c")
                    time.sleep(2)
                else:
                    print("❌")
            except Exception as e:
                print(f"❌ {e}")
    
    return results

def main():
    print("🦞 美团餐饮系统开放平台 - 数据抓取 v4")
    p, browser, context, page = create_page()
    
    try:
        sol_results = scrape_solutions(page)
        api_results = scrape_api_categories(page)
        
        report = {
            "platform": "美团餐饮系统(智能版)",
            "scrape_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "solutions": sol_results,
            "api_categories": api_results,
        }
        (SKILL_DIR / "scrape_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        
        sol_ok = len([r for r in sol_results if r.get('url')])
        api_ok = len([r for r in api_results if r.get('url')])
        print(f"\n{'='*50}")
        print(f"📊 完成: 解决方案 {sol_ok}/{len(sol_results)}, API {api_ok}/{len(api_results)}")
        print(f"Skill目录: {SKILL_DIR}")
        
    finally:
        browser.close()
        p.stop()

if __name__ == "__main__":
    main()
