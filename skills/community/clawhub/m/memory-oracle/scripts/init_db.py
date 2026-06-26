#!/usr/bin/env python3
"""
memory-oracle: init_db.py
Initialize SQLite database with FTS5 index.
Optionally import existing MEMORY.md and daily logs.
"""

import sqlite3
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = SCRIPT_DIR / "config" / "settings.json"

SCHEMA_VERSION = 1


def utcnow() -> datetime:
    """UTC now, compatible with Python 3.8-3.14+."""
    try:
        return datetime.now(timezone.utc).replace(tzinfo=None)
    except Exception:
        return utcnow()


SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=5000;

CREATE TABLE IF NOT EXISTS schema_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS facts (
    id              TEXT PRIMARY KEY,
    type            TEXT NOT NULL,
    content         TEXT NOT NULL,
    content_hash    TEXT NOT NULL,
    base_importance REAL NOT NULL DEFAULT 1.0,
    score           REAL NOT NULL DEFAULT 1.0,
    status          TEXT NOT NULL DEFAULT 'active',
    source          TEXT NOT NULL DEFAULT 'capture',
    source_session  TEXT,
    source_turn     INTEGER,
    confidence      REAL NOT NULL DEFAULT 1.0,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    accessed_at     TEXT,
    access_count    INTEGER NOT NULL DEFAULT 0,
    superseded_by   TEXT,
    tags            TEXT DEFAULT '[]',
    FOREIGN KEY (superseded_by) REFERENCES facts(id)
);

CREATE INDEX IF NOT EXISTS idx_facts_type ON facts(type);
CREATE INDEX IF NOT EXISTS idx_facts_status ON facts(status);
CREATE INDEX IF NOT EXISTS idx_facts_score ON facts(score DESC);
CREATE INDEX IF NOT EXISTS idx_facts_hash ON facts(content_hash);
CREATE INDEX IF NOT EXISTS idx_facts_created ON facts(created_at);

CREATE TABLE IF NOT EXISTS guardrails (
    id         TEXT PRIMARY KEY,
    content    TEXT NOT NULL,
    created_at TEXT NOT NULL,
    source     TEXT NOT NULL DEFAULT 'user',
    active     INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS access_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    fact_id    TEXT NOT NULL,
    query      TEXT,
    slot       TEXT,
    accessed_at TEXT NOT NULL,
    FOREIGN KEY (fact_id) REFERENCES facts(id)
);

CREATE INDEX IF NOT EXISTS idx_access_log_fact ON access_log(fact_id);
CREATE INDEX IF NOT EXISTS idx_access_log_date ON access_log(accessed_at);

CREATE TABLE IF NOT EXISTS reflections (
    id            TEXT PRIMARY KEY,
    date          TEXT NOT NULL,
    mode          TEXT NOT NULL,
    confidence    REAL NOT NULL DEFAULT 0.0,
    raw_output    TEXT NOT NULL,
    applied       INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_reflections_date ON reflections(date);

CREATE TABLE IF NOT EXISTS pending_queue (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    task_type  TEXT NOT NULL,
    payload    TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'pending'
);

-- FTS5 virtual table for full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(
    content,
    type,
    tags,
    content=facts,
    content_rowid=rowid,
    tokenize='unicode61 remove_diacritics 2'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS facts_ai AFTER INSERT ON facts BEGIN
    INSERT INTO facts_fts(rowid, content, type, tags)
    VALUES (new.rowid, new.content, new.type, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS facts_ad AFTER DELETE ON facts BEGIN
    INSERT INTO facts_fts(facts_fts, rowid, content, type, tags)
    VALUES ('delete', old.rowid, old.content, old.type, old.tags);
END;

CREATE TRIGGER IF NOT EXISTS facts_au AFTER UPDATE OF content, type, tags ON facts BEGIN
    INSERT INTO facts_fts(facts_fts, rowid, content, type, tags)
    VALUES ('delete', old.rowid, old.content, old.type, old.tags);
    INSERT INTO facts_fts(rowid, content, type, tags)
    VALUES (new.rowid, new.content, new.type, new.tags);
END;
"""


def load_settings():
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def content_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def generate_id(prefix: str = "f") -> str:
    ts = utcnow().strftime("%Y%m%d%H%M%S%f")[:20]
    rnd = hashlib.md5(os.urandom(8)).hexdigest()[:6]
    return f"{prefix}_{ts}_{rnd}"


def init_db(db_path: str) -> sqlite3.Connection:
    """Create database and apply schema."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_SQL)
    # Set schema version
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta (key, value) VALUES (?, ?)",
        ("schema_version", str(SCHEMA_VERSION)),
    )
    conn.commit()
    return conn


def import_memory_md(conn: sqlite3.Connection, memory_path: str):
    """Import existing MEMORY.md into facts table."""
    if not os.path.exists(memory_path):
        print(f"  No MEMORY.md found at {memory_path}, skipping import.")
        return 0

    with open(memory_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split by markdown headers or bullet points
    chunks = []
    current_section = "general"

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            current_section = re.sub(r"^#+\s*", "", line).strip().lower()
            continue
        # Remove bullet markers
        clean = re.sub(r"^[-*•]\s*", "", line).strip()
        if len(clean) >= 8:
            chunks.append((current_section, clean))

    now = utcnow().isoformat()
    imported = 0

    for section, chunk_text in chunks:
        chash = content_hash(chunk_text)
        # Check for duplicate
        existing = conn.execute(
            "SELECT id FROM facts WHERE content_hash = ?", (chash,)
        ).fetchone()
        if existing:
            continue

        fact_type = _guess_type(section, chunk_text)
        importance = 1.5 if fact_type == "guardrail" else 1.0

        fid = generate_id("imp")
        conn.execute(
            """INSERT INTO facts (id, type, content, content_hash, base_importance,
               score, status, source, confidence, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, 'active', 'import', 0.8, ?, ?)""",
            (fid, fact_type, chunk_text, chash, importance, importance, now, now),
        )
        imported += 1

    conn.commit()
    print(f"  Imported {imported} facts from MEMORY.md")
    return imported


def import_daily_logs(conn: sqlite3.Connection, logs_dir: str, max_days: int = 14):
    """Import recent daily log files into facts table."""
    if not os.path.exists(logs_dir):
        print(f"  No daily logs directory at {logs_dir}, skipping.")
        return 0

    log_files = sorted(Path(logs_dir).glob("????-??-??.md"), reverse=True)[:max_days]
    total_imported = 0
    now = utcnow().isoformat()

    for log_file in log_files:
        date_str = log_file.stem  # YYYY-MM-DD
        with open(log_file, "r", encoding="utf-8") as f:
            text = f.read()

        for line in text.split("\n"):
            line = line.strip()
            clean = re.sub(r"^[-*•]\s*", "", line).strip()
            if len(clean) < 10 or clean.startswith("#"):
                continue

            chash = content_hash(clean)
            existing = conn.execute(
                "SELECT id FROM facts WHERE content_hash = ?", (chash,)
            ).fetchone()
            if existing:
                continue

            fact_type = _guess_type("daily", clean)
            fid = generate_id("dly")
            conn.execute(
                """INSERT INTO facts (id, type, content, content_hash, base_importance,
                   score, status, source, source_session, confidence, created_at, updated_at)
                   VALUES (?, ?, ?, ?, 1.0, 0.8, 'active', 'daily_import', ?, 0.6, ?, ?)""",
                (fid, fact_type, clean, chash, date_str, f"{date_str}T00:00:00", now),
            )
            total_imported += 1

    conn.commit()
    print(f"  Imported {total_imported} facts from {len(log_files)} daily logs")
    return total_imported


def _guess_type(section: str, text: str) -> str:
    """Heuristic type classification for imported text."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["never", "always", "must", "никогда", "всегда", "обязательно"]):
        return "guardrail"
    if any(w in text_lower for w in ["decided", "decision", "chose", "решили", "решение"]):
        return "decision"
    if any(w in text_lower for w in ["prefer", "like to", "предпочитаю", "нравится"]):
        return "preference"
    if any(w in text_lower for w in ["task", "todo", "need to", "задача", "нужно"]):
        return "task"
    if any(w in text_lower for w in ["work at", "live in", "name is", "работаю", "живу"]):
        return "identity"
    if any(w in text_lower for w in ["project", "repo", "bot", "channel", "проект", "канал"]):
        return "project"
    return "insight"


def main():
    settings = load_settings()

    # Expand paths
    db_path = os.path.expanduser(settings["paths"]["db"])
    memory_path = os.path.expanduser(settings["paths"]["memory_md"])
    logs_dir = os.path.expanduser(settings["paths"]["daily_logs"])

    # Allow override via args
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    if len(sys.argv) > 2:
        memory_path = sys.argv[2]

    print(f"Memory Oracle — init_db v{SCHEMA_VERSION}")
    print(f"  Database: {db_path}")

    fresh = not os.path.exists(db_path)
    conn = init_db(db_path)

    if fresh:
        print("  Created new database with FTS5 index.")
        print("  Attempting import from existing files...")
        import_memory_md(conn, memory_path)
        import_daily_logs(conn, logs_dir)
    else:
        # Check schema version
        row = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        current = int(row[0]) if row else 0
        if current < SCHEMA_VERSION:
            print(f"  Schema upgrade needed: v{current} → v{SCHEMA_VERSION}")
            # Future: call migrate.py
        else:
            print(f"  Database exists, schema v{current}. Use --force to reimport.")

    # Stats
    total = conn.execute("SELECT COUNT(*) FROM facts WHERE status='active'").fetchone()[0]
    guards = conn.execute("SELECT COUNT(*) FROM guardrails WHERE active=1").fetchone()[0]
    print(f"  Active facts: {total}, Guardrails: {guards}")

    conn.close()
    print("  Done.")


if __name__ == "__main__":
    main()
