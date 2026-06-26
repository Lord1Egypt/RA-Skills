#!/usr/bin/env python3
"""Search Hui-Yi cold memory metadata by keyword or short query."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.common import load_tags_payload, read_text_fallback, resolve_memory_root

STATE_BOOST = {"hot": 0.2, "warm": 0.35, "cold": 0.25, "dormant": 0.05}
IMPORTANCE_BOOST = {"high": 0.35, "medium": 0.2, "low": 0.05}
STRENGTH_BOOST = {"strong": 0.25, "normal": 0.1, "weak": 0.0}


def load_tags(path: Path) -> list[dict]:
    payload = load_tags_payload(path.parent)
    notes = payload.get("notes", []) if isinstance(payload, dict) else []
    return notes if isinstance(notes, list) else []


def score_note(note: dict, query_terms: list[str]) -> tuple[float, dict]:
    fields = {
        "title": note.get("title", ""),
        "summary": note.get("summary", ""),
        "semantic_context": note.get("semantic_context", ""),
        "tags": " ".join(note.get("tags", []) if isinstance(note.get("tags"), list) else []),
        "triggers": " ".join(note.get("triggers", []) if isinstance(note.get("triggers"), list) else []),
        "scenarios": " ".join(note.get("scenarios", []) if isinstance(note.get("scenarios"), list) else []),
    }

    score = 0.0
    matched_fields = []
    for term in query_terms:
        term = term.lower().strip()
        if not term:
            continue
        if term in fields["title"].lower():
            score += 1.8
            matched_fields.append("title")
        if term in fields["summary"].lower():
            score += 1.2
            matched_fields.append("summary")
        if term in fields["semantic_context"].lower():
            score += 1.1
            matched_fields.append("semantic_context")
        if term in fields["tags"].lower():
            score += 0.8
            matched_fields.append("tags")
        if term in fields["triggers"].lower():
            score += 0.9
            matched_fields.append("triggers")
        if term in fields["scenarios"].lower():
            score += 0.7
            matched_fields.append("scenarios")

    score += IMPORTANCE_BOOST.get(note.get("importance", "medium"), 0.0)
    score += STATE_BOOST.get(note.get("state", "cold"), 0.0)
    score += STRENGTH_BOOST.get(note.get("strength", "weak"), 0.0)
    return score, {"matched_fields": sorted(set(matched_fields))}


def search_full_text(memory_root: Path, query_terms: list[str]) -> list[tuple[str, int, str]]:
    """Search note file bodies for query terms. Returns (filename, line_no, line) hits."""
    skip = {"index.md", "retrieval-log.md", "_template.md"}
    hits: list[tuple[str, int, str]] = []
    for path in sorted(memory_root.rglob("*.md")):
        if path.name in skip:
            continue
        try:
            lines = read_text_fallback(path).splitlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, 1):
            line_lower = line.lower()
            if any(term in line_lower for term in query_terms):
                hits.append((path.name, lineno, line.rstrip()))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Search Hui-Yi cold memory metadata by keyword or short query")
    parser.add_argument("query", help="keyword or short query")
    parser.add_argument("memory_root", nargs="?", default=None, help="optional cold memory root")
    parser.add_argument(
        "--full-text",
        action="store_true",
        help="Also search inside note file bodies, not just metadata",
    )
    args = parser.parse_args()

    query_raw = args.query
    query_terms = [part for part in query_raw.lower().split() if part.strip()]
    memory_root = resolve_memory_root(args.memory_root)
    index_path = memory_root / "index.md"
    tags_path = memory_root / "tags.json"

    print(f"=== Searching cold memory for: {query_raw} ===\n")

    if index_path.exists():
        lines = read_text_fallback(index_path).splitlines()
        hits = [(i + 1, line) for i, line in enumerate(lines) if any(term in line.lower() for term in query_terms)]
        if hits:
            print("## index.md matches:")
            for line_no, line in hits:
                print(f"{line_no}: {line}")
            print()
        else:
            print("## No matches in index.md\n")
    else:
        print(f"## index.md not found at {index_path}\n")

    notes = load_tags(tags_path)
    if not notes:
        print(f"## tags.json not found or empty at {tags_path}")
    else:
        ranked = []
        for note in notes:
            score, meta = score_note(note, query_terms)
            if score >= 1.0:
                ranked.append((score, note, meta))

        if not ranked:
            print("## No matches in tags.json")
        else:
            ranked.sort(key=lambda item: item[0], reverse=True)
            print("## ranked tags.json matches:")
            for score, note, meta in ranked[:10]:
                print(f"- score={score:.2f} | {note.get('title', 'untitled')} -> {note.get('path', '(missing path)')}")
                print(
                    f"  importance={note.get('importance', 'medium')} state={note.get('state', 'cold')} "
                    f"strength={note.get('strength', 'weak')} confidence={note.get('confidence', 'unknown')} "
                    f"next_review={note.get('next_review', 'n/a')}"
                )
                matched_fields = ", ".join(meta.get("matched_fields", [])) or "n/a"
                print(f"  matched_fields={matched_fields}")
            print()

    if args.full_text:
        ft_hits = search_full_text(memory_root, query_terms)
        if ft_hits:
            print("## full-text matches in note files:")
            last_file = ""
            for filename, lineno, line in ft_hits[:40]:
                if filename != last_file:
                    print(f"\n  {filename}")
                    last_file = filename
                print(f"  {lineno:4d}: {line}")
            if len(ft_hits) > 40:
                print(f"\n  ... {len(ft_hits) - 40} more lines omitted (narrow your query)")
            print()
        else:
            print("## No full-text matches in note files\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
