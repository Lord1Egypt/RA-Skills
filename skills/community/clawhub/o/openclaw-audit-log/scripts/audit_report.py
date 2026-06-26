#!/usr/bin/env python3
"""
OpenClaw Audit Report Generator
生成每日/每周审计报告，输出为 markdown 格式。
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))
from audit_logger import query, AUDIT_FILE

RISK_EMOJI = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🟢",
}


def daily_report(date: str = None) -> str:
    """生成指定日期的审计日报（默认昨天）。"""
    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    since = f"{date}T00:00:00"
    until = f"{date}T23:59:59"

    records = []
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                ts = r.get("timestamp", "")
                if since <= ts <= until:
                    records.append(r)
            except Exception:
                pass

    records.sort(key=lambda x: x.get("timestamp", ""))

    lines = [
        f"# 📋 OpenClaw 审计日报 — {date}",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**操作总数**: {len(records)}",
        "",
    ]

    # 按风险分组统计
    by_risk = {"critical": [], "high": [], "medium": [], "low": []}
    for r in records:
        by_risk[r.get("risk_level", "low")].append(r)

    lines.append("## 🔍 风险分布")
    lines.append("")
    for level in ["critical", "high", "medium", "low"]:
        if by_risk[level]:
            lines.append(f"- {RISK_EMOJI[level]} {level.upper()}: {len(by_risk[level])} 次")
    lines.append("")

    # 高危操作明细
    high_risk = by_risk["critical"] + by_risk["high"]
    if high_risk:
        lines.append("## ⚠️ 高危操作明细")
        lines.append("")
        for r in high_risk:
            emoji = RISK_EMOJI.get(r.get("risk_level", "high"), "⚠️")
            ts = r.get("timestamp", "")[11:19]
            lines.append(
                f"- {emoji} [{ts}] **{r.get('operation_name', r.get('operation'))}** — {r.get('detail', '-')}"
            )
        lines.append("")

    # 所有操作明细
    lines.append("## 📝 操作明细")
    lines.append("")
    if not records:
        lines.append("*当日无操作记录*")
    else:
        lines.append("| 时间 | 操作类型 | 详情 | 风险 |")
        lines.append("|------|----------|------|------|")
        for r in records:
            ts = r.get("timestamp", "")[11:19]
            op_name = r.get("operation_name", r.get("operation", ""))
            detail = r.get("detail", "-")
            risk = r.get("risk_level", "low")
            emoji = RISK_EMOJI.get(risk, "⚪")
            # 截断过长的详情
            if len(detail) > 60:
                detail = detail[:57] + "..."
            lines.append(f"| {ts} | {op_name} | {detail} | {emoji} {risk} |")
    lines.append("")

    # Session 分析
    sessions = set(r.get("session_key", "unknown") for r in records)
    lines.append(f"**涉及会话数**: {len(sessions)}")
    lines.append("")

    return "\n".join(lines)


def weekly_report() -> str:
    """生成本周审计周报。"""
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_start_str = week_start.strftime("%Y-%m-%d")

    since = f"{week_start_str}T00:00:00"
    records = []
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                if r.get("timestamp", "") >= since:
                    records.append(r)
            except Exception:
                pass

    by_op = {}
    by_risk = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    by_day = {}
    for r in records:
        op = r.get("operation", "unknown")
        by_op[op] = by_op.get(op, 0) + 1
        risk = r.get("risk_level", "low")
        by_risk[risk] = by_risk.get(risk, 0) + 1
        day = r.get("timestamp", "")[:10]
        by_day[day] = by_day.get(day, 0) + 1

    lines = [
        f"# 📊 OpenClaw 审计周报",
        "",
        f"**周期**: {week_start_str} ~ {today.strftime('%Y-%m-%d')}",
        f"**生成时间**: {today.strftime('%Y-%m-%d %H:%M')}",
        f"**操作总数**: {len(records)}",
        "",
        "## 📈 操作趋势（按天）",
        "",
    ]

    for day in sorted(by_day.keys()):
        count = by_day[day]
        bar = "█" * min(count, 20)
        lines.append(f"- {day}: {count} 次 {bar}")

    lines.append("")
    lines.append("## 📊 操作类型分布")
    lines.append("")
    sorted_ops = sorted(by_op.items(), key=lambda x: -x[1])
    for op, count in sorted_ops:
        pct = count / len(records) * 100 if records else 0
        lines.append(f"- {op}: {count} 次 ({pct:.1f}%)")

    lines.append("")
    lines.append("## 🔴 风险统计")
    lines.append("")
    for level in ["critical", "high", "medium", "low"]:
        if by_risk[level] > 0:
            lines.append(f"- {RISK_EMOJI[level]} {level.upper()}: {by_risk[level]} 次")

    lines.append("")
    lines.append("## 🕐 高危操作记录")
    lines.append("")

    high_risk = [r for r in records if r.get("risk_level") in ("critical", "high")]
    if not high_risk:
        lines.append("*本周无高危操作*")
    else:
        high_risk.sort(key=lambda x: x.get("timestamp", ""))
        lines.append("| 日期 | 操作类型 | 详情 | 风险 |")
        lines.append("|------|----------|------|------|")
        for r in high_risk:
            ts = r.get("timestamp", "")[:16]
            op_name = r.get("operation_name", r.get("operation", ""))
            detail = r.get("detail", "-")
            if len(detail) > 50:
                detail = detail[:47] + "..."
            risk = r.get("risk_level", "low")
            emoji = RISK_EMOJI.get(risk, "⚪")
            lines.append(f"| {ts} | {op_name} | {detail} | {emoji} {risk} |")

    lines.append("")
    lines.append("---")
    lines.append(f"*报告自动生成 — OpenClaw Audit System*")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: audit_report.py <daily|weekly> [date]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "daily":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        print(daily_report(date))
    elif cmd == "weekly":
        print(weekly_report())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
