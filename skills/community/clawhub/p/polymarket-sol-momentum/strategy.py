"""
polymarket-sol-momentum
-----------------------
Scans Polymarket for Solana/crypto prediction markets where the current
market price diverges significantly from CoinGecko-derived momentum signals.

Strategy logic:
  1. Fetch top crypto/Solana markets from Polymarket via Simmer
  2. Pull 24h price change + 7d trend from CoinGecko (free, no key needed)
  3. Compute a directional signal: strong up momentum → bullish markets
     should be priced higher; strong down → bearish markets higher
  4. Buy YES when market is underpriced vs signal, NO when overpriced
  5. Skip if context warns of flip-flop, high slippage, or low edge

Remix ideas:
  - Swap CoinGecko for your own price feed or CEX API
  - Add funding rate data from Binance/Bybit as a secondary signal
  - Tune DIVERGENCE_THRESHOLD and TRADE_AMOUNT to your risk tolerance
  - Point at Kalshi crypto markets instead (set venue="kalshi")

Usage:
  Dry run (default):  python strategy.py
  Live trading:       python strategy.py --live
"""

import os
import sys
import argparse
import requests
import time
import json
from datetime import datetime, timezone

# ── Config ──────────────────────────────────────────────────────────────────
SKILL_SLUG = "polymarket-sol-momentum"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
TRADE_AMOUNT = float(os.environ.get("TRADE_AMOUNT_USD", "10.0"))
DIVERGENCE_THRESHOLD = float(os.environ.get("DIVERGENCE_THRESHOLD", "0.08"))  # 8%
MAX_TRADES_PER_RUN = int(os.environ.get("MAX_TRADES_PER_RUN", "3"))
VENUE = os.environ.get("TRADING_VENUE", "sim")  # sim | polymarket | kalshi

# Keywords to match crypto/SOL prediction markets
KEYWORDS = ["solana", "sol", "bitcoin", "btc", "ethereum", "eth", "crypto"]

# CoinGecko IDs mapped to keywords for signal lookup
COINGECKO_IDS = {
    "solana": "solana",
    "sol": "solana",
    "bitcoin": "bitcoin",
    "btc": "bitcoin",
    "ethereum": "ethereum",
    "eth": "ethereum",
    "crypto": "bitcoin",  # fallback: use BTC as market proxy
}

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

# ── Helpers ──────────────────────────────────────────────────────────────────

def log(msg):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def get_client(live: bool):
    from simmer_sdk import SimmerClient
    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        raise RuntimeError("SIMMER_API_KEY environment variable not set.")
    venue = VENUE if live else "sim"
    return SimmerClient(api_key=api_key, venue=venue)


def fetch_coingecko_signals() -> dict:
    """
    Returns {coin_id: {"price_change_24h": float, "price_change_7d": float}}
    Falls back to empty dict on error (skip trading that run).
    """
    ids = list(set(COINGECKO_IDS.values()))
    params = {
        "ids": ",".join(ids),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_7d_change": "true",
    }
    try:
        r = requests.get(COINGECKO_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        signals = {}
        for coin_id in ids:
            if coin_id in data:
                signals[coin_id] = {
                    "price_change_24h": data[coin_id].get("usd_24h_change", 0.0),
                    "price_change_7d": data[coin_id].get("usd_7d_change", 0.0),
                }
        log(f"CoinGecko signals: {json.dumps(signals, indent=2)}")
        return signals
    except Exception as e:
        log(f"⚠️  CoinGecko fetch failed: {e} — skipping this run")
        return {}


def momentum_signal(signals: dict, coin_id: str) -> float:
    """
    Returns a directional signal in [-1, +1]:
      +1  = strong bullish momentum (markets predicting price rise should be priced higher)
      -1  = strong bearish momentum
       0  = neutral / no data
    Weighted: 60% 24h change, 40% 7d change (normalized to ±1 at ±20%).
    """
    s = signals.get(coin_id)
    if not s:
        return 0.0
    c24 = max(-1.0, min(1.0, s["price_change_24h"] / 20.0))
    c7d = max(-1.0, min(1.0, s["price_change_7d"] / 20.0))
    return round(0.6 * c24 + 0.4 * c7d, 4)


def detect_coin(question: str) -> str | None:
    """Return the best CoinGecko ID for a market question, or None."""
    q = question.lower()
    for kw, coin_id in COINGECKO_IDS.items():
        if kw in q:
            return coin_id
    return None


def question_is_bullish(question: str) -> bool | None:
    """
    Heuristic: does this question predict price going UP (True), DOWN (False),
    or unclear (None)?
    """
    q = question.lower()
    bullish_hints = ["above", "over", "reach", "hit", "exceed", "higher", "bull", "up", "gain"]
    bearish_hints = ["below", "under", "drop", "fall", "lose", "lower", "bear", "down", "crash"]
    b_score = sum(1 for h in bullish_hints if h in q)
    s_score = sum(1 for h in bearish_hints if h in q)
    if b_score > s_score:
        return True
    if s_score > b_score:
        return False
    return None  # ambiguous, skip


def compute_edge(market_prob: float, signal: float, bullish: bool) -> tuple[str, float]:
    """
    Returns (side, edge) where edge is how mispriced the market is.
    side: 'yes' | 'no'
    edge: 0..1 (fraction of mispricing)
    """
    # Expected prob if signal is correct:
    # strong bullish signal + bullish question → prob should be HIGH
    # strong bullish signal + bearish question → prob should be LOW
    if bullish:
        expected = 0.5 + 0.5 * signal   # signal=+1 → expected=1.0, signal=-1 → expected=0.0
    else:
        expected = 0.5 - 0.5 * signal   # signal=+1 (bullish) → bearish market LESS likely → expected=0.0

    expected = max(0.05, min(0.95, expected))
    divergence = expected - market_prob

    if divergence > 0:
        return "yes", abs(divergence)
    else:
        return "no", abs(divergence)


# ── Main ─────────────────────────────────────────────────────────────────────

def run(live: bool):
    log(f"{'🔴 LIVE' if live else '🟡 DRY RUN'} | venue={VENUE if live else 'sim'} | "
        f"threshold={DIVERGENCE_THRESHOLD:.0%} | max_trades={MAX_TRADES_PER_RUN}")

    # 1. Get price signals
    signals = fetch_coingecko_signals()
    if not signals:
        log("No signals available — exiting")
        return

    # 2. Connect to Simmer
    client = get_client(live)

    # 3. Fetch active crypto markets
    all_markets = []
    for kw in ["solana", "bitcoin", "ethereum", "crypto"]:
        try:
            batch = client.get_markets(q=kw, status="active", limit=20)
            all_markets.extend(batch)
            time.sleep(0.3)
        except Exception as e:
            log(f"⚠️  Market fetch failed for '{kw}': {e}")

    # Deduplicate by market ID
    seen = set()
    markets = []
    for m in all_markets:
        mid = getattr(m, "id", None) or m.get("id")
        if mid and mid not in seen:
            seen.add(mid)
            markets.append(m)

    log(f"Found {len(markets)} unique markets")

    # 4. Score each market
    candidates = []
    for m in markets:
        question = getattr(m, "question", None) or m.get("question", "")
        market_id = getattr(m, "id", None) or m.get("id")
        prob = getattr(m, "current_probability", None) or m.get("current_probability", 0.5)

        coin_id = detect_coin(question)
        if not coin_id:
            continue

        signal = momentum_signal(signals, coin_id)
        if abs(signal) < 0.1:
            log(f"  skip (neutral signal {signal:.2f}): {question[:60]}")
            continue

        bullish = question_is_bullish(question)
        if bullish is None:
            log(f"  skip (ambiguous direction): {question[:60]}")
            continue

        side, edge = compute_edge(prob, signal, bullish)
        if edge < DIVERGENCE_THRESHOLD:
            log(f"  skip (edge {edge:.1%} < threshold): {question[:60]}")
            continue

        candidates.append({
            "market_id": market_id,
            "question": question,
            "coin_id": coin_id,
            "signal": signal,
            "bullish": bullish,
            "side": side,
            "edge": edge,
            "prob": prob,
        })

    # Sort by edge descending
    candidates.sort(key=lambda x: x["edge"], reverse=True)
    log(f"{len(candidates)} candidates above threshold")

    # 5. Trade top N
    trades_placed = 0
    for c in candidates[:MAX_TRADES_PER_RUN]:
        log(f"\n{'─'*60}")
        log(f"Market:  {c['question'][:70]}")
        log(f"Signal:  {c['coin_id']} momentum={c['signal']:+.2f} | bullish_question={c['bullish']}")
        log(f"Edge:    {c['edge']:.1%} | current_prob={c['prob']:.1%} | side={c['side'].upper()}")

        # Check Simmer context for safeguards
        try:
            ctx = client.get_market_context(c["market_id"])
            trading = ctx.get("trading", {})
            flip_warn = trading.get("flip_flop_warning", "")
            slippage = ctx.get("slippage", {}).get("slippage_pct", 0)
            edge_rec = ctx.get("edge_analysis", {}).get("recommendation", "")

            if flip_warn and "SEVERE" in flip_warn.upper():
                log(f"  ⛔ Skip — flip-flop warning: {flip_warn}")
                continue
            if slippage > 0.15:
                log(f"  ⛔ Skip — slippage too high: {slippage:.1%}")
                continue
            if edge_rec == "HOLD":
                log(f"  ⛔ Skip — edge_analysis says HOLD")
                continue
        except Exception as e:
            log(f"  ⚠️  Context check failed ({e}) — proceeding without it")

        # Build reasoning string (shown publicly on Simmer)
        reasoning = (
            f"{c['coin_id'].upper()} momentum signal: {c['signal']:+.2f} "
            f"({'bullish' if c['signal'] > 0 else 'bearish'} 24h/7d blend). "
            f"Market priced at {c['prob']:.1%}, signal implies {c['side'].upper()} is underpriced "
            f"by ~{c['edge']:.1%}. CoinGecko-sourced, no key required."
        )

        if not live:
            log(f"  [DRY RUN] Would buy {c['side'].upper()} ${TRADE_AMOUNT} | {reasoning}")
            trades_placed += 1
            continue

        try:
            result = client.trade(
                c["market_id"],
                c["side"],
                TRADE_AMOUNT,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            shares = getattr(result, "shares_bought", "?")
            log(f"  ✅ Bought {shares} shares ({c['side'].upper()}) | ${TRADE_AMOUNT}")
            trades_placed += 1
        except Exception as e:
            log(f"  ❌ Trade failed: {e}")

    log(f"\n{'='*60}")
    log(f"Run complete. Trades {'placed' if live else 'simulated'}: {trades_placed}/{min(len(candidates), MAX_TRADES_PER_RUN)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solana/crypto momentum prediction market trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades (default: dry run)")
    args = parser.parse_args()
    run(live=args.live)
