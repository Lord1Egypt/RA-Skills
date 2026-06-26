#!/usr/bin/env python3
"""
check_prices.py - Fetch all watched URLs and extract current prices.

Usage:
  python3 check_prices.py

Reads watchlist.json, fetches each URL, extracts price, updates the watchlist,
and prints a JSON array of results to stdout.

Output format (JSON array):
  [
    {
      "name": "Product Name",
      "url": "https://...",
      "old_price": 29.99,
      "new_price": 24.99,
      "change_amount": -5.00,
      "change_pct": -16.72,
      "status": "ok" | "no_price" | "fetch_error",
      "error": "..."         // only on error
    },
    ...
  ]
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from html.parser import HTMLParser

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCHLIST_PATH = os.path.join(SKILL_DIR, "watchlist.json")

PRICE_PATTERNS = [
    r'\$\s*([\d,]+\.\d{2})',
    r'([\d,]+\.\d{2})\s*USD',
    r'USD\s*([\d,]+\.\d{2})',
    r'£\s*([\d,]+\.\d{2})',
    r'€\s*([\d,]+\.\d{2})',
    r'EUR\s*([\d,]+\.\d{2})',
    r'([\d,]+\.\d{2})\s*EUR',
    # JSON-LD structured data price
    r'"price"\s*:\s*"?([\d,]+\.\d{2})"?',
    r'"lowPrice"\s*:\s*"?([\d,]+\.\d{2})"?',
    # meta itemprop
    r'itemprop=["\']price["\'][^>]*content=["\']([^"\']+)["\']',
    r'content=["\']([^"\']+)["\'][^>]*itemprop=["\']price["\']',
    # Generic fallback near price text
    r'(?:price|cost|sale)[^\d]{0,20}([\d,]+\.\d{2})',
]


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_chunks = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True
        # Collect content from relevant meta tags
        if tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("itemprop") == "price" and "content" in attrs_dict:
                try:
                    self.text_chunks.append(f"$" + str(float(attrs_dict["content"])))
                except ValueError:
                    pass

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


def extract_price_from_html(html):
    """
    Multi-pass extraction:
    1. Structured data (JSON-LD, meta itemprop)
    2. Visible text
    3. Raw HTML fallback
    Returns float or None.
    """
    # Pass 1: JSON-LD structured data
    json_ld_blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    for block in json_ld_blocks:
        m = re.search(r'"price"\s*:\s*"?([\d,]+\.?\d*)"?', block)
        if m:
            raw = m.group(1).replace(",", "")
            try:
                val = float(raw)
                if val > 0:
                    return val
            except ValueError:
                pass

    # Pass 2: meta itemprop content
    m = re.search(
        r'<meta[^>]+itemprop=["\']price["\'][^>]+content=["\']([^"\']+)["\']',
        html,
        re.IGNORECASE,
    )
    if not m:
        m = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+itemprop=["\']price["\']',
            html,
            re.IGNORECASE,
        )
    if m:
        raw = m.group(1).replace(",", "")
        try:
            val = float(raw)
            if val > 0:
                return val
        except ValueError:
            pass

    # Pass 3: visible text
    parser = TextExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass
    text = parser.get_text()
    for pattern in PRICE_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            raw = matches[0].replace(",", "")
            try:
                val = float(raw)
                if val > 0:
                    return val
            except ValueError:
                continue

    # Pass 4: raw HTML scan
    for pattern in PRICE_PATTERNS:
        matches = re.findall(pattern, html, re.IGNORECASE)
        if matches:
            raw = matches[0].replace(",", "")
            try:
                val = float(raw)
                if val > 0:
                    return val
            except ValueError:
                continue

    return None


def fetch_page(url):
    """Return (html_str, error_str)."""
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
            "Accept-Encoding": "identity",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            # Anti-bot check: 200 but Captcha/blocked page
            raw = resp.read(512 * 1024)  # cap at 512KB
            encoding = resp.headers.get_content_charset("utf-8")
            html = raw.decode(encoding, errors="replace")
            return html, None
    except urllib.error.HTTPError as e:
        if e.code == 503:
            return None, "HTTP 503: anti-bot / rate limited"
        if e.code == 429:
            return None, "HTTP 429: too many requests"
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"URL error: {e.reason}"
    except Exception as e:
        return None, str(e)


def load_watchlist():
    if not os.path.exists(WATCHLIST_PATH):
        print("[ERROR] watchlist.json not found. Add products first with add_product.py.", file=sys.stderr)
        sys.exit(1)
    with open(WATCHLIST_PATH) as f:
        return json.load(f)


def save_watchlist(products):
    with open(WATCHLIST_PATH, "w") as f:
        json.dump(products, f, indent=2)


def main():
    products = load_watchlist()
    if not products:
        print("[]")
        return

    results = []
    now = datetime.now(timezone.utc).isoformat()

    for i, product in enumerate(products):
        url = product["url"]
        name = product["name"]
        old_price = product.get("last_price") or product.get("baseline_price")

        if i > 0:
            time.sleep(1)  # polite delay between requests

        print(f"[INFO] Checking: {name}", file=sys.stderr)
        html, err = fetch_page(url)

        if err:
            print(f"[WARN] {name}: {err}", file=sys.stderr)
            results.append({
                "name": name,
                "url": url,
                "old_price": old_price,
                "new_price": None,
                "change_amount": None,
                "change_pct": None,
                "status": "fetch_error",
                "error": err,
            })
            continue

        new_price = extract_price_from_html(html)

        if new_price is None:
            print(f"[WARN] {name}: could not extract price from page", file=sys.stderr)
            results.append({
                "name": name,
                "url": url,
                "old_price": old_price,
                "new_price": None,
                "change_amount": None,
                "change_pct": None,
                "status": "no_price",
                "error": "Price not found on page",
            })
            continue

        change_amount = round(new_price - old_price, 2) if old_price is not None else 0.0
        change_pct = (
            round((change_amount / old_price) * 100, 2) if old_price else 0.0
        )

        # Update watchlist entry
        product["last_price"] = new_price
        product["last_checked"] = now
        history = product.setdefault("price_history", [])
        history.append({"price": new_price, "date": now})
        # Keep last 90 entries
        if len(history) > 90:
            product["price_history"] = history[-90:]

        results.append({
            "name": name,
            "url": url,
            "old_price": old_price,
            "new_price": new_price,
            "change_amount": change_amount,
            "change_pct": change_pct,
            "status": "ok",
        })

    save_watchlist(products)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
