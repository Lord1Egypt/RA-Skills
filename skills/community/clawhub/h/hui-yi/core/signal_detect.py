#!/usr/bin/env python3
"""Detect high-confidence Hui-Yi cold-memory candidates from real session context."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.common import load_tags_payload, read_text_fallback, resolve_memory_root
from core.matching import FIELD_WEIGHTS, field_text, match_note, tokenize


def load_context_text(query: str | None, context_file: str | None, stdin_flag: bool) -> str | None:
    parts: list[str] = []
    if query:
        parts.append(query.strip())
    if context_file:
        parts.append(read_text_fallback(Path(context_file)).strip())
    if stdin_flag:
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            parts.append(stdin_text)
    combined = "\n".join(part for part in parts if part)
    return combined or None


def detect_match(note: dict, query: str) -> tuple[float, dict]:
    return match_note(note, query)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect real-session Hui-Yi activation candidates")
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--query", default=None)
    parser.add_argument("--context-file", default=None)
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--min-relevance", type=float, default=0.30)
    parser.add_argument("--json", action="store_true", help="emit machine-readable json")
    parser.add_argument("--include-sensitive", action="store_true", help="WARNING: include raw query/context and matching query terms in output; do not use for logs")
    args = parser.parse_args(argv)

    query_text = load_context_text(args.query, args.context_file, args.stdin)
    if not query_text:
        print("No query/context provided.")
        return 1

    memory_root = resolve_memory_root(args.memory_root)
    payload = load_tags_payload(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []

    candidates = []
    for note in notes:
        relevance, meta = detect_match(note, query_text)
        if relevance < args.min_relevance:
            continue
        if meta.get("confidence") == "none":
            continue
        candidate = {
            "title": note.get("title"),
            "path": note.get("path"),
            "relevance": relevance,
            "confidence": meta.get("confidence"),
            "matched_fields": meta.get("matched_fields", []),
            "raw_score": meta.get("raw_score", 0.0),
        }
        if args.include_sensitive:
            candidate["overlap_terms"] = meta.get("overlap_terms", [])
        candidates.append(candidate)

    candidates.sort(key=lambda item: item["relevance"], reverse=True)
    candidates = candidates[: args.limit]

    if args.json:
        result = {"candidates": candidates}
        if args.include_sensitive:
            result["query"] = query_text
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if not candidates:
        print("No session activation candidates.")
        return 0

    print("Session activation candidates:")
    for item in candidates:
        print(f"- relevance={item['relevance']:.3f} confidence={item['confidence']} | {item['title']}")
        if args.include_sensitive:
            print(f"  overlap_terms={', '.join(item['overlap_terms']) or 'n/a'}")
        print(f"  matched_fields={', '.join(item['matched_fields']) or 'n/a'}")
        print(f"  path: {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
