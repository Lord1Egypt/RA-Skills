#!/usr/bin/env python3
"""
Fetch Superinvestor portfolio and activity data from ValueSider.
Usage:
  python fetch_valuesider.py <guru_slug> [--portfolio-only | --activity-only]
  python fetch_valuesider.py --list-gurus [--limit N]
Example guru_slugs: warren-buffett-berkshire-hathaway, mason-hawkins-longleaf-partners
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print('{"error": "Install dependencies: pip install requests beautifulsoup4"}', file=sys.stderr)
    sys.exit(1)

BASE = "https://valuesider.com"


def _get(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    r = requests.get(url, timeout=30, headers=headers)
    r.raise_for_status()
    return r.text


def _text(el) -> str:
    if el is None:
        return ""
    return (el.get_text() or "").strip().replace("\n", " ")


def list_gurus(limit: int = 50) -> list[dict]:
    """Fetch guru list from value-investors page."""
    html = _get(f"{BASE}/value-investors")
    soup = BeautifulSoup(html, "html.parser")
    seen = set()
    out = []
    for a in soup.select('a[href*="/guru/"][href*="/portfolio"]'):
        href = a.get("href") or ""
        m = re.search(r"/guru/([^/]+)/portfolio", href)
        if not m:
            continue
        slug = m.group(1)
        if slug in seen:
            continue
        seen.add(slug)
        name = _text(a)
        if not name or not slug:
            continue
        row = a.find_parent("tr")
        portfolio_val = stocks_count = updated = ""
        if row:
            cells = row.select("td")
            if len(cells) >= 2:
                portfolio_val = _text(cells[1])
            if len(cells) >= 3:
                stocks_count = _text(cells[2])
            if len(cells) >= 4:
                updated = _text(cells[3])
        out.append({
            "slug": slug,
            "name": name,
            "portfolio_value": portfolio_val,
            "stocks_count": stocks_count,
            "last_updated": updated,
            "portfolio_url": urljoin(BASE, href),
        })
        if len(out) >= limit:
            break
    return out


def fetch_portfolio(guru_slug: str) -> dict:
    """Fetch portfolio holdings for a guru."""
    url = f"{BASE}/guru/{guru_slug}/portfolio"
    html = _get(url)
    soup = BeautifulSoup(html, "html.parser")

    summary = {}
    for p in soup.select("p"):
        t = _text(p)
        if "Portfolio value:" in t:
            summary["portfolio_value"] = t.replace("Portfolio value:", "").strip()
        elif "Period:" in t:
            summary["period"] = t.replace("Period:", "").strip()
        elif "Number of stock:" in t:
            summary["number_of_stocks"] = t.replace("Number of stock:", "").strip()
        elif "Update:" in t:
            summary["update_date"] = t.replace("Update:", "").strip()

    holdings = []
    table = soup.find("table")
    if table:
        rows = table.select("tr")
        header = None
        for tr in rows:
            cells = tr.select("td")
            if not cells:
                continue
            texts = [_text(c) for c in cells]
            if not header and len(texts) >= 5:
                header = texts
                continue
            if len(texts) >= 3:
                ticker = texts[0] if texts else ""
                stock_name = texts[1] if len(texts) > 1 else ""
                pct = texts[2] if len(texts) > 2 else ""
                shares = texts[3] if len(texts) > 3 else ""
                reported_price = texts[4] if len(texts) > 4 else ""
                value = texts[6] if len(texts) > 6 else ""
                activity = texts[7] if len(texts) > 7 else ""
                pct_change = texts[8] if len(texts) > 8 else ""
                holdings.append({
                    "ticker": ticker,
                    "stock_name": stock_name,
                    "pct_of_portfolio": pct,
                    "shares": shares,
                    "reported_price": reported_price,
                    "value": value,
                    "activity": activity,
                    "pct_change_to_portfolio": pct_change,
                })

    return {
        "source": url,
        "guru_slug": guru_slug,
        "summary": summary,
        "holdings": holdings,
    }


def fetch_activity(guru_slug: str) -> dict:
    """Fetch portfolio activity (buys/sells) for a guru."""
    url = f"{BASE}/guru/{guru_slug}/portfolio-activity"
    html = _get(url)
    soup = BeautifulSoup(html, "html.parser")

    activities = []
    current_quarter = None
    table = soup.find("table")
    if table:
        for tr in table.select("tr"):
            cells = tr.select("td")
            if not cells:
                continue
            texts = [_text(c) for c in cells]
            if len(texts) == 1 and re.match(r"20\d{2}\s*Q[1-4]", texts[0]):
                current_quarter = texts[0]
                continue
            if len(texts) >= 4 and current_quarter:
                ticker = texts[0] if texts else ""
                stock_name = texts[1] if len(texts) > 1 else ""
                activity_type = texts[2] if len(texts) > 2 else ""
                share_change = texts[3] if len(texts) > 3 else ""
                pct_change = texts[4] if len(texts) > 4 else ""
                reported_price = texts[5] if len(texts) > 5 else ""
                pct_portfolio = texts[7] if len(texts) > 7 else ""
                activities.append({
                    "quarter": current_quarter,
                    "ticker": ticker,
                    "stock_name": stock_name,
                    "activity_type": activity_type,
                    "share_change": share_change,
                    "pct_change_to_portfolio": pct_change,
                    "reported_price": reported_price,
                    "pct_of_portfolio": pct_portfolio,
                })

    return {
        "source": url,
        "guru_slug": guru_slug,
        "activities": activities,
    }


def main():
    ap = argparse.ArgumentParser(description="Fetch ValueSider Superinvestor data")
    ap.add_argument("guru_slug", nargs="?", help="Guru URL slug (e.g. mason-hawkins-longleaf-partners)")
    ap.add_argument("--list-gurus", action="store_true", help="List available gurus and slugs")
    ap.add_argument("--limit", type=int, default=50, help="Max gurus when using --list-gurus")
    ap.add_argument("--portfolio-only", action="store_true", help="Only fetch portfolio")
    ap.add_argument("--activity-only", action="store_true", help="Only fetch activity")
    args = ap.parse_args()

    if args.list_gurus:
        result = {"gurus": list_gurus(limit=args.limit)}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if not args.guru_slug:
        print('{"error": "Provide guru_slug or use --list-gurus"}', file=sys.stderr)
        sys.exit(1)

    out = {"guru_slug": args.guru_slug}
    try:
        if not args.activity_only:
            out["portfolio"] = fetch_portfolio(args.guru_slug)
        if not args.portfolio_only:
            out["activity"] = fetch_activity(args.guru_slug)
    except requests.RequestException as e:
        print(json.dumps({"error": str(e), "guru_slug": args.guru_slug}), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
