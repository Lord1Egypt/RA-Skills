#!/usr/bin/env python3
"""
RSS 新闻源获取器 - 获取RSS feed中的新闻列表
"""
import sys
import json
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
from urllib.error import URLError

def fetch_rss(url, timeout=30):
    """获取RSS feed"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error: {e}"

def parse_rss(xml_content, max_items=10):
    """解析RSS XML"""
    try:
        root = ET.fromstring(xml_content)
        
        # 处理不同格式的RSS
        items = []
        
        # RSS 2.0
        for item in root.findall('.//item')[:max_items]:
            title = item.find('title')
            link = item.find('link')
            desc = item.find('description') or item.find('summary')
            pub_date = item.find('pubDate') or item.find('published')
            
            items.append({
                "title": title.text if title is not None else "",
                "link": link.text if link is not None else "",
                "description": desc.text if desc is not None else "",
                "published": pub_date.text if pub_date is not None else ""
            })
        
        return items
    except Exception as e:
        return [{"error": str(e)}]

def main():
    if len(sys.argv) < 2:
        # 默认使用一些中文新闻源
        default_sources = {
            "tech": "https://www.techweb.com.cn/rss/all.xml",
            "36kr": "https://36kr.com/feed",
            "solidot": "https://www.solidot.org/index.rss"
        }
        print(json.dumps({"sources": default_sources}, ensure_ascii=False))
        return
    
    url = sys.argv[1]
    max_items = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    xml = fetch_rss(url)
    if xml.startswith("Error"):
        print(json.dumps({"error": xml}, ensure_ascii=False))
        sys.exit(1)
    
    items = parse_rss(xml, max_items)
    print(json.dumps({"items": items, "count": len(items)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
