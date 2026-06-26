"""OKX Performance Report — daily/weekly P&L summary from trade journal."""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import JOURNAL_PATH, MEMORY_DIR
from logger import get_logger

log = get_logger("okx.report")

# Learning system journal (from okx_learning.record_trade)
LEARNING_JOURNAL = os.path.join(MEMORY_DIR, "okx-trade-journal.json")


def _load_journal() -> list:
    """Merge both journal sources into a unified list of trade dicts."""
    trades = []

    # Primary journal (from config.log_trade)
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH) as f:
            data = json.load(f)
        for t in data.get("trades", []):
            trades.append({
                "ts": t.get("ts", ""),
                "inst_id": t.get("inst_id", ""),
                "action": t.get("action", ""),
                "pnl_pct": t.get("upl_pct", 0.0),
                "source": "monitor",
            })

    # Learning journal (from okx_learning.record_trade)
    if os.path.exists(LEARNING_JOURNAL):
        with open(LEARNING_JOURNAL) as f:
            data = json.load(f)
        for t in data.get("trades", []):
            trades.append({
                "ts": t.get("timestamp", ""),
                "inst_id": t.get("coin", ""),
                "action": t.get("signal_type", ""),
                "pnl_pct": t.get("pnl_pct", 0.0),
                "source": "learning",
            })

    return sorted(trades, key=lambda t: t.get("ts", ""))


def _date_of(ts: str) -> str:
    return ts[:10] if ts else ""


def _period_trades(trades: list, days: int) -> list:
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    return [t for t in trades if _date_of(t["ts"]) >= cutoff]


def _stats(trades: list) -> dict:
    if not trades:
        return {"count": 0, "wins": 0, "losses": 0, "win_rate": 0.0,
                "total_pnl": 0.0, "avg_pnl": 0.0, "best": 0.0, "worst": 0.0}
    pnls = [t["pnl_pct"] for t in trades if t.get("pnl_pct") not in (None, 0)]
    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    total = sum(pnls)
    return {
        "count": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(pnls) * 100 if pnls else 0.0,
        "total_pnl": total,
        "avg_pnl": total / len(pnls) if pnls else 0.0,
        "best": max(pnls) if pnls else 0.0,
        "worst": min(pnls) if pnls else 0.0,
    }


def _coin_breakdown(trades: list) -> dict:
    by_coin = defaultdict(list)
    for t in trades:
        coin = t["inst_id"].split("-")[0]
        by_coin[coin].append(t["pnl_pct"])
    result = {}
    for coin, pnls in by_coin.items():
        pnls = [p for p in pnls if p not in (None, 0)]
        if not pnls:
            continue
        result[coin] = {
            "trades": len(pnls),
            "total_pnl": sum(pnls),
            "win_rate": len([p for p in pnls if p > 0]) / len(pnls) * 100,
        }
    return dict(sorted(result.items(), key=lambda x: x[1]["total_pnl"], reverse=True))


def generate_report(period: str = "daily") -> str:
    """Generate a formatted text report for the given period (daily/weekly/all)."""
    all_trades = _load_journal()
    days = {"daily": 1, "weekly": 7, "all": 9999}.get(period, 1)
    trades = _period_trades(all_trades, days)
    s = _stats(trades)
    coins = _coin_breakdown(trades)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    period_label = {"daily": "今日", "weekly": "本周", "all": "全部"}.get(period, period)

    lines = [
        f"## 📊 OKX 交易绩效报告 — {period_label}",
        f"生成时间：{now}",
        "",
        "### 概览",
        f"| 项目 | 数值 |",
        f"|------|------|",
        f"| 总交易次数 | {s['count']} |",
        f"| 盈利次数 | {s['wins']} |",
        f"| 亏损次数 | {s['losses']} |",
        f"| 胜率 | {s['win_rate']:.1f}% |",
        f"| 总盈亏 | {s['total_pnl']:+.2f}% |",
        f"| 平均盈亏 | {s['avg_pnl']:+.2f}% |",
        f"| 最佳交易 | {s['best']:+.2f}% |",
        f"| 最差交易 | {s['worst']:+.2f}% |",
    ]

    if coins:
        lines += ["", "### 币种明细"]
        for coin, info in list(coins.items())[:5]:
            lines.append(
                f"- **{coin}**: {info['trades']}笔 | "
                f"总盈亏 {info['total_pnl']:+.2f}% | "
                f"胜率 {info['win_rate']:.0f}%"
            )

    if s["count"] == 0:
        lines.append("\n_暂无交易记录_")

    return "\n".join(lines)


def main(args: list) -> None:
    period = args[0] if args else "daily"
    if period not in ("daily", "weekly", "all"):
        log.error(f"Unknown period: {period}. Use: daily | weekly | all")
        sys.exit(1)
    print(generate_report(period))


if __name__ == "__main__":
    main(sys.argv[1:])
