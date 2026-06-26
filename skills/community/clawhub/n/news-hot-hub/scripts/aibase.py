#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AIBase Data Fetcher — AIBase新闻和日报数据获取工具

Self-contained script for news Hot Hub dispatcher.

Usage:
    python aibase.py news [--limit N]
    python aibase.py daily [--limit N]
    python aibase.py all [--limit N]
    python aibase.py hot-search [--limit N]   # alias for 'news' (hub compatibility)
"""

import argparse
import contextlib
import json
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ──────────────────────────── Constants ────────────────────────────

NEWS_URL = "https://news.aibase.cn/news"
DAILY_URL = "https://news.aibase.cn/daily"

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9",
}

# Nuxt data key mapping for each data type
_NUXT_KEYS = {
    "news": "getAINewsList",
    "daily": "getDailyNews",
}

# ──────────────────────────── Helpers ────────────────────────────


def _now():
    """返回带时区的当前时间戳字符串。"""
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _output(data_type, data):
    """构建标准输出信封。"""
    result = {
        "type": data_type,
        "timestamp": _now(),
        "count": len(data),
        "data": data,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _error(msg):
    """输出错误并退出。"""
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


# ──────────────────────────── HTTP Session ────────────────────────────


@contextlib.contextmanager
def _session():
    """创建带重试机制的HTTP会话（上下文管理器）。"""
    s = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    try:
        yield s
    finally:
        s.close()


# ──────────────────────────── Data Parsing ────────────────────────────


def _parse_nuxt_item(arr: List, idx: int) -> Any:
    """解析单个Nuxt数据项。"""
    if not isinstance(idx, int) or idx >= len(arr):
        return idx
    item = arr[idx]
    if isinstance(item, list) and item:
        tag = item[0]
        if tag in ["ShallowReactive", "Reactive", "Ref"]:
            return _parse_nuxt_item(arr, item[1])
    return item


def _parse_nuxt_data(arr: List, idx: int) -> Any:
    """递归解析Nuxt数据结构。"""
    item = _parse_nuxt_item(arr, idx)
    if isinstance(item, dict):
        result = {}
        for k, v in item.items():
            result[k] = _parse_nuxt_data(arr, v) if isinstance(v, int) else v
        return result
    if isinstance(item, list):
        return [_parse_nuxt_data(arr, i) for i in item]
    return item


def _extract_nuxt_data(html: str) -> Optional[Dict]:
    """从HTML中提取__NUXT_DATA__。"""
    match = re.search(r'<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not match:
        return None
    try:
        raw_data = json.loads(match.group(1))
        return _parse_nuxt_data(raw_data, 0)
    except Exception as e:
        print(f"解析Nuxt数据失败: {e}", file=sys.stderr)
        return None


def _fetch_article_content(session: requests.Session, url: str) -> str:
    """获取文章详细内容（HTML）。"""
    try:
        resp = session.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        content_div = soup.find("div", class_="article-content") or soup.find("article")
        return content_div.decode_contents() if content_div else ""
    except Exception as e:
        print(f"获取文章内容失败 {url}: {e}", file=sys.stderr)
        return ""


# ──────────────────────────── Fetchers ────────────────────────────


def _extract_items(data: Dict, data_type: str) -> List:
    """从Nuxt数据中提取列表项。"""
    nuxt_key = _NUXT_KEYS.get(data_type)
    if not nuxt_key:
        return []
    return data.get("data", {}).get(nuxt_key, {}).get("data", {}).get("list", [])


def _build_item(item: Dict, data_type: str, content: str = "") -> Dict:
    """构建单条结果数据。"""
    article_id = item.get("oid", "")
    result = {
        "id": article_id,
        "title": item.get("title", ""),
        "subtitle": item.get("subtitle", ""),
        "url": f"https://news.aibase.cn/{data_type}/{article_id}",
        "thumb": item.get("thumb", ""),
        "source": item.get("sourceName", ""),
        "create_time": item.get("createTime", ""),
        "pv": item.get("pv", 0),
        "description": item.get("description", ""),
    }
    if content is not None:
        result["content"] = content
    return result


def fetch_data(
    session: requests.Session,
    url: str,
    data_type: str,
    limit: int,
    with_content: bool = True,
) -> List[Dict]:
    """获取列表数据，可选附带文章内容。

    Returns list of items. Raises on HTTP/parsing errors.
    """
    resp = session.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    data = _extract_nuxt_data(resp.text)
    if not data:
        return []

    items = _extract_items(data, data_type)[:limit]
    results = []
    for item in items:
        content = ""
        if with_content:
            article_url = f"https://news.aibase.cn/{data_type}/{item.get('oid', '')}"
            content = _fetch_article_content(session, article_url)
        results.append(_build_item(item, data_type, content if with_content else None))

    return results


# ──────────────────────────── CLI ────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="AIBase数据获取工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # news
    news_parser = subparsers.add_parser("news", help="获取AI新闻资讯")
    news_parser.add_argument("--limit", type=int, default=20, help="获取数量")

    # daily
    daily_parser = subparsers.add_parser("daily", help="获取AI日报")
    daily_parser.add_argument("--limit", type=int, default=20, help="获取数量")

    # all
    all_parser = subparsers.add_parser("all", help="获取所有数据")
    all_parser.add_argument("--limit", type=int, default=20, help="获取数量")

    # hot-search (hub compatibility alias → news)
    hs_parser = subparsers.add_parser("hot-search", help="获取AI新闻资讯（hub兼容）")
    hs_parser.add_argument("--limit", type=int, default=20, help="获取数量")

    args = parser.parse_args()

    try:
        with _session() as session:
            if args.command in ("news", "hot-search"):
                data = fetch_data(session, NEWS_URL, "news", args.limit)
                _output("news", data)

            elif args.command == "daily":
                data = fetch_data(session, DAILY_URL, "daily", args.limit)
                _output("daily", data)

            elif args.command == "all":
                news = fetch_data(session, NEWS_URL, "news", args.limit)
                daily = fetch_data(session, DAILY_URL, "daily", args.limit)
                result = {
                    "news": {"type": "news", "timestamp": _now(), "count": len(news), "data": news},
                    "daily": {"type": "daily", "timestamp": _now(), "count": len(daily), "data": daily},
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))

    except requests.exceptions.RequestException as e:
        _error(f"网络请求失败: {e}")
    except Exception as e:
        _error(f"获取数据失败: {e}")


if __name__ == "__main__":
    main()
