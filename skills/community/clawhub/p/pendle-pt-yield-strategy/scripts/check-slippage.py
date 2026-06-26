#!/usr/bin/env python3
"""
check-slippage.py — Preview USDC→PT swap slippage for a candidate market.

Usage:
  python3 check-slippage.py \
    --chain-id 1 \
    --market 0x3c53fae231ad3c0408a8b6d33138bbff1caec330 \
    --pt 0x... \
    --amount 10000 \
    --max-slippage 2.0 \
    --wallet 0xYOUR_WALLET

Calls the Pendle Convert API in preview mode (no tx sent) and reports:
  - Amount of PT received
  - Effective APY
  - Price impact (slippage)
  - Pass/fail against max_slippage threshold
"""

import argparse, json, sys, urllib.request, urllib.parse

API_BASE = "https://api-v2.pendle.finance/core"

USDC_ADDRESSES = {
    1:     "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    42161: "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    8453:  "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
}

USDC_DECIMALS = 6


def fetch_json(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def preview_swap(chain_id, pt_address, amount_usd, wallet, slippage=0.01):
    usdc = USDC_ADDRESSES.get(chain_id)
    if not usdc:
        raise ValueError(f"No USDC address for chain {chain_id}")

    amount_raw = int(amount_usd * (10 ** USDC_DECIMALS))

    params = {
        "tokensIn": usdc,
        "amountsIn": str(amount_raw),
        "tokensOut": pt_address,
        "receiver": wallet,
        "slippage": str(slippage),
        "enableAggregator": "true",
        "aggregators": "kyberswap",
        "additionalData": "impliedApy,effectiveApy",
    }
    qs = urllib.parse.urlencode(params)
    url = f"{API_BASE}/v2/sdk/{chain_id}/convert?{qs}"
    return fetch_json(url)


def main():
    p = argparse.ArgumentParser(description="Preview USDC→PT slippage")
    p.add_argument("--chain-id", type=int, default=1)
    p.add_argument("--market", required=True, help="Market address")
    p.add_argument("--pt", required=True, help="PT token address")
    p.add_argument("--amount", type=float, default=10000, help="USDC amount")
    p.add_argument("--max-slippage", type=float, default=2.0, help="Max slippage %%")
    p.add_argument("--wallet", required=True, help="Wallet address for quote receiver")
    args = p.parse_args()

    print(f"Previewing swap: {args.amount} USDC → PT on chain {args.chain_id}")
    print(f"  Market: {args.market}")
    print(f"  PT:     {args.pt}")
    print()

    try:
        result = preview_swap(args.chain_id, args.pt, args.amount, args.wallet)
    except Exception as e:
        print(f"ERROR: API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    routes = result.get("routes", [])
    best_route = None
    if routes:
        best_route = max(routes, key=lambda r: int(((r.get("outputs") or [{}])[0]).get("amount", "0")))
    data = (best_route or {}).get("data", result.get("data", result))
    price_impact = float(data.get("priceImpact", 0) or 0)
    price_impact_pct = abs(price_impact * 100)

    outputs = (best_route or {}).get("outputs", [])
    amount_out = outputs[0].get("amount", "unknown") if outputs else data.get("amountOut", "unknown")
    implied_apy = data.get("impliedApy", "unknown")
    effective_apy = data.get("effectiveApy", "unknown")
    if isinstance(implied_apy, dict):
        implied_apy = implied_apy.get("after", implied_apy.get("before", implied_apy))

    implied_apy_display = f"{float(implied_apy)*100:.2f}%" if isinstance(implied_apy, (int, float)) else implied_apy
    effective_apy_display = f"{float(effective_apy)*100:.2f}%" if isinstance(effective_apy, (int, float)) else effective_apy

    print(f"  PT received:     {amount_out}")
    print(f"  Implied APY:     {implied_apy_display}")
    print(f"  Effective APY:   {effective_apy_display}")
    print(f"  Price impact:    {price_impact_pct:.3f}%")
    print()

    if price_impact_pct > args.max_slippage:
        print(f"  ❌ FAIL — slippage {price_impact_pct:.2f}% exceeds max {args.max_slippage}%")
        sys.exit(2)
    else:
        print(f"  ✅ PASS — slippage {price_impact_pct:.2f}% within {args.max_slippage}% limit")

    summary = {
        "market": args.market,
        "pt": args.pt,
        "chain_id": args.chain_id,
        "deposit_usd": args.amount,
        "amount_pt_out": amount_out,
        "implied_apy": implied_apy,
        "effective_apy": effective_apy,
        "price_impact_pct": price_impact_pct,
        "slippage_ok": price_impact_pct <= args.max_slippage,
    }
    print()
    print("--- JSON ---")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
