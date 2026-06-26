"""SQLite schema + minimal CRUD. 3 tables: tickets / draws / tasks."""
from __future__ import annotations

import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

CN_TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(CN_TZ).isoformat(timespec="seconds")


def cn_now() -> datetime:
    return datetime.now(CN_TZ)


def data_dir() -> Path:
    override = os.environ.get("LOTTO_AGENT_DATA_DIR")
    if override:
        return Path(override)
    return Path.home() / ".openclaw" / "workspace" / "lotto-agent-data"


def db_path() -> Path:
    return data_dir() / "lottery.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
  id            INTEGER PRIMARY KEY,
  lottery       TEXT NOT NULL,
  play_type     TEXT,
  numbers_json  TEXT NOT NULL,
  cost          REAL NOT NULL,
  multiple      INTEGER NOT NULL DEFAULT 1,
  is_additional INTEGER NOT NULL DEFAULT 0,
  batch_uuid    TEXT,
  issue         TEXT,
  draw_date     TEXT,
  status        TEXT NOT NULL DEFAULT 'active',
  prize_amount  REAL NOT NULL DEFAULT 0,
  prize_level   TEXT,
  prize_pending INTEGER NOT NULL DEFAULT 0,
  created_at    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tickets_lottery_issue ON tickets(lottery, issue);
CREATE INDEX IF NOT EXISTS idx_tickets_lottery_date  ON tickets(lottery, draw_date);
CREATE INDEX IF NOT EXISTS idx_tickets_status        ON tickets(status);

CREATE TABLE IF NOT EXISTS draws (
  lottery            TEXT NOT NULL,
  issue              TEXT NOT NULL,
  draw_date          TEXT,
  numbers_json       TEXT,
  prize_pool         REAL,
  prize_details_json TEXT,
  next_issue         TEXT,
  next_draw_date     TEXT,
  next_buy_end_time  TEXT,
  raw_json           TEXT,
  fetched_at         TEXT,
  PRIMARY KEY (lottery, issue)
);
CREATE INDEX IF NOT EXISTS idx_draws_date ON draws(lottery, draw_date);

CREATE TABLE IF NOT EXISTS tasks (
  id               INTEGER PRIMARY KEY,
  action           TEXT NOT NULL,
  params_json      TEXT,
  schedule_kind    TEXT NOT NULL,
  schedule_spec    TEXT,
  time_start       TEXT,
  time_end         TEXT,
  random_window    INTEGER NOT NULL DEFAULT 0,
  enabled          INTEGER NOT NULL DEFAULT 1,
  last_run_key     TEXT,
  last_run_at      TEXT,
  planned_run_key  TEXT,
  planned_run_time TEXT,
  delivery_json    TEXT,
  raw_text         TEXT,
  created_at       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_enabled ON tasks(enabled);
"""


def init_db() -> None:
    data_dir().mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.executescript(SCHEMA)
        conn.commit()


@contextmanager
def connect():
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(query: str, params: Iterable[Any] = ()) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(query, tuple(params)).fetchall()
        return [dict(row) for row in rows]


def fetch_one(query: str, params: Iterable[Any] = ()) -> dict[str, Any] | None:
    with connect() as conn:
        row = conn.execute(query, tuple(params)).fetchone()
        return dict(row) if row else None


def execute(query: str, params: Iterable[Any] = ()) -> int:
    with connect() as conn:
        cur = conn.execute(query, tuple(params))
        conn.commit()
        return int(cur.lastrowid or cur.rowcount or 0)


# Tickets ---------------------------------------------------------------
def insert_ticket(ticket: dict[str, Any]) -> int:
    return execute(
        """INSERT INTO tickets
           (lottery, play_type, numbers_json, cost, multiple, is_additional,
            batch_uuid, issue, draw_date, status, prize_amount, prize_level,
            prize_pending, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            ticket["lottery"], ticket.get("play_type"),
            json.dumps(ticket["numbers"], ensure_ascii=False),
            float(ticket["cost"]), int(ticket.get("multiple", 1)),
            int(bool(ticket.get("is_additional"))),
            ticket.get("batch_uuid"), ticket.get("issue"), ticket.get("draw_date"),
            ticket.get("status", "active"),
            float(ticket.get("prize_amount", 0)),
            ticket.get("prize_level"),
            int(bool(ticket.get("prize_pending", False))),
            ticket.get("created_at") or now_iso(),
        ),
    )


def cancel_recent(limit: int = 10) -> int:
    with connect() as conn:
        rows = conn.execute(
            "SELECT id FROM tickets WHERE status='active' ORDER BY id DESC LIMIT ?",
            (int(limit),),
        ).fetchall()
        ids = [int(row["id"]) for row in rows]
        if not ids:
            return 0
        ph = ",".join("?" for _ in ids)
        conn.execute(f"UPDATE tickets SET status='cancelled' WHERE id IN ({ph})", ids)
        conn.commit()
        return len(ids)


def update_ticket_prize(ticket_id: int, prize_amount: float, prize_level: str, pending: bool) -> None:
    execute(
        """UPDATE tickets SET prize_amount=?, prize_level=?, prize_pending=?,
           status=CASE WHEN ? > 0 OR ? = 1 THEN 'matched' ELSE 'matched' END
           WHERE id=?""",
        (float(prize_amount), prize_level or "", int(bool(pending)),
         float(prize_amount), int(bool(pending)), int(ticket_id)),
    )


# Draws ---------------------------------------------------------------
def upsert_draw(draw: dict[str, Any]) -> None:
    execute(
        """INSERT INTO draws
           (lottery, issue, draw_date, numbers_json, prize_pool,
            prize_details_json, next_issue, next_draw_date, next_buy_end_time,
            raw_json, fetched_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(lottery, issue) DO UPDATE SET
             draw_date=excluded.draw_date,
             numbers_json=excluded.numbers_json,
             prize_pool=excluded.prize_pool,
             prize_details_json=excluded.prize_details_json,
             next_issue=excluded.next_issue,
             next_draw_date=excluded.next_draw_date,
             next_buy_end_time=excluded.next_buy_end_time,
             raw_json=excluded.raw_json,
             fetched_at=excluded.fetched_at""",
        (
            draw["lottery"], draw["issue"], draw.get("draw_date"),
            json.dumps(draw.get("numbers", {}), ensure_ascii=False),
            _to_float(draw.get("prize_pool")),
            json.dumps(draw.get("prize_details", []), ensure_ascii=False),
            draw.get("next_issue"), draw.get("next_draw_date"),
            draw.get("next_buy_end_time"),
            json.dumps(draw.get("raw"), ensure_ascii=False) if draw.get("raw") else None,
            draw.get("fetched_at") or now_iso(),
        ),
    )


def latest_draw(lottery: str) -> dict[str, Any] | None:
    return fetch_one(
        """SELECT * FROM draws WHERE lottery=?
           ORDER BY COALESCE(draw_date,'') DESC, issue DESC LIMIT 1""",
        (lottery,),
    )


# Tasks ---------------------------------------------------------------
def insert_task(task: dict[str, Any]) -> int:
    return execute(
        """INSERT INTO tasks
           (action, params_json, schedule_kind, schedule_spec, time_start,
            time_end, random_window, enabled, delivery_json, raw_text, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            task["action"],
            json.dumps(task.get("params", {}), ensure_ascii=False),
            task["schedule_kind"], task.get("schedule_spec"),
            task.get("time_start"), task.get("time_end"),
            int(bool(task.get("random_window"))),
            int(task.get("enabled", 1)),
            json.dumps(task.get("delivery"), ensure_ascii=False) if task.get("delivery") else None,
            task.get("raw_text"),
            task.get("created_at") or now_iso(),
        ),
    )


def list_enabled_tasks() -> list[dict[str, Any]]:
    return fetch_all("SELECT * FROM tasks WHERE enabled=1 ORDER BY id ASC")


def list_all_tasks(include_disabled: bool = False) -> list[dict[str, Any]]:
    if include_disabled:
        return fetch_all("SELECT * FROM tasks ORDER BY id DESC")
    return fetch_all("SELECT * FROM tasks WHERE enabled=1 ORDER BY id DESC")


def disable_task(task_id: int) -> int:
    return execute("UPDATE tasks SET enabled=0 WHERE id=?", (int(task_id),))


def mark_task_run(task_id: int, run_key: str) -> None:
    execute(
        "UPDATE tasks SET last_run_key=?, last_run_at=? WHERE id=?",
        (run_key, now_iso(), int(task_id)),
    )


def set_task_planned(task_id: int, run_key: str, planned_time: str) -> None:
    execute(
        "UPDATE tasks SET planned_run_key=?, planned_run_time=? WHERE id=?",
        (run_key, planned_time, int(task_id)),
    )


# Helpers -------------------------------------------------------------
def new_batch_uuid() -> str:
    return uuid.uuid4().hex[:12]


def _to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    text = str(value).strip().replace(",", "").replace("元", "")
    mult = 1.0
    if text.endswith("亿"):
        mult, text = 1e8, text[:-1]
    elif text.endswith("万"):
        mult, text = 1e4, text[:-1]
    try:
        return float(text) * mult
    except ValueError:
        digits = "".join(ch for ch in text if ch.isdigit() or ch == ".")
        return float(digits) * mult if digits else None
