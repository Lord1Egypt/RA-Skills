#!/usr/bin/env python3
"""
OpenMem - setup.py
First-run setup: verifies requirements and creates the database.

Run once after installing the skill:
  python3 ~/.openclaw/workspace/skills/openmem/scripts/setup.py

Safe to re-run — all operations are idempotent.
"""

import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

DEFAULT_DB = Path(
    os.environ.get("OPENMEM_DB", "~/.openclaw/workspace/memory/openmem.db")
).expanduser()


def check_python_version():
    if sys.version_info < (3, 8):
        return False, f"Python 3.8+ required, got {sys.version}"
    return True, f"Python {sys.version.split()[0]}"


def check_sqlite_fts5():
    try:
        db = sqlite3.connect(":memory:")
        db.execute("CREATE VIRTUAL TABLE _fts5_test USING fts5(content)")
        db.close()
        return True, f"SQLite {sqlite3.sqlite_version} with FTS5"
    except Exception as e:
        return False, f"SQLite FTS5 not available: {e}"


def check_sqlite_wal():
    """WAL mode requires sqlite 3.7+, which is universal, but verify."""
    try:
        db = sqlite3.connect(":memory:")
        db.execute("PRAGMA journal_mode=WAL")
        db.close()
        return True, "WAL mode supported"
    except Exception as e:
        return False, f"WAL mode unavailable: {e}"


def init_database(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(db_path))
    db.execute("PRAGMA journal_mode=WAL")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS memories (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            content      TEXT    NOT NULL,
            category     TEXT    NOT NULL DEFAULT 'general',
            source       TEXT    NOT NULL DEFAULT 'manual',
            importance   REAL    NOT NULL DEFAULT 0.5,
            session_id   TEXT,
            created_at   INTEGER NOT NULL,
            updated_at   INTEGER NOT NULL,
            access_count INTEGER NOT NULL DEFAULT 0
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_memories_content ON memories(content);
        CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category, created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC, created_at DESC);
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            content, content='memories', content_rowid='id', tokenize='porter ascii'
        );
        CREATE TRIGGER IF NOT EXISTS memories_fts_insert
            AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
            END;
        CREATE TRIGGER IF NOT EXISTS memories_fts_delete
            AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content)
                    VALUES ('delete', old.id, old.content);
            END;
        CREATE TRIGGER IF NOT EXISTS memories_fts_update
            AFTER UPDATE OF content ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content)
                    VALUES ('delete', old.id, old.content);
                INSERT INTO memories_fts(rowid, content) VALUES (new.id, new.content);
            END;
        CREATE TABLE IF NOT EXISTS compressed_sessions (
            session_id   TEXT PRIMARY KEY,
            session_file TEXT NOT NULL,
            compressed_at INTEGER NOT NULL,
            memory_count  INTEGER NOT NULL DEFAULT 0
        );
    """)
    db.execute("INSERT OR IGNORE INTO meta (key, value) VALUES ('schema_version', '1')")
    db.execute("INSERT OR IGNORE INTO meta (key, value) VALUES ('created_at', CAST(strftime('%s','now') AS TEXT))")
    db.commit()
    db.close()


def _openclaw(*args) -> subprocess.CompletedProcess:
    """Run an openclaw CLI command. Returns CompletedProcess or raises."""
    openclaw_bin = shutil.which("openclaw")
    if not openclaw_bin:
        raise FileNotFoundError("openclaw not found in PATH")
    return subprocess.run(
        [openclaw_bin, *args],
        capture_output=True, text=True, timeout=10
    )


def register_mcp(mcp_script: Path) -> bool:
    """Register the MCP server with openclaw. Returns True on success."""
    try:
        config = json.dumps({"command": "python3", "args": [str(mcp_script)]})
        r = _openclaw("mcp", "set", "openmem", config)
        return r.returncode == 0
    except Exception:
        return False


CRON_JOB_NAME = "openmem-compress"


def register_cron(auto_compress_script: Path) -> tuple[bool, str]:
    """Register an OpenClaw cron job to run auto_compress.py every hour.

    Uses --tools exec to prevent the agent from doing anything except running
    the script. The script itself handles all guards (inactivity, daily limit).
    """
    python3 = shutil.which("python3") or sys.executable
    message = (
        f"Run this command exactly as written and report the output:\n"
        f"python3 {auto_compress_script}"
    )
    try:
        r = _openclaw(
            "cron", "add",
            "--name", CRON_JOB_NAME,
            "--every", "1h",
            "--message", message,
            "--tools", "exec",
            "--session", "isolated",
            "--light-context",
            "--timeout-seconds", "180",
            "--no-deliver",
        )
        if r.returncode == 0:
            return True, "registered (openclaw cron, every 1h)"
        return False, r.stderr.strip() or r.stdout.strip()
    except FileNotFoundError:
        return False, "openclaw not in PATH"
    except Exception as e:
        return False, str(e)


def remove_cron() -> str:
    """Remove the OpenClaw cron job by name."""
    try:
        # Find the job ID by name
        r = _openclaw("cron", "list", "--json")
        if r.returncode != 0:
            return f"list failed: {r.stderr.strip()}"
        jobs = json.loads(r.stdout)
        job_ids = [j["id"] for j in jobs if j.get("name") == CRON_JOB_NAME]
        if not job_ids:
            return "not found"
        for jid in job_ids:
            _openclaw("cron", "rm", jid)
        return f"removed ({len(job_ids)} job(s))"
    except FileNotFoundError:
        return "skipped (openclaw not in PATH)"
    except Exception as e:
        return str(e)


def main():
    print("OpenMem Setup\n")

    checks = [
        ("Python version", check_python_version),
        ("SQLite FTS5",    check_sqlite_fts5),
        ("SQLite WAL",     check_sqlite_wal),
    ]

    all_ok = True
    for label, fn in checks:
        ok, msg = fn()
        status = "OK " if ok else "FAIL"
        print(f"  [{status}] {label}: {msg}")
        if not ok:
            all_ok = False

    if not all_ok:
        print("\nSetup failed. Resolve the issues above before using OpenMem.")
        sys.exit(1)

    print()

    # Init database
    db_path = Path(os.environ.get("OPENMEM_DB", str(DEFAULT_DB))).expanduser()
    existed = db_path.exists()
    init_database(db_path)

    if existed:
        print(f"  [OK ] Database already exists: {db_path}")
    else:
        print(f"  [OK ] Database created: {db_path}")

    scripts_dir = Path(__file__).parent

    # Register MCP server
    mcp_script = scripts_dir / "mcp_server.py"
    mcp_ok = register_mcp(mcp_script)
    if mcp_ok:
        print(f"  [OK ] MCP server registered (openmem)")
    else:
        print(f"  [SKIP] MCP registration failed or openclaw not in PATH")

    # Register OpenClaw cron job for auto-compression
    auto_compress_script = scripts_dir / "auto_compress.py"
    cron_ok, cron_msg = register_cron(auto_compress_script)
    if cron_ok:
        print(f"  [OK ] Auto-compression cron registered ({cron_msg})")
    else:
        print(f"  [SKIP] Auto-compression cron: {cron_msg}")

    print("\nOpenMem is ready.")
    print("\nRemaining steps:")
    print("  1. Enable bootstrap hook:  openclaw hooks enable openmem")
    print("  2. Restart gateway:        openclaw gateway restart")
    print()


if __name__ == "__main__":
    main()
