"""
hermes-memory-bridge / queries.py
Hermes state.db 查询封装（带健壮错误处理）
"""
from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Any

from config import HERMES_DB, _get_logger

logger = _get_logger("queries")

# ─── 异常类 ─────────────────────────────────────────────────────────
class HermesDBError(Exception):
    """Hermes 数据库操作异常"""
    pass


class MemoryFileError(Exception):
    """记忆文件读写异常"""
    pass


# ─── 内部工具 ───────────────────────────────────────────────────────

def _row2dict(row: sqlite3.Row) -> dict:
    return dict(row)


def _safe_connect(path: str) -> sqlite3.Connection:
    """建立数据库连接，带异常处理"""
    try:
        conn = sqlite3.connect(path, timeout=5.0)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"数据库连接失败: {e}")
        raise HermesDBError(f"无法连接数据库: {e}") from e


# ─── 查询接口 ───────────────────────────────────────────────────────

def get_recent_sessions(days: int = 7, limit: int = 20) -> list[dict]:
    """返回最近 N 天的会话列表"""
    if not HERMES_DB.exists():
        logger.debug("Hermes 数据库不存在，返回空列表")
        return []

    try:
        cutoff = datetime.now() - timedelta(days=days)
        with _safe_connect(str(HERMES_DB)) as conn:
            cur = conn.execute(
                """
                SELECT id, source, model, title, started_at, ended_at,
                       end_reason, message_count, tool_call_count,
                       estimated_cost_usd, actual_cost_usd
                FROM sessions
                WHERE started_at > ?
                ORDER BY started_at DESC
                LIMIT ?
                """,
                (cutoff.timestamp(), limit),
            )
            rows = [_row2dict(r) for r in cur.fetchall()]
            logger.debug(f"查询会话: {len(rows)} 条（近 {days} 天）")
            return rows
    except HermesDBError:
        raise
    except Exception as e:
        logger.error(f"查询会话失败: {e}")
        return []


def get_session_messages(session_id: str, limit: int = 50) -> list[dict]:
    """返回指定会话的消息历史"""
    if not HERMES_DB.exists():
        return []

    try:
        with _safe_connect(str(HERMES_DB)) as conn:
            cur = conn.execute(
                """
                SELECT role, content, tool_name, timestamp, finish_reason
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp ASC
                LIMIT ?
                """,
                (session_id, limit),
            )
            return [_row2dict(r) for r in cur.fetchall()]
    except HermesDBError:
        raise
    except Exception as e:
        logger.error(f"查询消息历史失败（session={session_id}）: {e}")
        return []


def search_messages(keyword: str, days: int = 30) -> list[dict]:
    """全文模糊搜索 Hermes 会话"""
    if not HERMES_DB.exists():
        return []

    if not keyword or len(keyword) < 2:
        logger.debug("关键词过短，跳过搜索")
        return []

    try:
        cutoff = datetime.now() - timedelta(days=days)
        with _safe_connect(str(HERMES_DB)) as conn:
            cur = conn.execute(
                """
                SELECT m.session_id, m.role, m.content, m.tool_name, m.timestamp,
                       s.title, s.source
                FROM messages m
                JOIN sessions s ON m.session_id = s.id
                WHERE m.timestamp > ?
                  AND m.content LIKE ?
                ORDER BY m.timestamp DESC
                LIMIT 30
                """,
                (cutoff.timestamp(), f"%{keyword}%"),
            )
            rows = [_row2dict(r) for r in cur.fetchall()]
            logger.debug(f"搜索「{keyword}」: {len(rows)} 条匹配")
            return rows
    except HermesDBError:
        raise
    except Exception as e:
        logger.error(f"搜索消息失败: {e}")
        return []


def search_fts(keyword: str, limit: int = 20) -> list[dict]:
    """使用 FTS5 全文索引搜索（降级为 LIKE 搜索）"""
    if not HERMES_DB.exists():
        return []

    try:
        with _safe_connect(str(HERMES_DB)) as conn:
            cur = conn.execute(
                """
                SELECT m.session_id, m.role, m.content, m.tool_name,
                       s.title, s.started_at,
                       highlight(messages_fts, 0, '**', '**') AS hl_content
                FROM messages_fts
                JOIN messages m ON messages_fts.rowid = m.id
                JOIN sessions s ON m.session_id = s.id
                WHERE messages_fts MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (keyword, limit),
            )
            return [_row2dict(r) for r in cur.fetchall()]
    except sqlite3.OperationalError:
        logger.debug("FTS5 表不可用，降级为 LIKE 搜索")
        return search_messages(keyword, 30)
    except HermesDBError:
        raise
    except Exception as e:
        logger.error(f"FTS 搜索失败: {e}")
        return []


def get_session_stats(days: int = 30) -> dict[str, Any]:
    """获取 Hermes 使用统计"""
    if not HERMES_DB.exists():
        return {"period_days": days, "total_sessions": 0,
                "total_messages": 0, "total_tokens": 0,
                "estimated_cost_usd": 0.0}

    try:
        cutoff = datetime.now() - timedelta(days=days)
        with _safe_connect(str(HERMES_DB)) as conn:
            def count(sql: str, params: tuple) -> int:
                try:
                    return conn.execute(sql, params).fetchone()[0] or 0
                except Exception:
                    return 0

            total = count(
                "SELECT COUNT(*) FROM sessions WHERE started_at > ?",
                (cutoff.timestamp(),),
            )
            total_messages = count(
                """
                SELECT COUNT(*) FROM messages m
                JOIN sessions s ON m.session_id = s.id
                WHERE s.started_at > ?
                """,
                (cutoff.timestamp(),),
            )
            total_tokens = count(
                "SELECT SUM(input_tokens + output_tokens) FROM sessions WHERE started_at > ?",
                (cutoff.timestamp(),),
            )
            total_cost = count(
                """
                SELECT SUM(actual_cost_usd) FROM sessions
                WHERE started_at > ? AND actual_cost_usd IS NOT NULL
                """,
                (cutoff.timestamp(),),
            )

            stats = {
                "period_days": days,
                "total_sessions": total,
                "total_messages": total_messages,
                "total_tokens": total_tokens,
                "estimated_cost_usd": round(float(total_cost), 4),
            }
            logger.debug(f"统计: {stats}")
            return stats
    except HermesDBError:
        raise
    except Exception as e:
        logger.error(f"获取统计失败: {e}")
        return {"period_days": days, "total_sessions": 0,
                "total_messages": 0, "total_tokens": 0,
                "estimated_cost_usd": 0.0}


def read_hermes_memory() -> dict[str, str]:
    """读取 Hermes 内置记忆文件（MEMORY.md / USER.md）"""
    from config import HERMES_MEMORIES_DIR

    result: dict[str, dict] = {}
    for fname in ("MEMORY.md", "USER.md"):
        fpath = HERMES_MEMORIES_DIR / fname
        if not fpath.exists():
            result[fname] = {"entries": [], "raw": ""}
            continue
        try:
            content = fpath.read_text(encoding="utf-8")
            entries = [e.strip() for e in content.split("\n§\n") if e.strip()]
            result[fname] = {"entries": entries, "raw": content}
            logger.debug(f"读取 {fname}: {len(entries)} 条记忆")
        except (OSError, UnicodeDecodeError) as e:
            logger.warning(f"读取 {fpath} 失败: {e}")
            result[fname] = {"entries": [], "raw": ""}
    return result
