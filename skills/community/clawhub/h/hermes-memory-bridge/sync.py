"""
hermes-memory-bridge / sync.py
WorkBuddy ↔ Hermes 双向同步引擎（带健壮错误处理）
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from config import (
    BRIDGE_META,
    HERMES_DB,
    HERMES_MEMORIES_DIR,
    SHARED_DIR,
    WORKBUDDY_LOG,
    WORKBUDDY_MEMORY_DIR,
    _get_logger,
)

logger = _get_logger("sync")

# ─── 延迟导入（避免循环依赖）────────────────────────────────────────
# 注意：以下导入在运行时通过 bridge.py 的 import 链完成


def sync_workbuddy_to_hermes(
    work_summary: str,
    work_type: str = "task",
    tags: list[str] | None = None,
) -> dict[str, Any]:
    """
    将 WorkBuddy 完成的工作同步到 Hermes 记忆系统。

    三步操作（任一步失败均记录日志并继续）：
    1. 写入 Hermes MEMORY.md
    2. 写入共用互通日志
    3. 写入桥接元事件

    Returns:
        dict，含 status: 'synced' | 'partial' | 'failed'
    """
    from memory_writer import (
        append_hermes_memory,
        write_bridge_event,
        write_shared_log,
    )

    tags = tags or []
    result: dict[str, Any] = {"status": "failed", "entry": None, "log_path": None}
    success_count = 0

    # ① 写入 Hermes MEMORY.md
    try:
        entry = append_hermes_memory(
            target="memory",
            content=work_summary,
            source="WorkBuddy",
        )
        if entry:
            result["entry"] = entry
            success_count += 1
        else:
            logger.error("写入 Hermes MEMORY.md 失败")
    except Exception as e:
        logger.error(f"写入 Hermes MEMORY.md 异常: {e}")

    # ② 写入共用日志
    try:
        log_path = write_shared_log(
            f"[{work_type}] {work_summary}", log_type="workbuddy"
        )
        if log_path:
            result["log_path"] = str(log_path)
            success_count += 1
        else:
            logger.warning("写入共用日志失败")
    except Exception as e:
        logger.error(f"写入共用日志异常: {e}")

    # ③ 写入桥接元事件
    try:
        write_bridge_event("task_done", {
            "summary": work_summary,
            "work_type": work_type,
            "tags": tags,
        })
        success_count += 1
    except Exception as e:
        logger.error(f"写入桥接事件异常: {e}")

    # 综合状态
    if success_count == 3:
        result["status"] = "synced"
    elif success_count > 0:
        result["status"] = "partial"
        logger.warning(f"同步部分成功（{success_count}/3 步）")
    else:
        logger.error("同步全部失败")

    logger.info(f"sync_workbuddy_to_hermes: {result['status']} - {work_summary[:50]}")
    return result


def sync_hermes_to_workbuddy_context(days: int = 7) -> dict[str, Any]:
    """
    将 Hermes 最近的重要上下文同步到 WorkBuddy 可读格式，
    用于在 WorkBuddy 启动时了解 Hermes 侧的最新动态。
    """
    from memory_writer import write_bridge_event

    # 延迟导入 queries
    from queries import (
        get_recent_sessions,
        get_session_stats,
        read_hermes_memory,
    )

    try:
        sessions = get_recent_sessions(days=days)
        stats = get_session_stats(days=days)
        hermes_mem = read_hermes_memory()
    except Exception as e:
        logger.error(f"拉取 Hermes 数据失败: {e}")
        return {
            "sessions": [], "stats": {},
            "summary_text": f"[错误] 无法读取 Hermes 数据: {e}",
            "workbuddy_entries": [],
        }

    summary_lines = [
        f"## Hermes 近 {days} 天动态",
        "",
        f"**会话数**: {stats.get('total_sessions', 0)}",
        f"**消息数**: {stats.get('total_messages', 0)}",
        "",
        "### 最近会话",
    ]

    for s in sessions[:5]:
        try:
            ts = datetime.fromtimestamp(s["started_at"]).strftime("%m-%d %H:%M")
        except (ValueError, KeyError, TypeError):
            ts = "未知时间"
        title = s.get("title") or s.get("source") or "无标题"
        summary_lines.append(f"- [{ts}] {title}")

    # Hermes 记忆中关于 WorkBuddy 的条目
    wb_entries: list[str] = []
    for entry in hermes_mem.get("MEMORY.md", {}).get("entries", []):
        if "WorkBuddy" in entry:
            wb_entries.append(entry)

    if wb_entries:
        summary_lines.extend(["", "### Hermes 中关于 WorkBuddy 的记忆"])
        for e in wb_entries[-5:]:
            summary_lines.append(f"- {e[:200]}")

    summary_text = "\n".join(summary_lines)

    # 记录本次同步事件
    try:
        write_bridge_event("sync", {
            "direction": "hermes_to_workbuddy",
            "days": days,
            "sessions_found": len(sessions),
            "workbuddy_entries_found": len(wb_entries),
        })
    except Exception as e:
        logger.warning(f"写入同步事件失败: {e}")

    logger.debug(f"sync_hermes_to_workbuddy: {len(sessions)} sessions, {len(wb_entries)} WB entries")
    return {
        "sessions": sessions,
        "stats": stats,
        "summary_text": summary_text,
        "workbuddy_entries": wb_entries,
    }


def search_both_memories(keyword: str, days: int = 30) -> dict[str, Any]:
    """
    跨 WorkBuddy 和 Hermes 记忆的全文搜索。
    """
    from queries import search_messages

    if not keyword or len(keyword) < 2:
        logger.debug("关键词过短，跳过搜索")
        return {"keyword": keyword, "hermes": [], "workbuddy": []}

    # Hermes 侧搜索
    hermes_results: list[dict] = []
    try:
        hermes_results = search_messages(keyword, days=days)
    except Exception as e:
        logger.warning(f"Hermes 搜索失败: {e}")

    # WorkBuddy 侧搜索（读日志文件）
    wb_results: list[dict] = []
    try:
        wb_results = _search_workbuddy_memory(keyword)
    except Exception as e:
        logger.warning(f"WorkBuddy 记忆搜索失败: {e}")

    return {
        "keyword": keyword,
        "hermes": hermes_results,
        "workbuddy": wb_results,
    }


def _search_workbuddy_memory(keyword: str) -> list[dict]:
    """在 WorkBuddy 记忆文件中搜索（安全读取）"""
    results: list[dict] = []

    if WORKBUDDY_MEMORY_DIR is None:
        logger.debug("WORKBUDDY_MEMORY_DIR 未找到，跳过搜索")
        return results

    if not WORKBUDDY_MEMORY_DIR.exists():
        logger.debug(f"WorkBuddy 记忆目录不存在: {WORKBUDDY_MEMORY_DIR}")
        return results

    try:
        md_files = list(WORKBUDDY_MEMORY_DIR.glob("*.md"))
    except PermissionError as e:
        logger.warning(f"权限不足，无法扫描 {WORKBUDDY_MEMORY_DIR}: {e}")
        return results
    except OSError as e:
        logger.warning(f"扫描 WorkBuddy 记忆目录失败: {e}")
        return results

    kw_lower = keyword.lower()
    for fpath in md_files:
        try:
            content = fpath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            logger.warning(f"读取 {fpath} 失败: {e}")
            continue

        if kw_lower not in content.lower():
            continue

        lines = content.split("\n")
        for i, line in enumerate(lines):
            if kw_lower in line.lower():
                context = lines[max(0, i - 1):i + 3]
                snippet = " ... ".join(c.strip() for c in context if c.strip())[:200]
                results.append({
                    "file": fpath.name,
                    "line": i + 1,
                    "snippet": snippet,
                })

    logger.debug(f"WorkBuddy 记忆搜索「{keyword}」: {len(results)} 条")
    return results


def read_bridge_status() -> dict[str, Any]:
    """读取桥接状态总览（健壮版本）"""
    status: dict[str, Any] = {
        "hermes_memory_files": [],
        "shared_files": [],
        "recent_events": [],
        "db_exists": HERMES_DB.exists(),
        "workbuddy_memory_dir": str(WORKBUDDY_MEMORY_DIR) if WORKBUDDY_MEMORY_DIR else None,
    }

    # 确保目录存在（不抛异常）
    try:
        HERMES_MEMORIES_DIR.mkdir(parents=True, exist_ok=True)
        SHARED_DIR.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        logger.warning("权限不足，无法创建 Hermes 目录")

    # 列出记忆文件
    try:
        status["hermes_memory_files"] = [
            f.name for f in HERMES_MEMORIES_DIR.glob("*.md")
        ]
    except OSError as e:
        logger.warning(f"无法列出记忆文件: {e}")

    # 列出共用文件
    try:
        status["shared_files"] = [f.name for f in SHARED_DIR.glob("*") if f.is_file()]
    except OSError as e:
        logger.warning(f"无法列出共用文件: {e}")

    # 读取近期事件
    from memory_writer import read_shared_events
    try:
        status["recent_events"] = read_shared_events(limit=10)
    except Exception as e:
        logger.warning(f"读取桥接事件失败: {e}")

    logger.debug(f"read_bridge_status: db={status['db_exists']}, "
                 f"memories={len(status['hermes_memory_files'])}, "
                 f"shared={len(status['shared_files'])}")
    return status
