#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PayCensus Trust Check — on-chain x402 merchant risk lookup.

Looks up an address or merchant domain in the public Agent Trust Rank
(real settlement behaviour, hourly, keyless):
    https://agent.paycensus.com/data/rank.json

Stdlib only. Caches rank.json for one hour. Never blocks or moves money.
"""
import argparse
import json
import os
import sys
import time
import urllib.request

RANK_URL = "https://agent.paycensus.com/data/rank.json"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "paycensus")
CACHE = os.path.join(CACHE_DIR, "rank.json")
TTL = 3600


def fetch_rank(force=False):
    os.makedirs(CACHE_DIR, exist_ok=True)
    if (not force and os.path.exists(CACHE)
            and time.time() - os.path.getmtime(CACHE) < TTL):
        try:
            with open(CACHE, "r", encoding="utf-8") as f:
                return json.load(f), True
        except ValueError:
            pass
    req = urllib.request.Request(
        RANK_URL, headers={"User-Agent": "paycensus-trust-check/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    tmp = CACHE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f)
    os.replace(tmp, CACHE)
    return data, False


def match_entries(entries, addr=None, domain=None):
    out = []
    for e in entries:
        e_addr = (e.get("addr") or "").lower()
        e_dom = (e.get("domain") or "").lower()
        if addr:
            if e_addr == addr.lower():
                out.append(e)
        elif domain:
            d = domain.lower().strip().lstrip(".")
            if e_dom == d or e_dom.endswith("." + d):
                out.append(e)
    return out


def verdict_for(score):
    if score >= 60:
        return "trusted"
    if score >= 20:
        return "caution"
    return "weak"


def main():
    ap = argparse.ArgumentParser(
        description="PayCensus Trust Check - on-chain x402 merchant risk lookup")
    ap.add_argument("--addr", help="payment address (payTo), 0x…")
    ap.add_argument("--domain", help="merchant domain, e.g. api.example.com")
    ap.add_argument("--min-score", type=float, default=None,
                    help="policy floor; adds meetsFloor to output")
    ap.add_argument("--refresh", action="store_true",
                    help="bypass the 1-hour cache")
    a = ap.parse_args()
    if not a.addr and not a.domain:
        ap.error("provide --addr or --domain")

    try:
        data, cached = fetch_rank(force=a.refresh)
    except Exception as ex:  # noqa: BLE001
        print(json.dumps({"error": "rank.json unavailable: %s" % str(ex)[:120],
                          "advice": "data source down - fall back to user judgement, never invent a score"}))
        sys.exit(0)

    rows = match_entries(data.get("ranked", []), addr=a.addr, domain=a.domain)
    rows.sort(key=lambda e: -(float(e.get("score") or 0)))
    best = rows[0] if rows else None

    if best is None:
        out = {
            "queried": {"addr": a.addr, "domain": a.domain},
            "found": False,
            "matches": 0,
            "best": None,
            "verdict": "unknown",
            "meetsFloor": None if a.min_score is None else False,
            "data_generated_at": data.get("generated_at"),
            "cached": cached,
            "advice": ("no observed x402 settlements for this payee - unknown "
                       "is NOT a scam signal by itself; advise a small first "
                       "payment or off-chain verification"),
        }
        print(json.dumps(out, indent=1))
        sys.exit(0)

    score = float(best.get("score") or 0)
    verdict = verdict_for(score)
    advice = "score %.1f: %s" % (score, verdict)
    meets = None
    if a.min_score is not None:
        meets = score >= a.min_score
        advice = "score %.1f %s floor %.1f - %s" % (
            score, ">=" if meets else "<", a.min_score,
            "proceed" if meets else "below configured floor")

    out = {
        "queried": {"addr": a.addr, "domain": a.domain},
        "found": True,
        "matches": len(rows),
        "best": {
            "addr": best.get("addr"),
            "domain": best.get("domain"),
            "score": score,
            "class": best.get("class"),
            "volume_usd": best.get("volume"),
            "buyers": best.get("buyers"),
            "avg_ticket": best.get("avg_ticket"),
            "verified": best.get("verified"),
            "price_usdc": best.get("price_usdc"),
            "chains_settled": best.get("chains_settled"),
        },
        "verdict": verdict,
        "meetsFloor": meets,
        "data_generated_at": data.get("generated_at"),
        "cached": cached,
        "advice": advice,
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
