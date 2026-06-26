#!/usr/bin/env python3
"""Fetch Linux Journey lesson URLs from the public LabEx sitemap."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse


SITEMAP_URL = "https://labex.io/linuxjourney-lessons-sitemap.xml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Linux Journey lessons sitemap and generate a Markdown index."
    )
    parser.add_argument("--url", default=SITEMAP_URL, help="Sitemap URL to fetch.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "references" / "lessons.md",
        help="Path to the generated Markdown file.",
    )
    parser.add_argument(
        "--include-locales",
        action="store_true",
        help="Include locale-specific lesson URLs instead of only canonical lesson URLs.",
    )
    return parser.parse_args()


def fetch_xml(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "CodexSkillBuilder/1.0 (+https://labex.io/linuxjourney-lessons-sitemap.xml)"
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def is_canonical_lesson_url(url: str) -> bool:
    parts = [part for part in urlparse(url).path.split("/") if part]
    return len(parts) == 2 and parts[0] == "lesson"


def extract_lessons(xml_bytes: bytes, include_locales: bool) -> list[tuple[str, str]]:
    root = ET.fromstring(xml_bytes)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    lessons: list[tuple[str, str]] = []
    for loc in root.findall("sm:url/sm:loc", ns):
        url = (loc.text or "").strip()
        if not url:
            continue
        if not include_locales and not is_canonical_lesson_url(url):
            continue
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        title = slug.replace("-", " ").title()
        lessons.append((title, url))
    lessons.sort(key=lambda item: item[0].lower())
    return lessons


def render_markdown(lessons: list[tuple[str, str]], source_url: str) -> str:
    lines = [
        "# Linux Journey Lessons",
        "",
        f"Generated from: {source_url}",
        "",
        f"Total lessons: {len(lessons)}",
        "",
        "Use this index to map Linux topic requests to public Linux Journey lesson URLs.",
        "",
        "## Lessons",
        "",
    ]
    for title, url in lessons:
        lines.append(f"- {title}")
        lines.append(f"  URL: {url}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        xml_bytes = fetch_xml(args.url)
        lessons = extract_lessons(xml_bytes, args.include_locales)
    except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(lessons, args.url), encoding="utf-8")
    print(f"Wrote {len(lessons)} lessons to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
