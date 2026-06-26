#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


CHUNK_SIZE_CHARS = 1600      # ~400 tokens
CHUNK_OVERLAP_CHARS = 200    # ~50 tokens


@dataclass
class VaultChunk:
    file_path: str
    chunk_index: int
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    raw_fm = parts[1]
    body = parts[2]
    fm: dict[str, Any] = {}

    title_match = re.search(r"^title:\s*(.+)$", raw_fm, flags=re.MULTILINE)
    if title_match:
        fm["title"] = _strip_yaml(title_match.group(1))

    summary_match = re.search(r"^summary:\s*(.+)$", raw_fm, flags=re.MULTILINE)
    if summary_match:
        fm["summary"] = _strip_yaml(summary_match.group(1))

    category_match = re.search(r"^category:\s*(.+)$", raw_fm, flags=re.MULTILINE)
    if category_match:
        fm["category"] = _strip_yaml(category_match.group(1))

    source_match = re.search(r"^source:\s*(.+)$", raw_fm, flags=re.MULTILINE)
    if source_match:
        fm["source"] = _strip_yaml(source_match.group(1))

    tags = _parse_yaml_list(raw_fm, "tags")
    if tags:
        fm["tags"] = tags

    aliases = _parse_yaml_list(raw_fm, "aliases")
    if aliases:
        fm["aliases"] = aliases

    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", body)
    if wikilinks:
        fm["wikilinks"] = list(dict.fromkeys(wikilinks))

    return fm, body


def split_into_chunks(text: str, *, chunk_size: int = CHUNK_SIZE_CHARS, overlap: int = CHUNK_OVERLAP_CHARS) -> list[str]:
    text = text.strip()
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:].strip())
            break

        # Try to break at a paragraph boundary
        slice_text = text[start:end]
        break_pos = slice_text.rfind("\n\n")
        if break_pos == -1 or break_pos < chunk_size // 3:
            # Fall back to sentence boundary
            break_pos = slice_text.rfind(". ")
            if break_pos == -1 or break_pos < chunk_size // 3:
                break_pos = chunk_size

        actual_end = start + break_pos
        chunk = text[start:actual_end].strip()
        if chunk:
            chunks.append(chunk)
        start = max(0, actual_end - overlap)
        if start <= (actual_end - chunk_size):
            start = actual_end

    return chunks


def read_vault_file(file_path: Path, vault_root: Path) -> list[VaultChunk]:
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return []

    if not text.strip():
        return []

    frontmatter, body = parse_frontmatter(text)
    relative_path = str(file_path.relative_to(vault_root))

    # Determine category from directory structure
    rel_parts = file_path.relative_to(vault_root).parts
    if len(rel_parts) > 1:
        frontmatter.setdefault("category", rel_parts[0])

    # Use filename as title fallback
    frontmatter.setdefault("title", file_path.stem.replace("-", " ").strip())

    raw_chunks = split_into_chunks(body)
    if not raw_chunks:
        return []

    vault_chunks: list[VaultChunk] = []
    for idx, chunk_text in enumerate(raw_chunks):
        vault_chunks.append(VaultChunk(
            file_path=relative_path,
            chunk_index=idx,
            content=chunk_text,
            metadata=dict(frontmatter),
        ))

    return vault_chunks


def read_all_vault_files(vault_path: Path, inbox_folder: str = "_Inbox") -> list[VaultChunk]:
    all_chunks: list[VaultChunk] = []

    for md_path in vault_path.rglob("*.md"):
        if ".obsidian" in md_path.parts or inbox_folder in md_path.parts:
            continue
        chunks = read_vault_file(md_path, vault_path)
        all_chunks.extend(chunks)

    return all_chunks


def _strip_yaml(value: str) -> str:
    clean = value.strip()
    for quote in ("'", '"'):
        if clean.startswith(quote) and clean.endswith(quote) and len(clean) >= 2:
            clean = clean[1:-1]
            break
    return clean.strip()


def _parse_yaml_list(raw_fm: str, key: str) -> list[str]:
    inline_match = re.search(rf"^{key}:\s*\[(.*?)\]\s*$", raw_fm, flags=re.MULTILINE)
    if inline_match:
        return [_strip_yaml(item) for item in inline_match.group(1).split(",") if item.strip()]

    items: list[str] = []
    lines = raw_fm.splitlines()
    collecting = False
    for line in lines:
        if line.startswith(f"{key}:"):
            collecting = True
            continue
        if collecting:
            if re.match(r"^\s*-\s+", line):
                item = re.sub(r"^\s*-\s+", "", line)
                items.append(_strip_yaml(item))
            elif line.strip():
                break
    return items
