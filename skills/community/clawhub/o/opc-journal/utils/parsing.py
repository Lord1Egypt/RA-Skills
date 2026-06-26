"""Entry parsing utilities shared across commands."""
import re
from typing import List, Dict, Any, Optional


ENTRY_SEPARATOR = "\n\n---\ntype: entry"


def split_entries(content: str) -> List[str]:
    """Split memory file content into individual blocks.

    Returns blocks as-is, preserving frontmatter separators.
    """
    if ENTRY_SEPARATOR not in content:
        # Single block or no entries
        stripped = content.strip()
        return [stripped] if stripped else []

    parts = content.split(ENTRY_SEPARATOR)
    blocks = []
    for idx, part in enumerate(parts):
        stripped = part.strip()
        if not stripped:
            continue
        if idx > 0:
            # Restore the separator prefix that was consumed by split()
            block = "---\ntype: entry" + part
        else:
            block = part
        blocks.append(block)
    return blocks


def join_entries(blocks: List[str]) -> str:
    """Join entry blocks back into valid memory file content.

    Preserves proper separator formatting.
    """
    if not blocks:
        return ""
    if len(blocks) == 1:
        return blocks[0]

    # First block is written as-is; subsequent blocks get the full separator prefix
    first = blocks[0].rstrip()
    rest = [b.rstrip() for b in blocks[1:]]
    return first + ENTRY_SEPARATOR + ENTRY_SEPARATOR.join(rest)


def parse_entry_block(block: str) -> Optional[Dict[str, Any]]:
    """Parse a single entry block to extract metadata and body."""
    lines = block.split("\n")
    frontmatter = {}
    in_frontmatter = False
    body_lines = []

    for i, line in enumerate(lines):
        if line.strip() == "---" and i == 0:
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip() == "---":
            in_frontmatter = False
            continue

        if in_frontmatter:
            if ":" in line:
                key, val = line.split(":", 1)
                frontmatter[key.strip()] = val.strip()
        else:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()

    entry_type = frontmatter.get("type")
    if not entry_type:
        return None

    return {
        "type": entry_type,
        "entry_id": frontmatter.get("entry_id", ""),
        "date": frontmatter.get("date", ""),
        "day": frontmatter.get("day", ""),
        "emotion": frontmatter.get("emotion", ""),
        "language": frontmatter.get("language", ""),
        "body": body,
    }


def extract_entries(content: str) -> List[Dict[str, Any]]:
    """Extract all parsed entries from memory file content."""
    entries = []
    for block in split_entries(content):
        entry = parse_entry_block(block)
        if entry and entry.get("type") == "entry":
            entries.append(entry)
    return entries
