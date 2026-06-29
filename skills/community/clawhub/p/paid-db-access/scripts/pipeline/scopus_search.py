#!/usr/bin/env python3
"""
Scopus Search API 精简封装 · Lightweight Scopus Search Wrapper
==============================================================

直接调用 Elsevier Scopus Search API，支持自动翻页。

--count 现在是**目标数量**（不再是每页条数）。
脚本会自动翻页直到达到目标数量或结果耗尽。
内部每页拉 25 条（Scopus 单次上限），逐页去重追加。

用法:
    # 单页（兼容旧行为）：--count 25 只拉第一页
    python scopus_search.py -q "machine learning" -k KEY -c 25 -o results.json

    # 自动翻页：--count 80  拉 80 篇
    python scopus_search.py -q "machine learning" -k KEY -c 80 -o results.json

输出（仅一行，不进上下文）:
    Scopus: 80 results (total: 1234) [4 pages] → memory/scopus_results.json

精简后的字段（每篇 ~200 bytes）:
    title, authors, year, venue, doi, citations, link, type, openaccess
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

# Scopus 单次请求最大条数
SCOPUS_MAX_PER_PAGE = 25

# Scopus doc type mapping (abbreviation → full)
DOCTYPE_MAP = {
    "ar": "Article", "re": "Review", "cp": "Conference Paper",
    "ch": "Book Chapter", "no": "Note", "ed": "Editorial",
    "le": "Letter", "er": "Erratum", "sh": "Short Survey",
    "cr": "Conference Review", "bk": "Book", "tb": "Retracted",
}


def _search_one_page(query: str, api_key: str, count: int = 25,
                     start: int = 0, sort: str = "-citedby-count",
                     timeout: int = 15) -> dict:
    """调用 Scopus Search API（单页），返回精简后的结果。"""
    encoded = urllib.parse.quote(query)
    url = (f"https://api.elsevier.com/content/search/scopus"
           f"?query={encoded}&apiKey={api_key}"
           f"&count={count}&start={start}&sort={sort}")
    headers = {"X-ELS-APIKey": api_key, "Accept": "application/json"}

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = json.loads(resp.read().decode("utf-8"))

    sr = raw.get("search-results", {})
    total = sr.get("opensearch:totalResults", "?")

    entries = sr.get("entry", [])
    if not isinstance(entries, list):
        entries = [entries] if entries else []

    papers = []
    for e in entries:
        title = (e.get("dc:title") or "").strip()
        if not title:
            continue

        author_els = e.get("author", [])
        if isinstance(author_els, list) and author_els:
            authors = "; ".join(
                a.get("authname", "") for a in author_els
                if a.get("authname")
            )
        else:
            authors = (e.get("dc:creator") or "").strip()

        venue = (e.get("prism:publicationName") or "").strip()
        year = (e.get("prism:coverDate") or "")[:4]
        doi = (e.get("prism:doi") or "").strip()
        citations = e.get("citedby-count", "0")

        scp = e.get("dc:identifier", "")
        scp_id = scp.replace("SCOPUS_ID:", "") if scp.startswith("SCOPUS_ID:") else ""
        link = (f"https://www.scopus.com/inward/record.uri"
                f"?partnerID=HzOxMe3b&scp={scp_id}&origin=inward") if scp_id else ""

        subtype = (e.get("subtypeDescription") or "").strip()
        doctype = DOCTYPE_MAP.get(subtype.lower(), subtype.title() if subtype else "Unknown")

        oa_flag = e.get("openaccessFlag", "0")
        is_oa = oa_flag == "1"

        papers.append({
            "title": title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "doi": doi,
            "citations": int(citations) if str(citations).isdigit() else 0,
            "link": link,
            "type": doctype,
            "openaccess": is_oa,
            "_source_db": ["scopus"],
        })

    return {
        "total_results": str(total),
        "count": len(papers),
        "papers": papers,
    }


def _deduplicate(papers):
    """DOI 精确去重（跨页可能出现重复）。"""
    seen_dois = set()
    result = []
    for p in papers:
        doi = (p.get("doi") or "").strip()
        if doi and doi in seen_dois:
            continue
        if doi:
            seen_dois.add(doi)
        result.append(p)
    return result


def search_all(query: str, api_key: str, target_count: int,
               start: int = 0, sort: str = "-citedby-count",
               timeout: int = 15, delay: float = 0.3) -> dict:
    """
    自动翻页搜索 Scopus，直到达到 target_count 或结果耗尽。

    返回与旧 search() 兼容的结构，额外带 _pages_fetched。
    """
    all_papers = []
    total_available = "?"
    offset = start
    pages = 0
    # 每页请求数：取 target_count 和 Scopus 上限的较小值
    per_page = min(target_count, SCOPUS_MAX_PER_PAGE)

    while len(all_papers) < target_count:
        pages += 1
        try:
            page_result = _search_one_page(query, api_key, per_page,
                                           offset, sort, timeout)
        except Exception as e:
            print(f"  ⚠️  Scopus page {pages} (start={offset}): {e}",
                  file=sys.stderr)
            break

        new_papers = page_result["papers"]
        total_available = page_result["total_results"]

        if not new_papers:
            break

        all_papers.extend(new_papers)
        offset += len(new_papers)

        # 摘要行
        sample = (new_papers[0].get("title", "") or "")[:60]
        print(f"  [Scopus] Page {pages}: {len(new_papers)} papers "
              f"(total collected: {len(all_papers)}/{total_available}) "
              f"e.g. {sample}...",
              file=sys.stderr)

        # 最后一页（返回少于请求数）
        if len(new_papers) < per_page:
            break

        # 速率限制
        if len(all_papers) < target_count:
            time.sleep(delay)

    # 跨页去重
    before_dedup = len(all_papers)
    all_papers = _deduplicate(all_papers)

    return {
        "database": "scopus",
        "total_results": str(total_available),
        "count": len(all_papers),
        "pages_fetched": pages,
        "dedup_removed": before_dedup - len(all_papers),
        "papers": all_papers,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Scopus Search — auto-paginating lightweight wrapper")
    parser.add_argument("--query", "-q", required=True,
                        help="Scopus search query (e.g. 'TITLE-ABS-KEY(machine learning)')")
    parser.add_argument("--api-key", "-k", required=True, help="Elsevier API Key")
    parser.add_argument("--output", "-o", required=True, help="Output JSON file path")
    parser.add_argument("--count", "-c", type=int, default=25,
                        help="TARGET number of papers (auto-paginates to reach it. Default: 25)")
    parser.add_argument("--start", "-s", type=int, default=0,
                        help="Starting offset (default: 0)")
    parser.add_argument("--sort", default="-citedby-count",
                        help="Sort order (default: -citedby-count)")
    parser.add_argument("--timeout", "-t", type=int, default=15)
    parser.add_argument("--delay", "-d", type=float, default=0.3,
                        help="Delay between API calls in seconds (default: 0.3)")
    args = parser.parse_args()

    try:
        result = search_all(
            query=args.query,
            api_key=args.api_key,
            target_count=args.count,
            start=args.start,
            sort=args.sort,
            timeout=args.timeout,
            delay=args.delay,
        )
    except Exception as e:
        print(f"Scopus ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Write to file — NEVER print paper data to stdout
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # One-line summary — the ONLY thing that enters AI context
    pages_info = f" [{result.get('pages_fetched', 1)} pages]" if result.get('pages_fetched', 1) > 1 else ""
    dedup_info = f" (dedup: -{result.get('dedup_removed', 0)})" if result.get('dedup_removed', 0) > 0 else ""
    print(f"Scopus: {result['count']} results (total: {result['total_results']})"
          f"{pages_info}{dedup_info} → {out}")


if __name__ == "__main__":
    main()
