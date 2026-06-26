#!/usr/bin/env python3
"""
Kalshi Econ Revision Drift Trader

Trades CPI bin markets on Kalshi accounting for the systematic upward revision
bias in CPI initial releases. Historically, CPI initial releases are revised
upward by ~0.03 percentage points. This means markets pricing off the initial
release systematically underprice higher CPI bins.

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
import math
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
    "entry_edge":        {"env": "SIMMER_ECON_REV_ENTRY_EDGE",        "default": 0.08,  "type": float},
    "exit_threshold":    {"env": "SIMMER_ECON_REV_EXIT_THRESHOLD",    "default": 0.45,  "type": float},
    "max_position_usd":  {"env": "SIMMER_ECON_REV_MAX_POSITION_USD",  "default": 5.00,  "type": float},
    "max_trades_per_run":{"env": "SIMMER_ECON_REV_MAX_TRADES_PER_RUN","default": 3,     "type": int},
    "slippage_max":      {"env": "SIMMER_ECON_REV_SLIPPAGE_MAX",      "default": 0.15,  "type": float},
    "min_liquidity":     {"env": "SIMMER_ECON_REV_MIN_LIQUIDITY",     "default": 0.0,   "type": float},
}

_config = load_config(CONFIG_SCHEMA, __file__, slug="kalshi-econ-revision-drift-trader")

# =============================================================================
# Globals
# =============================================================================

_client = None
TRADE_SOURCE = "sdk:kalshi-econ-revision"
SKILL_SLUG = "kalshi-econ-revision-drift-trader"
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
# Revision Drift Model
# =============================================================================

# Historical CPI revision bias (in percentage points)
# BLS CPI initial releases are systematically revised upward by ~0.03 pp
# Source: Analysis of BLS CPI revision history 2000-2024
REVISION_BIAS_PP = 0.03

# Standard deviation of revisions (for uncertainty weighting)
REVISION_STD_PP = 0.05

# Assumed CPI distribution parameters
# Recent CPI YoY has centered around 2.5-3.5% with ~0.4% monthly variation
CPI_MEAN_ESTIMATE = 2.8  # Prior mean CPI YoY
CPI_STD_ESTIMATE = 0.5   # Prior std of CPI YoY

# Keywords for market classification
CPI_KEYWORDS = ["cpi", "inflation", "consumer price"]


def is_cpi_market(question: str) -> bool:
    """Check if a market question is about CPI / inflation."""
    q = question.lower()
    return any(kw in q for kw in CPI_KEYWORDS)


def normal_cdf(x, mu, sigma):
    """CDF of normal distribution."""
    z = (x - mu) / sigma
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))


def compute_bin_prob_initial(lower, upper, mu, sigma):
    """Compute probability for a CPI bin assuming initial release distribution."""
    p_upper = normal_cdf(upper, mu, sigma) if upper < float('inf') else 1.0
    p_lower = normal_cdf(lower, mu, sigma) if lower > float('-inf') else 0.0
    return max(0.0, p_upper - p_lower)


def compute_bin_prob_revised(lower, upper, mu, sigma, revision_bias):
    """Compute probability for a CPI bin accounting for revision drift.

    Since CPI is revised upward by revision_bias, the actual CPI distribution
    is shifted right. This means:
    - Higher CPI bins have more probability than the initial release suggests
    - Lower CPI bins have less probability
    """
    adjusted_mu = mu + revision_bias
    p_upper = normal_cdf(upper, adjusted_mu, sigma) if upper < float('inf') else 1.0
    p_lower = normal_cdf(lower, adjusted_mu, sigma) if lower > float('-inf') else 0.0
    return max(0.0, p_upper - p_lower)


def parse_cpi_bin(question: str) -> tuple:
    """Extract CPI range bin boundaries from market question."""
    q = question.lower().replace(",", "")

    for pat in ["above ", "at least ", "over ", "higher than ", "greater than ", "> "]:
        if pat in q:
            try:
                idx = q.index(pat) + len(pat)
                num_str = ""
                for c in q[idx:]:
                    if c.isdigit() or c == "." or c == "-":
                        num_str += c
                    elif c == "%":
                        break
                    elif num_str:
                        break
                if num_str:
                    return (float(num_str), float('inf'))
            except (ValueError, IndexError):
                pass

    for pat in ["below ", "under ", "less than ", "< "]:
        if pat in q:
            try:
                idx = q.index(pat) + len(pat)
                num_str = ""
                for c in q[idx:]:
                    if c.isdigit() or c == "." or c == "-":
                        num_str += c
                    elif c == "%":
                        break
                    elif num_str:
                        break
                if num_str:
                    return (float('-inf'), float(num_str))
            except (ValueError, IndexError):
                pass

    if "between" in q:
        try:
            parts = q.split("between")[1].split("and")
            if len(parts) == 2:
                lo_str = "".join(c for c in parts[0] if c.isdigit() or c == "." or c == "-")
                hi_str = "".join(c for c in parts[1] if c.isdigit() or c == "." or c == "-")
                if lo_str and hi_str:
                    return (float(lo_str), float(hi_str))
        except (ValueError, IndexError):
            pass

    nums = re.findall(r'(-?\d+\.?\d*)\s*%', q)
    if len(nums) >= 2:
        vals = [float(n) for n in nums]
        return (min(vals), max(vals))
    elif len(nums) == 1:
        val = float(nums[0])
        if any(w in q for w in ["above", "over", "higher", "least", "more"]):
            return (val, float('inf'))
        elif any(w in q for w in ["below", "under", "less", "lower"]):
            return (float('-inf'), val)

    return None


def estimate_cpi_mean_from_bins(bins: list[dict]) -> float:
    """Estimate CPI mean from market bin prices using probability-weighted midpoints."""
    if not bins:
        return CPI_MEAN_ESTIMATE

    weighted_sum = 0.0
    total_weight = 0.0

    for b in bins:
        lo, hi = b["lower"], b["upper"]
        price = b["price"]

        if lo == float('-inf'):
            lo = max(0.0, hi - 1.0)
        if hi == float('inf'):
            hi = lo + 1.0

        midpoint = (lo + hi) / 2.0
        weighted_sum += midpoint * price
        total_weight += price

    if total_weight == 0:
        return CPI_MEAN_ESTIMATE

    return weighted_sum / total_weight


def compute_revision_edge(bins: list[dict], cpi_mean: float) -> list[dict]:
    """Compute edge for each bin by comparing initial vs revision-adjusted probabilities.

    Returns bins with added 'initial_prob', 'revised_prob', and 'edge' fields.
    """
    for b in bins:
        lo, hi = b["lower"], b["upper"]

        # Market is assumed to price based on initial release distribution
        initial_p = compute_bin_prob_initial(lo, hi, cpi_mean, CPI_STD_ESTIMATE)

        # Fair value accounts for upward revision drift
        revised_p = compute_bin_prob_revised(lo, hi, cpi_mean, CPI_STD_ESTIMATE, REVISION_BIAS_PP)

        b["initial_prob"] = initial_p
        b["revised_prob"] = revised_p
        b["revision_edge"] = revised_p - initial_p  # Positive for higher bins

    return bins


# =============================================================================
# Helpers
# =============================================================================

def safe_print(text):
    """Windows-safe print that handles Unicode errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode())


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
    """Discover CPI/inflation markets on Kalshi and auto-import to Simmer."""
    client = get_client()
    imported = 0
    seen = set()

    for term in ["CPI", "inflation"]:
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
            if not is_cpi_market(question):
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


def fetch_cpi_markets():
    """Fetch active CPI / inflation markets from Simmer API."""
    all_markets = []
    for term in ["CPI", "inflation"]:
        try:
            result = get_client()._request(
                "GET", "/api/sdk/markets",
                params={"status": "active", "import_source": "kalshi",
                        "q": term, "limit": 50}
            )
            markets = result.get("markets", [])
            for m in markets:
                if is_cpi_market(m.get("question", "")):
                    all_markets.append(m)
        except Exception as e:
            safe_print(f"  Failed to fetch markets for '{term}': {e}")

    seen = set()
    unique = []
    for m in all_markets:
        mid = m.get("id")
        if mid and mid not in seen:
            seen.add(mid)
            unique.append(m)

    return unique


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
    """Check open revision-drift positions for exit opportunities."""
    positions = get_positions()
    if not positions:
        return 0, 0

    cpi_pos = [p for p in positions
               if TRADE_SOURCE in p.get("sources", [])
               or is_cpi_market(p.get("question") or "")]

    if not cpi_pos:
        return 0, 0

    log(f"\n  Checking {len(cpi_pos)} revision-drift positions for exit...")
    found, executed = 0, 0

    for pos in cpi_pos:
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
    """Run the CPI revision drift trading strategy."""
    global _automaton_reported

    def log(msg, force=False):
        if not quiet or force:
            safe_print(msg)

    log("Econ Revision Drift Trader (CPI)")
    log(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    log(f"  Entry edge: {ENTRY_EDGE:.0%}  Exit threshold: {EXIT_THRESHOLD:.0%}")
    log(f"  Max position: ${MAX_POSITION_USD:.2f}  Max trades/run: {MAX_TRADES_PER_RUN}")
    log(f"  Revision bias: +{REVISION_BIAS_PP:.2f} pp  Revision std: {REVISION_STD_PP:.2f} pp")
    log("")

    if show_config:
        log("Current config:")
        for k, v in _config.items():
            log(f"  {k}: {v}")
        log(f"\nRevision model:")
        log(f"  Bias: +{REVISION_BIAS_PP} pp")
        log(f"  Std: {REVISION_STD_PP} pp")
        log(f"  CPI mean prior: {CPI_MEAN_ESTIMATE}%")
        log(f"  CPI std prior: {CPI_STD_ESTIMATE}%")
        return

    # Init client
    get_client(live=not dry_run)

    # Positions only
    if positions_only:
        positions = get_positions()
        cpi = [p for p in positions if is_cpi_market(p.get("question") or "")]
        if not cpi:
            log("  No revision-drift positions")
        for p in cpi:
            log(f"  {p.get('question', '')[:60]}  price={p.get('current_price', 0):.2f}")
        return

    # --- Discovery ---
    log("Discovering CPI/inflation markets on Kalshi...")
    newly = discover_and_import(log=log)
    if newly:
        log(f"  Imported {newly} new markets")

    # --- Fetch ---
    markets = fetch_cpi_markets()
    log(f"  Found {len(markets)} active CPI/inflation markets")

    if not markets:
        log("  No CPI markets available")
        if os.environ.get("AUTOMATON_MANAGED"):
            _automaton_reported = True
            print(json.dumps({"automaton": {"signals": 0, "trades_executed": 0,
                                            "skip_reason": "no_markets"}}))
        return

    # --- Parse bins ---
    parsed_bins = []
    for m in markets:
        market_id = m.get("id")
        question = m.get("question", "")
        price = m.get("external_price_yes") or m.get("price_yes") or 0

        bin_range = parse_cpi_bin(question)
        if not bin_range:
            log(f"  ? Cannot parse bin: {question[:60]}")
            continue

        lo, hi = bin_range
        parsed_bins.append({
            "market_id": market_id, "question": question,
            "price": price, "lower": lo, "upper": hi,
        })

    if not parsed_bins:
        log("  No parseable CPI bins found")
        return

    # --- Estimate CPI mean from market ---
    cpi_mean = estimate_cpi_mean_from_bins(parsed_bins)
    log(f"\n  Estimated CPI mean (from market): {cpi_mean:.2f}%")
    log(f"  Revision-adjusted mean: {cpi_mean + REVISION_BIAS_PP:.2f}%")
    log("")

    # --- Compute revision edge ---
    bins_with_edge = compute_revision_edge(parsed_bins, cpi_mean)

    # Display model comparison
    log("Revision drift analysis:")
    log(f"  {'Bin':>20}  {'Market':>7}  {'Initial':>8}  {'Revised':>8}  {'Rev Edge':>9}")

    # Sort by revision edge (positive = higher bins benefit from upward revision)
    bins_with_edge.sort(key=lambda b: b["revision_edge"], reverse=True)

    for b in bins_with_edge:
        lo, hi = b["lower"], b["upper"]
        hi_str = f"{hi:.1f}%" if hi < float('inf') else "inf"
        lo_str = f"{lo:.1f}%" if lo > float('-inf') else "-inf"
        bin_label = f"{lo_str}-{hi_str}"
        log(f"  {bin_label:>20}  {b['price']:>6.1%}  {b['initial_prob']:>7.1%}  {b['revised_prob']:>7.1%}  {b['revision_edge']:>+8.1%}")

    log("")

    # --- Trade signals ---
    signals = 0
    trades_executed = 0
    total_usd = 0.0
    skip_reasons = []

    for b in bins_with_edge:
        market_id = b["market_id"]
        question = b["question"]
        mkt_price = b["price"]
        revised_p = b["revised_prob"]
        edge = revised_p - mkt_price  # Total edge = revision edge + market mispricing

        lo, hi = b["lower"], b["upper"]
        hi_str = f"{hi:.1f}%" if hi < float('inf') else "inf"
        lo_str = f"{lo:.1f}%" if lo > float('-inf') else "-inf"

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

        log(f"  SIGNAL: {lo_str}-{hi_str} mkt={mkt_price:.1%} fair={revised_p:.1%} edge={edge:+.1%}")
        log(f"    -> BUY {side.upper()}: |edge|={abs(edge):.1%}  size=${size:.2f}")

        if trades_executed >= MAX_TRADES_PER_RUN:
            log(f"    Skipped: max trades ({MAX_TRADES_PER_RUN}) reached")
            skip_reasons.append("max_trades")
            continue

        # Safeguards
        ctx = get_market_context(market_id, my_probability=revised_p if side == "yes" else 1 - revised_p)
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
                reasoning=f"Revision drift: bin={lo_str}-{hi_str} mkt={mkt_price:.1%} revised={revised_p:.1%} edge={edge:+.1%} bias=+{REVISION_BIAS_PP}pp",
                signal_data={"revised_prob": round(revised_p, 4), "initial_prob": round(b["initial_prob"], 4),
                             "bin_lower": lo if lo > float('-inf') else -99,
                             "bin_upper": hi if hi < float('inf') else 99,
                             "edge": round(edge, 4), "revision_bias": REVISION_BIAS_PP,
                             "cpi_mean_estimate": round(cpi_mean, 4)},
            )
            if result.get("success"):
                trades_executed += 1
                total_usd += size
                tag = "[PAPER] " if result.get("simulated") else ""
                log(f"    {tag}Bought {side.upper()} ${size:.2f}", force=True)
                if result.get("trade_id") and JOURNAL_AVAILABLE and not result.get("simulated"):
                    log_trade(trade_id=result["trade_id"], source=TRADE_SOURCE,
                              skill_slug=SKILL_SLUG, thesis="Revision drift edge on CPI bin", action="buy")
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
    parser = argparse.ArgumentParser(description="Kalshi Econ Revision Drift Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show positions only")
    parser.add_argument("--config", action="store_true", help="Show current config")
    parser.add_argument("--set", action="append", metavar="KEY=VALUE",
                        help="Set config value (e.g., --set entry_edge=0.10)")
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
