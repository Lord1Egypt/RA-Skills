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
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.common import load_tags_payload, read_text_fallback, resolve_memory_root

FIELD_WEIGHTS = {
    "title": 2.2,
    "summary": 1.5,
    "semantic_context": 1.8,
    "tags": 1.0,
    "triggers": 1.2,
    "scenarios": 1.1,
}


def tokenize(text: str | None) -> list[str]:
    if not text:
        return []
    return [part for part in re.split(r"[^\w\-\u4e00-\u9fff]+", text.lower()) if part]


def field_text(note: dict, field: str) -> str:
    value = note.get(field, "")
    if isinstance(value, list):
        return " ".join(str(x) for x in value)
    if value is None:
        return ""
    return str(value)


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
    query_terms = tokenize(query)
    if not query_terms:
        return 0.0, {"matched_fields": [], "overlap_terms": [], "raw_score": 0.0, "confidence": "none"}

    matched_fields: list[str] = []
    overlap_terms: set[str] = set()
    raw_score = 0.0
    for field, weight in FIELD_WEIGHTS.items():
        text = field_text(note, field)
        field_lower = text.lower()
        field_terms = set(tokenize(text))
        field_hits = 0
        for term in query_terms:
            if term in field_lower:
                raw_score += weight
                field_hits += 1
                overlap_terms.add(term)
            elif term in field_terms:
                raw_score += weight * 0.8
                field_hits += 1
                overlap_terms.add(term)
        if field_hits:
            matched_fields.append(field)
            raw_score += min(field_hits, 3) * 0.15

    semantic_context = field_text(note, "semantic_context")
    summary = field_text(note, "summary")
    combined_terms = set(tokenize(semantic_context + " " + summary))
    if combined_terms and query_terms:
        overlap_ratio = len(set(query_terms) & combined_terms) / max(len(set(query_terms)), 1)
        raw_score += overlap_ratio * 2.0

    relevance_value = min(1.0, (0.0 if raw_score <= 0 else __import__("math").log1p(raw_score) / __import__("math").log(10)))
    strong_fields = {"title", "summary", "tags", "triggers"}
    has_strong = bool(strong_fields & set(matched_fields))

    if relevance_value >= 0.60 and has_strong:
        confidence = "high"
    elif relevance_value >= 0.30 and (has_strong or len(matched_fields) >= 2):
        confidence = "medium"
    elif relevance_value >= 0.15:
        confidence = "low"
    else:
        confidence = "none"

    return relevance_value, {
        "matched_fields": sorted(set(matched_fields)),
        "overlap_terms": sorted(overlap_terms),
        "raw_score": raw_score,
        "confidence": confidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect real-session Hui-Yi activation candidates")
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--query", default=None)
    parser.add_argument("--context-file", default=None)
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--min-relevance", type=float, default=0.30)
    parser.add_argument("--json", action="store_true", help="emit machine-readable json")
    args = parser.parse_args()

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
        candidates.append(
            {
                "title": note.get("title"),
                "path": note.get("path"),
                "relevance": relevance,
                "confidence": meta.get("confidence"),
                "matched_fields": meta.get("matched_fields", []),
                "overlap_terms": meta.get("overlap_terms", []),
                "raw_score": meta.get("raw_score", 0.0),
            }
        )

    candidates.sort(key=lambda item: item["relevance"], reverse=True)
    candidates = candidates[: args.limit]

    if args.json:
        print(json.dumps({"query": query_text, "candidates": candidates}, ensure_ascii=False, indent=2))
        return 0

    if not candidates:
        print("No session activation candidates.")
        return 0

    print("Session activation candidates:")
    for item in candidates:
        print(f"- relevance={item['relevance']:.3f} confidence={item['confidence']} | {item['title']}")
        print(f"  overlap_terms={', '.join(item['overlap_terms']) or 'n/a'}")
        print(f"  matched_fields={', '.join(item['matched_fields']) or 'n/a'}")
        print(f"  path: {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
