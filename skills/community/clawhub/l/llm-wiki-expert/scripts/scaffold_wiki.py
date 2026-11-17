#!/usr/bin/env python3
"""Create a minimal, non-destructive LLM Wiki workspace."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


DIRECTORIES = (
    "raw/articles",
    "raw/papers",
    "raw/notes",
    "raw/refs",
    "wiki/concepts",
    "wiki/entities",
    "wiki/summaries",
    "wiki/decisions",
    "outputs/queries",
    "audit/open",
    "audit/resolved",
    "log",
    ".wiki",
)


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Safely scaffold a Markdown-first LLM Wiki without overwriting files."
    )
    cli.add_argument("target", type=Path, help="Wiki root directory")
    cli.add_argument("--title", required=True, help="Human-readable Wiki title")
    cli.add_argument("--owner", default="unassigned", help="Default content owner")
    cli.add_argument("--dry-run", action="store_true", help="Print the plan without writing")
    cli.add_argument("--json", action="store_true", help="Emit a JSON report")
    cli.add_argument(
        "--strict",
        action="store_true",
        help="Fail when any target file already exists instead of skipping it",
    )
    return cli


def render(template: Path, title: str, owner: str) -> str:
    return (
        template.read_text(encoding="utf-8")
        .replace("{{TITLE}}", title)
        .replace("{{OWNER}}", owner)
        .replace("{{DATE}}", date.today().isoformat())
    )


def main() -> int:
    args = parser().parse_args()
    target = args.target.expanduser().resolve()
    assets = Path(__file__).resolve().parent.parent / "assets"
    file_plan = {
        target / "WIKI.md": assets / "WIKI.template.md",
        target / "wiki/index.md": assets / "index.template.md",
        target / ".wiki/config.yml": assets / "wiki-config.template.yml",
        target / ".wiki/evaluation-set.jsonl": assets / "evaluation-set.template.jsonl",
    }

    missing_assets = [str(path) for path in file_plan.values() if not path.is_file()]
    conflicts = [str(path) for path in file_plan if path.exists()]
    errors: list[str] = []
    if missing_assets:
        errors.append("missing template assets: " + ", ".join(missing_assets))
    if args.strict and conflicts:
        errors.append("strict mode refuses existing files: " + ", ".join(conflicts))

    created_dirs: list[str] = []
    created_files: list[str] = []
    skipped_files = conflicts.copy()
    if not errors and not args.dry_run:
        for relative in DIRECTORIES:
            path = target / relative
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(path))
        for destination, template in file_plan.items():
            if destination.exists():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(render(template, args.title, args.owner), encoding="utf-8")
            created_files.append(str(destination))

    report = {
        "ok": not errors,
        "dry_run": args.dry_run,
        "target": str(target),
        "planned_directories": [str(target / item) for item in DIRECTORIES],
        "planned_files": [str(item) for item in file_plan],
        "created_directories": created_dirs,
        "created_files": created_files,
        "skipped_files": skipped_files,
        "errors": errors,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        mode = "DRY RUN" if args.dry_run else "SCAFFOLD"
        print(f"[{mode}] {target}")
        for path in report["planned_files"]:
            print(f"  file: {path}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        if not errors and not args.dry_run:
            print(f"Created {len(created_dirs)} directories and {len(created_files)} files.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
