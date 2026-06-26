#!/usr/bin/env python3
"""
KET News Fetcher
抓取KET级别英语新闻文章，支持JavaScript渲染
"""

import argparse
import os
import sys
import re
import json
import subprocess
import asyncio
from datetime import datetime
from requests_html import AsyncHTMLSession

# KET 词汇表（简化版）
KET_VOCABULARY = set([
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could", "should",
    "i", "me", "my", "you", "your", "he", "him", "his", "she", "her", "it", "its",
    "we", "us", "our", "they", "them", "their",
    "what", "which", "who", "this", "that", "these", "those",
    "and", "but", "or", "if", "then", "when", "where", "why", "how",
    "all", "each", "every", "both", "some", "any", "no", "not", "only",
    "book", "read", "write", "word", "talk", "speak", "say", "tell", "ask", "answer",
    "look", "see", "watch", "hear", "listen", "think", "know", "understand",
    "feel", "like", "want", "need", "love", "hate",
    "come", "go", "move", "walk", "run", "eat", "drink", "buy", "sell",
    "make", "put", "keep", "take", "get", "give", "send", "let", "may", "can",
    "house", "home", "school", "work", "city", "country", "world",
    "people", "man", "woman", "child", "children", "boy", "girl", "friend", "family",
    "money", "time", "year", "day", "week", "month", "today", "tomorrow", "yesterday",
    "good", "bad", "big", "small", "new", "old", "first", "last", "next",
    "car", "bus", "train", "plane", "ship", "boat",
    "water", "food", "money", "number",
    "news", "newspaper", "story", "information",
    "happy", "sad", "angry", "worried", "interesting",
    "important", "difficult", "easy", "different", "same",
    "right", "wrong", "true", "false", "real",
])

SOURCES = {
    "nil1": {
        "name": "News in Levels 1",
        "url": "https://www.newsinlevels.com/level-1/",
        "level": "KET"
    },
    "nil2": {
        "name": "News in Levels 2",
        "url": "https://www.newsinlevels.com/level-2/",
        "level": "KET-PET"
    },
    "nil3": {
        "name": "News in Levels 3",
        "url": "https://www.newsinlevels.com/level-3/",
        "level": "PET"
    },
    "bbc": {
        "name": "BBC Learning English",
        "url": "https://www.bbc.co.uk/learningenglish/english/course/lower-intermediate",
        "level": "KET-PET"
    },
    "voa": {
        "name": "VOA Learning English",
        "url": "https://learningenglish.voanews.com/english/learning-english",
        "level": "KET"
    }
}


async def fetch_with_js(url, session):
    """使用JavaScript渲染获取页面"""
    try:
        response = await session.get(url)
        await response.html.arender(timeout=30)
        return response.html.html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_news_in_levels(html, level=1):
    """解析News in Levels页面"""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    articles = []
    
    # 查找文章链接
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/world-' in href or '/news-' in href or '/story-' in href:
            if href.startswith('http'):
                title = link.get_text(strip=True)
                if title and len(title) > 5:
                    articles.append({
                        "title": title,
                        "url": href,
                        "source": "News in Levels",
                        "level": f"Level {level}"
                    })
    
    return articles[:10]  # 限制数量


def parse_bbc_le(html):
    """解析BBC Learning English页面"""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    articles = []
    
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/news/' in href or '/learningenglish/' in href:
            full_url = f"https://www.bbc.co.uk{href}" if href.startswith('/') else href
            title = link.get_text(strip=True)
            if title and len(title) > 10:
                articles.append({
                    "title": title,
                    "url": full_url,
                    "source": "BBC Learning English",
                    "level": "KET-PET"
                })
    
    return articles[:10]


def analyze_vocabulary(text):
    """分析文章词汇"""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    ket_words = [w for w in words if w in KET_VOCABULARY]
    non_ket = [w for w in words if w not in KET_VOCABULARY and len(w) > 3]
    
    total = len(words)
    ket_count = len(ket_words)
    coverage = (ket_count / total * 100) if total > 0 else 0
    
    return {
        "total_words": total,
        "ket_words": ket_count,
        "ket_coverage": round(coverage, 1),
        "non_ket_examples": list(set(non_ket))[:10]
    }


def save_article(article, output_dir):
    """保存文章"""
    os.makedirs(output_dir, exist_ok=True)
    
    filename = re.sub(r'[^\w\s-]', '', article.get('title', 'untitled'))
    filename = re.sub(r'\s+', '_', filename)[:50]
    
    # 保存原文
    txt_path = os.path.join(output_dir, f"{filename}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"Title: {article.get('title', 'N/A')}\n")
        f.write(f"Source: {article.get('source', 'N/A')}\n")
        f.write(f"Level: {article.get('level', 'N/A')}\n")
        f.write(f"URL: {article.get('url', 'N/A')}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("\n" + "="*50 + "\n\n")
        f.write(article.get('content', article.get('title', '')))
    
    return txt_path


async def fetch_articles(source_key, count=5):
    """获取文章列表"""
    source = SOURCES.get(source_key, SOURCES['bbc'])
    url = source['url']
    
    print(f"正在获取: {source['name']}")
    print(f"URL: {url}")
    
    session = AsyncHTMLSession()
    html = await fetch_with_js(url, session)
    
    if not html:
        print(f"获取失败: {url}")
        return []
    
    # 解析页面
    if 'newsinlevels' in url:
        level = 1 if 'level-1' in url else 2 if 'level-2' in url else 3
        articles = parse_news_in_levels(html, level)
    elif 'bbc' in url:
        articles = parse_bbc_le(html)
    else:
        articles = []
    
    return articles


def main():
    parser = argparse.ArgumentParser(description='KET News Fetcher')
    parser.add_argument('--source', '-s', default='bbc',
                        choices=['nil1', 'nil2', 'nil3', 'bbc', 'voa', 'all'],
                        help='新闻来源')
    parser.add_argument('--count', '-c', type=int, default=5,
                        help='获取数量')
    parser.add_argument('--output', '-o', default='/tmp/ket_news',
                        help='输出目录')
    
    args = parser.parse_args()
    
    print("="*50)
    print("KET News Fetcher - 英语新闻抓取工具")
    print("="*50)
    print()
    
    sources = ['nil1', 'nil2', 'nil3', 'bbc', 'voa'] if args.source == 'all' else [args.source]
    
    all_articles = []
    
    for src in sources:
        articles = asyncio.run(fetch_articles(src, args.count))
        all_articles.extend(articles)
        print(f"找到 {len(articles)} 篇 ({SOURCES[src]['name']})")
        print()
    
    if not all_articles:
        print("未找到文章，请检查网络连接")
        return
    
    print(f"总共找到 {len(all_articles)} 篇文章")
    print()
    
    # 保存文章
    output_dir = args.output
    saved = []
    
    for i, article in enumerate(all_articles[:args.count]):
        print(f"[{i+1}] {article.get('title', 'N/A')[:60]}...")
        print(f"    来源: {article.get('source')} | 级别: {article.get('level')}")
        print(f"    URL: {article.get('url', 'N/A')[:80]}")
        
        # 保存
        path = save_article(article, output_dir)
        saved.append(path)
        print(f"    已保存: {path}")
        print()
    
    print("="*50)
    print(f"完成！文章保存于: {output_dir}")
    print("="*50)


if __name__ == "__main__":
    main()
