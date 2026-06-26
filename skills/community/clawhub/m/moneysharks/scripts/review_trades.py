#!/usr/bin/env python3
"""
Post-trade review: analyse completed trades for learning signals.
Input (stdin JSON): array of trade journal entries.
Output: review summary with outcomes, lesson tags, win rate, avg PnL, regime performance.
"""
import json
import sys
from collections import Counter, defaultdict


def main() -> int:
    trades = json.load(sys.stdin)
    if not trades:
        print(json.dumps({"trade_count": 0, "outcomes": {}, "lesson_tags": {}, "win_rate": 0.0}))
        return 0

    # Only analyse closed/executed trades (not wait/hold)
    executed = [t for t in trades if t.get("decision") in ("long", "short", "close")]
    closed = [t for t in executed if t.get("outcome") in ("win", "loss", "breakeven")]

    by_outcome = Counter(t.get("outcome", "unknown") for t in closed)
    by_tag = Counter(tag for t in closed for tag in t.get("lesson_tags", []))
    by_symbol = Counter(t.get("symbol") for t in executed)

    # Win rate
    wins = by_outcome.get("win", 0)
    losses = by_outcome.get("loss", 0)
    total_closed = wins + losses
    win_rate = wins / total_closed if total_closed else 0.0

    # Avg PnL
    pnls = [float(t.get("realised_pnl", 0)) for t in closed if t.get("realised_pnl") is not None]
    avg_pnl = sum(pnls) / len(pnls) if pnls else 0.0
    total_pnl = sum(pnls)

    # PnL by symbol
    pnl_by_symbol = defaultdict(list)
    for t in closed:
        if t.get("realised_pnl") is not None:
            pnl_by_symbol[t.get("symbol", "unknown")].append(float(t["realised_pnl"]))

    # Loss streak detection
    max_streak = 0
    current_streak = 0
    for t in sorted(closed, key=lambda x: x.get("ts", "")):
        if t.get("outcome") == "loss":
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0

    # Regime performance (regime is set by trade_loop from features trend)
    regime_performance = defaultdict(lambda: {"wins": 0, "losses": 0, "total_pnl": 0.0})
    for t in closed:
        regime = t.get("regime") or t.get("features_1h", {}).get("trend", "unknown")
        if t.get("outcome") == "win":
            regime_performance[regime]["wins"] += 1
        elif t.get("outcome") == "loss":
            regime_performance[regime]["losses"] += 1
        regime_performance[regime]["total_pnl"] += float(t.get("realised_pnl", 0))

    # Confidence vs outcome
    high_conf_trades = [t for t in closed if float(t.get("confidence", 0)) >= 0.7]
    high_conf_wins = len([t for t in high_conf_trades if t.get("outcome") == "win"])
    high_conf_wr = high_conf_wins / len(high_conf_trades) if high_conf_trades else 0.0

    # Lessons
    lessons = []
    if win_rate < 0.4 and total_closed >= 5:
        lessons.append("win_rate_below_40pct_review_signal_quality")
    if max_streak >= 3:
        lessons.append(f"max_loss_streak_{max_streak}_consider_lower_leverage")
    if avg_pnl < 0:
        lessons.append("negative_avg_pnl_review_rr_ratio")
    if high_conf_wr > win_rate + 0.1:
        lessons.append("high_confidence_trades_outperform_raise_threshold")

    print(json.dumps({
        "trade_count": len(trades),
        "executed_count": len(executed),
        "closed_count": total_closed,
        "outcomes": dict(by_outcome),
        "win_rate": round(win_rate, 4),
        "avg_pnl": round(avg_pnl, 4),
        "total_pnl": round(total_pnl, 4),
        "max_loss_streak": max_streak,
        "lesson_tags": dict(by_tag),
        "lessons": lessons,
        "by_symbol": dict(by_symbol),
        "pnl_by_symbol": {k: round(sum(v), 4) for k, v in pnl_by_symbol.items()},
        "regime_performance": dict(regime_performance),
        "high_conf_win_rate": round(high_conf_wr, 4),
    }, indent=2, default=dict))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
