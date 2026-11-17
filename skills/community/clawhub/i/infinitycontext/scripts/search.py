#!/usr/bin/env python3
"""Query the InfinityContext SQLite archive.

Portable core: standard library only, read-only, no shell commands, no network.

The archive is produced by ``session_to_sqlite.py``: one row per conversation
chunk in ``session_chunks``, mirrored into the FTS5 table ``chunk_fts``.
FTS5 trigram search needs at least three characters; shorter queries fall back
to ``LIKE`` so two-character CJK terms still work.

Usage:
    python search.py --query "deployment token" --limit 5
    python search.py --db ~/.infinity-context/archive/agent_main_main-20260909-010203.db --query 压缩
    python search.py --archive-dir ~/.openclaw/sqlite-data --session-key agent:main:main --query goal
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

# T09：归档目录所有权校验（同目录模块，随包分发）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import secure_fs  # noqa: E402

DEFAULT_HOME = Path(os.environ.get("INFINITY_CONTEXT_HOME") or (Path.home() / ".infinity-context"))
DEFAULT_ARCHIVE = DEFAULT_HOME / "archive"

MAX_SNIPPET = 400


def pick_db(args) -> Path:
    if args.db:
        path = Path(args.db).expanduser()
        if not path.is_file():
            raise SystemExit(f"DB_NOT_FOUND: {path}")
        return path
    archive = Path(args.archive_dir).expanduser().resolve()
    if not archive.is_dir():
        raise SystemExit(f"ARCHIVE_MISSING: {archive}")
    # T09：拒绝读取属于其它本地账号的归档目录
    try:
        secure_fs.assert_safe_directory(archive)
    except secure_fs.UnsafeArchiveError as exc:
        raise SystemExit(f"SECURITY: {exc}")
    dbs = sorted((p for p in archive.glob("*.db") if p.is_file()),
                 key=lambda p: p.stat().st_mtime, reverse=True)
    if not dbs:
        raise SystemExit(f"ARCHIVE_EMPTY: no .db files in {archive}")
    return dbs[0]


def run_query(conn: sqlite3.Connection, query: str, limit: int, session_key: str | None):
    params: list = []
    where = ""
    if session_key:
        where = " AND c.session_key = ?"
        params.append(session_key)

    if len(query.strip()) >= 3:
        sql = (
            "SELECT c.session_key, c.start_msg_id, c.end_msg_id, c.summary, c.raw_content "
            "FROM chunk_fts f JOIN session_chunks c ON c.chunk_id = f.chunk_id "
            "WHERE chunk_fts MATCH ?" + where +
            " ORDER BY rank LIMIT ?"
        )
        args = [query] + params + [limit]
        try:
            return conn.execute(sql, args).fetchall()
        except sqlite3.OperationalError as exc:
            print(f"FTS_QUERY_REJECTED: {exc} (falling back to LIKE)", file=sys.stderr)

    sql = (
        "SELECT session_key, start_msg_id, end_msg_id, summary, raw_content "
        "FROM session_chunks WHERE raw_content LIKE ?" + where.replace("c.", "") +
        " ORDER BY chunk_id DESC LIMIT ?"
    )
    return conn.execute(sql, [f"%{query}%"] + params + [limit]).fetchall()


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the InfinityContext archive")
    parser.add_argument("--query", required=True, help="search text")
    parser.add_argument("--db", default=None, help="explicit SQLite archive file")
    parser.add_argument("--archive-dir", default=str(DEFAULT_ARCHIVE),
                        help=f"archive directory used when --db is omitted (default: {DEFAULT_ARCHIVE})")
    parser.add_argument("--session-key", default=None, help="restrict to one session key")
    parser.add_argument("--limit", type=int, default=10, help="max rows (default: 10)")
    parser.add_argument("--json", action="store_true", help="emit JSON lines")
    args = parser.parse_args()

    if not 1 <= args.limit <= 200:
        raise SystemExit(f"SECURITY: --limit must be 1..200, got {args.limit}")

    db = pick_db(args)
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        rows = run_query(conn, args.query, args.limit, args.session_key)
    finally:
        conn.close()

    if args.json:
        for session_key, start_id, end_id, summary, raw in rows:
            print(json.dumps({
                "db": str(db),
                "session_key": session_key,
                "start_msg_id": start_id,
                "end_msg_id": end_id,
                "summary": (summary or "")[:MAX_SNIPPET],
                "snippet": (raw or "")[:MAX_SNIPPET],
            }, ensure_ascii=False))
    else:
        print(f"DB: {db}")
        print(f"MATCHES: {len(rows)}")
        for session_key, start_id, end_id, summary, raw in rows:
            print("-" * 60)
            print(f"session : {session_key}  msgs {start_id}..{end_id}")
            if summary:
                print(f"summary : {summary[:MAX_SNIPPET]}")
            print(f"snippet : {(raw or '')[:MAX_SNIPPET]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
