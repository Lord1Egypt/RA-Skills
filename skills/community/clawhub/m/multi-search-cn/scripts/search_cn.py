#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Search-CN：零 API Key，优先用 DuckDuckGo HTML 抓取可解析结果；
同时输出国内常用搜索引擎直达链接，便于人工或浏览器打开。
仅依赖 Python 3 标准库。
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Iterable

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def search_urls(query: str) -> dict[str, str]:
    """各引擎搜索页（UTF-8 编码 query）。"""
    q = query.strip()
    enc = urllib.parse.quote(q)
    return {
        "duckduckgo_html": f"https://html.duckduckgo.com/html/?{urllib.parse.urlencode({'q': q, 'kl': 'cn-zh'})}",
        "bing_cn": f"https://cn.bing.com/search?q={enc}",
        "baidu": f"https://www.baidu.com/s?wd={enc}",
        "sogou": f"https://www.sogou.com/web?query={enc}",
        "so_360": f"https://www.so.com/s?q={enc}",
    }


def fetch(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def decode_ddg_redirect(href: str) -> str:
    """duckduckgo.com/l/?uddg= 真实 URL。"""
    if href.startswith("//"):
        href = "https:" + href
    parsed = urllib.parse.urlparse(href)
    qs = urllib.parse.parse_qs(parsed.query)
    uddg = qs.get("uddg", [""])[0]
    if uddg:
        return urllib.parse.unquote(uddg)
    return href


def parse_ddg_html(html_doc: str, limit: int) -> list[tuple[str, str]]:
    """解析 DDG HTML 版结果：标题 + 落地 URL。"""
    blocks = re.findall(
        r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]*)</a>',
        html_doc,
        flags=re.I,
    )
    out: list[tuple[str, str]] = []
    for href, title in blocks:
        title = html.unescape(re.sub(r"\s+", " ", title).strip())
        real = decode_ddg_redirect(href)
        if not real or real.startswith("https://duckduckgo.com"):
            continue
        out.append((title or real, real))
        if len(out) >= limit:
            break
    return out


def run_ddg(query: str, limit: int) -> list[tuple[str, str]]:
    """抓取 DuckDuckGo HTML（cn-zh）。"""
    q = urllib.parse.urlencode({"q": query.strip(), "kl": "cn-zh"})
    url = f"https://html.duckduckgo.com/html/?{q}"
    html = fetch(url)
    return parse_ddg_html(html, limit=limit)


def main(argv: Iterable[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Multi-Search-CN（国内检索聚合，零 API Key）")
    p.add_argument("query", help="搜索关键词")
    p.add_argument("--limit", type=int, default=8, help="DDG 解析条数上限（默认 8）")
    p.add_argument(
        "--urls-only",
        action="store_true",
        help="仅输出各搜索引擎直达链接，不发起网络请求",
    )
    p.add_argument("--json", action="store_true", help="JSON 输出（urls-only 与 DDG 结果）")
    args = p.parse_args(list(argv) if argv is not None else None)

    urls = search_urls(args.query)

    if args.urls_only:
        if args.json:
            print(json.dumps({"engines": urls}, ensure_ascii=False, indent=2))
        else:
            print("# 各引擎搜索页（复制到浏览器）\n")
            for name, u in urls.items():
                print(f"- {name}: {u}")
        return 0

    rows: list[tuple[str, str]] = []
    err: str | None = None
    try:
        rows = run_ddg(args.query, limit=args.limit)
    except urllib.error.HTTPError as e:
        err = f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        err = f"网络错误: {e.reason}"
    except Exception as e:  # noqa: BLE001
        err = f"未知错误: {e}"

    if args.json:
        payload = {
            "query": args.query.strip(),
            "engines": urls,
            "ddg_results": [{"title": t, "url": u} for t, u in rows],
            "error": err,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if not err else 1

    print(f"查询: {args.query.strip()}\n")
    print("## DuckDuckGo HTML（cn-zh）解析结果\n")
    if err:
        print(f"（抓取失败: {err}）\n")
    elif not rows:
        print("（无解析结果，可能被限流或页面结构变化。请改用下方直达链接。）\n")
    else:
        for i, (title, u) in enumerate(rows, 1):
            print(f"{i}. {title}\n   {u}\n")

    print("## 国内常用搜索引擎直达\n")
    for name, u in urls.items():
        print(f"- {name}: {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
