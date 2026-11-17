#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable


SUPPORTED_EXTENSIONS = {".jsonl", ".json", ".md", ".txt", ".html", ".htm"}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__"}


def default_codex_sessions() -> Path:
    return Path.home() / ".codex" / "sessions"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory Codex sessions and custom chat exports without reading message content."
    )
    parser.add_argument(
        "--codex-sessions",
        nargs="?",
        const=str(default_codex_sessions()),
        default=None,
        help="Include Codex sessions. Optionally pass a custom sessions path.",
    )
    parser.add_argument(
        "--custom",
        action="append",
        default=[],
        help="Custom chat export file or directory. May be passed more than once.",
    )
    parser.add_argument(
        "--limit-files",
        type=int,
        default=25,
        help="Maximum sample files to show per source. Default: 25.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Default: text.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Accepted for workflow consistency; inventory is always readonly.",
    )
    return parser.parse_args()


def iter_files(path: Path) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        base = Path(root)
        for name in files:
            yield base / name


def summarize_file(path: Path) -> dict[str, object]:
    stat = path.stat()
    return {
        "path": str(path),
        "bytes": stat.st_size,
        "modified": stat.st_mtime,
    }


def inventory_source(kind: str, raw_path: str, limit_files: int) -> dict[str, object]:
    path = Path(raw_path).expanduser().resolve()
    report: dict[str, object] = {
        "kind": kind,
        "path": str(path),
        "exists": path.exists(),
        "is_dir": path.is_dir() if path.exists() else False,
        "candidate_files": 0,
        "skipped_files": 0,
        "total_bytes": 0,
        "earliest_modified": None,
        "latest_modified": None,
        "sample_files": [],
        "errors": [],
    }

    if not path.exists():
        report["errors"] = [f"path not found: {path}"]
        return report

    candidates: list[dict[str, object]] = []
    earliest: float | None = None
    latest: float | None = None
    total_bytes = 0
    skipped = 0

    for file_path in iter_files(path):
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            skipped += 1
            continue
        try:
            item = summarize_file(file_path)
        except OSError as exc:
            report["errors"].append(f"{file_path}: {exc}")
            continue
        modified = float(item["modified"])
        earliest = modified if earliest is None else min(earliest, modified)
        latest = modified if latest is None else max(latest, modified)
        total_bytes += int(item["bytes"])
        candidates.append(item)

    candidates.sort(key=lambda item: float(item["modified"]), reverse=True)
    report["candidate_files"] = len(candidates)
    report["skipped_files"] = skipped
    report["total_bytes"] = total_bytes
    report["earliest_modified"] = earliest
    report["latest_modified"] = latest
    report["sample_files"] = candidates[: max(0, limit_files)]
    return report


def format_timestamp(value: object) -> str:
    if value is None:
        return "-"
    from datetime import datetime

    return datetime.fromtimestamp(float(value)).isoformat(timespec="seconds")


def emit_text(result: dict[str, object]) -> None:
    print("History inventory is readonly; no message content was extracted.")
    for source in result["sources"]:
        print("")
        print(f"Source: {source['kind']}")
        print(f"Path: {source['path']}")
        print(f"Exists: {source['exists']}")
        print(f"Candidate files: {source['candidate_files']}")
        print(f"Skipped files: {source['skipped_files']}")
        print(f"Total bytes: {source['total_bytes']}")
        print(f"Time range: {format_timestamp(source['earliest_modified'])} to {format_timestamp(source['latest_modified'])}")
        for error in source["errors"]:
            print(f"  ! {error}")
        for item in source["sample_files"]:
            print(f"  - {item['path']} ({item['bytes']} bytes, {format_timestamp(item['modified'])})")


def main() -> int:
    args = parse_args()
    sources: list[tuple[str, str]] = []
    if args.codex_sessions is not None:
        sources.append(("codex-sessions", args.codex_sessions))
    for custom in args.custom:
        sources.append(("custom", custom))

    result: dict[str, object] = {
        "readonly": True,
        "supported_extensions": sorted(SUPPORTED_EXTENSIONS),
        "sources": [inventory_source(kind, path, args.limit_files) for kind, path in sources],
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
