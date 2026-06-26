#!/usr/bin/env python3
"""chunker.py - Split markdown into structured chunks.

Detects headings (#, ##, numbered sections, Chinese chapter names 第X章).
Target chunk size: 3000-5000 chars, 200 char overlap.
Output: chunks.jsonl with one JSON object per line.

Usage: python3 scripts/chunker.py <markdown_file> <output_chunks_jsonl>
"""

import json
import os
import re
import sys

# Chunk size parameters
MIN_CHUNK = 3000
MAX_CHUNK = 5000
OVERLAP = 200

# Patterns for structural boundaries
HEADING_RE = re.compile(
    r'^(?:'
    r'#{1,6}\s+'                          # Markdown headings
    r'|第[一二三四五六七八九十百千\d]+[章节篇部回]'  # Chinese chapter names
    r'|\d+[\.\、]\s+'                      # Numbered sections: "1. " or "1、"
    r')',
    re.MULTILINE,
)


def detect_headings(text):
    """Find all heading positions and their text.
    Returns list of (char_pos, heading_text, level).
    Detects: Markdown headings, Chinese chapters, numbered sections,
    bold-text titles (standalone **...** lines), and diary-style entries.
    """
    headings = []
    seen_positions = set()

    # Pattern 1: Markdown headings
    for m in re.finditer(r'^(#{1,6})\s+(.+)$', text, re.MULTILINE):
        pos = m.start()
        level = len(m.group(1))
        title = m.group(2).strip()
        headings.append((pos, title, level))
        seen_positions.add(pos)

    # Pattern 2: Chinese chapter names (第X章/节/篇/部/回)
    for m in re.finditer(
        r'^(第[一二三四五六七八九十百千\d]+[章节篇部回])[\s\.:：]*(.*)$',
        text, re.MULTILINE,
    ):
        pos = m.start()
        if pos not in seen_positions:
            title = (m.group(1) + " " + (m.group(2) or "")).strip()
            headings.append((pos, title, 1))
            seen_positions.add(pos)

    # Pattern 3: Numbered sections (1. or 1、)
    for m in re.finditer(r'^(\d+[\.\、])\s+(.+)$', text, re.MULTILINE):
        pos = m.start()
        if pos not in seen_positions:
            title = (m.group(1) + " " + m.group(2)).strip()
            headings.append((pos, title, 2))
            seen_positions.add(pos)

    # Pattern 4: Bold-text titles — standalone lines that are entirely bold
    # Matches: **Title text here** (on its own line, possibly with trailing text)
    for m in re.finditer(r'^\*\*(.+?)\*\*\s*$', text, re.MULTILINE):
        pos = m.start()
        if pos not in seen_positions:
            title = m.group(1).strip()
            # Heuristic: skip if too long (>80 chars) — probably a bold paragraph, not a title
            if len(title) <= 80:
                headings.append((pos, title, 2))
                seen_positions.add(pos)

    # Sort by position
    headings.sort(key=lambda x: x[0])
    return headings


def build_heading_path(headings_so_far, current_level):
    """Maintain a heading path stack based on level."""
    path = []
    for _, title, level in headings_so_far:
        if level <= current_level:
            # Trim path to appropriate depth
            while len(path) >= level:
                if path:
                    path.pop()
                else:
                    break
            path.append(title)
        elif level == current_level:
            if path:
                path[-1] = title
            else:
                path.append(title)
    return path


def chunk_text(text):
    """Split text into chunks respecting structure.
    Returns list of dicts with chunk_id, heading_path, char_start, char_end, text.
    """
    if not text.strip():
        return [{
            "chunk_id": "ch-0001",
            "heading_path": [],
            "char_start": 0,
            "char_end": len(text),
            "text": text,
        }]

    headings = detect_headings(text)
    
    # Build split points: heading positions + paragraph breaks for large gaps
    split_points = [0]
    for pos, _, _ in headings:
        if pos > 0:
            split_points.append(pos)
    split_points.append(len(text))
    split_points = sorted(set(split_points))

    # Merge small sections, split large ones
    segments = []
    for i in range(len(split_points) - 1):
        start = split_points[i]
        end = split_points[i + 1]
        segments.append((start, end))

    # Now build chunks from segments
    chunks = []
    current_start = 0
    current_end = 0
    heading_stack = []  # list of (title, level)

    def flush_chunk(start, end):
        path = [t for t, _ in heading_stack]
        chunks.append({
            "char_start": start,
            "char_end": end,
            "heading_path": list(path),
            "text": text[start:end],
        })

    i = 0
    while i < len(segments):
        seg_start, seg_end = segments[i]
        seg_len = seg_end - seg_start

        # Update heading stack for this segment
        for pos, title, level in headings:
            if pos == seg_start:
                # Pop headings at same or deeper level
                while heading_stack and heading_stack[-1][1] >= level:
                    heading_stack.pop()
                heading_stack.append((title, level))

        if current_end == 0:
            # Starting new chunk
            current_start = seg_start
            current_end = seg_end
        elif (current_end - current_start) + seg_len <= MAX_CHUNK:
            # Extend current chunk
            current_end = seg_end
        else:
            # Current chunk is big enough, flush it
            if current_end - current_start > 0:
                flush_chunk(current_start, current_end)
            current_start = seg_start
            current_end = seg_end
        
        i += 1

    # Flush remaining
    if current_end > current_start:
        flush_chunk(current_start, current_end)

    # Handle oversized chunks: split by paragraph boundaries
    final_chunks = []
    for chunk in chunks:
        if len(chunk["text"]) <= MAX_CHUNK:
            final_chunks.append(chunk)
        else:
            # Split large chunk by paragraphs
            sub_chunks = _split_large_chunk(
                chunk["text"], chunk["char_start"], chunk["heading_path"]
            )
            final_chunks.extend(sub_chunks)

    # Handle undersized chunks: merge adjacent small ones
    merged = []
    for chunk in final_chunks:
        if merged and len(merged[-1]["text"]) < MIN_CHUNK and len(merged[-1]["text"]) + len(chunk["text"]) <= MAX_CHUNK:
            prev = merged[-1]
            prev["char_end"] = chunk["char_end"]
            prev["text"] = prev["text"] + chunk["text"]
            if chunk["heading_path"] and chunk["heading_path"] != prev["heading_path"]:
                prev["heading_path"] = chunk["heading_path"]
        else:
            merged.append(chunk)

    # Add overlap and assign IDs
    result = []
    for idx, chunk in enumerate(merged):
        chunk_id = f"ch-{idx + 1:04d}"
        # Add overlap from previous chunk
        if idx > 0 and chunk["char_start"] > 0:
            overlap_start = max(0, chunk["char_start"] - OVERLAP)
            overlap_text = text[overlap_start:chunk["char_start"]]
            final_text = overlap_text + chunk["text"]
            final_start = overlap_start
        else:
            final_text = chunk["text"]
            final_start = chunk["char_start"]

        result.append({
            "chunk_id": chunk_id,
            "heading_path": chunk["heading_path"],
            "char_start": final_start,
            "char_end": chunk["char_end"],
            "text": final_text,
        })

    return result


def _split_large_chunk(text, base_offset, heading_path):
    """Split an oversized chunk by paragraph boundaries."""
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_text = ""
    current_start = base_offset

    for para in paragraphs:
        para_with_sep = para + "\n\n"
        if len(current_text) + len(para_with_sep) > MAX_CHUNK and current_text:
            chunks.append({
                "char_start": current_start,
                "char_end": current_start + len(current_text),
                "heading_path": list(heading_path),
                "text": current_text,
            })
            current_start = current_start + len(current_text)
            current_text = para_with_sep
        else:
            current_text += para_with_sep

    if current_text.strip():
        chunks.append({
            "char_start": current_start,
            "char_end": current_start + len(current_text),
            "heading_path": list(heading_path),
            "text": current_text,
        })

    return chunks


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 chunker.py <markdown_file> <output_chunks_jsonl>")
        sys.exit(1)

    md_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(md_path):
        print(f"ERROR: File not found: {md_path}")
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"[chunker] Input: {len(text):,} characters")

    chunks = chunk_text(text)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"[chunker] Generated {len(chunks)} chunks")
    for ch in chunks[:5]:
        hp = " > ".join(ch["heading_path"]) if ch["heading_path"] else "(no heading)"
        print(f"  {ch['chunk_id']}: {len(ch['text']):,} chars - {hp}")
    if len(chunks) > 5:
        print(f"  ... and {len(chunks) - 5} more")

    print(f"[chunker] Output: {output_path}")


if __name__ == "__main__":
    main()
