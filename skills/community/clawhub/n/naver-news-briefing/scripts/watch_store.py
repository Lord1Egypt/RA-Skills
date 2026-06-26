from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Iterable, List

from _paths import DB_PATH, ensure_data_dir


SCHEMA = """
CREATE TABLE IF NOT EXISTS watch_rules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  raw_query TEXT NOT NULL,
  search_query TEXT NOT NULL,
  db_keyword TEXT NOT NULL,
  exclude_json TEXT NOT NULL,
  fetch_key TEXT NOT NULL,
  days INTEGER,
  limit_count INTEGER NOT NULL,
  label TEXT,
  tags_json TEXT NOT NULL DEFAULT '[]',
  context TEXT,
  template TEXT,
  schedule_json TEXT NOT NULL DEFAULT '{}',
  operator_hint_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  last_checked_at TEXT,
  last_new_count INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS seen_items (
  watch_id INTEGER NOT NULL,
  link TEXT NOT NULL,
  published_at TEXT,
  first_seen_at TEXT NOT NULL,
  PRIMARY KEY (watch_id, link),
  FOREIGN KEY (watch_id) REFERENCES watch_rules(id) ON DELETE CASCADE
);
"""


@contextmanager
def connect():
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA)
        columns = {row[1] for row in conn.execute("PRAGMA table_info(watch_rules)").fetchall()}
        migrations = {
            "label": "ALTER TABLE watch_rules ADD COLUMN label TEXT",
            "tags_json": "ALTER TABLE watch_rules ADD COLUMN tags_json TEXT NOT NULL DEFAULT '[]'",
            "context": "ALTER TABLE watch_rules ADD COLUMN context TEXT",
            "template": "ALTER TABLE watch_rules ADD COLUMN template TEXT",
            "schedule_json": "ALTER TABLE watch_rules ADD COLUMN schedule_json TEXT NOT NULL DEFAULT '{}'",
            "operator_hint_json": "ALTER TABLE watch_rules ADD COLUMN operator_hint_json TEXT NOT NULL DEFAULT '{}'",
        }
        for column, sql in migrations.items():
            if column not in columns:
                conn.execute(sql)
        yield conn
        conn.commit()
    finally:
        conn.close()


def _normalize_tags(tags: Iterable[str] | None) -> List[str]:
    seen = set()
    result: List[str] = []
    for tag in tags or []:
        value = str(tag or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def list_rules() -> List[Dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, name, raw_query, search_query, db_keyword, exclude_json, fetch_key, days, limit_count, label, tags_json, context, template, schedule_json, operator_hint_json, created_at, updated_at, last_checked_at, last_new_count FROM watch_rules ORDER BY name"
        ).fetchall()
    result = []
    for row in rows:
        result.append(
            {
                "id": row[0],
                "name": row[1],
                "raw_query": row[2],
                "search_query": row[3],
                "db_keyword": row[4],
                "exclude_words": json.loads(row[5]),
                "fetch_key": row[6],
                "days": row[7],
                "limit": row[8],
                "label": row[9],
                "tags": json.loads(row[10] or "[]"),
                "context": row[11],
                "template": row[12],
                "schedule": json.loads(row[13] or "{}"),
                "operator_hints": json.loads(row[14] or "{}"),
                "created_at": row[15],
                "updated_at": row[16],
                "last_checked_at": row[17],
                "last_new_count": row[18],
            }
        )
    return result


def add_rule(*, name: str, raw_query: str, search_query: str, db_keyword: str, exclude_words: List[str], fetch_key: str, days: int | None, limit: int, label: str | None = None, tags: Iterable[str] | None = None, context: str | None = None, template: str | None = None, schedule: Dict[str, Any] | None = None, operator_hints: Dict[str, Any] | None = None) -> Dict[str, Any]:
    now = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO watch_rules(name, raw_query, search_query, db_keyword, exclude_json, fetch_key, days, limit_count, label, tags_json, context, template, schedule_json, operator_hint_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                raw_query,
                search_query,
                db_keyword,
                json.dumps(exclude_words, ensure_ascii=False),
                fetch_key,
                days,
                limit,
                label,
                json.dumps(_normalize_tags(tags), ensure_ascii=False),
                context,
                template,
                json.dumps(schedule or {}, ensure_ascii=False),
                json.dumps(operator_hints or {}, ensure_ascii=False),
                now,
                now,
            ),
        )
    return get_rule(name)


def get_rule(name_or_id: str | int) -> Dict[str, Any]:
    query = "SELECT id, name, raw_query, search_query, db_keyword, exclude_json, fetch_key, days, limit_count, label, tags_json, context, template, schedule_json, operator_hint_json, created_at, updated_at, last_checked_at, last_new_count FROM watch_rules WHERE {} = ?"
    field = "id" if isinstance(name_or_id, int) or str(name_or_id).isdigit() else "name"
    with connect() as conn:
        row = conn.execute(query.format(field), (int(name_or_id) if field == "id" else name_or_id,)).fetchone()
    if not row:
        raise KeyError(f"watch rule not found: {name_or_id}")
    return {
        "id": row[0], "name": row[1], "raw_query": row[2], "search_query": row[3], "db_keyword": row[4],
        "exclude_words": json.loads(row[5]), "fetch_key": row[6], "days": row[7], "limit": row[8],
        "label": row[9], "tags": json.loads(row[10] or "[]"), "context": row[11], "template": row[12],
        "schedule": json.loads(row[13] or "{}"), "operator_hints": json.loads(row[14] or "{}"),
        "created_at": row[15], "updated_at": row[16], "last_checked_at": row[17], "last_new_count": row[18],
    }


def remove_rule(name_or_id: str | int) -> int:
    field = "id" if isinstance(name_or_id, int) or str(name_or_id).isdigit() else "name"
    with connect() as conn:
        cur = conn.execute(f"DELETE FROM watch_rules WHERE {field} = ?", (int(name_or_id) if field == 'id' else name_or_id,))
        return int(cur.rowcount or 0)


def mark_seen(watch_id: int, items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    now = datetime.now().isoformat(timespec="seconds")
    new_items: List[Dict[str, Any]] = []
    with connect() as conn:
        for item in items:
            link = str(item.get("link", "") or "").strip()
            if not link:
                continue
            exists = conn.execute("SELECT 1 FROM seen_items WHERE watch_id = ? AND link = ?", (watch_id, link)).fetchone()
            if exists:
                continue
            conn.execute(
                "INSERT INTO seen_items(watch_id, link, published_at, first_seen_at) VALUES (?, ?, ?, ?)",
                (watch_id, link, item.get("pub_date_iso"), now),
            )
            new_items.append(item)
        conn.execute(
            "UPDATE watch_rules SET last_checked_at = ?, last_new_count = ? WHERE id = ?",
            (now, len(new_items), watch_id),
        )
    return new_items
