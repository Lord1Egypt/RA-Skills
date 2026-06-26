#!/usr/bin/env python3
"""
Kalshi Fed Speech Signal Trader

Trades Fed rate markets on Kalshi based on hawkish/dovish sentiment signals
extracted from market question text. Scores net sentiment from keyword matching
and adjusts rate cut probabilities accordingly.

Usage:
    python trader.py              # Dry run (show opportunities, no trades)
    python trader.py --live       # Execute real trades via DFlow/Solana
    python trader.py --positions  # Show current positions only
    python trader.py --config     # Show current configuration

Requires:
    SIMMER_API_KEY environment variable (get from simmer.markets/dashboard)
    SOLANA_PRIVATE_KEY environment variable (base58-encoded, for live trading)
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime, timezone

# Force line-buffered stdout for non-TTY environments (cron, Docker, automaton)
sys.stdout.reconfigure(line_buffering=True)

# Optional: Trade Journal integration
try:
    from tradejournal import log_trade
    JOURNAL_AVAILABLE = True
except ImportError:
    try:
        from skills.tradejournal import log_trade
        JOURNAL_AVAILABLE = True
    except ImportError:
        JOURNAL_AVAILABLE = False
        def log_trade(*args, **kwargs):
            pass

# =============================================================================
# Configuration
# =============================================================================

from simmer_sdk.skill import load_config, update_config, get_config_path

CONFIG_SCHEMA = {
    "entry_edge":        {"env": "SIMMER_FED_SPEECH_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_FED_SPEECH_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_FED_SPEECH_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_FED_SPEECH_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_FED_SPEECH_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_FED_SPEECH_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-fed-speech-signal-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-fed-speech"
SKILL_SLUG = "kalshi-fed-speech-signal-trader"
_automaton_reported = False

# Kalshi constraints
MIN_SHARES_PER_ORDER = 1.0

# Strategy parameters from config
ENTRY_EDGE = _config["entry_edge"]
EXIT_THRESHOLD = _config["exit_threshold"]
MAX_POSITION_USD = _config["max_position_usd"]
_automaton_max = os.environ.get("AUTOMATON_MAX_BET")
if _automaton_max:
    MAX_POSITION_USD = min(MAX_POSITION_USD, float(_automaton_max))

MAX_TRADES_PER_RUN = _config["max_trades_per_run"]
SLIPPAGE_MAX_PCT = _config["slippage_max"]
MIN_LIQUIDITY_USD = _config["min_liquidity"]
TIME_TO_RESOLUTION_MIN_HOURS = 2

# =============================================================================
# Hawkish/Dovish Keyword Dictionaries
# =============================================================================

# Hawkish signals: inflation concerns, tightening bias, restrictive stance
HAWKISH_KEYWORDS = [
    "inflation persistent",
    "inflation expectations",
    "tightening",
    "restrictive",
    "price stability",
    "above target",
    "too high",
    "overheating",
    "wage pressure",
    "sticky inflation",
    "higher for longer",
    "not yet confident",
    "premature",
    "upside risk",
    "strong demand",
]

# Dovish signals: easing bias, labor concerns, balanced approach
DOVISH_KEYWORDS = [
    "data dependent",
    "labor softening",
    "gradual",
    "balanced",
    "appropriate to reduce",
    "progress on inflation",
    "cooling",
    "disinflation",
    "downside risk",
    "labor market cooling",
    "sufficient progress",
    "well positioned",
    "slowing growth",
    "moderating",
    "easing",
]

# Per-keyword weight (default 1.0, some signals stronger)
HAWKISH_WEIGHTS = {
    "inflation persistent": 1.5,
    "restrictive": 1.2,
    "higher for longer": 1.5,
    "overheating": 1.3,
    "not yet confident": 1.3,
}

DOVISH_WEIGHTS = {
    "appropriate to reduce": 1.5,
    "sufficient progress": 1.3,
    "labor softening": 1.2,
    "disinflation": 1.2,
    "easing": 1.0,
}

# Sentiment shift per net score unit
SENTIMENT_SHIFT_PER_UNIT = 0.05  # 5% probability shift per net unit

# Baseline rate cut probability
BASELINE_CUT_PROB = 0.50

# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    """Windows-safe print that handles Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


def is_rate_market(question: str) -> bool:
    """Check if market is about Fed rate decisions."""
    q = question.lower()
    return (("rate" in q and ("cut" in q or "hike" in q or "lower" in q
                              or "raise" in q or "hold" in q or "unchanged" in q))
            and ("fed" in q or "federal" in q or "fomc" in q))


def is_rate_cut_market(question: str) -> bool:
    """Check if market is specifically about a rate cut."""
    q = question.lower()
    return ("rate" in q and ("cut" in q or "lower" in q or "reduce" in q)
            and ("fed" in q or "federal" in q or "fomc" in q))


def score_sentiment(text: str) -> tuple[float, list[str], list[str]]:
    """Score hawkish/dovish sentiment from text.

    Returns (net_score, hawkish_hits, dovish_hits).
    Positive net_score = dovish (more likely to cut).
    Negative net_score = hawkish (less likely to cut).
    """
    t = text.lower()
    hawkish_hits = []
    dovish_hits = []
    hawkish_total = 0.0
    dovish_total = 0.0

    for kw in HAWKISH_KEYWORDS:
        if kw in t:
            weight = HAWKISH_WEIGHTS.get(kw, 1.0)
            hawkish_total += weight
            hawkish_hits.append(kw)

    for kw in DOVISH_KEYWORDS:
        if kw in t:
            weight = DOVISH_WEIGHTS.get(kw, 1.0)
            dovish_total += weight
            dovish_hits.append(kw)

    # Net score: positive = dovish, negative = hawkish
    net_score = dovish_total - hawkish_total
    return net_score, hawkish_hits, dovish_hits


def compute_speech_adjusted_prob(net_sentiment: float) -> float:
    """Compute speech-adjusted fair probability of rate cut.

    Positive sentiment (dovish) increases cut probability.
    Negative sentiment (hawkish) decreases cut probability.
    """
    shift = net_sentiment * SENTIMENT_SHIFT_PER_UNIT
    adjusted = BASELINE_CUT_PROB + shift
    return max(0.05, min(0.95, adjusted))


# =============================================================================
# Simmer Client
# =============================================================================

def get_client(live=True):
    """Lazy-init SimmerClient singleton."""
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY environment variable not set")
            print("Get your API key from: simmer.markets/dashboard -> SDK tab")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "kalshi")
        _client = SimmerClient(api_key=api_key, venue=venue, live=live)
    return _client


# =============================================================================
# Market Discovery
# =============================================================================

def discover_and_import(log=print):
    """Discover Fed rate markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["fed", "federal reserve", "rate"]:
        try:
            results = client.list_importable_markets(
                q=term, venue="kalshi", limit=20, min_volume=0
            )
        except Exception as e:
            if "429" in str(e):
                log("  Rate limit reached -- stopping discovery")
                return imported
            log(f"  Discovery failed for '{term}': {e}")
            continue

        for m in results:
            url = m.get("url", "")
            question = (m.get("question") or "").lower()
            if not url or url in seen:
                continue
            seen.add(url)
            if not is_rate_market(question):
                continue
            try:
                result = client.import_kalshi_market(url)
                status = result.get("status", "") if result else ""
                if status == "imported":
                    imported += 1
                    log(f"  Imported: {m.get('question', url)[:70]}")
            except Exception as e:
                if "rate limit" in str(e).lower() or "429" in str(e):
                    log("  Rate limit reached -- stopping discovery")
                    return imported

    return imported


def fetch_fed_markets():
    """Fetch active Fed rate markets from Simmer API."""
    all_markets = []
    seen_ids = set()

    for query in ["fed rate", "federal reserve", "fomc"]:
        try:
            result = get_client()._request(
                "GET", "/api/sdk/markets",
                params={"status": "active", "import_source": "kalshi",
                        "q": query, "limit": 50}
            )
            markets = result.get("markets", [])
            for m in markets:
                mid = m.get("id")
                if mid not in seen_ids and is_rate_market(m.get("question", "")):
                    all_markets.append(m)
                    seen_ids.add(mid)
        except Exception as e:
            safe_print(f"  Failed to fetch markets for '{query}': {e}")

    return all_markets


# =============================================================================
# Aggregate Sentiment from All Market Questions
# =============================================================================

def compute_aggregate_sentiment(markets: list, log=print) -> tuple[float, dict]:
    """Compute aggregate hawkish/dovish sentiment from all market question texts.

    Pools all question text together and scores once. Also returns per-market
    sentiment breakdown for logging.

    Returns (net_sentiment_score, details_dict).
    """
    all_text = " ".join(m.get("question", "") for m in markets)
    net_score, hawk_hits, dove_hits = score_sentiment(all_text)

    # Also compute per-market for detailed logging
    per_market = {}
    for m in markets:
        q = m.get("question", "")
        ms, mh, md = score_sentiment(q)
        if ms != 0:
            per_market[q[:50]] = {
                "score": ms,
                "hawkish": mh,
                "dovish": md,
            }

    details = {
        "net_score": net_score,
        "hawkish_hits": hawk_hits,
        "dovish_hits": dove_hits,
        "n_markets": len(markets),
        "per_market": per_market,
    }

    return net_score, details


# =============================================================================
# Context & Safeguards
# =============================================================================

def get_market_context(market_id: str, my_probability: float = None) -> dict:
    """Get market context with safeguards and edge analysis."""
    try:
        if my_probability is not None:
            return get_client()._request(
                "GET", f"/api/sdk/context/{market_id}",
                params={"my_probability": my_probability}
            )
        return get_client().get_market_context(market_id)
    except Exception:
        return None


def check_safeguards(context: dict) -> tuple[bool, list[str]]:
    """Check context for safeguards. Returns (should_trade, reasons)."""
    if not context:
        return True, []

    reasons = []
    market = context.get("market", {})
    warnings = context.get("warnings", [])
    discipline = context.get("discipline", {})
    slippage = context.get("slippage", {})

    for w in warnings:
        if "MARKET RESOLVED" in str(w).upper():
            return False, ["Market already resolved"]

    level = discipline.get("warning_level", "none")
    if level == "severe":
        return False, [f"Severe flip-flop: {discipline.get('flip_flop_warning', '')}"]
    elif level == "mild":
        reasons.append("Mild flip-flop warning")

    time_str = market.get("time_to_resolution", "")
    if time_str:
        try:
            hours = 0
            if "d" in time_str:
                hours += int(time_str.split("d")[0].strip()) * 24
            if "h" in time_str:
                h_part = time_str.split("h")[0]
                if "d" in h_part:
                    h_part = h_part.split("d")[-1].strip()
                hours += int(h_part)
            if hours < TIME_TO_RESOLUTION_MIN_HOURS:
                return False, [f"Resolves in {hours}h -- too soon"]
        except (ValueError, IndexError):
            pass

    if MIN_LIQUIDITY_USD > 0:
        liquidity = market.get("liquidity", 0) or 0
        if liquidity < MIN_LIQUIDITY_USD:
            return False, [f"Low liquidity: ${liquidity:.0f}"]

    estimates = slippage.get("estimates", []) if slippage else []
    if estimates:
        slip = estimates[0].get("slippage_pct", 0)
        if slip > SLIPPAGE_MAX_PCT:
            return False, [f"Slippage {slip:.1%} > max {SLIPPAGE_MAX_PCT:.0%}"]

    return True, reasons


# =============================================================================
# Trade Execution
# =============================================================================

def execute_trade(market_id: str, side: str, amount: float,
                  reasoning: str = "", signal_data: dict = None) -> dict:
    """Execute a trade via Simmer SDK with source tagging."""
    try:
        result = get_client().trade(
            market_id=market_id, side=side, amount=amount,
            source=TRADE_SOURCE, skill_slug=SKILL_SLUG,
            reasoning=reasoning, signal_data=signal_data,
        )
        return {
            "success": result.success,
            "trade_id": result.trade_id,
            "shares_bought": result.shares_bought,
            "error": result.error,
            "simulated": result.simulated,
        }
    except Exception as e:
        return {"error": str(e)}


def get_positions():
    """Get current open positions."""
    try:
        result = get_client()._request("GET", "/api/sdk/positions")
        return result.get("positions", []) if isinstance(result, dict) else result
    except Exception:
        return []


def check_exits(dry_run: bool, log=print) -> tuple[int, int]:
    """Check open Fed speech positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    fed_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or is_rate_market(p.get("question") or "")]

    if not fed_pos:
        return 0, 0

    log(f"\n  Checking {len(fed_pos)} Fed speech positions for exit...")
    found, executed = 0, 0

    for pos in fed_pos:
        market_id = pos.get("market_id")
        price = pos.get("current_price") or pos.get("price_yes") or 0
        shares = pos.get("shares_yes") or pos.get("shares") or 0
        question = pos.get("question", "")[:50]

        if shares < MIN_SHARES_PER_ORDER:
            continue

        if price >= EXIT_THRESHOLD:
            found += 1
            log(f"  EXIT: {question}  price={price:.2f} >= {EXIT_THRESHOLD:.2f}")

            ctx = get_market_context(market_id)
            ok, reasons = check_safeguards(ctx)
            if not ok:
                log(f"    Skipped: {'; '.join(reasons)}")
                continue

            if not dry_run:
                result = execute_trade(
                    market_id, "sell", shares,
                    reasoning=f"Exit: price {price:.2f} >= threshold {EXIT_THRESHOLD:.2f}",
                )
                if result.get("success"):
                    executed += 1
                    tag = "[PAPER] " if result.get("simulated") else ""
                    log(f"    {tag}Sold {shares:.1f} @ {price:.2f}")
                    if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                        log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                                  skill_slug=SKILL_SLUG, thesis="Exit on threshold", action="sell")
                else:
                    log(f"    Sell failed: {result.get('error')}")
            else:
                log(f"    [DRY RUN] Would sell {shares:.1f} shares")

    return found, executed


# =============================================================================
# Main Strategy
# =============================================================================

def run_strategy(dry_run: bool = True, positions_only: bool = False,
                 show_config: bool = False, quiet: bool = False):
    """Run the Fed Speech Signal trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Fed Speech Signal Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        log("\nHawkish keywords:")
        for kw in HAWKISH_KEYWORDS:
            w = HAWKISH_WEIGHTS.get(kw, 1.0)
            log(f"  - {kw} (weight={w:.1f})")
        log("\nDovish keywords:")
        for kw in DOVISH_KEYWORDS:
            w = DOVISH_WEIGHTS.get(kw, 1.0)
            log(f"  - {kw} (weight={w:.1f})")
        return

    # Init client
    get_client(live=not dry_run)

    # Positions only
    if positions_only:
        positions = get_positions()
        fed_pos = [p for p in positions if is_rate_market(p.get("question") or "")]
        if not fed_pos:
            log("  No Fed rate positions")
        for p in fed_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering Fed rate markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_fed_markets()
    log(f"  Found {len(markets)} active Fed rate markets")

    if not markets:
        log("  No Fed rate markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Compute aggregate sentiment ---
    net_sentiment, details = compute_aggregate_sentiment(markets, log=log)
    log(f"\n  Aggregate sentiment score: {net_sentiment:+.1f}")
    if details["hawkish_hits"]:
        log(f"    Hawkish: {', '.join(details['hawkish_hits'])}")
    if details["dovish_hits"]:
        log(f"    Dovish:  {', '.join(details['dovish_hits'])}")

    # --- Compute adjusted fair probability ---
    fair_cut_p = compute_speech_adjusted_prob(net_sentiment)
    direction = "dovish" if net_sentiment > 0 else "hawkish" if net_sentiment < 0 else "neutral"
    log(f"  Adjusted fair cut probability: {fair_cut_p:.1%} "
        f"(baseline={BASELINE_CUT_PROB:.0%}, sentiment={direction})")
    log("")

    # --- Filter to rate cut markets only for trading ---
    cut_markets = [m for m in markets if is_rate_cut_market(m.get("question", ""))]
    log(f"  Rate cut markets to trade: {len(cut_markets)}")

    # --- Analyze & Trade ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for m in cut_markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0

        edge = fair_cut_p - price
        log(f"  {question[:55]:55s}  market={price:.1%}  fair={fair_cut_p:.1%}  edge={edge:+.1%}")

        side = None
        if edge >= ENTRY_EDGE:
            side = "yes"
        elif edge <= -ENTRY_EDGE:
            side = "no"
        else:
            continue

        signals += 1

        # Conviction-based sizing
        raw_conv = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        log(f"    -> BUY {side.upper()}: |edge|={abs(edge):.1%}  size=${size:.2f}")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        ctx = get_market_context(market_id,
                                 my_probability=fair_cut_p if side == "yes" else 1 - fair_cut_p)
        ok, reasons = check_safeguards(ctx)
        if not ok:
            log(f"    Skipped: {'; '.join(reasons)}")
            skip_reasons.extend(reasons)
            continue
        if reasons:
            log(f"    Warnings: {'; '.join(reasons)}")

        if not dry_run:
            result = execute_trade(
                market_id, side, size,
                reasoning=(f"Speech signal: sentiment={net_sentiment:+.1f} ({direction}) "
                           f"fair={fair_cut_p:.1%} market={price:.1%} edge={edge:+.1%}"),
                signal_data={
                    "fair_prob": round(fair_cut_p, 4),
                    "market_price": round(price, 4),
                    "edge": round(edge, 4),
                    "net_sentiment": round(net_sentiment, 2),
                    "direction": direction,
                    "hawkish_hits": details["hawkish_hits"],
                    "dovish_hits": details["dovish_hits"],
                },
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG,
                              thesis=f"Speech signal: {direction} sentiment",
                              action="buy")
            else:
                log(f"    Trade failed: {result.get('error')}", force=True)
        else:
            log(f"    [DRY RUN] Would buy {side.upper()} ${size:.2f}")
            trades_executed += 1
            total_usd += size

    # --- Exits ---
    exits_found, exits_exec = check_exits(dry_run, log=log)

    # --- Summary ---
    log(f"\n  Signals: {signals}  Trades: {trades_executed}  USD: ${total_usd:.2f}")
    if exits_found:
        log(f"  Exits: {exits_found} found, {exits_exec} executed")

    # --- Automaton report ---
    if os.environ.get("AUTOMATON_MANAGED"):
        _automaton_reported = True
        report = {
            "signals": signals + exits_found,
            "trades_attempted": signals + exits_found,
            "trades_executed": trades_executed + exits_exec,
            "amount_usd": round(total_usd, 2),
        }
        if signals > 0 and trades_executed == 0 and skip_reasons:
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        print(json.dumps({"automaton": report}))


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kalshi Fed Speech Signal Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show positions only")
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set config value (e.g., --set entry_edge=0.15)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Only output on trades/errors")
    args = parser.parse_args()

    if args.set:
        updates = {}
        for item in args.set:
            if "=" in item:
                key, val = item.split("=", 1)
                if key in CONFIG_SCHEMA:
                    updates[key] = CONFIG_SCHEMA[key]["type"](val)
        if updates:
            update_config(updates, __file__)
            safe_print(f"Updated config: {updates}")

    dry_run = not args.live
    run_strategy(dry_run, args.positions, args.config, args.quiet)

    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_reported:
        print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                        "skip_reason": "no_signal"}}))
