"""Adapter for the Claude Code auto-memory format.

Layout (as used by ~/.claude/.../memory/):
  - one .md file per memory, with YAML frontmatter:
        ---
        name: <slug>
        description: <one line>
        metadata:
          type: user | feedback | project | reference
          node_type: memory
        ---
        <markdown body, may contain [[wiki-links]]>
  - MEMORY.md: an index, one line per memory:
        - [slug](file.md) — hook

This adapter is intentionally tolerant: real stores have hand-edited files, so a
malformed frontmatter must degrade (best-effort fields) rather than crash.
"""

from __future__ import annotations

import os
import re

from ..model import IndexEntry, MemoryStore, MemUnit

INDEX_FILE = "MEMORY.md"
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
# `- [slug](target.md) — hook`  (em dash, en dash or hyphen as separator)
INDEX_LINE_RE = re.compile(r"^\s*[-*]\s*\[([^\]]+)\]\(([^)]+)\)\s*(?:[—–-]\s*(.*))?$")


def _split_frontmatter(text: str):
    """Return (frontmatter_text, body). Frontmatter is the block between the first
    pair of `---` fences at the top of the file; absent -> ('', text)."""
    if not text.startswith("---"):
        return "", text
    lines = text.splitlines(keepends=True)
    # find the closing fence after line 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[1:i]), "".join(lines[i + 1:])
    return "", text  # unterminated fence -> treat as no frontmatter


def _parse_frontmatter(fm_text: str) -> dict:
    """Minimal YAML-subset parser: top-level `key: value` plus one level of
    2-space-indented nesting (enough for the `metadata:` block). No external deps."""
    data: dict = {}
    current_parent = None
    for raw in fm_text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if indent == 0:
            if val == "":           # a parent like `metadata:`
                current_parent = {}
                data[key] = current_parent
            else:
                data[key] = val
                current_parent = None
        else:                       # nested under the last parent
            if current_parent is not None:
                current_parent[key] = val
    return data


class AutoMemoryAdapter:
    name = "auto-memory"

    def load(self, root: str) -> MemoryStore:
        store = MemoryStore(root=root, fmt=self.name)
        index_path = os.path.join(root, INDEX_FILE)
        store.index_path = index_path

        for entry in sorted(os.listdir(root)):
            if not entry.endswith(".md") or entry == INDEX_FILE:
                continue
            path = os.path.join(root, entry)
            if not os.path.isfile(path):
                continue
            store.units.append(self._parse_file(path, entry))

        if os.path.isfile(index_path):
            store.index = self._parse_index(index_path)
        return store

    def _parse_file(self, path: str, filename: str) -> MemUnit:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm_text, body = _split_frontmatter(text)
        fm = _parse_frontmatter(fm_text)
        meta = fm.get("metadata", {}) if isinstance(fm.get("metadata"), dict) else {}

        slug = fm.get("name") or os.path.splitext(filename)[0]
        links = sorted(set(m.group(1).strip() for m in WIKILINK_RE.finditer(body)))
        return MemUnit(
            id=slug,
            gist=fm.get("description", "").strip(),
            body=body.strip(),
            path=path,
            type=meta.get("type", "unknown"),
            links=links,
            mtime=os.path.getmtime(path),
            raw_frontmatter=fm,
        )

    def _parse_index(self, path: str) -> list[IndexEntry]:
        entries = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = INDEX_LINE_RE.match(line.rstrip("\n"))
                if m:
                    entries.append(IndexEntry(
                        id=m.group(1).strip(),
                        target=m.group(2).strip(),
                        hook=(m.group(3) or "").strip(),
                    ))
        return entries
