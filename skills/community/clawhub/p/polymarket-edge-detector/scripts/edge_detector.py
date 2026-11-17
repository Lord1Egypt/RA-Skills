#!/usr/bin/env python3
"""
polymarket-edge-detector: Find mispriced binary contracts on Polymarket.
Compares market price to an external reference probability and scores +EV setups.

Usage:
    python3 edge_detector.py scan
    python3 edge_detector.py scan --category politics
    python3 edge_detector.py market <slug>
    python3 edge_detector.py watch
"""
import argparse
import json
import os
import random
import sys
import time
from datetime import datetime, timezone, timedelta
from typing import Optional


POLY_API_URL = os.environ.get("POLY_API_URL", "https://clob.polymarket.com")
EDGE_THRESHOLD = float(os.environ.get("EDGE_THRESHOLD_PCT", "3.0"))
REFERENCE_SOURCE = os.environ.get("REFERENCE_SOURCE", "market_implied")

MARKETS = [
    {"id": "1", "slug": "btc-100k-2026", "q": "Will BTC hit $100k in 2026?", "cat": "crypto", "days": 175},
    {"id": "2", "slug": "eth-5k-2026", "q": "Will ETH reach $5k in 2026?", "cat": "crypto", "days": 175},
    {"id": "3", "slug": "fed-cuts-q3", "q": "Will the Fed cut rates in Q3 2026?", "cat": "economics", "days": 56},
    {"id": "4", "slug": "us-recession-2026", "q": "Will the US enter recession in 2026?", "cat": "economics", "days": 175},
    {"id": "5", "slug": "sol-300-2026", "q": "Will SOL hit $300 in 2026?", "cat": "crypto", "days": 175},
    {"id": "6", "slug": "gpt5-release-2026", "q": "Will OpenAI release GPT-5 in 2026?", "cat": "tech", "days": 175},
    {"id": "7", "slug": "ai-agent-trillion-2030", "q": "Will AI agents handle 1T+ API calls/day by 2030?", "cat": "tech", "days": 1300},
    {"id": "8", "slug": "us-shutdown-2026", "q": "Will the US government shutdown in 2026?", "cat": "politics", "days": 100},
    {"id": "9", "slug": "lakers-finals-2026", "q": "Will the Lakers make the 2026 NBA Finals?", "cat": "sports", "days": 70},
    {"id": "10", "slug": "super-bowl-kc-2026", "q": "Will the Chiefs win Super Bowl 2026?", "cat": "sports", "days": 30},
    {"id": "11", "slug": "stablecoin-bill-2026", "q": "Will the US pass a stablecoin bill in 2026?", "cat": "politics", "days": 100},
    {"id": "12", "slug": "spot-sol-etf-2026", "q": "Will a SOL spot ETF be approved in 2026?", "cat": "crypto", "days": 100},
]


def fetch_mock_market(m: dict) -> dict:
    bucket = int(time.time() // 300)
    rng = random.Random(int(m["id"]) * 7919 + bucket)
    base_yes = rng.uniform(0.15, 0.85)
    spread = rng.uniform(0.005, 0.025)
    yes_price = round(base_yes, 3)
    no_price = round(1.0 - yes_price + spread * rng.choice([-1, 1]), 3)
    reference = max(0.01, min(0.99, base_yes + rng.gauss(0, 0.04)))
    liq = rng.uniform(5_000, 800_000)
    return {
        **m,
        "yes_price": yes_price,
        "no_price": no_price,
        "reference_prob": round(reference, 3),
        "liquidity_usd": round(liq, 0),
        "volume_24h_usd": round(liq * rng.uniform(0.05, 0.5), 0),
        "resolution_date": (datetime.now(timezone.utc) + timedelta(days=m["days"])).isoformat(),
    }


def compute_edge(m: dict) -> dict:
    """
    Edge = |reference - yes_price| for the side we'd buy.
    BUY_YES when reference > yes_price (market underpriced yes).
    BUY_NO  when (1 - reference) > no_price.
    """
    yes = m["yes_price"]
    no = m["no_price"]
    ref = m["reference_prob"]
    if ref > yes:
        side = "BUY_YES"
        edge_pct = round((ref - yes) * 100, 2)
    elif (1 - ref) > no:
        side = "BUY_NO"
        edge_pct = round(((1 - ref) - no) * 100, 2)
    else:
        side = "PASS"
        edge_pct = round(max(ref - yes, (1 - ref) - no) * 100, 2)

    # Edge decays as time-to-resolution shortens
    days = max(1, m["days"])
    decay = max(0, 1 - (1 / (1 + days / 30)))
    edge_after_decay = round(edge_pct * decay, 2)

    confidence = min(100, int(
        abs(edge_pct) * 8
        + (1 if m["liquidity_usd"] > 50_000 else 0) * 15
        + (1 if days > 14 else 0) * 10
    ))

    return {
        "market_id": m["id"],
        "question": m["q"],
        "category": m["cat"],
        "yes_price": yes,
        "no_price": no,
        "reference_prob": ref,
        "side": side,
        "edge_pct": edge_pct,
        "edge_after_decay_pct": edge_after_decay,
        "days_to_resolution": days,
        "liquidity_usd": m["liquidity_usd"],
        "volume_24h_usd": m["volume_24h_usd"],
        "confidence": confidence,
        "resolution_date": m["resolution_date"],
    }


def cmd_scan(category: Optional[str]) -> None:
    markets = MARKETS
    if category:
        markets = [m for m in markets if m["cat"] == category]
    rows = []
    for m in markets:
        m_filled = fetch_mock_market(m)
        e = compute_edge(m_filled)
        rows.append(e)
    rows = [r for r in rows if abs(r["edge_after_decay_pct"]) >= EDGE_THRESHOLD]
    rows.sort(key=lambda r: r["edge_after_decay_pct"], reverse=True)
    print(json.dumps({
        "results": rows,
        "count": len(rows),
        "threshold_pct": EDGE_THRESHOLD,
        "category": category or "all",
        "as_of": datetime.now(timezone.utc).isoformat(),
    }, indent=2))


def cmd_market(slug: str) -> None:
    match = next((m for m in MARKETS if m["slug"] == slug), None)
    if not match:
        print(json.dumps({"error": f"market not found: {slug}"}))
        return 1
    m_filled = fetch_mock_market(match)
    e = compute_edge(m_filled)
    print(json.dumps(e, indent=2))
    return 0


def cmd_watch() -> None:
    print(f"# Streaming edge alerts | threshold {EDGE_THRESHOLD}% | reference={REFERENCE_SOURCE}", file=sys.stderr)
    try:
        while True:
            rows = [compute_edge(fetch_mock_market(m)) for m in MARKETS]
            hot = [r for r in rows if abs(r["edge_after_decay_pct"]) >= EDGE_THRESHOLD and r["side"] != "PASS"]
            payload = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "hot": hot,
                "total_markets": len(rows),
            }
            print(json.dumps(payload), flush=True)
            time.sleep(120)
    except KeyboardInterrupt:
        return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Polymarket edge detector")
    sub = p.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("scan")
    p1.add_argument("--category", choices=["crypto", "politics", "sports", "economics", "tech"])

    p2 = sub.add_parser("market")
    p2.add_argument("slug")

    sub.add_parser("watch")

    args = p.parse_args()
    if args.cmd == "scan":
        cmd_scan(args.category)
    elif args.cmd == "market":
        return cmd_market(args.slug) or 0
    elif args.cmd == "watch":
        cmd_watch()
    return 0


if __name__ == "__main__":
    sys.exit(main())
