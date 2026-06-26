"""
hermes-memory-bridge / memory_writer.py
写入 Hermes 记忆文件（带健壮错误处理）
"""
from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from pathlib import Path

from config import (
    BRIDGE_META,
    ENTRY_DELIMITER,
    HERMES_MEMORIES_DIR,
    MAX_ENTRY_CHARS,
    MAX_EVENTS,
    SHARED_DIR,
    WORKBUDDY_LOG,
    _get_logger,
)

logger = _get_logger("memory_writer")


# ─── 内部工具 ───────────────────────────────────────────────────────

def _ensure_dir(path: Path) -> bool:
    """确保目录存在，返回是否成功"""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError as e:
        logger.error(f"权限不足，无法创建目录 {path.parent}: {e}")
        return False
    except OSError as e:
        logger.error(f"创建目录失败 {path.parent}: {e}")
        return False


def _safe_read(path: Path, default: str = "") -> str:
    """安全读取文件，失败时返回默认值"""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return default
    except PermissionError as e:
        logger.warning(f"权限不足，无法读取 {path}: {e}")
        return default
    except OSError as e:
        logger.warning(f"读取文件失败 {path}: {e}")
        return default


def _safe_write(path: Path, content: str) -> bool:
    """安全写入文件，返回是否成功"""
    try:
        path.write_text(content, encoding="utf-8")
        return True
    except PermissionError as e:
        logger.error(f"权限不足，无法写入 {path}: {e}")
        return False
    except OSError as e:
        logger.error(f"写入文件失败 {path}: {e}")
        return False


def _sanitize(content: str) -> str:
    """去除潜在注入风险内容"""
    patterns = [
        r"ignore\s+(previous|all|above|prior)\s+instructions",
        r"you\s+are\s+now\s+",
        r"system\s+prompt\s+override",
        r"<\|im_start\|>|<\|im_end\|>",
    ]
    for pat in patterns:
        content = re.sub(pat, "[FILTERED]", content, flags=re.IGNORECASE)
    return content[:MAX_ENTRY_CHARS]


# ─── 公开接口 ───────────────────────────────────────────────────────

def append_hermes_memory(
    target: str,
    content: str,
    source: str = "WorkBuddy",
) -> str | None:
    """
    向 Hermes 的 MEMORY.md 或 USER.md 追加一条记忆条目。

    Args:
        target: 'memory' | 'user'
        content: 要写入的内容
        source: 来源标记（默认为 WorkBuddy）

    Returns:
        写入的完整条目，或 None（失败时）
    """
    if not _ensure_dir(HERMES_MEMORIES_DIR):
        return None

    fname = "MEMORY.md" if target == "memory" else "USER.md"
    fpath = HERMES_MEMORIES_DIR / fname
    timestamp = datetime.now().strftime("%Y-%m-%d")
    safe_content = _sanitize(content)
    entry = f"[{timestamp} · {source}]\n{safe_content}"

    existing = _safe_read(fpath)
    if existing.strip():
        new_content = existing.rstrip() + ENTRY_DELIMITER + entry
    else:
        new_content = entry

    if _safe_write(fpath, new_content):
        logger.info(f"写入记忆: [{fname}] {timestamp} · {source}")
        return entry
    return None


def write_shared_log(
    content: str,
    log_type: str = "workbuddy",
) -> Path | None:
    """
    写入共用互通日志（Hermes 可通过 on_delegation hook 读取）。

    Args:
        content: 日志内容
        log_type: 'workbuddy' | 'hermes'

    Returns:
        写入的日志文件路径，或 None（失败时）
    """
    if not _ensure_dir(SHARED_DIR):
        return None

    log_file = SHARED_DIR / f"{log_type}.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"[{timestamp}] {content}\n"

    existing = _safe_read(log_file)
    # 保留最近 500 行，防止日志无限增长
    lines = (existing + entry).strip().split("\n")
    lines = lines[-500:]
    combined = "\n".join(lines) + "\n"

    if _safe_write(log_file, combined):
        logger.debug(f"写入日志: {log_file.name}")
        return log_file
    return None


def write_bridge_event(event_type: str, data: dict) -> bool:
    """
    写入桥接元事件，供两边 Agent 在下次启动时读取。

    Args:
        event_type: 'task_done' | 'config_change' | 'sync' | 'error'
        data: 事件附加数据

    Returns:
        是否写入成功
    """
    if not _ensure_dir(SHARED_DIR):
        return False

    meta_file = BRIDGE_META
    try:
        raw = _safe_read(meta_file)
        meta = json.loads(raw) if raw else {"events": []}
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"meta.json 格式损坏，重置: {e}")
        meta = {"events": []}

    event = {
        "type": event_type,
        "timestamp": datetime.now().isoformat(),
        **data,
    }
    meta["events"].append(event)
    # 保留最近 MAX_EVENTS 条
    meta["events"] = meta["events"][-MAX_EVENTS:]

    if _safe_write(meta_file, json.dumps(meta, ensure_ascii=False, indent=2)):
        logger.debug(f"写入事件: {event_type}")
        return True
    return False


def read_shared_events(
    event_type: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """
    读取共用互通事件。

    Args:
        event_type: 过滤特定类型，None 则返回全部
        limit: 返回最近 N 条

    Returns:
        事件列表
    """
    meta_file = BRIDGE_META
    if not meta_file.exists():
        return []

    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"读取 meta.json 失败: {e}")
        return []

    events = meta.get("events", [])
    if event_type:
        events = [e for e in events if e.get("type") == event_type]
    return events[-limit:]


def read_workbuddy_log(lines: int = 20) -> list[str]:
    """读取 WorkBuddy 写给 Hermes 的最新日志"""
    log_file = SHARED_DIR / "workbuddy.log"
    if not log_file.exists():
        return []

    try:
        all_lines = log_file.read_text(encoding="utf-8").strip().split("\n")
        return all_lines[-lines:]
    except (OSError, UnicodeDecodeError) as e:
        logger.warning(f"读取 workbuddy.log 失败: {e}")
        return []
