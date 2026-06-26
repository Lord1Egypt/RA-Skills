#!/usr/bin/env python3
"""
Dream Database Operations
==========================
Database access layer for dream consolidation system.

Handles:
  - Table creation and schema management
  - Memory loading from multiple table formats
  - Insight/pattern/session persistence
  - Query helpers for historical data

Author: Lilu / nima-core
"""

from __future__ import annotations

import os
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

__all__ = [
    "ensure_tables",
    "load_memories",
    "load_sqlite_turns",
    "open_connection",
    "MAX_MEMORIES",
    "MIN_IMPORTANCE",
]

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
MAX_MEMORIES = int(os.environ.get("NIMA_DREAM_MAX_MEMORIES", 500))
MIN_IMPORTANCE = 0.2


# ── Database Connection ────────────────────────────────────────────────────────

def open_connection(db_path: Path) -> sqlite3.Connection:
    """Open a database connection with Row factory."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


# ── Table Management ───────────────────────────────────────────────────────────

def ensure_tables(conn: sqlite3.Connection) -> None:
    """Ensure dream consolidation tables exist in the database."""
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS nima_insights (
        id          TEXT PRIMARY KEY,
        type        TEXT,
        content     TEXT NOT NULL,
        confidence  REAL DEFAULT 0.5,
        sources     TEXT,
        domains     TEXT,
        timestamp   TEXT,
        importance  REAL DEFAULT 0.5,
        bot_name    TEXT
    );

    CREATE TABLE IF NOT EXISTS nima_patterns (
        id          TEXT PRIMARY KEY,
        name        TEXT,
        description TEXT,
        occurrences INTEGER DEFAULT 1,
        domains     TEXT,
        examples    TEXT,
        first_seen  TEXT,
        last_seen   TEXT,
        strength    REAL DEFAULT 0.5,
        bot_name    TEXT
    );

    CREATE TABLE IF NOT EXISTS nima_dream_runs (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id          TEXT,
        started_at          TEXT,
        ended_at            TEXT,
        hours               INTEGER,
        memories_processed  INTEGER,
        patterns_found      INTEGER,
        insights_generated  INTEGER,
        top_domains         TEXT,
        dominant_emotion    TEXT,
        narrative           TEXT,
        bot_name            TEXT
    );
    """)
    conn.commit()


# ── Memory Loading ─────────────────────────────────────────────────────────────

def load_memories(conn: sqlite3.Connection, hours: int) -> List[Dict]:
    """
    Load memories from the memories table within the specified time window.

    Args:
        conn: Database connection
        hours: Number of hours to look back

    Returns:
        List of memory dictionaries
    """
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    try:
        rows = conn.execute("""
            SELECT id, text, summary, who, timestamp, importance,
                   layer, themes, memory_type
            FROM memories
            WHERE timestamp >= ?
              AND importance >= ?
              AND (is_ghost IS NULL OR is_ghost = 0)
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        """, (since, MIN_IMPORTANCE, MAX_MEMORIES)).fetchall()
        return [dict(r) for r in rows]
    except sqlite3.OperationalError as e:
        logger.warning(f"Could not load memories: {e}")
        return []


def load_sqlite_turns(conn: sqlite3.Connection, hours: int) -> List[Dict]:
    """
    Load memories from episodes table (graph.sqlite compatibility).

    Alternative table format for systems using raw SQLite episodes storage.

    Args:
        conn: Database connection
        hours: Number of hours to look back

    Returns:
        List of memory dictionaries normalized to standard format
    """
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    try:
        rows = conn.execute("""
            SELECT id, content, timestamp, source, properties_json
            FROM episodes
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (since, MAX_MEMORIES)).fetchall()
        result = []
        for r in rows:
            content = r["content"] or ""
            if len(content) < 10:
                continue
            props = {}
            try:
                props = json.loads(r["properties_json"] or "{}")
            except (json.JSONDecodeError, TypeError):
                pass
            affect = props.get("affect", {})
            dominant_emotion = None
            if affect:
                dominant_emotion = max(affect.items(), key=lambda x: x[1])[0]
            result.append({
                "id": r["id"],
                "text": content,
                "summary": content[:120],
                "who": props.get("who", r["source"] or ""),
                "timestamp": r["timestamp"],
                "importance": props.get("importance", 0.5),
                "affect": affect,
                "dominant_emotion": dominant_emotion,
                "participants": [props["who"]] if props.get("who") and props["who"] != "self" else [],
            })
        return result
    except sqlite3.OperationalError:
        return []
