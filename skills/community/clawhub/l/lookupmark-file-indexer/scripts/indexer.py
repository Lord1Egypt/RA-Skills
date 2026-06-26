#!/usr/bin/env python3
"""Filesystem metadata indexer — fast find by name/date/type/size.

Indexes only whitelisted directories. Stores metadata only (no content).
Uses SQLite with FTS5 for instant full-text search on filenames.

Usage:
    indexer.py --rebuild          # Full rebuild of index
    indexer.py --update           # Incremental update (add new, remove deleted)
    indexer.py --search "query"   # Search by filename (FTS5)
    indexer.py --stats            # Index statistics
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = os.path.expanduser("~/.local/share/file-indexer/catalog.db")

ALLOWED_ROOTS = [
    os.path.expanduser("~/Documenti"),
    os.path.expanduser("~/Scaricati"),
]

BLOCKED_DIRS = {
    ".git", ".svn", ".hg", "__pycache__", "node_modules", ".venv", "venv",
    ".ssh", ".gnupg", ".config", "credentials", ".local/share/local-rag",
    ".npm", ".cache", ".Trash",
}

SKIP_EXTENSIONS = {
    ".pyc", ".pyo", ".so", ".o", ".a", ".dylib", ".dll", ".exe",
    ".woff", ".woff2", ".ttf", ".eot", ".ico",
}

COLS = ["path", "name", "ext", "size_bytes", "modified", "indexed", "root"]


def sanitize_fts5_query(query: str) -> str:
    """Strip FTS5 special characters and operators, keep only alphanumeric + spaces."""
    # Remove FTS5 operators and special chars
    cleaned = re.sub(r'["\*\^\+\-]', ' ', query)
    cleaned = re.sub(r'\b(AND|OR|NOT)\b', ' ', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[(){}]', ' ', cleaned)
    # Collapse whitespace and strip
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def get_db():
    """Get SQLite connection, create schema with FTS5."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")

    # Main table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            ext TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            modified TEXT NOT NULL,
            indexed TEXT NOT NULL,
            root TEXT NOT NULL
        )
    """)

    # FTS5 virtual table for fast filename search
    try:
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS files_fts USING fts5(
                name, path, content='files', content_rowid=rowid
            )
        """)
        # Triggers to keep FTS in sync
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS files_ai AFTER INSERT ON files BEGIN
                INSERT INTO files_fts(rowid, name, path) VALUES (new.rowid, new.name, new.path);
            END
        """)
        conn.execute("""
            CREATE TRIGGER IF NOT EXISTS files_ad AFTER DELETE ON files BEGIN
                INSERT INTO files_fts(files_fts, rowid, name, path) VALUES('delete', old.rowid, old.name, old.path);
            END
        """)
    except sqlite3.OperationalError:
        pass  # FTS5 already exists

    conn.execute("CREATE INDEX IF NOT EXISTS idx_ext ON files(ext)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_modified ON files(modified)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_size ON files(size_bytes)")
    conn.commit()
    return conn


def should_skip_dir(dirname: str) -> bool:
    return dirname.startswith(".") or dirname in BLOCKED_DIRS


def scan_root(root: str):
    root = os.path.realpath(root)
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        for fn in filenames:
            ext = Path(fn).suffix.lower()
            if ext in SKIP_EXTENSIONS:
                continue
            full = os.path.join(dirpath, fn)
            try:
                stat = os.stat(full)
                yield {
                    "path": full, "name": fn, "ext": ext,
                    "size_bytes": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "indexed": datetime.now().isoformat(),
                    "root": root,
                }
                count += 1
                if count % 500 == 0:
                    print(f"  Scanned {count} files...", file=sys.stderr)
            except (OSError, PermissionError):
                continue


def rebuild(conn):
    # Backup existing DB before rebuild
    if os.path.exists(DB_PATH):
        backup_path = DB_PATH + ".bak"
        shutil.copy2(DB_PATH, backup_path)
        print(f"  Backup saved to {backup_path}", file=sys.stderr)
    # Drop and recreate to rebuild FTS index cleanly
    conn.execute("DROP TABLE IF EXISTS files")
    conn.execute("DROP TABLE IF EXISTS files_fts")
    conn.commit()
    conn = get_db()  # Recreate schema

    total = 0
    for root in ALLOWED_ROOTS:
        if not os.path.isdir(root):
            continue
        print(f"  Indexing {root}...")
        batch = []
        for meta in scan_root(root):
            batch.append(meta)
            if len(batch) >= 500:
                conn.executemany(
                    f"INSERT OR REPLACE INTO files VALUES ({','.join(':'+c for c in COLS)})",
                    batch
                )
                conn.commit()
                total += len(batch)
                batch = []
        if batch:
            conn.executemany(
                f"INSERT OR REPLACE INTO files VALUES ({','.join(':'+c for c in COLS)})",
                batch
            )
            conn.commit()
            total += len(batch)
    print(f"  Indexed {total} files")
    return total


def update(conn):
    existing = {row[0] for row in conn.execute("SELECT path FROM files")}
    current = set()
    added = 0

    for root in ALLOWED_ROOTS:
        if not os.path.isdir(root):
            continue
        for meta in scan_root(root):
            current.add(meta["path"])
            if meta["path"] not in existing:
                conn.execute(
                    f"INSERT OR REPLACE INTO files VALUES ({','.join(':'+c for c in COLS)})",
                    meta
                )
                added += 1

    deleted = existing - current
    if deleted:
        conn.executemany("DELETE FROM files WHERE path = ?", [(p,) for p in deleted])
    conn.commit()
    print(f"  Added: {added}, Removed: {len(deleted)}, Total: {conn.execute('SELECT COUNT(*) FROM files').fetchone()[0]}")


def search(conn, query: str, ext: str = None, min_size: int = None,
           max_size: int = None, after: str = None, limit: int = 50):
    """Search using FTS5 for fast full-text search, fallback to LIKE."""
    # Try FTS5 first
    try:
        fts_query = sanitize_fts5_query(query.strip())
        if not fts_query:
            fts_query = "*"
        sql = """
            SELECT f.* FROM files f
            JOIN files_fts ON f.rowid = files_fts.rowid
            WHERE files_fts MATCH ?
        """
        params = [fts_query]

        if ext:
            sql += " AND f.ext = ?"
            params.append(ext)
        if min_size is not None:
            sql += " AND f.size_bytes >= ?"
            params.append(min_size)
        if max_size is not None:
            sql += " AND f.size_bytes <= ?"
            params.append(max_size)
        if after:
            sql += " AND f.modified >= ?"
            params.append(after)

        sql += f" ORDER BY f.modified DESC LIMIT {limit}"
        return conn.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        # FTS5 not available, fallback to LIKE
        sql = "SELECT * FROM files WHERE name LIKE ?"
        params = [f"%{query}%"]
        if ext:
            sql += " AND ext = ?"
            params.append(ext)
        sql += f" ORDER BY modified DESC LIMIT {limit}"
        return conn.execute(sql, params).fetchall()


def format_size(size_bytes: int) -> str:
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024*1024*1024):.1f}G"
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024*1024):.1f}M"
    if size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f}K"
    return f"{size_bytes}B"


def main():
    parser = argparse.ArgumentParser(description="File metadata indexer with FTS5")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--search", "-s", help="Search by filename (FTS5)")
    parser.add_argument("--ext", help="Filter by extension")
    parser.add_argument("--min-size", type=int, help="Min size in bytes")
    parser.add_argument("--max-size", type=int, help="Max size in bytes")
    parser.add_argument("--after", help="Modified after date (YYYY-MM-DD)")
    parser.add_argument("--limit", "-n", type=int, default=50)
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    conn = get_db()

    if args.rebuild:
        rebuild(conn)
    elif args.update:
        update(conn)
    elif args.search:
        results = search(conn, args.search, args.ext, args.min_size, args.max_size, args.after, args.limit)
        if args.json:
            print(json.dumps([dict(zip(COLS, r)) for r in results], indent=2))
        else:
            if not results:
                print("No files found.")
            for r in results:
                print(f"  {format_size(r[3]):>8}  {r[4][:10]}  {r[0]}")
            print(f"\n  {len(results)} result(s)")
    elif args.stats:
        total = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
        exts = conn.execute("SELECT ext, COUNT(*) as cnt FROM files GROUP BY ext ORDER BY cnt DESC LIMIT 20").fetchall()
        total_size = conn.execute("SELECT SUM(size_bytes) FROM files").fetchone()[0] or 0
        print(f"📊 File Index: {total} files, {format_size(total_size)} total")
        print("\nTop extensions:")
        for ext, cnt in exts:
            print(f"  {ext or '(none)':<10} {cnt:>6}")
    else:
        parser.print_help()

    conn.close()


if __name__ == "__main__":
    main()
