#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Playwright获取动态渲染后的网页内容
用于处理JavaScript依赖的网站
"""

from playwright.sync_api import sync_playwright
import sys
import json

def fetch_dynamic_page(url: str, wait_time: int = 5000) -> dict:
    """
    使用Playwright获取动态渲染后的页面内容

    Args:
        url: 目标URL
        wait_time: 等待时间(毫秒)，默认5秒

    Returns:
        dict: 包含title, content, success, error的字典
    """
    result = {
        "url": url,
        "title": "",
        "content": "",
        "success": False,
        "error": None
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page()

                # 设置超时时间
                page.set_default_timeout(30000)  # 30秒

                # 访问页面
                page.goto(url, wait_until='networkidle')

                # 额外等待动态内容加载
                page.wait_for_timeout(wait_time)

                # 获取页面标题
                result["title"] = page.title()

                # 获取渲染后的HTML内容
                result["content"] = page.content()

                result["success"] = True
            finally:
                browser.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def extract_news_from_content(content: str, start_date: str, end_date: str) -> list:
    """
    从页面内容中提取新闻标题和日期

    Args:
        content: 页面HTML内容
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)

    Returns:
        list: 新闻列表 [{"title": "", "date": ""}, ...]
    """
    from bs4 import BeautifulSoup
    import re
    from datetime import datetime

    soup = BeautifulSoup(content, 'html.parser')
    news_list = []

    # 查找所有包含日期的文本
    date_pattern = r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?|\d{1,2}[-/]\d{1,2}|\d{2}月\d{2}日)'

    # 查找常见的新闻列表结构
    # 1. <li> 列表项
    for li in soup.find_all('li'):
        text = li.get_text(strip=True)
        date_match = re.search(date_pattern, text)
        if date_match and len(text) > 10 and len(text) < 200:
            title = re.sub(date_pattern, '', text).strip()
            if title:
                news_list.append({
                    "title": title[:100],  # 限制标题长度
                    "date": date_match.group(1)
                })

    # 2. <a> 链接
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        if len(text) > 10 and len(text) < 100:
            # 检查附近是否有日期
            parent = a.parent
            if parent:
                parent_text = parent.get_text()
                date_match = re.search(date_pattern, parent_text)
                if date_match:
                    news_list.append({
                        "title": text,
                        "date": date_match.group(1)
                    })

    # 去重
    seen = set()
    unique_news = []
    for item in news_list:
        key = (item["title"], item["date"])
        if key not in seen:
            seen.add(key)
            unique_news.append(item)

    return unique_news[:20]  # 返回最多20条


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python playwright_fetch.py <url> [wait_time_ms] [start_date] [end_date]")
        print("  url          - 目标网页 URL")
        print("  wait_time_ms - 等待时间（毫秒），默认 5000")
        print("  start_date   - 起始日期（YYYY-MM-DD），默认 30 天前")
        print("  end_date     - 结束日期（YYYY-MM-DD），默认今天")
        sys.exit(1)

    from datetime import datetime, timedelta

    url = sys.argv[1]
    wait_time = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    start_date = sys.argv[3] if len(sys.argv) > 3 else (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = sys.argv[4] if len(sys.argv) > 4 else datetime.now().strftime("%Y-%m-%d")

    print(f"Fetching: {url}")
    print(f"Wait time: {wait_time}ms")
    print(f"Date range: {start_date} ~ {end_date}")

    result = fetch_dynamic_page(url, wait_time)

    if result["success"]:
        print(f"\n=== Page Title: {result['title']} ===")
        print(f"\nContent length: {len(result['content'])} characters")

        # 提取新闻
        news = extract_news_from_content(result["content"], start_date, end_date)

        if news:
            print(f"\n=== Found {len(news)} news items ===")
            for i, item in enumerate(news, 1):
                print(f"{i}. [{item['date']}] {item['title']}")
        else:
            print("\nNo news items found in expected format.")
            print("\nFirst 500 chars of content:")
            print(result["content"][:500])
    else:
        print(f"\nError: {result['error']}")


if __name__ == "__main__":
    main()