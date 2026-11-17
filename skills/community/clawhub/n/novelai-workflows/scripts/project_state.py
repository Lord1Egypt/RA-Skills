#!/usr/bin/env python3
"""Manage local NovelAI project context without storing credentials."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


PROJECT_SUBDIRECTORIES = (
    "chapters",
    "images",
    "metadata",
    "metadata/generations",
)

CONTEXT_FILES = (
    ("canon.md", "Canon"),
    ("memory.md", "Memory"),
    ("lorebook.md", "Lorebook"),
    ("style.md", "Style"),
)

SENSITIVE_KEY_PARTS = (
    "token",
    "secret",
    "password",
    "authorization",
    "api_key",
    "apikey",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def project_path(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Project directory does not exist: {path}")
    return path


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def is_sensitive_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return any(part in normalized for part in SENSITIVE_KEY_PARTS)


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if is_sensitive_key(str(key)) else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def iter_existing_context(
    project: Path,
    context_files: Iterable[str],
) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    for filename, label in CONTEXT_FILES:
        path = project / filename
        if path.is_file():
            content = read_text_file(path).strip()
            if content:
                sections.append((label, content))

    for raw_path in context_files:
        path = Path(raw_path).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f"Context file does not exist: {path}")
        content = read_text_file(path).strip()
        if content:
            sections.append((f"External context: {path.name}", content))
    return sections


def compose_prompt(
    project: Path,
    task: str,
    context_files: Iterable[str],
    author_note: str,
    max_chars: int,
) -> dict[str, Any]:
    if not task.strip():
        raise ValueError("Task prompt must not be empty")
    if max_chars < len(task):
        raise ValueError("max_chars must be at least as large as the task prompt")

    sections = iter_existing_context(project, context_files)
    if author_note.strip():
        sections.append(("Author note", author_note.strip()))

    prefix_parts = [f"[{label}]\n{content}" for label, content in sections]
    prefix = "\n\n".join(prefix_parts)
    separator = "\n\n[Current task]\n"
    available = max_chars - len(separator) - len(task)
    truncated = False
    if len(prefix) > available:
        prefix = prefix[-max(0, available) :]
        truncated = True

    prompt = f"{prefix}{separator}{task.strip()}" if prefix else task.strip()
    return {
        "prompt": prompt,
        "sources": [label for label, _ in sections],
        "truncated": truncated,
        "characters": len(prompt),
        "max_chars": max_chars,
    }


def command_init(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    name = args.name.strip()
    if not name or Path(name).name != name or name in {".", ".."}:
        raise ValueError("Project name must be a single safe directory name")

    project = root / name
    if project.exists() and not args.force:
        raise ValueError(f"Project already exists: {project}")
    project.mkdir(parents=True, exist_ok=True)
    for relative in PROJECT_SUBDIRECTORIES:
        (project / relative).mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": 1,
        "name": name,
        "created_at": utc_now(),
        "files": {
            "canon": "canon.md",
            "memory": "memory.md",
            "lorebook": "lorebook.md",
            "style": "style.md",
            "chapters": "chapters/",
            "images": "images/",
            "generation_metadata": "metadata/generations/",
        },
    }
    write_json(project / "project.json", manifest)
    return {"project_dir": str(project), "manifest": manifest}


def command_compose(args: argparse.Namespace) -> dict[str, Any]:
    project = project_path(args.project_dir)
    return compose_prompt(
        project=project,
        task=args.task,
        context_files=args.context_file,
        author_note=args.author_note,
        max_chars=args.max_chars,
    )


def command_record(args: argparse.Namespace) -> dict[str, Any]:
    project = project_path(args.project_dir)
    metadata: dict[str, Any] = {}
    if args.metadata_file:
        metadata_path = Path(args.metadata_file).expanduser().resolve()
        if not metadata_path.is_file():
            raise ValueError(f"Metadata file does not exist: {metadata_path}")
        loaded = json.loads(read_text_file(metadata_path))
        if not isinstance(loaded, dict):
            raise ValueError("Metadata file must contain a JSON object")
        metadata.update(loaded)

    asset_path = Path(args.asset).expanduser().resolve() if args.asset else None
    asset: dict[str, Any] | None = None
    if asset_path:
        try:
            relative = asset_path.relative_to(project)
            asset = {"path": relative.as_posix(), "scope": "project"}
        except ValueError:
            asset = {"path": asset_path.name, "scope": "external-basename-only"}

    record = redact(
        {
            "schema_version": 1,
            "id": uuid.uuid4().hex,
            "created_at": utc_now(),
            "kind": args.kind,
            "model": args.model,
            "seed": args.seed,
            "prompt": args.prompt,
            "negative_prompt": args.negative_prompt,
            "asset": asset,
            "parameters": metadata,
        }
    )
    target = project / "metadata" / "generations" / f"{record['id']}.json"
    write_json(target, record)
    return {"record_file": str(target), "record": record}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a project layout")
    init_parser.add_argument("--root", required=True)
    init_parser.add_argument("--name", required=True)
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(handler=command_init)

    compose_parser = subparsers.add_parser("compose", help="Compose a bounded prompt")
    compose_parser.add_argument("--project-dir", required=True)
    compose_parser.add_argument("--task", required=True)
    compose_parser.add_argument("--context-file", action="append", default=[])
    compose_parser.add_argument("--author-note", default="")
    compose_parser.add_argument("--max-chars", type=int, default=30000)
    compose_parser.set_defaults(handler=command_compose)

    record_parser = subparsers.add_parser(
        "record",
        help="Record generation metadata without credentials",
    )
    record_parser.add_argument("--project-dir", required=True)
    record_parser.add_argument("--kind", required=True, choices=["text", "image", "edit"])
    record_parser.add_argument("--model", default="")
    record_parser.add_argument("--seed", type=int)
    record_parser.add_argument("--prompt", default="")
    record_parser.add_argument("--negative-prompt", default="")
    record_parser.add_argument("--asset")
    record_parser.add_argument("--metadata-file")
    record_parser.set_defaults(handler=command_record)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
