#!/usr/bin/env python3
"""
polymarket_optimizer.py — Polymarket Strategy Optimizer
Part of Wesley Agent Ecosystem | v1.0.0

Reads performance_metrics.json from polymarket_executor.py
Analyzes win rates, ROI, drawdowns per strategy
Adjusts learned_config.json to improve future performance
Runs every 6 hours via OpenClaw cron job

Architecture mirrors crypto-executor-optimizer pattern.
Author: Georges Andronescu (Wesley Armando)
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
WORKSPACE = os.environ.get("WORKSPACE", "/data/.openclaw/workspace")
METRICS_FILE = os.path.join(WORKSPACE, "performance_metrics.json")
CONFIG_FILE = os.path.join(WORKSPACE, "learned_config.json")
PORTFOLIO_FILE = os.path.join(WORKSPACE, "portfolio.json")
PAPER_TRADES_FILE = os.path.join(WORKSPACE, "paper_trades.json")
LIVE_TRADES_FILE = os.path.join(WORKSPACE, "live_trades.jsonl")
OPTIMIZER_LOG_FILE = os.path.join(WORKSPACE, "optimizer_log.jsonl")

# Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ─────────────────────────────────────────────
# DEFAULT CONFIG (baseline for optimizer)
# ─────────────────────────────────────────────
DEFAULT_CONFIG = {
    "version": "1.0.0",
    "last_optimized": None,
    "optimization_count": 0,

    # Strategy enable/disable
    "strategies": {
        "parity_arbitrage": True,
        "tail_end": True,
        "logical_arbitrage": True,
        "market_making": False,      # Needs proxy for VPS
        "latency_arbitrage": False   # Needs WebSocket feed
    },

    # Thresholds
    "min_edge_pct": 0.02,           # 2% minimum edge
    "min_tail_end_certainty": 0.95, # 95% certainty for tail-end
    "min_parity_profit": 0.02,      # 2% minimum parity profit
    "min_logical_edge": 0.05,       # 5% for logical arb

    # Position sizing
    "kelly_fraction": 0.25,         # Conservative Kelly (25%)
    "max_position_pct": 0.10,       # Max 10% of capital per trade
    "max_concurrent_trades": 3,     # Max simultaneous open positions

    # Risk management
    "circuit_breaker_pct": -0.15,   # -15% daily loss halts trading
    "stop_loss_pct": -0.50,         # -50% per position stop-loss
    "max_daily_trades": 20,         # Cap trades per day

    # Scan settings
    "scan_interval_seconds": 300,   # 5 minutes between scans
    "max_markets_to_scan": 500,     # Markets per scan cycle
    "scan_workers": 50,             # Parallel workers

    # Capital allocation per strategy (% of available capital)
    "strategy_allocation": {
        "parity_arbitrage": 0.30,
        "tail_end": 0.50,
        "logical_arbitrage": 0.20,
        "market_making": 0.00,
        "latency_arbitrage": 0.00
    }
}

# ─────────────────────────────────────────────
# OPTIMIZER THRESHOLDS
# ─────────────────────────────────────────────
# If a strategy's win rate drops below this → tighten thresholds
WIN_RATE_FLOOR = 0.50        # Below 50% → reduce aggressiveness
WIN_RATE_TARGET = 0.65       # Above 65% → can loosen thresholds
WIN_RATE_EXCELLENT = 0.80    # Above 80% → increase allocation

# Minimum trades before optimizer acts on a strategy
MIN_TRADES_TO_OPTIMIZE = 5

# Max single-step adjustments (prevent overcorrection)
MAX_THRESHOLD_STEP = 0.005   # 0.5% max change per cycle
MAX_KELLY_STEP = 0.05        # 5% max Kelly change
MAX_ALLOCATION_STEP = 0.10   # 10% max allocation change


# ─────────────────────────────────────────────
# TELEGRAM NOTIFIER
# ─────────────────────────────────────────────
def send_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }).encode()
        req = urllib.request.Request(url, data, {"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[TELEGRAM] Error: {e}")


# ─────────────────────────────────────────────
# FILE HELPERS
# ─────────────────────────────────────────────
def load_json(path: str, default=None):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}


def save_json(path: str, data: dict):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[SAVE] {path}")


def load_jsonl(path: str) -> list:
    """Load all records from a .jsonl file."""
    records = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    return records


def log_optimizer_run(summary: dict):
    """Append optimizer run summary to log file."""
    os.makedirs(os.path.dirname(OPTIMIZER_LOG_FILE), exist_ok=True)
    with open(OPTIMIZER_LOG_FILE, "a") as f:
        f.write(json.dumps(summary) + "\n")


# ─────────────────────────────────────────────
# METRICS ANALYSIS
# ─────────────────────────────────────────────
def analyze_metrics(metrics: dict) -> dict:
    """
    Analyze performance_metrics.json from polymarket_executor.
    Returns per-strategy analysis dict.
    """
    analysis = {}

    strategies = metrics.get("strategies", {})
    for strategy_name, stats in strategies.items():
        total = stats.get("total_trades", 0)
        wins = stats.get("wins", 0)
        losses = stats.get("losses", 0)
        total_pnl = stats.get("total_pnl", 0.0)
        avg_profit = stats.get("avg_profit_pct", 0.0)
        avg_loss = stats.get("avg_loss_pct", 0.0)

        win_rate = wins / total if total > 0 else 0.0
        profit_factor = abs(total_pnl / (avg_loss * losses)) if (losses > 0 and avg_loss != 0) else 0.0

        analysis[strategy_name] = {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "total_pnl": total_pnl,
            "avg_profit_pct": avg_profit,
            "avg_loss_pct": avg_loss,
            "profit_factor": profit_factor,
            "has_enough_data": total >= MIN_TRADES_TO_OPTIMIZE,
            "status": _classify_performance(win_rate, total_pnl, total)
        }

    return analysis


def _classify_performance(win_rate: float, total_pnl: float, total_trades: int) -> str:
    """Classify strategy performance."""
    if total_trades < MIN_TRADES_TO_OPTIMIZE:
        return "insufficient_data"
    if total_pnl < 0 and win_rate < WIN_RATE_FLOOR:
        return "poor"
    if win_rate < WIN_RATE_FLOOR:
        return "underperforming"
    if win_rate >= WIN_RATE_EXCELLENT and total_pnl > 0:
        return "excellent"
    if win_rate >= WIN_RATE_TARGET and total_pnl > 0:
        return "good"
    return "average"


def analyze_portfolio(portfolio: dict) -> dict:
    """Analyze overall portfolio health."""
    capital = portfolio.get("current_capital", 100.0)
    initial = portfolio.get("initial_capital", 100.0)
    daily_pnl = portfolio.get("daily_pnl", 0.0)
    total_trades = portfolio.get("total_trades", 0)
    winning_trades = portfolio.get("winning_trades", 0)
    circuit_breaker = portfolio.get("circuit_breaker_active", False)

    overall_return_pct = ((capital - initial) / initial) * 100 if initial > 0 else 0.0
    overall_win_rate = winning_trades / total_trades if total_trades > 0 else 0.0
    daily_return_pct = (daily_pnl / initial) * 100 if initial > 0 else 0.0

    return {
        "current_capital": capital,
        "initial_capital": initial,
        "overall_return_pct": overall_return_pct,
        "overall_win_rate": overall_win_rate,
        "daily_return_pct": daily_return_pct,
        "total_trades": total_trades,
        "circuit_breaker_active": circuit_breaker,
        "health": _classify_portfolio_health(overall_return_pct, overall_win_rate, circuit_breaker)
    }


def _classify_portfolio_health(return_pct: float, win_rate: float, circuit_breaker: bool) -> str:
    if circuit_breaker:
        return "circuit_breaker_active"
    if return_pct < -10:
        return "critical"
    if return_pct < -5:
        return "warning"
    if return_pct >= 10 and win_rate >= 0.65:
        return "excellent"
    if return_pct >= 0 and win_rate >= 0.55:
        return "healthy"
    return "neutral"


# ─────────────────────────────────────────────
# OPTIMIZATION ENGINE
# ─────────────────────────────────────────────
def optimize_config(current_config: dict, analysis: dict, portfolio_health: dict) -> tuple:
    """
    Core optimizer logic.
    Returns (new_config, list_of_changes_made)
    """
    config = json.loads(json.dumps(current_config))  # deep copy
    changes = []

    port_health = portfolio_health.get("health", "neutral")

    # ── GLOBAL RISK ADJUSTMENT ──────────────────
    # If portfolio is in trouble → go defensive
    if port_health == "critical":
        old_kelly = config.get("kelly_fraction", 0.25)
        new_kelly = max(0.10, old_kelly - MAX_KELLY_STEP)
        if new_kelly != old_kelly:
            config["kelly_fraction"] = new_kelly
            changes.append(f"⚠️ Portfolio critical → Kelly fraction {old_kelly:.2f} → {new_kelly:.2f}")

        old_max = config.get("max_position_pct", 0.10)
        new_max = max(0.05, old_max - 0.02)
        if new_max != old_max:
            config["max_position_pct"] = new_max
            changes.append(f"⚠️ Portfolio critical → Max position {old_max:.0%} → {new_max:.0%}")

    # If portfolio is excellent → can be slightly more aggressive
    elif port_health == "excellent":
        old_kelly = config.get("kelly_fraction", 0.25)
        new_kelly = min(0.40, old_kelly + MAX_KELLY_STEP)
        if new_kelly != old_kelly:
            config["kelly_fraction"] = new_kelly
            changes.append(f"✅ Portfolio excellent → Kelly fraction {old_kelly:.2f} → {new_kelly:.2f}")

    # ── PER-STRATEGY ADJUSTMENTS ─────────────────
    allocations = config.get("strategy_allocation", DEFAULT_CONFIG["strategy_allocation"].copy())
    total_alloc = sum(allocations.values())

    for strategy, stats in analysis.items():
        if not stats["has_enough_data"]:
            continue

        status = stats["status"]
        win_rate = stats["win_rate"]

        # ── PARITY ARBITRAGE ───────────────────
        if strategy == "parity_arbitrage":
            if status == "poor":
                # Raise minimum profit threshold — only trade better opportunities
                old_val = config.get("min_parity_profit", 0.02)
                new_val = min(0.05, old_val + MAX_THRESHOLD_STEP)
                config["min_parity_profit"] = new_val
                changes.append(f"📈 parity_arb underperforming → min_profit {old_val:.3f} → {new_val:.3f}")
                # Reduce allocation
                old_alloc = allocations.get("parity_arbitrage", 0.30)
                allocations["parity_arbitrage"] = max(0.10, old_alloc - MAX_ALLOCATION_STEP)
                changes.append(f"📉 parity_arb allocation {old_alloc:.0%} → {allocations['parity_arbitrage']:.0%}")

            elif status == "excellent":
                # Lower threshold — capture more opportunities
                old_val = config.get("min_parity_profit", 0.02)
                new_val = max(0.015, old_val - MAX_THRESHOLD_STEP)
                config["min_parity_profit"] = new_val
                changes.append(f"🚀 parity_arb excellent → min_profit {old_val:.3f} → {new_val:.3f}")
                # Increase allocation
                old_alloc = allocations.get("parity_arbitrage", 0.30)
                allocations["parity_arbitrage"] = min(0.50, old_alloc + MAX_ALLOCATION_STEP)
                changes.append(f"📈 parity_arb allocation {old_alloc:.0%} → {allocations['parity_arbitrage']:.0%}")

        # ── TAIL END TRADING ───────────────────
        elif strategy == "tail_end":
            if status == "poor":
                # Raise certainty bar — only the most certain outcomes
                old_val = config.get("min_tail_end_certainty", 0.95)
                new_val = min(0.99, old_val + MAX_THRESHOLD_STEP)
                config["min_tail_end_certainty"] = new_val
                changes.append(f"📈 tail_end underperforming → min_certainty {old_val:.3f} → {new_val:.3f}")
                old_alloc = allocations.get("tail_end", 0.50)
                allocations["tail_end"] = max(0.20, old_alloc - MAX_ALLOCATION_STEP)
                changes.append(f"📉 tail_end allocation {old_alloc:.0%} → {allocations['tail_end']:.0%}")

            elif status == "excellent":
                # Can lower certainty slightly — more volume
                old_val = config.get("min_tail_end_certainty", 0.95)
                new_val = max(0.90, old_val - MAX_THRESHOLD_STEP)
                config["min_tail_end_certainty"] = new_val
                changes.append(f"🚀 tail_end excellent → min_certainty {old_val:.3f} → {new_val:.3f}")
                old_alloc = allocations.get("tail_end", 0.50)
                allocations["tail_end"] = min(0.70, old_alloc + MAX_ALLOCATION_STEP)
                changes.append(f"📈 tail_end allocation {old_alloc:.0%} → {allocations['tail_end']:.0%}")

        # ── LOGICAL ARBITRAGE ──────────────────
        elif strategy == "logical_arbitrage":
            if status == "poor":
                old_val = config.get("min_logical_edge", 0.05)
                new_val = min(0.10, old_val + MAX_THRESHOLD_STEP)
                config["min_logical_edge"] = new_val
                changes.append(f"📈 logical_arb underperforming → min_edge {old_val:.3f} → {new_val:.3f}")
                old_alloc = allocations.get("logical_arbitrage", 0.20)
                allocations["logical_arbitrage"] = max(0.05, old_alloc - MAX_ALLOCATION_STEP)
                changes.append(f"📉 logical_arb allocation {old_alloc:.0%} → {allocations['logical_arbitrage']:.0%}")

            elif status == "excellent":
                old_val = config.get("min_logical_edge", 0.05)
                new_val = max(0.03, old_val - MAX_THRESHOLD_STEP)
                config["min_logical_edge"] = new_val
                changes.append(f"🚀 logical_arb excellent → min_edge {old_val:.3f} → {new_val:.3f}")
                old_alloc = allocations.get("logical_arbitrage", 0.20)
                allocations["logical_arbitrage"] = min(0.40, old_alloc + MAX_ALLOCATION_STEP)
                changes.append(f"📈 logical_arb allocation {old_alloc:.0%} → {allocations['logical_arbitrage']:.0%}")

    # ── NORMALIZE ALLOCATIONS ──────────────────
    # Ensure strategy allocations sum to 1.0
    enabled_strategies = [s for s, enabled in config.get("strategies", {}).items() if enabled]
    total = sum(allocations.get(s, 0) for s in enabled_strategies)
    if total > 0 and abs(total - 1.0) > 0.01:
        for s in enabled_strategies:
            if s in allocations:
                allocations[s] = round(allocations[s] / total, 3)
        changes.append(f"⚖️ Allocations renormalized (sum was {total:.2f})")

    config["strategy_allocation"] = allocations

    # ── SCAN FREQUENCY ADJUSTMENT ──────────────
    # If win rate is high and many opportunities → scan faster
    overall_win_rate = portfolio_health.get("overall_win_rate", 0.0)
    total_trades = portfolio_health.get("total_trades", 0)

    if overall_win_rate >= WIN_RATE_EXCELLENT and total_trades > 20:
        old_interval = config.get("scan_interval_seconds", 300)
        new_interval = max(120, old_interval - 30)
        if new_interval != old_interval:
            config["scan_interval_seconds"] = new_interval
            changes.append(f"⚡ High win rate → scan interval {old_interval}s → {new_interval}s")

    elif port_health in ("critical", "warning"):
        old_interval = config.get("scan_interval_seconds", 300)
        new_interval = min(600, old_interval + 60)
        if new_interval != old_interval:
            config["scan_interval_seconds"] = new_interval
            changes.append(f"🐢 Portfolio struggling → scan interval {old_interval}s → {new_interval}s")

    # ── UPDATE METADATA ────────────────────────
    config["last_optimized"] = datetime.utcnow().isoformat()
    config["optimization_count"] = current_config.get("optimization_count", 0) + 1

    return config, changes


# ─────────────────────────────────────────────
# PAPER TRADE ANALYSIS
# ─────────────────────────────────────────────
def analyze_paper_trades(paper_trades: list) -> dict:
    """
    Analyze paper trades to extract per-strategy performance.
    Builds metrics compatible with performance_metrics.json format.
    """
    strategy_stats = {}

    for trade in paper_trades:
        strategy = trade.get("strategy", "unknown")
        status = trade.get("status", "open")
        pnl = trade.get("actual_pnl", 0.0)
        win_prob = trade.get("win_probability", 0.5)

        if strategy not in strategy_stats:
            strategy_stats[strategy] = {
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "total_pnl": 0.0,
                "profits": [],
                "losses_list": []
            }

        if status in ("won", "lost", "closed"):
            strategy_stats[strategy]["total_trades"] += 1
            strategy_stats[strategy]["total_pnl"] += pnl
            if pnl > 0:
                strategy_stats[strategy]["wins"] += 1
                strategy_stats[strategy]["profits"].append(pnl)
            else:
                strategy_stats[strategy]["losses"] += 1
                strategy_stats[strategy]["losses_list"].append(pnl)

    # Compute averages
    result = {"strategies": {}}
    for strategy, stats in strategy_stats.items():
        profits = stats.get("profits", [])
        losses_list = stats.get("losses_list", [])
        result["strategies"][strategy] = {
            "total_trades": stats["total_trades"],
            "wins": stats["wins"],
            "losses": stats["losses"],
            "total_pnl": round(stats["total_pnl"], 4),
            "avg_profit_pct": round(sum(profits) / len(profits), 4) if profits else 0.0,
            "avg_loss_pct": round(sum(losses_list) / len(losses_list), 4) if losses_list else 0.0
        }

    return result


# ─────────────────────────────────────────────
# READINESS ASSESSMENT
# ─────────────────────────────────────────────
def assess_live_readiness(paper_trades: list, portfolio: dict) -> dict:
    """
    Assess whether paper trading results justify going live.
    Returns readiness report.
    """
    total_resolved = sum(
        1 for t in paper_trades
        if t.get("status") in ("won", "lost", "closed")
    )
    wins = sum(1 for t in paper_trades if t.get("actual_pnl", 0) > 0 and t.get("status") in ("won", "lost", "closed"))
    win_rate = wins / total_resolved if total_resolved > 0 else 0.0
    total_pnl = sum(t.get("actual_pnl", 0) for t in paper_trades if t.get("status") in ("won", "lost", "closed"))
    capital = portfolio.get("current_capital", 100.0)
    initial = portfolio.get("initial_capital", 100.0)
    return_pct = ((capital - initial) / initial) * 100 if initial > 0 else 0.0

    # Readiness criteria
    enough_trades = total_resolved >= 30
    good_win_rate = win_rate >= 0.55
    positive_pnl = total_pnl > 0
    no_circuit_breaker = not portfolio.get("circuit_breaker_active", False)

    ready = all([enough_trades, good_win_rate, positive_pnl, no_circuit_breaker])

    return {
        "ready_for_live": ready,
        "total_resolved_trades": total_resolved,
        "win_rate": round(win_rate, 3),
        "total_paper_pnl": round(total_pnl, 2),
        "return_pct": round(return_pct, 2),
        "criteria": {
            "enough_trades_30+": enough_trades,
            "win_rate_55%+": good_win_rate,
            "positive_pnl": positive_pnl,
            "no_circuit_breaker": no_circuit_breaker
        },
        "missing": [k for k, v in {
            "Need 30+ resolved trades": enough_trades,
            "Win rate must be 55%+": good_win_rate,
            "Need positive total P&L": positive_pnl,
            "Circuit breaker must be off": no_circuit_breaker
        }.items() if not v]
    }


# ─────────────────────────────────────────────
# TELEGRAM REPORT
# ─────────────────────────────────────────────
def build_telegram_report(
    analysis: dict,
    portfolio_health: dict,
    changes: list,
    readiness: dict,
    config: dict
) -> str:
    lines = []
    lines.append("🧠 <b>POLYMARKET OPTIMIZER REPORT</b>")
    lines.append(f"🕐 {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC")
    lines.append(f"🔄 Optimization #{config.get('optimization_count', 1)}")
    lines.append("")

    # Portfolio health
    health = portfolio_health.get("health", "unknown")
    health_emoji = {
        "excellent": "🟢", "healthy": "🟡", "neutral": "⚪",
        "warning": "🟠", "critical": "🔴", "circuit_breaker_active": "🚨"
    }.get(health, "⚪")
    lines.append(f"<b>Portfolio Health:</b> {health_emoji} {health.upper()}")
    lines.append(f"💰 Capital: ${portfolio_health.get('current_capital', 0):.2f}")
    lines.append(f"📈 Return: {portfolio_health.get('overall_return_pct', 0):.1f}%")
    lines.append(f"🎯 Win Rate: {portfolio_health.get('overall_win_rate', 0):.1%}")
    lines.append(f"📊 Total Trades: {portfolio_health.get('total_trades', 0)}")
    lines.append("")

    # Strategy performance
    lines.append("<b>Strategy Performance:</b>")
    for strategy, stats in analysis.items():
        if stats["total_trades"] == 0:
            continue
        status_emoji = {
            "excellent": "🚀", "good": "✅", "average": "⚪",
            "underperforming": "⚠️", "poor": "❌", "insufficient_data": "🔍"
        }.get(stats["status"], "⚪")
        lines.append(
            f"  {status_emoji} {strategy}: {stats['win_rate']:.1%} WR "
            f"| {stats['total_trades']} trades "
            f"| P&L: {stats['total_pnl']:+.3f}"
        )
    lines.append("")

    # Changes made
    if changes:
        lines.append("<b>Adjustments Made:</b>")
        for change in changes[:8]:  # Max 8 to keep message clean
            lines.append(f"  {change}")
    else:
        lines.append("✅ <b>No adjustments needed</b> — config is optimal")
    lines.append("")

    # Live readiness
    lines.append("<b>Live Trading Readiness:</b>")
    if readiness["ready_for_live"]:
        lines.append("🟢 READY FOR LIVE TRADING")
        lines.append(f"  ✅ {readiness['total_resolved_trades']} resolved trades")
        lines.append(f"  ✅ {readiness['win_rate']:.1%} win rate")
        lines.append(f"  ✅ P&L: +${readiness['total_paper_pnl']:.2f}")
    else:
        lines.append("🔴 NOT YET READY — Criteria missing:")
        for missing in readiness.get("missing", []):
            lines.append(f"  ❌ {missing}")
        lines.append(f"  📊 Progress: {readiness['total_resolved_trades']}/30 trades")
        lines.append(f"  🎯 Win rate: {readiness['win_rate']:.1%} (need 55%+)")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("POLYMARKET OPTIMIZER v1.0.0")
    print(f"Run time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 60)

    # ── STEP 1: Load current config ─────────────
    current_config = load_json(CONFIG_FILE, DEFAULT_CONFIG.copy())
    print(f"[CONFIG] Loaded. Optimization #{current_config.get('optimization_count', 0) + 1}")

    # ── STEP 2: Load portfolio ──────────────────
    portfolio = load_json(PORTFOLIO_FILE, {})
    portfolio_health = analyze_portfolio(portfolio)
    print(f"[PORTFOLIO] Health: {portfolio_health['health'].upper()}")
    print(f"[PORTFOLIO] Capital: ${portfolio_health['current_capital']:.2f} | Return: {portfolio_health['overall_return_pct']:.1f}%")

    # ── STEP 3: Load performance metrics ────────
    metrics = load_json(METRICS_FILE, {})

    # If no metrics yet, try to build from paper trades
    if not metrics.get("strategies"):
        print("[METRICS] No metrics file — building from paper trades...")
        paper_trades = load_json(PAPER_TRADES_FILE, [])
        if paper_trades:
            metrics = analyze_paper_trades(paper_trades)
            save_json(METRICS_FILE, metrics)
            print(f"[METRICS] Built from {len(paper_trades)} paper trades")
        else:
            print("[METRICS] No paper trades yet — optimizer will run but cannot adjust strategies")
            metrics = {"strategies": {}}

    # ── STEP 4: Analyze performance ─────────────
    analysis = analyze_metrics(metrics)
    for strategy, stats in analysis.items():
        if stats["total_trades"] > 0:
            print(
                f"[ANALYSIS] {strategy}: {stats['status'].upper()} | "
                f"WR={stats['win_rate']:.1%} | "
                f"Trades={stats['total_trades']} | "
                f"P&L={stats['total_pnl']:+.3f}"
            )

    # ── STEP 5: Optimize config ──────────────────
    new_config, changes = optimize_config(current_config, analysis, portfolio_health)

    if changes:
        print(f"[OPTIMIZER] {len(changes)} adjustments made:")
        for change in changes:
            print(f"  {change}")
        save_json(CONFIG_FILE, new_config)
        print("[OPTIMIZER] Config saved.")
    else:
        print("[OPTIMIZER] No adjustments needed — config is optimal.")
        # Still update timestamp
        new_config["last_optimized"] = datetime.utcnow().isoformat()
        new_config["optimization_count"] = current_config.get("optimization_count", 0) + 1
        save_json(CONFIG_FILE, new_config)

    # ── STEP 6: Assess live readiness ───────────
    paper_trades = load_json(PAPER_TRADES_FILE, [])
    readiness = assess_live_readiness(paper_trades, portfolio)
    print(f"[READINESS] Ready for live: {readiness['ready_for_live']}")
    print(f"[READINESS] Resolved trades: {readiness['total_resolved_trades']}/30")
    print(f"[READINESS] Win rate: {readiness['win_rate']:.1%} (need 55%+)")
    if readiness["missing"]:
        print(f"[READINESS] Missing: {', '.join(readiness['missing'])}")

    # ── STEP 7: Log run ─────────────────────────
    run_summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "optimization_count": new_config.get("optimization_count"),
        "portfolio_health": portfolio_health["health"],
        "overall_return_pct": portfolio_health["overall_return_pct"],
        "changes_count": len(changes),
        "changes": changes,
        "ready_for_live": readiness["ready_for_live"],
        "win_rate": readiness["win_rate"],
        "resolved_trades": readiness["total_resolved_trades"]
    }
    log_optimizer_run(run_summary)
    print(f"[LOG] Run logged to {OPTIMIZER_LOG_FILE}")

    # ── STEP 8: Telegram report ──────────────────
    report = build_telegram_report(analysis, portfolio_health, changes, readiness, new_config)
    send_telegram(report)
    print("[TELEGRAM] Report sent.")

    print("=" * 60)
    print("OPTIMIZER COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
