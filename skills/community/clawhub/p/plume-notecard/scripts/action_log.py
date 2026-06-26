#!/usr/bin/env python3
"""
操作日志读写模块

维护 action_log_{channel}.json，
记录每次创建/重试操作的完整参数和结果，供重试和熔断机制使用。

两步写入：
  1. create_notecard.py 创建任务后 append_entry（status=pending）
  2. create_notecard.py 任务终态后 update_entry（status=success/failed/...）
"""

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config


def _get_max_log_size() -> int:
    """从 EXTEND.md 读取 max_log_size，默认 10"""
    cfg = config.load_extend_config()
    storage = cfg.get("storage", {})
    if isinstance(storage, dict):
        size = storage.get("max_log_size")
        if isinstance(size, int) and size > 0:
            return size
    return 10


def _log_path(channel: str) -> Path:
    media_dir = config.get_media_dir()
    filename = f"action_log_{channel}.json" if channel else "action_log.json"
    return media_dir / filename


def read_log(channel: str) -> list[dict]:
    """读取指定渠道的操作日志"""
    path = _log_path(channel)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _write_log(channel: str, log: list[dict]):
    """写入日志，超出上限时 FIFO 淘汰"""
    max_size = _get_max_log_size()
    media_dir = config.get_media_dir()
    media_dir.mkdir(parents=True, exist_ok=True)
    if len(log) > max_size:
        log = log[-max_size:]
    _log_path(channel).write_text(
        json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def append_entry(channel: str, entry: dict):
    """创建任务时调用：追加一条 pending 记录"""
    log = read_log(channel)
    entry.setdefault("status", "pending")
    entry.setdefault("created_at", time.time())
    log.append(entry)
    _write_log(channel, log)


def update_entry(channel: str, task_id: str, updates: dict):
    """任务终态时调用：更新对应记录的 status/result 等字段"""
    log = read_log(channel)
    for entry in reversed(log):
        if entry.get("task_id") == task_id:
            entry.update(updates)
            entry.setdefault("completed_at", time.time())
            break
    _write_log(channel, log)
