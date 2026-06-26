#!/usr/bin/env python3
"""妈妈网育儿知识爬虫 - 爬取文章存入御知库"""
import sys
import re
import os
import json
import time
import random
import argparse
from pathlib import Path
from datetime import datetime

# 御知库路径
YUZHI_KB = Path.home() / ".yuzhi"
CRAWL_DIR = YUZHI_KB / "crawls" / "mama_cn"
CRAWL_DIR.mkdir(parents=True, exist_ok=True)

# 反爬：请求间隔（秒）
MIN_DELAY = 2
MAX_DELAY = 5

# 模拟浏览器 User-Agent
UA_MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
UA_PC = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
UA = UA_PC  # 默认 PC 端

# 分类配置（PC 端）
CATEGORIES = {
    "baby":  {"name": "亲子", "url": "https://www.mama.cn/z/baby/"},
    "yingyang": {"name": "营养", "url": "https://www.mama.cn/z/yingyang/"},
    "disease": {"name": "疾病", "url": "https://www.mama.cn/z/disease/"},
    "lady":   {"name": "女性", "url": "https://www.mama.cn/z/lady/"},
    "yongpin": {"name": "用品", "url": "https://www.mama.cn/z/yongpin/"},
    "life":   {"name": "生活", "url": "https://www.mama.cn/z/life/"},
}

# 搜索关键词列表（用于爬取）
SEARCH_KEYWORDS = ["育儿", "怀孕", "备孕", "新生儿", "孕妇", "月子", "亲子教育"]

def get(url, timeout=15):
    """发送 HTTP GET 请求（使用 curl 避免 SSL 问题）"""
    import subprocess
    result = subprocess.run(
        ["curl", "-s", "--max-time", str(timeout),
         "-A", UA, "-k",  # -k: 不验证 SSL 证书（妈妈网证书问题）
         url],
        capture_output=True, text=True
    )
    return result.stdout

def extract_article_urls(html):
    """从列表页提取文章 URL（PC: www.mama.cn/z/art/<id>/）"""
    # 匹配 PC 文章 URL: https://www.mama.cn/z/art/<id>/
    pattern = r'href="(https://www\.mama\.cn/z/art/\d+)/"'
    matches = re.findall(pattern, html)
    urls = list(dict.fromkeys(matches))  # 去重保持顺序
    return urls

def extract_article_content(html, url):
    """从文章页提取正文"""
    # 提取标题
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = ""
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    if not title:
        title_match = re.search(r'<title>(.*?)</title>', html)
        if title_match:
            title = title_match.group(1).split('_')[0].strip()

    # 提取正文区域（PC: detail-mod > mod-ctn，移动: rich-text）
    content = ""
    raw = None
    # PC: 提取 mod-ctn 内部所有文本（可能有嵌套 div）
    mod_ctn = re.search(r'<div class="mod-ctn">(.*)</div>\s*</div>\s*<div style=', html, re.DOTALL)
    if mod_ctn:
        raw = mod_ctn.group(1)
    if not raw:
        # 移动端
        for pattern in [
            r'<div[^>]*class="g-area rich-text"[^>]*>(.*?)</div>\s*<div',
            r'<div[^>]*class="rich-text[^"]*"[^>]*>(.*?)</div>\s*</div>',
            r'<div[^>]*class="rich-text[^"]*"[^>]*>(.*?)</div>',
        ]:
            content_match = re.search(pattern, html, re.DOTALL)
            if content_match and len(content_match.group(1)) > 50:
                raw = content_match.group(1)
                break

    if raw:
        # 替换块级标签为换行
        for tag in ['</p>', '</h1>', '</h2>', '</h3>', '</h4>', '</li>', '</tr>']:
            raw = raw.replace(tag, '\n')
        raw = raw.replace('<br\s*/?>', '\n', re.DOTALL)
        # 去除所有标签
        content = re.sub(r'<[^>]+>', '', raw)
        content = re.sub(r'\n{3,}', '\n\n', content).strip()

    # 如果仍然为空，从 meta description 提取
    if not content or len(content) < 50:
        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"', html)
        if desc_match:
            content = desc_match.group(1)

    # 提取发布时间
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', html)
    pub_date = date_match.group(1) if date_match else ""

    # 提取来源
    source_match = re.search(r'来源[:：]\s*([^\s<，,]+)', html)
    source = source_match.group(1) if source_match else "妈妈网"

    return {
        "title": title,
        "content": content,
        "pub_date": pub_date,
        "source": source,
        "url": url
    }

def html_to_markdown(title, content, url, source, pub_date, category):
    """转换为 Markdown 格式"""
    md = f"""# {title}

**分类**: {category} | **来源**: {source} | **日期**: {pub_date}
**链接**: {url}

---

{content}

---
*本文由妈妈网爬虫自动采集，存入御知库*
"""
    return md

def save_article(md_content, title, category):
    """保存文章到本地"""
    # 清理文件名
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)[:50]
    if not safe_title.strip():
        safe_title = f"article_{int(time.time())}"
    filename = CRAWL_DIR / category / f"{safe_title}.md"
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.write_text(md_content, encoding="utf-8")
    return filename

def crawl_category(cat_key, cat_info, max_pages=3, max_articles=20):
    """爬取单个分类"""
    print(f"\n📂 开始爬取分类: {cat_info['name']} ({cat_key})")
    base_url = cat_info["url"]
    fetched = 0
    seen_urls = set()

    for page in range(1, max_pages + 1):
        if fetched >= max_articles:
            break
        page_url = f"{base_url}?page={page}" if page > 1 else base_url
        print(f"  📄 第 {page} 页: {page_url}")
        html = get(page_url)
        if not html:
            continue

        # 提取文章 URL（列表页直接有链接）
        article_urls = extract_article_urls(html)
        print(f"     找到 {len(article_urls)} 个文章链接")

        for url in article_urls:
            if url in seen_urls or fetched >= max_articles:
                continue
            seen_urls.add(url)

            # 反爬延迟
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"  ⏳ 等待 {delay:.1f}s ...")
            time.sleep(delay)

            article_html = get(url + "/")
            if not article_html:
                continue

            article = extract_article_content(article_html, url)
            if not article["content"] or len(article["content"]) < 100:
                print(f"     ⚠️ 内容过短，跳过: {url}")
                continue

            md = html_to_markdown(
                article["title"], article["content"],
                article["url"], article["source"],
                article["pub_date"], cat_info["name"]
            )
            path = save_article(md, article["title"], cat_info["name"])
            print(f"  ✅ 已保存: {article['title'][:40]}...")
            fetched += 1

    print(f"  📊 {cat_info['name']} 分类完成，共获取 {fetched} 篇文章")
    return fetched

def crawl_search(keyword, max_results=20):
    """通过搜索爬取文章"""
    import urllib.parse
    print(f"\n🔍 搜索关键词: {keyword}")
    seen_urls = set()
    fetched = 0
    page = 1

    while fetched < max_results:
        encoded_key = urllib.parse.quote(keyword)
        search_url = f"https://www.mama.cn/search/?key={encoded_key}&page={page}"
        print(f"  📄 第 {page} 页...")
        html = get(search_url)
        if not html:
            break

        article_urls = extract_article_urls(html)
        if not article_urls:
            break
        print(f"     找到 {len(article_urls)} 个链接")

        # 如果所有 URL 都已见过，说明到底了，停止翻页
        new_urls = [u for u in article_urls if u not in seen_urls]
        if not new_urls:
            print(f"     所有文章已爬取，停止翻页")
            break

        for url in article_urls:
            if url in seen_urls or fetched >= max_results:
                continue
            seen_urls.add(url)

            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"  ⏳ 等待 {delay:.1f}s ... 抓取: {url}")
            time.sleep(delay)

            article_html = get(url + "/")
            if not article_html:
                continue

            article = extract_article_content(article_html, url)
            if not article["content"] or len(article["content"]) < 100:
                continue

            md = html_to_markdown(
                article["title"], article["content"],
                article["url"], article["source"],
                article["pub_date"], "育儿"
            )
            path = save_article(md, article["title"], "育儿")
            print(f"  ✅ 已保存: {article['title'][:40]}...")
            fetched += 1

        page += 1

    print(f"  📊 搜索完成，共获取 {fetched} 篇文章")
    return fetched

def main():
    parser = argparse.ArgumentParser(description="妈妈网育儿知识爬虫")
    parser.add_argument("--category", choices=list(CATEGORIES.keys()), help="爬取指定分类")
    parser.add_argument("--search", help="搜索关键词爬取")
    parser.add_argument("--max-pages", type=int, default=3, help="最大页数")
    parser.add_argument("--max-articles", type=int, default=20, help="最大文章数")
    parser.add_argument("--all", action="store_true", help="爬取所有分类")
    args = parser.parse_args()

    total = 0
    if args.all:
        for cat_key, cat_info in CATEGORIES.items():
            total += crawl_category(cat_key, cat_info, args.max_pages, args.max_articles)
    elif args.category:
        cat_info = CATEGORIES[args.category]
        total = crawl_category(args.category, cat_info, args.max_pages, args.max_articles)
    elif args.search:
        total = crawl_search(args.search, args.max_articles)
    else:
        # 默认爬取亲子分类
        total = crawl_category("baby", CATEGORIES["baby"], args.max_pages, args.max_articles)

    print(f"\n🎉 爬取完成，共获取 {total} 篇文章")
    print(f"📁 保存位置: {CRAWL_DIR}")

if __name__ == "__main__":
    main()
