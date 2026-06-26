#!/usr/bin/env python3
"""
add_product.py - Add a product URL to the price watchlist.

Usage:
  python3 add_product.py <url> [price] [name]
  python3 add_product.py "https://example.com/product" 29.99 "Widget Pro"
  python3 add_product.py "https://example.com/product"   # auto-fetches price

Watchlist stored at: ~/.openclaw/workspace/skills/price-watcher/watchlist.json
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from html.parser import HTMLParser

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCHLIST_PATH = os.path.join(SKILL_DIR, "watchlist.json")

PRICE_PATTERNS = [
    # $XX.XX or $X,XXX.XX
    r'\$\s*([\d,]+\.\d{2})',
    # XX.XX USD
    r'([\d,]+\.\d{2})\s*USD',
    # USD XX.XX
    r'USD\s*([\d,]+\.\d{2})',
    # £XX.XX
    r'£\s*([\d,]+\.\d{2})',
    # €XX.XX
    r'€\s*([\d,]+\.\d{2})',
    # EUR XX.XX
    r'EUR\s*([\d,]+\.\d{2})',
    # XX.XX EUR
    r'([\d,]+\.\d{2})\s*EUR',
    # Loose fallback: any decimal number near "price" keyword
    r'(?:price|cost|sale)[^\d]{0,20}([\d,]+\.\d{2})',
]


class TextExtractor(HTMLParser):
    """Extract visible text from HTML, skipping scripts/styles."""

    def __init__(self):
        super().__init__()
        self.text_chunks = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            stripped = data.strip()
            if stripped:
                self.text_chunks.append(stripped)

    def get_text(self):
        return " ".join(self.text_chunks)


def extract_price_from_text(text):
    """Try each pattern; return first float match or None."""
    for pattern in PRICE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            raw = matches[0].replace(",", "")
            try:
                return float(raw)
            except ValueError:
                continue
    return None


def extract_title_from_html(html):
    """Best-effort product name from <title> tag."""
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m:
        title = m.group(1).strip()
        # Strip site suffixes like "| Amazon" or "- Best Buy"
        title = re.split(r'\s*[|–—-]\s*(?:Amazon|eBay|Walmart|Best Buy|Target|Costco|Newegg)', title)[0]
        return title[:120].strip()
    return None


def fetch_page(url):
    """Fetch URL with browser-like headers. Returns (html_str, error_str)."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            encoding = resp.headers.get_content_charset("utf-8")
            return raw.decode(encoding, errors="replace"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"URL error: {e.reason}"
    except Exception as e:
        return None, str(e)


def load_watchlist():
    if os.path.exists(WATCHLIST_PATH):
        with open(WATCHLIST_PATH) as f:
            return json.load(f)
    return []


def save_watchlist(products):
    with open(WATCHLIST_PATH, "w") as f:
        json.dump(products, f, indent=2)


def main():
    if len(sys.argv) < 2:
        print("Usage: add_product.py <url> [price] [name]")
        sys.exit(1)

    url = sys.argv[1]
    manual_price = None
    manual_name = None

    if len(sys.argv) >= 3:
        try:
            manual_price = float(sys.argv[2])
        except ValueError:
            print(f"[ERROR] Price must be a number, got: {sys.argv[2]}")
            sys.exit(1)
    if len(sys.argv) >= 4:
        manual_name = sys.argv[3]

    price = manual_price
    name = manual_name

    if price is None or name is None:
        print(f"[INFO] Fetching page: {url}")
        html, err = fetch_page(url)
        if err:
            print(f"[WARN] Could not fetch page: {err}")
            if price is None:
                print("[ERROR] No price provided and page could not be fetched.")
                sys.exit(1)
        else:
            if price is None:
                parser = TextExtractor()
                parser.feed(html)
                text = parser.get_text()
                price = extract_price_from_text(text)
                if price is None:
                    # Try raw HTML (catches JSON-LD price data, etc.)
                    price = extract_price_from_text(html)
                if price is None:
                    print("[WARN] Could not auto-detect price from page.")
                    print("       Run again with an explicit price: add_product.py <url> <price>")
                    sys.exit(1)
                print(f"[INFO] Detected price: ${price:.2f}")
            if name is None:
                name = extract_title_from_html(html) or url

    products = load_watchlist()

    # Check for duplicate URL
    for p in products:
        if p["url"] == url:
            print(f"[WARN] URL already in watchlist as '{p['name']}'. Use check_prices.py to refresh.")
            sys.exit(0)

    now = datetime.now(timezone.utc).isoformat()
    entry = {
        "url": url,
        "name": name or url,
        "baseline_price": price,
        "last_price": price,
        "last_checked": now,
        "price_history": [{"price": price, "date": now}],
    }

    products.append(entry)
    save_watchlist(products)

    print(f"[OK] Added: {entry['name']}")
    print(f"     URL:   {url}")
    print(f"     Price: ${price:.2f}")
    print(f"     Saved: {WATCHLIST_PATH}")


if __name__ == "__main__":
    main()
