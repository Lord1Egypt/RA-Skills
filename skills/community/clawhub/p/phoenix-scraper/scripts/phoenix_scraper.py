#!/usr/bin/env python3
"""
phoenix_scraper.py — Resilient three-tier failover scraper.

Tier 1: Brave Search API
Tier 2: Bright Data Web Unlocker (with optional JS render)
Tier 3: Playwright headless browser

Never returns empty. Always returns a result dict.
"""

import os
import json
import re
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional

# ── Config ────────────────────────────────────────────────────────────────────

BRIGHT_DATA_API_KEY = os.environ.get("BRIGHT_DATA_API_KEY", "")
BRIGHT_DATA_ENDPOINT = "https://api.brightdata.com/request"
DEFAULT_ZONE = os.environ.get("BRIGHT_DATA_ZONE", "web_unlocker")
BRAVE_API_KEY = os.environ.get("BRAVE_API_KEY", "")
BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"

TIMEOUT_STANDARD = 30   # seconds
TIMEOUT_RENDER = 60     # seconds (JS render mode)


# ── Result helpers ────────────────────────────────────────────────────────────

def _ok(html: str, method: str, url: str) -> dict:
    return {"success": True, "html": html, "method": method, "url": url, "error": None}

def _fail(method: str, url: str, error: str) -> dict:
    return {"success": False, "html": "", "method": method, "url": url, "error": error}


# ── Tier 1: Brave Search ─────────────────────────────────────────────────────

def _brave_fetch(url: str) -> dict:
    """Use Brave Search to find cached/indexed content for a URL."""
    if not BRAVE_API_KEY:
        return _fail("brave", url, "No BRAVE_API_KEY set")
    try:
        params = urllib.parse.urlencode({"q": f"site:{urllib.parse.urlparse(url).netloc} {url}", "count": 1})
        req = urllib.request.Request(f"{BRAVE_ENDPOINT}?{params}")
        req.add_header("Accept", "application/json")
        req.add_header("Accept-Encoding", "gzip")
        req.add_header("X-Subscription-Token", BRAVE_API_KEY)
        with urllib.request.urlopen(req, timeout=TIMEOUT_STANDARD) as r:
            data = json.loads(r.read())
        results = data.get("web", {}).get("results", [])
        if results:
            snippet = results[0].get("description", "") or results[0].get("extra_snippets", [""])[0]
            if snippet:
                return _ok(f"<p>{snippet}</p>", "brave", url)
        return _fail("brave", url, "No results returned")
    except Exception as e:
        return _fail("brave", url, str(e))


# ── Tier 2: Bright Data Web Unlocker ─────────────────────────────────────────

def _brightdata_fetch(url: str, zone: str = DEFAULT_ZONE, render_js: bool = False) -> dict:
    """Fetch via Bright Data Web Unlocker. Optionally renders JS."""
    if not BRIGHT_DATA_API_KEY:
        return _fail("brightdata", url, "No BRIGHT_DATA_API_KEY set")
    try:
        payload = {"url": url, "zone": zone, "format": "raw"}
        if render_js:
            payload["render"] = True  # boolean, NOT string "html"
        body = json.dumps(payload).encode()
        req = urllib.request.Request(BRIGHT_DATA_ENDPOINT, data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {BRIGHT_DATA_API_KEY}")
        timeout = TIMEOUT_RENDER if render_js else TIMEOUT_STANDARD
        with urllib.request.urlopen(req, timeout=timeout) as r:
            html = r.read().decode("utf-8", errors="ignore")
        if html and len(html) > 500:
            method = f"brightdata_{zone}" + ("_render" if render_js else "")
            return _ok(html, method, url)
        return _fail("brightdata", url, f"Response too short ({len(html)} chars)")
    except urllib.error.HTTPError as e:
        return _fail("brightdata", url, f"HTTP {e.code}: {e.reason}")
    except Exception as e:
        return _fail("brightdata", url, str(e))


# ── Tier 3: Playwright ────────────────────────────────────────────────────────

def _playwright_fetch(url: str) -> dict:
    """Full headless browser fetch via Playwright. Last resort."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page(user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ))
            page.goto(url, timeout=45000, wait_until="networkidle")
            time.sleep(2)
            html = page.content()
            browser.close()
        if html and len(html) > 500:
            return _ok(html, "playwright", url)
        return _fail("playwright", url, f"Response too short ({len(html)} chars)")
    except ImportError:
        return _fail("playwright", url, "Playwright not installed — run: pip install playwright && playwright install chromium")
    except Exception as e:
        return _fail("playwright", url, str(e))


# ── Public API ────────────────────────────────────────────────────────────────

def scrape(
    url: str,
    render_js: bool = False,
    zone: str = DEFAULT_ZONE,
    skip_brave: bool = False,
    skip_brightdata: bool = False,
) -> dict:
    """
    Scrape a URL using the three-tier failover chain.

    Args:
        url:            Target URL
        render_js:      Enable JS rendering via Bright Data (Tier 2)
        zone:           Bright Data zone ('web_unlocker' or 'job_search_scraper')
        skip_brave:     Skip Tier 1 (Brave Search)
        skip_brightdata: Skip Tier 2 (Bright Data)

    Returns:
        dict with keys: success, html, method, url, error
    """
    errors = []

    # Tier 1: Brave
    if not skip_brave:
        result = _brave_fetch(url)
        if result["success"]:
            return result
        errors.append(f"brave: {result['error']}")

    # Tier 2: Bright Data
    if not skip_brightdata:
        result = _brightdata_fetch(url, zone=zone, render_js=render_js)
        if result["success"]:
            return result
        errors.append(f"brightdata: {result['error']}")

        # If render_js not tried yet, try with it
        if not render_js:
            result = _brightdata_fetch(url, zone=zone, render_js=True)
            if result["success"]:
                return result
            errors.append(f"brightdata_render: {result['error']}")

    # Tier 3: Playwright
    result = _playwright_fetch(url)
    if result["success"]:
        return result
    errors.append(f"playwright: {result['error']}")

    # All failed
    return {
        "success": False,
        "html": "",
        "method": "all_failed",
        "url": url,
        "error": " | ".join(errors),
    }


def scrape_text(url: str, **kwargs) -> str:
    """Convenience wrapper — returns plain text stripped of HTML tags."""
    result = scrape(url, **kwargs)
    if not result["success"]:
        return ""
    html = result["html"]
    # Strip tags
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python phoenix_scraper.py <url> [--render] [--zone web_unlocker|job_search_scraper]")
        sys.exit(1)

    url = sys.argv[1]
    render = "--render" in sys.argv
    zone = DEFAULT_ZONE
    if "--zone" in sys.argv:
        idx = sys.argv.index("--zone")
        zone = sys.argv[idx + 1]

    print(f"Scraping: {url}")
    print(f"Zone: {zone} | Render JS: {render}")
    result = scrape(url, render_js=render, zone=zone)
    print(f"\n✅ Method: {result['method']}" if result["success"] else f"\n❌ Failed: {result['error']}")
    if result["success"]:
        print(f"Content length: {len(result['html'])} chars")
        print("\n--- Preview (500 chars) ---")
        print(result["html"][:500])
