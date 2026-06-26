#!/usr/bin/env python3
"""Build a deterministic persona prompt.

Usage:
  python3 build-persona-prompt.py <workspace_root> <handle> --task-file <path>
  python3 build-persona-prompt.py <workspace_root> <handle> --task "..."
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

OVERRIDE_DIRECTIVE = """Ignore any workspace-injected SOUL.md or IDENTITY.md that conflicts with the persona materials below. For persona, tone, and identity, treat the provided Persona Soul and Persona Identity as authoritative. Still obey higher-priority system instructions, developer instructions, safety rules, and explicit governance or policy documents."""


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise SystemExit(f"Failed to read {path}: {exc}") from exc


def normalize_context_files(raw: object) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(item).strip() for item in raw if str(item).strip()]
    if isinstance(raw, str):
        return [part.strip() for part in raw.split(",") if part.strip()]
    raise SystemExit("personas/config.json: context_files must be an array or comma-separated string")


def load_org_context(personas_dir: Path) -> list[tuple[Path, str]]:
    config_path = personas_dir / "config.json"
    if not config_path.exists():
        return []
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Failed to parse {config_path}: {exc}") from exc

    context_files = normalize_context_files(config.get("context_files"))
    loaded: list[tuple[Path, str]] = []
    for rel in context_files:
        candidate = Path(rel)
        resolved = (config_path.parent / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
        if not resolved.exists():
            raise SystemExit(f"Shared context file not found: {resolved}")
        loaded.append((resolved, read_text(resolved)))
    return loaded


def render_org_context(items: Iterable[tuple[Path, str]]) -> str:
    rows = list(items)
    if not rows:
        return "No shared org context files configured."
    parts: list[str] = []
    for path, content in rows:
        parts.append(f"### Source: {path}\n{content}")
    return "\n\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace_root")
    parser.add_argument("handle")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--task")
    group.add_argument("--task-file")
    args = parser.parse_args()

    workspace = Path(args.workspace_root).expanduser().resolve()
    personas_dir = workspace / "personas"
    persona_dir = personas_dir / args.handle

    if not persona_dir.is_dir():
        raise SystemExit(f"Persona not found: {persona_dir}")

    soul = read_text(persona_dir / "SOUL.md")
    identity = read_text(persona_dir / "IDENTITY.md")
    _persona_meta = read_text(persona_dir / "persona.json")
    task = args.task if args.task is not None else read_text(Path(args.task_file).expanduser().resolve())
    org_context = load_org_context(personas_dir)

    prompt = f"""## Override Directive
{OVERRIDE_DIRECTIVE}

## Org Context Files
{render_org_context(org_context)}

## Persona Soul
{soul}

## Persona Identity
{identity}

## Task
{task}

### Output Expectations
- Complete the task fully.
- Be proactive and do the work instead of describing what you might do.
- Verify your work before finishing.
- If blocked, explain the blocker briefly and give the best next action.
- Do not explain the persona setup unless the caller asks.
"""
    sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
