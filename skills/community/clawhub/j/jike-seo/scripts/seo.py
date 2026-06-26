#!/usr/bin/env python3
"""
极义SEO CLI — OpenClaw skill script for SEO keyword platform API.

Usage:
  python3 seo.py check
  python3 seo.py search --keyword <keyword> [--platform <platform>] [--limit <limit>] [--page <page>]
  python3 seo.py detail --keyword <keyword> [--platform <platform>]

Configuration:
  Environment variable JIKE_SEO_API_KEY sets the API key.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "https://dso-dataserver.dso100.com/open/v1"
DEFAULT_PLATFORM = "douyin"
DEFAULT_LIMIT = 20
DEFAULT_PAGE = 1


def get_api_key() -> str:
    """Get API key from environment variable."""
    key = os.environ.get("JIKE_SEO_API_KEY", "").strip()
    if not key:
        print("Error: API key not configured.", file=sys.stderr)
        print("  Set it via JIKE_SEO_API_KEY environment variable.", file=sys.stderr)
        print("  Get your API Key at: https://jike-seo.100.city", file=sys.stderr)
        sys.exit(1)
    return key


def api_request(method: str, path: str, query: dict | None = None, raw: bool = False) -> dict:
    """Send HTTP request to SEO API. Returns parsed JSON response."""
    key = get_api_key()
    url = f"{DEFAULT_BASE_URL}{path}"
    if query:
        url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    req = urllib.request.Request(url, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(err_body)
            msg = err_json.get("message", err_body)
        except Exception:
            msg = err_body
        print(f"Error: HTTP {e.code} — {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Connection failed — {e.reason}", file=sys.stderr)
        sys.exit(1)

    if isinstance(result, dict) and result.get("code", 0) != 0:
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)
    return result


def cmd_check(args):
    """Check API connectivity."""
    try:
        key = get_api_key()
        print("✓ API key configured")
        print(f"  Key: {key[:10]}...{key[-4:]}")
    except SystemExit:
        sys.exit(1)


def cmd_search(args):
    """Search keywords by platform."""
    if not args.keyword:
        print("Error: --keyword is required", file=sys.stderr)
        sys.exit(1)

    query = {
        "platform": args.platform or DEFAULT_PLATFORM,
        "keyword": args.keyword,
        "page": args.page or DEFAULT_PAGE,
        "limit": args.limit or DEFAULT_LIMIT,
    }

    result = api_request("GET", "/keyword/search", query=query)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if isinstance(result, dict):
            total = result.get("total", 0)
            rows = result.get("rows", [])
            print(f"找到 {total} 个关键词（显示 {len(rows)} 个）\n")
            for i, row in enumerate(rows, 1):
                print(f"{i}. {row.get('keyword', 'N/A')}")
                print(f"   竞争度: {row.get('competition_text', 'N/A')}")
                if row.get("monthly_coverage"):
                    print(f"   月覆盖: {row.get('monthly_coverage'):,}")
                if row.get("monthly_search_volume"):
                    print(f"   月搜索: {row.get('monthly_search_volume'):,}")
                if row.get("index_avg") is not None:
                    print(f"   日均搜索(平均): {row.get('index_avg'):,}")
                if row.get("median") is not None:
                    print(f"   日均搜索(中位): {row.get('median'):,}")
                if row.get("tags"):
                    print(f"   标签: {', '.join(row.get('tags', []))}")
                print(f"   下拉词: {row.get('sug_keyword_count', 0)} 个")
                print()


def cmd_detail(args):
    """Get detailed keyword analysis."""
    if not args.keyword:
        print("Error: --keyword is required", file=sys.stderr)
        sys.exit(1)

    query = {
        "keyword": args.keyword,
        "platform": args.platform or DEFAULT_PLATFORM,
    }

    result = api_request("GET", "/keyword/detail", query=query)
    # detail 接口返回 {code, data: {...}}，取 data 字段
    result = result.get("data", result) if isinstance(result, dict) else result

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if isinstance(result, dict):
            keyword = result.get("keyword", "N/A")
            print(f"关键词: {keyword}\n")

            print(f"竞争度: {result.get('competition_text', 'N/A')}")
            if result.get("tags"):
                print(f"标签: {', '.join(result.get('tags', []))}\n")

            if result.get("monthly_coverage"):
                cov = result.get("monthly_coverage", {})
                print(f"月覆盖人次: {cov.get('value', 'N/A'):,} ({cov.get('rate', 'N/A')})\n")

            if result.get("monthly_search_volume"):
                print("月均搜索量:")
                for platform, data in result.get("monthly_search_volume", {}).items():
                    print(f"  {platform}: {data.get('value', 'N/A'):,} ({data.get('rate', 'N/A')})")
                print()

            if result.get("daily_search_7d"):
                print("近7日搜索趋势:")
                for day in result.get("daily_search_7d", []):
                    print(f"  {day.get('date')}: {day.get('value', 'N/A'):,}")
                print()

            if result.get("age_distribution"):
                print("年龄分布:")
                for age in result.get("age_distribution", []):
                    print(f"  {age.get('name')}: {age.get('rate', 0):.1f}% (TGI: {age.get('tgi', 0):.1f})")
                print()

            if result.get("gender_distribution"):
                print("性别分布:")
                for gender in result.get("gender_distribution", []):
                    print(f"  {gender.get('name')}: {gender.get('rate', 0):.1f}% (TGI: {gender.get('tgi', 0):.1f})")
                print()

            if result.get("related_keywords"):
                print(f"相关词 ({len(result.get('related_keywords', []))} 个):")
                for kw in result.get("related_keywords", [])[:10]:
                    print(f"  - {kw.get('keyword')}")
                print()

            if result.get("suggest_keywords"):
                print(f"下拉词 ({len(result.get('suggest_keywords', []))} 个):")
                for kw in result.get("suggest_keywords", [])[:10]:
                    print(f"  - {kw.get('keyword')}")


def build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="极义SEO — 关键词数据平台 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    sub = parser.add_subparsers(dest="command", help="Command")

    sub.add_parser("check", help="Check API connectivity")

    p = sub.add_parser("search", help="Search keywords")
    p.add_argument("--keyword", required=True, help="Keyword to search")
    p.add_argument("--platform", choices=["douyin", "xhs", "wechat"], help="Platform (default: douyin)")
    p.add_argument("--limit", type=int, help="Results per page (default: 20)")
    p.add_argument("--page", type=int, help="Page number (default: 1)")
    p.add_argument("--json", action="store_true", help="Output raw JSON")

    p = sub.add_parser("detail", help="Get keyword details")
    p.add_argument("--keyword", required=True, help="Keyword to analyze")
    p.add_argument("--platform", choices=["douyin", "xhs", "wechat"], help="Platform (default: douyin)")
    p.add_argument("--json", action="store_true", help="Output raw JSON")

    return parser


COMMAND_MAP = {
    "check": cmd_check,
    "search": cmd_search,
    "detail": cmd_detail,
}


def main():
    parser = build_parser()
    args = parser.parse_args()
    handler = COMMAND_MAP.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
