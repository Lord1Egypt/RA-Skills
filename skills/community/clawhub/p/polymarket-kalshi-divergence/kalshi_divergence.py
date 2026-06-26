#!/usr/bin/env python3
"""
Kalshi-Polymarket Divergence Arb — Cross-platform price arbitrage.

Compares Kalshi prices vs Polymarket for equivalent events across crypto,
macro, and politics categories. Generates BUY when gap >8%, SELL when >10%.

Author: Mibayy
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone

import requests
from simmer_sdk import SimmerClient

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SKILL_SLUG = "polymarket-kalshi-divergence"
TRADE_SOURCE = "sdk:polymarket-kalshi-divergence"

_client = None
def get_client():
    global _client
    if _client is None:
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=os.environ.get("TRADING_VENUE", "sim")
        )
    return _client


def check_context(client, market_id, my_probability=None):
    """Check market context before trading (flip-flop, slippage, edge)."""
    try:
        params = {}
        if my_probability is not None:
            params["my_probability"] = my_probability
        ctx = client.get_market_context(market_id, **params)
        trading = ctx.get("trading", {})
        flip_flop = trading.get("flip_flop_warning")
        if flip_flop and "SEVERE" in flip_flop:
            return False, f"flip-flop: {flip_flop}"
        slippage = ctx.get("slippage", {})
        if slippage.get("slippage_pct", 0) > 0.15:
            return False, "slippage too high"
        edge = ctx.get("edge_analysis", {})
        if edge.get("recommendation") == "HOLD":
            return False, "edge below threshold"
        return True, "ok"
    except Exception:
        return True, "context unavailable"


KALSHI_API_BASE = "https://api.elections.kalshi.com/trade-api/v2"

BUY_THRESHOLD = float(os.environ.get('KALSHI_BUY_THRESHOLD', '0.08'))
SELL_THRESHOLD = float(os.environ.get('KALSHI_SELL_THRESHOLD', '0.10'))
TRADE_SIZE_USD = float(os.environ.get('KALSHI_TRADE_SIZE', '20.0'))

# Kalshi series to monitor with Polymarket search keywords
KALSHI_SERIES = {
    "KXBTC":    {"keywords": ["bitcoin", "btc", "bitcoin price"], "category": "crypto"},
    "KXETH":    {"keywords": ["ethereum", "eth", "ether price"], "category": "crypto"},
    "KXSOL":    {"keywords": ["solana", "sol price"], "category": "crypto"},
    "KXXRP":    {"keywords": ["xrp", "ripple"], "category": "crypto"},
    "KXDOGE":   {"keywords": ["dogecoin", "doge"], "category": "crypto"},
    "KXFED":    {"keywords": ["fed", "interest rate", "fomc", "federal reserve"], "category": "macro"},
    "KXCPI":    {"keywords": ["cpi", "inflation", "consumer price"], "category": "macro"},
    "KXUNEMP":  {"keywords": ["unemployment", "jobs report", "nonfarm"], "category": "macro"},
    "KXGLD":    {"keywords": ["gold price", "gold above"], "category": "commodities"},
    "KXOIL":    {"keywords": ["oil price", "crude oil", "wti"], "category": "commodities"},
    "KXNASDAQ": {"keywords": ["nasdaq", "nasdaq 100"], "category": "indices"},
    "KXSPY":    {"keywords": ["s&p 500", "s&p", "spy"], "category": "indices"},
    "KXINX":    {"keywords": ["dow jones", "dow", "djia"], "category": "indices"},
}

log = logging.getLogger(SKILL_SLUG)


# ---------------------------------------------------------------------------
# Kalshi API
# ---------------------------------------------------------------------------
def fetch_kalshi_series(series_ticker: str) -> list:
    """Fetch active markets in a Kalshi series."""
    url = f"{KALSHI_API_BASE}/markets"
    params = {
        "series_ticker": series_ticker,
        "status": "open",
        "limit": 20,
    }

    try:
        resp = requests.get(url, params=params, timeout=15, headers={
            "Accept": "application/json",
        })
        resp.raise_for_status()
        data = resp.json()
        return data.get("markets", [])
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 429:
            log.warning("Kalshi rate limited, sleeping 5s")
            time.sleep(5)
        else:
            log.debug("Kalshi API error for %s: %s", series_ticker, e)
        return []
    except Exception as e:
        log.debug("Kalshi fetch failed for %s: %s", series_ticker, e)
        return []


def get_kalshi_price(market: dict) -> float | None:
    """Extract midpoint price from Kalshi market data."""
    yes_bid = market.get("yes_bid", 0)
    yes_ask = market.get("yes_ask", 0)

    if yes_bid and yes_ask:
        return (yes_bid + yes_ask) / 200.0  # Kalshi prices in cents

    last_price = market.get("last_price")
    if last_price:
        return last_price / 100.0

    return None


def extract_kalshi_description(market: dict) -> str:
    """Get human-readable description from Kalshi market."""
    title = market.get("title", "")
    subtitle = market.get("subtitle", "")
    return f"{title} {subtitle}".strip()


# ---------------------------------------------------------------------------
# Polymarket matching
# ---------------------------------------------------------------------------
def find_polymarket_match(client: SimmerClient, kalshi_market: dict, keywords: list) -> dict | None:
    """Find best matching Polymarket market for a Kalshi market."""
    kalshi_desc = extract_kalshi_description(kalshi_market).lower()

    # Try each keyword to search Polymarket
    for kw in keywords:
        try:
            markets = client.find_markets(query=kw)
        except Exception:
            markets = []

        if not markets:
            continue

        # Score matches
        best_match = None
        best_score = 0

        for pm in markets:
            q = (pm.question or "").lower()
            score = 0

            # Check for overlapping terms
            kalshi_tokens = set(kalshi_desc.split())
            pm_tokens = set(q.split())
            overlap = len(kalshi_tokens & pm_tokens)
            score += overlap * 2

            # Bonus for price-level matches (e.g., "$100,000", "above 5000")
            import re
            kalshi_nums = set(re.findall(r'\d+[,.]?\d*', kalshi_desc))
            pm_nums = set(re.findall(r'\d+[,.]?\d*', q))
            if kalshi_nums & pm_nums:
                score += 10

            # Bonus for keyword in question
            if kw.lower() in q:
                score += 5

            if score > best_score:
                best_score = score
                best_match = pm

        if best_match and best_score >= 5:
            return best_match

    return None


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------
def run(live: bool = False, quiet: bool = False):
    """Main divergence scan and trade loop."""
    client = get_client()

    signals = []
    series_scanned = 0

    for series_ticker, config in KALSHI_SERIES.items():
        log.info("Scanning Kalshi series: %s (%s)", series_ticker, config["category"])

        kalshi_markets = fetch_kalshi_series(series_ticker)
        if not kalshi_markets:
            log.debug("No active markets in %s", series_ticker)
            continue

        series_scanned += 1
        log.info("  Found %d active Kalshi markets", len(kalshi_markets))

        for km in kalshi_markets[:5]:  # cap per series to avoid rate limits
            kalshi_price = get_kalshi_price(km)
            if kalshi_price is None or kalshi_price <= 0.02 or kalshi_price >= 0.98:
                continue  # skip extreme prices

            kalshi_desc = extract_kalshi_description(km)

            # Find matching Polymarket market
            pm_match = find_polymarket_match(client, km, config["keywords"])
            if not pm_match:
                log.debug("  No Polymarket match for: %s", kalshi_desc[:60])
                continue

            pm_price = float(pm_match.current_probability or 0.5)
            pm_question = pm_match.question or ""
            market_id = pm_match.id
            token_id = pm_match.polymarket_token_id

            if not token_id:
                continue

            # Calculate divergence
            divergence = kalshi_price - pm_price  # positive = PM underpriced

            log.info(
                "  %s: Kalshi=%.1f%% Poly=%.1f%% div=%.1f%%",
                kalshi_desc[:50], kalshi_price * 100, pm_price * 100, divergence * 100,
            )

            # Check thresholds
            if divergence > BUY_THRESHOLD:
                signal = {
                    "side": "yes",
                    "market_id": market_id,
                    "token_id": token_id,
                    "pm_question": pm_question,
                    "kalshi_desc": kalshi_desc,
                    "kalshi_price": kalshi_price,
                    "pm_price": pm_price,
                    "divergence": divergence,
                    "series": series_ticker,
                }
                signals.append(signal)
            elif divergence < -SELL_THRESHOLD:
                signal = {
                    "side": "no",
                    "market_id": market_id,
                    "token_id": token_id,
                    "pm_question": pm_question,
                    "kalshi_desc": kalshi_desc,
                    "kalshi_price": kalshi_price,
                    "pm_price": pm_price,
                    "divergence": divergence,
                    "series": series_ticker,
                }
                signals.append(signal)

        time.sleep(0.5)  # rate limit between series

    # Execute trades
    log.info("Scan complete: %d series, %d divergence signals", series_scanned, len(signals))

    trades_made = 0
    for sig in signals:
        reasoning = (
            f"Kalshi-Polymarket divergence ({sig['series']}): "
            f"Kalshi={sig['kalshi_price']:.1%} vs Polymarket={sig['pm_price']:.1%}, "
            f"gap={abs(sig['divergence']):.1%}. "
            f"Kalshi event: {sig['kalshi_desc'][:80]}. "
            f"{'Polymarket underpriced — buying' if sig['side'] == 'yes' else 'Polymarket overpriced — selling'}."
        )

        target_price = round(sig["kalshi_price"] - (sig["divergence"] * 0.3), 2)
        target_price = max(0.01, min(0.99, target_price))

        log.info(
            "TRADE: %s %s @ %.2f — div=%.1f%%",
            sig["side"].upper(), sig["pm_question"][:50], target_price, sig["divergence"] * 100,
        )

        ok, reason = check_context(client, sig["market_id"])
        if not ok:
            log.warning("Skipping trade: %s", reason)
            continue

        if live:
            try:
                result = client.trade(
                    market_id=sig["market_id"],
                    side=sig["side"],
                    amount=TRADE_SIZE_USD,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                    reasoning=reasoning,
                )
                log.info("  Order placed: %s", json.dumps(result, default=str)[:200])
                trades_made += 1
            except Exception as e:
                log.error("  Order failed: %s", e)
        else:
            log.info("  [DRY RUN] Would %s $%.0f", sig["side"], TRADE_SIZE_USD)
            trades_made += 1

    if not quiet:
        print(f"\n{'='*60}")
        print(f"Kalshi-Polymarket Divergence Scan — {datetime.now(timezone.utc).isoformat()}")
        print(f"Series scanned: {series_scanned}/{len(KALSHI_SERIES)}")
        print(f"Divergence signals: {len(signals)}")
        print(f"Trades: {trades_made}")
        print(f"Mode: {'LIVE' if live else 'DRY RUN'}")
        print(f"{'='*60}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Kalshi-Polymarket Divergence Arb")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--quiet", action="store_true", help="Suppress summary output")
    parser.add_argument("--debug", action="store_true", help="Debug logging")
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else (logging.WARNING if args.quiet else logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")

    if not os.environ.get("SIMMER_API_KEY"):
        log.error("SIMMER_API_KEY not set")
        sys.exit(1)

    try:
        run(live=args.live, quiet=args.quiet)
    except KeyboardInterrupt:
        log.info("Interrupted")
    except Exception as e:
        log.error("Fatal: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
