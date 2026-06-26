#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def openclaw_root() -> Path:
    return Path(os.environ.get("OPENCLAW_HOME", "~/.openclaw")).expanduser()


def workspace_root() -> Path:
    return openclaw_root() / "workspace"


def long_memory_path() -> Path:
    return workspace_root() / "MEMORY.md"


def daily_memory_dir() -> Path:
    return workspace_root() / "memory"


def sqlite_db_path() -> Path:
    return openclaw_root() / "memory" / "main.sqlite"


@dataclass
class Result:
    path: str
    source: str
    score: int
    snippet: str


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def tokenize(query: str) -> list[str]:
    return [part.casefold() for part in query.split() if part.strip()]


def snippet_for(text: str, query: str, width: int = 140) -> str:
    compact = normalize_text(text)
    if not compact:
        return ""
    lower = compact.casefold()
    q = query.casefold()
    idx = lower.find(q)
    if idx < 0:
        idx = 0
    start = max(0, idx - width // 3)
    end = min(len(compact), start + width)
    snippet = compact[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(compact):
        snippet = snippet + "..."
    return snippet


def score_text(text: str, tokens: Iterable[str]) -> int:
    lowered = text.casefold()
    return sum(lowered.count(token) for token in tokens)


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    long_memory = long_memory_path()
    daily_dir = daily_memory_dir()
    if long_memory.exists():
        files.append(long_memory)
    if daily_dir.exists():
        files.extend(sorted(daily_dir.glob("*.md"), reverse=True))
    return files


def search_markdown(query: str, limit: int) -> list[Result]:
    tokens = tokenize(query)
    results: list[Result] = []
    for path in iter_markdown_files():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        score = score_text(text, tokens)
        if score <= 0:
            continue
        results.append(
            Result(
                path=str(path),
                source="markdown",
                score=score,
                snippet=snippet_for(text, query),
            )
        )
    results.sort(key=lambda item: (-item.score, item.path))
    return results[:limit]


def search_sqlite(query: str, limit: int) -> list[Result]:
    sqlite_db = sqlite_db_path()
    if not sqlite_db.exists():
        return []

    tokens = tokenize(query)
    if not tokens:
        return []

    clauses = " OR ".join(["lower(text) LIKE ?" for _ in tokens])
    params = [f"%{token}%" for token in tokens]
    sql = f"""
        SELECT path, text
        FROM chunks
        WHERE {clauses}
        ORDER BY updated_at DESC
        LIMIT ?
    """

    try:
        conn = sqlite3.connect(sqlite_db)
        rows = conn.execute(sql, (*params, limit * 3)).fetchall()
    except sqlite3.Error:
        return []
    finally:
        try:
            conn.close()
        except Exception:
            pass

    results: list[Result] = []
    workspace = workspace_root()
    for path, text in rows:
        score = score_text(text, tokens)
        if score <= 0:
            continue
        resolved = path
        if not os.path.isabs(resolved):
            resolved = str(workspace / resolved)
        results.append(
            Result(
                path=resolved,
                source="sqlite-chunks",
                score=score,
                snippet=snippet_for(text, query),
            )
        )

    deduped: dict[str, Result] = {}
    for item in results:
        prior = deduped.get(item.path)
        if prior is None or item.score > prior.score:
            deduped[item.path] = item
    return sorted(deduped.values(), key=lambda item: (-item.score, item.path))[:limit]


def command_search(args: argparse.Namespace) -> int:
    markdown_results = search_markdown(args.query, args.limit)
    seen = {item.path for item in markdown_results}
    sqlite_results = [item for item in search_sqlite(args.query, args.limit) if item.path not in seen]
    results = (markdown_results + sqlite_results)[: args.limit]

    if args.json:
        print(json.dumps([item.__dict__ for item in results], ensure_ascii=False, indent=2))
        return 0

    if not results:
        print("No OpenClaw memory matches found.")
        return 1

    for item in results:
        print(f"[{item.source}] score={item.score} {item.path}")
        print(f"  {item.snippet}")
    return 0


def command_recent(args: argparse.Namespace) -> int:
    files = iter_markdown_files()
    if not files:
        print("No OpenClaw markdown memory files found.")
        return 1
    for path in files[: args.limit]:
        print(path)
    return 0


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def append_text(path: Path, text: str, heading: str | None = None) -> None:
    ensure_parent(path)
    exists_before = path.exists()
    prefix = ""
    if not exists_before and heading:
        prefix = heading + "\n\n"

    with path.open("a", encoding="utf-8") as handle:
        if prefix:
            handle.write(prefix)
        if exists_before and path.stat().st_size > 0:
            handle.write("\n")
        handle.write(text.rstrip() + "\n")


def command_append(args: argparse.Namespace) -> int:
    text = args.text.strip()
    if not text:
        print("Refusing to append empty text.", file=sys.stderr)
        return 2

    if args.scope == "long":
        target = long_memory_path()
        heading = None
    else:
        date_str = args.date or dt.date.today().isoformat()
        target = daily_memory_dir() / f"{date_str}.md"
        heading = f"# {date_str}"

    if args.dry_run:
        print(json.dumps({"target": str(target), "text": text, "scope": args.scope}, ensure_ascii=False, indent=2))
        return 0

    append_text(target, text, heading=heading)
    print(target)
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    report = {
        "openclaw_root": str(openclaw_root()),
        "workspace": str(workspace_root()),
        "long_memory": str(long_memory_path()),
        "daily_memory_dir": str(daily_memory_dir()),
        "sqlite_db": str(sqlite_db_path()),
        "exists": {
            "workspace": workspace_root().exists(),
            "long_memory": long_memory_path().exists(),
            "daily_memory_dir": daily_memory_dir().exists(),
            "sqlite_db": sqlite_db_path().exists(),
        },
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for key in ("openclaw_root", "workspace", "long_memory", "daily_memory_dir", "sqlite_db"):
            print(f"{key}: {report[key]}")
        for key, exists in report["exists"].items():
            print(f"exists.{key}: {'yes' if exists else 'no'}")

    return 0 if any(report["exists"].values()) else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search or append OpenClaw memory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Show detected OpenClaw paths.")
    doctor.add_argument("--json", action="store_true", help="Emit JSON output.")
    doctor.set_defaults(func=command_doctor)

    search = subparsers.add_parser("search", help="Search OpenClaw memory.")
    search.add_argument("--query", required=True, help="Text to search for.")
    search.add_argument("--limit", type=int, default=8, help="Max results to return.")
    search.add_argument("--json", action="store_true", help="Emit JSON output.")
    search.set_defaults(func=command_search)

    recent = subparsers.add_parser("recent", help="List recent markdown memory files.")
    recent.add_argument("--limit", type=int, default=10, help="Max files to list.")
    recent.set_defaults(func=command_recent)

    append = subparsers.add_parser("append", help="Append a note into OpenClaw memory.")
    append.add_argument("--scope", choices=["daily", "long"], required=True, help="Write target.")
    append.add_argument("--text", required=True, help="Text to append.")
    append.add_argument("--date", help="Date for daily notes in YYYY-MM-DD format.")
    append.add_argument("--dry-run", action="store_true", help="Show the target without writing.")
    append.set_defaults(func=command_append)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
