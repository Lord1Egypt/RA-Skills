#!/usr/bin/env python3
"""
agent_communicator.py
两个 AI 之间通过共享文件直接对话的通信工具。

共享文件（~/.hermes/shared/agent_messages.json）:
  wb_to_hermes: WorkBuddy 发给 Hermes 的消息（待处理）
  hermes_to_wb: Hermes 回复 WorkBuddy 的消息（待处理）

格式：
  {
    "wb_to_hermes": [
      {"id": "uuid", "content": "...", "sent_at": "ISO8601", "status": "pending|read|replied"}
    ],
    "hermes_to_wb": [
      {"id": "uuid", "content": "...", "sent_at": "ISO8601", "status": "pending|read"}
    ]
  }
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone

SHARED_FILE = os.path.expanduser("~/.hermes/shared/agent_messages.json")

def _ensure_file():
    if not os.path.exists(SHARED_FILE):
        os.makedirs(os.path.dirname(SHARED_FILE), exist_ok=True)
        with open(SHARED_FILE, "w") as f:
            json.dump({"wb_to_hermes": [], "hermes_to_wb": []}, f, ensure_ascii=False, indent=2)

def _read():
    _ensure_file()
    with open(SHARED_FILE) as f:
        return json.load(f)

def _write(data):
    _ensure_file()
    with open(SHARED_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── WorkBuddy 端 API ──────────────────────────────────────

def send_to_hermes(content: str) -> str:
    """WorkBuddy 发送消息给 Hermes，返回消息 ID"""
    data = _read()
    msg = {
        "id": str(uuid.uuid4())[:8],
        "content": content,
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending"
    }
    data["wb_to_hermes"].append(msg)
    _write(data)
    print(f"[agent_comm] 📤 WB→Hermes [{msg['id']}]: {content[:60]}...")
    return msg["id"]

def read_from_hermes() -> list:
    """WorkBuddy 读取 Hermes 的所有回复，标记为已读"""
    data = _read()
    replies = [m for m in data["hermes_to_wb"] if m["status"] == "pending"]
    for r in replies:
        r["status"] = "read"
    if replies:
        _write(data)
        for r in replies:
            print(f"[agent_comm] 📥 Hermes→WB [{r['id']}]: {r['content'][:80]}...")
    return replies

def get_pending_to_hermes() -> list:
    """查看发给 Hermes 但 Hermes 还未读的消息"""
    data = _read()
    return [m for m in data["wb_to_hermes"] if m["status"] == "pending"]

# ── Hermes 端 API ─────────────────────────────────────────

def read_from_wb() -> list:
    """Hermes 读取 WorkBuddy 发来的所有消息，标记为已读"""
    data = _read()
    msgs = [m for m in data["wb_to_hermes"] if m["status"] == "pending"]
    for m in msgs:
        m["status"] = "read"
    if msgs:
        _write(data)
        for m in msgs:
            print(f"[agent_comm] 📥 WB→Hermes [{m['id']}]: {m['content'][:80]}...")
    return msgs

def reply_to_wb(content: str) -> str:
    """Hermes 回复 WorkBuddy"""
    data = _read()
    msg = {
        "id": str(uuid.uuid4())[:8],
        "content": content,
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending"
    }
    data["hermes_to_wb"].append(msg)
    _write(data)
    print(f"[agent_comm] 📤 Hermes→WB [{msg['id']}]: {content[:60]}...")
    return msg["id"]

def get_pending_from_wb() -> list:
    """Hermes 查看还有哪些消息等待处理"""
    data = _read()
    return [m for m in data["wb_to_hermes"] if m["status"] == "pending"]

# ── CLI 入口 ──────────────────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "send":
        # python3 agent_communicator.py send "消息内容"
        content = sys.argv[2] if len(sys.argv) > 2 else input("消息内容: ")
        send_to_hermes(content)

    elif cmd == "read":
        # python3 agent_communicator.py read
        replies = read_from_hermes()
        if not replies:
            print("[agent_comm] 没有新消息")
        for r in replies:
            print(f"\n=== Hermes 回复 [{r['id']}] ===")
            print(r["content"])

    elif cmd == "pending":
        msgs = get_pending_to_hermes()
        if msgs:
            print(f"[agent_comm] 还有 {len(msgs)} 条消息等待 Hermes 处理")
            for m in msgs:
                print(f"  [{m['id']}] {m['content'][:60]}")
        else:
            print("[agent_comm] 无待处理消息")

    elif cmd == "hermes-read":
        msgs = read_from_wb()
        if not msgs:
            print("[agent_comm] 没有新消息")
        for m in msgs:
            print(f"\n=== WB 发来 [{m['id']}] ===")
            print(m["content"])

    elif cmd == "hermes-reply":
        content = sys.argv[2] if len(sys.argv) > 2 else input("回复内容: ")
        reply_to_wb(content)

    elif cmd == "hermes-pending":
        msgs = get_pending_from_wb()
        if msgs:
            print(f"[agent_comm] 还有 {len(msgs)} 条消息等待处理")
        else:
            print("[agent_comm] 无待处理消息")

    else:
        print("用法:")
        print("  # WorkBuddy 端")
        print("  python3 agent_communicator.py send <消息>   # 发消息给 Hermes")
        print("  python3 agent_communicator.py read           # 读取 Hermes 回复")
        print("  python3 agent_communicator.py pending        # 查看待处理消息")
        print()
        print("  # Hermes 端")
        print("  python3 agent_communicator.py hermes-read    # 读取 WorkBuddy 消息")
        print("  python3 agent_communicator.py hermes-reply <回复>  # 回复 WorkBuddy")
        print("  python3 agent_communicator.py hermes-pending       # 查看待处理消息")
