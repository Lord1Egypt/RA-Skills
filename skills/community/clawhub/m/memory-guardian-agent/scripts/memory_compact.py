#!/usr/bin/env python3
"""memory-guardian: Memory compaction — detect and remove redundancy across files.

Real-world lesson: after a day of heavy use, MEMORY.md and daily notes grow
bloated with duplicated account info, platform rules, post IDs, etc. This script
detects cross-file redundancy and suggests or applies compaction.

Usage:
  python3 memory_compact.py [--workspace <path>] [--dry-run] [--auto] [--max-memory-kb <int>]
"""
import json, os, re, argparse, hashlib
from collections import Counter
from datetime import datetime
from mg_utils import jaccard_distance, tokenize, read_text_file, safe_print

print = safe_print

DAILY_NOTE_ROTATE_BYTES = 30 * 1024



def jaccard(set_a, set_b):
    """Jaccard similarity between two sets (0=identical, 1=completely different)."""
    return jaccard_distance(set_a, set_b)


def load_file(path):
    if not os.path.exists(path):
        return ""
    return read_text_file(path)


def estimate_tokens(text):
    """Rough token estimate: ~1.3 tokens per CJK char, ~0.75 per ASCII word."""
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    ascii_words = len(re.findall(r"[a-zA-Z]+", text))
    return int(cjk * 1.3 + ascii_words * 0.75)


def section_token_analysis(text, path_hint=""):
    """Analyze token usage by section."""
    lines = text.splitlines()
    sections = []
    current_section = "header"
    current_lines = []
    current_tokens = 0

    for line in lines:
        if re.match(r"^#{1,3}\s+", line):
            # Save previous section
            if current_lines:
                sections.append({
                    "heading": current_section,
                    "lines": len(current_lines),
                    "tokens": current_tokens,
                    "preview": "".join(current_lines)[:120],
                })
            current_section = line.strip("# ").strip()
            current_lines = []
            current_tokens = 0
        else:
            current_lines.append(line)
            current_tokens += estimate_tokens(line)

    if current_lines:
        sections.append({
            "heading": current_section,
            "lines": len(current_lines),
            "tokens": current_tokens,
            "preview": "".join(current_lines)[:120],
        })

    return sections


def detect_redundancy(memory_text, daily_texts):
    """Find redundant content between MEMORY.md and daily notes."""
    memory_tokens = set(tokenize(memory_text))
    issues = []

    for date_file, daily_text in daily_texts.items():
        daily_tokens = set(tokenize(daily_text))

        # Overall overlap (distance: 0=identical)
        overall_dist = jaccard(memory_tokens, daily_tokens)

        # Per-section overlap in daily notes
        daily_sections = re.split(r"\n(?=###?\s)", daily_text)
        for section in daily_sections:
            if not section.strip():
                continue
            section_tokens = set(tokenize(section))
            if not section_tokens:
                continue
            section_dist = jaccard(memory_tokens, section_tokens)

            # Flag sections with high similarity (low distance)
            if section_dist < 0.5 and len(section_tokens) > 5:
                section_sim = round(1.0 - section_dist, 3)
                heading = re.match(r"###?\s+(.*)", section)
                heading_text = heading.group(1).strip() if heading else "unknown"
                issues.append({
                    "file": date_file,
                    "section": heading_text,
                    "similarity": section_sim,
                    "shared_tokens": len(memory_tokens & section_tokens),
                    "section_tokens": len(section_tokens),
                    "severity": "high" if section_dist < 0.3 else "medium",
                    "recommendation": (
                        "REMOVE — fully duplicated in MEMORY.md"
                        if section_dist < 0.3 else
                        "COMPACT — keep only decisions/action items, remove details already in MEMORY.md"
                    ),
                })

    return issues


def detect_internal_redundancy(text, path_hint=""):
    """Find duplicated content within a single file."""
    tokens = set(tokenize(text))
    lines = text.splitlines()

    # Find repeated line patterns
    line_signatures = Counter()
    repeated = []
    for i, line in enumerate(lines):
        sig = line.strip().lower()
        if len(sig) < 10:
            continue
        line_signatures[sig] += 1
        if line_signatures[sig] > 1:
            repeated.append({"line_num": i + 1, "content": line[:100], "count": line_signatures[sig]})

    # Deduplicate by content
    seen = set()
    unique_repeated = []
    for r in repeated:
        key = r["content"]
        if key not in seen:
            seen.add(key)
            unique_repeated.append(r)

    return unique_repeated


def detect_bloat_sections(text, max_tokens_per_section=500):
    """Flag sections that are too large."""
    sections = section_token_analysis(text)
    bloated = [s for s in sections if s["tokens"] > max_tokens_per_section]
    bloated.sort(key=lambda x: x["tokens"], reverse=True)
    return bloated


def aggressive_compact_memory_text(text):
    """Compact MEMORY.md by removing consecutive duplicate lines.

    Only removes adjacent lines that are identical, preserving non-consecutive
    duplicates (which may be intentional in different sections).
    """
    compacted = []
    previous_line = None
    previous_blank = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            compacted.append(line)
            previous_line = line
            previous_blank = False
            continue
        if not line.strip():
            if not previous_blank and compacted:
                compacted.append("")
            previous_blank = True
            previous_line = line
            continue
        previous_blank = False
        # Only skip if identical to the immediately preceding line
        if line == previous_line:
            continue
        compacted.append(line)
        previous_line = line

    return "\n".join(compacted).strip() + ("\n" if compacted else "")


def rotate_oversized_daily_notes(workspace, dry_run=False):
    """Archive oversized daily notes and replace them with a short summary."""
    memory_dir = os.path.join(workspace, "memory")
    archive_dir = os.path.join(memory_dir, "archive")
    rotated = []

    if not os.path.exists(memory_dir):
        return rotated

    for name in sorted(os.listdir(memory_dir)):
        if not re.match(r"\d{4}-\d{2}-\d{2}\.md$", name):
            continue
        path = os.path.join(memory_dir, name)
        if not os.path.isfile(path):
            continue
        size = os.path.getsize(path)
        if size <= DAILY_NOTE_ROTATE_BYTES:
            continue

        original = load_file(path)
        archive_path = os.path.join(archive_dir, name.replace(".md", ".full.md"))
        # Avoid overwriting existing archive — add timestamp suffix
        if os.path.exists(archive_path):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = archive_path.replace(".md", f"_{ts}.md")
        preview_lines = [
            line[:200] + ("..." if len(line) > 200 else "")
            for line in original.splitlines()
            if line.strip()
        ][:10]
        summary = "\n".join(
            [
                "# Rotated Daily Note",
                f"Original file: {name}",
                f"Original size: {size} bytes",
                f"Archived copy: memory/archive/{os.path.basename(archive_path)}",
                "",
                "## Summary Preview",
                *preview_lines,
                "",
            ]
        )

        if not dry_run:
            os.makedirs(archive_dir, exist_ok=True)
            with open(archive_path, "w", encoding="utf-8") as f:
                f.write(original)
            with open(path, "w", encoding="utf-8") as f:
                f.write(summary)

        rotated.append(
            {
                "file": name,
                "original_size": size,
                "archive_path": archive_path,
                "summary_size": len(summary.encode("utf-8")),
            }
        )

    return rotated


def run(workspace, dry_run, auto, max_memory_kb, aggressive=False):
    memory_path = os.path.join(workspace, "MEMORY.md")
    memory_dir = os.path.join(workspace, "memory")
    memory_text = load_file(memory_path)
    memory_size_before = os.path.getsize(memory_path) if os.path.exists(memory_path) else 0

    # Collect daily notes
    daily_texts = {}
    if os.path.exists(memory_dir):
        for f in sorted(os.listdir(memory_dir)):
            if f.endswith(".md") and re.match(r"\d{4}-\d{2}-\d{2}\.md$", f):
                daily_texts[f] = load_file(os.path.join(memory_dir, f))

    print("=" * 60)
    print("MEMORY GUARDIAN — Compaction Analysis")
    print("=" * 60)

    # 1. Size report
    mem_size = memory_size_before
    mem_tokens = estimate_tokens(memory_text)
    print(f"\n📊 MEMORY.md: {mem_size:,} bytes ({len(memory_text):,} chars), ~{mem_tokens} tokens")

    if max_memory_kb and mem_size > max_memory_kb * 1024:
        print(f"  ⚠️  Exceeds {max_memory_kb}KB target ({mem_size // 1024}KB)")

    # 2. Section analysis
    sections = section_token_analysis(memory_text)
    print(f"  {len(sections)} sections:")
    for s in sorted(sections, key=lambda x: x["tokens"], reverse=True):
        bar = "█" * min(int(s["tokens"] / 50), 20)
        flag = " ⚠️" if s["tokens"] > 500 else ""
        print(f"    {s['heading']:30s} {s['tokens']:5d} tok {bar}{flag}")

    # 3. Cross-file redundancy
    issues = detect_redundancy(memory_text, daily_texts)
    if issues:
        print(f"\n🔍 Cross-file redundancy ({len(issues)} issues):")
        for issue in sorted(issues, key=lambda x: x["similarity"], reverse=True):
            emoji = "🔴" if issue["severity"] == "high" else "🟡"
            print(f"  {emoji} {issue['file']} → {issue['section']}")
            print(f"     similarity={issue['similarity']:.2f}  shared={issue['shared_tokens']} tokens")
            print(f"     → {issue['recommendation']}")
    else:
        print("\n✅ No significant cross-file redundancy detected.")

    # 4. Internal redundancy
    repeated = detect_internal_redundancy(memory_text)
    if repeated:
        print(f"\n🔁 Internal duplication in MEMORY.md ({len(repeated)} repeated lines):")
        for r in repeated[:10]:
            print(f"  L{r['line_num']} (×{r['count']}): {r['content']}")
    else:
        print("\n✅ No internal duplication in MEMORY.md.")

    # 5. Daily notes bloat
    for date_file, daily_text in daily_texts.items():
        size = os.path.getsize(os.path.join(workspace, "memory", date_file))
        tokens = estimate_tokens(daily_text)
        chars = len(daily_text)
        flag = ""
        if size > 8000:
            flag = " ⚠️ CONSIDER COMPRESSING"
        print(f"\n📝 {date_file}: {size:,} bytes ({chars:,} chars), ~{tokens} tokens{flag}")

    # 6. Summary
    high_severity = [i for i in issues if i["severity"] == "high"]
    total_daily_size = sum(len(t) for t in daily_texts.values())
    total_size = mem_size + total_daily_size

    print(f"\n{'=' * 60}")
    print(f"📈 Total memory footprint: {total_size:,} bytes (~{estimate_tokens(memory_text + ''.join(daily_texts.values()))} tokens)")
    print(f"   MEMORY.md: {mem_size:,} bytes ({mem_size / max(total_size, 1) * 100:.0f}%)")
    print(f"   Daily notes: {total_daily_size:,} bytes ({total_daily_size / max(total_size, 1) * 100:.0f}%)")
    print(f"   High-severity redundancy: {len(high_severity)}")
    print(f"   Internal duplicates: {len(repeated)}")

    if high_severity:
        print(f"\n💡 Recommendation: Review and remove {len(high_severity)} high-severity redundant sections from daily notes.")

    # 7. Apply compaction if requested
    if auto and issues:
        compacted_count = 0
        for issue in issues:
            if issue["severity"] != "high":
                continue
            fpath = os.path.join(workspace, "memory", issue["file"])
            if not os.path.exists(fpath):
                continue
            daily_text = read_text_file(fpath)
            # Remove the redundant section (match heading + content block)
            heading_escaped = re.escape(issue["section"])
            # Match ## heading followed by content until next heading or EOF
            pattern = rf'\n?###?\s*{heading_escaped}\n.*?(?=\n###?\s|\Z)'
            new_text = re.sub(pattern, '', daily_text, count=1, flags=re.DOTALL)
            if len(new_text) < len(daily_text):
                import tempfile
                fd, tmp = tempfile.mkstemp(dir=os.path.dirname(fpath))
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(new_text)
                    os.replace(tmp, fpath)
                except Exception:
                    try: os.unlink(tmp)
                    except OSError: pass
                    raise
                compacted_count += 1
                print(f"  ✂️ Compacted {issue['file']} → {issue['section']} (removed)")
        if compacted_count:
            print(f"\n✂️ Compacted {compacted_count} redundant sections from daily notes.")
        else:
            print("\n✅ No sections could be auto-compacted (pattern mismatch).")

    if aggressive and os.path.exists(memory_path):
        compacted_memory = aggressive_compact_memory_text(memory_text)
        if not dry_run and compacted_memory != memory_text:
            # Create .bak backup before modifying
            import shutil
            backup_path = memory_path + ".bak"
            shutil.copy2(memory_path, backup_path)
            with open(memory_path, "w", encoding="utf-8") as f:
                f.write(compacted_memory)
            memory_text = compacted_memory
            mem_size = os.path.getsize(memory_path)
        elif dry_run:
            mem_size = len(compacted_memory.encode("utf-8"))

    rotated = rotate_oversized_daily_notes(workspace, dry_run=dry_run) if auto else []
    if rotated:
        print(f"\n🗂️ Rotated {len(rotated)} oversized daily notes.")

    memory_size_after = os.path.getsize(memory_path) if os.path.exists(memory_path) else 0

    return {
        "memory_size": mem_size,
        "memory_tokens": mem_tokens,
        "cross_file_issues": issues,
        "internal_duplicates": len(repeated),
        "high_severity_count": len(high_severity),
        "sections": sections,
        "memory_size_before": memory_size_before,
        "memory_size_after": memory_size_after,
        "rotated": bool(rotated),
        "rotated_count": len(rotated),
        "rotated_files": rotated,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian compaction analysis")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--dry-run", action="store_true", help="Analysis only (default behavior)")
    p.add_argument("--auto", action="store_true", help="Auto-apply compaction suggestions")
    p.add_argument("--aggressive", action="store_true", help="Aggressively compact MEMORY.md and oversized notes")
    p.add_argument("--max-memory-kb", type=int, default=5, help="Target max size for MEMORY.md in KB (default: 5)")
    args = p.parse_args()

    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )
    run(workspace, args.dry_run, args.auto, args.max_memory_kb, aggressive=args.aggressive)
