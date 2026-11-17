#!/usr/bin/env python3
"""感知层（SPA）：用 Firecrawl 抓岗位详情页 JD 全文（careers 页是 React SPA，requests 拿不到正文）。

主路径 Firecrawl /v2/scrape（v1 兼容），失败回退 Jina Reader（免 key），再失败返回空串。
"""
import json
import os
import sys

from common import CONFIG, http, http_json, require_egress_consent


def firecrawl_scrape(url):
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        raise RuntimeError("FIRECRAWL_API_KEY not set")
    require_egress_consent("firecrawl", f"the URL of the posting being scraped: {url}")
    resp = http_json(
        "https://api.firecrawl.dev/v1/scrape",
        method="POST",
        headers={"Authorization": f"Bearer {key}"},
        json_body={"url": url, "formats": ["markdown"], "onlyMainContent": True},
        timeout=90,
    )
    md = (resp.get("data") or {}).get("markdown", "")
    if not md:
        raise RuntimeError(f"Firecrawl returned no markdown: {str(resp)[:200]}")
    return md


def jina_reader(url):
    require_egress_consent("jina", f"the URL of the posting being read: {url}")
    headers = {}
    if os.environ.get("JINA_API_KEY"):  # 免 key 通道对部分站点收紧，有 key 更稳
        headers["Authorization"] = f"Bearer {os.environ['JINA_API_KEY']}"
    status, body = http(f"https://r.jina.ai/{url}", headers=headers, timeout=60)
    if status >= 300:
        raise RuntimeError(f"Jina Reader HTTP {status}")
    return body.decode("utf-8", "replace")


def fetch_jd(url):
    """Returns (markdown, tool_used). Never raises."""
    limit = CONFIG["judge"]["jd_max_chars"]
    for tool, fn in (("firecrawl", firecrawl_scrape), ("jina", jina_reader)):
        try:
            return fn(url)[:limit], tool
        except Exception:  # noqa: BLE001
            continue
    return "", "none"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: enrich_jd.py <detail_url>")
    md, tool = fetch_jd(sys.argv[1])
    print(f"# fetched via {tool}, {len(md)} chars", file=sys.stderr)
    print(md)
