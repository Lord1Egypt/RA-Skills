#!/usr/bin/env python3
"""
Update performance metrics in state.json based on latest trade review.
Applies learning adaptations within config-allowed boundaries.

Input (stdin JSON):
  {
    "metrics": {...},   ← current metrics from state.json
    "review": {...},    ← output from review_trades.py
    "config": {...}     ← optional: config bounds to enforce
  }
Output: updated metrics dict to be written back to state.json
"""
import json
import sys
from datetime import datetime, timezone


def main() -> int:
    payload = json.load(sys.stdin)
    metrics = payload.get("metrics", {})
    review = payload.get("review", {})
    config = payload.get("config", {})
    ts = datetime.now(timezone.utc).isoformat()

    # Update review stats
    metrics["last_review_ts"] = ts
    metrics["last_review_trade_count"] = review.get("trade_count", 0)
    metrics["last_review_outcomes"] = review.get("outcomes", {})
    metrics["win_rate"] = review.get("win_rate", metrics.get("win_rate", 0.0))
    metrics["avg_pnl"] = review.get("avg_pnl", metrics.get("avg_pnl", 0.0))
    metrics["total_pnl"] = review.get("total_pnl", metrics.get("total_pnl", 0.0))
    metrics["max_loss_streak"] = review.get("max_loss_streak", metrics.get("max_loss_streak", 0))
    metrics["high_conf_win_rate"] = review.get("high_conf_win_rate", metrics.get("high_conf_win_rate", 0.0))
    metrics["lessons"] = review.get("lessons", [])

    # ── Learning adaptations (safe, bounded) ──
    max_lev = float(config.get("max_leverage", metrics.get("max_leverage_cap", 20.0)))
    min_lev = float(config.get("min_leverage", 1.0))

    # Reduce confidence multiplier after loss streaks
    streak = review.get("max_loss_streak", 0)
    current_conf_multiplier = float(metrics.get("confidence_multiplier", 1.0))
    if streak >= 4:
        new_mult = max(0.7, current_conf_multiplier - 0.1)
        metrics["confidence_multiplier"] = new_mult
        metrics["leverage_reduction_active"] = True
    elif streak <= 1 and review.get("win_rate", 0) >= 0.55:
        new_mult = min(1.0, current_conf_multiplier + 0.05)
        metrics["confidence_multiplier"] = new_mult
        metrics["leverage_reduction_active"] = False
    else:
        metrics.setdefault("confidence_multiplier", 1.0)

    # Adjust effective leverage cap based on performance (never above config max)
    eff_lev_cap = float(metrics.get("effective_leverage_cap", max_lev))
    win_rate = review.get("win_rate", 0.5)
    if streak >= 3 or win_rate < 0.35:
        # Reduce effective leverage cap by 1 step, floor at min_lev
        eff_lev_cap = max(min_lev, eff_lev_cap - 1.0)
    elif win_rate >= 0.60 and streak == 0 and review.get("closed_count", 0) >= 5:
        # Recover up towards config max
        eff_lev_cap = min(max_lev, eff_lev_cap + 0.5)
    metrics["effective_leverage_cap"] = eff_lev_cap

    # Flag underperforming symbols (dynamically scaled to 10% of max daily loss or $100)
    threshold = -float(config.get("max_daily_loss", 100)) * 0.5
    pnl_by_sym = review.get("pnl_by_symbol", {})
    underperforming = [s for s, pnl in pnl_by_sym.items() if pnl < threshold]
    if underperforming:
        metrics["underperforming_symbols"] = underperforming
    elif "underperforming_symbols" in metrics:
        del metrics["underperforming_symbols"]

    # High-confidence threshold adaptation
    if review.get("high_conf_win_rate", 0) > win_rate + 0.1:
        metrics["recommended_min_confidence"] = min(0.75, float(metrics.get("recommended_min_confidence", 0.55)) + 0.02)
    else:
        metrics.setdefault("recommended_min_confidence", 0.55)

    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
