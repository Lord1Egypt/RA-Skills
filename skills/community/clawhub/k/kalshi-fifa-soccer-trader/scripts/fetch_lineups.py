#!/usr/bin/env python3
"""
Fetch recent match lineups from TheSportsDB (free tier, no API key needed).
Caches confirmed starters to lineup_cache.json for injury signal detection.

Usage:
    python3 scripts/fetch_lineups.py Sweden Tunisia
    python3 scripts/fetch_lineups.py --all
    python3 scripts/fetch_lineups.py --demo Sweden Tunisia
"""

import json
import ssl
import sys
import time
import argparse
import unicodedata
from datetime import date
from pathlib import Path
from urllib import request as urlreq
from urllib.error import URLError
from urllib.parse import quote
from typing import Optional

# ---------------------------------------------------------------------------
# TLS: use certifi if installed (recommended on macOS Python 3.9 which lacks
# bundled CA certs), otherwise fall back to the system default context.
# Do NOT disable certificate verification — that opens MITM attacks.
# Fix on macOS if you see SSLCertVerificationError:
#   pip install certifi
#   /Applications/Python\ 3.x/Install\ Certificates.command
# ---------------------------------------------------------------------------
def _make_ssl_ctx() -> ssl.SSLContext:
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()
    return ctx

ROOT = Path(__file__).parent.parent
RATINGS_PATH = ROOT / "ratings.json"
CACHE_PATH = ROOT / "lineup_cache.json"

API_BASE = "https://www.thesportsdb.com/api/v1/json/3"
SLEEP_BETWEEN = 0.8  # seconds between requests (be polite)

# Pre-populated TheSportsDB team IDs for WC 2026 teams
# Run with --find-ids to discover missing ones
KNOWN_IDS = {
    "argentina":            133912,
    "australia":            133916,  # NOTE: recheck — may be wrong
    "belgium":              133948,
    "brazil":               133913,
    "canada":               133604,  # may be wrong — search to verify
    "colombia":             133914,
    "croatia":              133915,
    "ecuador":              133947,
    "egypt":                134386,
    "england":              133604,
    "france":               133918,
    "germany":              133945,
    "ghana":                134387,
    "iran":                 134386,   # placeholder — verify
    "japan":                133772,
    "mexico":               133906,
    "morocco":              134390,
    "netherlands":          133921,
    "norway":               133923,
    "portugal":             133917,
    "saudi arabia":         134385,
    "senegal":              134392,
    "south korea":          133922,
    "spain":                133909,
    "sweden":               133916,
    "switzerland":          133924,
    "tunisia":              136142,
    "united states":        133616,
    "usa":                  133616,
    "uruguay":              133920,
}

_SSL_CTX = None

def _ssl_ctx() -> ssl.SSLContext:
    global _SSL_CTX
    if _SSL_CTX is None:
        _SSL_CTX = _make_ssl_ctx()
    return _SSL_CTX


def _fetch(url: str) -> dict:
    try:
        with urlreq.urlopen(url, timeout=12, context=_ssl_ctx()) as r:
            return json.loads(r.read())
    except URLError as e:
        print(f"  ⚠  Fetch error: {e}")
        return {}
    except json.JSONDecodeError:
        print(f"  ⚠  JSON decode error for {url}")
        return {}


def search_team_id(name: str) -> Optional[int]:
    """Search TheSportsDB for a team; return team_id or None."""
    encoded = quote(name)
    url = f"{API_BASE}/searchteams.php?t={encoded}"
    data = _fetch(url)
    teams = data.get("teams") or []
    # Prefer international (national) teams
    for t in teams:
        sport = (t.get("strSport") or "").lower()
        country = (t.get("strCountry") or "").lower()
        team_name = (t.get("strTeam") or "").lower()
        if sport == "soccer" and (team_name == name.lower() or country == name.lower()):
            return int(t["idTeam"])
    # Fallback: first soccer result
    for t in teams:
        if (t.get("strSport") or "").lower() == "soccer":
            return int(t["idTeam"])
    return None


def fetch_recent_starters(team_id: int, n_events: int = 5) -> dict:
    """
    Fetch the last n_events for team_id and collect all confirmed starters
    (strSubstitute == "No", strHome == "Yes" or "No" for the team side).

    Returns:
        {
            "recent_starters": ["Alexander Isak", ...],   # deduplicated
            "last_event_date": "2026-06-04",
            "last_event": "Sweden 2-2 Greece",
            "n_events_checked": 3,
            "events": [{"id": ..., "date": ..., "match": ..., "starters": [...]}]
        }
    """
    url = f"{API_BASE}/eventslast.php?id={team_id}"
    data = _fetch(url)
    events = data.get("results") or []

    if not events:
        return {"recent_starters": [], "last_event_date": None, "last_event": None, "n_events_checked": 0}

    events = events[:n_events]
    all_starters = set()
    event_details = []

    last_event = events[0]
    last_date = last_event.get("dateEvent", "?")
    last_match = f"{last_event.get('strHomeTeam','?')} {last_event.get('intHomeScore','?')}-{last_event.get('intAwayScore','?')} {last_event.get('strAwayTeam','?')}"

    for event in events:
        eid = event.get("idEvent")
        if not eid:
            continue

        # Determine if our team was home or away in this event
        home_id = str(event.get("idHomeTeam", ""))
        our_side = "Yes" if home_id == str(team_id) else "No"

        lineup_url = f"{API_BASE}/lookuplineup.php?id={eid}"
        lineup_data = _fetch(lineup_url)
        lineup = lineup_data.get("lineup") or []
        time.sleep(SLEEP_BETWEEN)

        match_label = f"{event.get('strHomeTeam','?')} {event.get('intHomeScore','?')}-{event.get('intAwayScore','?')} {event.get('strAwayTeam','?')}"

        # Filter to only our team's starters using strHome flag
        starters = [
            p["strPlayer"]
            for p in lineup
            if (p.get("strSubstitute", "") == "No"
                and p.get("strPlayer")
                and p.get("strHome", "") == our_side)
        ]
        all_starters.update(starters)
        event_details.append({
            "id": eid,
            "date": event.get("dateEvent"),
            "match": match_label,
            "starters": starters,
        })

    return {
        "recent_starters": sorted(all_starters),
        "last_event_date": last_date,
        "last_event": last_match,
        "n_events_checked": len(event_details),
        "events": event_details,
    }


def load_cache() -> dict:
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            return json.load(f)
    return {}


def save_cache(cache: dict) -> None:
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def update_team(team_name: str, cache: dict, verbose: bool = True) -> dict:
    """Fetch and cache lineup data for one team. Returns updated cache entry."""
    key = team_name.lower()

    team_id = KNOWN_IDS.get(key)
    if not team_id:
        if verbose:
            print(f"  Searching TheSportsDB for '{team_name}'...")
        team_id = search_team_id(team_name)
        time.sleep(SLEEP_BETWEEN)

    if not team_id:
        if verbose:
            print(f"  ⚠  Could not find team ID for '{team_name}'")
        return {}

    if verbose:
        print(f"  Team ID: {team_id} — fetching recent events...")

    result = fetch_recent_starters(team_id, n_events=5)
    result["team_id"] = team_id
    result["fetched_at"] = date.today().isoformat()

    # Merge with existing cache (e.g. Wikipedia squad data from fetch_wc_squads.py).
    # Adding TheSportsDB match starters to the existing recent_starters list rather
    # than replacing it means the full official squad stays in the cache.
    existing = cache.get(key, {})
    sq = existing.get("squad_source") or ""
    if sq.startswith("wikipedia") and existing.get("recent_starters"):
        merged = sorted(set(existing["recent_starters"]) | set(result["recent_starters"]))
        result["recent_starters"] = merged
        result["squad_source"] = "wikipedia+thesportsdb"

    cache[key] = result

    if verbose:
        n = len(result["recent_starters"])
        last = result.get("last_event", "?")
        print(f"  ✓ {n} confirmed starters found across {result['n_events_checked']} event(s)")
        print(f"    Last event: {last} ({result.get('last_event_date', '?')})")
        if result["recent_starters"]:
            print(f"    Sample: {', '.join(result['recent_starters'][:5])}")

    return result


def demo_prediction(team_a: str, team_b: str) -> None:
    """Run a formation-aware OVR prediction demo and show lineup intelligence."""
    import sys
    sys.path.insert(0, str(ROOT))
    from lineup_intel import effective_lineup_ovr, print_xi, DEFAULT_FORMATION, formation_ovr
    import math

    cache = load_cache()

    print(f"\n{'='*60}")
    print(f"  LINEUP INTELLIGENCE DEMO: {team_a} vs {team_b}")
    print(f"{'='*60}")

    # Load ratings for both teams
    with open(RATINGS_PATH) as f:
        data = json.load(f)
    teams_map = {}
    for t in data["teams"]:
        teams_map[t["name"].lower()] = t
        for alias in t.get("aliases", []):
            teams_map[alias.lower()] = t

    for name in [team_a, team_b]:
        print_xi(name, DEFAULT_FORMATION)
        ovr, signals = effective_lineup_ovr(name, DEFAULT_FORMATION, verbose=True)
        print(f"  Effective OVR (with injury check): {ovr}")
        for s in signals:
            print(f"    {s}")

    # Updated prediction
    ovr_a, sigs_a = effective_lineup_ovr(team_a, DEFAULT_FORMATION, verbose=False)
    ovr_b, sigs_b = effective_lineup_ovr(team_b, DEFAULT_FORMATION, verbose=False)

    BASE_GOALS = 1.35
    ALPHA = 0.022
    HOME_BOOST = 0.12  # neutral venue for WC
    delta = ovr_a - ovr_b
    lam_a = BASE_GOALS * math.exp(ALPHA * delta)
    lam_b = BASE_GOALS * math.exp(-ALPHA * delta)

    def poisson(lam, k):
        return (lam ** k) * math.exp(-lam) / math.factorial(k)

    MAX_G = 10
    grid = [[poisson(lam_a, i) * poisson(lam_b, j) for j in range(MAX_G)] for i in range(MAX_G)]
    p_a = p_draw = p_b = 0.0
    for i in range(MAX_G):
        for j in range(MAX_G):
            v = grid[i][j]
            if i > j: p_a += v
            elif i == j: p_draw += v
            else: p_b += v

    # Most likely score
    best_score = (0, 0, 0.0)
    for i in range(MAX_G):
        for j in range(MAX_G):
            if grid[i][j] > best_score[2]:
                best_score = (i, j, grid[i][j])

    print(f"\n{'─'*60}")
    print(f"  PREDICTION (neutral venue, formation-aware OVR)")
    print(f"{'─'*60}")
    print(f"  {team_a:<16} OVR={ovr_a}  λ={lam_a:.3f}")
    print(f"  {team_b:<16} OVR={ovr_b}  λ={lam_b:.3f}")
    print()
    print(f"  {team_a} win:  {p_a*100:5.1f}%")
    print(f"  Draw:          {p_draw*100:5.1f}%")
    print(f"  {team_b} win:  {p_b*100:5.1f}%")
    print(f"\n  Most likely score: {team_a} {best_score[0]}–{best_score[1]} {team_b}  ({best_score[2]*100:.1f}%)")
    print()

    # Injury flags
    for name, sigs in [(team_a, sigs_a), (team_b, sigs_b)]:
        relevant = [s for s in sigs if "⚠" in s or "❓" in s]
        if relevant:
            print(f"  {name} flags:")
            for s in relevant:
                print(f"    {s}")


def main():
    parser = argparse.ArgumentParser(description="Fetch WC 2026 team lineups from TheSportsDB")
    parser.add_argument("teams", nargs="*", help="Team names to fetch (e.g. Sweden Tunisia)")
    parser.add_argument("--all", action="store_true", help="Fetch all teams in ratings.json")
    parser.add_argument("--demo", action="store_true", help="Show prediction demo for specified teams")
    parser.add_argument("--find-ids", action="store_true", help="Search and print team IDs (don't update cache)")
    args = parser.parse_args()

    cache = load_cache()

    if args.all:
        if not RATINGS_PATH.exists():
            print("ERROR: ratings.json not found")
            sys.exit(1)
        with open(RATINGS_PATH) as f:
            data = json.load(f)
        team_names = [t["name"] for t in data["teams"]]
    elif args.teams:
        team_names = args.teams
    else:
        parser.print_help()
        sys.exit(0)

    if args.demo and len(team_names) >= 2:
        # Update cache for both teams first
        for name in team_names[:2]:
            print(f"\n[{name}]")
            update_team(name, cache, verbose=True)
        save_cache(cache)
        demo_prediction(team_names[0], team_names[1])
        return

    for name in team_names:
        print(f"\n[{name}]")
        if args.find_ids:
            tid = search_team_id(name)
            print(f"  ID: {tid}")
            time.sleep(SLEEP_BETWEEN)
        else:
            update_team(name, cache, verbose=True)

    if not args.find_ids:
        save_cache(cache)
        print(f"\n✅ Saved → {CACHE_PATH}")


if __name__ == "__main__":
    main()
