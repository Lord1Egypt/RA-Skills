#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编码处理脚本
用于获取和处理GBK/GB2312编码的网页内容
"""

import requests
from bs4 import BeautifulSoup
import sys
import re


def fetch_with_encoding(url: str) -> dict:
    """
    处理各种编码的网页

    Args:
        url: 目标URL

    Returns:
        dict: 包含content, encoding, success, error的字典
    """
    result = {
        "url": url,
        "content": "",
        "encoding": "utf-8",
        "success": False,
        "error": None
    }

    try:
        response = requests.get(url, timeout=30)
        encoding = response.encoding

        # 如果是ISO-8859-1（默认值），尝试从HTML内容检测
        if encoding and encoding.lower() in ['iso-8859-1', 'latin-1']:
            soup = BeautifulSoup(response.content, 'html.parser')
            meta = soup.find('meta', attrs={'charset': True})
            if meta:
                encoding = meta.get('charset')
            else:
                meta = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
                if meta and meta.get('content'):
                    encoding = meta.get('content').split('charset=')[-1].strip()

        # 常见中文编码映射
        encoding_map = {
            'gb2312': 'gb18030',
            'gbk': 'gb18030',
            'x-gbk': 'gb18030',
        }
        if encoding:
            encoding = encoding_map.get(encoding.lower(), encoding)
        else:
            encoding = 'utf-8'

        result["encoding"] = encoding

        # 解码并重新编码为UTF-8
        try:
            content = response.content.decode(encoding)
        except:
            content = response.content.decode('utf-8', errors='ignore')

        result["content"] = content
        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result


def extract_news(content: str, start_date: str, end_date: str) -> list:
    """
    从页面内容中提取新闻标题和日期
    """
    soup = BeautifulSoup(content, 'html.parser')
    news_list = []

    # 日期模式
    date_patterns = [
        r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)',
        r'(\d{1,2}[-/]\d{1,2})',
        r'(\d{2}月\d{2}日)',
        r'(\d{2}-\d{2})',
    ]

    # 查找新闻列表
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        href = a.get('href', '')

        # 跳过无效链接
        if len(text) < 10 or len(text) > 150:
            continue

        # 查找日期
        date = None
        parent = a.parent
        if parent:
            parent_text = parent.get_text()
            for pattern in date_patterns:
                match = re.search(pattern, parent_text)
                if match:
                    date = match.group(1)
                    break

        if text:
            news_list.append({
                "title": text,
                "date": date or "未知",
                "url": href
            })

    # 去重
    seen = set()
    unique_news = []
    for item in news_list:
        key = item["title"]
        if key not in seen:
            seen.add(key)
            unique_news.append(item)

    return unique_news[:20]


def main():
    if len(sys.argv) < 2:
        print("Usage: python encoding_fetch.py <url> [start_date] [end_date]")
        print("  url        - 目标网页 URL")
        print("  start_date - 起始日期（YYYY-MM-DD），默认 30 天前")
        print("  end_date   - 结束日期（YYYY-MM-DD），默认今天")
        sys.exit(1)

    from datetime import datetime, timedelta

    url = sys.argv[1]
    start_date = sys.argv[2] if len(sys.argv) > 2 else (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y-%m-%d")

    print(f"Fetching: {url}")
    print(f"Date range: {start_date} ~ {end_date}")

    result = fetch_with_encoding(url)

    if result["success"]:
        print(f"\nDetected encoding: {result['encoding']}")
        print(f"Content length: {len(result['content'])} characters")

        # 提取新闻
        news = extract_news(result["content"], start_date, end_date)

        if news:
            print(f"\n=== Found {len(news)} items ===")
            for i, item in enumerate(news, 1):
                print(f"{i}. [{item['date']}] {item['title'][:80]}")
        else:
            print("\nNo items found.")
            print("\nFirst 500 chars:")
            print(result["content"][:500])
    else:
        print(f"\nError: {result['error']}")


if __name__ == "__main__":
    main()