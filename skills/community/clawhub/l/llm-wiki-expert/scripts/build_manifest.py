#!/usr/bin/env python3
"""Build a deterministic manifest for LLM Wiki pages and their relationships."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
WIKI_LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
REQUIRED = ("id", "type", "title", "status", "updated", "owner", "sources")


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description="Build .wiki/manifest.json from Wiki Markdown pages.")
    cli.add_argument("root", type=Path, help="Wiki root directory")
    cli.add_argument("--output", type=Path, help="Output path; defaults to ROOT/.wiki/manifest.json")
    cli.add_argument("--json", action="store_true", help="Emit the report as JSON")
    cli.add_argument("--strict", action="store_true", help="Fail on malformed or duplicate pages")
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


def local_links(body: str) -> list[str]:
    links = []
    for target in MARKDOWN_LINK.findall(body):
        target = target.split("#", 1)[0].strip()
        if target and not re.match(r"^[a-z]+://|^mailto:|^#", target, re.I):
            links.append(target)
    links.extend(f"{target}.md" if not target.endswith(".md") else target for target in WIKI_LINK.findall(body))
    return sorted(set(links))


def main() -> int:
    args = parser().parse_args()
    root = args.root.expanduser().resolve()
    wiki = root / "wiki"
    output = (args.output.expanduser() if args.output else root / ".wiki/manifest.json").resolve()
    pages: list[dict[str, object]] = []
    issues: list[dict[str, str]] = []
    seen: dict[str, str] = {}

    if not wiki.is_dir():
        issues.append({"code": "WIKI_DIR_MISSING", "path": str(wiki), "message": "wiki/ directory is missing"})
    else:
        for path in sorted(wiki.rglob("*.md")):
            if path == wiki / "index.md":
                continue
            metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            relative = path.relative_to(root).as_posix()
            missing = [field for field in REQUIRED if not metadata.get(field)]
            if missing:
                issues.append({
                    "code": "FRONTMATTER_REQUIRED",
                    "path": relative,
                    "message": "missing: " + ", ".join(missing),
                })
            page_id = str(metadata.get("id", ""))
            if page_id:
                if page_id in seen:
                    issues.append({
                        "code": "DUPLICATE_ID",
                        "path": relative,
                        "message": f"{page_id} already used by {seen[page_id]}",
                    })
                else:
                    seen[page_id] = relative
            sources = metadata.get("sources", [])
            if isinstance(sources, str):
                sources = [sources]
            pages.append({
                "id": page_id,
                "path": relative,
                "type": metadata.get("type", ""),
                "title": metadata.get("title", ""),
                "status": metadata.get("status", ""),
                "updated": metadata.get("updated", ""),
                "owner": metadata.get("owner", ""),
                "sources": sources,
                "links": local_links(body),
            })

    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "page_count": len(pages),
        "pages": pages,
        "issues": issues,
    }
    if not issues or not args.strict:
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_suffix(output.suffix + ".tmp")
        temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(output)

    report = {
        "ok": not issues,
        "root": str(root),
        "output": str(output),
        "page_count": len(pages),
        "issues": issues,
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Manifest: {len(pages)} pages, {len(issues)} issues -> {output}")
        for issue in issues:
            print(f"{issue['code']} {issue['path']}: {issue['message']}", file=sys.stderr)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
