#!/usr/bin/env python3

# APPLIED — one-shot migration, already run in production (2026-10-05).
# Kept as a re-auditable tool: the --apply path is idempotent, and a
# dry-run still answers "is there anything left to migrate?" in seconds.
# As of 2026-10-10 the answer is NO: subject IS NULL / active rows are
# all `archive/` or `daily-note` (out of derive_subject's scope by design).

"""Migrate existing rows to v3.3 subject keys — deterministic, no LLM.

M4 root cause: `add_memory()` never accepted a `subject`, so all 4 937 facts were
indexed with subject=NULL and conflict arbitration fell back to lexical overlap.

This backfill derives the SAME deterministic key the fixed indexer now produces
(`derive_subject`), so existing rows and future re-indexes agree. It is
idempotent: running it twice is a no-op. It only touches rows whose subject is
NULL; a subject already set (e.g. by auto_capture) is never overwritten.

Dry-run by default. Pass --apply to write.
"""
import argparse
import hashlib
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "hybrid-search"))
from hybrid_search import derive_subject  # noqa: E402


def backup(db_path: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = Path(db_path).parent / "backups" / f"{Path(db_path).name}.pre-subject-migration-{stamp}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(db_path)
    dest = sqlite3.connect(str(dst))
    with dest:
        src.backup(dest)
    dest.close()
    src.close()
    return str(dst)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(Path(__file__).parent / "hybrid-search" / "agent_memory.db"))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--status", default="active", help="rows to migrate (default: active)")
    args = ap.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=5000")

    rows = conn.execute(
        "SELECT id, source, category FROM memories WHERE subject IS NULL AND status=?",
        (args.status,),
    ).fetchall()
    plan = []
    for r in rows:
        subj = derive_subject(r["source"] or "", r["category"] or "")
        if subj:
            plan.append((subj, r["id"]))
    by_subj = {}
    for subj, _ in plan:
        by_subj[subj] = by_subj.get(subj, 0) + 1

    print(f"rows subject IS NULL / status={args.status} : {len(rows)}")
    print(f"rows to receive a subject                   : {len(plan)}")
    print(f"kept subjectless (daily/archive, by design) : {len(rows) - len(plan)}")
    print(f"distinct subjects                           : {len(by_subj)}")
    for subj, n in sorted(by_subj.items(), key=lambda x: -x[1])[:10]:
        print(f"   {n:5}  {subj}")

    if not args.apply:
        print("\n(dry-run — pass --apply to write)")
        return 0

    bkp = backup(args.db)
    print(f"\nbackup: {bkp}")
    try:
        conn.execute("BEGIN IMMEDIATE")
        for subj, rid in plan:
            conn.execute("UPDATE memories SET subject=? WHERE id=? AND subject IS NULL", (subj, rid))
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    remaining = conn.execute(
        "SELECT COUNT(*) FROM memories WHERE subject IS NULL AND status=?", (args.status,)
    ).fetchone()[0]
    print(f"done. subject still NULL for status={args.status}: {remaining}")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
