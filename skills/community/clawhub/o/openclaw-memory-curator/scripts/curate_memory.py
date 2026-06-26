#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class FileStat:
    path: Path
    lines: int
    bytes: int

    def rel(self, root: Path) -> str:
        return str(self.path.relative_to(root))


def count_lines(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text:
        return 0
    return len(text.splitlines())


def gather_stats(workspace: Path) -> list[FileStat]:
    memory_dir = workspace / "memory"
    stats: list[FileStat] = []
    if not memory_dir.is_dir():
        return stats
    for path in sorted(memory_dir.glob("*.md")):
        stats.append(FileStat(path=path, lines=count_lines(path), bytes=path.stat().st_size))
    return stats


def build_report(workspace: Path) -> dict:
    memory_dir = workspace / "memory"
    memory_md = workspace / "MEMORY.md"
    stats = gather_stats(workspace)
    total_lines = sum(item.lines for item in stats)
    total_bytes = sum(item.bytes for item in stats)
    largest = sorted(stats, key=lambda item: (item.lines, item.bytes, item.rel(workspace)), reverse=True)[:10]
    report = {
        "workspace": str(workspace),
        "memory_dir_exists": memory_dir.is_dir(),
        "memory_md_exists": memory_md.is_file(),
        "file_count": len(stats),
        "total_lines": total_lines,
        "total_bytes": total_bytes,
        "files": [
            {
                "path": item.rel(workspace),
                "lines": item.lines,
                "bytes": item.bytes,
            }
            for item in stats
        ],
        "largest_files": [
            {
                "path": item.rel(workspace),
                "lines": item.lines,
                "bytes": item.bytes,
            }
            for item in largest
        ],
    }
    if memory_md.is_file():
        report["memory_md_lines"] = count_lines(memory_md)
        report["memory_md_bytes"] = memory_md.stat().st_size
    return report


def cmd_report(workspace: Path) -> int:
    print(json.dumps(build_report(workspace), ensure_ascii=False, indent=2))
    return 0


def cmd_backup(workspace: Path) -> int:
    memory_dir = workspace / "memory"
    if not memory_dir.is_dir():
        raise SystemExit(f"memory directory not found: {memory_dir}")

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = workspace / "memory-backups" / ts
    backup_root.mkdir(parents=True, exist_ok=False)
    shutil.copytree(memory_dir, backup_root / "memory")

    memory_md = workspace / "MEMORY.md"
    if memory_md.is_file():
        shutil.copy2(memory_md, backup_root / "MEMORY.md")

    print(str(backup_root))
    return 0


def cmd_validate(workspace: Path) -> int:
    problems: list[str] = []
    if not workspace.is_dir():
        problems.append(f"workspace missing: {workspace}")
    if not (workspace / "AGENTS.md").is_file():
        problems.append("AGENTS.md missing")
    if not (workspace / "memory").is_dir():
        problems.append("memory/ directory missing")

    report = build_report(workspace)
    result = {
        "ok": not problems,
        "problems": problems,
        "report": report,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not problems else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Backup, inspect, and validate OpenClaw/Clawd memory files.")
    parser.add_argument("command", choices=["report", "backup", "validate"])
    parser.add_argument("--workspace", required=True, help="Workspace root, for example /root/clawd")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()

    if args.command == "report":
        return cmd_report(workspace)
    if args.command == "backup":
        return cmd_backup(workspace)
    if args.command == "validate":
        return cmd_validate(workspace)
    raise SystemExit(f"unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
