#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tech News Daily Digest - 每日自动推送版
"""

import feedparser
import json
import os
import re
from datetime import datetime

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "defaults")

def load_sources():
    sources_file = os.path.join(CONFIG_DIR, "sources.json")
    with open(sources_file, "r", encoding="utf-8") as f:
        return json.load(f)

def translate_to_chinese(text):
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
    except:
        return text

def clean_html(text):
    """清理 HTML 标签"""
    return re.sub(r'<[^>]+>', '', text)

def fetch_rss(url):
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:8]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")[:300]
            title_cn = translate_to_chinese(title)
            summary_cn = clean_html(translate_to_chinese(summary))
            items.append({
                "title": title,
                "title_cn": title_cn,
                "link": entry.get("link", ""),
                "summary_cn": summary_cn,
                "source": ""
            })
        return items
    except:
        return []

def generate_digest():
    sources = load_sources()
    all_news = []
    
    for source in sources.get("sources", []):
        if source.get("enabled") and source.get("type") == "rss":
            items = fetch_rss(source["url"])
            for item in items:
                item["source"] = source["name"]
            all_news.extend(items)
    
    # 生成摘要
    output = []
    output.append("=" * 50)
    output.append("[DAILY] Tech News Digest")
    output.append("=" * 50)
    
    for i, news in enumerate(all_news[:10], 1):
        output.append(f"\n### {i}. {news['title_cn']}")
        output.append(f"- 来源: {news['source']}")
        output.append(f"- 链接: {news['link']}")
        if news.get('summary_cn'):
            output.append(f"- 摘要: {news['summary_cn'][:120]}...")
    
    digest = "\n".join(output)
    
    # 保存
    output_file = os.path.join(os.path.dirname(__file__), "workspace", "tech-news.json")
    summary_file = os.path.join(os.path.dirname(__file__), "workspace", "daily-digest.txt")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(digest)
    
    return digest

if __name__ == "__main__":
    print(generate_digest())
