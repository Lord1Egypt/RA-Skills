"""
Agent 通知队列：脚本把事件写入队列文件，
agent（闪电）在心跳中读取并推送到 Telegram。

用法：
  from agent_notify import notify
  notify("transcribing", title="项目周会")
  notify("transcript", title="项目周会", path="/path/to/transcript.txt")
  notify("summary_ready", title="项目周会", path="/path/to/summary.md")
"""

import json
from datetime import datetime
from pathlib import Path

QUEUE_PATH = Path.home() / ".config" / "meeting-assistant" / "agent-queue.json"


def notify(event_type: str, **kwargs):
    """添加一条通知到队列。"""
    entry = {
        "type": event_type,
        "ts": datetime.now().isoformat(),
        **kwargs,
    }
    queue = []
    if QUEUE_PATH.exists():
        try:
            queue = json.loads(QUEUE_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    queue.append(entry)
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False))
