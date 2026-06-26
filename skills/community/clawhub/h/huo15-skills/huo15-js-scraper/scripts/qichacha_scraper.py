#!/usr/bin/env python3
"""
企查查 (Qichacha) 数据抓取模块 v1.1
支持二维码登录、Cookie管理、企业信息抓取

依赖:
    pip3 install playwright --break-system-packages
    playwright install chromium

用法:
    # 登录（生成二维码截图）
    python3 qichacha_scraper.py --login
    
    # 搜索企业
    python3 qichacha_scraper.py --search "腾讯"
    
    # 抓取企业详情
    python3 qichacha_scraper.py --company "https://www.qcc.com/firm/xxxxx.html"

推荐方案:
    企查查MCP（官方API）需要先在 https://agent.qcc.com 注册获取API Key，
    然后配置到OpenClaw插件中使用。
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

# Cookie存储路径
COOKIE_DIR = Path.home() / ".cache" / "huo15-js-scraper"
COOKIE_FILE = COOKIE_DIR / "qichacha_cookies.json"
QRCODE_FILE = COOKIE_DIR / "qichacha_qrcode.png"
QRCODE_TIMESTAMP = COOKIE_DIR / "qrcode_timestamp.txt"

def ensure_dirs():
    """确保目录存在"""
    COOKIE_DIR.mkdir(parents=True, exist_ok=True)

def save_cookies(context):
    """保存登录Cookie"""
    ensure_dirs()
    cookies = context.cookies()
    with open(COOKIE_FILE, 'w') as f:
        json.dump(cookies, f)
    print(f"Cookie已保存到: {COOKIE_FILE}")

def load_cookies():
    """加载已保存的Cookie"""
    if COOKIE_FILE.exists():
        with open(COOKIE_FILE, 'r') as f:
            return json.load(f)
    return None

def is_cookie_valid():
    """检查Cookie是否有效"""
    cookies = load_cookies()
    if not cookies:
        return False
    
    # 检查关键Cookie是否存在
    cookie_names = [c['name'] for c in cookies]
    has_auth = any('qcc' in name.lower() or 'token' in name.lower() or 'session' in name.lower() for name in cookie_names)
    return has_auth

def login_with_qrcode():
    """二维码登录，返回截图路径"""
    ensure_dirs()
    
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = context.new_page()
        
        # 访问登录页
        print('访问企查查登录页...')
        page.goto("https://www.qcc.com/weblogin", wait_until="domcontentloaded", timeout=20000)
        time.sleep(3)
        
        print(f'页面标题: {page.title()}')
        print(f'当前URL: {page.url}')
        
        # 截图登录页
        page.screenshot(path=str(COOKIE_DIR / 'qichacha_login.png'), full_page=False)
        print(f'\\n登录页截图已保存: {COOKIE_DIR / "qichacha_login.png"}')
        
        # 尝试提取QR码
        try:
            # 等待QR码加载
            page.wait_for_selector('.qrcode-img img, .qr-code img, canvas', timeout=5000)
            
            # 查找QR码img
            qr_img = page.locator('.qrcode-img img, .qr-code img').first
            if qr_img.count() > 0:
                src = qr_img.get_attribute('src')
                if src:
                    print(f'找到QR码图片src: {src[:50]}...')
                    qr_img.screenshot(path=str(QRCODE_FILE))
                    print(f'QR码截图已保存: {QRCODE_FILE}')
            
            # 查找canvas
            canvases = page.locator('canvas').all()
            if canvases:
                print(f'找到 {len(canvases)} 个canvas元素')
        except Exception as e:
            print(f'提取QR码失败: {e}')
        
        print('\\n' + '='*50)
        print('请用企查查APP扫码登录！')
        print('='*50)
        print(f'\\n截图位置: {COOKIE_DIR / "qichacha_login.png"}')
        print('请用手机扫码登录后告诉我，我会保存Cookie')
        print('\\n等待扫码确认...(最多5分钟)')
        
        # 等待扫码登录（最多5分钟）
        max_wait = 300
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            time.sleep(3)
            
            # 检查URL变化
            if 'weblogin' not in page.url:
                print('\\n✅ 登录成功! (URL变化检测)')
                save_cookies(context)
                browser.close()
                return True
            
            # 检查cookies
            cookies = context.cookies()
            if any(c['name'] == 'qcc_c' for c in cookies):
                print('\\n✅ 登录成功! (Cookie检测)')
                save_cookies(context)
                browser.close()
                return True
            
            # 每30秒提示一次
            elapsed = int(time.time() - start_time)
            if elapsed % 30 == 0 and elapsed > 0:
                print(f'  等待中... ({elapsed}秒)')
        
        print('\\n❌ 登录超时')
        browser.close()
        return False

def search_company(keyword, limit=10):
    """搜索企业"""
    from playwright.sync_api import sync_playwright
    
    cookies = load_cookies()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        if cookies:
            context.add_cookies(cookies)
        
        page = context.new_page()
        
        # 访问搜索页
        search_url = f"https://www.qcc.com/web/search?key={keyword}"
        page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(5)
        
        # 检查是否跳转到了登录页
        if 'weblogin' in page.url:
            browser.close()
            return {
                'error': '需要登录',
                'message': '请先运行 --login 命令扫码登录',
                'qrcode_file': str(COOKIE_DIR / 'qichacha_login.png')
            }
        
        results = []
        
        # 提取搜索结果
        # 企查查的搜索结果结构
        try:
            # 方法1: 查找公司列表项
            items = page.locator('.search-result li, .company-list .item, .nsearch-list .item, [class*="company"]').all()
            
            for item in items[:limit]:
                try:
                    # 公司名称
                    name_el = item.locator('.company-name, .name, h3 a, [class*="name"]').first
                    name = name_el.inner_text() if name_el.count() > 0 else ""
                    
                    # 状态
                    status_el = item.locator('.status, [class*="status"]').first
                    status = status_el.inner_text() if status_el.count() > 0 else ""
                    
                    # 法人
                    legal_el = item.locator('.legal, [class*="legal"], .fr, [class*="person"]').first
                    legal = legal_el.inner_text() if legal_el.count() > 0 else ""
                    
                    # 资本
                    capital_el = item.locator('.capital, [class*="capital"]').first
                    capital = capital_el.inner_text() if capital_el.count() > 0 else ""
                    
                    # 链接
                    link_el = item.locator('a').first
                    href = link_el.get_attribute('href') if link_el.count() > 0 else ""
                    
                    if name:
                        results.append({
                            'name': name.strip(),
                            'status': status.strip(),
                            'legal_person': legal.strip(),
                            'capital': capital.strip(),
                            'url': f"https://www.qcc.com{href}" if href and not href.startswith('http') else href
                        })
                except Exception as e:
                    continue
        except Exception as e:
            pass
        
        # 如果没找到，尝试提取页面文本
        if not results:
            body_text = page.locator('body').inner_text()
            results = [{'raw_text': body_text[:2000], 'note': '需要登录查看完整数据'}]
        
        browser.close()
        return results

def get_company_detail(company_url):
    """获取企业详细信息"""
    from playwright.sync_api import sync_playwright
    
    cookies = load_cookies()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        if cookies:
            context.add_cookies(cookies)
        
        page = context.new_page()
        page.goto(company_url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(5)
        
        # 检查登录
        if 'weblogin' in page.url:
            browser.close()
            return {'error': '需要登录', 'message': '请先运行 --login 命令'}
        
        data = {
            'url': page.url,
            'title': page.title(),
            '需要登录': False,
            'basic_info': {}
        }
        
        # 提取基本信息
        try:
            # 基础信息区域
            base_info = page.locator('.company-detail, #company-detail, .base-info').first
            if base_info.count() > 0:
                data['basic_info']['html'] = base_info.inner_html()
                data['basic_info']['text'] = base_info.inner_text()
        except:
            pass
        
        # 检查是否需要VIP
        try:
            vip_tip = page.locator('.vip-tip, .login-tip, [class*="vip"]').first
            if vip_tip.count() > 0:
                data['需要登录'] = True
                data['vip_tip'] = vip_tip.inner_text()
        except:
            pass
        
        browser.close()
        return data

def main():
    parser = argparse.ArgumentParser(
        description='企查查数据抓取工具\n\n推荐方案：企查查MCP（官方API）\n  访问 https://agent.qcc.com 注册获取API Key\n  然后配置到OpenClaw插件中使用',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--login', action='store_true', help='二维码登录')
    parser.add_argument('--search', type=str, help='搜索企业')
    parser.add_argument('--company', type=str, help='企业详情URL')
    parser.add_argument('--limit', type=int, default=10, help='搜索结果数量限制')
    parser.add_argument('--output', '-o', choices=['text', 'json'], default='text')
    
    args = parser.parse_args()
    
    if args.login:
        success = login_with_qrcode()
        if success:
            print('\\n✅ 登录成功! Cookie已保存。')
            print('现在可以运行 --search 进行搜索了。')
        else:
            print('\\n❌ 登录失败或超时。')
            print(f'\\nQR码截图: {COOKIE_DIR / "qichacha_login.png"}')
        sys.exit(0 if success else 1)
    
    elif args.search:
        results = search_company(args.search, args.limit)
        if isinstance(results, dict) and 'error' in results:
            print(f"错误: {results['error']}")
            print(f"提示: {results['message']}")
            if 'qrcode_file' in results:
                print(f"QR码截图: {results['qrcode_file']}")
        elif args.output == 'json':
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"搜索 \"{args.search}\" 找到 {len(results)} 个结果:")
            for i, r in enumerate(results, 1):
                if 'raw_text' in r:
                    print(r['raw_text'])
                else:
                    print(f"\\n{i}. {r.get('name', 'N/A')}")
                    if r.get('status'): print(f"   状态: {r['status']}")
                    if r.get('legal_person'): print(f"   法人: {r['legal_person']}")
                    if r.get('capital'): print(f"   资本: {r['capital']}")
                    if r.get('url'): print(f"   URL: {r['url']}")
    
    elif args.company:
        detail = get_company_detail(args.company)
        if args.output == 'json':
            print(json.dumps(detail, ensure_ascii=False, indent=2))
        else:
            print(f"标题: {detail.get('title', 'N/A')}")
            print(f"URL: {detail.get('url', 'N/A')}")
            print(f"需要VIP: {detail.get('需要登录', False)}")
            if detail.get('basic_info', {}).get('text'):
                print(f"\\n基本信息:\\n{detail['basic_info']['text'][:1000]}")
    else:
        parser.print_help()
        print('\\n' + '='*50)
        print('推荐方案：企查查MCP（官方API）')
        print('  访问 https://agent.qcc.com 注册获取API Key')
        print('  然后配置到OpenClaw插件中使用')
        print('='*50)

if __name__ == '__main__':
    main()
