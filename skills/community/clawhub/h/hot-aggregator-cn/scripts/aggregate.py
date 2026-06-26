#!/usr/bin/env python3
"""
全平台热点聚合器
All-Platform Hot Topics Aggregator
"""

import json
import sys
from datetime import datetime

# 模拟各平台数据
PLATFORMS = {
    "weibo": {
        "name": "微博",
        "emoji": "📱",
        "topics": [
            {"rank": 1, "title": "春节档票房破100亿", "hot": 9876543},
            {"rank": 2, "title": "AI大模型最新突破", "hot": 8765432},
            {"rank": 3, "title": "春运返程高峰", "hot": 7654321},
        ]
    },
    "zhihu": {
        "name": "知乎",
        "emoji": "💙",
        "topics": [
            {"rank": 1, "title": "AI会取代程序员吗？", "hot": 8765432},
            {"rank": 2, "title": "如何评价春节档电影？", "hot": 7654321},
            {"rank": 3, "title": "2026年投资建议", "hot": 6543210},
        ]
    },
    "baidu": {
        "name": "百度",
        "emoji": "🔍",
        "topics": [
            {"rank": 1, "title": "春节档电影票房", "hot": 1234567},
            {"rank": 2, "title": "AI技术新进展", "hot": 987654},
            {"rank": 3, "title": "春运最新消息", "hot": 876543},
        ]
    },
    "douyin": {
        "name": "抖音",
        "emoji": "🎵",
        "topics": [
            {"rank": 1, "title": "春节拜年视频", "hot": 8765432},
            {"rank": 2, "title": "新年穿搭", "hot": 7654321},
            {"rank": 3, "title": "AI特效挑战", "hot": 6543210},
        ]
    },
    "bilibili": {
        "name": "B站",
        "emoji": "📺",
        "topics": [
            {"rank": 1, "title": "春节联欢晚会鬼畜", "hot": 7654321},
            {"rank": 2, "title": "新年动漫推荐", "hot": 6543210},
            {"rank": 3, "title": "AI视频创作", "hot": 5432109},
        ]
    }
}

def get_all_platforms(limit=3):
    """获取所有平台热点"""
    result = {}
    for key, platform in PLATFORMS.items():
        result[key] = {
            "name": platform["name"],
            "emoji": platform["emoji"],
            "topics": platform["topics"][:limit]
        }
    return result

def find_common_topics(data, keyword=None):
    """查找共同话题"""
    all_titles = []
    for platform_data in data.values():
        for topic in platform_data["topics"]:
            all_titles.append(topic["title"])
    
    # 简单关键词匹配
    if keyword:
        matches = [t for t in all_titles if keyword.lower() in t.lower()]
        return matches
    return []

def format_aggregated(data):
    output = "🔥 全平台热点聚合\n\n"
    for key, platform in data.items():
        output += f"{platform['emoji']} {platform['name']} Top 3:\n"
        for topic in platform["topics"]:
            hot_str = f"{topic['hot'] / 10000:.0f}万"
            output += f"  {topic['rank']}. {topic['title']} ({hot_str})\n"
        output += "\n"
    return output

def main():
    limit = 3
    keyword = None
    
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
        elif arg not in ["--json", "-j"]:
            keyword = arg
    
    data = get_all_platforms(limit=limit)
    
    if "--json" in sys.argv or "-j" in sys.argv:
        result = {"platforms": data, "timestamp": datetime.now().isoformat()}
        if keyword:
            result["keyword_matches"] = find_common_topics(data, keyword)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_aggregated(data))
        if keyword:
            matches = find_common_topics(data, keyword)
            if matches:
                print(f"🔍 关键词 '{keyword}' 相关热点:")
                for m in matches:
                    print(f"  - {m}")

if __name__ == "__main__":
    main()
