#!/usr/bin/env python3
"""
提取脚本 - 从 HTML 中解析文章信息
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


DEFAULT_OUTPUT_DIR = "data/extracted"


def parse_score(score_text: str) -> int:
    """解析分数文本为数字"""
    if not score_text:
        return 0
    # 提取数字
    numbers = re.findall(r'\d+', score_text.replace(',', ''))
    return int(numbers[0]) if numbers else 0


def parse_time(time_text: str) -> Optional[str]:
    """解析时间文本为 ISO 格式"""
    if not time_text:
        return None
    
    # 尝试解析各种时间格式
    time_patterns = [
        (r'(\d+)\s*hours?\s+ago', lambda m: f"{int(m.group(1))} hours ago"),
        (r'(\d+)\s*minutes?\s+ago', lambda m: f"{int(m.group(1))} minutes ago"),
        (r'(\d+)\s*days?\s+ago', lambda m: f"{int(m.group(1))} days ago"),
    ]
    
    for pattern, _ in time_patterns:
        match = re.search(pattern, time_text, re.IGNORECASE)
        if match:
            return time_text.strip()
    
    return time_text.strip()


def categorize_article(title: str, url: str) -> str:
    """根据标题和 URL 对文章进行分类"""
    title_lower = title.lower()
    url_lower = url.lower()
    
    categories = {
        "AI": ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "neural", "llm", "gpt", "chatgpt", "claude", "model"],
        "Programming": ["programming", "code", "developer", "software", "github", "api", "framework", "library"],
        "Startup": ["startup", "venture", "funding", "invest", "series", "seed", "ipo", "acquisition"],
        "Science": ["science", "research", "paper", "study", "experiment", "physics", "biology"],
        "Security": ["security", "privacy", "hack", "vulnerability", "breach", "encryption", "cyber"],
        "Hardware": ["hardware", "chip", "gpu", "cpu", "semiconductor", "device", "robot"],
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in url_lower:
                return category
    
    return "Other"


def extract_article_from_element(element: BeautifulSoup, base_url: str) -> Optional[Dict[str, Any]]:
    """
    从单个文章元素中提取信息
    
    Args:
        element: BeautifulSoup 元素
        base_url: 基础 URL
        
    Returns:
        文章字典或 None
    """
    article = {}
    
    try:
        # 尝试多种常见的文章标题选择器
        title_elem = (
            element.select_one('.title a') or
            element.select_one('.storylink') or
            element.select_one('a.title') or
            element.select_one('h2 a') or
            element.select_one('.titleline > a') or
            element.select_one('a[href^="http"]')
        )
        
        if not title_elem:
            return None
        
        article['title'] = title_elem.get_text(strip=True)
        href = title_elem.get('href', '')
        
        # 处理相对链接
        if href.startswith('http'):
            article['url'] = href
        elif href.startswith('/'):
            article['url'] = urljoin(base_url, href)
        else:
            article['url'] = urljoin(base_url, href)
        
        # 提取分数
        score_elem = (
            element.select_one('.score') or
            element.select_one('.points') or
            element.select_one('[class*="score"]') or
            element.select_one('[class*="point"]')
        )
        if score_elem:
            article['score'] = parse_score(score_elem.get_text())
        else:
            article['score'] = 0
        
        # 提取评论数
        comment_elem = (
            element.select_one('a[href*="comments"]') or
            element.select_one('.comments') or
            element.select_one('[class*="comment"]')
        )
        if comment_elem:
            comment_text = comment_elem.get_text()
            numbers = re.findall(r'\d+', comment_text)
            article['comments_count'] = int(numbers[0]) if numbers else 0
        else:
            article['comments_count'] = 0
        
        # 提取发布时间
        time_elem = (
            element.select_one('.age') or
            element.select_one('.time') or
            element.select_one('[class*="time"]') or
            element.select_one('time')
        )
        if time_elem:
            article['published_at'] = parse_time(time_elem.get_text())
        else:
            article['published_at'] = None
        
        # 提取作者
        author_elem = (
            element.select_one('.hnuser') or
            element.select_one('.author') or
            element.select_one('[class*="user"]') or
            element.select_one('a[href^="user"]')
        )
        if author_elem:
            article['author'] = author_elem.get_text(strip=True)
        else:
            article['author'] = None
        
        # 提取摘要/来源网站
        source_elem = (
            element.select_one('.sitestr') or
            element.select_one('.source') or
            element.select_one('.domain')
        )
        if source_elem:
            article['source_site'] = source_elem.get_text(strip=True)
        else:
            # 从 URL 解析域名
            parsed = urlparse(article['url'])
            article['source_site'] = parsed.netloc.replace('www.', '')
        
        # 分类
        article['category'] = categorize_article(article['title'], article['url'])
        
        # 提取时间戳
        article['extracted_at'] = datetime.now().isoformat()
        
        return article
        
    except Exception as e:
        print(f"[Extract] 解析文章时出错: {e}", file=sys.stderr)
        return None


def extract_articles(html_content: str, base_url: str = "https://hn.aimaker.dev/") -> List[Dict[str, Any]]:
    """
    从 HTML 内容中提取所有文章
    
    Args:
        html_content: HTML 内容
        base_url: 基础 URL
        
    Returns:
        文章列表
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []
    
    # 尝试多种常见的文章列表选择器
    selectors = [
        '.item',           # Hacker News 风格
        '.story',          # 通用
        '.post',           # 通用
        '.article',        # 通用
        'tr.athing',       # Hacker News 特定
        '.news-item',      # 通用
        'article',         # HTML5
        '.entry',          # 通用
    ]
    
    article_elements = []
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            article_elements = elements
            print(f"[Extract] 使用选择器 '{selector}' 找到 {len(elements)} 个元素")
            break
    
    # 如果没有找到，尝试从表格行中提取
    if not article_elements:
        # 查找包含链接的行
        all_links = soup.find_all('a', href=True)
        print(f"[Extract] 尝试从 {len(all_links)} 个链接中提取")
        
        # 过滤出可能是文章标题的链接
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # 跳过导航链接
            if len(text) > 10 and href.startswith('http'):
                parent = link.find_parent(['tr', 'div', 'article', 'li'])
                if parent and parent not in article_elements:
                    article_elements.append(parent)
    
    print(f"[Extract] 开始解析 {len(article_elements)} 个元素...")
    
    for element in article_elements:
        article = extract_article_from_element(element, base_url)
        if article and article.get('title') and len(article['title']) > 5:
            articles.append(article)
    
    # 去重（基于 URL）
    seen_urls = set()
    unique_articles = []
    for article in articles:
        if article['url'] not in seen_urls:
            seen_urls.add(article['url'])
            unique_articles.append(article)
    
    print(f"[Extract] 成功提取 {len(unique_articles)} 篇文章（去重后）")
    
    return unique_articles


def save_articles(articles: List[Dict[str, Any]], output_dir: str, source_file: str = None) -> Path:
    """
    保存文章到 JSON 文件
    
    Args:
        articles: 文章列表
        output_dir: 输出目录
        source_file: 源文件路径
        
    Returns:
        保存的文件路径
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"articles_{timestamp}.json"
    file_path = output_path / filename
    
    data = {
        "articles": articles,
        "metadata": {
            "extracted_at": datetime.now().isoformat(),
            "total_count": len(articles),
            "source_file": str(source_file) if source_file else None,
            "source_url": "https://hn.aimaker.dev/"
        }
    }
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[Extract] 数据已保存到: {file_path}")
    
    return file_path


def main():
    parser = argparse.ArgumentParser(
        description="从 HTML 中提取文章信息"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="输入 HTML 文件路径（默认从 data/raw/ 目录查找最新文件）"
    )
    parser.add_argument(
        "--output-dir",
        default=os.getenv("OUTPUT_DIR", DEFAULT_OUTPUT_DIR),
        help=f"输出目录 (默认: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--base-url",
        default="https://hn.aimaker.dev/",
        help="基础 URL"
    )
    
    args = parser.parse_args()
    
    try:
        # 确定输入文件
        if args.input_file:
            input_path = Path(args.input_file)
        else:
            # 查找最新的 HTML 文件
            raw_dir = Path("data/raw")
            if raw_dir.exists():
                html_files = sorted(raw_dir.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
                if html_files:
                    input_path = html_files[0]
                    print(f"[Extract] 使用最新的 HTML 文件: {input_path}")
                else:
                    print("[Extract] 错误: 未找到 HTML 文件", file=sys.stderr)
                    return 1
            else:
                print("[Extract] 错误: data/raw/ 目录不存在", file=sys.stderr)
                return 1
        
        # 读取 HTML
        print(f"[Extract] 正在读取: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 提取文章
        articles = extract_articles(html_content, args.base_url)
        
        if not articles:
            print("[Extract] 警告: 未提取到任何文章", file=sys.stderr)
            return 1
        
        # 保存结果
        output_path = save_articles(articles, args.output_dir, input_path)
        
        print(f"[Extract] 完成！输出文件: {output_path}")
        print(f"OUTPUT_FILE:{output_path}")
        
        return 0
        
    except Exception as e:
        print(f"[Extract] 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
