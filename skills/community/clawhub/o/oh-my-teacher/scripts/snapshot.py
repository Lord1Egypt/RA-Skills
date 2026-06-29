#!/usr/bin/env python3
"""Manage Oh My Teacher course snapshots.

This helper keeps snapshot file paths and active-course bookkeeping
deterministic so the model does not need to hand-roll them.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

SNAPSHOT_START = "## Current Course Snapshot"
SNAPSHOT_FIELD_RE = re.compile(r"^-\s+\*\*(?P<key>[^*]+)\*\*:\s*(?P<value>.*)$")
REQUIRED_FIELDS = {
    "course",
    "assessment",
    "days_left",
    "level",
    "environment",
    "materials",
    "latex",
    "weak_points",
    "completed",
    "accuracy",
    "last_action",
    "next_recommended",
}


def slugify(course: str) -> str:
    slug = course.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug, flags=re.UNICODE)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "course"


def state_root(workspace: Path) -> Path:
    return workspace / ".oh-my-teacher"


def single_snapshot_path(workspace: Path) -> Path:
    return state_root(workspace) / "snapshot.md"


def snapshots_dir(workspace: Path) -> Path:
    return state_root(workspace) / "snapshots"


def snapshot_path(workspace: Path, slug: str | None) -> Path:
    if slug:
        return snapshots_dir(workspace) / f"{slug}.md"
    return single_snapshot_path(workspace)


def active_path(workspace: Path) -> Path:
    return snapshots_dir(workspace) / "_active"


def state_json_path(workspace: Path) -> Path:
    return state_root(workspace) / "state.json"


def parse_snapshot(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    in_snapshot = False
    for line in text.splitlines():
        if line.strip() == SNAPSHOT_START:
            in_snapshot = True
            continue
        if in_snapshot and line.startswith("## "):
            break
        if not in_snapshot:
            continue
        match = SNAPSHOT_FIELD_RE.match(line)
        if match:
            key = match.group("key").strip().lower().replace(" ", "_")
            fields[key] = match.group("value").strip()
    return fields


def write_state_json(workspace: Path, text: str, slug: str | None, path: Path) -> None:
    state_root(workspace).mkdir(parents=True, exist_ok=True)
    state = {
        "active_slug": slug,
        "snapshot_path": str(path),
        "snapshot": parse_snapshot(text),
    }
    state_json_path(workspace).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def read_stdin() -> str:
    text = sys.stdin.read()
    if not text.strip():
        raise SystemExit("No snapshot content received on stdin.")
    if SNAPSHOT_START not in text:
        raise SystemExit(f"Snapshot must contain {SNAPSHOT_START!r}.")
    return text.rstrip() + "\n"


def cmd_slug(args: argparse.Namespace) -> int:
    print(slugify(args.course))
    return 0


def cmd_save(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    slug = args.slug or (slugify(args.course) if args.course else None)
    path = snapshot_path(workspace, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = read_stdin()
    path.write_text(text, encoding="utf-8")
    if slug and args.active:
        active_path(workspace).write_text(slug, encoding="utf-8")
    write_state_json(workspace, text, slug, path)
    print(path)
    return 0


def cmd_load(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    if args.json:
        path = state_json_path(workspace)
        if not path.exists():
            raise SystemExit(f"State JSON not found: {path}")
        sys.stdout.write(path.read_text(encoding="utf-8"))
        return 0
    slug = args.slug
    if slug is None and args.active:
        active_file = active_path(workspace)
        if not active_file.exists():
            raise SystemExit("No active snapshot is set.")
        slug = active_file.read_text(encoding="utf-8").strip()
    path = snapshot_path(workspace, slug)
    if not path.exists():
        raise SystemExit(f"Snapshot not found: {path}")
    sys.stdout.write(path.read_text(encoding="utf-8"))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    single = single_snapshot_path(workspace)
    if single.exists():
        print(f"single\t{single}")
    directory = snapshots_dir(workspace)
    if directory.exists():
        for path in sorted(directory.glob("*.md")):
            print(f"{path.stem}\t{path}")
    return 0


def cmd_set_active(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    if not args.slug and not args.course:
        raise SystemExit("set-active requires --slug or --course.")
    slug = args.slug or slugify(args.course)
    path = snapshot_path(workspace, slug)
    if args.require_exists and not path.exists():
        raise SystemExit(f"Snapshot not found: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    active_path(workspace).write_text(slug, encoding="utf-8")
    print(slug)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate snapshot format and report missing or malformed fields."""
    workspace = Path(args.workspace).resolve()
    slug = args.slug
    if slug is None and args.active:
        active_file = active_path(workspace)
        if not active_file.exists():
            print("No active snapshot is set.", file=sys.stderr)
            return 1
        slug = active_file.read_text(encoding="utf-8").strip()
    path = snapshot_path(workspace, slug)
    if not path.exists():
        print(f"Snapshot not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    if SNAPSHOT_START not in text:
        print(f"ERROR: Snapshot does not contain '{SNAPSHOT_START}' heading.", file=sys.stderr)
        return 1

    fields = parse_snapshot(text)
    field_keys = set(fields.keys())
    missing = REQUIRED_FIELDS - field_keys
    unknown = field_keys - REQUIRED_FIELDS

    if missing:
        print(f"WARNING: Missing {len(missing)} field(s): {', '.join(sorted(missing))}", file=sys.stderr)
    if unknown:
        print(f"NOTE: Extra field(s): {', '.join(sorted(unknown))}", file=sys.stderr)

    for key, value in sorted(fields.items()):
        print(f"  {key}: {value}")

    if args.strict and missing:
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Oh My Teacher course snapshots.")
    parser.add_argument(
        "--workspace",
        default=os.environ.get("OMT_WORKSPACE", "."),
        help="Workspace root containing .oh-my-teacher/ (default: $OMT_WORKSPACE or current directory).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    slug = sub.add_parser("slug", help="Print the deterministic slug for a course name.")
    slug.add_argument("course")
    slug.set_defaults(func=cmd_slug)

    save = sub.add_parser("save", help="Save a snapshot from stdin.")
    save.add_argument("--course", help="Course name used to derive a slug.")
    save.add_argument("--slug", help="Explicit course slug. If omitted, single-course snapshot is used unless --course is given.")
    save.add_argument("--active", action="store_true", help="Set this slug as active in multi-course mode.")
    save.set_defaults(func=cmd_save)

    load = sub.add_parser("load", help="Load a snapshot.")
    load.add_argument("--slug", help="Course slug. If omitted, single-course snapshot is used unless --active is given.")
    load.add_argument("--active", action="store_true", help="Load the active multi-course snapshot.")
    load.add_argument("--json", action="store_true", help="Load .oh-my-teacher/state.json instead of Markdown.")
    load.set_defaults(func=cmd_load)

    list_cmd = sub.add_parser("list", help="List available snapshots.")
    list_cmd.set_defaults(func=cmd_list)

    active = sub.add_parser("set-active", help="Set the active multi-course snapshot slug.")
    active.add_argument("--course", help="Course name used to derive a slug.")
    active.add_argument("--slug", help="Explicit slug.")
    active.add_argument("--require-exists", action="store_true", help="Fail unless the snapshot file already exists.")
    active.set_defaults(func=cmd_set_active)

    validate = sub.add_parser("validate", help="Check snapshot format and report missing fields.")
    validate.add_argument("--slug", help="Course slug. If omitted, single-course snapshot is validated unless --active is given.")
    validate.add_argument("--active", action="store_true", help="Validate the active multi-course snapshot.")
    validate.add_argument("--strict", action="store_true", help="Return non-zero exit code if any required field is missing.")
    validate.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
