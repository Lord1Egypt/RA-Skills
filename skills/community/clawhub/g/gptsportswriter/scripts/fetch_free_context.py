#!/usr/bin/env python3
import argparse
import json
import sys

FREE_SOURCE_HINTS = {
    "baseball_mlb": ["Covers MLB odds", "OddsShark MLB picks", "Yahoo Sports MLB preview"],
    "basketball_nba": ["Covers NBA odds", "OddsShark NBA picks", "Yahoo Sports NBA preview"],
    "icehockey_nhl": ["Covers NHL odds", "OddsShark NHL picks", "Yahoo Sports NHL preview"],
    "soccer_epl": ["Covers EPL odds", "OddsShark soccer odds", "Yahoo Sports soccer preview"],
}


def main():
    ap = argparse.ArgumentParser(description="Provide free/public-source hints for GPTSportswriter")
    ap.add_argument("--sports", nargs="*", default=["baseball_mlb"])
    args = ap.parse_args()

    out = []
    for sport in args.sports:
        out.append({
            "sport_key": sport,
            "sources": FREE_SOURCE_HINTS.get(sport, ["Yahoo Sports", "AP Sports", "ESPN"]),
            "note": "Use public odds/news pages and treat prices as snapshots that may be stale.",
        })
    print(json.dumps({"sports": out}, indent=2))


if __name__ == "__main__":
    main()
