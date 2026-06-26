#!/usr/bin/env python3
"""
Kalshi Fed Futures Arb Trader

Compares CME FedWatch implied rate probabilities (derived from fed funds futures)
to Kalshi Fed rate decision market prices. Trades when divergence exceeds threshold.

Usage:
    python trader.py              # Dry run (show opportunities, no trades)
    python trader.py --live       # Execute real trades via DFlow/Solana
    python trader.py --positions  # Show current positions only
    python trader.py --config     # Show current configuration
    python trader.py --set FEDWATCH_JUN2026=0.65  # Update FedWatch prob

Requires:
    SIMMER_API_KEY environment variable (get from simmer.markets/dashboard)
    SOLANA_PRIVATE_KEY environment variable (base58-encoded, for live trading)
"""

import os
import sys
import json
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
    "entry_edge":        {"env": "SIMMER_FED_FUT_ENTRY_EDGE",        "default": 0.08,  "type": float},
    "exit_threshold":    {"env": "SIMMER_FED_FUT_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_FED_FUT_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_FED_FUT_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_FED_FUT_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_FED_FUT_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-fed-futures-arb-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-fed-futures"
SKILL_SLUG = "kalshi-fed-futures-arb-trader"
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
# CME FedWatch Implied Probabilities
# =============================================================================
# These represent the market-implied probability of a rate CUT at each meeting,
# derived from fed funds futures prices. Update periodically from CME FedWatch.
# Format: meeting_label -> P(cut at or before this meeting)
#
# Last updated: 2026-04-02
# Source: https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html

FEDWATCH_PROBS = {
    "may_2026":  0.12,   # May 2026 FOMC — low probability of cut
    "jun_2026":  0.35,   # June 2026 FOMC
    "jul_2026":  0.52,   # July 2026 FOMC
    "sep_2026":  0.68,   # September 2026 FOMC
    "nov_2026":  0.75,   # November 2026 FOMC
    "dec_2026":  0.82,   # December 2026 FOMC
}

# Meeting date aliases for market question parsing
MEETING_ALIASES = {
    "may": "may_2026", "may 2026": "may_2026", "may fomc": "may_2026",
    "june": "jun_2026", "jun": "jun_2026", "june 2026": "jun_2026",
    "jun 2026": "jun_2026", "june fomc": "jun_2026",
    "july": "jul_2026", "jul": "jul_2026", "july 2026": "jul_2026",
    "jul 2026": "jul_2026", "july fomc": "jul_2026",
    "september": "sep_2026", "sep": "sep_2026", "sept": "sep_2026",
    "september 2026": "sep_2026", "sep 2026": "sep_2026",
    "november": "nov_2026", "nov": "nov_2026", "november 2026": "nov_2026",
    "nov 2026": "nov_2026",
    "december": "dec_2026", "dec": "dec_2026", "december 2026": "dec_2026",
    "dec 2026": "dec_2026",
}

# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    """Windows-safe print that handles Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


def extract_meeting(question: str) -> str | None:
    """Extract FOMC meeting date from a market question string."""
    q = question.lower()
    # Try longest aliases first for correct matching
    for alias in sorted(MEETING_ALIASES.keys(), key=len, reverse=True):
        if alias in q:
            return MEETING_ALIASES[alias]
    return None


def is_rate_cut_market(question: str) -> bool:
    """Check if the market is about a Fed rate cut/decision."""
    q = question.lower()
    rate_terms = ["rate cut", "rate hike", "federal reserve", "fed funds",
                  "fomc", "interest rate", "federal funds rate", "rate decision"]
    return any(term in q for term in rate_terms)


def detect_market_direction(question: str) -> str:
    """Detect whether a YES on this market means a cut or a hold/hike.

    Returns 'cut' if YES = rate cut happens, 'hike' if YES = rate hike/hold.
    """
    q = question.lower()
    if "cut" in q or "lower" in q or "decrease" in q or "reduce" in q:
        return "cut"
    elif "hike" in q or "raise" in q or "increase" in q or "higher" in q:
        return "hike"
    # Default: assume YES = cut (most common on Kalshi)
    return "cut"


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

    search_terms = ["fed rate", "federal reserve rate", "rate cut",
                    "rate hike", "FOMC", "federal funds"]

    for term in search_terms:
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
            if not is_rate_cut_market(question):
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
    """Fetch active Fed rate decision markets from Simmer API."""
    try:
        all_markets = []
        for query in ["fed rate", "federal reserve", "FOMC", "rate cut"]:
            result = get_client()._request(
                "GET", "/api/sdk/markets",
                params={"status": "active", "import_source": "kalshi",
                        "q": query, "limit": 50}
            )
            markets = result.get("markets", [])
            all_markets.extend(markets)

        # Deduplicate by market ID
        seen_ids = set()
        unique = []
        for m in all_markets:
            mid = m.get("id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                if is_rate_cut_market(m.get("question", "")):
                    unique.append(m)
        return unique
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
    """Check open Fed rate positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    fed_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or is_rate_cut_market(p.get("question", ""))]

    if not fed_pos:
        return 0, 0

    log(f"\n  Checking {len(fed_pos)} Fed rate positions for exit...")
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

def compute_edge(market_price: float, fedwatch_prob: float,
                 direction: str) -> tuple[float, str]:
    """Compute edge between FedWatch fair value and market price.

    Returns (signed_edge, explanation).
    If direction == 'cut', YES = cut happens, so fair_yes = fedwatch_prob.
    If direction == 'hike', YES = hike, so fair_yes = 1 - fedwatch_prob.
    """
    if direction == "cut":
        fair_yes = fedwatch_prob
    else:
        fair_yes = 1.0 - fedwatch_prob

    edge = fair_yes - market_price
    explanation = (f"FedWatch={fedwatch_prob:.1%} direction={direction} "
                   f"fair_yes={fair_yes:.1%} market={market_price:.1%} edge={edge:+.1%}")
    return edge, explanation


def run_strategy(dry_run: bool = True, positions_only: bool = False,
                 show_config: bool = False, quiet: bool = False):
    """Run the FedWatch futures arbitrage trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Fed Futures Arb Trader (CME FedWatch vs Kalshi)")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        log("\nFedWatch probabilities:")
        for meeting, prob in sorted(FEDWATCH_PROBS.items()):
            log(f"  {meeting}: {prob:.1%}")
        return

    # Init client
    get_client(live=not dry_run)

    # Positions only
    if positions_only:
        positions = get_positions()
        fed_pos = [p for p in positions if is_rate_cut_market(p.get("question", ""))]
        if not fed_pos:
            log("  No Fed rate positions")
        for p in fed_pos:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- FedWatch Reference ---
    log("CME FedWatch Implied Cut Probabilities:")
    for meeting, prob in sorted(FEDWATCH_PROBS.items()):
        log(f"  {meeting:>12}: {prob:6.1%}")
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

        meeting = extract_meeting(question)
        if not meeting:
            log(f"  ? No meeting match: {question[:60]}")
            continue

        fedwatch_prob = FEDWATCH_PROBS.get(meeting)
        if fedwatch_prob is None:
            log(f"  ? No FedWatch data for: {meeting}")
            continue

        direction = detect_market_direction(question)
        edge, explanation = compute_edge(price, fedwatch_prob, direction)

        log(f"  {meeting:>12}: {explanation}")

        side = None
        if edge >= ENTRY_EDGE:
            side = "yes"
        elif edge <= -ENTRY_EDGE:
            side = "no"
        else:
            continue

        signals += 1

        # Conviction-based sizing: edge / entry_edge normalized to 0-1
        raw_conv = min(abs(edge) / ENTRY_EDGE, 2.0) / 2.0
        size = max(1.0, round(raw_conv * MAX_POSITION_USD, 2))

        log(f"    -> BUY {side.upper()}: |edge|={abs(edge):.1%}  size=${size:.2f}")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        fair_p = fedwatch_prob if direction == "cut" else 1.0 - fedwatch_prob
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
                reasoning=f"FedWatch arb: {meeting} {explanation}",
                signal_data={"meeting": meeting, "fedwatch_prob": fedwatch_prob,
                             "direction": direction, "edge": round(edge, 4),
                             "market_price": round(price, 4)},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG,
                              thesis=f"FedWatch arb on {meeting}", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi Fed Futures Arb Trader")
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
                # Allow updating FedWatch probs via --set FEDWATCH_KEY=VALUE
                if key.startswith("FEDWATCH_"):
                    meeting_key = key.replace("FEDWATCH_", "").lower()
                    try:
                        FEDWATCH_PROBS[meeting_key] = float(val)
                        safe_print(f"Updated FedWatch: {meeting_key} = {float(val):.1%}")
                    except ValueError:
                        safe_print(f"Invalid value for {key}: {val}")
                elif key in CONFIG_SCHEMA:
                    updates[key] = CONFIG_SCHEMA[key]["type"](val)
        if updates:
            update_config(updates, __file__)
            safe_print(f"Updated config: {updates}")

    dry_run = not args.live
    run_strategy(dry_run, args.positions, args.config, args.quiet)

    if os.environ.get("AUTOMATON_MANAGED") and not _automaton_reported:
        print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                        "skip_reason": "no_signal"}}))
