#!/usr/bin/env python3
"""Audit a Knowledge-style LLM Wiki.

This script is packaged with the llm-wiki skill under `schema/scripts/` so it can
be published together with the skill. It can be run from either location:

    python3 Knowledge/schema/scripts/verify_wiki.py

For this vault, `Knowledge/verify_wiki.py` is kept as a small compatibility
wrapper that delegates to this script.

The script locates the Knowledge root by walking upward until it finds both
`source/` and `wiki/` directories, then checks:

- source coverage by wiki source pages;
- broken Obsidian wikilinks;
- index coverage;
- UTF-8 decode errors.
"""

import glob
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def find_knowledge_root(start: Path) -> Path:
    """Find the nearest ancestor that looks like a Knowledge root."""
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    for candidate in [cur, *cur.parents]:
        if (candidate / "source").is_dir() and (candidate / "wiki").is_dir():
            return candidate
    raise SystemExit(
        "Could not locate Knowledge root: expected an ancestor containing both "
        "source/ and wiki/ directories."
    )


BASE_PATH = find_knowledge_root(Path(__file__))
BASE = str(BASE_PATH)
WIKI = os.path.join(BASE, "wiki")
SOURCE = os.path.join(BASE, "source")
INDEX = os.path.join(WIKI, "index.md")

issues: list[str] = []


def rel(path, root=BASE):
    return os.path.relpath(path, root).replace("\\", "/")


def read_utf8(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        issues.append(f"[UTF-8] Encoding error: {rel(path)}")
        return ""


def extract_wikilinks(text):
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text)


# Build a lookup: normalized target -> real file path.
# Normalize by stripping spaces and lowercasing for fuzzy matching.
def norm(s):
    return re.sub(r"\s+", "", s).lower()


all_wiki_files = glob.glob(os.path.join(WIKI, "**", "*.md"), recursive=True)
all_source_files = glob.glob(os.path.join(SOURCE, "**", "*.md"), recursive=True)
all_source_other = glob.glob(os.path.join(SOURCE, "**", "*.pdf"), recursive=True)
all_schema_files = glob.glob(os.path.join(BASE, "schema", "**", "*.md"), recursive=True)
all_vault_files = [
    f
    for f in glob.glob(os.path.join(BASE, "**", "*"), recursive=True)
    if os.path.isfile(f)
]
all_known_files = list(
    dict.fromkeys(
        all_wiki_files
        + all_source_files
        + all_source_other
        + all_schema_files
        + all_vault_files
    )
)

lookup = {}
for f in all_known_files:
    r = rel(f)
    lookup[norm(r)] = f
    if r.endswith(".md"):
        lookup[norm(r[:-3])] = f
    for ext in (".pdf", ".txt", ".html", ".py"):
        if r.endswith(ext):
            lookup[norm(r[: -len(ext)])] = f


def resolve_wikilink(target):
    clean = target.strip().split("#", 1)[0]
    if not clean or clean == "...":
        return "PLACEHOLDER"
    if clean.startswith("Knowledge/"):
        clean = clean[len("Knowledge/") :]
    elif not clean.startswith(("wiki/", "source/", "schema/")):
        clean = "wiki/" + clean
    n = norm(clean)
    if n in lookup:
        return lookup[n]
    return None


# === CHECK 1: source_file in source-summary pages ===
ziliao_pages = glob.glob(os.path.join(WIKI, "资料", "*.md"))
ziliao_sources = {}
for zp in ziliao_pages:
    text = read_utf8(zp)
    m = re.search(r'^source_file:\s*"?\[\[([^\]]+)\]\]"?', text, re.MULTILINE)
    if not m:
        m = re.search(r"^source_file:\s*(.+)$", text, re.MULTILINE)
    if m:
        target = m.group(1).strip().strip('"')
        ziliao_sources[rel(zp)] = target
    else:
        issues.append(f"[1-资料] Missing source_file frontmatter: {rel(zp)}")

ziliao_broken = 0
for zp_name, target in ziliao_sources.items():
    resolved = resolve_wikilink(target)
    if resolved is None:
        issues.append(f"[1-资料] source_file target not found: {zp_name} -> {target}")
        ziliao_broken += 1

source_set = set(rel(f) for f in all_source_files + all_source_other)
referenced_sources = set()
for target in ziliao_sources.values():
    resolved = resolve_wikilink(target)
    if resolved:
        referenced_sources.add(rel(resolved))

uncovered = source_set - referenced_sources
for s in sorted(uncovered):
    issues.append(f"[1-资料] No ziliao page for: {s}")

# === CHECK 2: Broken wikilinks ===
total_links = 0
broken_set = []
seen_broken = set()
for wf in all_wiki_files:
    text = read_utf8(wf)
    links = extract_wikilinks(text)
    total_links += len(links)
    for link in links:
        clean = link.strip()
        resolved = resolve_wikilink(clean)
        if resolved is None:
            key = (rel(wf), clean)
            if key not in seen_broken:
                seen_broken.add(key)
                broken_set.append(key)

for wf_name, target in broken_set[:30]:
    issues.append(f"[2-链接] Broken: {wf_name} -> [[{target}]]")
if len(broken_set) > 30:
    issues.append(f"[2-链接] ... and {len(broken_set)-30} more broken links")

# === CHECK 3: Index coverage ===
index_text = read_utf8(INDEX)
index_links = extract_wikilinks(index_text)
index_targets_resolved = set()
for link in index_links:
    resolved = resolve_wikilink(link.strip())
    if resolved:
        index_targets_resolved.add(rel(resolved))

wiki_pages_no_ext = set()
for f in all_wiki_files:
    bn = os.path.basename(f)
    if bn in ("index.md", "log.md", "README.md"):
        continue
    wiki_pages_no_ext.add(rel(f))

missing_index = wiki_pages_no_ext - index_targets_resolved
for p in sorted(missing_index):
    issues.append(f"[3-索引] Not in index.md: {p}")

# === CHECK 4: UTF-8 ===
utf8_issues = [i for i in issues if i.startswith("[UTF-8]")]

# === SUMMARY ===
cat_counts = {}
for i in issues:
    cat = i.split("]")[0] + "]"
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

print("=" * 60)
print("Knowledge Wiki Verification Report")
print("=" * 60)
print(f"Knowledge root:        {BASE}")
print(f"Source files:          {len(source_set)}")
print(f"Ziliao pages:          {len(ziliao_pages)}")
print(f"Wiki total pages:      {len(all_wiki_files)}")
print(f"Wikilinks checked:     {total_links}")
print(f"Index references:      {len(index_links)}")
print()
print("CHECK 1 - Source coverage:")
print(f"  Ziliao->source broken refs: {ziliao_broken}/{len(ziliao_pages)}")
print(f"  Sources without ziliao:     {len(uncovered)}/{len(source_set)}")
print()
print(f"CHECK 2 - Broken wikilinks:   {len(broken_set)}/{total_links}")
print()
print("CHECK 3 - Index coverage:")
print(f"  Pages not in index.md:      {len(missing_index)}/{len(wiki_pages_no_ext)}")
print()
print(f"CHECK 4 - UTF-8 issues:       {len(utf8_issues)}")
print("-" * 60)

for cat, _count in cat_counts.items():
    sample = [i for i in issues if i.startswith(cat)][:5]
    print(f"\n{cat} ({cat_counts[cat]} total):")
    for s in sample:
        print(f"  {s}")
    if cat_counts[cat] > 5:
        print(f"  ... ({cat_counts[cat]-5} more)")

print("\n" + "=" * 60)
if not issues:
    print("ALL CHECKS PASSED")
else:
    print(f"TOTAL ISSUES: {len(issues)}")
    critical = len(uncovered) + len(broken_set) + len(missing_index) + len(utf8_issues)
    print(f"CRITICAL: {critical} items need attention")
print("=" * 60)
