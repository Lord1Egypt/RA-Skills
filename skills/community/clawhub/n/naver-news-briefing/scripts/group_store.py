from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Iterable, List

from _paths import DB_PATH, ensure_data_dir


SCHEMA = """
CREATE TABLE IF NOT EXISTS keyword_groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  label TEXT,
  tags_json TEXT NOT NULL DEFAULT '[]',
  context TEXT,
  template TEXT,
  schedule_json TEXT NOT NULL DEFAULT '{}',
  operator_hint_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS group_queries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  group_id INTEGER NOT NULL,
  position INTEGER NOT NULL,
  raw_query TEXT NOT NULL,
  FOREIGN KEY (group_id) REFERENCES keyword_groups(id) ON DELETE CASCADE,
  UNIQUE(group_id, position)
);
"""


@contextmanager
def connect():
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(SCHEMA)
        columns = {row[1] for row in conn.execute("PRAGMA table_info(keyword_groups)").fetchall()}
        migrations = {
            "template": "ALTER TABLE keyword_groups ADD COLUMN template TEXT",
            "schedule_json": "ALTER TABLE keyword_groups ADD COLUMN schedule_json TEXT NOT NULL DEFAULT '{}'",
            "operator_hint_json": "ALTER TABLE keyword_groups ADD COLUMN operator_hint_json TEXT NOT NULL DEFAULT '{}'",
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
    normalized: List[str] = []
    for tag in tags or []:
        value = str(tag or "").strip()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    return normalized


def _serialize_group_row(row: sqlite3.Row | tuple[Any, ...], queries: List[str]) -> Dict[str, Any]:
    return {
        "id": row[0],
        "name": row[1],
        "label": row[2],
        "tags": json.loads(row[3] or "[]"),
        "context": row[4],
        "template": row[5],
        "schedule": json.loads(row[6] or "{}"),
        "operator_hints": json.loads(row[7] or "{}"),
        "created_at": row[8],
        "updated_at": row[9],
        "queries": queries,
        "query_count": len(queries),
    }


def _fetch_queries(conn: sqlite3.Connection, group_id: int) -> List[str]:
    rows = conn.execute("SELECT raw_query FROM group_queries WHERE group_id = ? ORDER BY position, id", (group_id,)).fetchall()
    return [row[0] for row in rows]


def list_groups() -> List[Dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute("SELECT id, name, label, tags_json, context, template, schedule_json, operator_hint_json, created_at, updated_at FROM keyword_groups ORDER BY name").fetchall()
        return [_serialize_group_row(row, _fetch_queries(conn, row[0])) for row in rows]


def get_group(name_or_id: str | int) -> Dict[str, Any]:
    field = "id" if isinstance(name_or_id, int) or str(name_or_id).isdigit() else "name"
    with connect() as conn:
        row = conn.execute(
            f"SELECT id, name, label, tags_json, context, template, schedule_json, operator_hint_json, created_at, updated_at FROM keyword_groups WHERE {field} = ?",
            (int(name_or_id) if field == "id" else name_or_id,),
        ).fetchone()
        if not row:
            raise KeyError(f"keyword group not found: {name_or_id}")
        return _serialize_group_row(row, _fetch_queries(conn, row[0]))


def create_group(*, name: str, queries: List[str], label: str | None = None, tags: Iterable[str] | None = None, context: str | None = None, template: str | None = None, schedule: Dict[str, Any] | None = None, operator_hints: Dict[str, Any] | None = None) -> Dict[str, Any]:
    clean_queries = [str(query or "").strip() for query in queries if str(query or "").strip()]
    if not clean_queries:
        raise ValueError("키워드 그룹에는 최소 1개 이상의 쿼리가 필요합니다.")
    now = datetime.now().isoformat(timespec="seconds")
    tag_values = _normalize_tags(tags)
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO keyword_groups(name, label, tags_json, context, template, schedule_json, operator_hint_json, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, label, json.dumps(tag_values, ensure_ascii=False), context, template, json.dumps(schedule or {}, ensure_ascii=False), json.dumps(operator_hints or {}, ensure_ascii=False), now, now),
        )
        group_id = int(cur.lastrowid)
        for idx, query in enumerate(clean_queries, start=1):
            conn.execute("INSERT INTO group_queries(group_id, position, raw_query) VALUES (?, ?, ?)", (group_id, idx, query))
    return get_group(name)


def update_group(name_or_id: str | int, *, label: str | None = None, context: str | None = None, tags: Iterable[str] | None | object = None, template: str | None = None, schedule: Dict[str, Any] | None = None, operator_hints: Dict[str, Any] | None = None, replace_queries: List[str] | None = None, add_queries: List[str] | None = None, remove_queries: List[str] | None = None) -> Dict[str, Any]:
    group = get_group(name_or_id)
    group_id = group["id"]
    new_label = group["label"] if label is None else label
    new_context = group["context"] if context is None else context
    new_template = group["template"] if template is None else template
    new_schedule = group["schedule"] if schedule is None else schedule
    new_operator_hints = group["operator_hints"] if operator_hints is None else operator_hints
    new_tags = group["tags"] if tags is None else _normalize_tags(tags)  # type: ignore[arg-type]

    queries = list(group["queries"])
    if replace_queries is not None:
        queries = [str(query or "").strip() for query in replace_queries if str(query or "").strip()]
    else:
        for query in add_queries or []:
            cleaned = str(query or "").strip()
            if cleaned and cleaned not in queries:
                queries.append(cleaned)
        for query in remove_queries or []:
            cleaned = str(query or "").strip()
            queries = [item for item in queries if item != cleaned]
    if not queries:
        raise ValueError("키워드 그룹에는 최소 1개 이상의 쿼리가 남아 있어야 합니다.")

    now = datetime.now().isoformat(timespec="seconds")
    with connect() as conn:
        conn.execute(
            "UPDATE keyword_groups SET label = ?, tags_json = ?, context = ?, template = ?, schedule_json = ?, operator_hint_json = ?, updated_at = ? WHERE id = ?",
            (new_label, json.dumps(new_tags, ensure_ascii=False), new_context, new_template, json.dumps(new_schedule, ensure_ascii=False), json.dumps(new_operator_hints, ensure_ascii=False), now, group_id),
        )
        conn.execute("DELETE FROM group_queries WHERE group_id = ?", (group_id,))
        for idx, query in enumerate(queries, start=1):
            conn.execute("INSERT INTO group_queries(group_id, position, raw_query) VALUES (?, ?, ?)", (group_id, idx, query))
    return get_group(group_id)


def remove_group(name_or_id: str | int) -> int:
    field = "id" if isinstance(name_or_id, int) or str(name_or_id).isdigit() else "name"
    with connect() as conn:
        cur = conn.execute(f"DELETE FROM keyword_groups WHERE {field} = ?", (int(name_or_id) if field == "id" else name_or_id,))
        return int(cur.rowcount or 0)
