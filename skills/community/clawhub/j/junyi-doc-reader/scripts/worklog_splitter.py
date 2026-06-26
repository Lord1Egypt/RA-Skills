#!/usr/bin/env python3
"""worklog_splitter.py — Split worklog Markdown by date into daily notes.

Part of junyi-doc-reader v5. Splits Feishu worklogs into per-date daily notes
with idempotent managed-block writing.

Usage:
    python3 worklog_splitter.py <input.md> --output /output/ [--dry-run]
"""

import re
import os
import sys
import json
import argparse
import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MANAGED_START = "<!-- doc-reader:start -->"
MANAGED_END = "<!-- doc-reader:end -->"

# Date patterns ---------------------------------------------------------------
# Group layout (always): year, month, day
# For patterns without year, year group will be None.

# 2024年3月1日 / 2024年03月01日
_RE_CN_FULL = r"(?P<y1>\d{4})\s*年\s*(?P<m1>\d{1,2})\s*月\s*(?P<d1>\d{1,2})\s*日"
# 3月1日 (no year)
_RE_CN_SHORT = r"(?P<m2>\d{1,2})\s*月\s*(?P<d2>\d{1,2})\s*日"
# 2024-03-01
_RE_ISO_DASH = r"(?P<y3>\d{4})-(?P<m3>\d{1,2})-(?P<d3>\d{1,2})"
# 2024/03/01
_RE_ISO_SLASH = r"(?P<y4>\d{4})/(?P<m4>\d{1,2})/(?P<d4>\d{1,2})"

# Combined — order matters: full CN before short CN, dash before slash
_DATE_RE = re.compile(
    "|".join([_RE_CN_FULL, _RE_ISO_DASH, _RE_ISO_SLASH, _RE_CN_SHORT])
)

# A line that starts a new section: heading or paragraph start with a date
_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s")


def _extract_date(match, default_year=None):
    """Extract (date_str, raw_match_text) from a regex match.

    Returns (iso_date_str, original_text) or (None, None) on failure.
    ``default_year`` is used when the pattern has no year (e.g. "3月1日").
    """
    g = match.groupdict()

    # Determine which alternative matched
    if g.get("y1") is not None:
        y, m, d = int(g["y1"]), int(g["m1"]), int(g["d1"])
    elif g.get("y3") is not None:
        y, m, d = int(g["y3"]), int(g["m3"]), int(g["d3"])
    elif g.get("y4") is not None:
        y, m, d = int(g["y4"]), int(g["m4"]), int(g["d4"])
    elif g.get("m2") is not None:
        y = default_year or datetime.date.today().year
        m, d = int(g["m2"]), int(g["d2"])
    else:
        return None, None

    try:
        dt = datetime.date(y, m, d)
    except ValueError:
        return None, None

    return dt.isoformat(), match.group(0)


def _is_section_start(line):
    """Check if a line qualifies as a section-start position.

    A line qualifies if:
    - It is a Markdown heading (# / ## / …), OR
    - The date appears at the very beginning of the line (paragraph start).
    """
    stripped = line.lstrip()
    # Heading line
    if _HEADING_RE.match(line):
        return True
    # Date at paragraph start — the date match must start within the first
    # few chars (allow up to 3 leading spaces, which lstrip already removed
    # for headings check; here we check the original line).
    m = _DATE_RE.search(line)
    if m and m.start() <= 3:
        return True
    return False


def _derive_title(line, date_raw):
    """Derive a human-readable title from the heading/line."""
    title = line.strip().lstrip("#").strip()
    if not title:
        title = date_raw
    return title


# ---------------------------------------------------------------------------
# Core: split_by_date
# ---------------------------------------------------------------------------

def split_by_date(text, default_year=None):
    """Split normalised Markdown *text* into per-date sections.

    Returns dict with keys: sections, unmatched_blocks, confidence.
    """
    lines = text.split("\n")

    # --- Pass 1: identify split points ----------------------------------------
    # A split point is a line that:
    #   1. Contains a date match, AND
    #   2. Is a heading or has the date at line-start (paragraph start).
    split_points = []  # list of (line_idx, iso_date, title)

    for idx, line in enumerate(lines):
        if not _is_section_start(line):
            continue
        m = _DATE_RE.search(line)
        if not m:
            continue
        # Extra guard: date must appear close to line start (within first 80
        # chars) to avoid mid-paragraph references on very long "heading" lines.
        if m.start() > 80:
            continue
        iso_date, raw = _extract_date(m, default_year=default_year)
        if iso_date is None:
            continue
        title = _derive_title(line, raw)
        split_points.append((idx, iso_date, title))

    # --- Pass 2: slice content between split points ---------------------------
    sections = []
    unmatched_lines = []

    if not split_points:
        # Nothing matched
        unmatched_lines = lines
    else:
        # Lines before first split point → unmatched
        if split_points[0][0] > 0:
            unmatched_lines = lines[: split_points[0][0]]

        for i, (start_idx, iso_date, title) in enumerate(split_points):
            end_idx = split_points[i + 1][0] if i + 1 < len(split_points) else len(lines)
            content = "\n".join(lines[start_idx:end_idx]).strip()
            sections.append({
                "date": iso_date,
                "title": title,
                "content": content,
            })

    # Build unmatched_blocks (non-empty text chunks)
    unmatched_text = "\n".join(unmatched_lines).strip()
    unmatched_blocks = [b.strip() for b in unmatched_text.split("\n\n") if b.strip()] if unmatched_text else []

    # --- Confidence -----------------------------------------------------------
    total_chars = sum(len(l) for l in lines if l.strip())
    if total_chars == 0:
        confidence = 0.0
    else:
        matched_chars = sum(len(l) for s in sections for l in s["content"].split("\n") if l.strip())
        confidence = round(matched_chars / total_chars, 4)

    # If confidence too low, clear sections
    if confidence < 0.5:
        sections = []

    return {
        "sections": sections,
        "unmatched_blocks": unmatched_blocks,
        "confidence": confidence,
    }


# ---------------------------------------------------------------------------
# Core: write_daily_notes
# ---------------------------------------------------------------------------

def write_daily_notes(sections, output_dir, dry_run=False):
    """Write each section to ``output_dir/<date>.md`` with managed blocks.

    Returns list of written file paths.
    """
    written = []

    if not dry_run:
        os.makedirs(output_dir, exist_ok=True)

    for sec in sections:
        fname = sec["date"] + ".md"
        fpath = os.path.join(output_dir, fname)
        managed_block = f"{MANAGED_START}\n{sec['content']}\n{MANAGED_END}"

        if os.path.exists(fpath):
            existing = _read_file(fpath)
            if MANAGED_START in existing and MANAGED_END in existing:
                # Replace managed block
                new_content = _replace_managed_block(existing, sec["content"])
                action = "replace"
            else:
                # Append managed block
                new_content = existing.rstrip("\n") + "\n\n" + managed_block + "\n"
                action = "append"
        else:
            new_content = f"# {sec['date']}\n\n{managed_block}\n"
            action = "create"

        if dry_run:
            print(f"[dry-run] {action}: {fpath}")
        else:
            _write_file(fpath, new_content)
            print(f"[write] {action}: {fpath}")

        written.append(fpath)

    return written


def _replace_managed_block(text, new_content):
    """Replace content between MANAGED_START and MANAGED_END markers."""
    start_idx = text.index(MANAGED_START)
    end_idx = text.index(MANAGED_END) + len(MANAGED_END)
    replacement = f"{MANAGED_START}\n{new_content}\n{MANAGED_END}"
    return text[:start_idx] + replacement + text[end_idx:]


# ---------------------------------------------------------------------------
# Core: generate_index
# ---------------------------------------------------------------------------

def generate_index(sections, output_dir):
    """Generate ``_daily_index.md`` in *output_dir*.

    Returns the index file path.
    """
    os.makedirs(output_dir, exist_ok=True)

    rows = []
    for sec in sorted(sections, key=lambda s: s["date"]):
        char_count = len(sec["content"])
        rows.append(f"| [[{sec['date']}]] | {sec['title']} | {char_count:,} |")

    table = "\n".join(rows)
    content = (
        "# Daily Notes Index\n\n"
        "| 日期 | 标题 | 字数 |\n"
        "|------|------|------|\n"
        f"{table}\n\n"
        "*Generated by doc-reader*\n"
    )

    fpath = os.path.join(output_dir, "_daily_index.md")
    _write_file(fpath, content)
    return fpath


# ---------------------------------------------------------------------------
# Main entry: split_and_write
# ---------------------------------------------------------------------------

def split_and_write(md_path, output_dir, dry_run=False):
    """Read *md_path*, split by date, write daily notes + index.

    Returns a summary dict.
    """
    text = _read_file(md_path)
    result = split_by_date(text)

    if result["confidence"] < 0.5:
        reason = (
            f"Low confidence ({result['confidence']:.2f} < 0.50): "
            "date structure not reliable enough for splitting"
        )
        print(f"[fallback] {reason}")
        return {
            "sections": 0,
            "files": [],
            "unmatched_blocks": len(result["unmatched_blocks"]),
            "confidence": result["confidence"],
            "fallback_reason": reason,
            "index_file": None,
        }

    files = write_daily_notes(result["sections"], output_dir, dry_run=dry_run)
    index_file = None
    if not dry_run:
        index_file = generate_index(result["sections"], output_dir)

    return {
        "sections": len(result["sections"]),
        "files": [os.path.basename(f) for f in files],
        "unmatched_blocks": len(result["unmatched_blocks"]),
        "confidence": result["confidence"],
        "fallback_reason": None,
        "index_file": os.path.basename(index_file) if index_file else None,
    }


# ---------------------------------------------------------------------------
# File I/O helpers
# ---------------------------------------------------------------------------

def _read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Split worklog Markdown by date into daily notes."
    )
    parser.add_argument("input", help="Path to normalised Markdown file")
    parser.add_argument("--output", required=True, help="Output directory for daily notes")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    result = split_and_write(args.input, args.output, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
