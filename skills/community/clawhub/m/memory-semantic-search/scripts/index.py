#!/usr/bin/env python3
"""Index markdown files in workspace into SQLite with embeddings."""

import argparse
import hashlib
import json
import math
import os
import re
import sqlite3
import struct
import sys
import urllib.request
import urllib.error

# --- Config ---

DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "memory_search.sqlite")
CHUNK_TARGET = 400  # target tokens (~chars * 0.75)
CHUNK_OVERLAP = 80
CHAR_PER_TOKEN = 4  # rough estimate

CHUNK_TARGET_CHARS = CHUNK_TARGET * CHAR_PER_TOKEN
CHUNK_OVERLAP_CHARS = CHUNK_OVERLAP * CHAR_PER_TOKEN


def init_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            line_start INTEGER NOT NULL,
            line_end INTEGER NOT NULL,
            content TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            embedding BLOB,
            UNIQUE(file_path, line_start, content_hash)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.commit()
    return conn


def chunk_markdown(text, file_path):
    """Split markdown into overlapping chunks, tracking line numbers."""
    lines = text.split("\n")
    chunks = []
    i = 0
    while i < len(lines):
        chunk_lines = []
        char_count = 0
        start = i
        while i < len(lines) and char_count < CHUNK_TARGET_CHARS:
            chunk_lines.append(lines[i])
            char_count += len(lines[i]) + 1
            i += 1
        content = "\n".join(chunk_lines).strip()
        if content:
            chunks.append({
                "file_path": file_path,
                "line_start": start + 1,
                "line_end": start + len(chunk_lines),
                "content": content,
                "content_hash": hashlib.md5(content.encode()).hexdigest(),
            })
        # overlap: rewind
        overlap_chars = 0
        rewind = 0
        for j in range(len(chunk_lines) - 1, -1, -1):
            overlap_chars += len(chunk_lines[j]) + 1
            rewind += 1
            if overlap_chars >= CHUNK_OVERLAP_CHARS:
                break
        if rewind > 0 and i < len(lines):
            i -= rewind
    return chunks


def get_embeddings(texts, api_base, api_key, model, batch_size=10):
    """Call OpenAI-compatible embedding API in batches."""
    url = f"{api_base.rstrip('/')}/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    all_embeddings = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        payload = json.dumps({"input": batch, "model": model}).encode()
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")
            print(f"Embedding API error {e.code}: {body}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Embedding request failed at batch {start}: {e}", file=sys.stderr)
            sys.exit(1)
        # sort by index to ensure order
        sorted_embs = sorted(data["data"], key=lambda x: x["index"])
        all_embeddings.extend([e["embedding"] for e in sorted_embs])
        done = start + len(batch)
        print(f"  Embedded {done}/{len(texts)} chunks", flush=True)
    return all_embeddings


def pack_vector(vec):
    """Pack float list to binary blob."""
    return struct.pack(f"{len(vec)}f", *vec)


def scan_markdown_files(workspace):
    """Find all .md files recursively."""
    md_files = []
    for root, dirs, files in os.walk(workspace):
        # skip hidden dirs and node_modules
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))
    return sorted(md_files)


def main():
    parser = argparse.ArgumentParser(description="Index markdown files for semantic search")
    parser.add_argument("workspace", nargs="?", default=os.environ.get("WORKSPACE", "."),
                        help="Workspace directory to scan (default: cwd or $WORKSPACE)")
    parser.add_argument("--db", default=os.environ.get("MSS_DB", DEFAULT_DB),
                        help="SQLite database path")
    parser.add_argument("--api-base", default=os.environ.get("EMBEDDING_API_BASE", DEFAULT_BASE_URL))
    parser.add_argument("--api-key", default=os.environ.get("EMBEDDING_API_KEY", ""))
    parser.add_argument("--model", default=os.environ.get("EMBEDDING_MODEL", DEFAULT_MODEL))
    parser.add_argument("--force", action="store_true", help="Force full reindex")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: No API key. Set EMBEDDING_API_KEY or --api-key", file=sys.stderr)
        sys.exit(1)

    workspace = os.path.abspath(args.workspace)
    db_path = os.path.abspath(args.db)
    print(f"Workspace: {workspace}")
    print(f"Database:  {db_path}")
    print(f"Provider:  {args.api_base}")
    print(f"Model:     {args.model}")

    conn = init_db(db_path)

    if args.force:
        conn.execute("DELETE FROM chunks")
        conn.commit()
        print("Cleared existing index (--force)")

    # scan files
    md_files = scan_markdown_files(workspace)
    print(f"Found {len(md_files)} markdown files")

    # chunk all files
    all_chunks = []
    for fpath in md_files:
        rel_path = os.path.relpath(fpath, workspace)
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except Exception as e:
            print(f"  Skip {rel_path}: {e}")
            continue
        chunks = chunk_markdown(text, rel_path)
        all_chunks.extend(chunks)

    print(f"Total chunks: {len(all_chunks)}")

    # filter out already-indexed chunks
    new_chunks = []
    for c in all_chunks:
        existing = conn.execute(
            "SELECT id FROM chunks WHERE file_path=? AND line_start=? AND content_hash=?",
            (c["file_path"], c["line_start"], c["content_hash"])
        ).fetchone()
        if not existing:
            new_chunks.append(c)

    # remove stale chunks (files deleted or content changed)
    indexed_files = set(c["file_path"] for c in all_chunks)
    db_files = set(r[0] for r in conn.execute("SELECT DISTINCT file_path FROM chunks").fetchall())
    stale_files = db_files - indexed_files
    if stale_files:
        for sf in stale_files:
            conn.execute("DELETE FROM chunks WHERE file_path=?", (sf,))
        conn.commit()
        print(f"Removed {len(stale_files)} stale files from index")

    if not new_chunks:
        print("Index is up to date. Nothing to embed.")
        conn.close()
        return

    print(f"New/changed chunks to embed: {len(new_chunks)}")

    # get embeddings
    texts = [c["content"] for c in new_chunks]
    embeddings = get_embeddings(texts, args.api_base, args.api_key, args.model)

    # insert
    for chunk, emb in zip(new_chunks, embeddings):
        conn.execute(
            "INSERT OR REPLACE INTO chunks (file_path, line_start, line_end, content, content_hash, embedding) VALUES (?, ?, ?, ?, ?, ?)",
            (chunk["file_path"], chunk["line_start"], chunk["line_end"],
             chunk["content"], chunk["content_hash"], pack_vector(emb))
        )
    conn.commit()

    total = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    print(f"Done. Total indexed chunks: {total}")
    conn.close()


if __name__ == "__main__":
    main()
