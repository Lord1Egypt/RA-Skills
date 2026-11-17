#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_DIR / "assets" / "bootstrap-templates"
PROFILES = ("layered", "lightweight", "memory-only")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create missing project-governance scaffold files without overwriting existing files."
    )
    parser.add_argument("--root", default=".", help="Project root to inspect or initialize.")
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        default="lightweight",
        help="Scaffold profile to use. Default: lightweight.",
    )
    parser.add_argument(
        "--project-name",
        default=None,
        help="Project name used for template placeholders. Defaults to the root directory name.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan the scaffold without writing files.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Default: text.",
    )
    return parser.parse_args()


def render_template(text: str, *, root: Path, project_name: str) -> str:
    values = {
        "PROJECT_NAME": project_name,
        "PROJECT_ROOT": str(root),
        "DATE": _dt.date.today().isoformat(),
        "DATE_COMPACT": _dt.date.today().strftime("%Y%m%d"),
    }
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def render_relative_path(rel: Path, *, root: Path, project_name: str) -> Path:
    rendered_parts = [
        render_template(".learnings" if part == "_learnings" else part, root=root, project_name=project_name) for part in rel.parts
    ]
    return Path(*rendered_parts)


def collect_plan(
    template_dir: Path, root: Path, project_name: str
) -> tuple[list[tuple[Path, Path]], list[dict[str, str]]]:
    planned: list[tuple[Path, Path]] = []
    conflicts: list[dict[str, str]] = []

    for source in sorted(template_dir.rglob("*")):
        if not source.is_file():
            continue
        rel = render_relative_path(
            source.relative_to(template_dir),
            root=root,
            project_name=project_name,
        )
        target = root / rel
        if target.exists():
            conflicts.append(
                {
                    "path": str(target),
                    "reason": "target exists; not overwritten",
                }
            )
        elif target.parent.exists() and not target.parent.is_dir():
            conflicts.append(
                {
                    "path": str(target),
                    "reason": "parent path exists but is not a directory",
                }
            )
        else:
            planned.append((source, target))
    return planned, conflicts


def write_files(
    planned: list[tuple[Path, Path]],
    *,
    root: Path,
    project_name: str,
    dry_run: bool,
) -> list[str]:
    created: list[str] = []
    for source, target in planned:
        if dry_run:
            created.append(str(target))
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        rendered = render_template(
            source.read_text(encoding="utf-8"),
            root=root,
            project_name=project_name,
        )
        target.write_text(rendered, encoding="utf-8", newline="\n")
        created.append(str(target))
    return created


def emit_text(result: dict[str, object]) -> None:
    action = "Would create" if result["dry_run"] else "Created"
    print(f"Profile: {result['profile']}")
    print(f"Project root: {result['root']}")
    print(f"{action}: {len(result['created'])}")
    for path in result["created"]:
        print(f"  + {path}")
    print(f"Conflicts: {len(result['conflicts'])}")
    for conflict in result["conflicts"]:
        print(f"  ! {conflict['path']} ({conflict['reason']})")


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Project root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    template_dir = TEMPLATE_ROOT / args.profile
    if not template_dir.exists() or not template_dir.is_dir():
        print(f"Template profile not found: {template_dir}", file=sys.stderr)
        return 2

    project_name = args.project_name or root.name
    planned, conflicts = collect_plan(template_dir, root, project_name)
    created = write_files(planned, root=root, project_name=project_name, dry_run=args.dry_run)

    result: dict[str, object] = {
        "profile": args.profile,
        "root": str(root),
        "dry_run": args.dry_run,
        "created": created,
        "conflicts": conflicts,
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
