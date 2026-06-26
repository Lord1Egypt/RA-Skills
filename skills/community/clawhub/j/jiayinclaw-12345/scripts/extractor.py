#!/usr/bin/env python3
"""
网页内容提取器技能脚本
从指定URL提取网页的标题、正文、图片、链接等结构化内容
"""

import sys
import json
import re
import argparse
from urllib.parse import urlparse, urljoin
from html import unescape
from datetime import datetime

def validate_url(url):
    """
    验证URL格式是否合法
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def clean_text(text):
    """
    清理文本内容，移除多余空白字符
    """
    if not text:
        return ""
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def extract_content(html_content, base_url):
    """
    从HTML内容中提取各类信息
    """
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取标题
    title = ""
    title_tag = soup.find('title')
    if title_tag:
        title = clean_text(title_tag.get_text())
    
    # 提取meta描述
    meta_desc = ""
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag:
        meta_desc = clean_text(meta_tag.get('content', ''))
    
    # 提取正文内容
    # 移除脚本和样式
    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()
    
    # 查找主要内容区域
    main_content = ""
    main_tag = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|article|post|entry'))
    if main_tag:
        main_content = clean_text(main_tag.get_text())
    else:
        body = soup.find('body')
        if body:
            main_content = clean_text(body.get_text())
    
    # 截断过长内容
    max_length = 5000
    if len(main_content) > max_length:
        main_content = main_content[:max_length] + "..."
    
    # 提取图片链接
    images = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
        if src:
            # 处理相对链接
            if not src.startswith(('http://', 'https://')):
                src = urljoin(base_url, src)
            images.append(src)
    
    # 提取链接
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if not href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
            href = urljoin(base_url, href)
        link_text = clean_text(link.get_text())
        if href.startswith('http'):
            links.append({"url": href, "text": link_text[:100]})
    
    # 去重链接
    seen = set()
    unique_links = []
    for item in links:
        if item['url'] not in seen:
            seen.add(item['url'])
            unique_links.append(item)
    links = unique_links[:50]  # 限制链接数量
    
    return {
        "url": base_url,
        "title": title,
        "meta_description": meta_desc,
        "content": main_content,
        "images": images[:20],  # 限制图片数量
        "links": links,
        "extracted_at": datetime.now().isoformat(),
        "stats": {
            "images_count": len(images),
            "links_count": len(links),
            "content_length": len(main_content)
        }
    }

def fetch_url(url):
    """
    获取网页内容
    """
    import requests
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    
    return response.text

def main():
    """
    主函数，处理命令行参数并执行提取
    """
    parser = argparse.ArgumentParser(description='网页内容提取器')
    parser.add_argument('url', nargs='?', help='要提取的网页URL')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    parser.add_argument('--no-images', action='store_true', help='不提取图片')
    parser.add_argument('--no-links', action='store_true', help='不提取链接')
    
    args = parser.parse_args()
    
    try:
        # 获取URL
        url = args.url
        if not url:
            url = input("请输入要提取的网页URL：").strip()
        
        if not url:
            print("错误：请提供有效的URL")
            sys.exit(1)
        
        # 添加协议前缀
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 验证URL
        if not validate_url(url):
            print("错误：URL格式无效")
            sys.exit(1)
        
        print(f"正在提取：{url}", file=sys.stderr)
        
        # 获取网页内容
        html = fetch_url(url)
        
        # 提取内容
        result = extract_content(html, url)
        
        # 根据参数过滤结果
        if args.no_images:
            result['images'] = []
            result['stats']['images_count'] = 0
        if args.no_links:
            result['links'] = []
            result['stats']['links_count'] = 0
        
        # 输出结果
        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 文本格式输出
            print(f"\n标题：{result['title']}")
            print(f"描述：{result['meta_description']}")
            print(f"\n正文内容：\n{result['content']}")
            if not args.no_images:
                print(f"\n图片数量：{result['stats']['images_count']}")
                for img in result['images'][:5]:
                    print(f"  - {img}")
            if not args.no_links:
                print(f"\n链接数量：{result['stats']['links_count']}")
        
        print(f"\n提取完成！", file=sys.stderr)
        
    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(0)
    except ImportError as e:
        print(f"错误：缺少必要的依赖库 - {e}", file=sys.stderr)
        print("请运行：pip install requests beautifulsoup4", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"提取失败：{str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
