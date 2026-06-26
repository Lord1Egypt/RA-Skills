#!/usr/bin/env python3
"""Initialize a new ppt-article-viz project folder.

Usage:
    python scripts/init_project.py <base_slug> <author> <mode> [projects_root]

Behavior:
- Prints the final slug to stdout (last line)
- Writes all diagnostic output to stderr
- Uses second-level timestamp precision
- Adds a numeric suffix when needed to avoid collisions
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class ProjectInitResult:
    slug: str
    project_dir: Path


def resolve_projects_root(raw: str | None) -> Path:
    if raw:
        path = Path(raw).expanduser()
        return path if path.is_absolute() else (Path.cwd() / path).resolve()
    return (Path.cwd() / "projects").resolve()


def build_slug(base_slug: str, now: datetime | None = None) -> str:
    ts = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
    return f"{base_slug}-{ts}"


def reserve_project_dir(projects_root: Path, initial_slug: str) -> ProjectInitResult:
    slug = initial_slug
    project_dir = projects_root / slug
    suffix = 2
    while project_dir.exists():
        slug = f"{initial_slug}-{suffix}"
        project_dir = projects_root / slug
        suffix += 1
    return ProjectInitResult(slug=slug, project_dir=project_dir)


def write_progress(project_dir: Path, slug: str, author: str, mode: str) -> None:
    started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"""# Progress — {slug}

**Source:** (set by AI after reading source file)
**Slug:** {slug}
**Author:** {author}
**Mode:** {mode}
**Started:** {started}

## Stages

phase1: pending
phase2: pending
phase3: pending
phase4: pending

## Decisions Log

"""
    (project_dir / "progress.md").write_text(content, encoding="utf-8")


def touch_artifacts(project_dir: Path) -> None:
    for name in [
        "01-analysis.md",
        "02-slide-plan.md",
        "03-visual-direction.md",
        "04-build-notes.md",
        "index.html",
    ]:
        (project_dir / name).touch()


def init_project(base_slug: str, author: str, mode: str, projects_root: Path) -> ProjectInitResult:
    projects_root.mkdir(parents=True, exist_ok=True)

    result = reserve_project_dir(projects_root, build_slug(base_slug))
    print(f"Creating project: {result.project_dir}", file=sys.stderr)
    result.project_dir.mkdir(parents=True, exist_ok=False)

    write_progress(result.project_dir, result.slug, author, mode)
    touch_artifacts(result.project_dir)

    print("Project initialized:", file=sys.stderr)
    print(f"  {result.project_dir}/", file=sys.stderr)
    print("  ├── progress.md  (written)", file=sys.stderr)
    print("  ├── 01-analysis.md", file=sys.stderr)
    print("  ├── 02-slide-plan.md", file=sys.stderr)
    print("  ├── 03-visual-direction.md", file=sys.stderr)
    print("  ├── 04-build-notes.md", file=sys.stderr)
    print("  └── index.html", file=sys.stderr)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialize a ppt-article-viz project folder.")
    parser.add_argument("base_slug")
    parser.add_argument("author", nargs="?", default="none")
    parser.add_argument("mode", nargs="?", default="review")
    parser.add_argument("projects_root", nargs="?", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    projects_root = resolve_projects_root(args.projects_root)
    result = init_project(args.base_slug, args.author, args.mode, projects_root)
    print(result.slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
