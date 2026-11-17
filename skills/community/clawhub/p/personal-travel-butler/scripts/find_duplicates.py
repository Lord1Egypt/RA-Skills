#!/usr/bin/env python3
"""Find likely duplicate travel entries before creating new records."""

from __future__ import annotations

import argparse
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from notion_common import resolve_db  # noqa: E402
from travel_model import ENTRY_DIRS, clean_list, normalize_city_name, parse_frontmatter_file, source_label  # noqa: E402


def compact_text(value: Any) -> str:
    return "".join(str(value or "").lower().split())


def load_entry_candidates(db: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for dirname, expected_type in ENTRY_DIRS.items():
        folder = db / dirname
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            frontmatter, _, errors = parse_frontmatter_file(path)
            if errors:
                continue
            if frontmatter.get("type") != expected_type:
                continue
            candidates.append({
                "id": frontmatter.get("id"),
                "type": frontmatter.get("type"),
                "name": frontmatter.get("name") or path.stem,
                "city": normalize_city_name(frontmatter.get("city")),
                "aliases": [str(item) for item in clean_list(frontmatter.get("aliases"))],
                "tags": [str(item) for item in clean_list(frontmatter.get("tags"))],
                "source": [source_label(item) for item in clean_list(frontmatter.get("source"))],
                "address": frontmatter.get("address"),
                "path": str(path.relative_to(db)),
            })
    return candidates


def duplicate_score(candidate: dict[str, Any], name: str, city: str | None, tags: list[str], sources: list[str]) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0
    wanted_name = compact_text(name)
    candidate_names = [candidate.get("name") or "", *candidate.get("aliases", [])]
    candidate_keys = [compact_text(item) for item in candidate_names]

    if wanted_name in candidate_keys:
        score += 80
        reasons.append("same name/alias")
    else:
        best_ratio = max((SequenceMatcher(None, wanted_name, key).ratio() for key in candidate_keys if key), default=0)
        if best_ratio >= 0.82:
            score += int(best_ratio * 55)
            reasons.append(f"similar name {best_ratio:.2f}")

    if city and candidate.get("city") == normalize_city_name(city):
        score += 25
        reasons.append("same city")
    elif city and candidate.get("city"):
        score -= 15

    tag_overlap = sorted(set(tags).intersection({str(tag) for tag in candidate.get("tags", [])}))
    if tag_overlap:
        score += min(20, len(tag_overlap) * 5)
        reasons.append("shared tags: " + ", ".join(tag_overlap[:4]))

    source_overlap = sorted(set(sources).intersection({str(source) for source in candidate.get("source", [])}))
    if source_overlap:
        score += min(25, len(source_overlap) * 10)
        reasons.append("shared sources: " + ", ".join(source_overlap[:3]))

    return score, reasons


def find_duplicates(db: Path, name: str, city: str | None = None, tags: list[str] | None = None, sources: list[str] | None = None, threshold: int = 70) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    tags = tags or []
    sources = sources or []
    for candidate in load_entry_candidates(db):
        score, reasons = duplicate_score(candidate, name, city, tags, sources)
        if score >= threshold:
            matches.append({**candidate, "score": score, "reasons": reasons})
    return sorted(matches, key=lambda item: (-item["score"], item.get("city") or "", item.get("name") or ""))


def print_matches(matches: list[dict[str, Any]], as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(matches, ensure_ascii=False, sort_keys=True, indent=2))
        return
    if not matches:
        print("No likely duplicates found.")
        return
    print(f"Found {len(matches)} likely duplicate(s):")
    for match in matches:
        reasons = "; ".join(match.get("reasons") or [])
        print(f"- {match.get('id')} | {match.get('name')} | {match.get('city') or 'Unknown'} | score {match['score']} | {match['path']}")
        if reasons:
            print(f"  reasons: {reasons}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=None, help="Path to travel-db.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--city", default=None)
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--threshold", type=int, default=70)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    matches = find_duplicates(resolve_db(args.db), args.name, args.city, args.tag, args.source, args.threshold)
    print_matches(matches, args.json)
    return 2 if matches else 0


if __name__ == "__main__":
    raise SystemExit(main())
