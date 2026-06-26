#!/usr/bin/env python3
"""
OpenClaw 高危操作飞书确认拦截系统
在执行高危操作前，先发飞书确认，用户回复后决定执行或跳过。
通过读取聊天历史（而非消息replies）来检测用户回复。
"""

import sys
import json
import time
import os
import threading
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

# 配置文件
APP_ID = "cli_a92fd77a9af8dcd4"
APP_SECRET = "GjLeLpcUeUe92GCSvFSlxSoKwqHvGXeF"
USER_ID = "ou_24d7f017625dc287e1eb2fa63b4a00ed"

PENDING_FILE = Path.home() / ".openclaw" / "audit" / "pending_confirms.json"
CONFIRM_TIMEOUT_SEC = 600  # 10分钟超时

# 已知的飞书聊天ID（与用户的私聊）
CHAT_ID = "oc_9f0e7d08404274474820544d37c37e48"


# ========== 飞书 API ==========

def get_token():
    req = Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]


def send_feishu_message(token, content: str) -> str:
    """发送飞书文本消息，返回 message_id"""
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
    with urlopen(req) as resp:
        result = json.loads(resp.read())
        if result.get("code") == 0:
            return result["data"]["message_id"]
        raise Exception(f"发送失败: {result}")


def get_recent_messages(token, page_size: int = 10) -> list:
    """获取最近的聊天消息（用于检测用户回复）"""
    req = Request(
        f"https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id={CHAT_ID}&page_size={page_size}&sort_type=ByCreateTimeDesc",
        headers={"Authorization": f"Bearer {token}"},
        method="GET"
    )
    with urlopen(req) as resp:
        data = json.loads(resp.read())
        if data.get("code") == 0:
            return data.get("data", {}).get("items", [])
        return []


# ========== 待确认队列 ==========

def load_pending():
    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    if PENDING_FILE.exists():
        with open(PENDING_FILE, "r") as f:
            return json.load(f)
    return {}


def save_pending(pending: dict):
    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PENDING_FILE, "w") as f:
        json.dump(pending, f, ensure_ascii=False, indent=2)


def add_pending(confirm_id: str, operation: str, detail: str, risk_level: str,
                action_script: str, timeout_sec: int = CONFIRM_TIMEOUT_SEC):
    """添加一个待确认的操作"""
    token = get_token()
    msg_content = build_confirm_message(operation, detail, risk_level, confirm_id)
    message_id = send_feishu_message(token, msg_content)

    pending = load_pending()
    pending[confirm_id] = {
        "operation": operation,
        "detail": detail,
        "risk_level": risk_level,
        "action_script": action_script,
        "message_id": message_id,
        "created_at": datetime.now().isoformat(),
        "timeout_at": (datetime.now() + timedelta(seconds=timeout_sec)).isoformat(),
        "status": "pending",  # pending / confirmed / rejected / timeout
    }
    save_pending(pending)
    return message_id


def build_confirm_message(operation: str, detail: str, risk_level: str, confirm_id: str) -> str:
    risk_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡"}.get(risk_level, "⚪")
    lines = [
        f"{risk_icon} **高危操作待确认**",
        "",
        f"**操作类型**: {operation}",
        f"**详情**: {detail}",
        f"**风险等级**: {risk_level.upper()}",
        "",
        "⏱️ 请在 10 分钟内回复：",
        "• 回复 **确认** → 执行此操作",
        "• 回复 **取消** → 跳过此操作",
        "• 无回复 → 10分钟后自动跳过",
        "",
        f"[确认ID: `{confirm_id}`]",
    ]
    return "\n".join(lines)


def check_pending_replies() -> dict:
    """检查所有待确认项的最新状态，通过读取聊天历史检测用户回复"""
    pending = load_pending()
    if not pending:
        return {}

    token = get_token()

    # 获取最近的聊天消息
    try:
        messages = get_recent_messages(token, page_size=20)
    except Exception as e:
        print(f"Error getting messages: {e}", file=sys.stderr)
        return {}

    updates = {}

    for confirm_id, info in list(pending.items()):
        if info["status"] != "pending":
            continue

        # 超时检查
        try:
            timeout_at = datetime.fromisoformat(info["timeout_at"])
            if datetime.now() >= timeout_at:
                pending[confirm_id]["status"] = "timeout"
                updates[confirm_id] = "timeout"
                continue
        except Exception:
            pass

        # 在聊天历史中查找用户的回复（sender = USER_ID）
        for msg in messages:
            sender_id = msg.get("sender", {}).get("id", "")
            if sender_id != USER_ID:
                continue

            body_content = msg.get("body", {}).get("content", "")
            if isinstance(body_content, str):
                try:
                    body = json.loads(body_content)
                    text = body.get("text", "").lower().strip()
                except Exception:
                    text = body_content.lower().strip()

                if "确认" in text or "confirm" in text or "ok" in text or "yes" in text:
                    pending[confirm_id]["status"] = "confirmed"
                    updates[confirm_id] = "confirmed"
                    break
                elif any(k in text for k in ["取消", "拒绝", "no", "reject", "stop"]):
                    pending[confirm_id]["status"] = "rejected"
                    updates[confirm_id] = "rejected"
                    break

    # 清理已处理的过期项（保留1小时）
    now = datetime.now()
    for confirm_id in list(pending.keys()):
        info = pending[confirm_id]
        if info["status"] in ("confirmed", "rejected", "timeout"):
            try:
                created = datetime.fromisoformat(info["created_at"])
                if (now - created).total_seconds() > 3600:
                    del pending[confirm_id]
            except Exception:
                del pending[confirm_id]

    save_pending(pending)
    return updates


def get_confirm_status(confirm_id: str) -> str:
    """查询某个确认项的状态"""
    pending = load_pending()
    if confirm_id in pending:
        return pending[confirm_id]["status"]
    return "unknown"


# ========== CLI 命令 ==========

def cmd_request():
    """发送确认请求（后台调用）"""
    if len(sys.argv) < 4:
        print("用法: confirm.py request <操作类型> <详情> [执行脚本] [风险等级]")
        sys.exit(1)

    operation = sys.argv[2]
    detail = sys.argv[3]
    action_script = sys.argv[4] if len(sys.argv) > 4 else ""
    risk_level = sys.argv[5] if len(sys.argv) > 5 else "high"

    confirm_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    msg_id = add_pending(confirm_id, operation, detail, risk_level, action_script)
    print(f"CONFIRM_ID={confirm_id}")
    print(f"MESSAGE_ID={msg_id}")
    print(f"STATUS=pending")
    print(f"TIMEOUT={CONFIRM_TIMEOUT_SEC}秒")


def cmd_check():
    """检查所有待确认项状态"""
    updates = check_pending_replies()
    pending = load_pending()

    pending_count = len([p for p in pending.values() if p["status"] == "pending"])
    print(f"PENDING_COUNT={pending_count}")

    for confirm_id, info in pending.items():
        print(f"\n[{confirm_id}] {info['operation']}: {info['status']}")

    if updates:
        print(f"\nUPDATED=yes")
        for cid, st in updates.items():
            print(f"  {cid} -> {st}")
    else:
        print(f"\nUPDATED=no")


def cmd_status():
    """查询指定确认ID状态"""
    if len(sys.argv) < 3:
        print("用法: confirm.py status <confirm_id>")
        sys.exit(1)

    confirm_id = sys.argv[2]
    status = get_confirm_status(confirm_id)
    print(f"CONFIRM_ID={confirm_id}")
    print(f"STATUS={status}")

    if status == "confirmed":
        pending = load_pending()
        if confirm_id in pending:
            print(f"ACTION_SCRIPT={pending[confirm_id].get('action_script','')}")
    elif status == "unknown":
        print("❌ 确认项不存在或已清理")


def cmd_wait():
    """等待用户确认（阻塞式，最多等N秒）"""
    wait_sec = int(sys.argv[2]) if len(sys.argv) > 2 else CONFIRM_TIMEOUT_SEC

    confirm_id = None
    for arg in sys.argv[3:]:
        if arg.startswith("CONFIRM_ID="):
            confirm_id = arg.split("=", 1)[1]

    if not confirm_id:
        print("ERROR: CONFIRM_ID required")
        sys.exit(1)

    start = time.time()
    while time.time() - start < wait_sec:
        updates = check_pending_replies()
        pending = load_pending()

        if confirm_id in pending:
            status = pending[confirm_id]["status"]
            if status != "pending":
                elapsed = int(time.time() - start)
                print(f"RESULT={status}")
                print(f"CONFIRM_ID={confirm_id}")
                print(f"ELAPSED={elapsed}秒")
                if status == "confirmed":
                    print(f"ACTION_SCRIPT={pending[confirm_id].get('action_script','')}")
                sys.exit(0)

        time.sleep(5)

    # 超时
    pending = load_pending()
    if confirm_id in pending and pending[confirm_id]["status"] == "pending":
        pending[confirm_id]["status"] = "timeout"
        save_pending(pending)

    print(f"RESULT=timeout")
    print(f"CONFIRM_ID={confirm_id}")
    print(f"ELAPSED={wait_sec}秒")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Commands: request, check, status, wait")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "request":
        cmd_request()
    elif cmd == "check":
        cmd_check()
    elif cmd == "status":
        cmd_status()
    elif cmd == "wait":
        cmd_wait()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
