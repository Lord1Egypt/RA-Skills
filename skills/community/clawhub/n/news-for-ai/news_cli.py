#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI News Fetcher CLI — AI新闻、日报和搜索数据获取工具

Single-file CLI tool for fetching AI news, daily reports and search results.

Usage:
    python news_cli.py news [--limit N] [--no-content]
    python news_cli.py daily [--limit N] [--no-content]
    python news_cli.py all [--limit N] [--no-content]
    python news_cli.py search <keyword> [--limit N] [--no-content] [--type TYPE]
    python news_cli.py hot-search [--limit N] [--no-content]
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
SEARCH_URL = "https://www.aibase.cn/search/"

SEARCH_TYPES = ("news", "products", "models", "mcp", "all")
_SEARCH_DATA_KEYS = {
    "news": "news",
    "products": "products",
    "models": "projectModels",
    "mcp": "mcp",
}

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


def _extract_media(soup_element) -> Dict[str, List]:
    """从内容元素中提取图片、视频和外部链接。"""
    media: Dict[str, List] = {"images": [], "videos": [], "links": []}

    for img in soup_element.find_all("img"):
        src = img.get("src", "")
        if src and "userlogo" not in src:
            media["images"].append({"src": src, "alt": img.get("alt", "")})

    for video in soup_element.find_all("video"):
        src = video.get("src", "")
        if not src:
            source_tag = video.find("source")
            src = source_tag.get("src", "") if source_tag else ""
        if src:
            media["videos"].append({"src": src})

    for a in soup_element.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if href and text and not href.startswith("#") and not href.startswith("javascript:"):
            media["links"].append({"text": text, "href": href})

    return media


_INLINE_TAGS = frozenset(["strong", "b", "em", "i", "span", "a", "code", "mark", "sub", "sup"])


def _collapse_inline(element) -> str:
    """将一个元素内的内联标签合并为连续文本，避免不必要的换行。"""
    from bs4 import NavigableString
    parts = []
    for child in element.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif getattr(child, "name", None) in _INLINE_TAGS:
            parts.append(child.get_text())
        elif getattr(child, "name", None) in ("br",):
            parts.append("\n")
        elif getattr(child, "name", None) in ("img", "video"):
            pass
        else:
            parts.append(child.get_text())
    return re.sub(r"[ \t]+", " ", "".join(parts)).strip()


def _html_to_clean_text(soup_element) -> str:
    """将 HTML 元素转换为结构化纯文本，保留标题层级和引用块。"""
    parts: List[str] = []
    for child in soup_element.children:
        if isinstance(child, str):
            text = child.strip()
            if text:
                parts.append(text)
            continue

        tag = getattr(child, "name", None)
        if not tag:
            continue

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag[1])
            heading = _collapse_inline(child)
            if heading:
                parts.append(f"\n{'#' * level} {heading}\n")
        elif tag == "blockquote":
            text = _collapse_inline(child)
            for line in text.split("\n"):
                line = line.strip()
                if line:
                    parts.append(f"> {line}")
        elif tag in ("ul", "ol"):
            for li in child.find_all("li", recursive=False):
                parts.append(f"- {_collapse_inline(li)}")
        elif tag in ("img", "video"):
            pass
        elif tag == "p" and child.find("img") and not _collapse_inline(child):
            pass
        else:
            text = _collapse_inline(child)
            if text:
                parts.append(text)

    return "\n".join(parts)


def _fetch_article_detail(session: requests.Session, url: str) -> Dict:
    """获取文章详细内容，返回纯文本 + 媒体资源。"""
    result: Dict[str, Any] = {"content": "", "images": [], "videos": [], "links": []}
    try:
        resp = session.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        content_div = soup.find("div", class_="post-content")
        if not content_div:
            content_div = soup.find("div", class_="articleContent")
        if not content_div:
            content_div = soup.find("div", class_="article-content") or soup.find("article")

        if content_div:
            result["content"] = _html_to_clean_text(content_div)
            media = _extract_media(content_div)
            result["images"] = media["images"]
            result["videos"] = media["videos"]
            result["links"] = media["links"]
    except Exception as e:
        print(f"获取文章内容失败 {url}: {e}", file=sys.stderr)
    return result


# ──────────────────────────── Fetchers ────────────────────────────


def _extract_items(data: Dict, data_type: str) -> List:
    """从Nuxt数据中提取列表项。"""
    nuxt_key = _NUXT_KEYS.get(data_type)
    if not nuxt_key:
        return []
    return data.get("data", {}).get(nuxt_key, {}).get("data", {}).get("list", [])


def _build_item(item: Dict, data_type: str, detail: Optional[Dict] = None) -> Dict:
    """构建单条结果数据。"""
    article_id = item.get("oid", "")
    result = {
        "id": article_id,
        "title": item.get("title", "").strip(),
        "subtitle": item.get("subtitle", "").strip(),
        "url": f"https://news.aibase.cn/{data_type}/{article_id}",
        "thumb": item.get("thumb", ""),
        "source": item.get("sourceName", ""),
        "author": item.get("author", ""),
        "create_time": item.get("createTime", ""),
        "pv": item.get("pv", 0),
        "description": item.get("description", "").strip(),
    }
    if detail is not None:
        result["content"] = detail["content"]
        result["images"] = detail["images"]
        result["videos"] = detail["videos"]
        result["links"] = detail["links"]
    return result


def fetch_data(
    session: requests.Session,
    url: str,
    data_type: str,
    limit: int,
    with_content: bool = True,
) -> List[Dict]:
    """获取列表数据，可选附带文章详情（纯文本+媒体）。"""
    resp = session.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    data = _extract_nuxt_data(resp.text)
    if not data:
        return []

    items = _extract_items(data, data_type)[:limit]
    results = []
    for item in items:
        detail = None
        if with_content:
            article_url = f"https://news.aibase.cn/{data_type}/{item.get('oid', '')}"
            detail = _fetch_article_detail(session, article_url)
        results.append(_build_item(item, data_type, detail))

    return results


# ──────────────────────────── Search ────────────────────────────


def _build_search_news_item(item: Dict) -> Dict:
    """构建搜索结果中的新闻条目。"""
    oid = item.get("oid", "")
    news_type = item.get("type", 1)
    url_prefix = "daily" if news_type == 2 else "news"
    return {
        "id": oid,
        "title": (item.get("title") or "").strip(),
        "subtitle": (item.get("subtitle") or "").strip(),
        "url": f"https://news.aibase.cn/{url_prefix}/{oid}",
        "thumb": item.get("thumb") or item.get("logo", ""),
        "create_time": item.get("publishDate") or item.get("timestamp", ""),
        "pv": item.get("pv") or item.get("viewNum", 0),
        "description": (item.get("description") or "").strip(),
    }


def _build_search_product_item(item: Dict) -> Dict:
    """构建搜索结果中的产品条目。"""
    oid = item.get("oid", "")
    return {
        "id": oid,
        "name": (item.get("productName") or "").strip(),
        "url": f"https://app.aibase.cn/tool/{oid}",
        "logo": item.get("logo") or item.get("imgUrl", ""),
        "category": item.get("className", []),
        "tags": item.get("tags", []),
        "pv": item.get("pv") or item.get("viewNum", 0),
        "description": (item.get("info") or item.get("description") or "").strip(),
    }


def _build_search_model_item(item: Dict) -> Dict:
    """构建搜索结果中的模型条目。"""
    return {
        "id": item.get("oid", ""),
        "name": (item.get("modelName") or item.get("productName") or "").strip(),
        "full_name": (item.get("modelFullName") or "").strip(),
        "provider": item.get("modelOwner") or item.get("provider", ""),
        "tags": item.get("tags", []),
        "category": item.get("className", []),
        "downloads": item.get("downloads", 0),
        "likes": item.get("star") or item.get("likes", 0),
        "description": (item.get("modelInfo") or item.get("description") or "").strip(),
    }


def _build_search_mcp_item(item: Dict) -> Dict:
    """构建搜索结果中的 MCP 服务条目。"""
    return {
        "id": item.get("oid") or item.get("id", ""),
        "name": (item.get("name") or "").strip(),
        "tag": item.get("tag", ""),
        "downloads": item.get("downloads", 0),
        "rating": item.get("rating", 0),
        "provider": item.get("provider", ""),
        "description": (item.get("description") or "").strip(),
    }


_SEARCH_BUILDERS = {
    "news": _build_search_news_item,
    "products": _build_search_product_item,
    "models": _build_search_model_item,
    "mcp": _build_search_mcp_item,
}


def fetch_search(
    session: requests.Session,
    keyword: str,
    limit: int,
    search_type: str = "all",
    with_content: bool = False,
) -> Dict:
    """搜索全站，返回按分类组织的结果。"""
    from urllib.parse import quote

    url = SEARCH_URL + quote(keyword, safe="")
    resp = session.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    data = _extract_nuxt_data(resp.text)
    if not data:
        return {}

    search_data = data.get("data", {}).get("searchData", {})

    if search_type == "all":
        categories = list(_SEARCH_DATA_KEYS.keys())
    else:
        categories = [search_type]

    result: Dict[str, Any] = {}
    for cat in categories:
        raw_key = _SEARCH_DATA_KEYS.get(cat)
        if not raw_key:
            continue
        raw_items = search_data.get(raw_key, [])
        if not isinstance(raw_items, list):
            continue

        builder = _SEARCH_BUILDERS[cat]
        items = [builder(item) for item in raw_items[:limit]]

        if cat == "news" and with_content and items:
            for item in items:
                detail = _fetch_article_detail(session, item["url"])
                item["content"] = detail["content"]
                item["images"] = detail["images"]
                item["videos"] = detail["videos"]
                item["links"] = detail["links"]

        result[cat] = {
            "type": cat,
            "count": len(items),
            "data": items,
        }

    return result


# ──────────────────────────── CLI ────────────────────────────


def _add_common_args(sub_parser: argparse.ArgumentParser):
    """为子命令添加通用参数。"""
    sub_parser.add_argument("--limit", type=int, default=20, help="获取数量（默认20）")
    sub_parser.add_argument(
        "--no-content", action="store_true",
        help="仅获取列表摘要，不抓取文章正文（速度更快）",
    )


def main():
    parser = argparse.ArgumentParser(description="AI资讯数据获取工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_common_args(subparsers.add_parser("news", help="获取AI新闻资讯"))
    _add_common_args(subparsers.add_parser("daily", help="获取AI日报"))
    _add_common_args(subparsers.add_parser("all", help="获取所有数据"))
    _add_common_args(subparsers.add_parser("hot-search", help="获取AI新闻资讯（hub兼容）"))

    search_parser = subparsers.add_parser("search", help="搜索AI相关内容")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument(
        "--type", dest="search_type", choices=SEARCH_TYPES,
        default="all", help="搜索类型: news/products/models/mcp/all（默认all）",
    )
    _add_common_args(search_parser)

    args = parser.parse_args()
    with_content = not getattr(args, "no_content", False)

    try:
        with _session() as session:
            if args.command in ("news", "hot-search"):
                data = fetch_data(session, NEWS_URL, "news", args.limit, with_content)
                _output("news", data)

            elif args.command == "daily":
                data = fetch_data(session, DAILY_URL, "daily", args.limit, with_content)
                _output("daily", data)

            elif args.command == "all":
                news = fetch_data(session, NEWS_URL, "news", args.limit, with_content)
                daily = fetch_data(session, DAILY_URL, "daily", args.limit, with_content)
                result = {
                    "news": {"type": "news", "timestamp": _now(), "count": len(news), "data": news},
                    "daily": {"type": "daily", "timestamp": _now(), "count": len(daily), "data": daily},
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))

            elif args.command == "search":
                result = fetch_search(
                    session, args.keyword, args.limit,
                    args.search_type, with_content,
                )
                output = {
                    "type": "search",
                    "keyword": args.keyword,
                    "search_type": args.search_type,
                    "timestamp": _now(),
                    **result,
                }
                print(json.dumps(output, ensure_ascii=False, indent=2))

    except requests.exceptions.RequestException as e:
        _error(f"网络请求失败: {e}")
    except Exception as e:
        _error(f"获取数据失败: {e}")


if __name__ == "__main__":
    main()
