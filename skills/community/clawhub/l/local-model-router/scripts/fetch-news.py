#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tech News Fetcher with Translation - 输出格式优化版
"""

import feedparser
import json
import os
from datetime import datetime

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "defaults")

def load_sources():
    sources_file = os.path.join(CONFIG_DIR, "sources.json")
    with open(sources_file, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_to_chinese(text):
    """翻译文本到中文"""
    if not text:
        return ""
    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source='auto', target='zh-CN')
        if len(text) > 500:
            parts = [text[i:i+500] for i in range(0, len(text), 500)]
            translated_parts = [translator.translate(p) for p in parts]
            return "".join(translated_parts)
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def fetch_rss(url):
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:8]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")[:300]
            
            title_cn = translate_to_chinese(title)
            summary_cn = translate_to_chinese(summary)
            
            items.append({
                "title": title,
                "title_cn": title_cn,
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": summary,
                "summary_cn": summary_cn
            })
        return items
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def format_news_for_display(news_list):
    """格式化新闻为中文摘要"""
    output = []
    output.append("=" * 60)
    output.append("[NEWS] Tech News Summary")
    output.append("=" * 60)
    
    for i, news in enumerate(news_list[:10], 1):
        output.append(f"\n### {i}. {news['title_cn']}")
        output.append(f"- **来源:** {news['source']}")
        output.append(f"- **链接:** {news['link']}")
        if news.get('summary_cn'):
            output.append(f"- **摘要:** {news['summary_cn'][:150]}...")
    
    output.append("\n" + "=" * 60)
    return "\n".join(output)

def main():
    print("Fetching tech news...")
    print("=" * 50)
    
    sources = load_sources()
    all_news = []
    
    for source in sources.get("sources", []):
        if source.get("enabled") and source.get("type") == "rss":
            print(f"[Fetch] {source['name']}")
            items = fetch_rss(source["url"])
            for item in items:
                item["source"] = source["name"]
                item["topics"] = source.get("topics", [])
            all_news.extend(items)
            print(f"   -> {len(items)} news")
    
    # 保存 JSON
    output_file = os.path.join(os.path.dirname(__file__), "workspace", "tech-news.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    print("=" * 50)
    print(f"[OK] Total: {len(all_news)} news")
    print(f"[File] Saved: {output_file}")
    
    # 打印中文摘要
    print(format_news_for_display(all_news))
    
    # 保存摘要文本
    summary_file = os.path.join(os.path.dirname(__file__), "workspace", "tech-news-summary.md")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(format_news_for_display(all_news))
    print(f"\n[File] Summary saved: {summary_file}")

if __name__ == "__main__":
    main()
