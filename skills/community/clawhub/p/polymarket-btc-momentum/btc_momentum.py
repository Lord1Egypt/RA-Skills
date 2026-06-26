"""
BTC Momentum Trader — polymarket-btc-momentum
Trades Polymarket 5-min Bitcoin sprint markets using Binance momentum signals.
"""

import os
import sys
import argparse
import requests
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
TRADE_AMOUNT = 10.0       # USD per trade
MIN_EDGE = 0.05           # Minimum edge (probability gap) to trade
SKILL_SLUG = "polymarket-btc-momentum"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
DRY_RUN = True            # Always default to dry run; pass --live to override

# ── Simmer client ─────────────────────────────────────────────────────────────
_client = None

def get_client(venue="polymarket"):
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("ERROR: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
    return _client


# ── BTC signal ────────────────────────────────────────────────────────────────

def get_binance_klines(symbol="BTCUSDT", interval="1m", limit=15):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def ema(values, period):
    """Simple EMA calculation."""
    k = 2 / (period + 1)
    result = [values[0]]
    for v in values[1:]:
        result.append(v * k + result[-1] * (1 - k))
    return result


def compute_signal(klines):
    """
    Returns (side, confidence, reasoning) based on EMA momentum.
    side: 'yes' (price going up) or 'no' (price going down)
    confidence: float 0-1 (our estimated probability that side wins)
    """
    closes = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]

    ema_fast = ema(closes, 3)   # fast EMA
    ema_slow = ema(closes, 8)   # slow EMA

    last_fast = ema_fast[-1]
    last_slow = ema_slow[-1]
    prev_fast = ema_fast[-2]
    prev_slow = ema_slow[-2]

    current_price = closes[-1]
    prev_price = closes[-2]
    price_change_pct = (current_price - prev_price) / prev_price * 100

    avg_volume = sum(volumes[:-1]) / len(volumes[:-1])
    last_volume = volumes[-1]
    volume_ratio = last_volume / avg_volume if avg_volume > 0 else 1.0

    # EMA crossover signal
    bullish = last_fast > last_slow and prev_fast <= prev_slow
    bearish = last_fast < last_slow and prev_fast >= prev_slow
    bullish_trend = last_fast > last_slow
    bearish_trend = last_fast < last_slow

    # Volume confirmation
    volume_confirmed = volume_ratio > 1.2

    # Build confidence based on signal strength
    base_conf = 0.55  # slight edge baseline

    if bullish and volume_confirmed:
        confidence = base_conf + 0.12
        side = "yes"
        reason = f"Bullish EMA crossover (fast={last_fast:.0f} > slow={last_slow:.0f}) with {volume_ratio:.1f}x volume. BTC +{price_change_pct:.2f}%."
    elif bearish and volume_confirmed:
        confidence = base_conf + 0.12
        side = "no"
        reason = f"Bearish EMA crossover (fast={last_fast:.0f} < slow={last_slow:.0f}) with {volume_ratio:.1f}x volume. BTC {price_change_pct:.2f}%."
    elif bullish_trend and price_change_pct > 0.1:
        confidence = base_conf + 0.06
        side = "yes"
        reason = f"Bullish trend continuation. EMA spread {last_fast - last_slow:.0f}. BTC +{price_change_pct:.2f}%."
    elif bearish_trend and price_change_pct < -0.1:
        confidence = base_conf + 0.06
        side = "no"
        reason = f"Bearish trend continuation. EMA spread {last_slow - last_fast:.0f}. BTC {price_change_pct:.2f}%."
    else:
        return None, 0.5, "No clear signal — momentum is neutral."

    return side, confidence, reason


# ── Market discovery ──────────────────────────────────────────────────────────

def find_target_market():
    """Find the next active BTC sprint market."""
    client = get_client()
    markets = client.get_markets(q="Bitcoin Up or Down", status="active", limit=20)
    
    now = datetime.now(timezone.utc)
    candidates = []

    for m in markets:
        # Filter to 5-min sprint markets that haven't resolved
        if "Bitcoin Up or Down" not in (m.question or ""):
            continue
        prob = getattr(m, "current_probability", None)
        if prob is None:
            continue
        # Look for markets close to 50/50 (most liquid, best edge opportunity)
        candidates.append(m)

    if not candidates:
        return None

    # Sort by probability closest to 0.50 (most uncertain = most tradeable)
    candidates.sort(key=lambda m: abs(getattr(m, "current_probability", 0.5) - 0.5))
    return candidates[0]


# ── Main trading loop ─────────────────────────────────────────────────────────

def run(live=False):
    dry = not live
    print(f"{'🧪 DRY RUN' if dry else '💰 LIVE TRADE'} | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)

    # 1. Get BTC signal
    print("📡 Fetching BTC momentum from Binance...")
    try:
        klines = get_binance_klines()
    except Exception as e:
        print(f"❌ Binance fetch failed: {e}")
        return

    side, confidence, reasoning = compute_signal(klines)
    current_price = float(klines[-1][4])
    print(f"   BTC price: ${current_price:,.2f}")
    print(f"   Signal: {side} | Confidence: {confidence:.1%}")
    print(f"   Reasoning: {reasoning}")

    if side is None:
        print("⏭  No trade — neutral momentum.")
        return

    # 2. Find market
    print("\n🔍 Finding target market...")
    try:
        market = find_target_market()
    except Exception as e:
        print(f"❌ Market discovery failed: {e}")
        return

    if not market:
        print("⏭  No active BTC sprint markets found.")
        return

    market_prob = getattr(market, "current_probability", 0.5)
    print(f"   Market: {market.question}")
    print(f"   Market prob (YES): {market_prob:.1%}")

    # 3. Calculate edge
    if side == "yes":
        market_side_prob = market_prob
    else:
        market_side_prob = 1 - market_prob

    edge = confidence - market_side_prob
    print(f"   Our edge: {edge:.1%} (need >{MIN_EDGE:.0%})")

    if edge < MIN_EDGE:
        print(f"⏭  Edge too small ({edge:.1%} < {MIN_EDGE:.0%}). Skipping.")
        return

    # 4. Check context
    print("\n🔎 Checking market context...")
    try:
        ctx = get_client().get_market_context(market.id, my_probability=confidence)
        warnings = ctx.get("warnings", [])
        trading = ctx.get("trading", {})
        flip_flop = trading.get("flip_flop_warning", "")
        slippage = ctx.get("slippage", {}).get("slippage_pct", 0)

        if flip_flop and "SEVERE" in flip_flop:
            print(f"⛔ Flip-flop warning: {flip_flop}. Aborting.")
            return
        if slippage > 0.15:
            print(f"⛔ Slippage too high ({slippage:.1%}). Aborting.")
            return
        if warnings:
            print(f"   ⚠️  Warnings: {warnings}")
        else:
            print("   ✅ No blocking warnings.")
    except Exception as e:
        print(f"   ⚠️  Context check failed: {e} — proceeding anyway.")

    # 5. Execute trade
    full_reasoning = f"{reasoning} Edge: {edge:.1%} vs market {market_side_prob:.1%}."
    print(f"\n{'🧪 Would trade' if dry else '⚡ Trading'}: {side.upper()} ${TRADE_AMOUNT} on {market.question[:60]}")
    print(f"   Reasoning: {full_reasoning}")

    if dry:
        print("\n✅ Dry run complete. Pass --live to execute real trades.")
        return

    try:
        result = get_client().trade(
            market.id,
            side,
            TRADE_AMOUNT,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=full_reasoning,
        )
        shares = getattr(result, "shares_bought", "?")
        print(f"\n✅ Trade executed! Bought {shares} shares.")
    except Exception as e:
        print(f"❌ Trade failed: {e}")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BTC Momentum Trader for Polymarket")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: dry run)")
    args = parser.parse_args()

    if "SIMMER_API_KEY" not in os.environ:
        print("ERROR: SIMMER_API_KEY environment variable not set.")
        sys.exit(1)

    run(live=args.live)
