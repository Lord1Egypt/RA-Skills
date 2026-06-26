#!/usr/bin/env python3
"""
huo15-js-scraper - JavaScript渲染网站抓取工具
基于Playwright，支持stealth模式和scrapling降级
"""
import argparse
import json
import sys
import time
from pathlib import Path

def scrape_with_playwright(url, selector=None, wait=5, headless=True, output_format='text'):
    """使用Playwright抓取JS渲染页面"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        
        # 设置User-Agent
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        page.goto(url, wait_until='networkidle')
        time.sleep(wait)
        
        if selector:
            content = page.locator(selector).inner_text()
        else:
            content = page.locator('body').inner_text()
        
        result = {
            'url': page.url,
            'title': page.title(),
            'content': content,
            'engine': 'playwright'
        }
        
        browser.close()
        return result


def scrape_with_scrapling(url, selector=None, mode='dynamic', wait=3):
    """使用scrapling抓取（降级方案）"""
    try:
        from scrapling.fetchers import DynamicFetcher
        
        page = DynamicFetcher.fetch(url, headless=True, network_idle=True)
        time.sleep(wait)
        
        if selector:
            content = ''.join(page.css(f'{selector} *::text').getall())
        else:
            content = ''.join(page.css('body *::text').getall())
        
        return {
            'url': page.url,
            'title': page.css('title::text').get() or '',
            'content': content,
            'engine': 'scrapling'
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'engine': 'scrapling'
        }


def main():
    parser = argparse.ArgumentParser(description='JS渲染网站抓取工具')
    parser.add_argument('url', help='目标URL')
    parser.add_argument('--selector', '-s', help='CSS选择器')
    parser.add_argument('--wait', '-w', type=int, default=3, help='等待秒数')
    parser.add_argument('--engine', '-e', choices=['playwright', 'scrapling', 'auto'], default='auto')
    parser.add_argument('--output', '-o', choices=['text', 'json'], default='text')
    parser.add_argument('--stealth', action='store_true', help='隐身模式')
    
    args = parser.parse_args()
    
    # 自动选择引擎
    if args.engine == 'auto':
        # 优先playwright，更稳定
        try:
            result = scrape_with_playwright(args.url, args.selector, args.wait)
        except Exception as e:
            print(f"Playwright失败，尝试scrapling: {e}", file=sys.stderr)
            result = scrape_with_scrapling(args.url, args.selector)
    elif args.engine == 'playwright':
        result = scrape_with_playwright(args.url, args.selector, args.wait)
    else:
        result = scrape_with_scrapling(args.url, args.selector)
    
    # 输出
    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"URL: {result.get('url', 'N/A')}")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Engine: {result.get('engine', 'N/A')}")
        print("-" * 50)
        print(result.get('content', result.get('error', 'No content')))


if __name__ == '__main__':
    main()
