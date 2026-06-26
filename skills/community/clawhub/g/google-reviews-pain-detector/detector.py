#!/usr/bin/env python3
"""
Google Reviews Pain Detector
Scans Google/Yelp reviews for businesses and detects pain words indicating
missed calls / unreachable staff — hot signals for Gracie AI Receptionist leads.
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

# ─── Bootstrap scrapling venv ──────────────────────────────────────────────────

SCRAPLING_VENV_SITE = "/Users/wlc-studio/StudioBrain/00_SYSTEM/skills/scrapling/.venv/lib/python3.14/site-packages"
if SCRAPLING_VENV_SITE not in sys.path:
    sys.path.insert(0, SCRAPLING_VENV_SITE)

try:
    from scrapling.fetchers import Fetcher, StealthyFetcher
except ImportError as e:
    print(f"[error] Cannot import Scrapling: {e}", file=sys.stderr)
    print(f"  Make sure to activate venv: source ~/StudioBrain/00_SYSTEM/skills/scrapling/.venv/bin/activate", file=sys.stderr)
    sys.exit(1)

# ─── Config ────────────────────────────────────────────────────────────────────

MASTER_LEAD_LIST = Path("/Users/wlc-studio/StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md")

PAIN_WORDS = [
    "voicemail",
    "no answer",
    "hard to reach",
    "couldn't get through",
    "could not get through",
    "called 3 times",
    "called three times",
    "never called back",
    "missed call",
    "missed my call",
    "didn't answer",
    "did not answer",
    "goes to voicemail",
    "went to voicemail",
    "unanswered",
    "unreachable",
    "left a message",
    "left messages",
    "no one answered",
    "nobody answered",
    "can't reach",
    "cannot reach",
    "phone just rings",
    "rings and rings",
    "answering machine",
]

PAIN_SCORE_MAX = 10


# ─── Fetchers ──────────────────────────────────────────────────────────────────

def fetch_stealth(url: str, timeout_ms: int = 45000) -> str:
    """Fetch a URL using StealthyFetcher (headless browser, bypasses bot detection)."""
    try:
        print(f"  → StealthyFetcher: {url[:80]}...", file=sys.stderr)
        page = StealthyFetcher.fetch(
            url,
            headless=True,
            network_idle=True,
            timeout=timeout_ms,
            solve_cloudflare=True,
        )
        body = page.css("body")
        if body:
            return body[0].get_all_text()
        return ""
    except Exception as e:
        print(f"  [stealth error] {e}", file=sys.stderr)
        return ""


def fetch_basic(url: str) -> str:
    """Fetch a URL using basic Fetcher (fast, may be blocked by some sites)."""
    try:
        print(f"  → Basic fetch: {url[:80]}...", file=sys.stderr)
        page = Fetcher.get(url, stealthy_headers=True, timeout=20, impersonate="chrome")
        body = page.css("body")
        if body:
            return body[0].get_all_text()
        return ""
    except Exception as e:
        print(f"  [fetch error] {e}", file=sys.stderr)
        return ""


# ─── Review sources ─────────────────────────────────────────────────────────────

def fetch_yelp_reviews(business_name: str, address: str = "") -> str:
    """Search Yelp for the business and scrape its reviews page."""
    # Search Yelp
    location = ""
    if address:
        # Extract city/state hint
        parts = re.findall(r'[A-Z]{2}\s*\d{5}|Staten Island|Brooklyn|Queens|Manhattan|Bronx', address)
        location = parts[0] if parts else address.split(",")[-1].strip()
    if not location:
        location = "Staten Island, NY"

    q = urllib.parse.quote_plus(business_name)
    loc = urllib.parse.quote_plus(location)
    search_url = f"https://www.yelp.com/search?find_desc={q}&find_loc={loc}"

    print(f"  → Yelp search: {search_url[:80]}...", file=sys.stderr)
    try:
        page = StealthyFetcher.fetch(
            search_url,
            headless=True,
            network_idle=True,
            timeout=45000,
            solve_cloudflare=True,
        )
        # Find first business result link
        links = page.css('a[href*="/biz/"]')
        if links:
            biz_href = links[0].attrib.get("href", "")
            if biz_href.startswith("/"):
                biz_url = "https://www.yelp.com" + biz_href
            else:
                biz_url = biz_href

            # Strip query params and get reviews page
            biz_base = biz_url.split("?")[0]
            reviews_url = f"{biz_base}?sort_by=rating_asc"  # lowest ratings first = more pain
            print(f"  → Yelp reviews: {reviews_url[:80]}...", file=sys.stderr)
            time.sleep(1)
            reviews_page = StealthyFetcher.fetch(
                reviews_url,
                headless=True,
                network_idle=True,
                timeout=45000,
                solve_cloudflare=True,
            )
            body = reviews_page.css("body")
            if body:
                return body[0].get_all_text()
    except Exception as e:
        print(f"  [yelp error] {e}", file=sys.stderr)

    return ""


def fetch_google_maps_reviews(business_name: str, address: str = "") -> str:
    """Try to scrape Google Maps for the business reviews."""
    query = f"{business_name} {address}".strip()
    url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}"
    return fetch_stealth(url, timeout_ms=45000)


def fetch_google_search_reviews(business_name: str, address: str = "") -> str:
    """Fetch Google search results page for the business reviews."""
    query = f"{business_name} reviews site complaints"
    if address:
        query = f"{business_name} {address} reviews"
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    return fetch_stealth(url)


def follow_review_links(google_text: str) -> str:
    """Extract review site URLs from Google search text and scrape them."""
    # Look for customerlobby, reviews pages from the business site, bbb, etc.
    review_sites = re.findall(
        r'https?://(?:www\.)?(?:customerlobby\.com|bbb\.org|birdeye\.com|reviews\.io|'
        r'trustpilot\.com|angi\.com|homeadvisor\.com)[^\s"<>]+',
        google_text
    )
    texts = []
    for url in review_sites[:2]:
        print(f"  → Following review link: {url[:70]}...", file=sys.stderr)
        t = fetch_basic(url)
        if t and len(t) > 200:
            texts.append(t)
        time.sleep(1)
    return "\n\n".join(texts)


def fetch_all_reviews(business_name: str, address: str = "") -> str:
    """Aggregate review text from multiple sources."""
    all_text = []

    # 1. Google search results (has review snippets embedded)
    gsearch_text = fetch_google_search_reviews(business_name, address)
    if gsearch_text and len(gsearch_text) > 200:
        all_text.append(f"=== GOOGLE SEARCH ===\n{gsearch_text}")
        # Follow any review site links found
        follow_text = follow_review_links(gsearch_text)
        if follow_text:
            all_text.append(f"=== REVIEW SITES ===\n{follow_text}")
    time.sleep(2)

    # 2. Yelp (try, may 403)
    yelp_text = fetch_yelp_reviews(business_name, address)
    if yelp_text and len(yelp_text) > 200:
        all_text.append(f"=== YELP ===\n{yelp_text}")
    time.sleep(2)

    # 3. Google Maps
    maps_text = fetch_google_maps_reviews(business_name, address)
    if maps_text and len(maps_text) > 200:
        all_text.append(f"=== GOOGLE MAPS ===\n{maps_text}")

    return "\n\n".join(all_text)


# ─── Pain detection ─────────────────────────────────────────────────────────────

def extract_sentences(text: str) -> list:
    """Split text into rough sentences/chunks for context snippets."""
    chunks = re.split(r'(?<=[.!?])\s+|\n+', text)
    return [c.strip() for c in chunks if len(c.strip()) > 20]


def detect_pain(text: str) -> dict:
    """Scan text for pain words. Returns hits dict and snippets."""
    text_lower = text.lower()
    sentences = extract_sentences(text)

    hits = {}  # pain_word -> count
    snippets = []  # (pain_word, sentence)

    for pain_word in PAIN_WORDS:
        count = text_lower.count(pain_word)
        if count > 0:
            hits[pain_word] = count
            for sent in sentences:
                if pain_word in sent.lower() and len(snippets) < 10:
                    snippets.append((pain_word, sent[:200]))

    return {"hits": hits, "snippets": snippets}


def calculate_pain_score(hits: dict) -> int:
    """
    Score 0–10:
    - Number of distinct pain words found × 1.5
    - Total occurrences (capped) × 0.5
    """
    if not hits:
        return 0
    distinct = len(hits)
    total = sum(hits.values())
    raw = (distinct * 1.5) + min(total, 10) * 0.5
    return min(int(raw), PAIN_SCORE_MAX)


# ─── Lead list parsing ──────────────────────────────────────────────────────────

def parse_lead_list(path: Path) -> list:
    """Parse markdown table rows from the master lead list."""
    leads = []
    if not path.exists():
        print(f"[error] Lead list not found: {path}", file=sys.stderr)
        return leads

    content = path.read_text()
    row_pattern = re.compile(r'^\|\s*\d+\s*\|(.+)$', re.MULTILINE)

    for match in row_pattern.finditer(content):
        cells = [c.strip() for c in match.group(0).split('|')]
        cells = [c for c in cells if c]

        if len(cells) < 3:
            continue

        business_raw = cells[1] if len(cells) > 1 else ""
        business = re.sub(r'\*+', '', business_raw).strip()

        phone = ""
        address = ""
        for cell in cells[2:]:
            phone_match = re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', cell)
            if phone_match:
                phone = phone_match.group(0)
            if re.search(r'\d+\s+\w+\s+(Ave|Blvd|St|Rd|Dr|Ln|Way|Pl|Ct)', cell, re.I):
                address = cell.strip()

        if business and business not in ("Business", "#"):
            leads.append({"business": business, "phone": phone, "address": address})

    return leads


# ─── Output formatting ──────────────────────────────────────────────────────────

def format_result(result: dict) -> str:
    lines = []
    lines.append("\n" + "═" * 54)
    lines.append(f"🔍 {result['business']}")
    lines.append("═" * 54)

    if result.get("address"):
        lines.append(f"📍 {result['address']}")
    if result.get("phone"):
        lines.append(f"📞 {result['phone']}")

    score = result["pain_score"]
    if score >= 7:
        emoji, label = "🚨", "CRITICAL"
    elif score >= 5:
        emoji, label = "🔥", "HIGH"
    elif score >= 3:
        emoji, label = "⚠️ ", "MODERATE"
    elif score >= 1:
        emoji, label = "💛", "LOW"
    else:
        emoji, label = "✅", "CLEAN"

    lines.append(f"{emoji} PAIN SCORE: {score}/10  [{label}]")
    lines.append(f"   Text scraped: {result.get('text_length', 0):,} chars")

    if result["hits"]:
        hits_str = ", ".join(
            f'"{w}" ({c}x)' for w, c in sorted(result["hits"].items(), key=lambda x: -x[1])
        )
        lines.append(f"🎯 Pain Words: {hits_str}")

        if result["snippets"]:
            lines.append("\n📋 Example Snippets:")
            for _, snippet in result["snippets"][:4]:
                lines.append(f'  • "...{snippet.strip()}..."')
    else:
        lines.append("   No pain words detected in available review text.")

    if score >= 3:
        lines.append("\n✅ HOT LEAD — Strong signal for Gracie AI Receptionist pitch")
    elif score >= 1:
        lines.append("\n   Weak signal — monitor or pitch lightly")

    return "\n".join(lines)


# ─── Save HOT leads ─────────────────────────────────────────────────────────────

def append_hot_lead(result: dict):
    """Append a HOT-tagged entry to the master lead list."""
    path = MASTER_LEAD_LIST
    if not path.exists():
        print(f"[warn] Lead list not found: {path}", file=sys.stderr)
        return

    content = path.read_text()
    date_str = datetime.now().strftime("%Y-%m-%d")
    pain_words = ", ".join(f'"{w}"' for w in result["hits"].keys())
    hot_note = (
        f"🔥 PAIN SCORE {result['pain_score']}/10 | "
        f"Pain words: {pain_words} | Auto-detected {date_str}"
    )

    if f"**{result['business']}**" in content and "PAIN SCORE" in content:
        print(f"  [skip] Already in list with pain tag: {result['business']}", file=sys.stderr)
        return

    row = (
        f"| - | **{result['business']}** | "
        f"{result.get('phone', 'TBD')} | "
        f"{result.get('address', '')} | "
        f"{hot_note} |\n"
    )

    if "AUTO-DETECTED HOT LEADS" not in content:
        header = (
            "\n\n---\n## 🔥 AUTO-DETECTED HOT LEADS (Pain Detector)\n\n"
            "| # | Business | Phone | Address | Notes |\n"
            "|---|----------|-------|---------|-------|\n"
        )
        content += header + row
    else:
        content = content.rstrip() + "\n" + row

    path.write_text(content)
    print(f"  [saved] {result['business']} → master lead list (HOT)", file=sys.stderr)


# ─── Main ───────────────────────────────────────────────────────────────────────

def analyze_business(business: str, address: str = "") -> dict:
    print(f"\n[analyzing] {business} {address}".strip(), file=sys.stderr)
    text = fetch_all_reviews(business, address)

    pain_data = detect_pain(text)
    score = calculate_pain_score(pain_data["hits"])

    return {
        "business": business,
        "address": address,
        "pain_score": score,
        "hits": pain_data["hits"],
        "snippets": pain_data["snippets"],
        "text_length": len(text),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Google Reviews Pain Detector — find businesses losing calls (Gracie leads)"
    )
    parser.add_argument("business", nargs="?", help="Business name to analyze")
    parser.add_argument("--address", default="", help="Optional address for disambiguation")
    parser.add_argument("--list", action="store_true", help="Run against full master lead list")
    parser.add_argument("--save", action="store_true", help="Save HOT leads (score >= 3) to master list")
    parser.add_argument("--json", action="store_true", dest="json_out", help="Output as JSON")
    parser.add_argument("--min-score", type=int, default=0, help="Only show results >= N")
    args = parser.parse_args()

    results = []

    if args.list:
        print(f"[pain-detector] Loading: {MASTER_LEAD_LIST}", file=sys.stderr)
        leads = parse_lead_list(MASTER_LEAD_LIST)
        if not leads:
            print("[error] No leads found.", file=sys.stderr)
            sys.exit(1)

        print(f"[pain-detector] Scanning {len(leads)} businesses...\n", file=sys.stderr)
        for lead in leads:
            result = analyze_business(lead["business"], lead.get("address", ""))
            result["phone"] = lead.get("phone", "")
            results.append(result)
            time.sleep(3)  # be polite

        results.sort(key=lambda r: r["pain_score"], reverse=True)

    elif args.business:
        result = analyze_business(args.business, args.address)
        results.append(result)
    else:
        parser.print_help()
        sys.exit(1)

    if args.min_score > 0:
        results = [r for r in results if r["pain_score"] >= args.min_score]

    # Output
    if args.json_out:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(format_result(r))

        if args.list and results:
            hot = [r for r in results if r["pain_score"] >= 3]
            print(f"\n{'═'*54}")
            print(f"📊 SUMMARY: {len(results)} businesses scanned")
            print(f"🔥 HOT LEADS (score ≥ 3): {len(hot)}")
            if hot:
                print("\nTop leads:")
                for r in hot[:5]:
                    print(f"  {r['pain_score']}/10  {r['business']}  {r.get('phone','')}")

    # Save if requested
    if args.save:
        hot_leads = [r for r in results if r["pain_score"] >= 3]
        print(f"\n[saving] {len(hot_leads)} HOT leads...", file=sys.stderr)
        for r in hot_leads:
            append_hot_lead(r)


if __name__ == "__main__":
    main()
