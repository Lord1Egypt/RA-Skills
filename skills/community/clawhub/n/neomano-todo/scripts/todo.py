#!/usr/bin/env python3
"""SQLite-backed TODO manager (deterministic helper for the neomano-todo skill).

This script manages tasks, tags, and reminder metadata in a local SQLite DB.
Reminder scheduling itself is handled by OpenClaw cron (outside this script),
but the script stores remind_at + cron_job_id to support create/update/cancel.

Environment variables:
- NEOMANO_TODO_DB_PATH: path to sqlite db file.

Priority convention:
- 1 = high
- 2 = medium
- 3 = low

Exit codes:
- 0 success
- 2 usage/validation error
- 1 unexpected error
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_DB_PATH = os.path.expanduser("~/.openclaw/workspace/data/neomano-todo.sqlite3")


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def utc_now_iso() -> str:
    return utc_now().isoformat()


def parse_iso(dt: str) -> datetime:
    # Minimal ISO parser: expects timezone-aware ISO strings.
    # Python's fromisoformat handles offsets like -05:00.
    out = datetime.fromisoformat(dt)
    if out.tzinfo is None:
        raise ValueError("timestamp must be timezone-aware ISO-8601 (e.g. 2026-03-22T16:30:00-05:00)")
    return out


def get_db_path() -> str:
    return os.path.expanduser(os.environ.get("NEOMANO_TODO_DB_PATH", DEFAULT_DB_PATH))


def connect(db_path: str) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          notes TEXT,
          status TEXT NOT NULL DEFAULT 'open',
          priority INTEGER NOT NULL DEFAULT 2,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL,
          last_touched_at TEXT NOT NULL,
          due_at TEXT,
          remind_at TEXT,
          completed_at TEXT,
          cron_job_id TEXT
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tags (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL UNIQUE
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS task_tags (
          task_id INTEGER NOT NULL,
          tag_id INTEGER NOT NULL,
          PRIMARY KEY (task_id, tag_id),
          FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
          FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        );
        """
    )

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_status_priority
        ON tasks(status, priority, id);
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_due
        ON tasks(due_at);
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_remind
        ON tasks(remind_at);
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_touched
        ON tasks(last_touched_at);
        """
    )
    conn.commit()


VALID_STATUSES = {"open", "done", "blocked", "expired", "forgotten"}


def validate_priority(p: int) -> None:
    if p < 1 or p > 3:
        raise ValueError("priority must be 1 (high), 2 (medium), or 3 (low)")


def normalize_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    parts = [p.strip() for p in raw.replace("#", "").split(",")]
    tags = [p for p in parts if p]
    seen: set[str] = set()
    out: list[str] = []
    for t in tags:
        k = t.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(t)
    return out


@dataclass
class Task:
    id: int
    title: str
    notes: str | None
    status: str
    priority: int
    created_at: str
    updated_at: str
    last_touched_at: str
    due_at: str | None
    remind_at: str | None
    completed_at: str | None
    cron_job_id: str | None
    tags: list[str]


def print_json(obj: Any) -> None:
    import json

    json.dump(obj, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def fetch_task(conn: sqlite3.Connection, task_id: int) -> Task | None:
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        return None
    tag_rows = conn.execute(
        """
        SELECT t.name
        FROM tags t
        JOIN task_tags tt ON tt.tag_id = t.id
        WHERE tt.task_id = ?
        ORDER BY t.name ASC
        """,
        (task_id,),
    ).fetchall()
    tags = [str(r[0]) for r in tag_rows]
    return Task(
        id=int(row["id"]),
        title=str(row["title"]),
        notes=row["notes"],
        status=str(row["status"]),
        priority=int(row["priority"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
        last_touched_at=str(row["last_touched_at"]),
        due_at=row["due_at"],
        remind_at=row["remind_at"],
        completed_at=row["completed_at"],
        cron_job_id=row["cron_job_id"],
        tags=tags,
    )


def ensure_tags(conn: sqlite3.Connection, names: list[str]) -> list[int]:
    ids: list[int] = []
    for n in names:
        name = n.strip()
        if not name:
            continue
        conn.execute("INSERT OR IGNORE INTO tags(name) VALUES(?)", (name,))
        row = conn.execute("SELECT id FROM tags WHERE name = ?", (name,)).fetchone()
        ids.append(int(row[0]))
    return ids


def set_task_tags(conn: sqlite3.Connection, task_id: int, tag_names: list[str]) -> None:
    conn.execute("DELETE FROM task_tags WHERE task_id = ?", (task_id,))
    tag_ids = ensure_tags(conn, tag_names)
    for tid in tag_ids:
        conn.execute(
            "INSERT OR IGNORE INTO task_tags(task_id, tag_id) VALUES(?, ?)",
            (task_id, tid),
        )


def cmd_add(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    now = utc_now_iso()
    priority = int(args.priority)
    validate_priority(priority)

    cur = conn.execute(
        """
        INSERT INTO tasks(
          title, notes, status, priority,
          created_at, updated_at, last_touched_at,
          due_at, remind_at, completed_at, cron_job_id
        )
        VALUES(?, ?, 'open', ?, ?, ?, ?, ?, ?, NULL, NULL)
        """,
        (args.title, args.notes, priority, now, now, now, args.due_at, args.remind_at),
    )
    task_id = int(cur.lastrowid)
    set_task_tags(conn, task_id, normalize_tags(args.tags))
    conn.commit()

    task = fetch_task(conn, task_id)
    print_json({"ok": True, "task": asdict(task)})


def cmd_get(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task = fetch_task(conn, int(args.id))
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    print_json({"ok": True, "task": asdict(task)})


def cmd_list(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    status = args.status
    tag = args.tag
    order = args.order

    where = ["1=1"]
    params: list[Any] = []

    if status:
        where.append("tasks.status = ?")
        params.append(status)

    join = ""
    if tag:
        join = (
            "JOIN task_tags tt ON tt.task_id = tasks.id "
            "JOIN tags tg ON tg.id = tt.tag_id"
        )
        where.append("lower(tg.name) = lower(?)")
        params.append(tag)

    if order == "priority":
        order_by = "ORDER BY tasks.priority ASC, tasks.id ASC"
    elif order == "recent":
        order_by = "ORDER BY tasks.id DESC"
    elif order == "due":
        order_by = "ORDER BY (tasks.due_at IS NULL) ASC, tasks.due_at ASC, tasks.priority ASC"
    else:
        raise ValueError("invalid order")

    rows = conn.execute(
        f"SELECT tasks.id FROM tasks {join} WHERE {' AND '.join(where)} {order_by}",
        tuple(params),
    ).fetchall()

    tasks: list[dict[str, Any]] = []
    for r in rows:
        t = fetch_task(conn, int(r[0]))
        if t:
            tasks.append(asdict(t))

    print_json({"ok": True, "count": len(tasks), "tasks": tasks})


def cmd_done(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task_id = int(args.id)
    now = utc_now_iso()
    conn.execute(
        """
        UPDATE tasks
        SET status = 'done', completed_at = ?, updated_at = ?, last_touched_at = ?
        WHERE id = ?
        """,
        (now, now, now, task_id),
    )
    conn.commit()
    task = fetch_task(conn, task_id)
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    print_json({"ok": True, "task": asdict(task)})


def cmd_reopen(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task_id = int(args.id)
    now = utc_now_iso()
    conn.execute(
        """
        UPDATE tasks
        SET status = 'open', completed_at = NULL, updated_at = ?, last_touched_at = ?
        WHERE id = ?
        """,
        (now, now, task_id),
    )
    conn.commit()
    task = fetch_task(conn, task_id)
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    print_json({"ok": True, "task": asdict(task)})


def cmd_set_priority(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task_id = int(args.id)
    p = int(args.priority)
    validate_priority(p)
    now = utc_now_iso()
    conn.execute(
        "UPDATE tasks SET priority = ?, updated_at = ?, last_touched_at = ? WHERE id = ?",
        (p, now, now, task_id),
    )
    conn.commit()
    task = fetch_task(conn, task_id)
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    print_json({"ok": True, "task": asdict(task)})


def cmd_set_status(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task_id = int(args.id)
    status = str(args.status)
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of: {sorted(VALID_STATUSES)}")
    now = utc_now_iso()
    completed_at = now if status == "done" else None
    conn.execute(
        """
        UPDATE tasks
        SET status = ?, completed_at = ?, updated_at = ?, last_touched_at = ?
        WHERE id = ?
        """,
        (status, completed_at, now, now, task_id),
    )
    conn.commit()
    task = fetch_task(conn, task_id)
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    print_json({"ok": True, "task": asdict(task)})


def cmd_set_tags(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task_id = int(args.id)
    now = utc_now_iso()
    conn.execute(
        "UPDATE tasks SET updated_at = ?, last_touched_at = ? WHERE id = ?",
        (now, now, task_id),
    )
    set_task_tags(conn, task_id, normalize_tags(args.tags))
    conn.commit()
    task = fetch_task(conn, task_id)
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    print_json({"ok": True, "task": asdict(task)})


def cmd_set_dates(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task_id = int(args.id)
    now = utc_now_iso()
    conn.execute(
        """
        UPDATE tasks
        SET due_at = ?, remind_at = ?, updated_at = ?, last_touched_at = ?
        WHERE id = ?
        """,
        (args.due_at, args.remind_at, now, now, task_id),
    )
    conn.commit()
    task = fetch_task(conn, task_id)
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    print_json({"ok": True, "task": asdict(task)})


def cmd_set_cron_job(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task_id = int(args.id)
    now = utc_now_iso()
    conn.execute(
        "UPDATE tasks SET cron_job_id = ?, updated_at = ? WHERE id = ?",
        (args.cron_job_id, now, task_id),
    )
    conn.commit()
    task = fetch_task(conn, task_id)
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    print_json({"ok": True, "task": asdict(task)})


def cmd_stale_candidates(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    # Returns open/blocked tasks that are old enough to review.
    # P3 threshold: 30d, P2 threshold: 45d (defaults from our design).
    now = parse_iso(args.now) if args.now else utc_now()
    p3_days = int(args.p3_days)
    p2_days = int(args.p2_days)

    # Fetch candidates that are not terminal.
    rows = conn.execute(
        """
        SELECT id, priority, last_touched_at
        FROM tasks
        WHERE status IN ('open','blocked')
          AND priority IN (2,3)
        """
    ).fetchall()

    ids: list[int] = []
    for r in rows:
        tid = int(r["id"])
        pr = int(r["priority"])
        touched = parse_iso(str(r["last_touched_at"]))
        age_days = (now - touched).total_seconds() / 86400.0
        if pr == 3 and age_days >= p3_days:
            ids.append(tid)
        elif pr == 2 and age_days >= p2_days:
            ids.append(tid)

    tasks = [asdict(fetch_task(conn, tid)) for tid in ids if fetch_task(conn, tid)]
    print_json({"ok": True, "count": len(tasks), "tasks": tasks, "policy": {"p3_days": p3_days, "p2_days": p2_days}})


def cmd_delete(conn: sqlite3.Connection, args: argparse.Namespace) -> None:
    task_id = int(args.id)
    task = fetch_task(conn, task_id)
    if not task:
        print_json({"ok": False, "error": "not_found"})
        return
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print_json({"ok": True, "deleted": task_id})


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo.py")
    p.add_argument("--db", help="Override db path (else uses NEOMANO_TODO_DB_PATH)")

    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="Add a new task")
    a.add_argument("title")
    a.add_argument("--notes")
    a.add_argument("--priority", default="2", help="1 (high) .. 3 (low)")
    a.add_argument("--due-at", dest="due_at", help="ISO-8601 timestamp (optional)")
    a.add_argument("--remind-at", dest="remind_at", help="ISO-8601 timestamp (optional)")
    a.add_argument("--tags", help="Comma-separated tags, e.g. 'sales,calls'")
    a.set_defaults(func=cmd_add)

    g = sub.add_parser("get", help="Get a task by id")
    g.add_argument("id")
    g.set_defaults(func=cmd_get)

    l = sub.add_parser("list", help="List tasks")
    l.add_argument("--status", choices=sorted(VALID_STATUSES), help="Filter by status")
    l.add_argument("--tag", help="Filter by a single tag name")
    l.add_argument("--order", choices=["priority", "recent", "due"], default="priority")
    l.set_defaults(func=cmd_list)

    d = sub.add_parser("done", help="Mark task done")
    d.add_argument("id")
    d.set_defaults(func=cmd_done)

    r = sub.add_parser("reopen", help="Reopen a task")
    r.add_argument("id")
    r.set_defaults(func=cmd_reopen)

    sp = sub.add_parser("set-priority", help="Set task priority")
    sp.add_argument("id")
    sp.add_argument("priority")
    sp.set_defaults(func=cmd_set_priority)

    ss = sub.add_parser("set-status", help="Set task status")
    ss.add_argument("id")
    ss.add_argument("status", choices=sorted(VALID_STATUSES))
    ss.set_defaults(func=cmd_set_status)

    st = sub.add_parser("set-tags", help="Replace task tags")
    st.add_argument("id")
    st.add_argument("tags", help="Comma-separated")
    st.set_defaults(func=cmd_set_tags)

    sd = sub.add_parser("set-dates", help="Set due_at and/or remind_at")
    sd.add_argument("id")
    sd.add_argument("--due-at", dest="due_at")
    sd.add_argument("--remind-at", dest="remind_at")
    sd.set_defaults(func=cmd_set_dates)

    scj = sub.add_parser("set-cron-job", help="Store associated OpenClaw cron job id")
    scj.add_argument("id")
    scj.add_argument("cron_job_id")
    scj.set_defaults(func=cmd_set_cron_job)

    stale = sub.add_parser("stale-candidates", help="List stale candidates according to the policy")
    stale.add_argument("--p3-days", default="30")
    stale.add_argument("--p2-days", default="45")
    stale.add_argument("--now", help="Override now (ISO-8601, timezone-aware)")
    stale.set_defaults(func=cmd_stale_candidates)

    x = sub.add_parser("delete", help="Delete a task")
    x.add_argument("id")
    x.set_defaults(func=cmd_delete)

    return p


def main() -> int:
    try:
        parser = build_parser()
        args = parser.parse_args()

        db_path = os.path.expanduser(args.db) if args.db else get_db_path()
        conn = connect(db_path)
        init_db(conn)
        args.func(conn, args)
        return 0
    except SystemExit as e:
        return int(e.code) if isinstance(e.code, int) else 2
    except Exception as e:
        sys.stderr.write(f"ERROR: {e}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
