#!/usr/bin/env python3
"""
nft-floor-sweep-calculator: pulls live NFT collection floor prices (Solana
via Magic Eden's public API, EVM via CoinGecko's free NFT API — both work
without an API key) and calculates the total cost, average price impact,
and marketplace fees for sweeping N items off the floor.

This does NOT execute trades or place orders. It is a pre-trade cost
estimator: "if I want to sweep N floor items on collection X right now,
roughly what will it cost me including fees and a naive slippage curve."
Real fills depend on live order-book depth, which this tool approximates
with a configurable slippage-per-item assumption since public free APIs
don't expose full order-book depth.

Usage:
    python3 floor_sweep.py floor degods                     # Magic Eden (Solana)
    python3 floor_sweep.py floor degods --sweep 5
    python3 floor_sweep.py evm-floor autoglyphs               # CoinGecko (EVM)
    python3 floor_sweep.py evm-floor autoglyphs --sweep 3 --json
"""
import argparse
import json
import sys
import urllib.request
import urllib.error

TIMEOUT = 8

MAGICEDEN_FEE_PCT = 2.0  # Magic Eden marketplace fee (approx, excludes royalties)
COINGECKO_FEE_PCT = 2.5  # rough default assumption for EVM marketplaces (e.g. OpenSea/Blur blended)
DEFAULT_SLIPPAGE_PER_ITEM_PCT = 3.0  # naive: each successive item assumed this much pricier than the last


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "nft-floor-sweep-calculator/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode())


def sweep_cost(floor_price, count, slippage_pct, fee_pct):
    items = []
    running_total = 0.0
    for i in range(count):
        price = floor_price * (1 + slippage_pct / 100 * i)
        items.append(round(price, 6))
        running_total += price
    fee = running_total * fee_pct / 100
    return {
        "floor_price": floor_price,
        "count": count,
        "item_prices": items,
        "subtotal": round(running_total, 6),
        "fee_pct": fee_pct,
        "fee_amount": round(fee, 6),
        "total_cost": round(running_total + fee, 6),
        "avg_price_per_item": round((running_total + fee) / count, 6) if count else 0,
    }


def magiceden_floor(slug):
    stats = http_get(f"https://api-mainnet.magiceden.dev/v2/collections/{slug}/stats")
    if "floorPrice" not in stats:
        raise RuntimeError(f"collection '{slug}' not found on Magic Eden or missing floorPrice")
    floor_sol = stats["floorPrice"] / 1e9  # lamports -> SOL
    return {
        "marketplace": "magiceden",
        "slug": slug,
        "currency": "SOL",
        "floor_price": floor_sol,
        "listed_count": stats.get("listedCount"),
        "volume_7d_sol": stats.get("volume7d", 0) / 1e9 if stats.get("volume7d") else None,
    }


def coingecko_floor(nft_id):
    data = http_get(f"https://api.coingecko.com/api/v3/nfts/{nft_id}")
    fp = data.get("floor_price", {})
    native = fp.get("native_currency")
    symbol = data.get("native_currency_symbol", "ETH")
    if native is None:
        raise RuntimeError(f"no floor_price data for nft id '{nft_id}' on CoinGecko")
    return {
        "marketplace": "coingecko-aggregate",
        "slug": nft_id,
        "currency": symbol,
        "floor_price": native,
        "name": data.get("name"),
        "market_cap_native": data.get("market_cap", {}).get("native_currency"),
    }


def print_report(meta, cost):
    print(f"Collection : {meta.get('name', meta['slug'])} ({meta['marketplace']})")
    print(f"Floor price: {meta['floor_price']:.6f} {meta['currency']}")
    if meta.get("listed_count") is not None:
        print(f"Listed     : {meta['listed_count']}")
    print()
    print(f"Sweeping {cost['count']} items, assuming {DEFAULT_SLIPPAGE_PER_ITEM_PCT}% price step per item up the book:")
    for i, p in enumerate(cost["item_prices"], 1):
        print(f"  #{i}: {p:.6f} {meta['currency']}")
    print()
    print(f"Subtotal        : {cost['subtotal']:.6f} {meta['currency']}")
    print(f"Marketplace fee : {cost['fee_pct']}% = {cost['fee_amount']:.6f} {meta['currency']}")
    print(f"TOTAL COST      : {cost['total_cost']:.6f} {meta['currency']}")
    print(f"Avg per item    : {cost['avg_price_per_item']:.6f} {meta['currency']}")
    print()
    print("Estimate only — real fills depend on live order-book depth and royalties,")
    print("which free public APIs don't expose. Verify against the live book before buying.")


def main():
    parser = argparse.ArgumentParser(description="NFT floor sweep cost calculator")
    sub = parser.add_subparsers(dest="command", required=True)

    me_p = sub.add_parser("floor", help="Solana collection via Magic Eden")
    me_p.add_argument("slug", help="Magic Eden collection symbol, e.g. degods")
    me_p.add_argument("--sweep", type=int, default=1)
    me_p.add_argument("--slippage", type=float, default=DEFAULT_SLIPPAGE_PER_ITEM_PCT)
    me_p.add_argument("--fee", type=float, default=MAGICEDEN_FEE_PCT)
    me_p.add_argument("--json", action="store_true")

    cg_p = sub.add_parser("evm-floor", help="EVM collection via CoinGecko NFT API")
    cg_p.add_argument("nft_id", help="CoinGecko NFT id, e.g. autoglyphs (see /nfts/list)")
    cg_p.add_argument("--sweep", type=int, default=1)
    cg_p.add_argument("--slippage", type=float, default=DEFAULT_SLIPPAGE_PER_ITEM_PCT)
    cg_p.add_argument("--fee", type=float, default=COINGECKO_FEE_PCT)
    cg_p.add_argument("--json", action="store_true")

    args = parser.parse_args()

    try:
        if args.command == "floor":
            meta = magiceden_floor(args.slug)
        else:
            meta = coingecko_floor(args.nft_id)
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError, TimeoutError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    cost = sweep_cost(meta["floor_price"], args.sweep, args.slippage, args.fee)

    if args.json:
        print(json.dumps({**meta, **cost}, indent=2))
    else:
        print_report(meta, cost)


if __name__ == "__main__":
    main()
