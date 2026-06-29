#!/usr/bin/env python3
"""
INI file section & key alignment tool.
Reorders sections in a target INI file to match the order in a source INI file,
and also reorders key-value pairs within each section accordingly.
"""

import re
import sys
from collections import OrderedDict
from pathlib import Path


def parse_ini(filepath):
    """
    Parse an INI file into an OrderedDict of sections.
    Each section value is an OrderedDict of key-value pairs.
    Preserves section order and key order. Comments are preserved as metadata.

    Returns (sections, duplicates_warning) where sections is:
        OrderedDict[section_name -> OrderedDict[key -> value]]
    """
    sections = OrderedDict()
    current_section = None
    duplicates = []
    seen_sections = {}

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for lineno, line in enumerate(f, 1):
            line = line.rstrip('\n\r')
            # Match section headers like [SectionName]
            m = re.match(r'^\s*\[(.+?)\]\s*$', line)
            if m:
                name = m.group(1).strip()
                if name in sections:
                    duplicates.append((lineno, name))
                    continue  # Skip duplicate sections, keep first
                sections[name] = OrderedDict()
                current_section = name
                seen_sections[name] = lineno
                continue

            if current_section is None:
                continue

            # Match key=value (ignoring comment-only lines and blank lines)
            m = re.match(r'^\s*([^=;\n#]+?)\s*=\s*(.*?)\s*$', line)
            if m:
                key = m.group(1).strip()
                val = m.group(2).strip()
                if key not in sections[current_section]:
                    sections[current_section][key] = val
                # Skip duplicate keys within same section

    return sections, duplicates


def align_ini(source_path, target_path, output_path):
    """
    Align target INI to match source INI section/key order.

    Args:
        source_path: Path to the reference (source) INI file
        target_path: Path to the INI file to be reordered
        output_path: Path to write the output
    """
    source_sections, src_dupes = parse_ini(source_path)
    target_sections, tgt_dupes = parse_ini(target_path)

    src_section_names = list(source_sections.keys())
    tgt_section_names = set(target_sections.keys())

    # --- Statistics ---
    common = set(src_section_names) & tgt_section_names
    src_only = set(src_section_names) - tgt_section_names
    tgt_only = tgt_section_names - set(src_section_names)

    lines = []

    # Section 1: Common sections in source order, with keys in source order
    for sec_name in src_section_names:
        if sec_name not in target_sections:
            continue

        lines.append(f"[{sec_name}]")
        src_keys = list(source_sections[sec_name].keys())
        tgt_kv = target_sections[sec_name]

        # Keys in source order
        seen_keys = set()
        for key in src_keys:
            if key in tgt_kv:
                lines.append(f"{key}={tgt_kv[key]}")
                seen_keys.add(key)

        # Keys in target that are not in source (target-only keys)
        for key, val in tgt_kv.items():
            if key not in seen_keys:
                lines.append(f"{key}={val}")

        lines.append("")

    # Section 2: Source-only sections (no content, just markers)
    if src_only:
        lines.append("; ===== 标准文件独有 section =====")
        lines.append("")
        for sec_name in src_section_names:
            if sec_name in src_only:
                lines.append(f"; [{sec_name}]")
                lines.append("")
        lines.append("")

    # Section 3: Target-only sections (full content)
    if tgt_only:
        lines.append("; ===== 旧文件独有 section =====")
        lines.append("")
        for sec_name in tgt_section_names:
            if sec_name in tgt_only:
                lines.append(f"[{sec_name}]")
                for key, val in target_sections[sec_name].items():
                    lines.append(f"{key}={val}")
                lines.append("")

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    # Print statistics
    print(f"对齐完成。")
    print(f"")
    print(f"| 项目 | 数量 |")
    print(f"|------|------|")
    print(f"| 源文件 section 总数 | {len(src_section_names)} |")
    print(f"| 目标文件 section 总数 | {len(tgt_section_names)} |")
    print(f"| 两文件共有 section | {len(common)} |")
    print(f"| 源文件独有 section | {len(src_only)} |")
    print(f"| 目标文件独有 section | {len(tgt_only)} |")

    if src_dupes:
        print(f"\n警告：源文件中存在 {len(src_dupes)} 个重复 section，已取首次出现：")
        for lineno, name in src_dupes:
            print(f"  第 {lineno} 行: [{name}]")

    if tgt_dupes:
        print(f"\n警告：目标文件中存在 {len(tgt_dupes)} 个重复 section，已跳过：")
        for lineno, name in tgt_dupes:
            print(f"  第 {lineno} 行: [{name}]")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ini_align.py <source.ini> <target.ini> <output.ini>")
        sys.exit(1)

    align_ini(sys.argv[1], sys.argv[2], sys.argv[3])
