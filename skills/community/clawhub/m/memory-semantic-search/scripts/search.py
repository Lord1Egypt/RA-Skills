#!/usr/bin/env python3
"""Semantic search over indexed markdown chunks."""

import argparse
import json
import math
import os
import sqlite3
import struct
import sys
import urllib.request
import urllib.error

DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "memory_search.sqlite")
DEFAULT_TOP_K = 5
DEFAULT_MIN_SCORE = 0.3


def unpack_vector(blob):
    n = len(blob) // 4
    return struct.unpack(f"{n}f", blob)


def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def get_embedding(text, api_base, api_key, model):
    url = f"{api_base.rstrip('/')}/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = json.dumps({"input": [text], "model": model}).encode()
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"Embedding API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    return data["data"][0]["embedding"]


def search(query_vec, conn, top_k, min_score):
    rows = conn.execute(
        "SELECT file_path, line_start, line_end, content, embedding FROM chunks WHERE embedding IS NOT NULL"
    ).fetchall()

    results = []
    for file_path, line_start, line_end, content, emb_blob in rows:
        vec = unpack_vector(emb_blob)
        score = cosine_similarity(query_vec, vec)
        if score >= min_score:
            results.append({
                "file": file_path,
                "lines": f"{line_start}-{line_end}",
                "score": round(score, 4),
                "snippet": content[:700],
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def main():
    parser = argparse.ArgumentParser(description="Semantic search over indexed markdown")
    parser.add_argument("query", help="Search query text")
    parser.add_argument("--db", default=os.environ.get("MSS_DB", DEFAULT_DB))
    parser.add_argument("--api-base", default=os.environ.get("EMBEDDING_API_BASE", DEFAULT_BASE_URL))
    parser.add_argument("--api-key", default=os.environ.get("EMBEDDING_API_KEY", ""))
    parser.add_argument("--model", default=os.environ.get("EMBEDDING_MODEL", DEFAULT_MODEL))
    parser.add_argument("--top-k", type=int, default=int(os.environ.get("MSS_TOP_K", DEFAULT_TOP_K)))
    parser.add_argument("--min-score", type=float, default=float(os.environ.get("MSS_MIN_SCORE", DEFAULT_MIN_SCORE)))
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output as JSON")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: No API key. Set EMBEDDING_API_KEY or --api-key", file=sys.stderr)
        sys.exit(1)

    db_path = os.path.abspath(args.db)
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}. Run index.py first.", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    total = conn.execute("SELECT COUNT(*) FROM chunks WHERE embedding IS NOT NULL").fetchone()[0]
    if total == 0:
        print("Error: No indexed chunks. Run index.py first.", file=sys.stderr)
        sys.exit(1)

    # embed query
    query_vec = get_embedding(args.query, args.api_base, args.api_key, args.model)

    # search
    results = search(query_vec, conn, args.top_k, args.min_score)
    conn.close()

    if args.json_output:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("No results found.")
            return
        for i, r in enumerate(results, 1):
            print(f"\n--- Result {i} (score: {r['score']}) ---")
            print(f"File: {r['file']} (lines {r['lines']})")
            print(r["snippet"])


if __name__ == "__main__":
    main()
