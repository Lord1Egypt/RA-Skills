#!/usr/bin/env python3
"""
锂电设备推广平台搜索脚本
多引擎搜索目标国家的展会、B2B平台、行业媒体
"""

import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# 搜索配置
SEARCH_ENGINES = {
    "bing_cn": "https://cn.bing.com/search?q={query}&ensearch=0",
    "bing_intl": "https://cn.bing.com/search?q={query}&ensearch=1",
}

COUNTRY_QUERIES = {
    "US": {
        "exhibition": [
            "battery show USA 2025 2026",
            "The Battery Show North America",
            "lithium battery exhibition America",
            "energy storage conference USA",
        ],
        "b2b": [
            "B2B platform battery equipment USA",
            "industrial equipment marketplace US",
            "battery manufacturing equipment suppliers USA",
        ],
        "media": [
            "battery industry news USA",
            "EV battery media America",
            "energy storage news US",
        ],
    },
    "JP": {
        "exhibition": [
            "battery show Japan 2025",
            "Battery Japan Tokyo",
            "smart energy week Japan",
        ],
        "b2b": [
            "Japan B2B battery equipment platform",
            "Monozukuri B2B platform battery",
        ],
        "media": [
            "battery japan news",
            "Japan energy storage media",
        ],
    },
    "KR": {
        "exhibition": [
            "InterBattery 2025 2026",
            "Korea battery exhibition",
            "K-Battery Show",
        ],
        "b2b": [
            "Korea B2B platform battery equipment",
            "EC21 Korea battery",
            "KoreaTrade battery",
        ],
        "media": [
            "Korea battery industry news",
            "The Elec battery Korea",
        ],
    },
    "RU": {
        "exhibition": [
            "battery exhibition Russia 2025",
            "Power Electronics Russia",
            "Renwex Russia energy",
        ],
        "b2b": [
            "Russia B2B battery equipment",
            "Tiu.ru battery",
            "Pulscen Russia B2B",
        ],
        "media": [
            "battery news Russia",
            "Russia energy storage media",
        ],
    },
    "EU": {
        "exhibition": [
            "The Battery Show Europe 2025",
            "battery exhibition Germany",
            "Energy Storage Europe",
        ],
        "b2b": [
            "European B2B battery equipment marketplace",
            "Kompass battery equipment Europe",
            "Europages battery machinery",
        ],
        "media": [
            "battery industry news Europe",
            "Energy Storage News EU",
            "Batteries International magazine",
        ],
    },
}


def build_search_url(query, engine="bing_intl"):
    """构建搜索URL"""
    encoded = urllib.parse.quote(query)
    return SEARCH_ENGINES[engine].format(query=encoded)


def search_platforms(country="ALL", platform_type="all"):
    """
    生成搜索任务列表
    
    Args:
        country: US/JP/KR/RU/EU/ALL
        platform_type: exhibition/b2b/media/all
    
    Returns:
        list: 搜索任务列表，每个任务包含url、country、type、query
    """
    tasks = []
    
    countries = [country] if country != "ALL" else list(COUNTRY_QUERIES.keys())
    types = [platform_type] if platform_type != "all" else ["exhibition", "b2b", "media"]
    
    for c in countries:
        if c not in COUNTRY_QUERIES:
            continue
        for t in types:
            if t not in COUNTRY_QUERIES[c]:
                continue
            for query in COUNTRY_QUERIES[c][t]:
                url = build_search_url(query)
                tasks.append({
                    "country": c,
                    "type": t,
                    "query": query,
                    "search_url": url,
                    "engine": "bing_intl",
                })
    
    return tasks


def save_search_tasks(tasks, output_dir=None):
    """保存搜索任务到JSON"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"search_tasks_{timestamp}.json"
    
    data = {
        "generated_at": datetime.now().isoformat(),
        "total_tasks": len(tasks),
        "tasks": tasks,
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"搜索任务已保存: {output_file}")
    print(f"共 {len(tasks)} 个搜索任务")
    
    # 按国家/类型统计
    stats = {}
    for t in tasks:
        key = f"{t['country']}/{t['type']}"
        stats[key] = stats.get(key, 0) + 1
    
    print("\n任务分布:")
    for key, count in sorted(stats.items()):
        print(f"  {key}: {count} 个任务")
    
    return output_file


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="锂电设备推广平台搜索")
    parser.add_argument("--country", default="ALL", choices=["US", "JP", "KR", "RU", "EU", "ALL"],
                        help="目标国家")
    parser.add_argument("--type", default="all", choices=["exhibition", "b2b", "media", "all"],
                        help="平台类型")
    parser.add_argument("--output", default=None, help="输出目录")
    
    args = parser.parse_args()
    
    print(f"开始生成搜索任务: country={args.country}, type={args.type}")
    
    tasks = search_platforms(args.country, args.type)
    
    if not tasks:
        print("没有找到匹配的搜索任务")
        return 1
    
    output_file = save_search_tasks(tasks, args.output)
    
    # 打印前5个任务示例
    print("\n前5个搜索任务:")
    for i, t in enumerate(tasks[:5], 1):
        print(f"  {i}. [{t['country']}/{t['type']}] {t['query']}")
        print(f"     URL: {t['search_url']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
