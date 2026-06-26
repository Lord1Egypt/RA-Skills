"""
Chunker — Handles large daily files by splitting into digestible pieces.

Problem: Power users may have 50K+ character daily files (agent logs, code output,
conversation transcripts). A single LLM call can't process all of it.

Solution:
1. Pre-filter: strip code blocks, log output, repetitive lines
2. Chunk: split into ~4K character pieces at section boundaries
3. Extract per chunk, merge results with dedup
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ChunkConfig:
    max_chunk_size: int = 4000
    pre_filter: bool = True
    min_line_length: int = 3  # skip very short lines


def pre_filter(text: str) -> str:
    """
    Remove low-signal content before sending to LLM.
    
    Strips:
    - Code blocks (```...```) unless they're short
    - Log output (lines starting with timestamps/brackets)
    - Repeated patterns (heartbeat checks, status lines)
    - Pure whitespace sections
    """
    lines = text.split('\n')
    filtered = []
    in_code_block = False
    code_block_lines = 0
    code_block_buffer = []
    seen_patterns = set()

    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block — keep if short, skip if long
                if code_block_lines <= 5:
                    filtered.extend(code_block_buffer)
                    filtered.append(line)
                else:
                    filtered.append(f"  [code block: {code_block_lines} lines omitted]")
                in_code_block = False
                code_block_lines = 0
                code_block_buffer = []
            else:
                in_code_block = True
                code_block_buffer = [line]
            continue

        if in_code_block:
            code_block_lines += 1
            code_block_buffer.append(line)
            continue

        # Skip log-like lines (timestamps, brackets, repeated status)
        stripped = line.strip()
        if not stripped:
            filtered.append(line)
            continue

        # Skip heartbeat/status lines
        if any(p in stripped.lower() for p in [
            'heartbeat_ok', 'no alert needed', 'no trend analysis',
            'pnl change since last', 'under $100 threshold',
            'within normal range'
        ]):
            continue

        # Skip very short lines
        if len(stripped) < 3:
            continue

        # Dedup near-identical lines (like repeated status checks)
        # Use first 40 chars as fingerprint
        fingerprint = stripped[:40]
        if fingerprint in seen_patterns:
            continue
        seen_patterns.add(fingerprint)

        filtered.append(line)

    return '\n'.join(filtered)


def chunk_text(text: str, config: ChunkConfig | None = None) -> list[str]:
    """
    Split text into chunks at natural boundaries.
    
    Tries to split at:
    1. ## headers (markdown sections)
    2. Empty lines (paragraph breaks)
    3. Hard limit at max_chunk_size
    """
    if config is None:
        config = ChunkConfig()

    if config.pre_filter:
        text = pre_filter(text)

    # If small enough, return as-is
    if len(text) <= config.max_chunk_size:
        return [text]

    chunks = []
    current = []
    current_len = 0

    lines = text.split('\n')

    for line in lines:
        line_len = len(line) + 1  # +1 for newline

        # Check if adding this line would exceed limit
        if current_len + line_len > config.max_chunk_size and current:
            # Try to find a good split point
            chunks.append('\n'.join(current))
            current = []
            current_len = 0

        # Start new chunk at ## headers if current chunk has content
        if line.startswith('## ') and current and current_len > config.max_chunk_size // 4:
            chunks.append('\n'.join(current))
            current = []
            current_len = 0

        current.append(line)
        current_len += line_len

    if current:
        chunks.append('\n'.join(current))

    return chunks


def merge_extractions(results: list[dict]) -> dict:
    """
    Merge multiple extraction results, deduplicating entities and triplets.
    
    Entities with the same name are merged (facts combined).
    Triplets are deduped by (subject, predicate, object).
    Events are deduped by description similarity.
    """
    entities_map: dict[str, dict] = {}
    triplets_set: set[tuple] = set()
    triplets: list[dict] = []
    events_set: set[str] = set()
    events: list[dict] = []

    for result in results:
        # Merge entities
        for entity in result.get("entities", []):
            name = entity.get("name", "")
            if not name:
                continue
            
            if name in entities_map:
                # Merge facts
                existing_facts = set(entities_map[name].get("facts", []))
                new_facts = entity.get("facts", [])
                for f in new_facts:
                    if f not in existing_facts:
                        entities_map[name].setdefault("facts", []).append(f)
            else:
                entities_map[name] = entity

        # Merge triplets (dedup by s,p,o)
        for t in result.get("triplets", []):
            key = (t.get("subject", ""), t.get("predicate", ""), t.get("object", ""))
            if key not in triplets_set:
                triplets_set.add(key)
                triplets.append(t)

        # Merge events (dedup by description prefix)
        for e in result.get("events", []):
            desc = e.get("description", "")
            fingerprint = desc[:60].lower()
            if fingerprint not in events_set:
                events_set.add(fingerprint)
                events.append(e)

    return {
        "entities": list(entities_map.values()),
        "triplets": triplets,
        "events": events,
    }
