#!/usr/bin/env python3
"""
Options Flow Intelligence Script
Fetches real-time option flow data from OptionWhales API including:
- Current institutional option flow
- Per-ticker flow details with momentum and abnormal trade signals
- Momentum rankings across the market
- Historical flow for trend analysis
"""

import json
import sys
import os
from datetime import datetime

API_KEY = os.environ.get("OPTIONWHALES_API_KEY", "")
BASE_URL = "https://api.optionwhales.com/v1"


def fetch_json(endpoint: str) -> dict:
    """Make authenticated API request to OptionWhales."""
    if not API_KEY:
        print("ERROR: OPTIONWHALES_API_KEY environment variable not set")
        print("Get your API key at: https://optionwhales.com/api")
        sys.exit(1)

    import urllib.request
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={"X-API-Key": API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"ERROR: Failed to fetch {endpoint}: {e}")
        sys.exit(1)


def get_current_flow(limit: int = 20) -> None:
    """Fetch current institutional option flow across all tickers."""
    print(f"\n=== CURRENT OPTION FLOW (Top {limit}) ===")
    print(f"Fetched: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    data = fetch_json(f"/flow/current?limit={limit}")
    for item in data.get("flow", [])[:limit]:
        ticker = item.get("ticker", "N/A")
        direction = item.get("direction", "N/A")
        volume = item.get("volume", 0)
        premium = item.get("premium", 0)
        signal = item.get("intent_momentum", "N/A")
        print(f"  [{signal}] {ticker} | {direction} | Vol: {volume:,} | Premium: ${premium:,.0f}")
    print()


def get_ticker_flow(ticker: str) -> None:
    """Get detailed option flow for a specific ticker."""
    print(f"\n=== OPTION FLOW: {ticker.upper()} ===\n")
    data = fetch_json(f"/flow/current/{ticker.upper()}")

    if not data.get("flow"):
        print(f"No active flow data for {ticker.upper()}")
        return

    item = data["flow"][0]
    print(f"Ticker:       {item.get('ticker')}")
    print(f"Direction:    {item.get('direction')}")
    print(f"Volume:       {item.get('volume', 0):,}")
    print(f"Premium:      ${item.get('premium', 0):,.0f}")
    print(f"Signal:       {item.get('intent_momentum', 'N/A')}")
    print(f"Momentum:     {item.get('momentum_rank', 'N/A')}")
    if item.get("abnormal_trade"):
        print(f"ABNORMAL:     Yes")
    print()


def get_momentum_rankings(limit: int = 20) -> None:
    """Get top momentum rankings - stocks with strongest option activity."""
    print(f"\n=== TOP {limit} MOMENTUM STOCKS ===\n")
    data = fetch_json(f"/momentum/rankings?limit={limit}")
    for rank, item in enumerate(data.get("rankings", [])[:limit], 1):
        ticker = item.get("ticker", "?")
        score = item.get("momentum_score", 0)
        bias = item.get("direction_bias", "N/A")
        vol = item.get("volume_change_pct", 0)
        print(f"  {rank:2d}. {ticker:6s} | Score: {score:.1f} | Bias: {bias:6s} | Vol Chg: {vol:+.0f}%")
    print()


def get_abnormal_trades(limit: int = 15) -> None:
    """Get abnormal options trades - potential insider activity."""
    print(f"\n=== ABNORMAL OPTIONS TRADES (Last {limit}) ===\n")
    data = fetch_json(f"/abnormal-trades/current?limit={limit}")
    for trade in data.get("trades", [])[:limit]:
        ticker = trade.get("ticker", "?")
        vol = trade.get("volume", 0)
        premium = trade.get("premium", 0)
        unusual = trade.get("unusual_size", False)
        flag = "⚠️ UNUSUAL" if unusual else ""
        print(f"  {ticker:6s} | Vol: {vol:,} | Premium: ${premium:,.0f} {flag}")
    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python optionflow.py <command> [args]")
        print("Commands:")
        print("  flow              - Show current market-wide option flow")
        print("  momentum          - Show top momentum stocks")
        print("  abnormal          - Show abnormal option trades")
        print("  ticker <SYMBOL>   - Get flow for specific ticker (e.g., AAPL)")
        print("\nEnvironment: OPTIONWHALES_API_KEY required")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "flow":
        get_current_flow(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
    elif cmd == "momentum":
        get_momentum_rankings(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
    elif cmd == "abnormal":
        get_abnormal_trades(int(sys.argv[2]) if len(sys.argv) > 2 else 15)
    elif cmd == "ticker" and len(sys.argv) > 2:
        get_ticker_flow(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()