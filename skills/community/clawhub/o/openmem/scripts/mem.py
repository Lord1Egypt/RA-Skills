#!/usr/bin/env python3
"""
OpenMem - mem.py
Long-term memory store for OpenClaw agents.

Usage:
  mem.py init                          Init or migrate the database
  mem.py add TEXT [options]            Add a memory
  mem.py search QUERY [options]        Search memories (FTS + recency rank)
  mem.py get ID                        Get a single memory by ID
  mem.py list [options]                List recent memories
  mem.py update ID TEXT [options]      Update memory content
  mem.py delete ID                     Delete a memory
  mem.py stats                         Show database statistics
  mem.py export [--format json|md]     Export all memories

Options:
  --db PATH           Database path (default: ~/.openclaw/workspace/memory/openmem.db
                      or OPENMEM_DB env var)
  --category CAT      Category: fact|insight|preference|correction|event|general
  --importance FLOAT  Importance score 0.0-1.0 (default: 0.5)
  --source TEXT       Source label (default: manual)
  --limit N           Max results (default: 10)
  --json              Output as JSON lines
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

CATEGORIES = ("fact", "insight", "preference", "correction", "event", "general")
DEFAULT_DB = Path(os.environ.get("OPENMEM_DB", "~/.openclaw/workspace/memory/openmem.db")).expanduser()
CACHE_LIMIT = int(os.environ.get("OPENMEM_BOOTSTRAP_LIMIT", "20"))
SCHEMA_VERSION = 1


def write_cache(db: sqlite3.Connection, db_path: Path) -> None:
    """Write top memories to a JSON cache file the bootstrap hook reads directly.
    Called after every write operation so the hook never needs to spawn a process."""
    cache_path = db_path.parent / "openmem-cache.json"
    try:
        rows = db.execute(
            "SELECT id, content, category, importance FROM memories "
            "ORDER BY importance DESC, created_at DESC LIMIT ?",
            (CACHE_LIMIT,)
        ).fetchall()
        cache = {
            "updated_at": int(time.time()),
            "memories": [dict(r) for r in rows],
        }
        cache_path.write_text(json.dumps(cache, indent=2))
    except Exception:
        pass  # Cache write failure must never break normal operations


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def open_db(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    return db


def init_db(db: sqlite3.Connection) -> None:
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

        CREATE UNIQUE INDEX IF NOT EXISTS idx_memories_content
            ON memories(content);

        CREATE INDEX IF NOT EXISTS idx_memories_category
            ON memories(category, created_at DESC);

        CREATE INDEX IF NOT EXISTS idx_memories_importance
            ON memories(importance DESC, created_at DESC);

        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
            content,
            content='memories',
            content_rowid='id',
            tokenize='porter ascii'
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
    """)

    # Track schema version
    db.execute(
        "INSERT OR IGNORE INTO meta (key, value) VALUES ('schema_version', ?)",
        (str(SCHEMA_VERSION),)
    )
    db.commit()


def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_init(args, db):
    init_db(db)
    print(f"OK: database ready at {args.db}")


def cmd_add(args, db):
    content = args.text.strip()
    if not content:
        print("ERROR: content cannot be empty", file=sys.stderr)
        sys.exit(1)

    category = args.category or "general"
    if category not in CATEGORIES:
        print(f"ERROR: category must be one of: {', '.join(CATEGORIES)}", file=sys.stderr)
        sys.exit(1)

    importance = float(args.importance or 0.5)
    importance = max(0.0, min(1.0, importance))
    now = int(time.time())

    try:
        cur = db.execute(
            """INSERT INTO memories (content, category, source, importance, session_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (content, category, args.source or "manual", importance, args.session_id, now, now)
        )
        db.commit()
        write_cache(db, args.db)
        mem_id = cur.lastrowid
    except sqlite3.IntegrityError:
        # Duplicate content — update importance if higher
        row = db.execute("SELECT id, importance FROM memories WHERE content = ?", (content,)).fetchone()
        if row and importance > row["importance"]:
            db.execute(
                "UPDATE memories SET importance = ?, updated_at = ? WHERE id = ?",
                (importance, now, row["id"])
            )
            db.commit()
            write_cache(db, args.db)
            mem_id = row["id"]
            print(f"UPDATED: #{mem_id} (importance raised to {importance:.2f})")
        else:
            print(f"SKIP: duplicate content (existing id={row['id'] if row else '?'})")
        return

    if args.json:
        print(json.dumps({"id": mem_id, "category": category, "importance": importance}))
    else:
        print(f"OK: added memory #{mem_id} [{category}]")


def _is_wildcard_query(query: str) -> bool:
    return "*" in query or "?" in query


def _wildcard_to_like(query: str) -> str:
    """Convert shell-style wildcards (* and ?) to SQL LIKE pattern."""
    # Escape existing LIKE metacharacters first
    pattern = query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    pattern = pattern.replace("*", "%").replace("?", "_")
    return pattern


def cmd_search(args, db):
    query = args.query.strip()
    if not query:
        print("ERROR: query cannot be empty", file=sys.stderr)
        sys.exit(1)

    limit = int(args.limit or 10)
    category_filter = args.category

    if _is_wildcard_query(query):
        # LIKE search — no relevance ranking, sort by importance + recency
        like_pattern = _wildcard_to_like(query)
        sql = """
            SELECT id, content, category, source, importance,
                   created_at, access_count
            FROM memories
            WHERE content LIKE ? ESCAPE '\\' COLLATE NOCASE
        """
        params = [like_pattern]

        if category_filter:
            sql += " AND category = ?"
            params.append(category_filter)

        sql += " ORDER BY importance DESC, created_at DESC LIMIT ?"
        params.append(limit)
    else:
        # FTS search ranked by relevance + importance + recency
        sql = """
            SELECT m.id, m.content, m.category, m.source, m.importance,
                   m.created_at, m.access_count,
                   bm25(memories_fts) AS fts_rank
            FROM memories_fts
            JOIN memories m ON memories_fts.rowid = m.id
            WHERE memories_fts MATCH ?
        """
        params = [query]

        if category_filter:
            sql += " AND m.category = ?"
            params.append(category_filter)

        sql += """
            ORDER BY (bm25(memories_fts) - m.importance * 2.0
                      - (CAST(strftime('%s','now') AS REAL) - m.created_at) / 86400.0 * 0.05)
            LIMIT ?
        """
        params.append(limit)

    rows = db.execute(sql, params).fetchall()

    # Bump access count
    for row in rows:
        db.execute(
            "UPDATE memories SET access_count = access_count + 1 WHERE id = ?",
            (row["id"],)
        )
    if rows:
        db.commit()

    _print_rows(rows, args.json)


def cmd_get(args, db):
    row = db.execute("SELECT * FROM memories WHERE id = ?", (args.id,)).fetchone()
    if not row:
        print(f"ERROR: memory #{args.id} not found", file=sys.stderr)
        sys.exit(1)
    db.execute("UPDATE memories SET access_count = access_count + 1 WHERE id = ?", (args.id,))
    db.commit()
    _print_rows([row], args.json)


def cmd_list(args, db):
    limit = int(args.limit or 10)
    category_filter = args.category

    sql = "SELECT * FROM memories"
    params = []

    if category_filter:
        sql += " WHERE category = ?"
        params.append(category_filter)

    sql += " ORDER BY importance DESC, created_at DESC LIMIT ?"
    params.append(limit)

    rows = db.execute(sql, params).fetchall()
    _print_rows(rows, args.json)


def cmd_update(args, db):
    content = args.text.strip()
    if not content:
        print("ERROR: content cannot be empty", file=sys.stderr)
        sys.exit(1)

    now = int(time.time())
    fields, params = ["content = ?", "updated_at = ?"], [content, now]

    if args.category:
        if args.category not in CATEGORIES:
            print(f"ERROR: invalid category", file=sys.stderr)
            sys.exit(1)
        fields.append("category = ?")
        params.append(args.category)

    if args.importance is not None:
        fields.append("importance = ?")
        params.append(max(0.0, min(1.0, float(args.importance))))

    params.append(args.id)
    db.execute(f"UPDATE memories SET {', '.join(fields)} WHERE id = ?", params)
    db.commit()
    write_cache(db, args.db)
    print(f"OK: updated memory #{args.id}")


def cmd_delete(args, db):
    cur = db.execute("DELETE FROM memories WHERE id = ?", (args.id,))
    db.commit()
    write_cache(db, args.db)
    if cur.rowcount == 0:
        print(f"ERROR: memory #{args.id} not found", file=sys.stderr)
        sys.exit(1)
    print(f"OK: deleted memory #{args.id}")


def cmd_stats(args, db):
    total = db.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    by_cat = db.execute(
        "SELECT category, COUNT(*) AS n, AVG(importance) AS avg_imp "
        "FROM memories GROUP BY category ORDER BY n DESC"
    ).fetchall()
    oldest = db.execute("SELECT MIN(created_at) FROM memories").fetchone()[0]
    newest = db.execute("SELECT MAX(created_at) FROM memories").fetchone()[0]

    if args.json:
        print(json.dumps({
            "total": total,
            "by_category": [dict(r) for r in by_cat],
            "oldest": oldest,
            "newest": newest,
        }))
        return

    print(f"Total memories: {total}")
    if oldest:
        import datetime
        print(f"Date range: {_ts(oldest)} to {_ts(newest)}")
    print()
    print(f"{'Category':<14} {'Count':>6}  {'Avg Importance':>14}")
    print("-" * 38)
    for r in by_cat:
        print(f"{r['category']:<14} {r['n']:>6}  {r['avg_imp']:>14.2f}")


def cmd_export(args, db):
    rows = db.execute("SELECT * FROM memories ORDER BY importance DESC, created_at DESC").fetchall()
    fmt = args.format or "json"

    if fmt == "json":
        for row in rows:
            print(json.dumps(row_to_dict(row)))
    elif fmt == "md":
        print("# OpenMem Export\n")
        for row in rows:
            d = row_to_dict(row)
            ts = _ts(d["created_at"])
            print(f"## [{d['category']}] #{d['id']} (importance: {d['importance']:.2f})")
            print(f"*{ts} · source: {d['source']}*\n")
            print(d["content"])
            print()
    else:
        print(f"ERROR: unknown format '{fmt}'", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def _ts(epoch: int) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M")


def _print_rows(rows, as_json: bool) -> None:
    if not rows:
        print("(no results)")
        return

    if as_json:
        for row in rows:
            print(json.dumps(row_to_dict(row)))
        return

    for row in rows:
        d = row_to_dict(row)
        ts = _ts(d["created_at"])
        importance_bar = "█" * int(d["importance"] * 10)
        print(f"#{d['id']:>5}  [{d['category']:<12}]  {d['importance']:.1f} {importance_bar:<10}  {ts}")
        # Wrap content at 80 chars
        content = d["content"]
        if len(content) > 200:
            content = content[:197] + "..."
        for line in content.splitlines()[:3]:
            print(f"        {line}")
        print()


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mem.py", description="OpenMem - long-term memory CLI")
    p.add_argument("--db", type=Path, default=DEFAULT_DB, help="Database path")
    p.add_argument("--json", action="store_true", help="JSON output")

    sub = p.add_subparsers(dest="command", required=True)

    # init
    sub.add_parser("init", help="Initialize the database")

    # add
    a = sub.add_parser("add", help="Add a memory")
    a.add_argument("text", help="Memory content")
    a.add_argument("--category", choices=CATEGORIES)
    a.add_argument("--importance", type=float, default=0.5)
    a.add_argument("--source", default="manual")
    a.add_argument("--session-id", dest="session_id")

    # search
    s = sub.add_parser("search", help="Search memories")
    s.add_argument("query")
    s.add_argument("--category", choices=CATEGORIES)
    s.add_argument("--limit", type=int, default=10)

    # get
    g = sub.add_parser("get", help="Get a memory by ID")
    g.add_argument("id", type=int)

    # list
    li = sub.add_parser("list", help="List recent memories")
    li.add_argument("--category", choices=CATEGORIES)
    li.add_argument("--limit", type=int, default=10)

    # update
    u = sub.add_parser("update", help="Update a memory")
    u.add_argument("id", type=int)
    u.add_argument("text")
    u.add_argument("--category", choices=CATEGORIES)
    u.add_argument("--importance", type=float)

    # delete
    d = sub.add_parser("delete", help="Delete a memory")
    d.add_argument("id", type=int)

    # stats
    sub.add_parser("stats", help="Database statistics")

    # export
    e = sub.add_parser("export", help="Export memories")
    e.add_argument("--format", choices=["json", "md"], default="json")

    return p


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = build_parser()
    args = parser.parse_args()

    db = open_db(args.db)
    init_db(db)  # idempotent — safe to call on every run

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "search": cmd_search,
        "get": cmd_get,
        "list": cmd_list,
        "update": cmd_update,
        "delete": cmd_delete,
        "stats": cmd_stats,
        "export": cmd_export,
    }

    commands[args.command](args, db)
    db.close()


if __name__ == "__main__":
    main()
