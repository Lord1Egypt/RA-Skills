#!/usr/bin/env python3
"""Trim core.md when it exceeds the word limit.

Moves oldest/least-relevant sections to archival memory.
"""

import argparse
import re
from pathlib import Path


def count_words(text: str) -> int:
    return len(text.split())


def parse_sections(content: str) -> list[dict]:
    """Parse markdown into sections by header."""
    sections = []
    current_header = None
    current_lines = []

    for line in content.split("\n"):
        header_match = re.match(r"^(#+)\s+(.+)", line)
        if header_match:
            if current_header is not None:
                sections.append({
                    "header": current_header,
                    "lines": current_lines,
                    "words": count_words("\n".join(current_lines)),
                })
            current_header = line
            current_lines = [line]
        else:
            current_lines.append(line)

    # Don't forget the last section
    if current_header is not None:
        sections.append({
            "header": current_header,
            "lines": current_lines,
            "words": count_words("\n".join(current_lines)),
        })

    return sections


def demote_section(section: dict, archival_dir: Path, dry_run: bool) -> str | None:
    """Move a section to archival memory."""
    header_text = section["header"].strip("# ").strip().lower()

    # Map section names to archival categories
    category_map = {
        "active context": "projects",
        "quick reference": "reference",
        "user": "people",
        "identity": "reference",
        "decisions": "decisions",
        "learnings": "learnings",
    }

    category = "reference"
    for key, cat in category_map.items():
        if key in header_text:
            category = cat
            break

    archival_dir.mkdir(parents=True, exist_ok=True)
    filepath = archival_dir / f"demoted-{category}.md"

    content = "\n".join(section["lines"]) + "\n"

    if dry_run:
        return f"[DRY RUN] Would demote '{section['header'].strip()}' to {filepath}"

    if filepath.exists():
        existing = filepath.read_text(encoding="utf-8")
        existing += "\n---\n" + content
        filepath.write_text(existing, encoding="utf-8")
    else:
        filepath.write_text(content, encoding="utf-8")

    return f"Demoted '{section['header'].strip()}' to {filepath}"


def trim_core(workspace: Path, max_words: int, dry_run: bool) -> list[str]:
    """Trim core.md to fit within word limit."""
    core_path = workspace / "memory" / "core.md"
    results = []

    if not core_path.exists():
        results.append("No core.md found. Run initialization first.")
        return results

    content = core_path.read_text(encoding="utf-8")
    word_count = count_words(content)

    results.append(f"Core memory: {word_count} words (limit: {max_words})")

    if word_count <= max_words:
        results.append("Within limit. No trimming needed.")
        return results

    sections = parse_sections(content)
    # Sort by demotion priority: Active Context first, then Quick Reference, then User details
    demotion_order = ["active context", "quick reference", "projects", "decisions"]

    while word_count > max_words and sections:
        # Find the section with highest demotion priority
        best_idx = None
        for priority, keyword in enumerate(demotion_order):
            for i, section in enumerate(sections):
                if keyword in section["header"].lower():
                    if best_idx is None or i > best_idx:
                        best_idx = i
                    break

        if best_idx is None:
            # Demote the last section
            best_idx = len(sections) - 1

        section = sections.pop(best_idx)
        archival_dir = workspace / "memory" / "archival"
        result = demote_section(section, archival_dir, dry_run)
        results.append(result)
        word_count -= section["words"]

    # Rebuild core.md
    if not dry_run:
        new_content = "\n".join(
            line for section in sections for line in section["lines"]
        )
        # Add reference to demoted sections
        new_content += "\n\n<!-- Some sections demoted to archival. Search archival for details. -->\n"
        core_path.write_text(new_content, encoding="utf-8")
        results.append(f"Core memory trimmed to ~{word_count} words")
    else:
        results.append(f"[DRY RUN] Core would be ~{word_count} words after trimming")

    return results


def main():
    parser = argparse.ArgumentParser(description="Trim core.md to word limit")
    parser.add_argument("--max-words", type=int, default=1000, help="Maximum words for core.md")
    parser.add_argument("--workspace", type=str, default=".", help="Workspace root path")
    parser.add_argument("--dry-run", action="store_true", help="Show without writing")

    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()

    results = trim_core(workspace, args.max_words, args.dry_run)
    for r in results:
        print(r)


if __name__ == "__main__":
    main()