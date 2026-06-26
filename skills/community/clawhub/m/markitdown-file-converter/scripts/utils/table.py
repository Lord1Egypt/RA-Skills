#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown table beautifier - convert various table formats to clean pipe tables.
"""

import re
from typing import List


def is_separator(line: str) -> bool:
    """Check if a line is a table separator (---, ===, ~~~)."""
    s = line.strip()
    if not s:
        return False
    if not re.match(r"^[\s\-=~]+$", s):
        return False
    return len(re.sub(r"[^\-=~]", "", s)) >= 21


def parse_grid_row(line: str) -> List[str]:
    """Parse a grid table row (separated by 2+ spaces)."""
    s = line.strip()
    if not s:
        return []
    return [p.strip() for p in re.split(r"\s{2,}", s) if p.strip()]


def beautify_markdown_tables(md_text: str) -> str:
    """
    Convert various Markdown table formats to clean pipe tables.
    
    Handles:
    - pandoc grid tables (full-width, 2+ space separation)
    - pandoc simple tables (2-space aligned, no pipes)
    - pipe tables (| col1 | col2 |)
    """
    lines = md_text.splitlines()
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # pandoc full-width grid table
        if is_separator(line):
            while i < len(lines) and is_separator(lines[i]):
                i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            block_rows = []
            saw_mid = False
            while i < len(lines):
                cur = lines[i]
                cur_s = cur.strip()
                if is_separator(cur):
                    if saw_mid:
                        break
                    saw_mid = True
                    i += 1
                    while i < len(lines) and not lines[i].strip():
                        i += 1
                    continue
                if not cur_s:
                    i += 1
                    continue
                if cur_s.startswith("#"):
                    break
                block_rows.append(cur.rstrip())
                i += 1
            while i < len(lines) and is_separator(lines[i]):
                i += 1
            
            dr = [r for r in block_rows if r.strip()]
            all_r = [parse_grid_row(r) for r in dr]
            all_r = [r for r in all_r if r]
            
            if len(all_r) >= 2:
                cc = len(all_r[0])
                if all(len(r) == cc for r in all_r):
                    result.append("| " + " | ".join(all_r[0]) + " |")
                    result.append("| " + " | ".join(["---"] * cc) + " |")
                    for row in all_r[1:]:
                        result.append("| " + " | ".join(row) + " |")
                    continue
            for r in dr:
                result.append(r)
            continue

        stripped = line.strip()

        # pandoc simple table (2-space aligned, no pipes)
        if (stripped
                and "|" not in stripped
                and not stripped.startswith("#")
                and re.search(r"\s{2,}", stripped)):
            block = []
            while i < len(lines):
                cur_s = lines[i].strip()
                if (cur_s and "|" not in cur_s
                        and not cur_s.startswith("#")
                        and re.search(r"\s{2,}", cur_s)):
                    block.append(cur_s)
                    i += 1
                else:
                    break
            if len(block) >= 2:
                all_r = [parse_grid_row(r) for r in block]
                cc = len(all_r[0])
                if all(len(r) == cc for r in all_r):
                    result.append("| " + " | ".join(all_r[0]) + " |")
                    result.append("| " + " | ".join(["---"] * cc) + " |")
                    for row in all_r[1:]:
                        result.append("| " + " | ".join(row) + " |")
                    continue
            for r in block:
                result.append(r)
            continue

        # pipe table
        if stripped.startswith("|") and stripped.endswith("|"):
            rows = []
            while i < len(lines):
                cur = lines[i].strip()
                if cur.startswith("|") and cur.endswith("|"):
                    rows.append(cur)
                    i += 1
                else:
                    break
            if len(rows) >= 2:
                parsed = [
                    [c.strip() for c in re.split(r"\s*\|\s*", r.strip("|")) if c.strip()]
                    for r in rows
                ]
                ccs = [len(cells) for cells in parsed]
                if len(set(ccs)) == 1 and ccs[0] > 1:
                    has_sep = any(is_separator(r) for r in rows)
                    result.append(rows[0])
                    if not has_sep:
                        result.append("| " + " | ".join(["---"] * ccs[0]) + " |")
                    result.extend(rows[1:])
                    continue
            result.extend(rows)
            continue

        result.append(line)
        i += 1

    return "\n".join(result)