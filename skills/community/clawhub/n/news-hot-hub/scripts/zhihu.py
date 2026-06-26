#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Zhihu Hot Search Fetcher — 知乎热搜榜数据获取工具

获取知乎热搜榜数据，输出结构化 JSON。

Usage:
    python zhihu.py hot-search
"""

import argparse
import contextlib
import json
import sys
import urllib.parse
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ──────────────────────────── Constants ────────────────────────────

HOT_SEARCH_URL = "https://www.zhihu.com/topsearch"

HEADERS = {
    "x-api-version": "3.0.76",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "referer": "https://www.zhihu.com/",
    "origin": "https://www.zhihu.com",
}

RETRIES = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])


# ──────────────────────────── Helpers ──────────────────────────────

def _now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


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


def _output(data_type, data):
    result = {
        "type": data_type,
        "timestamp": _now(),
        "count": len(data),
        "data": data,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _error(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


# ──────────────────────────── Fetcher ──────────────────────────────

def fetch_hot_search():
    """获取知乎热搜榜（公开接口，无需登录）"""
    items = []
    with _session() as s:
        resp = s.get(HOT_SEARCH_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, features="html.parser")
        script = soup.find("script", type="text/json", id="js-initialData")
        if script:
            obj = json.loads(script.string)
            raw_items = obj.get("initialState", {}).get("topsearch", {}).get("data", [])
            for item in raw_items:
                q = item.get("realQuery", "")
                items.append({
                    "title": item.get("queryDisplay", ""),
                    "url": f"https://www.zhihu.com/search?q={urllib.parse.quote(q)}",
                    "query": q,
                })
    return items


# ──────────────────────────── CLI ──────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="知乎热搜榜数据获取工具")
    sub = parser.add_subparsers(dest="command", help="Available commands")
    sub.add_parser("hot-search", help="获取知乎热搜榜")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "hot-search":
            data = fetch_hot_search()
            _output("hot_search", data)

    except requests.exceptions.HTTPError as e:
        _error(f"HTTP error: {e}")
    except requests.exceptions.ConnectionError:
        _error("Network connection failed")
    except json.JSONDecodeError:
        _error("Failed to parse API response")
    except Exception as e:
        _error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
