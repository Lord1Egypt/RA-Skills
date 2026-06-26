#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""今日头条热榜数据获取 — Toutiao Hot Board Fetcher

获取今日头条热榜数据，输出结构化 JSON。

Usage:
    python toutiao.py hot-search [--limit N]
"""

import argparse
import contextlib
import json
import sys
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ──────────────────────────── Constants ────────────────────────────

API_URL = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.toutiao.com/",
}

RETRIES = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
)


# ──────────────────────────── Helpers ────────────────────────────────

def _now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _output(data_type, data):
    result = {
        "type": data_type,
        "timestamp": _now(),
        "count": len(data),
        "data": data,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


@contextlib.contextmanager
def _session():
    s = requests.Session()
    try:
        s.headers.update(HEADERS)
        s.mount("http://", HTTPAdapter(max_retries=RETRIES))
        s.mount("https://", HTTPAdapter(max_retries=RETRIES))
        yield s
    finally:
        s.close()


# ──────────────────────────── Fetcher ────────────────────────────────

def fetch_hot_search(limit=50):
    """获取今日头条热榜"""
    items = []
    with _session() as s:
        resp = s.get(API_URL, timeout=15)
        resp.raise_for_status()
        raw = resp.json()
        for entry in raw.get("data", [])[:limit]:
            title = entry.get("Title") or entry.get("QueryWord", "")
            if not title:
                continue
            items.append({
                "title": title,
                "url": entry.get("Url", ""),
                "hot": entry.get("HotValue", ""),
                "label": entry.get("Label", ""),
            })
    return items


# ──────────────────────────── CLI ───────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="今日头条热榜数据获取")
    sub = parser.add_subparsers(dest="command")

    p_hs = sub.add_parser("hot-search", help="获取今日头条热榜")
    p_hs.add_argument("--limit", type=int, default=50, help="结果数量 (默认 50)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "hot-search":
        try:
            data = fetch_hot_search(limit=args.limit)
            _output("hot_search", data)
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP error: {e}", file=sys.stderr)
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            print("Error: Network connection failed", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print("Error: Failed to parse API response", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
