#!/usr/bin/env python3
"""
Kalshi Fed Dot Plot Trader

Trades Fed rate markets on Kalshi using FOMC dot plot median implied rate path.
Computes fair probability of cut/hike per meeting from dot plot, trades when
market diverges from implied path.

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
import math
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
    "entry_edge":        {"env": "SIMMER_FED_DOT_ENTRY_EDGE",        "default": 0.10,  "type": float},
    "exit_threshold":    {"env": "SIMMER_FED_DOT_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_FED_DOT_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_FED_DOT_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_FED_DOT_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_FED_DOT_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-fed-dot-plot-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-fed-dotplot"
SKILL_SLUG = "kalshi-fed-dot-plot-trader"
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
# Dot Plot Implied Rate Path
# =============================================================================

# FOMC dot plot median implies these end-of-quarter target rates for 2026.
# Update after each SEP (Summary of Economic Projections) release.
# Current values reflect the March 2026 dot plot median.
DOT_PLOT = {
    "2026Q2": 4.50,   # End of Q2 2026 (June meeting)
    "2026Q3": 4.25,   # End of Q3 2026 (September meeting)
    "2026Q4": 4.00,   # End of Q4 2026 (December meeting)
}

# Current effective rate (upper bound of target range)
CURRENT_RATE = 4.75

# Each cut is 25bps
CUT_SIZE = 0.25

# Map FOMC meetings to quarters
MEETING_TO_QUARTER = {
    "january": "Q1", "march": "Q1",
    "april": "Q2", "june": "Q2",
    "july": "Q3", "september": "Q3",
    "october": "Q4", "december": "Q4",
}

# FOMC meeting month list for parsing
FOMC_MONTHS = [
    "january", "march", "april", "june",
    "july", "september", "october", "december",
]

MONTH_ALIASES = {
    "jan": "january", "feb": "march", "mar": "march",
    "apr": "april", "may": "june",
    "jun": "june", "jul": "july",
    "aug": "september", "sep": "september",
    "oct": "october", "nov": "december",
    "dec": "december",
}

# Quarter ordering for cumulative cut computation
QUARTER_ORDER = ["2026Q1", "2026Q2", "2026Q3", "2026Q4"]

# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    """Windows-safe print that handles Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


def extract_meeting_month(question: str) -> str | None:
    """Extract FOMC meeting month from market question."""
    q = question.lower()
    for month in FOMC_MONTHS:
        if month in q:
            return month
    for abbr, canonical in MONTH_ALIASES.items():
        if re.search(r'\b' + abbr + r'\b', q):
            return canonical
    return None


def extract_year(question: str) -> int | None:
    """Extract year from market question."""
    m = re.search(r'20(2[4-9])', question)
    if m:
        return int("20" + m.group(1))
    return None


def is_rate_cut_market(question: str) -> bool:
    """Check if market is about Fed rate cut."""
    q = question.lower()
    return ("rate" in q and ("cut" in q or "lower" in q or "reduce" in q))


def is_rate_hike_market(question: str) -> bool:
    """Check if market is about Fed rate hike."""
    q = question.lower()
    return ("rate" in q and ("hike" in q or "raise" in q or "increase" in q))


# =============================================================================
# Dot Plot Fair Value Computation
# =============================================================================

def compute_implied_rate_by_meeting(month: str, year: int = 2026) -> float:
    """Compute the dot-plot implied target rate at a given FOMC meeting.

    Interpolates between quarter-end dot plot values. If the meeting is before
    the first dot plot quarter, returns CURRENT_RATE.
    """
    quarter = MEETING_TO_QUARTER.get(month)
    if quarter is None:
        return CURRENT_RATE

    quarter_key = f"{year}{quarter}"

    # If before our dot plot range, use current rate
    if quarter_key not in DOT_PLOT and year <= 2026:
        # Check if quarter_key is before all dot plot keys
        for q in QUARTER_ORDER:
            if q in DOT_PLOT:
                if quarter_key <= q:
                    return CURRENT_RATE
                break

    # Direct match
    if quarter_key in DOT_PLOT:
        return DOT_PLOT[quarter_key]

    return CURRENT_RATE


def compute_cuts_by_meeting(month: str, year: int = 2026) -> int:
    """Compute number of 25bp cuts implied by dot plot from now to meeting."""
    implied_rate = compute_implied_rate_by_meeting(month, year)
    cuts = (CURRENT_RATE - implied_rate) / CUT_SIZE
    return max(0, round(cuts))


def fair_cut_probability(month: str, year: int = 2026) -> float:
    """Compute fair probability of at least one rate cut by this meeting.

    If the dot plot implies N cuts by this meeting date, the fair probability
    of "at least one cut" is high. We model uncertainty around the dot plot
    using a simple logistic function based on the number of implied cuts.
    """
    cuts = compute_cuts_by_meeting(month, year)

    if cuts <= 0:
        # Dot plot says no cut expected -- low probability but not zero
        return 0.15
    elif cuts == 1:
        # One cut implied -- moderately confident
        return 0.70
    elif cuts == 2:
        # Two cuts implied -- high confidence at least one happens
        return 0.85
    else:
        # Three+ cuts implied -- very high probability
        return 0.92


def fair_hike_probability(month: str, year: int = 2026) -> float:
    """Compute fair probability of rate hike by this meeting.

    If the dot plot implies cuts, hike probability is very low.
    """
    cuts = compute_cuts_by_meeting(month, year)
    if cuts >= 2:
        return 0.03
    elif cuts == 1:
        return 0.05
    else:
        return 0.10


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
            if not ("rate" in question and ("fed" in question or "federal" in question)):
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
    try:
        result = get_client()._request(
            "GET", "/api/sdk/markets",
            params={"status": "active", "import_source": "kalshi",
                    "q": "rate", "limit": 50}
        )
        markets = result.get("markets", [])
        return [m for m in markets
                if is_rate_cut_market(m.get("question", ""))
                or is_rate_hike_market(m.get("question", ""))]
    except Exception as e:
        safe_print(f"  Failed to fetch markets: {e}")
        return []


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
    """Check open Fed dot plot positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    fed_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or ("rate" in (p.get("question") or "").lower()
                   and ("fed" in (p.get("question") or "").lower()
                        or "federal" in (p.get("question") or "").lower()))]

    if not fed_pos:
        return 0, 0

    log(f"\n  Checking {len(fed_pos)} Fed dot plot positions for exit...")
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
    """Run the Fed Dot Plot trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Fed Dot Plot Trader")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        log("\nDot Plot Implied Path:")
        for q_key in QUARTER_ORDER:
            rate = DOT_PLOT.get(q_key, CURRENT_RATE)
            log(f"  {q_key}: {rate:.2f}%")
        return

    # Init client
    get_client(live=not dry_run)

    # Positions only
    if positions_only:
        positions = get_positions()
        fed_pos = [p for p in positions
                   if "rate" in (p.get("question") or "").lower()]
        if not fed_pos:
            log("  No Fed rate positions")
        for p in fed_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Display dot plot model ---
    log("Dot Plot Implied Rate Path:")
    log(f"  Current rate: {CURRENT_RATE:.2f}%")
    for q_key in QUARTER_ORDER:
        if q_key in DOT_PLOT:
            rate = DOT_PLOT[q_key]
            cuts = round((CURRENT_RATE - rate) / CUT_SIZE)
            log(f"  {q_key}: {rate:.2f}% ({cuts} cuts implied)")
    log("")

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

    # --- Analyze & Trade ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for m in markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0

        month = extract_meeting_month(question)
        year = extract_year(question) or 2026

        if month is None:
            log(f"  ? No meeting date: {question[:60]}")
            continue

        # Determine market type and fair value
        if is_rate_cut_market(question):
            fair_p = fair_cut_probability(month, year)
            market_type = "cut"
        elif is_rate_hike_market(question):
            fair_p = fair_hike_probability(month, year)
            market_type = "hike"
        else:
            continue

        edge = fair_p - price
        implied_rate = compute_implied_rate_by_meeting(month, year)
        log(f"  {month:>12} {year} {market_type}: market={price:.1%}  "
            f"fair={fair_p:.1%}  edge={edge:+.1%}  implied_rate={implied_rate:.2f}%")

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
                                 my_probability=fair_p if side == "yes" else 1 - fair_p)
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
                reasoning=(f"Dot plot: {month} {year} {market_type} "
                           f"market={price:.1%} fair={fair_p:.1%} edge={edge:+.1%}"),
                signal_data={
                    "fair_prob": round(fair_p, 4),
                    "market_price": round(price, 4),
                    "edge": round(edge, 4),
                    "implied_rate": implied_rate,
                    "meeting": f"{month} {year}",
                    "market_type": market_type,
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
                              thesis=f"Dot plot edge on {month} {year} {market_type}",
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
    parser = argparse.ArgumentParser(description="Kalshi Fed Dot Plot Trader")
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
