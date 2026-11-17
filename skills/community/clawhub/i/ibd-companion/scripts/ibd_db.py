#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import stat
import sys
import uuid
from collections.abc import Mapping
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median
from typing import Any


def resolve_default_db(environ: Mapping[str, str] | None = None) -> Path:
    values = os.environ if environ is None else environ
    override = values.get("IBD_DB_PATH")
    if override:
        return Path(override).expanduser()
    state_override = values.get("OPENCLAW_STATE_DIR")
    state_dir = Path(state_override).expanduser() if state_override else Path.home() / ".openclaw"
    return state_dir / "private" / "ibd" / "ibd.sqlite3"


DEFAULT_DB = resolve_default_db()
YES_NO_UNKNOWN = ("yes", "no", "unknown")
STATUSES = ("pending", "completed", "delayed", "cancelled")
REMINDER_STATUSES = ("pending", "sent", "completed", "cancelled")
REMINDER_KINDS = ("primary", "advance", "due_day")
ABNORMAL_FLAGS = ("low", "high", "normal", "abnormal")


def new_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_iso(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include timezone: {value}")
    return parsed


def validate_date(value: str) -> str:
    date.fromisoformat(value)
    return value


class PrivateStorageError(ValueError):
    """Private storage could not be secured; do not open it anyway."""


def _secure_file(path: Path, *, create: bool = False) -> None:
    """Validate without following links, then enforce mode on the opened inode."""
    flags = os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK
    try:
        if create:
            try:
                fd = os.open(path, flags | os.O_CREAT | os.O_EXCL, 0o600)
            except FileExistsError:
                fd = os.open(path, flags)
        else:
            fd = os.open(path, flags)
    except FileNotFoundError:
        if not create:
            return
        raise
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise PrivateStorageError(f"private database file must be regular: {path}")
        if info.st_uid != os.getuid() or info.st_nlink != 1:
            raise PrivateStorageError(f"private database file must be owned by you with no hard links: {path}")
        os.fchmod(fd, 0o600)
        checked = os.fstat(fd)
        current = path.lstat()
        if stat.S_IMODE(checked.st_mode) != 0o600:
            raise PrivateStorageError(f"cannot enforce private file mode 0600: {path}")
        if (current.st_dev, current.st_ino) != (info.st_dev, info.st_ino):
            raise PrivateStorageError(f"private database path changed during validation: {path}")
    finally:
        os.close(fd)


def _private_path(path: Path, *, create_parent: bool) -> Path:
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        raise PrivateStorageError("private storage requires POSIX ownership and no-follow permission checks")
    path = Path(os.path.abspath(Path(path).expanduser()))
    if create_parent:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    info = path.parent.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
        raise PrivateStorageError(f"database directory must be a real directory owned by you: {path.parent}")
    if stat.S_IMODE(info.st_mode) != 0o700:
        raise PrivateStorageError(
            f"database directory must have mode 0700; use a dedicated private directory: {path.parent}"
        )
    # Resolve ancestor aliases (e.g. macOS /var) only after rejecting a linked leaf directory.
    return path.parent.resolve(strict=True) / path.name


def connect(path: Path = DEFAULT_DB, *, create_parent: bool = False) -> sqlite3.Connection:
    conn = None
    try:
        path = _private_path(path, create_parent=create_parent)
        _secure_file(path, create=True)
        for suffix in ("-wal", "-shm", "-journal"):
            _secure_file(Path(str(path) + suffix))
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 5000")
        conn.execute("PRAGMA journal_mode = WAL")
        # SQLite inherits the secured database's permissions for new WAL/SHM files.
        for suffix in ("-wal", "-shm", "-journal"):
            _secure_file(Path(str(path) + suffix))
        return conn
    except (OSError, PrivateStorageError) as exc:
        if conn is not None:
            conn.close()
        raise PrivateStorageError(f"private storage check failed: {exc}") from exc
    except Exception:
        if conn is not None:
            conn.close()
        raise


def storage_notice(path: Path) -> None:
    """Disclose persistence on stderr without mixing notices with JSON results."""
    print(
        f"IBD storage: commands may create or migrate a local SQLite database at {Path(path).expanduser()}. "
        "Confirmed records persist as sensitive health data, protected by permissions, not encryption. "
        "Keep the directory and backups private. No external notifications are sent by these scripts.",
        file=sys.stderr,
    )


SCHEMA = """
CREATE TABLE IF NOT EXISTS symptom_logs (
    id TEXT PRIMARY KEY,
    log_date TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    stool_count INTEGER CHECK (stool_count IS NULL OR stool_count >= 0),
    stool_count_mode TEXT CHECK (stool_count_mode IN ('day_total','increment')),
    stool_state TEXT CHECK (stool_state IN ('formed','loose','watery','mixed')),
    pain_score INTEGER CHECK (pain_score IS NULL OR pain_score BETWEEN 0 AND 10),
    bloating_score INTEGER CHECK (bloating_score IS NULL OR bloating_score BETWEEN 0 AND 10),
    blood TEXT CHECK (blood IN ('yes','no','unknown')),
    urgency TEXT CHECK (urgency IN ('yes','no','unknown')),
    night_stool TEXT CHECK (night_stool IN ('yes','no','unknown')),
    temperature_c REAL,
    overall_vs_usual TEXT CHECK (overall_vs_usual IN ('better','usual','slightly_worse','much_worse')),
    back_to_usual INTEGER CHECK (back_to_usual IN (0,1)),
    raw_text TEXT NOT NULL,
    supersedes_id TEXT REFERENCES symptom_logs(id),
    created_at TEXT NOT NULL,
    CHECK ((stool_count IS NULL AND stool_count_mode IS NULL) OR
           (stool_count IS NOT NULL AND stool_count_mode IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS factor_terms (
    id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL CHECK (category IN ('food','sleep','stress','infection','exercise','medication','other')),
    aliases_json TEXT NOT NULL DEFAULT '[]',
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0,1))
);

CREATE TABLE IF NOT EXISTS factor_logs (
    id TEXT PRIMARY KEY,
    factor_id TEXT NOT NULL REFERENCES factor_terms(id),
    log_date TEXT NOT NULL,
    occurred_at TEXT,
    raw_label TEXT NOT NULL,
    detail TEXT,
    suspected INTEGER CHECK (suspected IN (0,1)),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS injections (
    id TEXT PRIMARY KEY,
    sequence_no INTEGER,
    drug_name TEXT NOT NULL,
    original_scheduled_at TEXT NOT NULL,
    current_scheduled_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('pending','completed','delayed','cancelled')),
    interval_days INTEGER CHECK (interval_days IS NULL OR interval_days > 0),
    dose_note TEXT,
    vial_count INTEGER CHECK (vial_count IS NULL OR vial_count >= 0),
    delay_reason TEXT,
    reaction_note TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (status <> 'completed' OR completed_at IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS checkups (
    id TEXT PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('lab','visit','other')),
    title TEXT NOT NULL,
    original_due_at TEXT NOT NULL,
    current_due_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('pending','completed','delayed','cancelled')),
    related_injection_id TEXT REFERENCES injections(id),
    timing TEXT CHECK (timing IN ('pre_injection','post_injection','routine','unknown')),
    delay_reason TEXT,
    summary_note TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (status <> 'completed' OR completed_at IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS metric_definitions (
    code TEXT PRIMARY KEY,
    display_name TEXT NOT NULL UNIQUE,
    value_type TEXT NOT NULL CHECK (value_type IN ('numeric','qualitative')),
    default_unit TEXT,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0,1))
);

CREATE TABLE IF NOT EXISTS checkup_results (
    id TEXT PRIMARY KEY,
    checkup_id TEXT NOT NULL REFERENCES checkups(id),
    metric_code TEXT NOT NULL REFERENCES metric_definitions(code),
    numeric_value REAL,
    text_value TEXT,
    unit TEXT,
    reference_low REAL,
    reference_high REAL,
    abnormal_flag TEXT CHECK (abnormal_flag IN ('low','high','normal','abnormal')),
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (checkup_id, metric_code),
    CHECK ((numeric_value IS NOT NULL AND text_value IS NULL) OR
           (numeric_value IS NULL AND text_value IS NOT NULL)),
    CHECK (reference_low IS NULL OR reference_high IS NULL OR reference_low <= reference_high)
);

CREATE TABLE IF NOT EXISTS reminders (
    id TEXT PRIMARY KEY,
    injection_id TEXT REFERENCES injections(id),
    checkup_id TEXT REFERENCES checkups(id),
    reminder_kind TEXT NOT NULL CHECK (reminder_kind IN ('primary','advance','due_day')),
    remind_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('pending','sent','completed','cancelled')),
    external_system TEXT,
    external_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK ((injection_id IS NOT NULL AND checkup_id IS NULL) OR
           (injection_id IS NULL AND checkup_id IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_symptom_date_time ON symptom_logs(log_date, observed_at, recorded_at);
CREATE INDEX IF NOT EXISTS idx_factor_date ON factor_logs(log_date, occurred_at);
CREATE INDEX IF NOT EXISTS idx_injection_current ON injections(status, current_scheduled_at);
CREATE INDEX IF NOT EXISTS idx_checkup_current ON checkups(status, current_due_at);
CREATE INDEX IF NOT EXISTS idx_result_metric ON checkup_results(metric_code, checkup_id);
CREATE INDEX IF NOT EXISTS idx_reminder_time ON reminders(status, remind_at);
"""


METRICS = (
    ("crp", "C反应蛋白", "numeric", "mg/L"),
    ("esr", "血沉", "numeric", "mm/h"),
    ("hgb", "血红蛋白", "numeric", "g/L"),
    ("wbc", "白细胞计数", "numeric", "10^9/L"),
    ("plt", "血小板计数", "numeric", "10^9/L"),
    ("alb", "白蛋白", "numeric", "g/L"),
)

FACTOR_TERMS = (
    ("spicy_food", "辣食", "food", ["辣的", "微辣", "辣椒", "吃辣"]),
    ("milk", "牛奶", "food", ["纯牛奶", "鲜奶"]),
    ("yogurt", "酸奶", "food", []),
    ("coffee", "咖啡", "food", ["手冲咖啡"]),
    ("late_sleep", "熬夜", "sleep", ["睡得晚", "晚睡"]),
    ("stress", "压力", "stress", ["精神压力", "压力大"]),
)


def init_db(path: Path = DEFAULT_DB) -> sqlite3.Connection:
    conn = connect(path, create_parent=True)
    current_version = conn.execute("PRAGMA user_version").fetchone()[0]
    with conn:
        conn.executescript(SCHEMA)
        conn.executemany(
            "INSERT OR IGNORE INTO metric_definitions(code,display_name,value_type,default_unit) VALUES (?,?,?,?)",
            METRICS,
        )
        conn.executemany(
            "INSERT OR IGNORE INTO factor_terms(id,canonical_name,category,aliases_json) VALUES (?,?,?,?)",
            [(i, n, c, json.dumps(a, ensure_ascii=False)) for i, n, c, a in FACTOR_TERMS],
        )
        stamp = now_iso()
        conn.executemany(
            "INSERT INTO settings(key,value,updated_at) VALUES (?,?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value,updated_at=excluded.updated_at",
            (("timezone", "Asia/Shanghai", stamp), ("summary_interval_days", "7", stamp)),
        )
        # The base schema is V1. Never lower a care database's newer version:
        # doing so would make the care layer replay historical migrations.
        if current_version < 1:
            conn.execute("PRAGMA user_version = 1")
    return conn


def open_or_init_db(path: Path = DEFAULT_DB) -> sqlite3.Connection:
    resolved = Path(path).expanduser()
    if resolved.exists():
        return connect(resolved)
    return init_db(resolved)


def normalize_label(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def resolve_factor(conn: sqlite3.Connection, label: str) -> sqlite3.Row | None:
    target = normalize_label(label)
    for row in conn.execute("SELECT * FROM factor_terms WHERE active=1"):
        names = [row["canonical_name"], *json.loads(row["aliases_json"])]
        if any(normalize_label(name) == target for name in names):
            return row
    return None


def add_factor_term(conn: sqlite3.Connection, canonical_name: str, category: str, aliases: list[str]) -> str:
    identifier = new_id()
    with conn:
        conn.execute(
            "INSERT INTO factor_terms(id,canonical_name,category,aliases_json) VALUES (?,?,?,?)",
            (identifier, canonical_name, category, json.dumps(aliases, ensure_ascii=False)),
        )
    return identifier


def add_metric_definition(
    conn: sqlite3.Connection, *, code: str, display_name: str,
    value_type: str, default_unit: str | None = None,
) -> dict[str, Any]:
    """Register one explicitly adopted metric without changing existing facts."""
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", code):
        raise ValueError("metric code must use lowercase snake_case and start with a letter")
    display_name = display_name.strip()
    if not display_name:
        raise ValueError("metric display_name is required")
    if value_type not in ("numeric", "qualitative"):
        raise ValueError("metric value_type must be numeric or qualitative")
    default_unit = default_unit.strip() if default_unit else None
    if conn.execute("SELECT 1 FROM metric_definitions WHERE code=?", (code,)).fetchone():
        raise ValueError("metric code already exists and is immutable")
    if conn.execute(
        "SELECT 1 FROM metric_definitions WHERE display_name=?", (display_name,)
    ).fetchone():
        raise ValueError("metric display_name already exists")
    with conn:
        conn.execute(
            "INSERT INTO metric_definitions(code,display_name,value_type,default_unit,active) VALUES (?,?,?,?,1)",
            (code, display_name, value_type, default_unit),
        )
    return dict(conn.execute("SELECT * FROM metric_definitions WHERE code=?", (code,)).fetchone())


def deactivate_metric_definition(conn: sqlite3.Connection, *, code: str) -> dict[str, Any]:
    """Stop new entries for a metric while preserving all historical results."""
    with conn:
        cursor = conn.execute("UPDATE metric_definitions SET active=0 WHERE code=?", (code,))
        if cursor.rowcount == 0:
            raise ValueError("metric not found")
    return dict(conn.execute("SELECT * FROM metric_definitions WHERE code=?", (code,)).fetchone())


def classify_back_to_usual(text: str) -> int | None:
    compact = re.sub(r"\s+", "", text)
    if re.search(r"(还没|还没有|尚未|仍未|没有).*恢复|还不.*平时", compact):
        return 0
    if re.search(r"(好一点|好多了|缓解|没那么|快恢复|基本没事|差不多)", compact):
        return None
    positive = (
        r"(已经|现已|现在)?(完全)?恢复(到)?(平时|正常|往常|原来)(状态)?",
        r"(现在|已经)?.{0,4}(和|跟)(平时|往常).{0,3}一样",
        r"完全恢复了?",
    )
    if any(re.search(pattern, compact) for pattern in positive):
        return 1
    return None


def active_symptoms(conn: sqlite3.Connection, log_date: str) -> list[sqlite3.Row]:
    return list(
        conn.execute(
            """
            SELECT * FROM symptom_logs s
            WHERE s.log_date=?
              AND NOT EXISTS (
                  SELECT 1 FROM symptom_logs newer WHERE newer.supersedes_id=s.id
              )
            ORDER BY observed_at, recorded_at, id
            """,
            (log_date,),
        )
    )


def aggregate_day(conn: sqlite3.Connection, log_date: str) -> dict[str, Any]:
    rows = active_symptoms(conn, validate_date(log_date))
    last_total_index = None
    for index, row in enumerate(rows):
        if row["stool_count_mode"] == "day_total":
            last_total_index = index
    if last_total_index is None:
        stool_total = sum(
            row["stool_count"] or 0 for row in rows if row["stool_count_mode"] == "increment"
        )
        has_stool_data = any(row["stool_count_mode"] == "increment" for row in rows)
    else:
        stool_total = rows[last_total_index]["stool_count"]
        stool_total += sum(
            row["stool_count"] or 0
            for row in rows[last_total_index + 1 :]
            if row["stool_count_mode"] == "increment"
        )
        has_stool_data = True

    def latest(field: str) -> Any:
        values = [row[field] for row in rows if row[field] is not None]
        return values[-1] if values else None

    def any_state(field: str) -> str | None:
        values = [row[field] for row in rows if row[field] is not None and row[field] != "unknown"]
        if "yes" in values:
            return "yes"
        if "no" in values:
            return "no"
        return None

    pains = [row["pain_score"] for row in rows if row["pain_score"] is not None]
    bloating_scores = [row["bloating_score"] for row in rows if row["bloating_score"] is not None]
    temperatures = [row["temperature_c"] for row in rows if row["temperature_c"] is not None]
    return {
        "log_date": log_date,
        "active_entries": len(rows),
        "stool_total": stool_total if has_stool_data else None,
        "stool_state_latest": latest("stool_state"),
        "pain_max": max(pains) if pains else None,
        "pain_latest": latest("pain_score"),
        "bloating_max": max(bloating_scores) if bloating_scores else None,
        "bloating_latest": latest("bloating_score"),
        "blood_any": any_state("blood"),
        "urgency_any": any_state("urgency"),
        "night_stool_any": any_state("night_stool"),
        "temperature_max_c": max(temperatures) if temperatures else None,
        "temperature_latest_c": latest("temperature_c"),
        "overall_vs_usual": latest("overall_vs_usual"),
        "back_to_usual": latest("back_to_usual"),
    }


def record_symptom(
    conn: sqlite3.Connection,
    *,
    raw_text: str,
    observed_at: str,
    recorded_at: str | None = None,
    log_date: str | None = None,
    stool_count: int | None = None,
    stool_count_mode: str | None = None,
    stool_state: str | None = None,
    pain_score: int | None = None,
    bloating_score: int | None = None,
    blood: str | None = None,
    urgency: str | None = None,
    night_stool: str | None = None,
    temperature_c: float | None = None,
    overall_vs_usual: str | None = None,
    back_to_usual: int | None = None,
    supersedes_id: str | None = None,
) -> str:
    observed = parse_iso(observed_at)
    recorded_at = recorded_at or now_iso()
    parse_iso(recorded_at)
    log_date = log_date or observed.date().isoformat()
    validate_date(log_date)
    if (stool_count is None) != (stool_count_mode is None):
        raise ValueError("stool_count and stool_count_mode must be provided together")
    if stool_count_mode not in (None, "day_total", "increment"):
        raise ValueError("invalid stool_count_mode")
    identifier = new_id()
    with conn:
        conn.execute(
            """
            INSERT INTO symptom_logs(
                id,log_date,observed_at,recorded_at,stool_count,stool_count_mode,
                stool_state,pain_score,bloating_score,blood,urgency,night_stool,
                temperature_c,overall_vs_usual,back_to_usual,raw_text,supersedes_id,created_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                identifier, log_date, observed_at, recorded_at, stool_count, stool_count_mode,
                stool_state, pain_score, bloating_score, blood, urgency, night_stool,
                temperature_c, overall_vs_usual, back_to_usual, raw_text, supersedes_id, now_iso(),
            ),
        )
    return identifier


def record_factor(
    conn: sqlite3.Connection,
    *,
    label: str,
    log_date: str,
    occurred_at: str | None = None,
    detail: str | None = None,
    suspected: int | None = None,
) -> str:
    validate_date(log_date)
    if occurred_at:
        parse_iso(occurred_at)
    term = resolve_factor(conn, label)
    if term is None:
        raise ValueError(f"unknown factor label: {label}; add or confirm a canonical term first")
    identifier = new_id()
    with conn:
        conn.execute(
            "INSERT INTO factor_logs(id,factor_id,log_date,occurred_at,raw_label,detail,suspected,created_at) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (identifier, term["id"], log_date, occurred_at, label, detail, suspected, now_iso()),
        )
    return identifier


def add_reminder(
    conn: sqlite3.Connection,
    *,
    remind_at: str,
    reminder_kind: str = "primary",
    injection_id: str | None = None,
    checkup_id: str | None = None,
) -> str:
    parse_iso(remind_at)
    if (injection_id is None) == (checkup_id is None):
        raise ValueError("exactly one reminder target is required")
    identifier = new_id()
    stamp = now_iso()
    with conn:
        conn.execute(
            "INSERT INTO reminders(id,injection_id,checkup_id,reminder_kind,remind_at,status,created_at,updated_at) "
            "VALUES (?,?,?,?,?,'pending',?,?)",
            (identifier, injection_id, checkup_id, reminder_kind, remind_at, stamp, stamp),
        )
    return identifier


def schedule_injection(
    conn: sqlite3.Connection,
    *,
    drug_name: str,
    scheduled_at: str,
    sequence_no: int | None = None,
    interval_days: int | None = None,
    dose_note: str | None = None,
    vial_count: int | None = None,
    reminder_at: str | None = None,
) -> str:
    parse_iso(scheduled_at)
    identifier = new_id()
    stamp = now_iso()
    with conn:
        conn.execute(
            """
            INSERT INTO injections(
              id,sequence_no,drug_name,original_scheduled_at,current_scheduled_at,status,
              interval_days,dose_note,vial_count,created_at,updated_at
            ) VALUES (?,?,?,?,?,'pending',?,?,?,?,?)
            """,
            (identifier, sequence_no, drug_name, scheduled_at, scheduled_at,
             interval_days, dose_note, vial_count, stamp, stamp),
        )
    if reminder_at:
        add_reminder(conn, injection_id=identifier, remind_at=reminder_at)
    return identifier


def _cancel_pending_reminders(conn: sqlite3.Connection, column: str, target_id: str) -> None:
    if column not in ("injection_id", "checkup_id"):
        raise ValueError("invalid reminder target")
    stamp = now_iso()
    conn.execute(
        f"UPDATE reminders SET status='cancelled',updated_at=? "
        f"WHERE {column}=? AND status='pending'",
        (stamp, target_id),
    )


def reschedule_injection(
    conn: sqlite3.Connection, identifier: str, new_at: str, reason: str | None,
    reminder_at: str | None = None,
) -> None:
    parse_iso(new_at)
    with conn:
        row = conn.execute("SELECT * FROM injections WHERE id=?", (identifier,)).fetchone()
        if row is None:
            raise ValueError("injection not found")
        conn.execute(
            "UPDATE injections SET current_scheduled_at=?,status='delayed',delay_reason=?,updated_at=? WHERE id=?",
            (new_at, reason, now_iso(), identifier),
        )
        _cancel_pending_reminders(conn, "injection_id", identifier)
    if reminder_at:
        add_reminder(conn, injection_id=identifier, remind_at=reminder_at)


def complete_injection(
    conn: sqlite3.Connection, identifier: str, completed_at: str, reaction_note: str | None = None,
) -> None:
    parse_iso(completed_at)
    with conn:
        cursor = conn.execute(
            "UPDATE injections SET completed_at=?,status='completed',reaction_note=?,updated_at=? WHERE id=?",
            (completed_at, reaction_note, now_iso(), identifier),
        )
        if cursor.rowcount == 0:
            raise ValueError("injection not found")
        _cancel_pending_reminders(conn, "injection_id", identifier)


def schedule_checkup(
    conn: sqlite3.Connection,
    *,
    kind: str,
    title: str,
    due_at: str,
    related_injection_id: str | None = None,
    timing: str = "unknown",
    reminder_at: str | None = None,
) -> str:
    parse_iso(due_at)
    identifier = new_id()
    stamp = now_iso()
    with conn:
        conn.execute(
            """
            INSERT INTO checkups(
              id,kind,title,original_due_at,current_due_at,status,related_injection_id,
              timing,created_at,updated_at
            ) VALUES (?,?,?,?,?,'pending',?,?,?,?)
            """,
            (identifier, kind, title, due_at, due_at, related_injection_id, timing, stamp, stamp),
        )
    if reminder_at:
        add_reminder(conn, checkup_id=identifier, remind_at=reminder_at)
    return identifier


def reschedule_checkup(
    conn: sqlite3.Connection, identifier: str, new_at: str, reason: str | None,
    reminder_at: str | None = None,
) -> None:
    parse_iso(new_at)
    with conn:
        row = conn.execute("SELECT * FROM checkups WHERE id=?", (identifier,)).fetchone()
        if row is None:
            raise ValueError("checkup not found")
        conn.execute(
            "UPDATE checkups SET current_due_at=?,status='delayed',delay_reason=?,updated_at=? WHERE id=?",
            (new_at, reason, now_iso(), identifier),
        )
        _cancel_pending_reminders(conn, "checkup_id", identifier)
    if reminder_at:
        add_reminder(conn, checkup_id=identifier, remind_at=reminder_at)


def complete_checkup(
    conn: sqlite3.Connection, identifier: str, completed_at: str, summary_note: str | None = None,
) -> None:
    parse_iso(completed_at)
    with conn:
        cursor = conn.execute(
            "UPDATE checkups SET completed_at=?,status='completed',summary_note=?,updated_at=? WHERE id=?",
            (completed_at, summary_note, now_iso(), identifier),
        )
        if cursor.rowcount == 0:
            raise ValueError("checkup not found")
        _cancel_pending_reminders(conn, "checkup_id", identifier)


def add_result(
    conn: sqlite3.Connection,
    *,
    checkup_id: str,
    metric_code: str,
    numeric_value: float | None = None,
    text_value: str | None = None,
    unit: str | None = None,
    reference_low: float | None = None,
    reference_high: float | None = None,
    abnormal_flag: str | None = None,
    notes: str | None = None,
) -> str:
    metric = conn.execute("SELECT * FROM metric_definitions WHERE code=? AND active=1", (metric_code,)).fetchone()
    if metric is None:
        raise ValueError("unknown metric")
    if (numeric_value is None) == (text_value is None):
        raise ValueError("provide exactly one of numeric_value or text_value")
    if metric["value_type"] == "numeric" and numeric_value is None:
        raise ValueError("numeric metric requires numeric_value")
    if metric["value_type"] == "qualitative" and text_value is None:
        raise ValueError("qualitative metric requires text_value")
    if abnormal_flag not in (None, *ABNORMAL_FLAGS):
        raise ValueError("invalid abnormal_flag")
    if reference_low is not None and reference_high is not None and reference_low > reference_high:
        raise ValueError("reference_low cannot exceed reference_high")
    identifier = new_id()
    stamp = now_iso()
    with conn:
        conn.execute(
            """
            INSERT INTO checkup_results(
              id,checkup_id,metric_code,numeric_value,text_value,unit,
              reference_low,reference_high,abnormal_flag,notes,created_at,updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(checkup_id,metric_code) DO UPDATE SET
              numeric_value=excluded.numeric_value,
              text_value=excluded.text_value,
              unit=excluded.unit,
              reference_low=excluded.reference_low,
              reference_high=excluded.reference_high,
              abnormal_flag=excluded.abnormal_flag,
              notes=excluded.notes,
              updated_at=excluded.updated_at
            """,
            (identifier, checkup_id, metric_code, numeric_value, text_value, unit,
             reference_low, reference_high, abnormal_flag, notes, stamp, stamp),
        )
    row = conn.execute(
        "SELECT id FROM checkup_results WHERE checkup_id=? AND metric_code=?",
        (checkup_id, metric_code),
    ).fetchone()
    return row["id"]


def _rounded(value: float | int | None) -> float | None:
    return None if value is None else round(float(value), 3)


def _median(values: list[float | int]) -> float | None:
    return _rounded(median(values)) if values else None


def _comparison(
    daily_by_date: dict[str, dict[str, Any]],
    exposed_dates: set[str],
    comparison_dates: set[str],
    field: str,
) -> dict[str, Any]:
    exposed = [
        daily_by_date[day][field]
        for day in sorted(exposed_dates)
        if day in daily_by_date and daily_by_date[day][field] is not None
    ]
    comparison = [
        daily_by_date[day][field]
        for day in sorted(comparison_dates)
        if day in daily_by_date and daily_by_date[day][field] is not None
    ]
    exposed_median = _median(exposed)
    comparison_median = _median(comparison)
    difference = (
        _rounded(exposed_median - comparison_median)
        if exposed_median is not None and comparison_median is not None
        else None
    )
    return {
        "exposed_days_with_data": len(exposed),
        "comparison_days_with_data": len(comparison),
        "exposed_median": exposed_median,
        "comparison_median": comparison_median,
        "median_difference": difference,
        "evidence": (
            "exploratory"
            if len(exposed) >= 3 and len(comparison) >= 3
            else "insufficient_data"
        ),
    }


def _worsening_pattern(daily: list[dict[str, Any]]) -> dict[str, Any]:
    worse_values = {"slightly_worse", "much_worse"}
    explicit_worse_days = 0
    current_streak = 0
    max_streak = 0
    previous_date: date | None = None
    for item in daily:
        current_date = date.fromisoformat(item["log_date"])
        is_consecutive = previous_date is not None and current_date == previous_date + timedelta(days=1)
        if item["overall_vs_usual"] in worse_values:
            explicit_worse_days += 1
            current_streak = current_streak + 1 if is_consecutive else 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
        previous_date = current_date
    if not daily:
        classification = "insufficient_data"
    elif max_streak >= 2:
        classification = "multi_day_recorded_worsening"
    elif max_streak == 1:
        classification = "isolated_recorded_worsening"
    else:
        classification = "no_explicit_worsening"
    return {
        "explicit_worse_days": explicit_worse_days,
        "max_consecutive_worse_days": max_streak,
        "classification": classification,
        "clinical_activity_inference": False,
    }


def _recorded_usual_day_evidence(daily: list[dict[str, Any]]) -> dict[str, Any]:
    """Describe explicitly marked usual days without promoting them to a baseline.

    A confirmed symptom baseline is managed by ibd_care.py.  This helper is
    deliberately descriptive so a recent run of logs cannot silently redefine
    what counts as normal for comparisons.
    """
    usual_days = [
        item
        for item in daily
        if item["overall_vs_usual"] == "usual" or item["back_to_usual"] == 1
    ]
    stool_values = [item["stool_total"] for item in usual_days if item["stool_total"] is not None]
    pain_values = [item["pain_max"] for item in usual_days if item["pain_max"] is not None]
    if len(usual_days) >= 3:
        status = "available"
    elif usual_days:
        status = "limited"
    else:
        status = "unavailable"
    return {
        "status": status,
        "explicitly_recorded_usual_days": len(usual_days),
        "stool_total_median_descriptive": _median(stool_values),
        "pain_max_median_descriptive": _median(pain_values),
        "is_confirmed_baseline": False,
    }


def _factor_associations(
    conn: sqlite3.Connection,
    *,
    start: date,
    end: date,
    daily: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = list(
        conn.execute(
            """
            SELECT t.canonical_name, f.log_date
            FROM factor_logs f JOIN factor_terms t ON t.id=f.factor_id
            WHERE f.log_date BETWEEN ? AND ?
            ORDER BY t.canonical_name, f.log_date
            """,
            (start.isoformat(), end.isoformat()),
        )
    )
    grouped: dict[str, list[str]] = {}
    for row in rows:
        grouped.setdefault(row["canonical_name"], []).append(row["log_date"])
    daily_by_date = {item["log_date"]: item for item in daily}
    recorded_dates = set(daily_by_date)
    output: list[dict[str, Any]] = []
    for name, event_dates in sorted(grouped.items()):
        exposure_dates = {date.fromisoformat(value) for value in event_dates}
        all_impacted = {
            (exposure + timedelta(days=lag)).isoformat()
            for exposure in exposure_dates
            for lag in (0, 1, 2)
            if start <= exposure + timedelta(days=lag) <= end
        }
        comparison_dates = recorded_dates - all_impacted
        lags = []
        for lag in (0, 1, 2):
            target_dates = {
                (exposure + timedelta(days=lag)).isoformat()
                for exposure in exposure_dates
                if start <= exposure + timedelta(days=lag) <= end
            }
            lags.append(
                {
                    "lag_days": lag,
                    "stool_total": _comparison(
                        daily_by_date, target_dates, comparison_dates, "stool_total"
                    ),
                    "pain_max": _comparison(
                        daily_by_date, target_dates, comparison_dates, "pain_max"
                    ),
                }
            )
        output.append(
            {
                "canonical_name": name,
                "exposure_events": len(event_dates),
                "exposure_days": len(exposure_dates),
                "lag_basis": "calendar_day",
                "lags": lags,
            }
        )
    return output


def _metric_trends(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str | None, str], list[dict[str, Any]]] = {}
    for item in results:
        value_type = "numeric" if item["numeric_value"] is not None else "qualitative"
        key = (item["code"], item["display_name"], item["unit"], value_type)
        grouped.setdefault(key, []).append(item)
    output: list[dict[str, Any]] = []
    for (code, display_name, unit, value_type), items in sorted(grouped.items()):
        items.sort(key=lambda item: item["completed_at"])
        first = items[0]
        latest = items[-1]
        entry: dict[str, Any] = {
            "code": code,
            "display_name": display_name,
            "value_type": value_type,
            "unit": unit,
            "count": len(items),
            "first_at": first["completed_at"],
            "latest_at": latest["completed_at"],
            "latest_abnormal_flag": latest["abnormal_flag"],
        }
        if value_type == "numeric":
            first_value = float(first["numeric_value"])
            latest_value = float(latest["numeric_value"])
            change = latest_value - first_value if len(items) >= 2 else None
            entry.update(
                {
                    "first_value": _rounded(first_value),
                    "latest_value": _rounded(latest_value),
                    "absolute_change": _rounded(change),
                    "percent_change": (
                        _rounded(change / first_value * 100)
                        if change is not None and first_value != 0
                        else None
                    ),
                    "direction": (
                        None
                        if change is None
                        else "up" if change > 0 else "down" if change < 0 else "unchanged"
                    ),
                }
            )
        else:
            entry.update(
                {
                    "first_value": first["text_value"],
                    "latest_value": latest["text_value"],
                    "changed": (
                        first["text_value"] != latest["text_value"]
                        if len(items) >= 2
                        else None
                    ),
                }
            )
        output.append(entry)
    return output


def _injection_analysis(
    conn: sqlite3.Connection, *, start: date, end: date
) -> dict[str, Any]:
    rows = list(
        conn.execute(
            """
            SELECT drug_name,original_scheduled_at,current_scheduled_at,completed_at,status
            FROM injections
            WHERE substr(original_scheduled_at,1,10) BETWEEN ? AND ?
               OR substr(current_scheduled_at,1,10) BETWEEN ? AND ?
               OR (completed_at IS NOT NULL AND substr(completed_at,1,10) BETWEEN ? AND ?)
            ORDER BY current_scheduled_at
            """,
            (
                start.isoformat(), end.isoformat(),
                start.isoformat(), end.isoformat(),
                start.isoformat(), end.isoformat(),
            ),
        )
    )
    status_counts = {status: 0 for status in STATUSES}
    timing = []
    rescheduled = 0
    for row in rows:
        status_counts[row["status"]] += 1
        if row["original_scheduled_at"] != row["current_scheduled_at"]:
            rescheduled += 1
        if row["completed_at"]:
            completed = parse_iso(row["completed_at"])
            original = parse_iso(row["original_scheduled_at"])
            current = parse_iso(row["current_scheduled_at"])
            timing.append(
                {
                    "drug_name": row["drug_name"],
                    "completed_at": row["completed_at"],
                    "days_from_original_schedule": _rounded(
                        (completed - original).total_seconds() / 86400
                    ),
                    "days_from_current_schedule": _rounded(
                        (completed - current).total_seconds() / 86400
                    ),
                }
            )
    return {
        "events_in_window": len(rows),
        "status_counts": status_counts,
        "rescheduled_count": rescheduled,
        "completed_timing": timing,
    }


def _period_analysis(
    conn: sqlite3.Connection,
    *,
    start: date,
    end: date,
    days: int,
    daily: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "method": {
            "type": "descriptive_personal",
            "causality_established": False,
            "disease_activity_inference": False,
            "factor_lag_basis": "calendar_day",
        },
        "coverage": {
            "calendar_days": days,
            "recorded_days": len(daily),
            "recorded_day_ratio": _rounded(len(daily) / days),
            "stool_days": sum(item["stool_total"] is not None for item in daily),
            "pain_days": sum(item["pain_max"] is not None for item in daily),
            "bloating_days": sum(item["bloating_max"] is not None for item in daily),
            "temperature_days": sum(item["temperature_max_c"] is not None for item in daily),
        },
        "recorded_usual_day_evidence": _recorded_usual_day_evidence(daily),
        "worsening_pattern": _worsening_pattern(daily),
        "factor_associations": _factor_associations(
            conn, start=start, end=end, daily=daily
        ),
        "metric_trends": _metric_trends(results),
        "injection_summary": _injection_analysis(conn, start=start, end=end),
    }


def period_summary(
    conn: sqlite3.Connection, *, end_date: str, days: int, analysis: bool = False
) -> dict[str, Any]:
    end = date.fromisoformat(end_date)
    start = end - timedelta(days=days - 1)
    dates = [
        row["log_date"]
        for row in conn.execute(
            "SELECT DISTINCT log_date FROM symptom_logs WHERE log_date BETWEEN ? AND ? ORDER BY log_date",
            (start.isoformat(), end.isoformat()),
        )
    ]
    daily = [aggregate_day(conn, day) for day in dates]
    factors = [
        dict(row)
        for row in conn.execute(
            """
            SELECT t.canonical_name, COUNT(*) AS count
            FROM factor_logs f JOIN factor_terms t ON t.id=f.factor_id
            WHERE f.log_date BETWEEN ? AND ?
            GROUP BY t.id ORDER BY count DESC, t.canonical_name
            """,
            (start.isoformat(), end.isoformat()),
        )
    ]
    results = [
        dict(row)
        for row in conn.execute(
            """
            SELECT c.completed_at, d.code, d.display_name, r.numeric_value, r.text_value,
                   r.unit, r.reference_low, r.reference_high, r.abnormal_flag
            FROM checkup_results r
            JOIN checkups c ON c.id=r.checkup_id
            JOIN metric_definitions d ON d.code=r.metric_code
            WHERE c.completed_at IS NOT NULL
              AND substr(c.completed_at,1,10) BETWEEN ? AND ?
            ORDER BY c.completed_at, d.code
            """,
            (start.isoformat(), end.isoformat()),
        )
    ]
    summary = {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "recorded_days": len(daily),
        "daily": daily,
        "factors": factors,
        "checkup_results": results,
    }
    if analysis:
        summary["analysis"] = _period_analysis(
            conn, start=start, end=end, days=days, daily=daily, results=results
        )
    return summary


def row_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def tri(value: str | None) -> int | None:
    if value in (None, "unknown"):
        return None
    return 1 if value == "yes" else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Private IBD MVP SQLite CLI")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init")
    sub.add_parser("schema")
    sub.add_parser("list-metrics", aliases=["metric-list"])

    p = sub.add_parser("metric-add")
    p.add_argument("--code", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--value-type", required=True, choices=("numeric", "qualitative"))
    p.add_argument("--default-unit")

    p = sub.add_parser("metric-deactivate")
    p.add_argument("--code", required=True)

    p = sub.add_parser("record-symptom")
    p.add_argument("--raw-text", required=True)
    p.add_argument("--observed-at", required=True)
    p.add_argument("--recorded-at")
    p.add_argument("--date")
    p.add_argument("--stool-count", type=int)
    p.add_argument("--count-mode", choices=("day_total", "increment"))
    p.add_argument("--stool-state", choices=("formed", "loose", "watery", "mixed"))
    p.add_argument("--pain-score", type=int)
    p.add_argument("--bloating-score", type=int)
    p.add_argument("--blood", choices=YES_NO_UNKNOWN)
    p.add_argument("--urgency", choices=YES_NO_UNKNOWN)
    p.add_argument("--night-stool", choices=YES_NO_UNKNOWN)
    p.add_argument("--temperature", type=float)
    p.add_argument("--overall", choices=("better", "usual", "slightly_worse", "much_worse"))
    p.add_argument("--back-to-usual", choices=("auto", "yes", "no", "unknown"), default="auto")
    p.add_argument("--supersedes-id")

    p = sub.add_parser("daily-summary")
    p.add_argument("--date", required=True)

    p = sub.add_parser("factor-term-add")
    p.add_argument("--name", required=True)
    p.add_argument("--category", required=True, choices=("food","sleep","stress","infection","exercise","medication","other"))
    p.add_argument("--alias", action="append", default=[])

    p = sub.add_parser("record-factor")
    p.add_argument("--label", required=True)
    p.add_argument("--date", required=True)
    p.add_argument("--occurred-at")
    p.add_argument("--detail")
    p.add_argument("--suspected", choices=YES_NO_UNKNOWN, default="unknown")

    p = sub.add_parser("schedule-injection")
    p.add_argument("--drug", required=True)
    p.add_argument("--scheduled-at", required=True)
    p.add_argument("--sequence", type=int)
    p.add_argument("--interval-days", type=int)
    p.add_argument("--dose-note")
    p.add_argument("--vial-count", type=int)
    p.add_argument("--remind-at")

    p = sub.add_parser("reschedule-injection")
    p.add_argument("--id", required=True)
    p.add_argument("--new-at", required=True)
    p.add_argument("--reason")
    p.add_argument("--remind-at")

    p = sub.add_parser("complete-injection")
    p.add_argument("--id", required=True)
    p.add_argument("--completed-at", required=True)
    p.add_argument("--reaction-note")

    p = sub.add_parser("schedule-checkup")
    p.add_argument("--kind", required=True, choices=("lab","visit","other"))
    p.add_argument("--title", required=True)
    p.add_argument("--due-at", required=True)
    p.add_argument("--related-injection-id")
    p.add_argument("--timing", choices=("pre_injection","post_injection","routine","unknown"), default="unknown")
    p.add_argument("--remind-at")

    p = sub.add_parser("reschedule-checkup")
    p.add_argument("--id", required=True)
    p.add_argument("--new-at", required=True)
    p.add_argument("--reason")
    p.add_argument("--remind-at")

    p = sub.add_parser("complete-checkup")
    p.add_argument("--id", required=True)
    p.add_argument("--completed-at", required=True)
    p.add_argument("--summary-note")

    p = sub.add_parser("add-result")
    p.add_argument("--checkup-id", required=True)
    p.add_argument("--metric", required=True)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--value", type=float)
    group.add_argument("--text-value")
    p.add_argument("--unit")
    p.add_argument("--reference-low", type=float)
    p.add_argument("--reference-high", type=float)
    p.add_argument("--abnormal-flag", choices=ABNORMAL_FLAGS)
    p.add_argument("--notes")

    p = sub.add_parser("reminder-link")
    p.add_argument("--id", required=True)
    p.add_argument("--external-id", required=True)
    p.add_argument("--external-system", default="apple_reminders")

    p = sub.add_parser("reminder-status")
    p.add_argument("--id", required=True)
    p.add_argument("--status", required=True, choices=REMINDER_STATUSES)

    p = sub.add_parser("upcoming")
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("period-summary")
    p.add_argument("--end-date", default=date.today().isoformat())
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--analysis", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    storage_notice(args.db)
    if args.command == "init":
        conn = init_db(args.db)
        print_json({"database": str(Path(args.db).expanduser()), "tables": 9, "user_version": conn.execute("PRAGMA user_version").fetchone()[0]})
        return 0

    conn = open_or_init_db(args.db)

    if args.command == "schema":
        tables = [row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        print_json({"tables": tables, "user_version": conn.execute("PRAGMA user_version").fetchone()[0]})
    elif args.command in ("list-metrics", "metric-list"):
        print_json([dict(row) for row in conn.execute("SELECT * FROM metric_definitions WHERE active=1 ORDER BY code")])
    elif args.command == "metric-add":
        print_json(add_metric_definition(
            conn, code=args.code, display_name=args.name,
            value_type=args.value_type, default_unit=args.default_unit,
        ))
    elif args.command == "metric-deactivate":
        print_json(deactivate_metric_definition(conn, code=args.code))
    elif args.command == "record-symptom":
        back = classify_back_to_usual(args.raw_text) if args.back_to_usual == "auto" else tri(args.back_to_usual)
        identifier = record_symptom(
            conn, raw_text=args.raw_text, observed_at=args.observed_at, recorded_at=args.recorded_at,
            log_date=args.date, stool_count=args.stool_count, stool_count_mode=args.count_mode,
            stool_state=args.stool_state, pain_score=args.pain_score, bloating_score=args.bloating_score,
            blood=args.blood, urgency=args.urgency, night_stool=args.night_stool,
            temperature_c=args.temperature, overall_vs_usual=args.overall,
            back_to_usual=back, supersedes_id=args.supersedes_id,
        )
        print_json({"id": identifier, "daily": aggregate_day(conn, args.date or parse_iso(args.observed_at).date().isoformat())})
    elif args.command == "daily-summary":
        print_json(aggregate_day(conn, args.date))
    elif args.command == "factor-term-add":
        print_json({"id": add_factor_term(conn, args.name, args.category, args.alias)})
    elif args.command == "record-factor":
        print_json({"id": record_factor(conn, label=args.label, log_date=args.date, occurred_at=args.occurred_at, detail=args.detail, suspected=tri(args.suspected))})
    elif args.command == "schedule-injection":
        print_json({"id": schedule_injection(conn, drug_name=args.drug, scheduled_at=args.scheduled_at, sequence_no=args.sequence, interval_days=args.interval_days, dose_note=args.dose_note, vial_count=args.vial_count, reminder_at=args.remind_at)})
    elif args.command == "reschedule-injection":
        reschedule_injection(conn, args.id, args.new_at, args.reason, args.remind_at)
        print_json(row_dict(conn.execute("SELECT * FROM injections WHERE id=?", (args.id,)).fetchone()))
    elif args.command == "complete-injection":
        complete_injection(conn, args.id, args.completed_at, args.reaction_note)
        print_json(row_dict(conn.execute("SELECT * FROM injections WHERE id=?", (args.id,)).fetchone()))
    elif args.command == "schedule-checkup":
        print_json({"id": schedule_checkup(conn, kind=args.kind, title=args.title, due_at=args.due_at, related_injection_id=args.related_injection_id, timing=args.timing, reminder_at=args.remind_at)})
    elif args.command == "reschedule-checkup":
        reschedule_checkup(conn, args.id, args.new_at, args.reason, args.remind_at)
        print_json(row_dict(conn.execute("SELECT * FROM checkups WHERE id=?", (args.id,)).fetchone()))
    elif args.command == "complete-checkup":
        complete_checkup(conn, args.id, args.completed_at, args.summary_note)
        print_json(row_dict(conn.execute("SELECT * FROM checkups WHERE id=?", (args.id,)).fetchone()))
    elif args.command == "add-result":
        print_json({"id": add_result(conn, checkup_id=args.checkup_id, metric_code=args.metric, numeric_value=args.value, text_value=args.text_value, unit=args.unit, reference_low=args.reference_low, reference_high=args.reference_high, abnormal_flag=args.abnormal_flag, notes=args.notes)})
    elif args.command == "reminder-link":
        with conn:
            cursor = conn.execute("UPDATE reminders SET external_system=?,external_id=?,updated_at=? WHERE id=?", (args.external_system, args.external_id, now_iso(), args.id))
            if cursor.rowcount == 0:
                raise ValueError("reminder not found")
        print_json({"id": args.id, "linked": True})
    elif args.command == "reminder-status":
        with conn:
            cursor = conn.execute("UPDATE reminders SET status=?,updated_at=? WHERE id=?", (args.status, now_iso(), args.id))
            if cursor.rowcount == 0:
                raise ValueError("reminder not found")
        print_json({"id": args.id, "status": args.status})
    elif args.command == "upcoming":
        print_json({
            "injections": [dict(row) for row in conn.execute("SELECT * FROM injections WHERE status IN ('pending','delayed') ORDER BY current_scheduled_at LIMIT ?", (args.limit,))],
            "checkups": [dict(row) for row in conn.execute("SELECT * FROM checkups WHERE status IN ('pending','delayed') ORDER BY current_due_at LIMIT ?", (args.limit,))],
            "reminders": [dict(row) for row in conn.execute("SELECT * FROM reminders WHERE status='pending' ORDER BY remind_at LIMIT ?", (args.limit,))],
        })
    elif args.command == "period-summary":
        if args.days <= 0:
            raise ValueError("days must be positive")
        print_json(period_summary(conn, end_date=args.end_date, days=args.days, analysis=args.analysis))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, sqlite3.IntegrityError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
