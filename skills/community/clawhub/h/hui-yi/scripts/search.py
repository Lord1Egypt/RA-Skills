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
import os
import re
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.common import load_tags_payload, note_file_path, parse_heading_value, read_text_fallback, resolve_memory_root
from core.matching import match_note, note_is_retrievable
from core.safe_fs import iter_files, safe_exists

STATE_BOOST = {"hot": 0.2, "warm": 0.35, "cold": 0.25, "dormant": 0.05}
IMPORTANCE_BOOST = {"high": 0.35, "medium": 0.2, "low": 0.05}
STRENGTH_BOOST = {"strong": 0.25, "normal": 0.1, "weak": 0.0}


def load_tags(path: Path) -> list[dict]:
    payload = load_tags_payload(path.parent)
    notes = payload.get("notes", []) if isinstance(payload, dict) else []
    return notes if isinstance(notes, list) else []


def score_note(note: dict, query_terms: list[str]) -> tuple[float, dict]:
    relevance, meta = match_note(note, " ".join(query_terms))
    if not meta["match_eligible"]:
        return 0.0, meta
    metadata_boost = (IMPORTANCE_BOOST.get(note.get("importance", "medium"), 0.0)
                      + STATE_BOOST.get(note.get("state", "cold"), 0.0)
                      + STRENGTH_BOOST.get(note.get("strength", "weak"), 0.0))
    # Preserve a useful display scale while keeping metadata a bounded tie-break.
    return relevance * (3.0 + 0.1 * metadata_boost), meta


def line_matches(line: str, query_terms: list[str]) -> bool:
    _, meta = match_note({"summary": line}, " ".join(query_terms))
    return meta["match_eligible"]


def path_key(value: str) -> str:
    return value.casefold() if os.name == "nt" else value


def retrievable_paths(memory_root: Path) -> set[str] | None:
    """An existing index owns scope; unknown/unindexed notes are excluded.

    A missing tags.json permits only the explicit full-text fallback. Invalid or
    empty existing metadata has an empty scope, so it cannot bypass lifecycle
    controls. Conflicting duplicate paths are excluded conservatively.
    """
    if not safe_exists(memory_root / "tags.json"):
        return None
    included: set[str] = set()
    excluded: set[str] = set()
    for note in load_tags(memory_root / "tags.json"):
        if not isinstance(note, dict) or not note.get("path"):
            continue
        key = path_key(note_file_path(memory_root, note).relative_to(memory_root).as_posix())
        (included if note_is_retrievable(note) else excluded).add(key)
    return included - excluded


def unindexed_note_is_retrievable(text: str) -> bool:
    """Fallback honors explicit lifecycle headings in the supported note schema."""
    def value(heading: str) -> str:
        result = (parse_heading_value(text, heading) or "").strip()
        return "" if result == "-" else result
    note = {"type": value("Memory type"), "status": value("Status"),
            "superseded_by": value("Superseded by"),
            "is_fixture": value("Fixture").casefold() == "true" or value("Is fixture").casefold() == "true"}
    if value("Active").casefold() == "false":
        note["active"] = False
    return note_is_retrievable(note)


def search_index(memory_root: Path, query_terms: list[str]) -> list[tuple[int, str]]:
    """Only return lines belonging to an explicitly indexed eligible note."""
    allowed = retrievable_paths(memory_root)
    if allowed is None or not safe_exists(memory_root / "index.md"):
        return []
    hits: list[tuple[int, str]] = []
    entry_allowed = False
    for lineno, line in enumerate(read_text_fallback(memory_root / "index.md").splitlines(), 1):
        # The package's index format puts the complete relative path in backticks.
        # Unknown formats/headings have no authority to select a record.
        entry = re.match(r"^-\s+`([^`]+)`(?:\s|$)", line)
        if entry:
            relative = entry.group(1).replace("\\", "/").removeprefix("memory/cold/")
            entry_allowed = path_key(relative) in allowed
        elif line.startswith(("#", "- ")):
            entry_allowed = False
        if entry_allowed and line_matches(line, query_terms):
            hits.append((lineno, line))
    return hits


def search_full_text(memory_root: Path, query_terms: list[str]) -> list[tuple[str, int, str]]:
    """Search eligible note bodies; return full relative paths to disambiguate."""
    skip = {"index.md", "retrieval-log.md", "_template.md"}
    allowed = retrievable_paths(memory_root)
    hits: list[tuple[str, int, str]] = []
    for path in iter_files(memory_root, "*.md"):
        relative = path.relative_to(memory_root).as_posix()
        if path.name.casefold() in skip or (allowed is not None and path_key(relative) not in allowed):
            continue
        try:
            text = read_text_fallback(path)
        except OSError:
            continue
        if allowed is None and not unindexed_note_is_retrievable(text):
            continue
        lines = text.splitlines()
        for lineno, line in enumerate(lines, 1):
            if line_matches(line, query_terms):
                hits.append((relative, lineno, line.rstrip()))
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
    query_terms = [query_raw]
    memory_root = resolve_memory_root(args.memory_root)
    index_path = memory_root / "index.md"
    tags_path = memory_root / "tags.json"

    print("=== Cold memory search results ===\n")

    if safe_exists(index_path):
        hits = search_index(memory_root, query_terms)
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
            if meta.get("match_eligible"):
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
        if not safe_exists(tags_path):
            print("## tags.json is absent; full-text fallback uses note lifecycle headings (rebuild metadata for indexed retrieval).\n")
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
