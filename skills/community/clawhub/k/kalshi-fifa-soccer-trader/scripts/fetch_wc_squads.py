#!/usr/bin/env python3
"""
Fetch official 2026 FIFA World Cup squads from Wikipedia and populate
lineup_cache.json with full 26-man rosters.

This gives lineup_intel.py accurate squad membership data so injury signals
only fire for players genuinely excluded from the WC squad, not just
absent from TheSportsDB's sparse free-tier lineups.

Usage:
    python3 scripts/fetch_wc_squads.py              # all WC teams
    python3 scripts/fetch_wc_squads.py Spain France # specific teams only
    python3 scripts/fetch_wc_squads.py --dry-run    # print squads, don't write
"""

import json
import re
import ssl
import sys
import argparse
from datetime import date
from pathlib import Path
from urllib import request as urlreq
from urllib.parse import urlencode
from urllib.error import URLError

ROOT = Path(__file__).parent.parent
CACHE_PATH = ROOT / "lineup_cache.json"

WIKI_API = "https://en.wikipedia.org/w/api.php"
WC_PAGE = "2026 FIFA World Cup squads"

# ---------------------------------------------------------------------------
# TLS
# ---------------------------------------------------------------------------

def _ssl_ctx() -> ssl.SSLContext:
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def _fetch_url(url: str) -> str:
    ctx = _ssl_ctx()
    req = urlreq.Request(url, headers={"User-Agent": "kalshi-soccer-trader/1.0 (research)"})
    try:
        with urlreq.urlopen(req, timeout=20, context=ctx) as r:
            return r.read().decode("utf-8")
    except URLError as e:
        print(f"  ⚠  Fetch error: {e}")
        return ""


# ---------------------------------------------------------------------------
# Wikipedia wikitext fetch
# ---------------------------------------------------------------------------

def fetch_wikitext(page: str) -> str:
    params = urlencode({
        "action": "query",
        "titles": page,
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "format": "json",
        "formatversion": "2",
    })
    url = f"{WIKI_API}?{params}"
    raw = _fetch_url(url)
    if not raw:
        return ""
    data = json.loads(raw)
    try:
        pages = data["query"]["pages"]
        wikitext = pages[0]["revisions"][0]["slots"]["main"]["content"]
        return wikitext
    except (KeyError, IndexError):
        print("  ⚠  Could not extract wikitext from API response")
        return ""


# ---------------------------------------------------------------------------
# Parse squad tables from wikitext
# ---------------------------------------------------------------------------

def _strip_wiki_markup(s: str) -> str:
    """Remove [[link|text]] → text, [[link]] → link, {{template}} → ''."""
    # [[display|text]] → text
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", s)
    # {{templates}}
    s = re.sub(r"\{\{[^}]+\}\}", "", s)
    # '''bold''', ''italic''
    s = re.sub(r"'{2,3}", "", s)
    # HTML tags
    s = re.sub(r"<[^>]+>", "", s)
    # Wikipedia disambiguation suffixes: "Rodri (footballer, born 1996)" → "Rodri"
    s = re.sub(r"\s*\([^)]*\)\s*$", "", s)
    return s.strip()


def parse_squads(wikitext: str) -> dict:
    """
    Parse the WC squads wikitext into {team_name: [player_full_name, ...]} dict.

    The page structure is:
        == Group A ==
        === Country ===
        {{nat fs player|...}}  or  {{Fs player|...|name=[[Player]]|...}}
    """
    squads = {}

    # Split into sections by === Team === headings
    # Handle both == Group X == and === Team === and = Team = variants
    section_re = re.compile(r"^={2,3}\s*(.+?)\s*={2,3}\s*$", re.MULTILINE)
    sections = section_re.split(wikitext)

    # sections is: [text_before, heading1, content1, heading2, content2, ...]
    current_team = None

    for i, chunk in enumerate(sections):
        if i % 2 == 0:
            # This is content
            if current_team:
                players = _extract_players(chunk)
                if players:
                    squads[current_team] = players
        else:
            # This is a heading
            heading = chunk.strip()
            # Skip group headings like "Group A", "Group B", etc.
            if re.match(r"Group [A-Z]", heading, re.IGNORECASE):
                current_team = None
            elif heading.lower() in ("see also", "references", "external links", "notes"):
                current_team = None
            else:
                current_team = heading

    return squads


def _extract_players(content: str) -> list:
    """
    Extract player full names from a team's squad section wikitext.

    Handles formats:
        {{Fs player|no=1|nat=ESP|pos=GK|name=[[Unai Simón]]|...}}
        {{nat fs player|no=1|pos=GK|name=[[Unai Simón]]|...}}
        {{FIFA WC squad player|name=[[Unai Simón]]|...}}
    """
    players = []
    # Match |name=... parameter inside {{ }} templates
    # The name value may be [[Player Name]] or plain text
    name_re = re.compile(r"\|name\s*=\s*([^\|}\n]+)", re.IGNORECASE)

    for match in name_re.finditer(content):
        raw = match.group(1).strip()
        name = _strip_wiki_markup(raw)
        # Filter out empty strings, template names, etc.
        if name and len(name) > 2 and not name.startswith("{") and not name.startswith("|"):
            # Remove any remaining brackets
            name = re.sub(r"[\[\]{}]", "", name).strip()
            if name:
                players.append(name)

    return players


# ---------------------------------------------------------------------------
# Team name mapping: Wikipedia names → our ratings.json cache keys
# ---------------------------------------------------------------------------

# Map Wikipedia section title → lowercase key used in lineup_cache.json
WIKI_TO_CACHE_KEY = {
    "United States": "united states",
    "USA": "united states",
    "South Korea": "south korea",
    "Korea Republic": "south korea",
    "Saudi Arabia": "saudi arabia",
    "New Zealand": "new zealand",
    "Costa Rica": "costa rica",
    "Cape Verde": "cape verde",
    "Trinidad and Tobago": "trinidad and tobago",
    "DR Congo": "dr congo",
    "Ivory Coast": "ivory coast",
    "Côte d'Ivoire": "ivory coast",
    "Bosnia-Herzegovina": "bosnia and herzegovina",
    "Bosnia and Herzegovina": "bosnia and herzegovina",
}


def _wiki_to_key(wiki_name: str) -> str:
    if wiki_name in WIKI_TO_CACHE_KEY:
        return WIKI_TO_CACHE_KEY[wiki_name]
    return wiki_name.lower()


# ---------------------------------------------------------------------------
# Cache I/O
# ---------------------------------------------------------------------------

def load_cache() -> dict:
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            return json.load(f)
    return {}


def save_cache(cache: dict) -> None:
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fetch WC 2026 official squads from Wikipedia")
    parser.add_argument("teams", nargs="*", help="Specific team names to update (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Print squads without writing cache")
    parser.add_argument("--show-missing", action="store_true", help="Show teams in ratings.json not found in Wikipedia")
    args = parser.parse_args()

    print(f"Fetching Wikipedia page: '{WC_PAGE}'...")
    wikitext = fetch_wikitext(WC_PAGE)
    if not wikitext:
        print("ERROR: Could not fetch wikitext")
        sys.exit(1)

    print(f"  ✓ Got {len(wikitext):,} chars of wikitext")

    print("Parsing squad tables...")
    squads = parse_squads(wikitext)
    print(f"  ✓ Found {len(squads)} team sections")

    if not squads:
        print("ERROR: No squads parsed — page structure may have changed")
        sys.exit(1)

    # Filter to requested teams if specified
    filter_keys = set()
    if args.teams:
        for t in args.teams:
            filter_keys.add(t.lower())
            filter_keys.add(_wiki_to_key(t))

    today = date.today().isoformat()
    cache = {} if args.dry_run else load_cache()
    updated = 0

    for wiki_name, players in sorted(squads.items()):
        cache_key = _wiki_to_key(wiki_name)

        if filter_keys and cache_key not in filter_keys and wiki_name.lower() not in filter_keys:
            continue

        if not players:
            continue

        if args.dry_run:
            print(f"\n[{wiki_name}] ({len(players)} players)")
            for p in players:
                print(f"  {p}")
            continue

        # Build cache entry compatible with lineup_intel.py
        # Use all squad members as recent_starters — injury signals now only
        # fire for players genuinely excluded from the declared WC squad
        cache[cache_key] = {
            "recent_starters": players,
            "last_event_date": today,
            "last_event": f"WC 2026 official squad ({len(players)} players)",
            "n_events_checked": 1,
            "squad_source": "wikipedia",
            "fetched_at": today,
            "events": [],
        }
        print(f"  [{wiki_name}] → '{cache_key}': {len(players)} players")
        updated += 1

    if not args.dry_run:
        save_cache(cache)
        print(f"\n✅ Updated {updated} team(s) → {CACHE_PATH}")

    if args.show_missing:
        # Load ratings.json and report teams not found in Wikipedia
        ratings_path = ROOT / "ratings.json"
        if ratings_path.exists():
            with open(ratings_path) as f:
                data = json.load(f)
            wiki_keys = {_wiki_to_key(k) for k in squads}
            print("\nTeams in ratings.json NOT found in Wikipedia squads:")
            for t in data.get("teams", []):
                tkey = t["name"].lower()
                aliases = [a.lower() for a in t.get("aliases", [])]
                found = tkey in wiki_keys or any(a in wiki_keys for a in aliases)
                if not found:
                    print(f"  {t['name']}")


if __name__ == "__main__":
    main()
