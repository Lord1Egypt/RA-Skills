#!/usr/bin/env python3
"""
Collect table/collection related query locations from a repository.

Usage:
  python3 collect_table_queries.py --table wallet --repo-root .
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass


FILE_GLOBS = [
    "*.go",
    "*.sql",
    "*.xml",
    "*.yaml",
    "*.yml",
    "*.tmpl",
    "*.tpl",
]


@dataclass(frozen=True)
class Match:
    path: pathlib.Path
    line: int
    text: str


def run_rg(pattern: str, search_roots: list[pathlib.Path]) -> list[Match]:
    cmd = [
        "rg",
        "--no-heading",
        "--line-number",
        "--with-filename",
        "--smart-case",
        "-e",
        pattern,
    ]
    for glob in FILE_GLOBS:
        cmd.extend(["-g", glob])
    cmd.extend(
        [
            "--glob",
            "!.git/**",
            "--glob",
            "!vendor/**",
            "--glob",
            "!logs/**",
        ]
    )
    cmd.extend(str(p) for p in search_roots if p.exists())

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        print("ERROR: `rg` is required but not found in PATH.", file=sys.stderr)
        sys.exit(2)

    if proc.returncode not in (0, 1):
        print(proc.stderr.strip(), file=sys.stderr)
        sys.exit(proc.returncode)

    matches: list[Match] = []
    for raw in proc.stdout.splitlines():
        # Format: /abs/path:line:text
        parts = raw.split(":", 2)
        if len(parts) != 3:
            continue
        file_part, line_part, text_part = parts
        try:
            line_no = int(line_part)
        except ValueError:
            continue
        matches.append(
            Match(
                path=pathlib.Path(file_part).resolve(),
                line=line_no,
                text=text_part.strip(),
            )
        )
    return matches


def dedupe(matches: list[Match]) -> list[Match]:
    seen: set[tuple[str, int, str]] = set()
    out: list[Match] = []
    for item in matches:
        key = (str(item.path), item.line, item.text)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def filter_sql_like(matches: list[Match], table: str) -> list[Match]:
    sql_kw = re.compile(
        rf"(?i)\b(from|join|update|into|delete\s+from|table)\b[^;\n]*\b`?{re.escape(table)}`?\b"
    )
    return [m for m in matches if sql_kw.search(m.text)]


def filter_mongo_like(matches: list[Match], table: str) -> list[Match]:
    mongo_kw = re.compile(
        rf"(?i)(db\.{re.escape(table)}\.(find|findOne|aggregate|update|updateOne|updateMany|deleteOne|deleteMany)"
        rf"|collection\(\"{re.escape(table)}\"\)|collection\('{re.escape(table)}'\)"
        rf"|createIndex\(|dropIndex\(|explain\()"
    )
    return [m for m in matches if mongo_kw.search(m.text)]


def snake_to_camel(table: str) -> str:
    return "".join(x.capitalize() for x in table.split("_") if x)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect query locations for a table/collection with path:line output."
    )
    parser.add_argument("--table", required=True, help="Table/collection name to search")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root path (default: current directory)",
    )
    parser.add_argument(
        "--paths",
        default="apps,pkg,cmd,global,docs/sql",
        help="Comma-separated subdirectories to search under repo-root",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    table = args.table.strip()
    if not table:
        print("ERROR: table/collection name must not be empty", file=sys.stderr)
        sys.exit(2)

    search_roots = [
        (repo_root / p.strip()).resolve()
        for p in args.paths.split(",")
        if p.strip()
    ]
    table_ref_pattern = rf"\b`?{re.escape(table)}`?\b"
    all_mentions = dedupe(run_rg(table_ref_pattern, search_roots))
    sql_like = dedupe(filter_sql_like(all_mentions, table))
    mongo_like = dedupe(filter_mongo_like(all_mentions, table))
    model = snake_to_camel(table)
    orm_pattern = (
        rf"(?i)(GetQuery\(\)|Query\(|repo\.Query|q\.)[^\n]*\.{re.escape(model)}\b"
        rf"|\.{re.escape(model)}\.(WithContext|Where|Select|Order|Limit|Find|First|Take|Update|Updates|Delete)\b"
    )
    orm_like = dedupe(run_rg(orm_pattern, search_roots))

    print(f"# Table/Collection Query Inventory: {table}")
    print(f"Repository: {repo_root}")
    print("")
    print(f"SQL-like matches: {len(sql_like)}")
    print(f"Mongo-like matches: {len(mongo_like)}")
    print(f"ORM-like matches: {len(orm_like)}")
    print(f"All table mentions: {len(all_mentions)}")
    print("")

    print("## SQL-like matches")
    if not sql_like:
        print("- (none)")
    for item in sorted(sql_like, key=lambda x: (str(x.path), x.line)):
        print(f"- {item.path}:{item.line} | {item.text}")

    print("")
    print("## Mongo-like matches")
    if not mongo_like:
        print("- (none)")
    for item in sorted(mongo_like, key=lambda x: (str(x.path), x.line)):
        print(f"- {item.path}:{item.line} | {item.text}")

    print("")
    print("## ORM-like matches")
    if not orm_like:
        print("- (none)")
    for item in sorted(orm_like, key=lambda x: (str(x.path), x.line)):
        print(f"- {item.path}:{item.line} | {item.text}")

    print("")
    print("## Other table mentions")
    if not all_mentions:
        print("- (none)")
    skip_index = {(m.path, m.line, m.text) for m in sql_like}
    skip_index.update((m.path, m.line, m.text) for m in mongo_like)
    skip_index.update((m.path, m.line, m.text) for m in orm_like)
    others = [
        m
        for m in all_mentions
        if (m.path, m.line, m.text) not in skip_index
    ]
    for item in sorted(others, key=lambda x: (str(x.path), x.line)):
        print(f"- {item.path}:{item.line} | {item.text}")


if __name__ == "__main__":
    main()
