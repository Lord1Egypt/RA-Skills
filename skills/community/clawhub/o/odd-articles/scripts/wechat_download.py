#!/usr/bin/env python3
"""
微信文章抓取脚本
WeChat Article Fetcher

用于从微信公众平台抓取文章内容。
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from html import unescape
from datetime import datetime


def get_wechat_headers():
    """获取微信请求头，模拟浏览器访问"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
    }


def extract_article_id(url: str) -> str:
    """从URL中提取文章ID"""
    # 匹配各种微信文章URL格式
    patterns = [
        r'/(appmsg.*?)\?',  # /appmsg/v4?
        r'/s\?.*?(mid=\w+)',  # /s?mid=
        r'/s\?.*?(sn=\w+)',  # /s?sn=
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # 尝试直接从完整URL获取
    if 'mp.weixin.qq.com' in url:
        # 从URL中提取关键参数
        match = re.search(r'mid=(\w+)', url)
        if match:
            return match.group(1)
        match = re.search(r'sn=(\w+)', url)
        if match:
            return match.group(1)
    
    return ''


def fetch_article(url: str) -> dict:
    """抓取微信文章"""
    headers = get_wechat_headers()
    request = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return {
            'success': False,
            'error': f'HTTP Error: {e.code}',
            'message': '微信文章抓取失败，请尝试手动复制文章正文'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': '网络错误，请检查网络连接'
        }
    
    # 解析HTML
    article = parse_html(html, url)
    article['fetched_at'] = datetime.utcnow().isoformat() + 'Z'
    
    return {
        'success': True,
        'article': article
    }


def parse_html(html: str, url: str) -> dict:
    """解析微信文章HTML"""
    article = {
        'url': url,
        'title': '',
        'author': '',
        'content': '',
        'content_html': '',
        'publish_date': '',
        'source': '',
        'cover_image': '',
        'images': []
    }
    
    # 提取标题
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        article['title'] = unescape(title_match.group(1))
    
    # 提取作者
    author_match = re.search(r'["\']author["\']\s*:\s*["\']([^"\']+)["\']', html)
    if author_match:
        article['author'] = author_match.group(1)
    
    # 提取发布时间
    date_match = re.search(r'["\']pub_date["\']\s*:\s*["\']([^"\']+)["\']', html)
    if date_match:
        article['publish_date'] = date_match.group(1)
    
    # 提取封面图
    cover_match = re.search(r'["\']cover["\']\s*:\s*["\']([^"\']+\.(?:jpg|png|webp))["\']', html, re.I)
    if cover_match:
        article['cover_image'] = cover_match.group(1)
    
    # 提取正文内容 - 尝试多种方式
    content_match = re.search(r'id="js_content"[^>]*>([\s\S]*?)</div>', html)
    if content_match:
        content_html = content_match.group(1)
        article['content_html'] = content_html
        
        # 提取纯文本
        content_text = re.sub(r'<[^>]+>', '', content_html)
        content_text = unescape(content_text)
        content_text = re.sub(r'\s+', ' ', content_text).strip()
        article['content'] = content_text
        
        # 提取所有图片
        img_matches = re.findall(r'<img[^>]+src="([^"]+)"', content_html)
        article['images'] = [img for img in img_matches if 'mmbiz' in img or 'qpic' in img]
    
    # 提取摘要
    digest_match = re.search(r'["\']digest["\']\s*:\s*["\']([^"\']*)["\']', html)
    if digest_match:
        article['digest'] = digest_match.group(1)
    
    return article


def main():
    parser = argparse.ArgumentParser(description='抓取微信文章')
    parser.add_argument('url', help='微信文章URL')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    result = fetch_article(args.url)
    
    if args.json:
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"已保存到: {args.output}")
        else:
            print(output)
    else:
        if result['success']:
            article = result['article']
            print(f"标题: {article['title']}")
            print(f"作者: {article['author']}")
            print(f"发布日期: {article['publish_date']}")
            print(f"字数: {len(article['content'])}")
            print(f"图片数: {len(article['images'])}")
            print(f"\n内容预览:\n{article['content'][:500]}...")
        else:
            print(f"错误: {result.get('message', result.get('error', '未知错误'))}")
            return 1
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())