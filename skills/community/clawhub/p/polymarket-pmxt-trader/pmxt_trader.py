#!/usr/bin/env python3
"""
PMXT Cross-Exchange Polymarket Trader
Trades using PMXT API signals for cross-exchange price discovery.
Usage: python pmxt_trader.py [--live] [--positions] [--smart-sizing]
Requires: SIMMER_API_KEY + PMXT_API_KEY environment variables
"""
from __future__ import annotations
import sys, os, json, math, argparse, subprocess
from datetime import datetime, timezone

sys.stdout.reconfigure(line_buffering=True)

try:
    from simmer_sdk import SimmerClient
except ImportError:
    print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
    sys.exit(1)

# ─── Config ───────────────────────────────────────────────────────────────────
PMXT_API_KEY = os.environ.get("PMXT_API_KEY", "")
SIMMER_API_KEY = os.environ.get("SIMMER_API_KEY", "")
PMXT_BASE = "https://api.pmxt.dev/api"

ENTRY_THRESHOLD = float(os.environ.get("PMXT_ENTRY_THRESHOLD", "0.25"))
EXIT_THRESHOLD = float(os.environ.get("PMXT_EXIT_THRESHOLD", "0.45"))
MAX_POSITION_USD = float(os.environ.get("PMXT_MAX_POSITION_USD", "2.00"))
MIN_VOLUME = float(os.environ.get("PMXT_MIN_VOLUME", "10000"))
MAX_TRADES_PER_RUN = int(os.environ.get("PMXT_MAX_TRADES_PER_RUN", "5"))
SMART_SIZING_PCT = 0.05  # 5% Kelly fraction
ORDER_TYPE = os.environ.get("PMXT_ORDER_TYPE", "GTC").upper()

TRADE_SOURCE = "sdk:pmxt"
SKILL_SLUG = "polymarket-pmxt-trader"

# ─── PMXT API via curl ──────────────────────────────────────────────────────
def pmxt_request(method: str, exchange: str = "polymarket", params: dict = None) -> dict:
    if not PMXT_API_KEY:
        return {"error": "PMXT_API_KEY not set"}
    payload = json.dumps({"args": [params or {}]})
    env = os.environ.copy()
    r = subprocess.run(
        ["curl", "-s", "--max-time", "10",
         f"{PMXT_BASE}/{exchange}/{method}",
         "-X", "POST",
         "-H", f"Authorization: Bearer {PMXT_API_KEY}",
         "-H", "Content-Type: application/json",
         "-d", payload],
        capture_output=True, text=True, timeout=12, env=env)
    if r.returncode != 0:
        return {"error": r.stderr[:80]}
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"error": "parse failed"}

# ─── Simmer Client ──────────────────────────────────────────────────────────
_client = None

def get_client(live=True):
    global _client
    if _client is None:
        api_key = SIMMER_API_KEY or os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY not set")
            sys.exit(1)
        _client = SimmerClient.from_env(venue="polymarket", live=live)
    if live != _client.live:
        _client = SimmerClient.from_env(venue="polymarket", live=live)
    return _client

# ─── Market Discovery ──────────────────────────────────────────────────────
def fetch_pmxt_markets(limit=50):
    """Fetch active markets from PMXT."""
    result = pmxt_request("fetchMarkets", "polymarket", {"limit": limit})
    if result.get("error"):
        print(f"PMXT fetch error: {result['error']}")
        return []
    data = result.get("data", [])
    if isinstance(data, dict):
        data = data.get("data", [])
    return data

def filter_opportunities(markets):
    """Filter PMXT markets by entry threshold + volume."""
    opps = []
    for m in markets:
        volume = float(m.get("volume", 0))
        if volume < MIN_VOLUME:
            continue

        yes_price = 0.0
        yes_field = m.get("yes", {})
        if isinstance(yes_field, dict):
            yes_price = float(yes_field.get("price", 0))

        if not yes_price or yes_price > EXIT_THRESHOLD:
            continue

        title = m.get("title", "")
        slug = m.get("slug", "")
        market_url = m.get("url", "")
        market_id = m.get("marketId", m.get("id", ""))

        if yes_price <= ENTRY_THRESHOLD:
            signal = "STRONG_BUY"
        else:
            signal = "BARGAIN"

        opps.append({
            "title": title,
            "slug": slug,
            "market_url": market_url,
            "market_id": market_id,
            "yes_price": yes_price,
            "volume": volume,
            "signal": signal,
        })
    return opps

# ─── Trade Execution ─────────────────────────────────────────────────────────
def execute_trade(market_id, side, amount, reasoning, client):
    try:
        if client.live:
            pf = client.preflight(planned_amount=amount, exposure_cap_usd=0, venue=client.venue)
            if not pf.ok_to_trade:
                blockers = ", ".join(pf.blockers)
                print(f"  Preflight blocked: {blockers}")
                return {"error": f"preflight_blocked: {blockers}"}
        result = client.trade(
            market_id=market_id, side=side, amount=amount,
            source=TRADE_SOURCE, skill_slug=SKILL_SLUG,
            reasoning=reasoning, order_type=ORDER_TYPE)
        out = {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "error": result.error,
            "simulated": result.simulated,
        }
        return out
    except Exception as e:
        return {"error": str(e)}

def get_sizing(balance_usd):
    """Kelly-based sizing."""
    if not SMART_SIZING_PCT:
        return min(MAX_POSITION_USD, balance_usd * 0.05)
    return min(MAX_POSITION_USD, balance_usd * SMART_SIZING_PCT)

# ─── Positions ──────────────────────────────────────────────────────────────
def show_positions():
    client = get_client(live=False)
    portfolio = client.get_portfolio(venue="polymarket")
    positions = portfolio.get("positions", portfolio.get("polymarket", {}).get("positions", []))
    if not positions:
        print("No open positions")
        return
    print(f"\n📊 Open Positions ({len(positions)}):")
    for pos in positions:
        print(f"  {pos.get('question', pos.get('market_id', '?'))[:50]}")
        print(f"    Shares: {pos.get('shares', 0):.1f}  Avg: {pos.get('avg_price', 0)*100:.1f}¢  P&L: ${pos.get('pnl', 0):.2f}")

# ─── Main ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="PMXT Cross-Exchange Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show positions only")
    parser.add_argument("--smart-sizing", action="store_true", help="Use Kelly-based position sizing")
    parser.add_argument("--dry", action="store_true", help="Dry run (default)")
    args = parser.parse_args()

    live = args.live and not args.dry
    tag = "[LIVE]" if live else "[PAPER]"

    print(f"🔮 PMXT Cross-Exchange Trader {tag}")
    print("=" * 50)

    if args.positions:
        show_positions()
        return

    if not PMXT_API_KEY:
        print("⚠️ PMXT_API_KEY not set")
        return

    # Fetch PMXT markets
    print("\n🔍 Fetching PMXT markets...")
    markets = fetch_pmxt_markets(limit=50)
    print(f"   Fetched {len(markets)} markets from PMXT")

    if not markets:
        print("No markets fetched")
        return

    # Filter opportunities
    opps = filter_opportunities(markets)
    print(f"   {len(opps)} opportunities below {EXIT_THRESHOLD*100:.0f}¢ threshold")

    if not opps:
        print("No tradeable opportunities")
        return

    # Get balance
    client = get_client(live=live)
    try:
        briefing = client.get_briefing()
        balance = briefing.get("venues", {}).get("polymarket", {}).get("balance", 0)
        if not balance:
            balance = float(briefing.get("balance", 0))
    except Exception:
        balance = 10.0  # fallback

    print(f"   Balance: ${balance:.2f} pUSD")

    # Auto-redeem
    try:
        redeem = client.auto_redeem()
        for r in redeem:
            if r.get("success"):
                print(f"   ✅ Redeemed: {r.get('market_id', '')[:30]}")
    except Exception:
        pass

    # Execute trades
    trades_done = 0
    for opp in opps[:MAX_TRADES_PER_RUN]:
        if trades_done >= MAX_TRADES_PER_RUN:
            break

        price = opp["yes_price"]
        mid_pct = price * 100

        # Smart sizing
        if args.smart_sizing:
            position_size = get_sizing(balance)
        else:
            position_size = min(MAX_POSITION_USD, balance * 0.05)
        position_size = round(position_size, 2)  # max 2 decimal places

        if balance < 0.50:
            print(f"   Balance too low (${balance:.2f}), stopping")
            break

        reasoning = (f"PMXT signal: {opp['signal']} | "
                     f"YES {mid_pct:.1f}¢ | "
                     f"volume ${opp['volume']:,.0f} | "
                     f"{opp['title'][:60]}")

        print(f"\n  📌 {opp['title'][:60]}")
        print(f"     Price: {mid_pct:.1f}¢ | Signal: {opp['signal']} | Vol: ${opp['volume']:,.0f}")
        print(f"     Size: ${position_size:.2f} {tag}")

        # Import market if needed
        market_id = opp.get("market_id", "")
        market_url = opp.get("market_url", "")
        if not market_id or not market_url:
            print(f"     Missing market ID or URL")
            continue
        # Import via Polymarket URL to get Simmer market ID
        result_import = client.import_market(market_url)
        market_id = result_import.get("market_id", "")
        status = result_import.get("status", "")
        if status == "already_exists":
            print(f"     (already indexed)")
        elif market_id:
            print(f"     Imported: {market_id[:20]}...")
        else:
            print(f"     Import failed: {result_import.get('error', 'unknown')}")
            continue

        result = execute_trade(market_id, "yes", position_size, reasoning, client)

        if result.get("success"):
            shares = result.get("shares_bought", 0)
            print(f"     ✅ Bought {shares:.1f} YES shares @ {mid_pct:.1f}¢")
            balance -= position_size
        elif result.get("error"):
            err = result["error"]
            if "preflight" in err.lower():
                print(f"     ⛔ Preflight: {err}")
            else:
                print(f"     ❌ Error: {err}")

        trades_done += 1

    print(f"\n📊 Session summary: {trades_done} trades attempted")

if __name__ == "__main__":
    main()