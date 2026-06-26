#!/usr/bin/env python3
import argparse
from pathlib import Path

SCHEMA_MD = """# Schema

## Purpose
This vault stores compiled knowledge derived from raw sources.

## Directory conventions
- `raw/`: immutable or lightly normalized source material
- `wiki/`: maintained knowledge pages
- `logs/`: maintenance history

## Page naming
- Prefer clear noun phrases
- Reuse existing canonical names when possible
- Avoid duplicate pages that differ only by wording

## Required sections for concept pages
- Summary
- Key points
- Relationships
- Sources
- Open questions

## Linking
- Prefer `[[Wiki Links]]` between pages
- Add at least one related link for non-leaf pages

## Maintenance rules
- Update existing pages before creating duplicates
- Log meaningful structural changes in `logs/knowledge-log.md`
- Mark uncertainty explicitly
"""

INDEX_MD = """# Knowledge Index

## Hubs
- [[Projects]]
- [[People]]
- [[Concepts]]
- [[Timeline]]
- [[Sources]]

## Active topics
- Add active topic pages here

## Recently updated
- Add recently updated pages here
"""

KNOWLEDGE_LOG_MD = """# Knowledge Log

## {date}
- Initialized knowledge vault scaffold.
- Review `SCHEMA.md` and adapt conventions before large ingests.
"""

HUB_PAGES = {
    "wiki/projects/Projects.md": "# Projects\n\n- Add project pages here\n",
    "wiki/people/People.md": "# People\n\n- Add people pages here\n",
    "wiki/concepts/Concepts.md": "# Concepts\n\n- Add concept pages here\n",
    "wiki/timelines/Timeline.md": "# Timeline\n\n- Add timeline pages here\n",
    "wiki/sources/Sources.md": "# Sources\n\n- Add source pages here\n",
}

README_MD = """# LLM Wiki Vault

This vault is designed for an agent-maintained Markdown wiki.

## Layout
- `raw/`: source material
- `wiki/`: compiled knowledge pages
- `logs/`: maintenance history
- `INDEX.md`: navigation
- `SCHEMA.md`: conventions

## Suggested workflows
1. Drop or copy new source material into `raw/`.
2. Ask the agent to ingest the new material into `wiki/`.
3. Ask questions against the compiled wiki first.
4. Periodically reindex and lint the vault.
"""


def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return f"skip {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"write {path}"


def main():
    parser = argparse.ArgumentParser(description="Initialize an LLM wiki vault scaffold")
    parser.add_argument("target", help="Target directory for the wiki vault")
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffold files")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    dirs = [
        "raw/inbox",
        "raw/docs",
        "raw/transcripts",
        "raw/web",
        "wiki/concepts",
        "wiki/people",
        "wiki/projects",
        "wiki/timelines",
        "wiki/sources",
        "logs",
    ]

    actions = []
    for d in dirs:
        p = target / d
        p.mkdir(parents=True, exist_ok=True)
        actions.append(f"mkdir {p}")

    actions.append(write_file(target / "SCHEMA.md", SCHEMA_MD, args.force))
    actions.append(write_file(target / "INDEX.md", INDEX_MD, args.force))
    actions.append(write_file(target / "README.md", README_MD, args.force))

    from datetime import datetime
    actions.append(write_file(target / "logs/knowledge-log.md", KNOWLEDGE_LOG_MD.format(date=datetime.now().date().isoformat()), args.force))

    for rel, content in HUB_PAGES.items():
        actions.append(write_file(target / rel, content, args.force))

    print(f"Initialized wiki scaffold at: {target}")
    for a in actions:
        print(a)


if __name__ == "__main__":
    main()
