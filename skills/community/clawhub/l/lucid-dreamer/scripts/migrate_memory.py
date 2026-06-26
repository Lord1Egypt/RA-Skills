#!/usr/bin/env python3
"""Lucid memory migration: split MEMORY.md into section files + index manifest.

Usage:
    python3 scripts/migrate_memory.py
    python3 scripts/migrate_memory.py --source path/to/MEMORY.md --output-dir memory/sections/
    python3 scripts/migrate_memory.py --dry-run
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


HEADER_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
SLUG_RE = re.compile(r"[^a-z0-9]+")
DEFAULT_DESCRIPTION = "Migrated from MEMORY.md; refine this description after first review."
DESCRIPTION_HINTS = {
    "identity": "Personal identity, household context, and stable human facts.",
    "infrastructure": "Servers, services, ports, paths, and operational infrastructure facts.",
    "projects": "Active projects, repos, URLs, and current project state.",
    "skills": "Published skills, plugins, and related package metadata.",
    "decisions": "Key decisions, reversals, and rationale worth keeping long-term.",
    "lessons": "Technical lessons learned that should remain easy to reload.",
    "models": "Model choices, agent strategy, providers, and routing notes.",
    "operations": "Operational policy, cron jobs, workflows, and maintenance rules.",
}
ALWAYS_SECTIONS = {"identity", "operations"}


@dataclass
class Section:
    title: str
    slug: str
    body: str


def slugify(title: str) -> str:
    slug = SLUG_RE.sub("-", title.strip().lower()).strip("-")
    return slug or "section"


def extract_sections(text: str) -> list[Section]:
    matches = list(HEADER_RE.finditer(text))
    if not matches:
        raise ValueError("No level-2 (##) section headers found in source file.")

    sections: list[Section] = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip("\n")
        slug = slugify(title)
        sections.append(Section(title=title, slug=slug, body=body))
    return sections


def ensure_unique_slugs(sections: Iterable[Section]) -> list[Section]:
    seen: dict[str, int] = {}
    unique: list[Section] = []
    for section in sections:
        count = seen.get(section.slug, 0)
        if count:
            slug = f"{section.slug}-{count + 1}"
        else:
            slug = section.slug
        seen[section.slug] = count + 1
        unique.append(Section(title=section.title, slug=slug, body=section.body))
    return unique


def section_markdown(section: Section) -> str:
    body = section.body.strip()
    if body:
        return f"# {section.title}\n\n{body}\n"
    return f"# {section.title}\n\n<!-- Empty section created by migrate_memory.py -->\n"


def build_index(sections: list[Section], output_dir: Path, source: Path) -> str:
    today = date.today().isoformat()
    rows = [
        "| Section | File | Description | Last Updated | Default Load |",
        "|---|---|---|---|---|",
    ]
    for section in sections:
        description = DESCRIPTION_HINTS.get(section.slug, DEFAULT_DESCRIPTION)
        default_load = "always" if section.slug in ALWAYS_SECTIONS else "on-demand"
        rows.append(
            f"| {section.title} | sections/{section.slug}.md | {description} | {today} | {default_load} |"
        )

    return "\n".join(
        [
            "# Memory Index",
            "",
            f"Generated from `{source.name}` on {today} by `scripts/migrate_memory.py`.",
            "",
            "Read this file first. Always load `sections/identity.md` and `sections/operations.md`, then load other section files only when the current task needs them.",
            "",
            *rows,
            "",
            "## Maintenance Notes",
            "",
            "- Update `Last Updated` whenever a section file changes.",
            "- Refine section descriptions after migration so agents can route reads accurately.",
            "- Keep file names stable once other prompts start referencing them.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Split MEMORY.md into memory/sections/*.md files.")
    parser.add_argument("--source", default="MEMORY.md", help="Source MEMORY markdown file (default: MEMORY.md)")
    parser.add_argument(
        "--output-dir",
        default="memory/sections/",
        help="Directory for generated section files (default: memory/sections/)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show planned outputs without writing files")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Source file not found: {source}")

    text = source.read_text(encoding="utf-8")
    sections = ensure_unique_slugs(extract_sections(text))
    index_path = output_dir.parent / "index.md"

    if args.dry_run:
        print(f"[dry-run] source: {source}")
        print(f"[dry-run] output directory: {output_dir}")
        for section in sections:
            print(f"[dry-run] would write: {output_dir / f'{section.slug}.md'}")
        print(f"[dry-run] would write: {index_path}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    index_path.parent.mkdir(parents=True, exist_ok=True)

    for section in sections:
        path = output_dir / f"{section.slug}.md"
        path.write_text(section_markdown(section), encoding="utf-8")

    index_path.write_text(build_index(sections, output_dir, source), encoding="utf-8")

    print(f"Wrote {len(sections)} section files to {output_dir}")
    print(f"Wrote manifest to {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
