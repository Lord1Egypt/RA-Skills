#!/usr/bin/env python3
"""文章管线：下载网页 → 提取正文 → Markdown化"""
import requests, sys, json
from bs4 import BeautifulSoup
from readability import Document
import html2text

def extract_article(url: str) -> dict:
    """获取网页并提取正文"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.encoding = resp.apparent_encoding
    
    # readability 提取正文
    doc = Document(resp.text)
    title = doc.title()
    html_content = doc.summary()
    
    # 转 markdown
    converter = html2text.HTML2Text()
    converter.body_width = 0
    markdown = converter.handle(html_content)
    
    # 提取元信息
    soup = BeautifulSoup(resp.text, "html.parser")
    description = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        description = meta_desc.get("content", "")
    
    return {
        "title": title,
        "description": description,
        "content": markdown,
        "url": url,
        "chars": len(markdown)
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 extract_article.py <文章URL>")
        sys.exit(1)
    result = extract_article(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
