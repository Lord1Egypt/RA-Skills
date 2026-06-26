#!/usr/bin/env python3
"""assembler.py - Assemble final output files from chunks.

Generates: source.md, ROOT_INDEX.md, processing_report.md,
           indexes/by-year.md, indexes/by-topic.md (if enriched),
           parts/*.md (if --split-by specified).

Usage: python3 scripts/assembler.py <chunks_jsonl> <output_dir> [--split-by year|topic|chapter|none]
"""

import json
import os
import sys
from collections import defaultdict


def load_chunks(chunks_path):
    """Load chunks from JSONL file."""
    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    # Sort by char_start to ensure correct order
    chunks.sort(key=lambda c: c.get("char_start", 0))
    return chunks


def has_enrichment(chunks):
    """Check if chunks have enrichment data."""
    for ch in chunks:
        if ch.get("summary"):
            return True
    return False


def generate_source_md(chunks, output_dir):
    """Concatenate chunk texts into a clean source.md, removing overlaps."""
    path = os.path.join(output_dir, "source.md")
    last_end = 0
    parts = []

    for ch in chunks:
        start = ch.get("char_start", 0)
        text = ch["text"]

        if start < last_end and last_end > 0:
            # This chunk has overlap with previous — trim the overlap
            overlap = last_end - start
            if 0 < overlap < len(text):
                text = text[overlap:]

        parts.append(text)
        last_end = ch.get("char_end", start + len(text))

    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(parts))

    size = os.path.getsize(path)
    print(f"[assembler] source.md: {size:,} bytes")
    return path


def generate_root_index(chunks, output_dir, enriched):
    """Generate ROOT_INDEX.md with chapter structure and optional summaries."""
    path = os.path.join(output_dir, "ROOT_INDEX.md")
    lines = ["# Document Index\n\n"]

    # Build structure from heading paths
    seen_headings = []
    current_path = []

    for ch in chunks:
        hp = ch.get("heading_path", [])
        if hp and hp != current_path:
            current_path = hp
            # Determine indent level
            depth = len(hp) - 1
            indent = "  " * depth
            title = hp[-1] if hp else ch["chunk_id"]

            entry = f"{indent}- **{title}**"
            if enriched and ch.get("summary"):
                entry += f" — {ch['summary']}"
            entry += f" `{ch['chunk_id']}`"
            lines.append(entry + "\n")
            seen_headings.append(title)
        elif not hp and ch["chunk_id"] == "ch-0001":
            # First chunk with no heading
            entry = f"- *(Start)* `{ch['chunk_id']}`"
            if enriched and ch.get("summary"):
                entry += f" — {ch['summary']}"
            lines.append(entry + "\n")

    if not seen_headings:
        # No headings detected — list all chunks
        lines.append("*No heading structure detected. Listing all chunks:*\n\n")
        for ch in chunks:
            entry = f"- `{ch['chunk_id']}` (chars {ch.get('char_start', '?')}-{ch.get('char_end', '?')})"
            if enriched and ch.get("summary"):
                entry += f" — {ch['summary']}"
            lines.append(entry + "\n")

    lines.append(f"\n---\n*Total chunks: {len(chunks)}*\n")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[assembler] ROOT_INDEX.md: {len(seen_headings)} headings")
    return path


def generate_indexes(chunks, output_dir):
    """Generate by-year.md and by-topic.md from classification data."""
    idx_dir = os.path.join(output_dir, "indexes")
    os.makedirs(idx_dir, exist_ok=True)
    generated = []

    # Group by year
    by_year = defaultdict(list)
    by_topic = defaultdict(list)

    for ch in chunks:
        cls = ch.get("classification", {})
        if not cls:
            continue
        year = cls.get("year", "").strip()
        topic = cls.get("topic", "").strip()
        if year:
            by_year[year].append(ch)
        if topic:
            by_topic[topic].append(ch)

    # by-year.md
    if by_year:
        path = os.path.join(idx_dir, "by-year.md")
        lines = ["# Index by Year\n\n"]
        for year in sorted(by_year.keys()):
            lines.append(f"## {year}\n\n")
            for ch in by_year[year]:
                summary = ch.get("summary", "")
                hp = " > ".join(ch.get("heading_path", []))
                label = hp if hp else ch["chunk_id"]
                entry = f"- **{label}** `{ch['chunk_id']}`"
                if summary:
                    entry += f" — {summary}"
                lines.append(entry + "\n")
            lines.append("\n")
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        generated.append("indexes/by-year.md")
        print(f"[assembler] by-year.md: {len(by_year)} years")

    # by-topic.md
    if by_topic:
        path = os.path.join(idx_dir, "by-topic.md")
        lines = ["# Index by Topic\n\n"]
        for topic in sorted(by_topic.keys()):
            lines.append(f"## {topic}\n\n")
            for ch in by_topic[topic]:
                summary = ch.get("summary", "")
                hp = " > ".join(ch.get("heading_path", []))
                label = hp if hp else ch["chunk_id"]
                entry = f"- **{label}** `{ch['chunk_id']}`"
                if summary:
                    entry += f" — {summary}"
                lines.append(entry + "\n")
            lines.append("\n")
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        generated.append("indexes/by-topic.md")
        print(f"[assembler] by-topic.md: {len(by_topic)} topics")

    return generated


def generate_parts(chunks, output_dir, split_by):
    """Generate parts/*.md based on split strategy."""
    if split_by == "none" or not split_by:
        return []

    parts_dir = os.path.join(output_dir, "parts")
    os.makedirs(parts_dir, exist_ok=True)
    generated = []

    groups = defaultdict(list)

    for ch in chunks:
        if split_by == "year":
            key = ch.get("classification", {}).get("year", "unknown")
        elif split_by == "topic":
            key = ch.get("classification", {}).get("topic", "uncategorized")
        elif split_by == "chapter":
            hp = ch.get("heading_path", [])
            key = hp[0] if hp else "no-chapter"
        else:
            key = "all"
        groups[key.strip() or "unknown"].append(ch)

    for key, group_chunks in sorted(groups.items()):
        # Sanitize filename
        safe_name = "".join(c if c.isalnum() or c in "-_ " else "_" for c in key).strip()
        if not safe_name:
            safe_name = "unknown"
        filename = f"{safe_name}.md"
        path = os.path.join(parts_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {key}\n\n")
            for ch in group_chunks:
                f.write(ch["text"])
                f.write("\n\n---\n\n")

        generated.append(f"parts/{filename}")
        print(f"[assembler] parts/{filename}: {len(group_chunks)} chunks")

    return generated


def generate_report(output_dir, chunks, enriched, warnings=None, failed_chunks=None, mode="unknown"):
    """Generate processing_report.md."""
    path = os.path.join(output_dir, "processing_report.md")
    lines = ["# Processing Report\n\n"]

    lines.append(f"- **Mode:** {mode}\n")
    lines.append(f"- **Total chunks:** {len(chunks)}\n")

    total_chars = sum(len(ch.get("text", "")) for ch in chunks)
    lines.append(f"- **Total characters:** {total_chars:,}\n")

    if enriched:
        enriched_count = sum(1 for ch in chunks if ch.get("summary"))
        failed_count = sum(1 for ch in chunks if ch.get("enrichment_error"))
        lines.append(f"- **Enriched chunks:** {enriched_count}\n")
        if failed_count:
            lines.append(f"- **Failed enrichment:** {failed_count}\n")

    if warnings:
        lines.append("\n## Conversion Warnings\n\n")
        for w in warnings:
            lines.append(f"- {w}\n")

    if failed_chunks:
        lines.append("\n## Failed Chunks\n\n")
        for cid in failed_chunks:
            lines.append(f"- {cid}\n")

    # Chunk size distribution
    lines.append("\n## Chunk Size Distribution\n\n")
    sizes = [len(ch.get("text", "")) for ch in chunks]
    if sizes:
        lines.append(f"- Min: {min(sizes):,} chars\n")
        lines.append(f"- Max: {max(sizes):,} chars\n")
        lines.append(f"- Avg: {sum(sizes) // len(sizes):,} chars\n")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[assembler] processing_report.md generated")
    return path


def assemble(chunks_path, output_dir, split_by="none", warnings=None, failed_chunks=None, mode="unknown"):
    """Main assembly function. Returns list of generated file paths."""
    chunks = load_chunks(chunks_path)
    if not chunks:
        print("[assembler] WARNING: No chunks to assemble")
        return []

    enriched = has_enrichment(chunks)
    print(f"[assembler] {len(chunks)} chunks, enriched={enriched}")

    os.makedirs(output_dir, exist_ok=True)
    outputs = []

    # source.md
    generate_source_md(chunks, output_dir)
    outputs.append("source.md")

    # ROOT_INDEX.md
    generate_root_index(chunks, output_dir, enriched)
    outputs.append("ROOT_INDEX.md")

    # processing_report.md
    generate_report(output_dir, chunks, enriched, warnings, failed_chunks, mode)
    outputs.append("processing_report.md")

    # Indexes (only if enriched)
    if enriched:
        idx_files = generate_indexes(chunks, output_dir)
        outputs.extend(idx_files)

    # Parts (only if split-by specified)
    if split_by and split_by != "none":
        part_files = generate_parts(chunks, output_dir, split_by)
        outputs.extend(part_files)

    print(f"[assembler] Generated {len(outputs)} output files")
    return outputs


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 assembler.py <chunks_jsonl> <output_dir> [--split-by year|topic|chapter|none]")
        sys.exit(1)

    chunks_path = sys.argv[1]
    output_dir = sys.argv[2]

    split_by = "none"
    if "--split-by" in sys.argv:
        idx = sys.argv.index("--split-by")
        if idx + 1 < len(sys.argv):
            split_by = sys.argv[idx + 1]

    if not os.path.exists(chunks_path):
        print(f"ERROR: Chunks file not found: {chunks_path}")
        sys.exit(1)

    assemble(chunks_path, output_dir, split_by)


if __name__ == "__main__":
    main()
