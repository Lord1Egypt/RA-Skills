#!/usr/bin/env python3
"""Consolidate daily memory notes into archival entries.

Reads memory/YYYY-MM-DD.md files, extracts notable items, and writes
structured archival entries under memory/archival/.
"""

import argparse
import os
import re
from datetime import datetime, timedelta
from pathlib import Path


def read_daily_notes(workspace: Path, days: int) -> list[dict]:
    """Read daily notes from the last N days."""
    notes = []
    memory_dir = workspace / "memory"
    if not memory_dir.exists():
        return notes

    today = datetime.now().date()
    for i in range(days):
        date = today - timedelta(days=i)
        filename = f"{date.isoformat()}.md"
        filepath = memory_dir / filename
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
            notes.append({"date": date, "file": filepath, "content": content})

    return notes


def extract_items(content: str) -> list[dict]:
    """Extract notable items from a daily note."""
    items = []
    lines = content.split("\n")
    current_header = "general"

    for line in lines:
        # Track headers as categories
        header_match = re.match(r"^#+\s+(.+)", line)
        if header_match:
            current_header = header_match.group(1).strip().lower()
            continue

        # Look for decision-like patterns
        if re.search(r"(decid[ió]|decisi[ó]n|acordamos|agregamos|cambiamos|resolvimos)", line, re.IGNORECASE):
            items.append({"category": "decisions", "text": line.strip()})

        # Look for learning-like patterns
        if re.search(r"(aprend[í]|lecci[ó]n| lesson|descubr[í]|error|fall[ó]|corregir)", line, re.IGNORECASE):
            items.append({"category": "learnings", "text": line.strip()})

        # Look for project-related patterns
        if re.search(r"(proyecto|project|loCatering|Pezu[ñ]o|bot|vps|openclaw)", line, re.IGNORECASE):
            items.append({"category": "projects", "text": line.strip()})

        # Look for person-related patterns
        if re.search(r"(florentina|fernanda|ximena|francisca|renate)", line, re.IGNORECASE):
            items.append({"category": "people", "text": line.strip()})

    return items


def write_archival_entry(workspace: Path, category: str, date_str: str, items: list[str]) -> Path | None:
    """Write an archival entry. Returns path to file written, or None."""
    archival_dir = workspace / "memory" / "archival" / category
    archival_dir.mkdir(parents=True, exist_ok=True)

    filepath = archival_dir / f"{date_str}.md"

    if not items:
        return None

    content = f"# {category.title()} — {date_str}\n\n"
    for item in items:
        content += f"- {item}\n"
    content += f"\n## Tags\n{category}, {date_str}\n"

    if filepath.exists():
        existing = filepath.read_text(encoding="utf-8")
        # Append new items that aren't already there
        new_items = [i for i in items if i not in existing]
        if not new_items:
            return None
        existing += f"\n# Added {date_str}\n\n"
        for item in new_items:
            existing += f"- {item}\n"
        filepath.write_text(existing, encoding="utf-8")
    else:
        filepath.write_text(content, encoding="utf-8")

    return filepath


def consolidate(workspace: Path, days: int, dry_run: bool = False) -> list[str]:
    """Main consolidation logic."""
    notes = read_daily_notes(workspace, days)
    results = []

    if not notes:
        results.append("No daily notes found in the last {} days.".format(days))
        return results

    # Collect items by category and date
    all_items: dict[str, dict[str, list[str]]] = {}

    for note in notes:
        date_str = note["date"].isoformat()
        items = extract_items(note["content"])

        for item in items:
            cat = item["category"]
            if cat not in all_items:
                all_items[cat] = {}
            if date_str not in all_items[cat]:
                all_items[cat][date_str] = []
            all_items[cat][date_str].append(item["text"])

    # Write archival entries
    for category, dates in sorted(all_items.items()):
        for date_str, items in sorted(dates.items()):
            if dry_run:
                results.append(f"[DRY RUN] Would write {category}/{date_str}.md with {len(items)} items:")
                for item in items:
                    results.append(f"  - {item}")
            else:
                path = write_archival_entry(workspace, category, date_str, items)
                if path:
                    results.append(f"Wrote {path} ({len(items)} items)")
                else:
                    results.append(f"No new items for {category}/{date_str}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Consolidate daily notes into archival memory")
    parser.add_argument("--days", type=int, default=7, help="Look back N days")
    parser.add_argument("--workspace", type=str, default=".", help="Workspace root path")
    parser.add_argument("--dry-run", action="store_true", help="Show without writing")

    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()

    results = consolidate(workspace, args.days, args.dry_run)
    for r in results:
        print(r)


if __name__ == "__main__":
    main()