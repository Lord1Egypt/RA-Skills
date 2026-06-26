#!/usr/bin/env python3
"""
新闻爬虫脚本 - 爬取指定URL的新闻并生成摘要
"""
import sys
import json
import re
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
        self.in_script = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.in_script = True
            
    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script = False
            
    def handle_data(self, d):
        if not self.in_script:
            self.fed.append(d)
            
    def get_data(self):
        return ''.join(self.fed)

def strip_html(html):
    s = HTMLStripper()
    try:
        s.feed(html)
        return s.get_data()
    except:
        return re.sub('<[^<]+?>', '', html)

def fetch_url(url, timeout=30):
    """获取URL内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except URLError as e:
        return f"Error fetching {url}: {e}"
    except Exception as e:
        return f"Error: {e}"

def extract_text(html, max_length=5000):
    """从HTML中提取纯文本"""
    text = strip_html(html)
    # 清理空白
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)
    # 限制长度
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: news_crawler.py <url> [max_length]"}, ensure_ascii=False))
        sys.exit(1)
    
    url = sys.argv[1]
    max_length = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    
    html = fetch_url(url)
    if html.startswith("Error"):
        print(json.dumps({"error": html}, ensure_ascii=False))
        sys.exit(1)
    
    text = extract_text(html, max_length)
    
    result = {
        "url": url,
        "title": "",  # 可由调用者进一步解析
        "content": text,
        "length": len(text)
    }
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
