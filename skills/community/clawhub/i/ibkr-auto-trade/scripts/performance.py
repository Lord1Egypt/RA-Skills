"""
performance.py — Trade logging, PnL calculation, and self-improvement loop.

Tracks every trade entry/exit, computes rolling stats, and suggests parameter
adjustments to the strategy engine.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
from loguru import logger

from strategy_engine import Signal, StrategyEngine


ROOT = Path(__file__).parent.parent
TRADES_PATH = ROOT / "memory" / "trades.json"
STRATEGIES_PATH = ROOT / "memory" / "strategies.json"
PERFORMANCE_PATH = ROOT / "memory" / "performance.json"


# ── I/O Helpers ───────────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _save_json(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


# ── PerformanceTracker ─────────────────────────────────────────────────────────

class PerformanceTracker:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self._open_trades: dict[str, dict] = {}  # symbol → trade record
        logger.info("PerformanceTracker initialized.")

    # ── Trade Logging ─────────────────────────────────────────────────────────

    def log_trade_open(self, executed_trade, signal: Signal) -> None:
        """Record a newly opened trade."""
        record = {
            "id": str(uuid.uuid4()),
            "symbol": signal.symbol,
            "direction": signal.direction,
            "entry_time": datetime.now(timezone.utc).isoformat(),
            "exit_time": None,
            "entry_price": signal.entry_price,
            "exit_price": None,
            "stop_price": signal.stop_price,
            "quantity": signal.quantity,
            "strategy": signal.strategy,
            "entry_reason": signal.entry_reason,
            "exit_reason": None,
            "indicators": signal.indicators,
            "market_conditions": signal.market_conditions,
            "pnl": None,
            "pnl_pct": None,
            "holding_minutes": None,
            "order_id": executed_trade.order_id,
            "status": "OPEN",
        }
        self._open_trades[signal.symbol] = record
        self._append_trade(record)
        logger.info(f"📝 Trade opened: {signal.symbol} {signal.direction} @ {signal.entry_price}")

    def mark_trade_closed(
        self,
        symbol: str,
        exit_price: Optional[float] = None,
        exit_reason: str = "unknown",
    ) -> None:
        """Update trade record when a position closes."""
        if symbol not in self._open_trades:
            return
        record = self._open_trades.pop(symbol)

        exit_time = datetime.now(timezone.utc)
        entry_time = datetime.fromisoformat(record["entry_time"])
        holding_minutes = int((exit_time - entry_time).total_seconds() / 60)

        # If exit_price not provided, use entry as fallback (rare)
        ep = exit_price if exit_price is not None else record["entry_price"]
        qty = record["quantity"]
        if record["direction"] == "LONG":
            pnl = (ep - record["entry_price"]) * qty
        else:
            pnl = (record["entry_price"] - ep) * qty
        pnl_pct = pnl / (record["entry_price"] * qty) * 100

        record.update({
            "exit_time": exit_time.isoformat(),
            "exit_price": ep,
            "exit_reason": exit_reason,
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl_pct, 4),
            "holding_minutes": holding_minutes,
            "status": "CLOSED",
        })
        self._update_trade(record)
        logger.info(
            f"📝 Trade closed: {symbol} | PnL=${pnl:.2f} ({pnl_pct:.2f}%) | "
            f"reason={exit_reason} | held={holding_minutes}m"
        )

    def _append_trade(self, record: dict) -> None:
        data = _load_json(TRADES_PATH)
        data["trades"].append(record)
        _save_json(TRADES_PATH, data)

    def _update_trade(self, record: dict) -> None:
        data = _load_json(TRADES_PATH)
        for i, t in enumerate(data["trades"]):
            if t["id"] == record["id"]:
                data["trades"][i] = record
                break
        _save_json(TRADES_PATH, data)

    # ── Performance Evaluation ─────────────────────────────────────────────────

    def evaluate_performance(self) -> dict:
        """Compute win rate, Sharpe, drawdown, profit factor from closed trades."""
        data = _load_json(TRADES_PATH)
        closed = [t for t in data["trades"] if t["status"] == "CLOSED" and t["pnl"] is not None]

        if len(closed) < 3:
            logger.info("Not enough closed trades to evaluate.")
            return {}

        pnls = [t["pnl"] for t in closed]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p <= 0]

        win_rate = len(wins) / len(pnls)
        total_pnl = sum(pnls)
        avg_win = np.mean(wins) if wins else 0
        avg_loss = abs(np.mean(losses)) if losses else 1
        profit_factor = (sum(wins) / abs(sum(losses))) if losses else float("inf")

        returns = np.array(pnls)
        sharpe = (np.mean(returns) / np.std(returns) * np.sqrt(252)) if np.std(returns) > 0 else 0

        # Max drawdown
        cumulative = np.cumsum(pnls)
        peak = np.maximum.accumulate(cumulative)
        drawdown = peak - cumulative
        max_dd = float(np.max(drawdown))

        hold_times = [t["holding_minutes"] for t in closed if t["holding_minutes"] is not None]
        avg_hold = np.mean(hold_times) if hold_times else 0

        stats = {
            "total_trades": len(pnls),
            "win_rate": round(win_rate, 4),
            "total_pnl": round(total_pnl, 2),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "profit_factor": round(profit_factor, 4),
            "sharpe_ratio": round(sharpe, 4),
            "max_drawdown": round(max_dd, 2),
            "avg_holding_minutes": round(avg_hold, 1),
        }

        # Persist
        perf_data = _load_json(PERFORMANCE_PATH)
        perf_data["last_evaluated"] = datetime.now(timezone.utc).isoformat()
        perf_data["all_time"].update(stats)
        _save_json(PERFORMANCE_PATH, perf_data)

        logger.info(f"📊 Performance: {stats}")
        return stats

    # ── Self-Improvement ───────────────────────────────────────────────────────

    def suggest_improvements(self, stats: dict) -> list[dict]:
        """
        Rule-based parameter recommendations based on performance stats.
        Returns a list of {strategy, param, old, new, reason}.
        """
        if not stats:
            return []

        recommendations = []
        strat_data = _load_json(STRATEGIES_PATH)
        current_params = strat_data["versions"][-1]["params"]

        win_rate = stats.get("win_rate", 0)
        sharpe = stats.get("sharpe_ratio", 0)
        profit_factor = stats.get("profit_factor", 1)

        # RSI: if win rate low, tighten signal thresholds
        rsi_params = current_params.get("rsi_mean_reversion", {})
        if win_rate < 0.45 and rsi_params:
            new_oversold = max(20, rsi_params["oversold"] - 5)
            new_overbought = min(80, rsi_params["overbought"] + 5)
            if new_oversold != rsi_params["oversold"]:
                recommendations.append({
                    "strategy": "rsi_mean_reversion",
                    "param": "oversold",
                    "old": rsi_params["oversold"],
                    "new": new_oversold,
                    "reason": f"Win rate {win_rate:.0%} — tightening RSI thresholds",
                })
                recommendations.append({
                    "strategy": "rsi_mean_reversion",
                    "param": "overbought",
                    "old": rsi_params["overbought"],
                    "new": new_overbought,
                    "reason": f"Win rate {win_rate:.0%} — tightening RSI thresholds",
                })

        # MACD: if low profit factor, raise minimum histogram size
        macd_params = current_params.get("macd_momentum", {})
        if profit_factor < 1.2 and macd_params:
            new_min_hist = round(macd_params["min_histogram"] * 1.25, 4)
            recommendations.append({
                "strategy": "macd_momentum",
                "param": "min_histogram",
                "old": macd_params["min_histogram"],
                "new": new_min_hist,
                "reason": f"Profit factor {profit_factor:.2f} — raising MACD signal filter",
            })

        if recommendations:
            logger.info(f"💡 {len(recommendations)} improvement(s) suggested.")
        return recommendations

    def apply_improvements(self, recommendations: list[dict], strategy_engine: StrategyEngine) -> None:
        """Apply parameter recommendations and save a new strategy version."""
        if not recommendations:
            return

        strat_data = _load_json(STRATEGIES_PATH)
        current = strat_data["versions"][-1]["params"]

        # Apply changes
        for rec in recommendations:
            strat = rec["strategy"]
            param = rec["param"]
            if strat in current:
                current[strat][param] = rec["new"]
                logger.info(
                    f"🔧 {strat}.{param}: {rec['old']} → {rec['new']} ({rec['reason']})"
                )

        # Save new version
        new_version = strat_data["current_version"] + 1
        strat_data["current_version"] = new_version
        strat_data["versions"].append({
            "version": new_version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "self_improvement",
            "params": current,
            "recommendations": recommendations,
        })
        _save_json(STRATEGIES_PATH, strat_data)

        # Push to live strategy engine
        for strat_name, params in current.items():
            strategy_engine.update_params(strat_name, params)

        # Log to improvement_log
        perf_data = _load_json(PERFORMANCE_PATH)
        perf_data["improvement_log"].append({
            "version": new_version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "changes": recommendations,
        })
        _save_json(PERFORMANCE_PATH, perf_data)

        logger.info(f"✅ Strategy params updated to version {new_version}.")
