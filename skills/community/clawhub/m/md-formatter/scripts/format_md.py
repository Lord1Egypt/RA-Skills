#!/usr/bin/env python3
"""Format a markdown file with consistent conventions."""

import sys
import re
from pathlib import Path


def fix_headings(text):
    """Fix heading levels: ensure no skips, convert setext to atx."""
    lines = text.split("\n")
    result = []
    current_level = 0

    for i, line in enumerate(lines):
        # Convert setext headings
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            if not line.startswith("#") and line.strip():
                if re.match(r"^={3,}\s*$", next_line):
                    result.append(f"# {line.strip()}")
                    current_level = 1
                    continue
                elif re.match(r"^-{3,}\s*$", next_line):
                    result.append(f"## {line.strip()}")
                    current_level = 2
                    continue

        if not line.startswith("#") and current_level > 0:
            result.append(f"\n{line}\n" if i < len(lines) - 1 else line)
            continue

        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            if level > current_level + 1:
                line = "#" * (current_level + 1) + line[level:]
            current_level = level

        result.append(line)

    return "\n".join(result)


def fix_emphasis(text):
    """Prefer **bold** over __bold__, *italic* over _italic_."""
    text = re.sub(r"\*\*(.+?)\*\*", r"**\1**", text)  # already atx bold
    text = re.sub(r"__(.+?)__", r"**\1**", text)
    text = re.sub(r"_(.+?)_", r"*\1*", text)
    return text


def fix_trailing_whitespace(text):
    return re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)


def fix_blank_lines(text):
    """Ensure blank line before and after headings and code fences."""
    text = re.sub(r"(\S)\n(#{1,6} )", r"\1\n\n\2", text)
    text = re.sub(r"(#{1,6} .+?\n)([^\n#])", r"\1\n\2", text)
    return text


def main():
    if len(sys.argv) < 2:
        print("Usage: format_md.py <file.md>")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    original = text

    text = fix_emphasis(text)
    text = fix_headings(text)
    text = fix_trailing_whitespace(text)
    text = fix_blank_lines(text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"Formatted: {path}")
    else:
        print(f"No changes needed: {path}")


if __name__ == "__main__":
    main()