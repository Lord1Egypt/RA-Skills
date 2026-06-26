#!/usr/bin/env python3
"""
OpenClaw Audit Report - 飞书推送脚本
每日/每周生成审计报告并推送到飞书。
"""

import sys
import json
from pathlib import Path

# Add scripts dir to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from audit_logger import AUDIT_FILE, summary
from datetime import datetime, timedelta

# 飞书配置
APP_ID = "cli_a92fd77a9af8dcd4"
APP_SECRET = "GjLeLpcUeUe92GCSvFSlxSoKwqHvGXeF"
USER_ID = "ou_24d7f017625dc287e1eb2fa63b4a00ed"

RISK_EMOJI = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🟢",
}


def get_token():
    import urllib.request
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]


def send_feishu(token, content: str):
    import urllib.request
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=json.dumps({
            "receive_id": USER_ID,
            "msg_type": "text",
            "content": json.dumps({"text": content})
        }).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        return result.get("code") == 0


def build_daily_message(date: str = None) -> str:
    """构建每日审计日报（Markdown 格式）"""
    if date is None:
        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    since = f"{date}T00:00:00"
    until = f"{date}T23:59:59"

    records = []
    if AUDIT_FILE.exists():
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

    # 风险统计
    by_risk = {"critical": [], "high": [], "medium": [], "low": []}
    for r in records:
        by_risk[r.get("risk_level", "low")].append(r)

    total = len(records)
    high_total = len(by_risk["critical"]) + len(by_risk["high"])

    lines = [
        f"# 📋 OpenClaw 审计日报",
        f"**日期**: {date}",
        f"**操作总数**: {total} 次",
        f"**高危操作**: {high_total} 次",
        "",
        "## 🔍 风险分布",
        "",
        f"- 🔴 critical: {len(by_risk['critical'])} 次",
        f"- 🟠 high: {len(by_risk['high'])} 次",
        f"- 🟡 medium: {len(by_risk['medium'])} 次",
        f"- 🟢 low: {len(by_risk['low'])} 次",
        "",
    ]

    # 高危操作明细
    high_risk = by_risk["critical"] + by_risk["high"]
    if high_risk:
        lines.append("## ⚠️ 高危操作")
        lines.append("")
        for r in high_risk:
            emoji = RISK_EMOJI.get(r.get("risk_level", "high"), "⚠️")
            ts = r.get("timestamp", "")[11:19]
            lines.append(f"- {emoji} [{ts}] **{r.get('operation_name', r.get('operation'))}** — {r.get('detail', '-')}")
        lines.append("")
    else:
        lines.append("## ✅ 无高危操作")
        lines.append("")

    # 近30天趋势
    s = summary(days=30)
    by_day = s.get("by_day", {})
    if by_day:
        lines.append("## 📈 近30天操作趋势")
        lines.append("")
        sorted_days = sorted(by_day.keys())[-7:]  # 最近7天
        for day in sorted_days:
            count = by_day[day]
            bar = "█" * min(count, 20)
            lines.append(f"- {day}: {count} 次 {bar}")
        lines.append("")

    lines.append("---")
    lines.append(f"*由 OpenClaw 自动生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def build_weekly_message() -> str:
    """构建本周审计周报"""
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_str = week_start.strftime("%Y-%m-%d")
    end_str = today.strftime("%Y-%m-%d")

    s = summary(days=today.weekday() + 1)
    total = s["total_operations"]
    by_risk = s["by_risk_level"]
    by_day = s["by_day"]
    by_op = {}
    for r in s.get("records", []):
        op = r.get("operation", "unknown")
        by_op[op] = by_op.get(op, 0) + 1

    lines = [
        f"# 📊 OpenClaw 审计周报",
        f"**周期**: {week_str} ~ {end_str}",
        f"**操作总数**: {total} 次",
        "",
        "## 🔴 风险统计",
        "",
        f"- 🔴 critical: {by_risk.get('critical', 0)} 次",
        f"- 🟠 high: {by_risk.get('high', 0)} 次",
        f"- 🟡 medium: {by_risk.get('medium', 0)} 次",
        f"- 🟢 low: {by_risk.get('low', 0)} 次",
        "",
        "## 📈 每日趋势",
        "",
    ]

    for day in sorted(by_day.keys()):
        count = by_day[day]
        bar = "█" * min(count, 15)
        lines.append(f"- {day}: {count} 次 {bar}")

    if by_op:
        lines.append("")
        lines.append("## 📊 操作类型 Top5")
        lines.append("")
        sorted_ops = sorted(by_op.items(), key=lambda x: -x[1])[:5]
        for op, count in sorted_ops:
            lines.append(f"- {op}: {count} 次")

    high_risk = [r for r in s.get("records", []) if r.get("risk_level") in ("critical", "high")]
    if high_risk:
        lines.append("")
        lines.append("## ⚠️ 高危记录")
        lines.append("")
        for r in high_risk[-10:]:
            ts = r.get("timestamp", "")[:16]
            lines.append(f"- [{ts}] **{r.get('operation_name', r.get('operation'))}** — {r.get('detail', '-')}")

    lines.append("")
    lines.append("---")
    lines.append(f"*由 OpenClaw 自动生成 · {today.strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def send_realtime_alert(operation: str, detail: str, risk_level: str):
    """
    实时发送高危操作预警到飞书（立即发送，不等待确认）。
    用于检测到 critical 操作时立即通知用户。
    """
    risk_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡"}.get(risk_level, "⚪")
    content = (
        f"{risk_icon} **紧急：检测到高危操作**\n\n"
        f"**操作**: {operation}\n"
        f"**详情**: {detail}\n"
        f"**风险**: {risk_level.upper()}\n"
        f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "请核实是否为您本人操作。"
    )
    token = get_token()
    ok = send_feishu(token, content)
    print(f"实时预警: {'✅' if ok else '❌'}")
    return ok


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "daily"

    if mode == "daily":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        message = build_daily_message(date)
    elif mode == "weekly":
        message = build_weekly_message()
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

    print(message)
    print("\n---")

    # 发送到飞书
    token = get_token()
    # 飞书 text 消息有长度限制，超过4000截断
    if len(message) > 4000:
        # 分段发送
        parts = [message[i:i+3800] for i in range(0, len(message), 3800)]
        for i, part in enumerate(parts):
            if len(parts) > 1:
                part = f"[{i+1}/{len(parts)}]\n\n{part}"
            ok = send_feishu(token, part)
            print(f"Part {i+1}: {'✅' if ok else '❌'}")
    else:
        ok = send_feishu(token, message)
        print(f"Sent to Feishu: {'✅' if ok else '❌'}")


if __name__ == "__main__":
    main()
