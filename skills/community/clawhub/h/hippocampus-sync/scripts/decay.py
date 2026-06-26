#!/usr/bin/env python3
"""Auto-decay stale learnings entries for hippocampus-sync.

Rules:
- pending entries older than 30 days become stale
- stale entries older than 90 days are archived by month and removed from source
- resolved/promoted/in_progress/wont_fix entries are never modified
- print COMPACT warnings for files over 200 lines after processing
"""

from __future__ import annotations

import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import os
import re
from typing import Iterable

TARGET_FILES = (
    "LEARNINGS.md",
    "ERRORS.md",
    "FEATURE_REQUESTS.md",
)
PROTECTED_STATUSES = {"resolved", "promoted", "in_progress", "wont_fix"}
HEADER_RE = re.compile(
    r"(?m)^## \[(?P<id>(?:LRN|ERR|FEAT)-(?P<datestr>\d{8})-\d+)\][^\n]*(?:\n|$)"
)
SEPARATOR_RE = re.compile(r"(?m)^---\s*$")
STATUS_RE = re.compile(
    r"(?im)^(?P<prefix>\s*(?:-\s*)?\*\*Status\*\*:?\s*)(?P<status>[A-Za-z_]+)(?P<suffix>[^\n]*)$"
)


@dataclass
class EntrySpan:
    start: int
    block_end: int
    remove_end: int
    entry_id: str
    entry_date: date | None
    status: str | None
    block_text: str


@dataclass
class ProcessResult:
    new_text: str
    marked_stale: int
    archived_blocks: list[tuple[str, str]]


def atomic_write(path: Path, content: str) -> None:
    """Write content atomically to path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as tmp:
        tmp.write(content)
        temp_name = tmp.name
    os.replace(temp_name, path)


def parse_entry_date(entry_id_date: str) -> date | None:
    try:
        return datetime.strptime(entry_id_date, "%Y%m%d").date()
    except ValueError:
        return None


def find_entry_spans(text: str) -> list[EntrySpan]:
    matches = list(HEADER_RE.finditer(text))
    spans: list[EntrySpan] = []

    for index, match in enumerate(matches):
        next_header_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body_region = text[match.end() : next_header_start]
        separator_match = SEPARATOR_RE.search(body_region)

        if separator_match:
            block_end = match.end() + separator_match.start()
            remove_end = match.end() + separator_match.end()
            trailing_ws = re.match(r"(?:[ \t]*\n)+", text[remove_end:next_header_start])
            if trailing_ws:
                remove_end += trailing_ws.end()
        else:
            block_end = next_header_start
            remove_end = block_end

        block_text = text[match.start() : block_end]
        status_match = STATUS_RE.search(block_text)
        status = status_match.group("status").strip().lower() if status_match else None

        spans.append(
            EntrySpan(
                start=match.start(),
                block_end=block_end,
                remove_end=remove_end,
                entry_id=match.group("id"),
                entry_date=parse_entry_date(match.group("datestr")),
                status=status,
                block_text=block_text,
            )
        )

    return spans


def update_status(block_text: str, new_status: str) -> str:
    return STATUS_RE.sub(rf"\g<prefix>{new_status}\g<suffix>", block_text, count=1)


def append_archive(existing_text: str, blocks: Iterable[str]) -> str:
    cleaned_existing = existing_text.rstrip()
    new_parts = [block.strip() for block in blocks if block.strip()]
    if not new_parts:
        return existing_text
    if not cleaned_existing:
        return "\n\n---\n\n".join(new_parts) + "\n"
    return cleaned_existing + "\n\n---\n\n" + "\n\n---\n\n".join(new_parts) + "\n"


def process_text(text: str, today: date) -> ProcessResult:
    spans = find_entry_spans(text)
    if not spans:
        return ProcessResult(new_text=text, marked_stale=0, archived_blocks=[])

    output_parts: list[str] = []
    cursor = 0
    marked_stale = 0
    archived_blocks: list[tuple[str, str]] = []

    for span in spans:
        output_parts.append(text[cursor : span.start])

        if span.entry_date is None or span.status is None or span.status in PROTECTED_STATUSES:
            output_parts.append(span.block_text)
            cursor = span.block_end
            continue

        age_days = (today - span.entry_date).days

        if span.status == "pending" and age_days > 30:
            output_parts.append(update_status(span.block_text, "stale"))
            cursor = span.block_end
            marked_stale += 1
            continue

        if span.status == "stale" and age_days > 90:
            archived_blocks.append((span.entry_date.strftime("%Y-%m"), span.block_text.strip()))
            cursor = span.remove_end
            continue

        output_parts.append(span.block_text)
        cursor = span.block_end

    output_parts.append(text[cursor:])
    return ProcessResult(
        new_text="".join(output_parts),
        marked_stale=marked_stale,
        archived_blocks=archived_blocks,
    )


def line_count(text: str) -> int:
    if not text:
        return 0
    return len(text.splitlines())


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: decay.py <workspace_path>", file=sys.stderr)
        return 1

    workspace = Path(argv[1]).expanduser().resolve()
    workspace_name = workspace.name or str(workspace)
    learnings_dir = workspace / ".learnings"

    if not learnings_dir.exists() or not learnings_dir.is_dir():
        print(f"DECAY: {workspace_name}: no changes")
        return 0

    today = date.today()
    total_marked_stale = 0
    total_archived = 0
    compaction_warnings: list[str] = []
    source_updates: dict[Path, str] = {}
    archive_blocks_by_month: dict[str, list[str]] = defaultdict(list)

    for filename in TARGET_FILES:
        source_path = learnings_dir / filename
        if not source_path.exists() or not source_path.is_file():
            continue

        original_text = source_path.read_text(encoding="utf-8")
        result = process_text(original_text, today)

        total_marked_stale += result.marked_stale
        total_archived += len(result.archived_blocks)

        if result.new_text != original_text:
            source_updates[source_path] = result.new_text

        for month, block in result.archived_blocks:
            archive_blocks_by_month[month].append(block)

        final_text = source_updates.get(source_path, original_text)
        lines = line_count(final_text)
        if lines > 200:
            compaction_warnings.append(
                f"COMPACT: {filename} has {lines} lines — manual compaction needed"
            )

    if archive_blocks_by_month:
        archive_dir = learnings_dir / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        for month, blocks in sorted(archive_blocks_by_month.items()):
            archive_path = archive_dir / f"{month}.md"
            existing = archive_path.read_text(encoding="utf-8") if archive_path.exists() else ""
            atomic_write(archive_path, append_archive(existing, blocks))

    for source_path, new_text in source_updates.items():
        atomic_write(source_path, new_text)

    for warning in compaction_warnings:
        print(warning)

    if total_marked_stale == 0 and total_archived == 0:
        print(f"DECAY: {workspace_name}: no changes")
    else:
        print(
            f"DECAY: {workspace_name}: {total_marked_stale} marked stale, "
            f"{total_archived} archived, {len(compaction_warnings)} compaction warnings"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
