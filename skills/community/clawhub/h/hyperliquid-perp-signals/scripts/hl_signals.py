#!/usr/bin/env python3
"""
hyperliquid-perp-signals: Signal scanner for Hyperliquid perpetual futures.
Funding rates, OI shifts, liquidation events, cross-venue basis.

Usage:
    python3 hl_signals.py funding
    python3 hl_signals.py funding SOL
    python3 hl_signals.py oi
    python3 hl_signals.py liqs
    python3 hl_signals.py basis BTC
    python3 hl_signals.py squeeze ETH
"""
import argparse
import json
import os
import random
import sys
import time
from datetime import datetime, timezone
from typing import Optional


HL_API_URL = os.environ.get("HL_API_URL", "https://api.hyperliquid.xyz/info")
INCLUDE_BINANCE = os.environ.get("HL_BINANCE_FUNDING_COMPARE", "true").lower() != "false"

COINS = ["BTC", "ETH", "SOL", "ARB", "OP", "AVAX", "DOGE", "WIF", "INJ", "SUI",
         "APT", "TIA", "LINK", "MATIC", "ATOM", "TON", "PEPE", "TRX", "LTC", "BCH"]


def fetch_mock_meta(coin: str) -> dict:
    """
    Production: POST {type: "metaAndAssetCtxs"} to HL_API_URL and parse.
    Mock: deterministic synthesis keyed on coin + minute bucket.
    """
    bucket = int(time.time() // 60)
    rng = random.Random(sum(ord(c) for c in coin) + bucket)
    base_prices = {
        "BTC": 65_000, "ETH": 3_400, "SOL": 150, "ARB": 1.10, "OP": 2.30,
        "AVAX": 35, "DOGE": 0.16, "WIF": 2.10, "INJ": 28, "SUI": 1.05,
        "APT": 8.5, "TIA": 6.8, "LINK": 14, "MATIC": 0.72, "ATOM": 8.4,
        "TON": 6.5, "PEPE": 0.000009, "TRX": 0.13, "LTC": 85, "BCH": 410,
    }
    px = base_prices.get(coin, 10.0)
    drift = rng.uniform(-0.03, 0.03)
    mark = round(px * (1 + drift), 6 if px < 0.001 else 4)
    funding_1h = round(rng.gauss(0.0001, 0.0004), 6)
    oi_usd = rng.uniform(10_000_000, 800_000_000)
    oi_chg = rng.gauss(0, 5)
    return {
        "coin": coin,
        "mark_price": mark,
        "oracle_price": round(px, 6 if px < 0.001 else 4),
        "funding_rate_1h": funding_1h,
        "open_interest_usd": round(oi_usd, 0),
        "oi_change_24h_pct": round(oi_chg, 2),
        "next_funding_eta_seconds": rng.randint(60, 3600),
    }


def fetch_mock_binance_funding(coin: str) -> dict:
    bucket = int(time.time() // 60)
    rng = random.Random(sum(ord(c) for c in coin) * 7 + bucket)
    funding_8h = round(rng.gauss(0.0001, 0.0003), 6)
    return {"coin": coin, "funding_rate_8h": funding_8h}


def classify_bias(meta: dict) -> str:
    f = meta["funding_rate_1h"]
    if f > 0.001:
        return "LONG_BIAS"
    if f < -0.0005:
        return "SHORT_BIAS"
    return "NEUTRAL"


def squeeze_score(meta: dict) -> dict:
    """
    Short-squeeze setup: negative funding + OI build + mark > oracle
    Higher score = stronger setup.
    """
    score = 50
    if meta["funding_rate_1h"] < -0.0005:
        score += 20
    if meta["oi_change_24h_pct"] > 3:
        score += 15
    if meta["mark_price"] > meta["oracle_price"]:
        score += 15
    if abs(meta["mark_price"] - meta["oracle_price"]) / meta["oracle_price"] > 0.005:
        score += 5
    score = min(100, max(0, score))
    return {
        "coin": meta["coin"],
        "score": score,
        "verdict": "STRONG" if score >= 80 else "MODERATE" if score >= 65 else "WEAK",
        "components": {
            "negative_funding": meta["funding_rate_1h"] < -0.0005,
            "oi_build_24h": meta["oi_change_24h_pct"] > 3,
            "mark_premium": meta["mark_price"] > meta["oracle_price"],
        },
    }


def cmd_funding(target: Optional[str]) -> None:
    coins = [target.upper()] if target else COINS
    results = []
    for c in coins:
        m = fetch_mock_meta(c)
        annualized = m["funding_rate_1h"] * 24 * 365 * 100
        m["funding_annualized_pct"] = round(annualized, 2)
        m["bias"] = classify_bias(m)
        m["signal"] = (
            "FUNDING_BURNT_LONGS" if m["funding_rate_1h"] > 0.002
            else "FUNDING_PAYING_LONGS" if m["funding_rate_1h"] < -0.001
            else "NEUTRAL"
        )
        results.append(m)
    print(json.dumps({"results": results, "count": len(results)}, indent=2))


def cmd_oi() -> None:
    rows = [fetch_mock_meta(c) for c in COINS]
    rows.sort(key=lambda r: abs(r["oi_change_24h_pct"]), reverse=True)
    crowded = [
        {
            "coin": r["coin"],
            "oi_change_24h_pct": r["oi_change_24h_pct"],
            "open_interest_usd": r["open_interest_usd"],
            "signal": (
                "OI_BULL_DIV" if r["oi_change_24h_pct"] > 5
                else "OI_BEAR_DIV" if r["oi_change_24h_pct"] < -5
                else "STABLE"
            ),
        }
        for r in rows
    ]
    print(json.dumps({"ranked": crowded, "count": len(crowded)}, indent=2))


def cmd_liqs() -> None:
    bucket = int(time.time() // 300)
    rng = random.Random(bucket)
    events = []
    for i in range(20):
        c = rng.choice(COINS)
        side = rng.choice(["long", "short"])
        size = rng.uniform(50_000, 5_000_000)
        events.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "coin": c,
            "side": side,
            "size_usd": round(size, 0),
            "price": round(rng.uniform(0.5, 65_000), 4),
        })
    events.sort(key=lambda e: e["size_usd"], reverse=True)
    long_liq = sum(e["size_usd"] for e in events if e["side"] == "long")
    short_liq = sum(e["size_usd"] for e in events if e["side"] == "short")
    ratio = long_liq / (short_liq + 1)
    cascade = "LONG_CASCADE" if ratio > 2 else "SHORT_CASCADE" if ratio < 0.5 else "BALANCED"
    print(json.dumps({
        "events": events[:10],
        "summary": {
            "long_liqs_usd": round(long_liq, 0),
            "short_liqs_usd": round(short_liq, 0),
            "liq_ratio_long_short": round(ratio, 2),
            "cascade_signal": cascade,
        },
    }, indent=2))


def cmd_basis(coin: str) -> None:
    hl = fetch_mock_meta(coin.upper())
    bn = fetch_mock_binance_funding(coin.upper())
    hl_8h = hl["funding_rate_1h"] * 8
    basis_bps = (hl_8h - bn["funding_rate_8h"]) * 10_000
    arb_open = abs(basis_bps) > 5
    print(json.dumps({
        "coin": coin.upper(),
        "hyperliquid_funding_8h_equiv": round(hl_8h, 6),
        "binance_funding_8h": bn["funding_rate_8h"],
        "basis_bps": round(basis_bps, 2),
        "arb_opportunity": arb_open,
        "side": "SHORT_HL_LONG_BINANCE" if basis_bps > 0 else "LONG_HL_SHORT_BINANCE" if basis_bps < 0 else "FAIR",
        "annualized_edge_pct": round(basis_bps * 365 / 100, 2),
    }, indent=2))


def cmd_squeeze(coin: str) -> None:
    m = fetch_mock_meta(coin.upper())
    print(json.dumps(squeeze_score(m), indent=2))


def main() -> int:
    p = argparse.ArgumentParser(description="Hyperliquid perp signals")
    sub = p.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("funding")
    p1.add_argument("coin", nargs="?")

    sub.add_parser("oi")
    sub.add_parser("liqs")

    p4 = sub.add_parser("basis")
    p4.add_argument("coin")

    p5 = sub.add_parser("squeeze")
    p5.add_argument("coin")

    args = p.parse_args()
    if args.cmd == "funding":
        cmd_funding(args.coin)
    elif args.cmd == "oi":
        cmd_oi()
    elif args.cmd == "liqs":
        cmd_liqs()
    elif args.cmd == "basis":
        cmd_basis(args.coin)
    elif args.cmd == "squeeze":
        cmd_squeeze(args.coin)
    return 0


if __name__ == "__main__":
    sys.exit(main())
