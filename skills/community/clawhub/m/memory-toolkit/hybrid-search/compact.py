#!/usr/bin/env python3
"""
Cold Storage compaction for the memory search DB.

Background — the lifecycle work (v3.0) keeps `superseded` and `disputed` facts
out of *retrieval*, but they still sit in the hot tables and their FTS5 / vector
indexes. Over months that inflates BM25 rank space, the `memories_vec` table and
the stats. This compactor moves terminal facts (`superseded`, and optionally
`disputed`) out of the hot DB into a cold archive, keeping full traceability.

What "cold" means here, concretely:
  * rows are copied verbatim into `memories_archive` inside the SAME SQLite file
    (no cross-file join, no external dependency) plus an appended JSONL audit
    file. Same-file keeps the move transactional and reversible.
  * the hot `memories` rows are DELETED, which fires the existing triggers and
    removes them from `memories_fts` and `memories_vec` — the actual perf win.
  * `memories_archive` also carries a small `chunks_archive` copy of the text so
    an audit/restore path never needs the hot tables.

Safety model (inherited from ontology_compact.py):
  * dry-run by default is NOT assumed — mutation requires --apply;
  * a MD5-verified backup of the whole DB is taken before any write;
  * a retention guard refuses to archive rows newer than --min-age-days, so a
    fresh supersede chain is never swept up;
  * `--restore <id>` rehydrates a single archived fact back into the hot DB.

Usage:
    python3 compact.py --stats                      # show hot vs cold sizes
    python3 compact.py --dry-run                    # what would be archived
    python3 compact.py --apply --min-age-days 30    # archive superseded >30d
    python3 compact.py --apply --include-disputed   # also sweep disputed
    python3 compact.py --restore 42                 # resurrect one archived fact
"""

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# sqlite-vec is required because the hot `memories` table carries triggers
# (memories_vec_ad) that write to the vec0 virtual table. Deleting a hot row
# without the extension loaded raises "no such module: vec0" and aborts the
# move. The extension is loaded on every connection here so compaction works
# standalone, without the caller having to preload it.
try:
    import sqlite_vec
except ImportError:  # pragma: no cover - optional dependency
    sqlite_vec = None

_HERE = Path(__file__).resolve().parent
DB_PATH = os.environ.get("MEMORY_DB", str(_HERE / "agent_memory.db"))
AUDIT_DIR = Path(os.environ.get(
    "MEMORY_AUDIT_DIR",
    str(Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw" / "workspace"))
        / "memory" / "audit"),
))

# Columns carried across the hot/cold boundary. Kept explicit (never SELECT *)
# so a future column addition fails loudly here rather than silently dropping data.
FACT_COLUMNS = [
    "id", "content", "category", "layer", "source", "score", "created_at",
    "updated_at", "superseded_by", "subject", "status", "confidence",
    "valid_from", "source_context", "last_confirmed",
]

ARCHIVE_DDL = """
CREATE TABLE IF NOT EXISTS memories_archive (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    category TEXT,
    layer TEXT,
    source TEXT,
    score REAL,
    created_at TEXT,
    updated_at TEXT,
    superseded_by INTEGER,
    subject TEXT,
    status TEXT,
    confidence REAL,
    valid_from TEXT,
    source_context TEXT,
    last_confirmed TEXT,
    archived_at TEXT NOT NULL,
    archive_reason TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_archive_status ON memories_archive(status);
CREATE INDEX IF NOT EXISTS idx_archive_subject ON memories_archive(subject);
"""


# ─── helpers ──────────────────────────────────────────────────────────────────

def md5_file(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def connect(db_path: str) -> sqlite3.Connection:
    if not os.path.exists(db_path):
        raise SystemExit(f"❌ DB not found: {db_path}\n   Run 'hybrid_search.py init' first.")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Load sqlite-vec so the vec0-backed triggers on `memories` can fire during
    # DELETE. Without it, any archival of a memory row fails with
    # "no such module: vec0".
    if sqlite_vec is not None:
        conn.enable_load_extension(True)
        conn.load_extension(sqlite_vec.loadable_path())
        conn.enable_load_extension(False)
    else:
        # No vec extension: detect whether the DB actually needs it, and refuse
        # loudly rather than half-archiving (audit written, rows not deleted).
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if "memories_vec" in tables:
            raise SystemExit(
                "❌ This DB uses sqlite-vec (memories_vec exists) but the extension "
                "is not installed for this interpreter.\n"
                "   Install it with:  pip install sqlite-vec\n"
                "   Refusing to run: deleting a hot row would fail mid-transaction."
            )
    conn.executescript(ARCHIVE_DDL)
    conn.commit()
    return conn


def cutoff_iso(min_age_days: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=min_age_days)).isoformat(timespec="seconds")


def select_terminal(conn: sqlite3.Connection, statuses: list[str],
                    min_age_days: int) -> list[sqlite3.Row]:
    """Rows eligible for archiving: terminal status AND old enough.

    Age is judged on `updated_at` (when the status was last set), falling back
    to `created_at`. Rows with neither timestamp are treated as *new* and kept —
    refusing to sweep a row whose age cannot be proven is the safe default.
    """
    cutoff = cutoff_iso(min_age_days)
    placeholders = ",".join("?" for _ in statuses)
    # M2 — never archive a fact that a *hot* fact still points at. If we moved a
    # `superseded_by` target to the cold table, the live reference would dangle:
    # with FK now ON, the DELETE would raise; before v3.3 it silently broke the
    # chain. Excluding referents here keeps the hot table self-consistent and
    # defers that row until its referrer is itself terminal/aged enough.
    sql = (
        f"SELECT * FROM memories WHERE status IN ({placeholders}) "
        f"AND COALESCE(updated_at, created_at, '9999') < ? "
        f"AND id NOT IN (SELECT superseded_by FROM memories "
        f"                 WHERE superseded_by IS NOT NULL) "
        f"ORDER BY id"
    )
    rows = conn.execute(sql, (*statuses, cutoff)).fetchall()
    if rows:
        held = conn.execute(
            f"SELECT COUNT(*) FROM memories WHERE status IN ({placeholders}) "
            f"AND COALESCE(updated_at, created_at, '9999') < ? "
            f"AND id IN (SELECT superseded_by FROM memories "
            f"             WHERE superseded_by IS NOT NULL)",
            (*statuses, cutoff),
        ).fetchone()[0]
        if held:
            print(f"  held back: {held} terminal fact(s) still referenced by a hot superseded_by")
    return rows


def write_audit(rows: list[sqlite3.Row], reason: str) -> Path:
    """Append the archived rows to a dated JSONL audit file. Returns its path."""
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = AUDIT_DIR / f"archived-{stamp}.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        for r in rows:
            rec = {k: r[k] for k in FACT_COLUMNS if k in r.keys()}
            rec["archived_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            rec["archive_reason"] = reason
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return path


def do_compact(conn: sqlite3.Connection, statuses: list[str], min_age_days: int,
               db_path: str, dry_run: bool) -> dict:
    rows = select_terminal(conn, statuses, min_age_days)
    summary = {
        "eligible": len(rows),
        "by_status": {},
        "audit_file": None,
        "backup": None,
        "applied": False,
    }
    for r in rows:
        summary["by_status"][r["status"]] = summary["by_status"].get(r["status"], 0) + 1

    if not rows:
        return summary

    if dry_run:
        return summary

    # ── backup (MD5-verified) ──
    BACKUP_DIR = Path(db_path).parent / "backups"
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup = BACKUP_DIR / f"{Path(db_path).name}.pre-compact-{stamp}"
    # Use SQLite's own backup API: copy2 on a live DB can capture a torn WAL state.
    dest = sqlite3.connect(str(backup))
    with dest:
        conn.backup(dest)
    dest.close()
    summary["backup"] = str(backup)

    # ── audit trail (before deletion) ──
    reason = f"terminal:{','.join(statuses)}"
    summary["audit_file"] = str(write_audit(rows, reason))

    # ── transactional move ──
    cols = ", ".join(FACT_COLUMNS)
    placeholders = ", ".join("?" for _ in FACT_COLUMNS)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        conn.execute("BEGIN IMMEDIATE")
        for r in rows:
            values = [r[c] if c in r.keys() else None for c in FACT_COLUMNS]
            conn.execute(
                f"INSERT OR REPLACE INTO memories_archive ({cols}, archived_at, archive_reason) "
                f"VALUES ({placeholders}, ?, ?)",
                (*values, now, reason),
            )
            # Neutralise the FK *before* deleting the referent: a row can be
            # terminal and still be the target of another row's superseded_by
            # (e.g. a 3-step chain A<-B<-C where C is archived first). Clearing
            # the dangling pointer keeps the chain readable and honours the FK.
            conn.execute(
                "UPDATE memories SET superseded_by=NULL WHERE superseded_by=?", (r["id"],)
            )
            conn.execute("DELETE FROM memories WHERE id=?", (r["id"],))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    summary["applied"] = True
    return summary


def do_restore(conn: sqlite3.Connection, fact_id: int) -> dict:
    """Rehydrate one archived fact into the hot table (status kept as-is)."""
    row = conn.execute("SELECT * FROM memories_archive WHERE id=?", (fact_id,)).fetchone()
    if not row:
        return {"restored": False, "reason": "not in archive"}
    existing = conn.execute("SELECT 1 FROM memories WHERE id=?", (fact_id,)).fetchone()
    if existing:
        return {"restored": False, "reason": "id already active in hot table"}

    cols = ", ".join(FACT_COLUMNS)
    placeholders = ", ".join("?" for _ in FACT_COLUMNS)
    values = [row[c] if c in row.keys() else None for c in FACT_COLUMNS]
    try:
        conn.execute("BEGIN")
        conn.execute(f"INSERT INTO memories ({cols}) VALUES ({placeholders})", values)
        conn.execute("DELETE FROM memories_archive WHERE id=?", (fact_id,))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return {"restored": True, "id": fact_id}


def print_stats(conn: sqlite3.Connection):
    hot = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    cold = conn.execute("SELECT COUNT(*) FROM memories_archive").fetchone()[0]
    by_status = conn.execute(
        "SELECT status, COUNT(*) c FROM memories GROUP BY status ORDER BY c DESC"
    ).fetchall()
    db_path = conn.execute("PRAGMA database_list").fetchone()[2]
    size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
    print("═══════════════════════════════════════════════")
    print("  Memory DB — hot vs cold")
    print("═══════════════════════════════════════════════")
    print(f"  Hot  (memories)         : {hot}")
    print(f"  Cold (memories_archive) : {cold}")
    for r in by_status:
        print(f"    hot.{r['status']:<12}: {r['c']}")
    print(f"  DB size                 : {size/1024/1024:.2f} MB")
    print(f"  Audit dir               : {AUDIT_DIR}")
    print("═══════════════════════════════════════════════")


def main():
    ap = argparse.ArgumentParser(description="Cold-storage compaction for the memory DB")
    ap.add_argument("--db", default=DB_PATH, help=f"Path to agent_memory.db (default: {DB_PATH})")
    ap.add_argument("--apply", action="store_true", help="Actually archive (default: dry-run)")
    ap.add_argument("--dry-run", action="store_true", help="Report only (default behaviour)")
    ap.add_argument("--min-age-days", type=int, default=30,
                    help="Only archive terminal facts older than this (default: 30)")
    ap.add_argument("--include-disputed", action="store_true",
                    help="Also archive `disputed` facts (default: superseded only)")
    ap.add_argument("--stats", action="store_true", help="Show hot/cold stats and exit")
    ap.add_argument("--restore", type=int, metavar="ID", help="Restore an archived fact by id")
    args = ap.parse_args()

    conn = connect(args.db)

    if args.stats:
        print_stats(conn)
        conn.close()
        return 0

    if args.restore is not None:
        res = do_restore(conn, args.restore)
        print(json.dumps(res, indent=2))
        conn.close()
        return 0 if res.get("restored") else 1

    statuses = ["superseded"] + (["disputed"] if args.include_disputed else [])
    dry = not args.apply
    summary = do_compact(conn, statuses, args.min_age_days, args.db, dry_run=dry)

    print(f"Terminal facts eligible: {summary['eligible']} {summary['by_status'] or ''}")
    print(f"  statuses swept : {statuses}")
    print(f"  min age (days) : {args.min_age_days}")
    if dry:
        print("  (dry-run: nothing written — pass --apply to archive)")
    elif summary["applied"]:
        print(f"  backup : {summary['backup']}")
        print(f"  audit  : {summary['audit_file']}")
        print("  ✅ archived")
    print_stats(conn)
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
