"""查询新闻文章列表"""
import os
import sys
import json
import argparse
import requests

BASE_URL = os.getenv("NEWS_API_BASE_URL", "http://localhost:8030/api/v1")
HEADERS = {"Authorization": "Bearer PharmaBlock Gateway"}


def get_articles(keyword=None, category_id=None, start_date=None, end_date=None,
                 page=1, page_size=20):
    params = {"page": page, "page_size": page_size}
    if keyword:
        params["keyword"] = keyword
    if category_id:
        params["category_id"] = category_id
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date

    resp = requests.get(f"{BASE_URL}/articles", headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def format_output(data):
    payload = data.get("data", {})
    items = payload.get("items", [])
    total = payload.get("total", 0)

    print(f"\n📰 新闻列表 (共 {total} 条，显示 {len(items)} 条)\n")

    if not items:
        print("  暂无新闻数据")
        return

    status_icons = {True: "🟢", False: "⬜"}
    for i, a in enumerate(items, 1):
        icon = status_icons.get(a.get("analyzed"), "⬜")
        print(f"{i:>3}. {icon} [ID:{a['id']}] {a['title']}")
        parts = []
        if a.get("category_name"):
            parts.append(f"分类: {a['category_name']}")
        if a.get("source"):
            parts.append(f"来源: {a['source']}")
        if a.get("published_at"):
            parts.append(a["published_at"][:16])
        print(f"     {' | '.join(parts)}")
        if a.get("summary"):
            summary = a["summary"][:80] + ("..." if len(a["summary"]) > 80 else "")
            print(f"     摘要: {summary}")
        if a.get("keywords"):
            print(f"     关键词: {', '.join(a['keywords'][:5])}")
        print()


def main():
    parser = argparse.ArgumentParser(description="查询新闻文章列表")
    parser.add_argument("--keyword", help="搜索关键词")
    parser.add_argument("--category_id", type=int, help="分类 ID")
    parser.add_argument("--start_date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end_date", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--limit", type=int, default=20, help="每页数量")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    try:
        data = get_articles(
            keyword=args.keyword, category_id=args.category_id,
            start_date=args.start_date, end_date=args.end_date,
            page=args.page, page_size=args.limit,
        )
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            format_output(data)
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
