#!/usr/bin/env python3
"""
保险产品页面文字抓取
从保险产品网页链接中提取条款文本
用法: python web_scrape.py <url> [--output <output_txt>]
"""

import argparse
import os
import re
import sys
import html as html_module


def extract_text_from_html(body_text, url):
    """从HTML中提取纯净文本"""
    import re

    # 移除 script 和 style 内容
    body_text = re.sub(r'<script[^>]*>.*?</script>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<style[^>]*>.*?</style>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<noscript[^>]*>.*?</noscript>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<svg[^>]*>.*?</svg>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<nav[^>]*>.*?</nav>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<footer[^>]*>.*?</footer>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<header[^>]*>.*?</header>', '', body_text, flags=re.DOTALL | re.IGNORECASE)
    body_text = re.sub(r'<aside[^>]*>.*?</aside>', '', body_text, flags=re.DOTALL | re.IGNORECASE)

    # 移除所有HTML标签
    body_text = re.sub(r'<[^>]+>', '\n', body_text)

    # 解码HTML实体
    import html as html_module
    body_text = html_module.unescape(body_text)

    # 清理多余空白
    body_text = re.sub(r'[ \t]+', ' ', body_text)
    body_text = re.sub(r'\n\s*\n', '\n\n', body_text)
    body_text = body_text.strip()

    return body_text


def scrape_with_requests(url):
    """使用 requests 抓取网页内容"""
    try:
        import requests
        from bs4 import BeautifulSoup

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        resp = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')

        # 移除不可见元素
        for tag in soup.find_all(['script', 'style', 'noscript', 'svg', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()

        # 提取body
        body = soup.body
        if body is None:
            body = soup

        text = body.get_text('\n', strip=False)
        text = html_module.unescape(text)

        # 清理多余空白
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()

        return text

    except ImportError as e:
        missing = str(e).split("'")[1] if "'" in str(e) else "未知模块"
        print(f"[提示] {missing} 未安装。正在尝试安装...", file=sys.stderr)
        import subprocess
        install_cmd = []
        if 'requests' in missing or 'bs4' in missing or 'beautifulsoup4' in missing:
            install_cmd = ["pip", "install", "requests", "beautifulsoup4",
                          "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/",
                          "--trusted-host", "pypi.tuna.tsinghua.edu.cn"]
        if install_cmd:
            subprocess.check_call(
                [sys.executable] + install_cmd[1:],
                stdout=sys.stderr, stderr=sys.stderr)
            return scrape_with_requests(url)
        raise
    except Exception as e:
        return f"[错误] 网页抓取失败: {e}"


def main():
    parser = argparse.ArgumentParser(description='保险产品页面文字抓取')
    parser.add_argument('url', help='保险产品页面URL')
    parser.add_argument('--output', '-o', help='输出文本文件路径')

    args = parser.parse_args()

    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"正在抓取: {url}", file=sys.stderr)

    text = scrape_with_requests(url)

    if not text or not text.strip():
        print("[警告] 未能提取到有效的文字内容。可能的原因：\n1. 页面需要JavaScript渲染\n2. 页面包含验证码或反爬机制\n3. URL无效或需要登录")
        text = f"[提示] 未能从 {url} 提取到有效内容。建议手动复制页面文字后粘贴分析。"

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"内容已保存至: {args.output}", file=sys.stderr)
    else:
        print(text)


if __name__ == '__main__':
    main()
