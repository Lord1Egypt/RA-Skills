#!/usr/bin/env python3
"""Audit deterministic structure, provenance, navigation, and freshness rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path


MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
WIKI_LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
REQUIRED_PATHS = ("WIKI.md", "wiki/index.md", "raw", "audit/open", "audit/resolved", "outputs/queries", "log", ".wiki")
REQUIRED_FIELDS = ("id", "type", "title", "status", "updated", "owner", "sources")
ALLOWED_TYPES = {"concept", "entity", "source-summary", "how-to", "reference", "explanation", "decision", "archive"}
ALLOWED_STATUSES = {"draft", "active", "disputed", "stale", "deprecated"}


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description="Audit an LLM Wiki and report stable issue codes.")
    cli.add_argument("root", type=Path, help="Wiki root directory")
    cli.add_argument("--max-age-days", type=int, default=180, help="Warn when active pages exceed this age")
    cli.add_argument("--json", action="store_true", help="Emit a JSON report")
    cli.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors")
    return cli


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, text
    data: dict[str, object] = {}
    active_list: str | None = None
    for raw in lines[1:end]:
        if re.match(r"^\s+-\s+", raw) and active_list:
            value = re.sub(r"^\s+-\s+", "", raw).strip().strip('"\'')
            assert isinstance(data[active_list], list)
            data[active_list].append(value)
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not match:
            active_list = None
            continue
        key, value = match.groups()
        if not value:
            data[key] = []
            active_list = key
        else:
            data[key] = value.strip().strip('"\'')
            active_list = None
    return data, "\n".join(lines[end + 1 :])


def inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def add(issues: list[dict[str, str]], severity: str, code: str, path: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "path": path, "message": message})


def resolve_link(source: Path, target: str, wiki_root: Path) -> Path | None:
    target = target.split("#", 1)[0].strip()
    if not target or re.match(r"^[a-z]+://|^mailto:|^#", target, re.I):
        return None
    if target.startswith("/"):
        return Path(target)
    candidate = (source.parent / target).resolve()
    if candidate.exists() or target.endswith(".md"):
        return candidate
    wiki_candidate = (wiki_root / target).with_suffix(".md").resolve()
    return wiki_candidate


def main() -> int:
    args = parser().parse_args()
    if args.max_age_days < 0:
        parser().error("--max-age-days must be non-negative")
    root = args.root.expanduser().resolve()
    wiki = root / "wiki"
    issues: list[dict[str, str]] = []
    for relative in REQUIRED_PATHS:
        if not (root / relative).exists():
            add(issues, "error", "REQUIRED_PATH_MISSING", relative, "required Wiki path is missing")

    pages = [] if not wiki.is_dir() else [path for path in sorted(wiki.rglob("*.md")) if path != wiki / "index.md"]
    index_text = (wiki / "index.md").read_text(encoding="utf-8") if (wiki / "index.md").is_file() else ""
    ids: dict[str, str] = {}
    inbound: dict[Path, int] = {path.resolve(): 0 for path in pages}

    link_sources = ([wiki / "index.md"] if (wiki / "index.md").is_file() else []) + pages
    for path in link_sources:
        text = path.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(text) if path != wiki / "index.md" else ({}, text)
        relative = path.relative_to(root).as_posix()

        if path != wiki / "index.md":
            missing = [field for field in REQUIRED_FIELDS if not metadata.get(field)]
            if missing:
                add(issues, "error", "FRONTMATTER_REQUIRED", relative, "missing: " + ", ".join(missing))
            page_id = str(metadata.get("id", ""))
            if page_id:
                if page_id in ids:
                    add(issues, "error", "DUPLICATE_ID", relative, f"{page_id} already used by {ids[page_id]}")
                else:
                    ids[page_id] = relative
            page_type = str(metadata.get("type", ""))
            status = str(metadata.get("status", ""))
            if page_type and page_type not in ALLOWED_TYPES:
                add(issues, "error", "TYPE_INVALID", relative, f"unsupported type: {page_type}")
            if status and status not in ALLOWED_STATUSES:
                add(issues, "error", "STATUS_INVALID", relative, f"unsupported status: {status}")
            updated = str(metadata.get("updated", ""))
            if updated:
                try:
                    changed = date.fromisoformat(updated)
                    age = (date.today() - changed).days
                    if age < 0:
                        add(issues, "error", "UPDATED_IN_FUTURE", relative, f"updated date is {abs(age)} days in the future")
                    elif status == "active" and age > args.max_age_days:
                        add(issues, "warning", "PAGE_STALE", relative, f"active page is {age} days old")
                except ValueError:
                    add(issues, "error", "UPDATED_INVALID", relative, "updated must be YYYY-MM-DD")
            page_from_wiki = path.relative_to(wiki).as_posix()
            if page_from_wiki not in index_text:
                add(issues, "warning", "INDEX_MISSING_PAGE", relative, "page is not linked from wiki/index.md")

            sources = metadata.get("sources", [])
            if isinstance(sources, str):
                sources = [sources]
            for source in sources if isinstance(sources, list) else []:
                source_path = (path.parent / str(source)).resolve()
                if not inside(source_path, root):
                    add(issues, "error", "SOURCE_PATH_ESCAPE", relative, f"source escapes Wiki root: {source}")
                elif not source_path.is_file():
                    add(issues, "error", "SOURCE_MISSING", relative, f"source does not exist: {source}")
                elif not inside(source_path, root / "raw"):
                    add(issues, "warning", "SOURCE_OUTSIDE_RAW", relative, f"source is not under raw/: {source}")

        targets = list(MARKDOWN_LINK.findall(body)) + list(WIKI_LINK.findall(body))
        for target in targets:
            resolved = resolve_link(path, target, wiki)
            if resolved is None:
                continue
            if not inside(resolved, root):
                add(issues, "error", "LINK_PATH_ESCAPE", relative, f"link escapes Wiki root: {target}")
            elif not resolved.is_file():
                add(issues, "error", "LINK_BROKEN", relative, f"link target does not exist: {target}")
            elif resolved in inbound:
                inbound[resolved] += 1

    for path, count in inbound.items():
        if count == 0:
            add(issues, "warning", "ORPHAN_PAGE", path.relative_to(root).as_posix(), "page has no inbound Wiki link")

    errors = sum(issue["severity"] == "error" for issue in issues)
    warnings = sum(issue["severity"] == "warning" for issue in issues)
    failed = errors > 0 or (args.strict and warnings > 0)
    report = {
        "ok": not failed,
        "root": str(root),
        "checked_at": datetime.now().astimezone().isoformat(),
        "page_count": len(pages),
        "errors": errors,
        "warnings": warnings,
        "strict": args.strict,
        "issues": issues,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Audit: {len(pages)} pages, {errors} errors, {warnings} warnings")
        for issue in issues:
            print(f"{issue['severity'].upper()} {issue['code']} {issue['path']}: {issue['message']}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
