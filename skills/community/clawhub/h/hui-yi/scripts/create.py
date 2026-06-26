#!/usr/bin/env python3
"""Create a new Hui-Yi cold memory note with proper Ebbinghaus defaults.

Usage:
  python3 scripts/create.py --title "Topic title" [options]

The note is written to <memory-root>/<slug>.md with:
  - Memory state: warm
  - interval_days: 1  (Ebbinghaus: first review tomorrow while memory is fresh)
  - next_review: today + 1 day
  - All mandatory schema sections pre-populated as placeholders

After writing the note, rebuild.py is called automatically to sync index.md
and tags.json (pass --no-rebuild to skip).
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
from datetime import date, timedelta
from pathlib import Path
import re

from core.common import resolve_memory_root, run_main_with_argv
from scripts.rebuild import main as rebuild_main

SCRIPT_DIR = Path(__file__).resolve().parent

VALID_TYPES = {"fact", "experience", "background"}
VALID_IMPORTANCE = {"high", "medium", "low"}


def slugify(title: str) -> str:
    """Convert a title to a safe filesystem slug (ASCII + CJK preserved)."""
    slug = title.lower().strip()
    # Keep word chars, hyphens, CJK characters; replace everything else with space
    slug = re.sub(r"[^\w\s\u4e00-\u9fff-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:60]


def build_note_content(title: str, memory_type: str, importance: str, tags: list[str]) -> str:
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    tags_block = "\n".join(f"- {t}" for t in tags) if tags else "- "
    return f"""\
# {title}

## TL;DR
-
-
-

## Memory type
- {memory_type}

## Importance
- {importance}

## Semantic context
1-2 sentences: describe when this note is useful and why.

## Triggers
-

## Use this when
-

## Memory state
- warm

## Review cadence
- interval_days: 1
- review_count: 0
- review_success: 0
- review_fail: 0
- retrieval_count: 0
- reinforcement_count: 0

## Last seen
- {today}

## Last reviewed
-

## Next review
- {tomorrow}

## Confidence
- medium

## Last verified
- {today}

## Session signals
- current_session_hits: 1
- recent_session_hits: 1
- cross_session_repeat_count: 1
- consecutive_session_count: 1
- last_activated: {today}

## Related tags
{tags_block}
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new Hui-Yi cold memory note with proper Ebbinghaus defaults."
    )
    parser.add_argument("--title", required=True, help="Note title (required)")
    parser.add_argument(
        "--type",
        dest="memory_type",
        default="experience",
        choices=sorted(VALID_TYPES),
        help="Memory type (default: experience)",
    )
    parser.add_argument(
        "--importance",
        default="medium",
        choices=sorted(VALID_IMPORTANCE),
        help="Importance level (default: medium)",
    )
    parser.add_argument(
        "--tags",
        default="",
        help="Comma-separated tags, e.g. --tags 'postgres,devops'",
    )
    parser.add_argument("--memory-root", default=None, help="Cold memory root path")
    parser.add_argument(
        "--no-rebuild",
        action="store_true",
        help="Skip running rebuild.py after note creation",
    )
    args = parser.parse_args()

    memory_root = resolve_memory_root(args.memory_root)
    if not memory_root.exists():
        print(f"Error: memory root not found: {memory_root}")
        print("Run first-time setup, or pass --memory-root to specify a different path.")
        return 1

    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    slug = slugify(args.title)
    if not slug:
        print("Error: title produces an empty slug. Use letters, numbers, or CJK characters.")
        return 1

    note_path = memory_root / f"{slug}.md"
    if note_path.exists():
        print(f"Error: a note already exists at: {note_path}")
        print("Use a different title or edit the existing note directly.")
        return 1

    content = build_note_content(args.title, args.memory_type, args.importance, tags)
    note_path.write_text(content, encoding="utf-8")

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    print(f"Created:      {note_path}")
    print(f"  title:      {args.title}")
    print(f"  type:       {args.memory_type}  importance: {args.importance}")
    print(f"  next_review: {tomorrow}  (Ebbinghaus +1 day)")
    if tags:
        print(f"  tags:       {', '.join(tags)}")

    if not args.no_rebuild:
        print()
        # Directly invoke rebuild logic without spawning a subprocess
        heartbeat_path = memory_root.parent / "heartbeat-state.json"
        exit_code = run_main_with_argv(
            rebuild_main,
            [
                "rebuild.py",
                "--memory-root",
                str(memory_root),
                "--heartbeat-path",
                str(heartbeat_path),
            ],
        )
        if exit_code == 0:
            print("Rebuild completed successfully via direct function call.")
        else:
            print(f"Warning: rebuild reported error (exit code {exit_code}).")
    else:
        print("\nSkipped rebuild. Run rebuild.py to update index.md and tags.json.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
