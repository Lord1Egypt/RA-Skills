#!/usr/bin/env python3
"""
热点提醒器
Hot Topics Alert System
"""

import json
import sys
from datetime import datetime

# 模拟热搜数据
HOT_TOPICS = {
    "weibo": [
        {"title": "AI大模型最新突破", "rank": 2, "hot": 8765432},
        {"title": "春节档票房破100亿", "rank": 1, "hot": 9876543},
    ],
    "zhihu": [
        {"title": "AI会取代程序员吗？", "rank": 1, "hot": 8765432},
    ],
    "baidu": [
        {"title": "AI技术新进展", "rank": 2, "hot": 987654},
    ]
}

def check_keyword(keyword):
    """检查关键词是否在热搜"""
    results = []
    for platform, topics in HOT_TOPICS.items():
        for topic in topics:
            if keyword.lower() in topic["title"].lower():
                results.append({
                    "platform": platform,
                    "title": topic["title"],
                    "rank": topic["rank"],
                    "hot": topic["hot"]
                })
    return results

def format_alert(keyword, results):
    if not results:
        return f"ℹ️ 关键词 '{keyword}' 暂未上热搜"
    
    output = f"🔔 热点提醒！\n\n关键词 \"{keyword}\" 已登上热搜：\n\n"
    for r in results:
        hot_w = f"{r['hot'] / 10000:.1f}万"
        output += f"📱 {r['platform']} #{r['rank']}\n"
        output += f"   {r['title']}\n"
        output += f"   热度：{hot_w}\n\n"
    
    output += "💡 建议：现在可以发相关内容获取流量！"
    return output

def main():
    if len(sys.argv) < 2:
        print("用法: hot_alert.py <关键词>")
        sys.exit(1)
    
    keyword = sys.argv[1]
    results = check_keyword(keyword)
    
    if "--json" in sys.argv or "-j" in sys.argv:
        print(json.dumps({"keyword": keyword, "results": results}, ensure_ascii=False, indent=2))
    else:
        print(format_alert(keyword, results))

if __name__ == "__main__":
    main()
