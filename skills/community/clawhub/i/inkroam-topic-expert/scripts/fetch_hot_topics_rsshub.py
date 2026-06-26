#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取热点数据 - 使用 RSSHub
支持：微博、知乎、36氪、虎嗅、少数派等
"""

import json
import requests
from datetime import datetime
import sys
import feedparser


# RSSHub 公共实例
RSSHUB_BASE = "https://rsshub.app"

# 数据源配置
DATA_SOURCES = {
    "weibo": {
        "url": f"{RSSHUB_BASE}/weibo/search/hot",
        "name": "微博热搜"
    },
    "zhihu": {
        "url": f"{RSSHUB_BASE}/zhihu/hotlist",
        "name": "知乎热榜"
    },
    "36kr": {
        "url": f"{RSSHUB_BASE}/36kr/newsflashes",
        "name": "36氪快讯"
    },
    "huxiu": {
        "url": f"{RSSHUB_BASE}/huxiu/article",
        "name": "虎嗅资讯"
    },
    "sspai": {
        "url": f"{RSSHUB_BASE}/sspai/matrix",
        "name": "少数派"
    },
    "github": {
        "url": f"{RSSHUB_BASE}/github/trending/daily",
        "name": "GitHub Trending"
    }
}


def fetch_rss_feed(url, source_name):
    """获取 RSS feed"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        
        print(f"正在获取 {source_name}...", file=sys.stderr)
        
        # 使用 feedparser 解析 RSS
        feed = feedparser.parse(url)
        
        items = []
        for idx, entry in enumerate(feed.entries[:20], 1):
            items.append({
                "rank": idx,
                "title": entry.get('title', ''),
                "url": entry.get('link', ''),
                "summary": entry.get('summary', ''),
                "published": entry.get('published', ''),
                "source": source_name
            })
        
        print(f"✓ {source_name}：{len(items)} 条", file=sys.stderr)
        return items
        
    except Exception as e:
        print(f"✗ {source_name} 获取失败: {e}", file=sys.stderr)
        return []


def main():
    """主函数"""
    print("正在获取热点数据...\n", file=sys.stderr)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "sources": {}
    }
    
    total_count = 0
    
    # 获取所有数据源
    for source_key, source_config in DATA_SOURCES.items():
        items = fetch_rss_feed(source_config["url"], source_config["name"])
        result["sources"][source_key] = items
        total_count += len(items)
    
    result["total"] = total_count
    
    # 输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到文件
    output_file = "/tmp/hot_topics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 获取成功：共 {total_count} 条", file=sys.stderr)
    print(f"数据已保存到：{output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
