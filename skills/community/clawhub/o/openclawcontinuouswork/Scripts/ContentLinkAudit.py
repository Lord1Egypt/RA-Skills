#!/usr/bin/env python3
"""
ContentLinkAudit.py
Audit markdown modules for:
1) duplicate paragraphs (possible repetition)
2) missing intra-repo markdown links in ReferenceMap.md
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from collections import defaultdict


def norm_text(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s


def extract_paragraphs(md: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", md)
    out = []
    for b in blocks:
        t = norm_text(b)
        if not t:
            continue
        if t.startswith("#"):
            continue
        if len(t) < 40:
            continue
        out.append(t)
    return out


def extract_md_links(md: str) -> list[str]:
    # [text](path)
    return re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", md, flags=re.IGNORECASE)


def scan(root: Path) -> dict:
    md_files = sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)
    paragraph_index: dict[str, list[str]] = defaultdict(list)
    missing_links = []

    for f in md_files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        rel = str(f.relative_to(root))

        for para in extract_paragraphs(text):
            paragraph_index[para].append(rel)

        for link in extract_md_links(text):
            target = (f.parent / link).resolve()
            if not target.exists():
                missing_links.append({"file": rel, "link": link})

    duplicates = []
    for para, files in paragraph_index.items():
        uniq = sorted(set(files))
        if len(uniq) > 1:
            duplicates.append({
                "files": uniq,
                "sample": para[:160] + ("..." if len(para) > 160 else "")
            })

    return {
        "root": str(root),
        "markdown_files": len(md_files),
        "duplicate_paragraph_groups": duplicates,
        "missing_links": missing_links,
        "duplicate_count": len(duplicates),
        "missing_link_count": len(missing_links),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.target).resolve()
    result = scan(root)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"Root: {result['root']}")
    print(f"Markdown Files: {result['markdown_files']}")
    print(f"Duplicate Paragraph Groups: {result['duplicate_count']}")
    print(f"Missing Links: {result['missing_link_count']}")


if __name__ == "__main__":
    main()
