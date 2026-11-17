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
STATE_FILE = Path(".learnings") / "GOVERNANCE_STATE.json"
LEGACY_MAP_LEARNINGS = Path(".learnings") / "LEGACY_SCAFFOLD_MAP.md"
LEGACY_MAP_LAYERED = Path("README") / "legacy-scaffold-map.md"
LEGACY_CANDIDATES = (
    "AGENTS.md",
    "README.md",
    "code.md",
    "AGENTS",
    "README",
    "code",
    "tmp.md",
    "tmp",
    ".learnings",
    "docs",
    "doc",
    "documentation",
    "notes",
    "plan",
    "plans",
    "work",
    "tasks",
    "specs",
    "design",
    "adr",
    "decisions",
    "handoff",
    ".cursor/rules",
    ".cursor",
    ".cursorrules",
    ".continue",
    ".github",
    "CLAUDE.md",
    "GEMINI.md",
    "CONTRIBUTING.md",
    "RULES.md",
    "PROJECT.md",
    "TODO.md",
    "CHANGELOG.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Adapt a project with existing docs/rules to the governance scaffold without overwriting old files."
    )
    parser.add_argument("--root", default=".", help="Project root to inspect or adapt.")
    parser.add_argument(
        "--profile",
        choices=PROFILES,
        default="lightweight",
        help="Target scaffold profile. Default: lightweight.",
    )
    parser.add_argument(
        "--project-name",
        default=None,
        help="Project name used for template placeholders. Defaults to the root directory name.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan adaptation without writing files.",
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


def detect_legacy(root: Path) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for rel in LEGACY_CANDIDATES:
        path = root / rel
        if not path.exists():
            continue
        kind = "directory" if path.is_dir() else "file"
        found.append(
            {
                "path": rel,
                "kind": kind,
                "note": "preserved in place; referenced by compatibility map",
            }
        )
    return found


def collect_template_files(
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
        if rel == STATE_FILE:
            continue
        target = root / rel
        if target.exists():
            conflicts.append(
                {
                    "path": str(target),
                    "reason": "target exists; preserved",
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


def build_legacy_map(*, root: Path, project_name: str, legacy: list[dict[str, str]]) -> str:
    today = _dt.date.today().isoformat()
    rows = "\n".join(
        f"| `{item['path']}` | {item['kind']} | {item['note']} |" for item in legacy
    )
    if not rows:
        rows = "| - | - | No legacy scaffold candidates detected. |"

    return f"""# Legacy Scaffold Map

> Last Updated: {today}
> Project: {project_name}
> Status: Compatibility adapter

This project was adapted to the project-management governance scaffold while preserving existing files in place.

## Preserved Existing Structure

| Path | Type | Adaptation Note |
| --- | --- | --- |
{rows}

## Routing

- Use `AGENTS.md` and `AGENTS/` for durable agent workflow and collaboration rules.
- Use `README.md` and `README/` for project navigation, onboarding, active work, and legacy scaffold links.
- Use `code.md` and `code/` for code contracts, commands, runtime notes, and validation procedures.
- Use `.learnings/` for candidate findings before promotion into durable docs.

## Preservation Rule

Do not move, delete, or rewrite preserved legacy scaffold files during adaptation. Link to them from the new framework and promote only validated stable content.
"""


def build_state(profile: str, legacy: list[dict[str, str]]) -> str:
    payload = {
        "project_management_governance": {
            "initialized": True,
            "adapted_from_existing_scaffold": True,
            "profile": profile,
            "created_on": _dt.date.today().isoformat(),
            "schema_version": 1,
            "memory_layer": {
                "outline": "tmp.md",
                "daily_dir": "tmp",
            },
            "history_import": {
                "status": "not_configured",
                "custom_paths": [],
            },
            "preserved_legacy_paths": [item["path"] for item in legacy],
        }
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def add_dynamic_file(
    planned_dynamic: list[tuple[Path, str]],
    conflicts: list[dict[str, str]],
    root: Path,
    rel: Path,
    content: str,
) -> None:
    target = root / rel
    if target.exists():
        conflicts.append({"path": str(target), "reason": "target exists; preserved"})
    elif target.parent.exists() and not target.parent.is_dir():
        conflicts.append({"path": str(target), "reason": "parent path exists but is not a directory"})
    else:
        planned_dynamic.append((target, content))


def write_files(
    planned_templates: list[tuple[Path, Path]],
    planned_dynamic: list[tuple[Path, str]],
    *,
    root: Path,
    project_name: str,
    dry_run: bool,
) -> list[str]:
    created: list[str] = []
    for source, target in planned_templates:
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            rendered = render_template(
                source.read_text(encoding="utf-8"),
                root=root,
                project_name=project_name,
            )
            target.write_text(rendered, encoding="utf-8", newline="\n")
        created.append(str(target))

    for target, content in planned_dynamic:
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")
        created.append(str(target))
    return created


def emit_text(result: dict[str, object]) -> None:
    action = "Would create" if result["dry_run"] else "Created"
    print(f"Profile: {result['profile']}")
    print(f"Project root: {result['root']}")
    print(f"Legacy items preserved: {len(result['legacy_scaffold'])}")
    for item in result["legacy_scaffold"]:
        print(f"  = {item['path']} ({item['kind']})")
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
    legacy = detect_legacy(root)
    planned_templates, conflicts = collect_template_files(template_dir, root, project_name)
    planned_dynamic: list[tuple[Path, str]] = []

    map_rel = LEGACY_MAP_LAYERED if args.profile == "layered" else LEGACY_MAP_LEARNINGS
    add_dynamic_file(
        planned_dynamic,
        conflicts,
        root,
        map_rel,
        build_legacy_map(root=root, project_name=project_name, legacy=legacy),
    )
    add_dynamic_file(
        planned_dynamic,
        conflicts,
        root,
        STATE_FILE,
        build_state(args.profile, legacy),
    )

    created = write_files(
        planned_templates,
        planned_dynamic,
        root=root,
        project_name=project_name,
        dry_run=args.dry_run,
    )

    result: dict[str, object] = {
        "profile": args.profile,
        "root": str(root),
        "dry_run": args.dry_run,
        "legacy_scaffold": legacy,
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
