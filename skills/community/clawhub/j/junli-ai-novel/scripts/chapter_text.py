#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared chapter text parsing helpers."""

from __future__ import annotations

import re
from pathlib import Path


BODY_HEADING_RE = re.compile(r"^\s*##\s*正文\s*$")
NOTES_HEADING_RE = re.compile(r"^\s*##\s*章节备注\s*$")
CHAPTER_TITLE_RE = re.compile(r"^\s*#{1,6}\s*第.+章(?:[:：\s].*)?$")
SEPARATOR_RE = re.compile(r"^\s*---\s*$")


def is_chapter_file(path: Path) -> bool:
    name = path.name
    return bool(re.match(r"^\d{3}[_-].+\.md$", name)) or ("第" in name and "章" in name and name.endswith(".md"))


def extract_body_section(content: str) -> str:
    """Support both legacy markdown-section chapters and pure-body chapters."""
    lines = content.splitlines()
    body_start = 0

    for index, line in enumerate(lines):
        if BODY_HEADING_RE.match(line):
            body_start = index + 1
            break

    body_end = len(lines)
    for index in range(body_start, len(lines)):
        if NOTES_HEADING_RE.match(lines[index]):
            body_end = index
            break

    body_lines = lines[body_start:body_end]

    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    while body_lines and not body_lines[-1].strip():
        body_lines.pop()

    while body_lines and SEPARATOR_RE.match(body_lines[0]):
        body_lines.pop(0)
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
    while body_lines and SEPARATOR_RE.match(body_lines[-1]):
        body_lines.pop()
        while body_lines and not body_lines[-1].strip():
            body_lines.pop()

    if body_start == 0 and body_lines and CHAPTER_TITLE_RE.match(body_lines[0]):
        body_lines.pop(0)
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)

    return "\n".join(body_lines).strip()


def extract_content_from_chapter(file_path: Path) -> str:
    """Extract the body content while ignoring optional markdown wrappers."""
    content = file_path.read_text(encoding="utf-8")
    return extract_body_section(content)
