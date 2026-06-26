"""
common.py — 公共工具函数

price-monitor.py 和 news-monitor.py 共享的工具函数：
  - get_session_uuid: 通过 session_key 查询 sessionId
  - deliver_message:  通过 openclaw agent --deliver 发送通知
  - atomic_write_json: 原子替换方式写 JSON（防并发损坏）
"""

import json
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


def get_session_uuid(session_key: str, agent_id: str) -> Optional[str]:
    """通过 session_key 查询对应的 sessionId（用于 --session-id 参数）"""
    try:
        result = subprocess.run(
            ["openclaw", "sessions", "--agent", agent_id, "--json"],
            capture_output=True, text=True, timeout=10,
        )
        data = json.loads(result.stdout)
        for s in data.get("sessions", []):
            if s.get("key") == session_key:
                return s.get("sessionId")
    except Exception:
        pass
    return None


def deliver_message(alert: dict, msg: str) -> None:
    """
    通过 openclaw agent --deliver 发送通知。
    路由参数从 alert 字典中读取（agent_id / session_key / reply_channel / reply_to）。
    """
    agent_id      = alert.get("agent_id", "laok")
    session_key   = alert.get("session_key", "")
    reply_channel = alert.get("reply_channel", "feishu")
    reply_to      = alert.get("reply_to", "")

    session_uuid = get_session_uuid(session_key, agent_id) if session_key else None

    cmd = ["openclaw", "agent", "--deliver", "--reply-account", agent_id,
           "--reply-channel", reply_channel]
    if reply_to:
        cmd += ["--reply-to", reply_to]
    if session_uuid:
        cmd += ["--session-id", session_uuid]
    else:
        cmd += ["--agent", agent_id]
    cmd += ["--message", msg]

    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def atomic_write_json(path: Path, data: object) -> None:
    """
    原子替换方式写 JSON 文件。
    先写到同目录下的临时文件，再用 os.replace 原子替换，
    防止多进程并发写入时文件损坏。
    """
    with tempfile.NamedTemporaryFile(
        "w", dir=str(path.parent), delete=False, suffix=".tmp",
        encoding="utf-8",
    ) as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        tmp = f.name
    os.replace(tmp, str(path))
