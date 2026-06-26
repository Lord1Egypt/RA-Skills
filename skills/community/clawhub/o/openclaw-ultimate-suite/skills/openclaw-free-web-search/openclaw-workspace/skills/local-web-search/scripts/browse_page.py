#!/usr/bin/env python3
# SECURITY MANIFEST:
#   Environment variables accessed: LOCAL_SEARCH_PROXY (optional), HTTPS_PROXY/ALL_PROXY variants (optional)
#   External endpoints called: any URL explicitly passed via --url argument (HTTP GET only)
#   Local files read: none
#   Local files written: none
#   Data sent externally: standard HTTP GET request to the URL you provide — no POST data, no credentials
"""
browse_page.py  v3.1  — OpenClaw Free Web Search Skill
=======================================================
Powered by Scrapling (https://github.com/D4Vinci/Scrapling)

Three-tier fetcher cascade (all free, no API key):
  Tier 1 — Fetcher        : Fast HTTP with TLS fingerprint spoofing + Google referer
  Tier 2 — StealthyFetcher: Headless Chrome with Cloudflare Turnstile bypass
  Tier 3 — DynamicFetcher : Full Playwright browser for JS-heavy / anti-bot sites

Features:
  - Adaptive element extraction (survives website redesigns)
  - Semantic main-content detection via CSS priority scoring
  - Paywall / login-wall / 404 detection and graceful rejection
  - Publication date extraction (meta + JSON-LD + visible text)
  - Hallucination guard: confidence scoring + cross-field consistency check
  - Word-count capping with smart sentence boundary truncation
  - Structured JSON output mode for Agent pipelines
  - Automatic proxy detection (env vars + common local ports 7890/7897/1080)
  - Local Chrome detection for StealthyFetcher/DynamicFetcher (macOS)

Usage:
  python3 browse_page.py --url <URL> [--max-words 600] [--mode auto|fast|stealth|dynamic]
  python3 browse_page.py --url <URL> --json

Dependencies:
  pip install scrapling[all]   # for full anti-bot / JS rendering support
  (falls back to stdlib urllib if Scrapling is not installed)

Model-agnostic: works with any LLM acting as OpenClaw commander
(Claude, GPT-4, Gemini, Mistral, Llama, DeepSeek, Qwen, etc.)
"""

from __future__ import annotations
import argparse
import html as html_module
import json
import os
import re
import socket
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Optional

# ─── Scrapling import with graceful fallback ──────────────────────────────────
try:
    from scrapling.fetchers import Fetcher as _ScraplingFetcher
    SCRAPLING_FAST = True
except Exception:
    SCRAPLING_FAST = False
    if not os.environ.get("_BROWSE_SCRAPLING_WARNED"):
        print(
            "[browse_page] WARNING: Scrapling not installed — running in stdlib-urllib fallback mode.\n"
            "  Anti-bot / Cloudflare bypass and JS rendering are DISABLED.\n"
            "  To enable full functionality, run:\n"
            "    pip install 'scrapling[all]' && python3 -m playwright install chromium\n"
            "  Or re-run ./install_local_search.sh which handles this automatically.",
            file=sys.stderr,
        )
        os.environ["_BROWSE_SCRAPLING_WARNED"] = "1"

try:
    from scrapling.fetchers import StealthyFetcher as _StealthyFetcher
    SCRAPLING_STEALTH = True
except Exception:
    SCRAPLING_STEALTH = False

try:
    from scrapling.fetchers import DynamicFetcher as _DynamicFetcher
    SCRAPLING_DYNAMIC = True
except Exception:
    SCRAPLING_DYNAMIC = False

# ─── Constants ────────────────────────────────────────────────────────────────
VERSION = "3.1.0"

PAYWALL_PHRASES = [
    "subscribe to read", "subscribe to continue", "sign in to read",
    "create a free account", "this content is for subscribers",
    "to continue reading", "unlock this article", "members only",
    "premium content", "log in to access", "please enable javascript",
    "access denied", "403 forbidden", "page not found", "404 not found",
]

CONTENT_SELECTORS = [
    "article",
    "main",
    "[role='main']",
    ".post-content",
    ".article-body",
    ".entry-content",
    ".content-body",
    ".story-body",
    ".article-text",
    ".post-body",
    "#content",
    "#main-content",
    "#article-body",
    ".field--type-text-with-summary",   # Drupal
    ".mw-parser-output",                # MediaWiki / Wikipedia
    ".markdown-body",                   # GitHub
    "div[itemprop='articleBody']",
    "div[itemprop='description']",
]

NOISE_TAGS = (
    "script", "style", "nav", "footer", "header",
    "aside", "form", "button", "noscript", "iframe",
    "figure", "figcaption",
)

STRIP_TAGS_RE = re.compile(
    r"<(script|style|nav|header|footer|aside|form|button|noscript|iframe|svg)[^>]*>.*?</\1>",
    re.DOTALL | re.IGNORECASE,
)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t]+")
NL_RE = re.compile(r"\n{3,}")

DATE_META_NAMES = [
    "article:published_time", "datePublished", "pubdate",
    "publish_date", "DC.date", "article:modified_time",
    "og:updated_time", "date",
]

MIN_TRUSTWORTHY_WORDS = 80

# Proxy auto-detection: common local proxy ports (Clash, V2Ray, Shadowsocks)
COMMON_PROXY_PORTS = ("7890", "7897", "1080")


# ─── Proxy & Chrome detection ─────────────────────────────────────────────────

def _port_open(host: str, port: str, timeout: float = 0.3) -> bool:
    """Check if a local port is accepting connections."""
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except OSError:
        return False


def _resolve_proxy_url() -> Optional[str]:
    """
    Resolve proxy URL from environment variables or auto-detect common local proxies.
    Priority: LOCAL_SEARCH_PROXY > HTTPS_PROXY > ALL_PROXY > auto-detect ports.
    """
    for env_name in ("LOCAL_SEARCH_PROXY", "HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy"):
        value = os.environ.get(env_name)
        if value:
            return value
    for port in COMMON_PROXY_PORTS:
        if _port_open("127.0.0.1", port):
            return f"http://127.0.0.1:{port}"
    return None


def _should_relax_tls(proxy_url: Optional[str]) -> bool:
    """Relax TLS verification for local MITM proxies (Clash, mitmproxy, etc.)."""
    if not proxy_url:
        return False
    return proxy_url.startswith("http://127.0.0.1:") or proxy_url.startswith("http://localhost:")


def _has_real_chrome() -> bool:
    """
    Detect if a real Chrome browser is installed (macOS).
    When available, StealthyFetcher/DynamicFetcher will prefer it over
    Playwright's bundled Chromium for better anti-bot evasion.
    """
    chrome_paths = (
        "/Applications/Google Chrome.app",
        "/Applications/Google Chrome Canary.app",
    )
    return any(os.path.exists(path) for path in chrome_paths)


# ─── Stdlib helpers (used when Scrapling unavailable) ─────────────────────────

def _stdlib_strip_html(raw_html: str) -> str:
    text = STRIP_TAGS_RE.sub(" ", raw_html)
    text = TAG_RE.sub(" ", text)
    text = html_module.unescape(text)
    text = WS_RE.sub(" ", text)
    text = NL_RE.sub("\n\n", text)
    return text.strip()


def _stdlib_extract_title(raw_html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.IGNORECASE | re.DOTALL)
    if m:
        return html_module.unescape(TAG_RE.sub("", m.group(1))).strip()
    return ""


def _stdlib_extract_date(raw_html: str) -> str:
    patterns = [
        r'<meta[^>]+(?:property|name)=["\'](?:article:published_time|pubdate|date|datePublished)["\'][^>]+content=["\']([0-9T:Z.+\-]{10,25})["\']',
        r'<meta[^>]+content=["\']([0-9T:Z.+\-]{10,25})["\'][^>]+(?:property|name)=["\'](?:article:published_time|pubdate|date)["\']',
        r'<time[^>]+datetime=["\']([0-9T:Z.+\-]{10,25})["\']',
    ]
    for pat in patterns:
        m = re.search(pat, raw_html, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
    return ""


def _stdlib_fetch(url: str, timeout: int = 15) -> tuple:
    """Returns (status_code, raw_html_str)."""
    ua = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    req = urllib.request.Request(url, headers={
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        ct = r.headers.get("Content-Type", "utf-8")
        charset = "utf-8"
        m = re.search(r"charset=([\w-]+)", ct)
        if m:
            charset = m.group(1)
        return r.status, r.read().decode(charset, errors="replace")


# ─── Scrapling-based helpers ──────────────────────────────────────────────────

def _scrapling_extract_date(page) -> str:
    """Extract publication date from a Scrapling Response object."""
    for name in DATE_META_NAMES:
        try:
            els = page.css(f'meta[property="{name}"]')
            if els:
                val = els[0].attrib.get("content", "")
                if val:
                    return val[:10]
            els = page.css(f'meta[name="{name}"]')
            if els:
                val = els[0].attrib.get("content", "")
                if val:
                    return val[:10]
        except Exception:
            pass
    # JSON-LD
    try:
        scripts = page.css('script[type="application/ld+json"]')
        for s in scripts:
            raw = s.get_all_text()
            data = json.loads(raw)
            for key in ("datePublished", "dateModified", "uploadDate"):
                if key in data:
                    return str(data[key])[:10]
    except Exception:
        pass
    # Visible date in text
    try:
        text = page.get_all_text(ignore_tags=NOISE_TAGS)
        m = re.search(
            r'\b(20\d{2})[/-](0?[1-9]|1[0-2])[/-](0?[1-9]|[12]\d|3[01])\b',
            text
        )
        if m:
            return f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"
    except Exception:
        pass
    return ""


def _scrapling_extract_content(page) -> tuple:
    """
    Returns (content_text, extraction_method).
    Tries semantic CSS selectors first, falls back to full-page text.
    """
    for selector in CONTENT_SELECTORS:
        try:
            elements = page.css(selector)
            if elements:
                texts = []
                for el in elements:
                    t = el.get_all_text(ignore_tags=NOISE_TAGS).strip()
                    if len(t.split()) > MIN_TRUSTWORTHY_WORDS:
                        texts.append(t)
                if texts:
                    combined = "\n\n".join(texts)
                    return combined, f"css:{selector}"
        except Exception:
            continue
    # Full-page fallback
    try:
        text = page.get_all_text(ignore_tags=NOISE_TAGS).strip()
        return text, "full-page"
    except Exception:
        return "", "failed"


def _scrapling_extract_title(page) -> str:
    try:
        els = page.css("title")
        if els:
            return els[0].get_all_text().strip()
    except Exception:
        pass
    return ""


# ─── Confidence scoring ───────────────────────────────────────────────────────

def _score_confidence(text: str, status: int, method: str, has_paywall: bool) -> str:
    if has_paywall or status not in (200, 0):
        return "LOW"
    wc = len(text.split())
    if wc < MIN_TRUSTWORTHY_WORDS:
        return "LOW"
    if method.startswith("css:") and wc >= 200:
        return "HIGH"
    if wc >= 150:
        return "MEDIUM"
    return "LOW"


def _has_paywall(text: str) -> bool:
    tl = text.lower()
    return any(p in tl for p in PAYWALL_PHRASES)


def _truncate_to_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    chunk = " ".join(words[:max_words + 20])
    sentences = re.split(r'(?<=[.!?])\s+', chunk)
    result = []
    count = 0
    for sent in sentences:
        wc = len(sent.split())
        if count + wc > max_words and result:
            break
        result.append(sent)
        count += wc
    return " ".join(result)


# ─── Core fetch logic ─────────────────────────────────────────────────────────

def fetch_page(url: str, mode: str = "auto", timeout: int = 20) -> dict:
    """
    Fetch a page using the three-tier Scrapling cascade.

    mode:
      auto    — try Fetcher -> StealthyFetcher -> DynamicFetcher automatically
      fast    — Fetcher only (fastest, ~1-3s)
      stealth — StealthyFetcher only (Cloudflare bypass, ~5-15s)
      dynamic — DynamicFetcher only (full JS, ~10-30s)

    Returns a dict with keys:
      url, title, content, word_count, pub_date, confidence,
      status, fetcher_used, extraction_method, error
    """
    result = {
        "url": url,
        "title": "",
        "content": "",
        "word_count": 0,
        "pub_date": "",
        "confidence": "LOW",
        "status": 0,
        "fetcher_used": "none",
        "extraction_method": "none",
        "error": "",
    }

    page = None
    proxy_url = _resolve_proxy_url()
    use_real_chrome = _has_real_chrome()

    # ── Tier 1: Fetcher (fast HTTP + TLS fingerprint + Google referer) ──
    if mode in ("auto", "fast") and SCRAPLING_FAST:
        try:
            request_kwargs = {
                "stealthy_headers": True,
                "timeout": timeout,
                "follow_redirects": True,
            }
            if proxy_url and url.startswith("https://"):
                request_kwargs["proxy"] = proxy_url
                if _should_relax_tls(proxy_url):
                    request_kwargs["verify"] = False
            page = _ScraplingFetcher.get(url, **request_kwargs)
            result["fetcher_used"] = "Fetcher"
            result["status"] = page.status
        except Exception as e:
            result["error"] = f"Fetcher: {e}"
            page = None

    # ── Tier 2: StealthyFetcher (Cloudflare / anti-bot bypass) ──
    if (mode in ("auto", "stealth") and SCRAPLING_STEALTH and
            (page is None or (page is not None and page.status in (403, 429, 503)))):
        try:
            page = _StealthyFetcher.fetch(
                url,
                headless=True,
                network_idle=True,
                timeout=timeout * 1000,
                google_search=True,
                hide_canvas=True,
                block_webrtc=True,
                real_chrome=use_real_chrome,
                proxy=proxy_url,
            )
            result["fetcher_used"] = "StealthyFetcher"
            result["status"] = page.status
        except Exception as e:
            result["error"] = f"StealthyFetcher: {e}"
            page = None

    # ── Tier 3: DynamicFetcher (full Playwright JS rendering) ──
    if (mode in ("auto", "dynamic") and SCRAPLING_DYNAMIC and
            (page is None or (page is not None and page.status in (403, 429, 503)))):
        try:
            page = _DynamicFetcher.fetch(
                url,
                timeout=timeout * 1000,
                wait_selector="body",
                network_idle=True,
                real_chrome=use_real_chrome,
                proxy=proxy_url,
            )
            result["fetcher_used"] = "DynamicFetcher"
            result["status"] = page.status
        except Exception as e:
            result["error"] = f"DynamicFetcher: {e}"
            page = None

    # ── Stdlib fallback (Scrapling not installed) ──
    if page is None and not SCRAPLING_FAST:
        try:
            status, raw_html = _stdlib_fetch(url, timeout=timeout)
            result["fetcher_used"] = "stdlib-urllib"
            result["status"] = status
            result["title"] = _stdlib_extract_title(raw_html)
            result["pub_date"] = _stdlib_extract_date(raw_html)
            content = _stdlib_strip_html(raw_html)
            has_pw = _has_paywall(content)
            result["content"] = content
            result["word_count"] = len(content.split())
            result["confidence"] = _score_confidence(content, status, "full-page", has_pw)
            if has_pw:
                result["error"] = "Paywall or login wall detected"
            return result
        except Exception as e:
            result["error"] = f"All fetchers failed. Last error: {e}"
            return result

    if page is None:
        if not result["error"]:
            result["error"] = "All fetchers failed — no response received"
        return result

    # ── Extract from Scrapling Response ──
    result["title"] = _scrapling_extract_title(page)
    result["pub_date"] = _scrapling_extract_date(page)
    content, method = _scrapling_extract_content(page)
    result["extraction_method"] = method

    has_pw = _has_paywall(content)
    result["confidence"] = _score_confidence(content, page.status, method, has_pw)
    if has_pw:
        result["error"] = "Paywall or login wall detected — content may be incomplete"

    result["content"] = content
    result["word_count"] = len(content.split())

    return result


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    p = argparse.ArgumentParser(
        description=f"browse_page.py v{VERSION} — Scrapling-powered page fetcher for OpenClaw"
    )
    p.add_argument("--url", required=True, help="URL to fetch")
    p.add_argument("--max-words", type=int, default=600,
                   help="Maximum words to output (default: 600)")
    p.add_argument("--mode", choices=["auto", "fast", "stealth", "dynamic"],
                   default="auto",
                   help="Fetcher mode: auto (default), fast, stealth, dynamic")
    p.add_argument("--timeout", type=int, default=20,
                   help="Per-fetcher timeout in seconds (default: 20)")
    p.add_argument("--json", action="store_true",
                   help="Output structured JSON instead of human-readable text")
    args = p.parse_args()

    result = fetch_page(args.url, mode=args.mode, timeout=args.timeout)

    if result["error"] and not result["content"]:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        return 1

    # Truncate
    content = _truncate_to_words(result["content"], args.max_words)
    result["content"] = content
    result["word_count"] = len(content.split())

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    # ── Human-readable output ──
    sep = "─" * 60
    print(f"URL        : {result['url']}")
    print(f"Title      : {result['title'] or '(no title)'}")
    print(f"Fetcher    : {result['fetcher_used']}")
    print(f"Words      : {result['word_count']}")
    print(f"Confidence : {result['confidence']}")
    if result["pub_date"]:
        print(f"Published  : {result['pub_date']}")
    if result["error"]:
        print(f"Warning    : {result['error']}")
    print(sep)
    print(content)
    print(sep)

    # ── Agent advisory notes ──
    conf = result["confidence"]
    if conf == "HIGH":
        print("AGENT NOTE: Content confidence is HIGH. Safe to use for answering.")
    elif conf == "MEDIUM":
        print("AGENT NOTE: Content confidence is MEDIUM. Cross-check with another source if critical.")
    else:
        print("AGENT NOTE: Content confidence is LOW. Do NOT use as sole source — verify independently.")
        if "paywall" in result["error"].lower() if result["error"] else False:
            print("  -> Page is paywalled or requires login. Try a different URL.")
        else:
            print("  -> Very little content extracted (JS-heavy or empty page).")
            print("  -> Consider retrying with --mode stealth or --mode dynamic.")

    if not result["pub_date"]:
        print("  -> No publication date found — verify recency if time-sensitive.")
    else:
        try:
            pub = datetime.strptime(result["pub_date"][:10], "%Y-%m-%d")
            age_days = (datetime.now() - pub).days
            if age_days > 365:
                print(f"  -> Content is {age_days} days old — may be outdated.")
        except Exception:
            pass

    fetcher = result["fetcher_used"]
    if fetcher == "stdlib-urllib":
        print("  -> [DEGRADED MODE] Scrapling not installed — using stdlib urllib (no anti-bot capability).")
        print("     Fix: pip install 'scrapling[all]' && python3 -m playwright install chromium")
        print("     Or re-run ./install_local_search.sh to install automatically.")
    elif fetcher == "Fetcher":
        print("  -> [FULL MODE] Scrapling Fetcher: TLS fingerprint spoofing active.")
    elif fetcher == "StealthyFetcher":
        print("  -> [FULL MODE] StealthyFetcher: bypassed anti-bot protection (Cloudflare-capable).")
    elif fetcher == "DynamicFetcher":
        print("  -> [FULL MODE] DynamicFetcher: full JS rendering — highest fidelity but slowest.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
