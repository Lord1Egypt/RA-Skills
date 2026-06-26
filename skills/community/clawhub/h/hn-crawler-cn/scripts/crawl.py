#!/usr/bin/env python3
"""
爬取脚本 - 获取 hn.aimaker.dev 网站原始 HTML 内容
"""

import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


DEFAULT_URL = "https://hn.aimaker.dev/"
DEFAULT_TIMEOUT = 30
DEFAULT_OUTPUT_DIR = "data/raw"


def create_session():
    """创建带有重试机制的 HTTP Session"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def crawl_website(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    爬取指定 URL 的网页内容
    
    Args:
        url: 目标 URL
        timeout: 请求超时时间
        
    Returns:
        网页 HTML 内容
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    session = create_session()
    
    print(f"[Crawl] 正在爬取: {url}")
    
    try:
        response = session.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True
        )
        response.raise_for_status()
        
        print(f"[Crawl] 成功获取页面，状态码: {response.status_code}")
        print(f"[Crawl] 内容长度: {len(response.text)} 字符")
        
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"[Crawl] 爬取失败: {e}", file=sys.stderr)
        raise


def save_html(html_content: str, output_dir: str, url: str) -> Path:
    """
    保存 HTML 内容到文件
    
    Args:
        html_content: HTML 内容
        output_dir: 输出目录
        url: 来源 URL
        
    Returns:
        保存的文件路径
    """
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"{domain}_{timestamp}.html"
    
    file_path = output_path / filename
    
    # 保存文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"[Crawl] HTML 已保存到: {file_path}")
    
    return file_path


def main():
    parser = argparse.ArgumentParser(
        description="爬取 hn.aimaker.dev 网站内容"
    )
    parser.add_argument(
        "--url",
        default=os.getenv("TARGET_URL", DEFAULT_URL),
        help=f"目标 URL (默认: {DEFAULT_URL})"
    )
    parser.add_argument(
        "--output-dir",
        default=os.getenv("OUTPUT_DIR", DEFAULT_OUTPUT_DIR),
        help=f"输出目录 (默认: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.getenv("TIMEOUT", DEFAULT_TIMEOUT)),
        help=f"请求超时时间 (默认: {DEFAULT_TIMEOUT}秒)"
    )
    parser.add_argument(
        "--output-file",
        help="指定输出文件路径（可选，默认自动生成）"
    )
    
    args = parser.parse_args()
    
    try:
        # 爬取网页
        html_content = crawl_website(args.url, args.timeout)
        
        # 保存文件
        if args.output_file:
            output_path = Path(args.output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"[Crawl] HTML 已保存到: {output_path}")
            saved_path = output_path
        else:
            saved_path = save_html(html_content, args.output_dir, args.url)
        
        print(f"[Crawl] 完成！文件路径: {saved_path}")
        
        # 输出文件路径供其他脚本使用
        print(f"OUTPUT_FILE:{saved_path}")
        
        return 0
        
    except Exception as e:
        print(f"[Crawl] 错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
