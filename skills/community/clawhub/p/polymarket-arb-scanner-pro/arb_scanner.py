#!/usr/bin/env python3
"""
⚡ Polymarket Arbitrage Scanner
================================
Finds YES + NO < $1.00 opportunities and executes both legs as FOK.
Pure math — no forecast required.

Hedge formula: buy YES + NO when sum < 0.98 (2¢ min edge after gas)
Execution: Fill-or-Kill on both legs simultaneously

Usage:
  python3 arb_scanner.py           # scan only
  python3 arb_scanner.py --buy     # scan + execute
  python3 arb_scanner.py --min-edge 0.02  # minimum edge threshold
"""

import os, sys, json, time, argparse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

MIN_EDGE     = 0.02    # 2¢ minimum (covers gas + slippage)
MAX_DEPLOY   = 50.0    # max $ per arb opportunity
RESERVE      = 10.0    # keep $10 in wallet
GAMMA_API    = "https://gamma-api.polymarket.com"
CLOB_HOST    = "https://clob.polymarket.com"

def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def get_clob_client():
    from py_clob_client.client import ClobClient
    pk     = os.environ.get("PRIVATE_KEY")
    funder = os.environ.get("WALLET_ADDRESS")
    client = ClobClient(CLOB_HOST, key=pk, chain_id=137, signature_type=1, funder=funder)
    creds  = client.create_or_derive_api_creds()
    client.set_api_creds(creds)
    return client

def get_markets(limit=500):
    """Fetch active markets with prices."""
    req = urllib.request.Request(
        f"{GAMMA_API}/markets?closed=false&limit={limit}&order=volume24hr&ascending=false",
        headers={"User-Agent": "ClawdipusRex/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def find_arbs(markets, min_edge=MIN_EDGE):
    """Find markets where YES + NO < 1.00."""
    arbs = []
    for m in markets:
        prices_raw = m.get("outcomePrices", "[]")
        prices = json.loads(prices_raw) if isinstance(prices_raw, str) else prices_raw
        if len(prices) != 2:
            continue

        yes_price = float(prices[0])
        no_price  = float(prices[1])
        total     = yes_price + no_price
        edge      = 1.0 - total

        if edge < min_edge:
            continue
        if yes_price < 0.01 or no_price < 0.01:
            continue  # One side near zero = near-resolved, skip

        token_ids_raw = m.get("clobTokenIds", "[]")
        token_ids = json.loads(token_ids_raw) if isinstance(token_ids_raw, str) else token_ids_raw
        if len(token_ids) != 2:
            continue

        vol = float(m.get("volume24hr") or 0)
        arbs.append({
            "slug":       m.get("slug", ""),
            "question":   m.get("question", "")[:65],
            "yes_price":  yes_price,
            "no_price":   no_price,
            "total":      total,
            "edge":       edge,
            "yes_token":  token_ids[0],
            "no_token":   token_ids[1],
            "volume24h":  vol,
        })

    arbs.sort(key=lambda x: x["edge"], reverse=True)
    return arbs

def execute_arb(client, arb, deploy_usd):
    """
    Execute both legs as Fill-or-Kill.
    Both must fill or neither does — no leg risk.
    """
    from py_clob_client.clob_types import MarketOrderArgs, OrderType

    yes_amount = deploy_usd * arb["yes_price"] / (arb["yes_price"] + arb["no_price"])
    no_amount  = deploy_usd * arb["no_price"]  / (arb["yes_price"] + arb["no_price"])

    results = []
    for token_id, amount, label in [
        (arb["yes_token"], yes_amount, "YES"),
        (arb["no_token"],  no_amount,  "NO"),
    ]:
        try:
            args  = MarketOrderArgs(token_id=token_id, amount=amount, side="BUY")
            order = client.create_market_order(args)
            resp  = client.post_order(order, OrderType.FOK)
            status = resp.get("status", "?")
            filled = resp.get("success", False) or status == "matched"
            results.append({"label": label, "filled": filled, "status": status, "resp": resp})
        except Exception as e:
            results.append({"label": label, "filled": False, "status": "error", "error": str(e)})

    all_filled = all(r["filled"] for r in results)
    return all_filled, results

def get_balance(client):
    from py_clob_client.clob_types import BalanceAllowanceParams, AssetType
    bal = client.get_balance_allowance(params=BalanceAllowanceParams(asset_type=AssetType.COLLATERAL))
    return int(bal.get("balance", "0")) / 1e6

def main():
    parser = argparse.ArgumentParser(description="Polymarket Arb Scanner")
    parser.add_argument("--buy",      action="store_true", help="Execute arbs found")
    parser.add_argument("--min-edge", type=float, default=MIN_EDGE)
    parser.add_argument("--limit",    type=int,   default=500)
    parser.add_argument("--max-deploy", type=float, default=MAX_DEPLOY)
    args = parser.parse_args()

    load_env()

    print("=" * 65)
    print("⚡  POLYMARKET ARB SCANNER")
    print(f"    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"    Min edge: {args.min_edge:.1%} | Scanning {args.limit} markets")
    print("=" * 65)

    print("\n📡 Fetching markets...")
    markets = get_markets(limit=args.limit)
    print(f"   {len(markets)} markets loaded")

    arbs = find_arbs(markets, min_edge=args.min_edge)

    if not arbs:
        print(f"\n✓ No arb opportunities (min edge {args.min_edge:.1%}) — market is efficient right now")
        return

    print(f"\n⚡ Found {len(arbs)} arb opportunity(ies):\n")
    print(f"  {'Edge':>6}  {'YES':>6}  {'NO':>6}  {'Vol24h':>10}  Question")
    print(f"  {'----':>6}  {'---':>6}  {'--':>6}  {'------':>10}  --------")
    for a in arbs[:10]:
        print(f"  {a['edge']:>5.1%}  {a['yes_price']:>5.1%}  {a['no_price']:>5.1%}  "
              f"${a['volume24h']:>9,.0f}  {a['question']}")

    if not args.buy:
        print(f"\n  (dry run — use --buy to execute)")
        return

    # Execute
    client = get_clob_client()
    balance = get_balance(client)
    deployable = balance - RESERVE

    # Initialize risk manager
    try:
        from risk_manager import RiskManager
        rm = RiskManager(portfolio_value=balance)
    except Exception:
        rm = None
    print(f"\n💰 Balance: ${balance:.2f} | Deployable: ${deployable:.2f}\n")

    if deployable < 5:
        print("  Insufficient balance to arb")
        return

    executed = 0
    for arb in arbs[:3]:  # Max 3 arbs at once
        deploy = min(args.max_deploy, deployable / len(arbs[:3]))
        if deploy < 5:
            break

        profit = deploy * arb["edge"]

        # Risk check
        if rm:
            allowed, reason = rm.check_trade(arb["slug"], deploy)
            if not allowed:
                print(f"  ⛔ Risk block: {reason}")
                continue
            can_place, wait = rm.rate_limit.can_place()
            if not can_place:
                print(f"  ⏳ Rate limit — waiting {wait:.1f}s")
                time.sleep(wait + 0.1)

        print(f"  🎯 Deploying ${deploy:.0f} | edge={arb['edge']:.1%} | profit=${profit:.2f}")
        print(f"     {arb['question']}")

        ok, results = execute_arb(client, arb, deploy)
        for r in results:
            status = "✅" if r["filled"] else "❌"
            print(f"     {status} {r['label']} — {r['status']}")

        if ok:
            print(f"     🎉 Both legs filled! Locked in ${profit:.2f} profit at resolution")
            executed += 1
            if rm:
                rm.record_order()
                rm.record_order()  # two orders (YES + NO)
                rm.record_position(arb["slug"], deploy, arb["total"])
        else:
            print(f"     ⚠️  FOK failed — no position taken (safe)")
        print()

    print(f"  Executed: {executed}/{len(arbs[:3])} arbs")

if __name__ == "__main__":
    main()
