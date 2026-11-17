# -*- coding: utf-8 -*-
"""零 API Key 的网页搜索工具(给本地 AI 用的「搜索引擎外挂」)。

依次尝试 DuckDuckGo HTML 版 / 必应 / 百度,任一成功即返回:
  [{"title": ..., "url": ..., "snippet": ...}, ...]

用法:
  python scripts/web_search.py "查询词" --n 5
  python scripts/web_search.py "查询词" --engine bing --json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request

from lxml import html as lhtml

UA = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml",
}


def _fetch(url: str, timeout: int = 15) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def _clean(s: str) -> str:
    return " ".join((s or "").split())


def search_ddg(query: str, n: int) -> list[dict]:
    page = _fetch("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query))
    doc = lhtml.fromstring(page)
    out: list[dict] = []
    for a in doc.xpath('//a[contains(@class,"result__a")]')[: n * 2]:
        title = _clean(a.text_content())
        href = a.get("href") or ""
        if "uddg=" in href:  # DDG 的跳转链接,还原真实 URL
            q = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
            href = q.get("uddg", [href])[0]
        if not href.startswith("http"):
            continue
        snip = ""
        node = a.getparent()
        if node is not None:
            node = node.getparent()
        if node is not None:
            sn = node.xpath('.//a[contains(@class,"result__snippet")]')
            if sn:
                snip = _clean(sn[0].text_content())[:300]
        if title:
            out.append({"title": title, "url": href, "snippet": snip})
        if len(out) >= n:
            break
    return out


def search_bing(query: str, n: int) -> list[dict]:
    page = _fetch("https://www.bing.com/search?q=" + urllib.parse.quote(query) + "&count=20")
    doc = lhtml.fromstring(page)
    out: list[dict] = []
    for li in doc.xpath('//li[contains(@class,"b_algo")]')[: n * 2]:
        a = li.xpath('.//h2/a')
        if not a:
            continue
        title = _clean(a[0].text_content())
        href = a[0].get("href") or ""
        p = li.xpath('.//p')
        snip = _clean(p[0].text_content())[:300] if p else ""
        if title and href.startswith("http"):
            out.append({"title": title, "url": href, "snippet": snip})
        if len(out) >= n:
            break
    return out


def search_baidu(query: str, n: int) -> list[dict]:
    page = _fetch("https://www.baidu.com/s?wd=" + urllib.parse.quote(query) + "&rn=20")
    doc = lhtml.fromstring(page)
    out: list[dict] = []
    for div in doc.xpath('//div[contains(@class,"result") and contains(@class,"c-container")]')[: n * 2]:
        a = div.xpath('.//h3//a')
        if not a:
            continue
        title = _clean(a[0].text_content())
        href = a[0].get("href") or ""
        abs_div = div.xpath('.//div[contains(@class,"c-abstract")] | .//span[contains(@class,"content-right")]')
        snip = _clean(abs_div[0].text_content())[:300] if abs_div else ""
        if title and href.startswith("http"):
            out.append({"title": title, "url": href, "snippet": snip})
        if len(out) >= n:
            break
    return out


ENGINES = {"duckduckgo": search_ddg, "bing": search_bing, "baidu": search_baidu}


def search(query: str, n: int = 5, engine: str | None = None, rounds: int = 3):
    """按指定引擎或自动降级顺序搜索;网络抖动时自动重试若干轮。
    返回 (引擎名, 结果列表)。"""
    order = [engine] if engine else ["duckduckgo", "bing", "baidu"]
    for rnd in range(rounds):
        for name in order:
            fn = ENGINES.get(name)
            if not fn:
                continue
            try:
                res = fn(query, n)
                if res:
                    return name, res
                print(f"[{name}] 无结果,换下一个引擎", file=sys.stderr)
            except Exception as e:
                print(f"[{name}] 失败: {type(e).__name__}: {e}", file=sys.stderr)
        if rnd < rounds - 1:
            print(f"[搜索] 第 {rnd + 1} 轮全部失败,{12}s 后重试", file=sys.stderr)
            time.sleep(12)
    return None, []


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    p = argparse.ArgumentParser(description="零 API Key 网页搜索")
    p.add_argument("query")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--engine", choices=list(ENGINES), default=None)
    p.add_argument("--json", action="store_true", help="输出 JSON(供程序调用)")
    args = p.parse_args()

    used, results = search(args.query, args.n, args.engine)
    if not results:
        print("[搜索] 所有引擎都失败或无结果")
        sys.exit(1)
    print(f"[引擎: {used}] {len(results)} 条结果\n", file=sys.stderr)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        if r["snippet"]:
            print(f"   {r['snippet']}")


if __name__ == "__main__":
    main()
