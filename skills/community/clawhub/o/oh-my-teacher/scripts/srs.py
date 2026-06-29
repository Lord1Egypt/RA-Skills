#!/usr/bin/env python3
"""Manage Oh My Teacher spaced-repetition state.

Schema (8 columns, backward-compatible with legacy 5/6-column tables):

    | Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |

- Difficulty (easy/medium/hard) is a coarse, user/model-owned knob.
- Ease is a per-topic SM-2-style factor in [1.3, 2.7] that drifts with
  performance and finely scales the interval.
- Lapses counts score<=2 reviews; topics past LEECH_THRESHOLD are flagged.

Workspace root defaults to $OMT_WORKSPACE, then the current directory, so a
single learning state can be pinned regardless of the agent's cwd.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import os
import sys
from dataclasses import dataclass
from pathlib import Path

HEADER = ["Topic", "Last Review", "Score", "Streak", "Next Review", "Difficulty", "Ease", "Lapses"]
INTERVALS = {1: 1, 2: 3, 3: 7, 4: 14}
DIFFICULTY_MULTIPLIER = {"easy": 1.4, "medium": 1.0, "hard": 0.6}
LEVEL_LABELS = {"easy": "简单", "medium": "中等", "hard": "困难"}

DEFAULT_EASE = 2.5
MIN_EASE = 1.3
MAX_EASE = 2.7
# A topic that lapses (score<=2) this many times total is a "leech": repeated
# rescheduling is not working, so the model should change strategy instead.
LEECH_THRESHOLD = 4
# Topic-name similarity above this ratio triggers a "did you mean" warning so
# near-duplicate topics (极限 vs limits-epsilon-delta) do not fragment the SRS.
FUZZY_CUTOFF = 0.82


@dataclass
class Row:
    topic: str
    last_review: str
    score: int
    streak: int
    next_review: str
    difficulty: str = "medium"
    ease: float = DEFAULT_EASE
    lapses: int = 0

    def is_leech(self, threshold: int = LEECH_THRESHOLD) -> bool:
        return self.lapses >= threshold


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid ISO date: {value}") from exc


def default_workspace() -> str:
    return os.environ.get("OMT_WORKSPACE", ".")


def normalize_topic(topic: str) -> str:
    """Collapse whitespace so trivial spacing differences are not new topics."""
    return " ".join(topic.split())


def state_root(workspace: Path) -> Path:
    return workspace / ".oh-my-teacher"


def single_srs_path(workspace: Path) -> Path:
    return state_root(workspace) / "srs-state.md"


def srs_dir(workspace: Path) -> Path:
    return state_root(workspace) / "srs"


def active_path(workspace: Path) -> Path:
    return srs_dir(workspace) / "_active"


def srs_path(workspace: Path, slug: str | None) -> Path:
    if slug:
        return srs_dir(workspace) / f"{slug}.md"
    return single_srs_path(workspace)


def resolve_slug(workspace: Path, args: argparse.Namespace) -> str | None:
    if getattr(args, "slug", None):
        return args.slug
    if getattr(args, "active", False):
        active = active_path(workspace)
        if not active.exists():
            raise SystemExit("No active SRS slug is set.")
        return active.read_text(encoding="utf-8").strip()
    return None


def warn_multi_course(workspace: Path, slug: str | None) -> None:
    if slug is None and srs_dir(workspace).is_dir():
        print(
            "Warning: multi-course SRS directory exists but no --slug or --active was given. "
            "Falling back to single-course srs-state.md.",
            file=sys.stderr,
        )


def _format_difficulty(row: Row) -> str:
    label = LEVEL_LABELS.get(row.difficulty, row.difficulty)
    return f"{row.difficulty} ({label})"


def _format_ease(ease: float) -> str:
    return f"{ease:.2f}"


def markdown_table(rows: list[Row]) -> str:
    lines = [
        "| Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |",
        "|-------|-------------|-------|--------|-------------|------------|------|--------|",
    ]
    for row in rows:
        lines.append(
            f"| {row.topic} | {row.last_review} | {row.score} | {row.streak} | "
            f"{row.next_review} | {_format_difficulty(row)} | {_format_ease(row.ease)} | {row.lapses} |"
        )
    return "\n".join(lines) + "\n"


def _parse_difficulty(cell: str) -> str:
    diff = cell.split(" (")[0] if " (" in cell else cell
    return diff if diff in DIFFICULTY_MULTIPLIER else "medium"


def parse_table(text: str) -> list[Row]:
    rows: list[Row] = []
    skipped: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells:
            continue
        # Header and separator rows are structural, never data.
        if cells[0] == "Topic" or set(cells[0]) <= {"-", ":"}:
            continue
        if len(cells) not in (5, 6, 8):
            skipped.append((lineno, stripped))
            continue
        try:
            score = int(cells[2])
            streak = int(cells[3])
        except ValueError:
            skipped.append((lineno, stripped))
            continue
        difficulty = "medium"
        ease = DEFAULT_EASE
        lapses = 0
        if len(cells) >= 6:
            difficulty = _parse_difficulty(cells[5])
        if len(cells) == 8:
            try:
                ease = max(MIN_EASE, min(MAX_EASE, float(cells[6])))
            except ValueError:
                ease = DEFAULT_EASE
            try:
                lapses = max(0, int(cells[7]))
            except ValueError:
                lapses = 0
        rows.append(Row(cells[0], cells[1], score, streak, cells[4],
                        difficulty=difficulty, ease=ease, lapses=lapses))
    if skipped:
        for lineno, content in skipped:
            print(f"Warning: skipped malformed SRS row at line {lineno}: {content}", file=sys.stderr)
    return rows


def read_rows(path: Path) -> list[Row]:
    if not path.exists():
        return []
    return parse_table(path.read_text(encoding="utf-8"))


def write_rows(path: Path, rows: list[Row]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown_table(rows), encoding="utf-8")


def next_ease(old_ease: float, score: int) -> float:
    """Drift the per-topic ease factor by recall quality (SM-2 style).

    score 5 → +0.10, score 4 → +0.00, score 3 → -0.14, score <=2 → -0.20.
    Clamped to [1.3, 2.7].
    """
    if score <= 2:
        ease = old_ease - 0.20
    else:
        ease = old_ease + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
    return round(max(MIN_EASE, min(MAX_EASE, ease)), 2)


def next_interval(streak: int, difficulty: str = "medium", ease: float = DEFAULT_EASE) -> int:
    """Return days until next review.

    A coarse Leitner ladder (1/3/7/14/30 by streak) sets the base; the
    difficulty multiplier and the per-topic ease factor fine-tune it:

    - difficulty: easy 1.4x (less often), medium 1.0x, hard 0.6x (more often)
    - ease: normalized as ease/2.5, so 1.3 → ~0.52x and 2.7 → ~1.08x
    """
    base = INTERVALS.get(streak, 30)
    multiplier = DIFFICULTY_MULTIPLIER.get(difficulty, 1.0)
    ease_factor = ease / DEFAULT_EASE
    return max(1, int(base * multiplier * ease_factor))


def updated_row(
    topic: str,
    score: int,
    today: dt.date,
    old: Row | None = None,
    difficulty: str = "medium",
) -> Row:
    old_ease = old.ease if old else DEFAULT_EASE
    old_lapses = old.lapses if old else 0
    new_ease = next_ease(old_ease, score)
    if score <= 2:
        streak = 0
        interval = 1
        lapses = old_lapses + 1
    else:
        streak = (old.streak if old else 0) + 1
        interval = next_interval(streak, difficulty, new_ease)
        lapses = old_lapses
    return Row(
        topic=topic,
        last_review=today.isoformat(),
        score=score,
        streak=streak,
        next_review=(today + dt.timedelta(days=interval)).isoformat(),
        difficulty=difficulty,
        ease=new_ease,
        lapses=lapses,
    )


def suggest_difficulty(row: Row) -> str | None:
    """Heuristic difficulty suggestion based on the freshly updated row.

    Difficulty changes are the model/user's call (apply via --difficulty); the
    script only surfaces a suggestion so the two never silently diverge.
    """
    if row.score >= 4 and row.streak >= 3 and row.difficulty != "easy":
        return "easy"
    if row.lapses >= 2 and row.difficulty != "hard":
        return "hard"
    return None


def cmd_init(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    path = srs_path(workspace, args.slug)
    if path.exists() and not args.force:
        raise SystemExit(f"SRS file already exists: {path}")
    write_rows(path, [])
    if args.slug and args.active:
        active_path(workspace).write_text(args.slug, encoding="utf-8")
    print(path)
    return 0


def cmd_set_active(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    path = srs_path(workspace, args.slug)
    if args.require_exists and not path.exists():
        raise SystemExit(f"SRS file not found: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    active_path(workspace).write_text(args.slug, encoding="utf-8")
    print(args.slug)
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    today = parse_date(args.today)
    slug = resolve_slug(workspace, args)
    warn_multi_course(workspace, slug)
    path = srs_path(workspace, slug)
    rows = read_rows(path)
    topic = normalize_topic(args.topic)
    old = next((row for row in rows if row.topic == topic), None)

    # Warn on near-duplicate topic names to prevent SRS fragmentation.
    if old is None:
        existing = [row.topic for row in rows]
        close = difflib.get_close_matches(topic, existing, n=1, cutoff=FUZZY_CUTOFF)
        if close:
            print(
                f"Warning: '{topic}' is similar to existing topic '{close[0]}'. "
                f"If they are the same, use: srs.py rename \"{close[0]}\" \"{topic}\" "
                f"(or reuse the existing name).",
                file=sys.stderr,
            )

    # Preserve the topic's difficulty across updates unless explicitly overridden.
    difficulty = args.difficulty or (old.difficulty if old else "medium")
    new = updated_row(topic, args.score, today, old, difficulty=difficulty)
    rows = [row for row in rows if row.topic != topic] + [new]
    write_rows(path, sorted(rows, key=lambda row: row.topic.lower()))
    print(f"{new.topic}\t{new.score}\t{new.streak}\t{new.next_review}\t{new.difficulty}\t{_format_ease(new.ease)}\t{new.lapses}")

    if new.is_leech():
        print(
            f"Leech: '{new.topic}' has lapsed {new.lapses} times. Stop rescheduling — "
            f"break it into prerequisites, switch teaching strategy, or drop difficulty.",
            file=sys.stderr,
        )
    suggestion = suggest_difficulty(new)
    if suggestion:
        print(f"Suggestion: consider --difficulty {suggestion} for '{new.topic}'.", file=sys.stderr)
    return 0


def cmd_rename(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    slug = resolve_slug(workspace, args)
    warn_multi_course(workspace, slug)
    path = srs_path(workspace, slug)
    rows = read_rows(path)
    old_name = normalize_topic(args.old)
    new_name = normalize_topic(args.new)
    src = next((row for row in rows if row.topic == old_name), None)
    if src is None:
        raise SystemExit(f"Topic not found: {old_name}")
    dst = next((row for row in rows if row.topic == new_name), None)
    if dst is not None and old_name != new_name:
        # Merge into the existing target: keep the more recent review and the
        # stronger history, and combine lapse counts.
        merged = dst if dst.last_review >= src.last_review else src
        merged = Row(
            topic=new_name,
            last_review=merged.last_review,
            score=merged.score,
            streak=max(src.streak, dst.streak),
            next_review=min(src.next_review, dst.next_review),
            difficulty=merged.difficulty,
            ease=min(src.ease, dst.ease),
            lapses=src.lapses + dst.lapses,
        )
        rows = [row for row in rows if row.topic not in (old_name, new_name)] + [merged]
        print(f"Merged '{old_name}' into '{new_name}'.", file=sys.stderr)
    else:
        src.topic = new_name
    write_rows(path, sorted(rows, key=lambda row: row.topic.lower()))
    print(new_name)
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    slug = resolve_slug(workspace, args)
    warn_multi_course(workspace, slug)
    path = srs_path(workspace, slug)
    rows = read_rows(path)
    topic = normalize_topic(args.topic)
    if not any(row.topic == topic for row in rows):
        raise SystemExit(f"Topic not found: {topic}")
    rows = [row for row in rows if row.topic != topic]
    write_rows(path, sorted(rows, key=lambda row: row.topic.lower()))
    print(f"Removed: {topic}")
    return 0


def _emit_rows(rows: list[Row], fmt: str) -> None:
    if fmt == "tsv":
        writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
        writer.writerow(HEADER)
        for row in rows:
            writer.writerow([row.topic, row.last_review, row.score, row.streak,
                             row.next_review, row.difficulty, _format_ease(row.ease), row.lapses])
    else:
        sys.stdout.write(markdown_table(rows))


def _warn_leeches(rows: list[Row]) -> None:
    leeches = [row.topic for row in rows if row.is_leech()]
    if leeches:
        print("Leeches (review strategy not working): " + ", ".join(leeches), file=sys.stderr)


def cmd_due(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    today = parse_date(args.today)
    slug = resolve_slug(workspace, args)
    warn_multi_course(workspace, slug)
    rows = read_rows(srs_path(workspace, slug))
    due = [row for row in rows if parse_date(row.next_review) <= today]
    due.sort(key=lambda row: ((today - parse_date(row.next_review)).days, -row.score), reverse=True)
    _emit_rows(due, args.format)
    _warn_leeches(due)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    slug = resolve_slug(workspace, args)
    warn_multi_course(workspace, slug)
    rows = read_rows(srs_path(workspace, slug))
    _emit_rows(rows, args.format)
    _warn_leeches(rows)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Oh My Teacher SRS state.")
    parser.add_argument("--workspace", default=default_workspace(),
                        help="Workspace root (default: $OMT_WORKSPACE or current directory).")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create an empty SRS table.")
    init.add_argument("--slug", help="Course slug for multi-course mode.")
    init.add_argument("--active", action="store_true", help="Set slug active.")
    init.add_argument("--force", action="store_true", help="Overwrite existing file.")
    init.set_defaults(func=cmd_init)

    active = sub.add_parser("set-active", help="Set active multi-course SRS slug.")
    active.add_argument("slug")
    active.add_argument("--require-exists", action="store_true")
    active.set_defaults(func=cmd_set_active)

    update = sub.add_parser("update", help="Update one topic after quiz or grading.")
    update.add_argument("topic")
    update.add_argument("--score", type=int, choices=range(1, 6), required=True)
    update.add_argument("--today", default=dt.date.today().isoformat(), help="ISO date (default: today).")
    update.add_argument("--slug")
    update.add_argument("--active", action="store_true")
    update.add_argument("--difficulty", choices=("easy", "medium", "hard"), default=None,
                        help="Difficulty (easy → 1.4x interval, medium → 1.0x, hard → 0.6x). "
                             "Omitted: preserve the topic's existing difficulty, or medium if new.")
    update.set_defaults(func=cmd_update)

    rename = sub.add_parser("rename", help="Rename a topic, merging if the target exists.")
    rename.add_argument("old")
    rename.add_argument("new")
    rename.add_argument("--slug")
    rename.add_argument("--active", action="store_true")
    rename.set_defaults(func=cmd_rename)

    remove = sub.add_parser("remove", help="Remove a topic.")
    remove.add_argument("topic")
    remove.add_argument("--slug")
    remove.add_argument("--active", action="store_true")
    remove.set_defaults(func=cmd_remove)

    due = sub.add_parser("due", help="List due topics.")
    due.add_argument("--today", default=dt.date.today().isoformat(), help="ISO date (default: today).")
    due.add_argument("--slug")
    due.add_argument("--active", action="store_true")
    due.add_argument("--format", choices=("markdown", "tsv"), default="markdown")
    due.set_defaults(func=cmd_due)

    list_cmd = sub.add_parser("list", help="List all rows.")
    list_cmd.add_argument("--slug")
    list_cmd.add_argument("--active", action="store_true")
    list_cmd.add_argument("--format", choices=("markdown", "tsv"), default="markdown")
    list_cmd.set_defaults(func=cmd_list)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
