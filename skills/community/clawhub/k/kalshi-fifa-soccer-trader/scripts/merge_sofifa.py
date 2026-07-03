#!/usr/bin/env python3
"""
Merge scraped SoFIFA data (sofifa_wc2026.json) into ratings.json.
Run after scrape_sofifa.mjs completes successfully.

Usage:
    python3 scripts/merge_sofifa.py
    python3 scripts/merge_sofifa.py --dry-run
"""

import json
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
SOFIFA_PATH = ROOT / "sofifa_wc2026.json"
RATINGS_PATH = ROOT / "ratings.json"

CANON = {
    "united states": "USA",
    "türkiye": "Turkey",
    "czech republic": "Czech Republic",
    "czechia": "Czech Republic",
    "dr congo": "Congo DR",
    "congo dr": "Congo DR",
    "côte d'ivoire": "Ivory Coast",
    "cote d'ivoire": "Ivory Coast",
    "ivory coast": "Ivory Coast",
    "korea republic": "South Korea",
    "curaçao": "Curaçao",
    "curacao": "Curaçao",
    "cape verde": "Cabo Verde",
    "bosnia and herzegovina": "Bosnia and Herzegovina",
    "bosnia & herzegovina": "Bosnia and Herzegovina",
}

def canon(name: str) -> str:
    return CANON.get(name.lower(), name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing")
    args = parser.parse_args()

    if not SOFIFA_PATH.exists():
        print(f"ERROR: {SOFIFA_PATH} not found. Run scripts/scrape_sofifa.mjs first.")
        return

    with open(SOFIFA_PATH) as f:
        sofifa = json.load(f)

    with open(RATINGS_PATH) as f:
        ratings = json.load(f)

    # Build index of scraped teams by canonical name
    scraped = {}
    for t in sofifa["teams"]:
        key = canon(t["name"])
        scraped[key.lower()] = t

    updated = 0
    for team in ratings["teams"]:
        key = team["name"].lower()
        if key in scraped:
            src = scraped[key]
            changes = []
            for field in ("ovr", "att", "mid", "def", "top11_avg_ovr"):
                if field in src and src[field] is not None:
                    old = team.get(field)
                    if old != src[field]:
                        changes.append(f"{field}: {old} → {src[field]}")
                    team[field] = src[field]
            if changes:
                updated += 1
                print(f"  {team['name']}: {', '.join(changes)}")

    not_in_ratings = [k for k in scraped if k not in {t["name"].lower() for t in ratings["teams"]}]
    if not_in_ratings:
        print(f"\n⚠  Teams in SoFIFA not in ratings.json (add manually): {', '.join(not_in_ratings)}")

    ratings["_meta"]["last_updated"] = sofifa.get("scraped_at", "")[:10]
    ratings["_meta"]["source"] = f"EA Sports FC 26 (SoFIFA, scraped {sofifa.get('scraped_at', '')[:10]})"

    if args.dry_run:
        print(f"\n[DRY RUN] Would update {updated} teams.")
    else:
        with open(RATINGS_PATH, "w") as f:
            json.dump(ratings, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Updated {updated} teams in {RATINGS_PATH}")

if __name__ == "__main__":
    main()
