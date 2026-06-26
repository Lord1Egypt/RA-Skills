#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from _common import dump_frontmatter, now_date, now_id, read_text, slugify, write_text


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    default_template = here.parent / "references" / "note-template-base.md"

    p = argparse.ArgumentParser(
        description="Create an Obsidian-compatible reading note scaffold from the base template."
    )
    p.add_argument("--template", default=str(default_template), help="Path to note-template-base.md")
    p.add_argument("--title", default="", help="Paper title")
    p.add_argument("--source", default="", help="Source identifier, PDF path, citation key, or note source")
    p.add_argument("--authors", default="", help="Semicolon-separated or comma-separated authors")
    p.add_argument("--year", default="", help="Publication year")
    p.add_argument("--venue", default="", help="Venue, journal, conference, or status")
    p.add_argument("--status", default="", help="published / preprint / working paper / etc.")
    p.add_argument("--doi", default="", help="DOI")
    p.add_argument("--url", default="", help="URL")
    p.add_argument("--fields", nargs="*", default=None, help="Frontmatter fields list")
    p.add_argument("--tags", nargs="*", default=None, help="Frontmatter tags list")
    p.add_argument("--id", dest="note_id", default=now_id(), help="Frontmatter id")
    p.add_argument("--created", default=now_date(), help="Creation date YYYY-MM-DD")
    p.add_argument("--updated", default=now_date(), help="Updated date YYYY-MM-DD")
    p.add_argument(
        "--output",
        default="",
        help="Output markdown path. Defaults to <slug(title)>-reading-note.md in the current directory.",
    )
    return p.parse_args()


def split_authors(raw: str) -> str:
    if not raw.strip():
        return ""
    return ", ".join([x.strip() for x in raw.replace(";", ",").split(",") if x.strip()])


def replace_first(text: str, old: str, new: str) -> str:
    return text.replace(old, new, 1)


def main() -> None:
    args = parse_args()
    template = read_text(args.template)

    frontmatter = {
        "id": args.note_id,
        "created": args.created,
        "updated": args.updated,
        "source": args.source,
        "title": args.title,
        "authors": split_authors(args.authors),
        "year": args.year,
        "venue": args.venue,
        "status": args.status,
        "doi": args.doi,
        "url": args.url,
        "fields": args.fields or [],
        "tags": args.tags or ["reading-note"],
    }

    body = template
    if body.startswith("---\n"):
        end = body.find("\n---\n", 4)
        if end != -1:
            body = body[end + 5 :]

    title_line = f"# {args.title}" if args.title else "# Untitled Paper"
    body = replace_first(body, "# {{title}}", title_line)

    replacements = {
        "- **Authors:** ": f"- **Authors:** {split_authors(args.authors)}",
        "- **Venue / status:** ": f"- **Venue / status:** {args.venue or args.status}",
        "- **Year:** ": f"- **Year:** {args.year}",
        "- **Source / link:** ": f"- **Source / link:** {args.url or args.source}",
    }
    for old, new in replacements.items():
        body = replace_first(body, old, new)

    final_md = dump_frontmatter(frontmatter) + "\n\n" + body.lstrip("\n")

    output = args.output or f"{slugify(args.title or 'untitled-paper')}-reading-note.md"
    write_text(output, final_md)
    print(output)


if __name__ == "__main__":
    main()
