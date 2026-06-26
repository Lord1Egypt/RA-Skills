"""获取仪表盘概览数据"""
import os
import sys
import json
import argparse
import requests

BASE_URL = os.getenv("NEWS_API_BASE_URL", "http://localhost:8030/api/v1")
HEADERS = {"Authorization": "Bearer PharmaBlock Gateway"}


def get_dashboard():
    resp = requests.get(f"{BASE_URL}/dashboard", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def format_output(data):
    d = data.get("data", {})
    print("\n📊 新闻智能体仪表盘\n")

    print("📈 数据概览")
    print(f"  新闻总数: {d.get('total_articles', 0)}")
    print(f"  今日新增: {d.get('today_articles', 0)}")
    cat_dist = d.get("category_distribution", [])
    hot_kw = d.get("hot_keywords", [])
    print(f"  分类数量: {len(cat_dist)}")
    print(f"  热门关键词: {len(hot_kw)}")

    if cat_dist:
        print(f"\n📁 分类分布")
        for c in cat_dist:
            print(f"  {c['name']}: {c['count']} 篇")

    if hot_kw:
        print(f"\n🔥 热词 TOP{len(hot_kw)}")
        max_count = max(k["count"] for k in hot_kw) if hot_kw else 1
        for i, k in enumerate(hot_kw, 1):
            bar_len = int(k["count"] / max_count * 20)
            bar = "█" * bar_len
            print(f"  {i:>2}. {k['keyword']:<12} {bar} {k['count']}")

    daily = d.get("daily_counts", [])
    if daily:
        print(f"\n📅 近7日采集量")
        for dc in daily:
            print(f"  {dc['date']}: {dc['count']} 篇")

    latest = d.get("latest_articles", [])
    if latest:
        print(f"\n📰 最新新闻")
        for a in latest:
            cat = f"[{a['category_name']}] " if a.get("category_name") else ""
            print(f"  • {cat}{a['title']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="获取仪表盘概览数据")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    try:
        data = get_dashboard()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            format_output(data)
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
