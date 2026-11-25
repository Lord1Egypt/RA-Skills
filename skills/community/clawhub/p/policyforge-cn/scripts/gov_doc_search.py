# -*- coding: utf-8 -*-
"""PolicyForge: search official Chinese policy sources and extract citable sentences.

Dependency-free (Python standard library only).

Subcommands
    search    query the gov.cn policy library and print / export the register rows
    fulltext  same library, full-text search (no title field restriction)
    doc       fetch one document body and print citable sentences
    so        fallback search-engine lookup, returns candidate official URLs
    verify    fetch a page and return its <title> plus size (link sanity check)

Examples
    python gov_doc_search.py search 普惠金融 --t bm
    python gov_doc_search.py fulltext "完全成本保险" --kw 保险 --n 10
    python gov_doc_search.py doc "https://www.gov.cn/zhengce/zhengceku/...htm" --kw 保险 金融
    python gov_doc_search.py so "某省 政策性农业保险 实施方案 转发" --host gov.cn
    python gov_doc_search.py search 乡村振兴 --t gw --export register.md

Field facts worth remembering
    * Only two library type values return results: the State Council set and the
      ministry set. Any other value answers every query with zero hits, which is a
      bad-parameter signal, not proof that a document does not exist.
    * Dropping the title-field restriction turns the query into a full-text search;
      that is how you find a document from a half-remembered sentence.
    * Central Committee documents are not in this library at all. Locate them on the
      portal's central-document column and confirm by re-fetching the page title.
    * Endpoint parameters change with site revisions. If a call starts failing, check
      the official search page by hand before burning more attempts.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

TYPE_ALIAS = {
    "gw": "zhengcelibrary_gw",
    "state": "zhengcelibrary_gw",
    "bm": "zhengcelibrary_bm",
    "ministry": "zhengcelibrary_bm",
}

SEARCH_HOST = "https://sousuo.www.gov.cn/search-gov/data"


def utf8_console() -> None:
    """Align stdout with a UTF-8 console code page so Chinese output is not mangled."""
    if os.name != "nt":
        return
    try:
        import ctypes

        if ctypes.windll.kernel32.GetConsoleOutputCP() == 65001:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def build_opener(no_proxy: bool):
    """Return an opener; --no-proxy avoids environment proxies that break TLS here."""
    handlers = [urllib.request.ProxyHandler({})] if no_proxy else []
    return urllib.request.build_opener(*handlers)


def fetch(url: str, timeout: int = 25, no_proxy: bool = False, data: bytes | None = None) -> str:
    opener = build_opener(no_proxy)
    req = urllib.request.Request(url, headers=UA, data=data)
    with opener.open(req, timeout=timeout) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            try:
                raw = gzip.decompress(raw)
            except OSError:
                pass
        charset = resp.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, errors="replace")


def search(
    query: str,
    doc_type: str = "bm",
    title_only: bool = True,
    limit: int = 20,
    page: int = 1,
    timeout: int = 25,
    no_proxy: bool = False,
) -> dict:
    """Query the library. Returns {'total': int, 'hits': [...]}."""
    resolved = TYPE_ALIAS.get(doc_type, doc_type)
    url = (
        "%s?t=%s&q=%s&timetype=timeqb&sort=score&sortType=1&p=%d&n=%d"
        % (SEARCH_HOST, resolved, urllib.parse.quote(query), page, limit)
    )
    if title_only:
        url += "&searchfield=title"
    try:
        payload = json.loads(fetch(url, timeout=timeout, no_proxy=no_proxy))
    except Exception as exc:  # network or JSON shape change
        print("[ERR] query=%s %s" % (query, exc))
        return {"total": 0, "hits": [], "error": str(exc)}

    body = payload.get("searchVO") or {}
    hits = []
    for item in body.get("listVO") or []:
        hits.append(
            {
                "doc_no": item.get("pcode") or "",
                "date": item.get("pubtimeStr") or "",
                "title": re.sub(r"<[^>]+>", "", item.get("title") or "").strip(),
                "url": item.get("url") or "",
                "issuer": item.get("puborg") or "",
                "summary": re.sub(r"<[^>]+>", "", item.get("summary") or "").strip(),
            }
        )
    return {"total": body.get("totalCount") or 0, "hits": hits, "type": resolved}


def print_hits(result: dict, query: str) -> None:
    print("==== query=%s type=%s total=%s hits=%d"
          % (query, result.get("type", "?"), result.get("total"), len(result["hits"])))
    if not result["hits"] and result.get("total") == 0:
        print("    zero hits: check the type value first (state / ministry),")
        print("    then retry without the title restriction.")
    for hit in result["hits"]:
        print("  %s | %s | %s" % (hit["doc_no"] or "-", hit["date"] or "-", hit["title"]))
        if hit["url"]:
            print("      %s" % hit["url"])


def export_markdown(path: str, rows: list[dict], append: bool = True) -> None:
    """Write register rows in the source-register table shape."""
    header = (
        "| No. | Title | Doc. no. | Issued | Issuer | Link | Citation value |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    lines = []
    start = 1
    if append and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            existing = [ln for ln in fh.read().splitlines() if ln.startswith("| ")]
        start = max(1, len(existing) - 1) + 1 if len(existing) > 1 else 1
    else:
        lines.append(header)
    for offset, row in enumerate(rows):
        lines.append(
            "| %02d | %s | %s | %s | %s | %s | 待评 |\n"
            % (
                start + offset,
                row.get("title", "").replace("|", "/"),
                row.get("doc_no", ""),
                row.get("date", ""),
                row.get("issuer", ""),
                row.get("url", ""),
            )
        )
    mode = "a" if append and os.path.exists(path) else "w"
    with open(path, mode, encoding="utf-8") as fh:
        fh.write("".join(lines))
    print("[OK] register rows written to %s" % path)


def page_body(url: str, timeout: int = 30, no_proxy: bool = False) -> str:
    """Fetch and flatten one document body, preferring the official content container."""
    html = fetch(url, timeout=timeout, no_proxy=no_proxy)
    match = re.search(
        r'<div[^>]*(?:id="UCAP-CONTENT"|class="pages_content"|id="content")[^>]*>(.*?)</div>\s*</div>',
        html,
        re.S,
    )
    body = match.group(1) if match else html
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", "\n", body)
    body = (body.replace("&nbsp;", " ")
                .replace("&ldquo;", '"')
                .replace("&rdquo;", '"')
                .replace("&mdash;", "—"))
    body = re.sub(r"[ \t]+", " ", body)
    return re.sub(r"\n{2,}", "\n", body).strip()


def citable_sentences(text: str, keywords: tuple[str, ...] = (), low: int = 10, high: int = 200) -> list[str]:
    """Split on the punctuation Chinese clauses actually use, then keep quotable lines."""
    pieces = re.split(r"[。；\n]", text)
    out = []
    for piece in pieces:
        sentence = piece.strip().strip("　 ")
        if not (low < len(sentence) < high):
            continue
        if keywords and not any(k in sentence for k in keywords):
            continue
        out.append(sentence)
    return out


def metric_sentences(text: str, width: int = 150) -> list[str]:
    """Pull target-year and threshold sentences, the most persuasive lines in a brief."""
    anchors = ("到20", "不低于", "不高于", "覆盖率", "比重", "占比", "增速", "目标")
    found = []
    for anchor in anchors:
        pattern = re.escape(anchor) + r"[^。]{0,%d}" % width
        found.extend(m.group(0).strip() for m in re.finditer(pattern, text))
    return list(dict.fromkeys(s for s in found if len(s) > 8))


def soap_urls(query: str, hosts: tuple[str, ...] = ("gov.cn",), limit: int = 8,
              timeout: int = 25, no_proxy: bool = False) -> tuple[list[str], str]:
    """Fallback search: harvest candidate URLs and the visible text of the result page."""
    url = "https://www.so.com/s?q=" + urllib.parse.quote(query)
    try:
        html = fetch(url, timeout=timeout, no_proxy=no_proxy)
    except Exception as exc:
        print("[ERR] fallback search failed: %s" % exc)
        return [], ""
    urls = []
    for candidate in re.findall(r"https?://[^\"'<> ]+", html):
        candidate = urllib.parse.unquote(candidate).rstrip(".,;)")
        if any(host in candidate for host in hosts) and "so.com" not in candidate and "360.cn" not in candidate:
            urls.append(candidate)
    urls = list(dict.fromkeys(urls))[:limit]
    visible = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))
    return urls, visible


def cmd_search(args) -> int:
    result = search(args.query, args.t, not args.fulltext, args.n, 1, args.timeout, args.no_proxy)
    print_hits(result, args.query)
    if args.export and result["hits"]:
        export_markdown(args.export, result["hits"], append=not args.overwrite)
    return 0 if result["hits"] else 0


def cmd_doc(args) -> int:
    text = page_body(args.url, timeout=args.timeout, no_proxy=args.no_proxy)
    print("[OK] body characters: %d" % len(text))
    print(text[: args.head])
    print("\n--- citable sentences ---")
    for sentence in citable_sentences(text, tuple(args.kw))[: args.top]:
        print(" *", sentence)
    metrics = metric_sentences(text)
    if metrics:
        print("\n--- target / threshold sentences (verify against the source page) ---")
        for sentence in metrics[:10]:
            print(" !", sentence)
    return 0


def cmd_so(args) -> int:
    urls, visible = soap_urls(args.query, tuple(args.host), args.n, args.timeout, args.no_proxy)
    for url in urls:
        print("URL", url)
    if args.kw:
        for match in list(re.finditer(r".{0,120}(%s).{0,120}" % "|".join(map(re.escape, args.kw)), visible))[:8]:
            print(" ..", match.group(0).strip())
    return 0


def cmd_verify(args) -> int:
    html = fetch(args.url, timeout=args.timeout, no_proxy=args.no_proxy)
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    print("title:", (title.group(1).strip() if title else "?"))
    print("bytes:", len(html))
    return 0


def main(argv: list[str]) -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="Search official Chinese policy sources.")
    sub = parser.add_subparsers(dest="command")

    p_search = sub.add_parser("search", help="query the policy library")
    p_search.add_argument("query")
    p_search.add_argument("--t", default="bm", help="state (State Council) or ministry (default ministry)")
    p_search.add_argument("--n", type=int, default=20)
    p_search.add_argument("--fulltext", action="store_true", help="drop the title restriction")
    p_search.add_argument("--export", default="", help="append rows to a markdown register file")
    p_search.add_argument("--overwrite", action="store_true")
    p_search.add_argument("--timeout", type=int, default=25)
    p_search.add_argument("--no-proxy", action="store_true")

    p_full = sub.add_parser("fulltext", help="full-text search across both library types")
    p_full.add_argument("query")
    p_full.add_argument("--kw", nargs="*", default=[])
    p_full.add_argument("--n", type=int, default=10)
    p_full.add_argument("--timeout", type=int, default=25)
    p_full.add_argument("--no-proxy", action="store_true")

    p_doc = sub.add_parser("doc", help="fetch one body and print citable sentences")
    p_doc.add_argument("url")
    p_doc.add_argument("--kw", nargs="*", default=[])
    p_doc.add_argument("--head", type=int, default=2000)
    p_doc.add_argument("--top", type=int, default=20)
    p_doc.add_argument("--timeout", type=int, default=30)
    p_doc.add_argument("--no-proxy", action="store_true")

    p_so = sub.add_parser("so", help="fallback search for candidate official URLs")
    p_so.add_argument("query")
    p_so.add_argument("--host", nargs="*", default=["gov.cn"])
    p_so.add_argument("--kw", nargs="*", default=[])
    p_so.add_argument("--n", type=int, default=8)
    p_so.add_argument("--timeout", type=int, default=25)
    p_so.add_argument("--no-proxy", action="store_true")

    p_verify = sub.add_parser("verify", help="check a page title and size")
    p_verify.add_argument("url")
    p_verify.add_argument("--timeout", type=int, default=25)
    p_verify.add_argument("--no-proxy", action="store_true")

    args = parser.parse_args(argv)
    if args.command == "search":
        return cmd_search(args)
    if args.command == "fulltext":
        for doc_type in ("bm", "gw"):
            result = search(args.query, doc_type, False, args.n, 1, args.timeout, args.no_proxy)
            print_hits(result, args.query)
            time.sleep(0.5)
        return 0
    if args.command == "doc":
        return cmd_doc(args)
    if args.command == "so":
        return cmd_so(args)
    if args.command == "verify":
        return cmd_verify(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
