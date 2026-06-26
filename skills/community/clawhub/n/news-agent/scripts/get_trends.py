"""趋势分析 - 热词排行、关键词趋势、分类趋势"""
import os
import sys
import json
import argparse
import requests

BASE_URL = os.getenv("NEWS_API_BASE_URL", "http://localhost:8030/api/v1")
HEADERS = {"Authorization": "Bearer PharmaBlock Gateway"}


def get_hot(days=7, top_n=20):
    resp = requests.get(f"{BASE_URL}/trends/hot", headers=HEADERS,
                        params={"days": days, "top_n": top_n}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_keyword(keyword, days=30):
    resp = requests.get(f"{BASE_URL}/trends/keyword", headers=HEADERS,
                        params={"keyword": keyword, "days": days}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_category(days=30):
    resp = requests.get(f"{BASE_URL}/trends/category", headers=HEADERS,
                        params={"days": days}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def format_hot(data, days):
    items = data.get("data", [])
    print(f"\n🔥 热词排行 TOP{len(items)} (近{days}天)\n")
    if not items:
        print("  暂无热词数据")
        return
    max_count = max(i["count"] for i in items)
    for idx, item in enumerate(items, 1):
        bar_len = int(item["count"] / max_count * 20) if max_count else 0
        bar = "█" * bar_len
        print(f" {idx:>2}. {item['keyword']:<14} {bar} {item['count']}")
    print()


def format_keyword(data, keyword):
    items = data.get("data", [])
    print(f"\n📈 关键词趋势: {keyword} (共 {len(items)} 天)\n")
    if not items:
        print("  暂无趋势数据")
        return
    max_count = max(i["count"] for i in items) if items else 1
    for item in items:
        bar_len = int(item["count"] / max_count * 30) if max_count else 0
        bar = "█" * bar_len
        print(f"  {item['date']} {bar} {item['count']}")
    print()


def format_category(data, days):
    items = data.get("data", [])
    print(f"\n📊 分类趋势 (近{days}天，共 {len(items)} 条记录)\n")
    if not items:
        print("  暂无趋势数据")
        return
    date_groups = {}
    for item in items:
        d = item["date"]
        if d not in date_groups:
            date_groups[d] = []
        cat_label = f"分类{item['category_id']}" if item.get("category_id") else "未分类"
        date_groups[d].append(f"{cat_label}({item['count']})")
    for d in sorted(date_groups):
        print(f"  {d}: {', '.join(date_groups[d])}")
    print()


def main():
    parser = argparse.ArgumentParser(description="趋势分析")
    sub = parser.add_subparsers(dest="command", required=True)

    hot_p = sub.add_parser("hot", help="热词排行")
    hot_p.add_argument("--days", type=int, default=7, help="天数 (默认7)")
    hot_p.add_argument("--top", type=int, default=20, help="TOP N (默认20)")
    hot_p.add_argument("--json", action="store_true")

    kw_p = sub.add_parser("keyword", help="关键词趋势")
    kw_p.add_argument("--keyword", required=True, help="关键词")
    kw_p.add_argument("--days", type=int, default=30, help="天数 (默认30)")
    kw_p.add_argument("--json", action="store_true")

    cat_p = sub.add_parser("category", help="分类趋势")
    cat_p.add_argument("--days", type=int, default=30, help="天数 (默认30)")
    cat_p.add_argument("--json", action="store_true")

    args = parser.parse_args()

    try:
        if args.command == "hot":
            data = get_hot(args.days, args.top)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                format_hot(data, args.days)

        elif args.command == "keyword":
            data = get_keyword(args.keyword, args.days)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                format_keyword(data, args.keyword)

        elif args.command == "category":
            data = get_category(args.days)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                format_category(data, args.days)

    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
