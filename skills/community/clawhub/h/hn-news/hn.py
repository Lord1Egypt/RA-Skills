#!/usr/bin/env python3
# hn_cli.py

import argparse
import requests
import time
import sys

API_URL = "https://hn.algolia.com/api/v1/search_by_date"


def build_query():
    # 你的关键词
    return '(AI OR "agent" OR claude)'


def fetch_data(mode: str, page: int = 0):
    params = {
        "query": build_query(),
        "tags": "story",
        "page": page,
    }

    if mode == "week":
        now = int(time.time())
        week_ago = now - 7 * 24 * 60 * 60
        params["numericFilters"] = f"created_at_i>{week_ago}"

    resp = requests.get(API_URL, params=params, timeout=10)

    if resp.status_code != 200:
        print("Request failed:", resp.status_code, file=sys.stderr)
        sys.exit(1)

    return resp.json()


def print_results(data):
    hits = data.get("hits", [])

    if not hits:
        print("No results.")
        return

    # Force UTF-8 output on Windows
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    for i, item in enumerate(hits, 1):
        title = item.get("title") or "No title"
        url = item.get("url") or "No URL"
        author = item.get("author")
        points = item.get("points")
        created = item.get("created_at")

        print(f"{i}. {title}")
        print(f"   👤 {author} | ⭐ {points} | 🕒 {created}")
        print(f"   🔗 {url}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Hacker News AI/Agent/Claude CLI"
    )

    parser.add_argument(
        "mode",
        choices=["latest", "week"],
        help="latest: 最新 | week: 过去一周"
    )

    parser.add_argument(
        "--page",
        type=int,
        default=0,
        help="分页 (默认: 0)"
    )

    args = parser.parse_args()

    data = fetch_data(args.mode, args.page)
    print_results(data)


if __name__ == "__main__":
    main()
