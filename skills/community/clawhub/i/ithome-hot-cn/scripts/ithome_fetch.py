#!/usr/bin/env python3
"""
IT之家热门获取脚本
IT Home Hot News Fetcher
"""

import json
import sys

def get_ithome_hot(limit=10):
    """获取IT之家热门（模拟数据）"""
    mock_news = [
        {"id": 1, "title": "华为 P70 Pro 评测：影像能力再升级", "category": "手机", "views": 253000, "comments": 567},
        {"id": 2, "title": "英特尔 15 代酷睿发布，性能提升 20%", "category": "电脑", "views": 187000, "comments": 432},
        {"id": 3, "title": "苹果 iPhone 16 系列销量不及预期", "category": "手机", "views": 165000, "comments": 389},
        {"id": 4, "title": "小米 15 Ultra 渲染图曝光", "category": "手机", "views": 143000, "comments": 321},
        {"id": 5, "title": "英伟达 RTX 5090 规格泄露", "category": "电脑", "views": 132000, "comments": 298},
        {"id": 6, "title": "特斯拉 Model 3 改款上市", "category": "汽车", "views": 121000, "comments": 267},
        {"id": 7, "title": "索尼 PS6 发布时间确认", "category": "游戏", "views": 98000, "comments": 234},
        {"id": 8, "title": "高通骁龙 8 Gen 4 跑分曝光", "category": "手机", "views": 87000, "comments": 198},
        {"id": 9, "title": "三星 Galaxy S26 Ultra 评测", "category": "手机", "views": 76000, "comments": 176},
        {"id": 10, "title": "Meta Quest 4 发布，支持混合现实", "category": "智能硬件", "views": 65000, "comments": 154},
    ]
    return mock_news[:limit]

def format_output(data):
    output = "📱 IT之家今日热榜\n\n"
    for item in data:
        views_w = f"{item['views'] / 10000:.1f}万"
        output += f"{item['id']}. {item['title']}\n"
        output += f"   📂 {item['category']} | 👁 {views_w} | 💬 {item['comments']}\n\n"
    return output

def main():
    limit = 10
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
    
    data = get_ithome_hot(limit=limit)
    
    if "--json" in sys.argv or "-j" in sys.argv:
        print(json.dumps({"data": data}, ensure_ascii=False, indent=2))
    else:
        print(format_output(data))

if __name__ == "__main__":
    main()
