#!/usr/bin/env python3
"""搜索笔记关键词 — 只拉第 1 页的推荐结果，避免翻页触发风控。

    export XHS_COOKIE='...'
    python3 scrape-search.py --keyword 宠物用品 --out /tmp/search.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_client import XHSClient, load_cookie_from_env, XHSError  # noqa: E402
from xhs_parser import parse_search_page  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="搜索小红书笔记关键词")
    ap.add_argument("--keyword", required=True)
    ap.add_argument("--out", "-o", default="")
    ap.add_argument("--save-html", default="")
    ap.add_argument("--min-delay", type=float, default=3.0)
    ap.add_argument("--max-delay", type=float, default=7.0)
    args = ap.parse_args()

    try:
        cookie = load_cookie_from_env()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 2

    client = XHSClient(cookie=cookie, min_delay=args.min_delay, max_delay=args.max_delay)
    try:
        html = client.get_search_page(args.keyword)
    except XHSError as e:
        print(f"抓取失败：{e}", file=sys.stderr)
        return 1

    if args.save_html:
        Path(args.save_html).write_text(html, encoding="utf-8")

    results = parse_search_page(html)
    data = {"keyword": args.keyword, "count": len(results), "results": results}
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}（命中 {len(results)} 条）")
    else:
        print(text)

    if not results:
        print("⚠ 没有解析到结果。如果 Cookie 没过期、HTML 也正常返回，可能是搜索页的数据结构有新变化，"
              "请加 --save-html 导出看看。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
