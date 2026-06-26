#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import defaultdict

BASE = "https://api.the-odds-api.com/v4/sports"
DEFAULT_BOOKS = ["fanduel", "draftkings", "betmgm"]
DEFAULT_MARKETS = ["h2h", "spreads", "totals"]
DEFAULT_SPORTS = ["baseball_mlb", "basketball_nba", "icehockey_nhl"]


def get_json(url: str):
    with urllib.request.urlopen(url) as resp:
        return json.load(resp)


def american_price(val):
    if val is None:
        return None
    return int(val)


def outcome_map(outcomes, key_name="name"):
    m = {}
    for o in outcomes or []:
        m[o.get(key_name)] = o
    return m


def summarize_game(game):
    home = game.get("home_team")
    away = game.get("away_team")
    books = game.get("bookmakers", []) or []

    best = {
        "h2h": {},
        "spreads": defaultdict(list),
        "totals": defaultdict(list),
    }
    by_book = []

    for b in books:
        book_key = b.get("key")
        book_summary = {"book": book_key, "markets": {}}
        for market in b.get("markets", []) or []:
            mkey = market.get("key")
            outs = market.get("outcomes", []) or []
            if mkey == "h2h":
                mapped = outcome_map(outs)
                h = mapped.get(home)
                a = mapped.get(away)
                if h and a:
                    hp = american_price(h.get("price"))
                    ap = american_price(a.get("price"))
                    book_summary["markets"]["h2h"] = {
                        home: hp,
                        away: ap,
                    }
                    for team, price in [(home, hp), (away, ap)]:
                        prev = best["h2h"].get(team)
                        if prev is None:
                            best["h2h"][team] = {"price": price, "book": book_key}
                        else:
                            if price is not None and prev["price"] is not None:
                                if price > prev["price"]:
                                    best["h2h"][team] = {"price": price, "book": book_key}
            elif mkey == "spreads":
                summary = []
                for o in outs:
                    entry = {
                        "name": o.get("name"),
                        "point": o.get("point"),
                        "price": american_price(o.get("price")),
                    }
                    summary.append(entry)
                    if entry["name"]:
                        best["spreads"][entry["name"]].append({
                            "point": entry["point"],
                            "price": entry["price"],
                            "book": book_key,
                        })
                book_summary["markets"]["spreads"] = summary
            elif mkey == "totals":
                summary = []
                for o in outs:
                    entry = {
                        "name": o.get("name"),
                        "point": o.get("point"),
                        "price": american_price(o.get("price")),
                    }
                    summary.append(entry)
                    if entry["name"]:
                        best["totals"][entry["name"]].append({
                            "point": entry["point"],
                            "price": entry["price"],
                            "book": book_key,
                        })
                book_summary["markets"]["totals"] = summary
        by_book.append(book_summary)

    def range_summary(entries):
        points = sorted({e["point"] for e in entries if e.get("point") is not None})
        prices = sorted({e["price"] for e in entries if e.get("price") is not None})
        return {
            "points": points,
            "prices": prices,
            "books": sorted({e["book"] for e in entries if e.get("book")}),
        }

    return {
        "sport_key": game.get("sport_key"),
        "commence_time": game.get("commence_time"),
        "away_team": away,
        "home_team": home,
        "best_h2h": best["h2h"],
        "spread_ranges": {team: range_summary(entries) for team, entries in best["spreads"].items()},
        "total_ranges": {side: range_summary(entries) for side, entries in best["totals"].items()},
        "bookmakers": by_book,
    }


def fetch_free_web(sport):
    # Very lightweight free fallback: emit empty structured payload with source marker.
    # The skill can then use web search/news context without hard failing on missing paid APIs.
    return {"sport_key": sport, "active": True, "game_count": 0, "games": [], "source": "free-web-fallback"}


def main():
    p = argparse.ArgumentParser(description="Fetch and normalize live odds for GPTSportswriter")
    p.add_argument("--sports", nargs="*", default=DEFAULT_SPORTS, help="Sport keys to fetch")
    p.add_argument("--bookmakers", default=",".join(DEFAULT_BOOKS), help="Comma-separated bookmaker keys")
    p.add_argument("--markets", default=",".join(DEFAULT_MARKETS), help="Comma-separated market keys")
    p.add_argument("--regions", default="us")
    p.add_argument("--odds-format", default="american", choices=["american", "decimal"])
    p.add_argument("--date-format", default="iso", choices=["iso", "unix"])
    p.add_argument("--mode", default="auto", choices=["auto", "premium", "free"])
    p.add_argument("--pretty", action="store_true")
    args = p.parse_args()

    api_key = os.getenv("THE_ODDS_API_KEY")
    requested = [s for s in args.sports if s]
    use_premium = args.mode == "premium" or (args.mode == "auto" and bool(api_key))

    payload = {"generated_from": requested, "mode": args.mode, "sports": []}

    if use_premium:
        active_url = f"{BASE}?apiKey={urllib.parse.quote(api_key)}"
        active = get_json(active_url)
        active_keys = {s.get('key') for s in active if s.get('active')}

        for sport in requested:
            if sport not in active_keys:
                payload["sports"].append({"sport_key": sport, "active": False, "games": [], "source": "the-odds-api"})
                continue
            qs = urllib.parse.urlencode({
                "apiKey": api_key,
                "regions": args.regions,
                "markets": args.markets,
                "oddsFormat": args.odds_format,
                "dateFormat": args.date_format,
                "bookmakers": args.bookmakers,
            })
            url = f"{BASE}/{sport}/odds?{qs}"
            games = get_json(url)
            payload["sports"].append({
                "sport_key": sport,
                "active": True,
                "game_count": len(games),
                "games": [summarize_game(g) for g in games],
                "source": "the-odds-api",
            })
    else:
        for sport in requested:
            payload["sports"].append(fetch_free_web(sport))

    if args.pretty:
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload))


if __name__ == "__main__":
    main()
