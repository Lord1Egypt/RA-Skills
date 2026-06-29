#!/usr/bin/env python3
"""
Stdlib-only DuckDuckGo HTML search + URL fetch.

Use this when scripts/search_web.py fails with ModuleNotFoundError on
'bs4' or 'requests' (common on macOS system Python 3.9). Pure stdlib:
urllib, re, html, json, ssl, sys. No pip install required.

Usage:
  python3 search_web_stdlib.py "search query"        # search DDG
  python3 search_web_stdlib.py "https://url" --fetch # fetch + extract
"""

import urllib.request
import urllib.parse
import re
import html
import json
import ssl
import sys


def _ua():
    return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def _ctx():
    c = ssl.create_default_context()
    return c


def search(query: str, n: int = 8) -> list[dict]:
    """Search DuckDuckGo HTML endpoint. Returns list of {title, url, snippet}."""
    url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
    req = urllib.request.Request(url, headers={"User-Agent": _ua()})
    with urllib.request.urlopen(req, timeout=20, context=_ctx()) as r:
        data = r.read().decode("utf-8", "ignore")
    results = []
    # DDG HTML wraps each hit in <div class="result ...">...<a class="result__a" href=...>title</a><a class="result__snippet">...</a>...</div>
    blocks = re.split(r'<div[^>]*class="[^"]*\bresult\b[^"]*"[^>]*>', data)
    for b in blocks[1:n + 8]:
        m_a = re.search(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        m_s = re.search(r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>', b, re.S)
        if m_a:
            href = html.unescape(m_a.group(1))
            title = re.sub(r"<[^>]+>", "", m_a.group(2)).strip()
            snip = re.sub(r"<[^>]+>", "", m_s.group(1)).strip() if m_s else ""
            results.append({
                "title": html.unescape(title),
                "url": href,
                "snippet": html.unescape(snip),
            })
        if len(results) >= n:
            break
    return results


def fetch_url(url: str, max_chars: int = 8000) -> dict:
    """Fetch a URL and extract title + main text. Strips script/style/nav/footer."""
    req = urllib.request.Request(url, headers={"User-Agent": _ua()})
    with urllib.request.urlopen(req, timeout=20, context=_ctx()) as r:
        data = r.read().decode("utf-8", "ignore")
    m_title = re.search(r"<title[^>]*>(.*?)</title>", data, re.S | re.I)
    title = html.unescape(re.sub(r"<[^>]+>", "", m_title.group(1)).strip()) if m_title else ""
    # strip noise
    for tag in ("script", "style", "nav", "footer", "noscript"):
        data = re.sub(rf"<{tag}[^>]*>.*?</{tag}>", " ", data, flags=re.S | re.I)
    # crude main-content extraction
    main = (re.search(r"<main[^>]*>(.*?)</main>", data, re.S | re.I) or
            re.search(r"<article[^>]*>(.*?)</article>", data, re.S | re.I) or
            re.search(r"<body[^>]*>(.*?)</body>", data, re.S | re.I))
    body = main.group(1) if main else data
    text = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    return {
        "url": url,
        "title": title,
        "content": text[:max_chars],
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: search_web_stdlib.py <query|url> [--fetch] [--n N]", file=sys.stderr)
        sys.exit(1)
    arg = sys.argv[1]
    fetch_mode = "--fetch" in sys.argv
    n = 8
    if "--n" in sys.argv:
        i = sys.argv.index("--n")
        n = int(sys.argv[i + 1])
    if fetch_mode or arg.startswith("http"):
        result = fetch_url(arg)
    else:
        result = search(arg, n=n)
    print(json.dumps(result, ensure_ascii=False, indent=2))
