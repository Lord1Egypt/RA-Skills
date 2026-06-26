#!/usr/bin/env python3
"""
OpenClaw 操作链分析引擎
检测同一上下文中的危险操作组合模式，发现隐蔽的链式攻击。
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

# 危险操作链模式：操作序列 → 告警描述
DANGEROUS_CHAINS = [
    {
        "pattern": ["credential_access", "external_send"],
        "description": "凭证访问 → 外部发送（可疑数据外传）",
        "level": "critical",
        "window_minutes": 60,  # 60分钟内
    },
    {
        "pattern": ["credential_access", "file_write"],
        "description": "凭证访问 → 文件写入（凭证可能被保存）",
        "level": "high",
        "window_minutes": 30,
    },
    {
        "pattern": ["file_delete", "external_send"],
        "description": "文件删除 → 外部发送（销毁+外传）",
        "level": "critical",
        "window_minutes": 30,
    },
    {
        "pattern": ["credential_access", "file_move"],
        "description": "凭证访问 → 文件移动（可疑转移）",
        "level": "high",
        "window_minutes": 30,
    },
    {
        "pattern": ["external_api", "external_send"],
        "description": "外部API调用 → 外部发送（API数据外传）",
        "level": "high",
        "window_minutes": 60,
    },
    {
        "pattern": ["file_write", "external_send"],
        "description": "文件写入 → 外部发送（敏感文件外传）",
        "level": "high",
        "window_minutes": 60,
    },
    {
        "pattern": ["destruction", "external_send"],
        "description": "破坏性操作 → 外部发送（销毁证据+外传）",
        "level": "critical",
        "window_minutes": 30,
    },
    {
        "pattern": ["destruction", "credential_access"],
        "description": "破坏性操作 → 凭证访问（可能是入侵准备）",
        "level": "critical",
        "window_minutes": 30,
    },
    {
        "pattern": ["credential_access", "credential_access"],
        "description": "短时间内多次凭证访问（异常行为）",
        "level": "high",
        "window_minutes": 10,
        "min_count": 3,
    },
]

# 告警冷却
COOLDOWN_FILE = Path.home() / ".openclaw" / "audit" / "chain_alert_cooldown.json"
COOLDOWN_SECONDS = 600  # 10分钟不重复告警同一模式


def get_token():
    req = Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]


def send_alert(token, title: str, detail: str, level: str = "critical"):
    icon = {"critical": "🔴", "high": "🟠", "medium": "🟡"}.get(level, "⚪")
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


def load_recent_records(minutes: int = 120) -> list:
    """加载最近 N 分钟的操作记录"""
    if not AUDIT_FILE.exists():
        return []

    cutoff = (datetime.now() - timedelta(minutes=minutes)).isoformat()
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

    return records


def detect_chains():
    """检测危险操作链"""
    # 先用最大时间窗口
    all_records = load_recent_records(minutes=120)
    if not all_records:
        return []

    alerts = []

    for chain in DANGEROUS_CHAINS:
        pattern = chain["pattern"]
        window = chain["window_minutes"]
        min_count = chain.get("min_count", 2)

        # 获取窗口内的记录
        cutoff = (datetime.now() - timedelta(minutes=window)).isoformat()
        window_records = [r for r in all_records if r.get("timestamp", "") >= cutoff]

        # 按 session_key 或 context_id 分组
        groups = {}
        for r in window_records:
            ctx = r.get("session_key", "unknown")
            if ctx not in groups:
                groups[ctx] = []
            groups[ctx].append(r)

        # 检查每个组
        for ctx, recs in groups.items():
            # 按时间排序
            recs.sort(key=lambda x: x.get("timestamp", ""))

            ops = [r.get("operation", "") for r in recs]
            ops_str = ",".join(ops)

            # 检查顺序模式（所有pattern中的操作都出现，且顺序一致）
            found = True
            last_pos = -1
            matched_positions = []

            for p in pattern:
                pos = ops_str.find(p, last_pos + 1)
                if pos == -1:
                    found = False
                    break
                matched_positions.append(pos)
                last_pos = pos

            if found:
                # 检查出现次数（如果pattern是重复操作）
                if min_count > 2:
                    count = ops_str.count(pattern[0])
                    if count < min_count:
                        continue

                # 触发告警
                detail_parts = []
                for r in recs:
                    detail_parts.append(
                        f"- [{r.get('timestamp','')[:19]}] {r.get('operation_name', r.get('operation'))}: {r.get('detail','-')}"
                    )

                alerts.append({
                    "chain": chain,
                    "context": ctx,
                    "records": recs,
                    "detail": "\n".join(detail_parts[:10]),  # 最多显示10条
                })

    return alerts


def check_and_alert():
    """检测危险链并告警"""
    alerts = detect_chains()
    if not alerts:
        print(f"操作链分析: 无异常 ✅ ({len(load_recent_records(10))} 条近记录)")
        return

    cooldown = load_cooldown()
    now = datetime.now()
    sent = 0

    for alert in alerts:
        chain = alert["chain"]
        pattern_str = "→".join(chain["pattern"])
        key = f"{alert['context']}:{pattern_str}"

        # 检查冷却
        last = cooldown.get(key, "1970-01-01T00:00:00")
        last_time = datetime.fromisoformat(last)
        if (now - last_time).total_seconds() < COOLDOWN_SECONDS:
            continue

        # 发送告警
        token = get_token()
        title = f"危险操作链: {chain['description']}"
        detail = f"**检测到可疑操作链**\n\n"
        detail += f"**模式**: {pattern_str}\n"
        detail += f"**上下文**: {alert['context']}\n"
        detail += f"**风险**: {chain['level'].upper()}\n\n"
        detail += "**操作明细**:\n" + alert["detail"]
        detail += f"\n\n请立即确认是否为本人操作！"

        ok = send_alert(token, title, detail, chain["level"])
        print(f"链式告警已发送: {'✅' if ok else '❌'} {chain['description']}")
        sent += 1

        # 更新冷却
        cooldown[key] = now.isoformat()
        save_cooldown(cooldown)

    if sent > 0:
        print(f"共发送 {sent} 个链式告警")
    else:
        print(f"检测到 {len(alerts)} 个危险链（均在冷却期）")


if __name__ == "__main__":
    check_and_alert()
