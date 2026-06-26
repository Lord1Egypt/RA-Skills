#!/usr/bin/env python3
import argparse
import json

SPORT_QUERIES = {
    "baseball_mlb": [
        "Covers MLB odds today",
        "OddsShark MLB odds today",
        "Yahoo Sports MLB preview today",
    ],
    "basketball_nba": [
        "Covers NBA odds today",
        "OddsShark NBA odds today",
        "Yahoo Sports NBA preview today",
    ],
    "icehockey_nhl": [
        "Covers NHL odds today",
        "OddsShark NHL odds today",
        "Yahoo Sports NHL preview today",
    ],
    "soccer_epl": [
        "Covers EPL odds today",
        "OddsShark EPL odds today",
        "Yahoo Sports EPL preview today",
    ],
}


def main():
    ap = argparse.ArgumentParser(description="Free-mode public odds query planner for GPTSportswriter")
    ap.add_argument("--sports", nargs="*", default=["baseball_mlb"])
    args = ap.parse_args()

    payload = {"sports": []}
    for sport in args.sports:
        payload["sports"].append({
            "sport_key": sport,
            "queries": SPORT_QUERIES.get(sport, [f"{sport} odds today", f"{sport} betting preview today"]),
            "note": "Use these queries with web search/web fetch to assemble free-mode line snapshots and context.",
        })

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
