#!/usr/bin/env python3
"""
OpenClaw 操作速率监控 & 异常检测
检测短时间内大量敏感操作，触发实时告警。
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

APP_ID = "cli_a92fd77a9af8dcd4"
APP_SECRET = "GjLeLpcUeUe92GCSvFSlxSoKwqHvGXeF"
USER_ID = "ou_24d7f017625dc287e1eb2fa63b4a00ed"

AUDIT_FILE = Path.home() / ".openclaw" / "audit" / "audit.log"

# 速率阈值
WINDOW_MINUTES = 5  # 时间窗口：5分钟
HIGH_RISK_THRESHOLD = 3  # 高危操作超过3次 → 告警
TOTAL_OPS_THRESHOLD = 10  # 总操作超过10次 → 告警

# 告警冷却（防止重复告警）
COOLDOWN_FILE = Path.home() / ".openclaw" / "audit" / "rate_alert_cooldown.json"
COOLDOWN_SECONDS = 300  # 5分钟内不重复告警


def get_token():
    req = Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]


def send_alert(token, title: str, detail: str, level: str = "warning"):
    icon = {"critical": "🔴", "warning": "🟠", "info": "🟡"}.get(level, "⚪")
    content = (
        f"{icon} **{title}**\n\n"
        f"{detail}\n\n"
        f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    req = Request(
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
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read()).get("code") == 0
    except Exception:
        return False


def load_cooldown():
    if COOLDOWN_FILE.exists():
        return json.loads(COOLDOWN_FILE.read_text())
    return {}


def save_cooldown(cooldown: dict):
    COOLDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
    COOLDOWN_FILE.write_text(json.dumps(cooldown, ensure_ascii=False, indent=2))


def check_and_alert():
    """检查操作速率，异常则告警"""
    if not AUDIT_FILE.exists():
        return

    # 读取最近 WINDOW_MINUTES 分钟的操作
    cutoff = (datetime.now() - timedelta(minutes=WINDOW_MINUTES)).isoformat()
    records = []

    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                if r.get("timestamp", "") >= cutoff:
                    records.append(r)
            except Exception:
                pass

    if not records:
        return

    # 统计
    high_risk_count = sum(
        1 for r in records
        if r.get("risk_level") in ("critical", "high")
    )
    total_count = len(records)

    # 检查是否触发告警
    cooldown = load_cooldown()
    now = datetime.now()

    alerts = []

    if high_risk_count >= HIGH_RISK_THRESHOLD:
        alerts.append(f"高危操作：{high_risk_count} 次（阈值: {HIGH_RISK_THRESHOLD}）")

    if total_count >= TOTAL_OPS_THRESHOLD:
        alerts.append(f"总操作量：{total_count} 次（阈值: {TOTAL_OPS_THRESHOLD}）")

    if alerts:
        # 检查冷却期
        last_alert = cooldown.get("last_alert", "1970-01-01T00:00:00")
        last_time = datetime.fromisoformat(last_alert)
        if (now - last_time).total_seconds() > COOLDOWN_SECONDS:
            # 触发告警
            token = get_token()
            detail = "\n".join([f"• {a}" for a in alerts])
            detail += f"\n\n时间窗口：最近 {WINDOW_MINUTES} 分钟"
            detail += "\n\n请核实是否为本人操作。"

            ok = send_alert(token, "操作速率异常告警", detail, "warning")
            print(f"速率告警已发送: {'✅' if ok else '❌'}")
            print(f"  高危: {high_risk_count}, 总计: {total_count}")

            # 更新冷却时间
            cooldown["last_alert"] = now.isoformat()
            cooldown["high_risk"] = high_risk_count
            cooldown["total"] = total_count
            save_cooldown(cooldown)
        else:
            remaining = int(COOLDOWN_SECONDS - (now - last_time).total_seconds())
            print(f"冷却中，剩余 {remaining} 秒不重复告警")
    else:
        print(f"速率正常: 高危={high_risk_count}, 总计={total_count}")


if __name__ == "__main__":
    check_and_alert()
