"""Adapter for the mneme format (https://github.com/.../mneme) — Casper's plain-text
memory format for LLM agents.

A `.mneme` / `.mn` file is a sequence of cells separated by blank lines:

    @ DEC-0042  storage/cache
    gist  Local cache uses SQLite instead of JSON files
    state live   conf high   since 2026-06-03   seen 2026-06-03
    cue   concurrent writes / cache corruption / slow queries
    > rationale / cost / context (may span lines)
    link  supersedes DEC-0031

Key differences from auto-memory that this adapter normalizes for the unified report:
  - the spine is *derived*, never a persisted file → store.has_index = False
    (so memory-doctor must not report "index drift" / index-based orphans here).
  - each cell carries `state` and `seen` → freshness uses `seen` (the real decay signal),
    and history states (superseded/retired/proposed) are excluded from "active" health.
  - links are typed (relation, target) → kept in rel_links for supersede-symmetry checks.

Parsing is deliberately tolerant (mirrors mneme's own tool): the line-head key is the
anchor, unknown lines are ignored, missing fields take defaults.
"""

from __future__ import annotations

import datetime as _dt
import os
import re

from ..model import MemoryStore, MemUnit

HEAD_RE = re.compile(r"@\s+(\S+)\s*(\S+)?")
STATUS_KEYS = {"state", "conf", "since", "seen"}
# ID prefix -> freshness bucket (reuses report's HALFLIFE_DAYS keys)
PREFIX_BUCKET = {
    "PREF": "user", "FACT": "reference", "GOTCHA": "reference",
    "DEC": "project", "OKR": "project", "TODO": "project",
}


def _bucket(cell_id: str) -> str:
    prefix = cell_id.split("-", 1)[0].upper()
    return PREFIX_BUCKET.get(prefix, "unknown")


def _seen_epoch(seen: str) -> float:
    try:
        d = _dt.date.fromisoformat(seen)
        return _dt.datetime(d.year, d.month, d.day).timestamp()
    except (ValueError, TypeError):
        return 0.0


def _parse_cells(text: str) -> list[dict]:
    cells, cur = [], None
    body_lines: list[str] = []

    def flush():
        if cur is not None:
            cur["body"] = "\n".join(body_lines).strip()
            cells.append(cur)

    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if line.startswith("#"):
            continue
        if line.startswith("@"):
            flush()
            m = HEAD_RE.match(line)
            cur = {"id": (m.group(1) if m else line[1:].strip()),
                   "topic": (m.group(2) if (m and m.group(2)) else ""),
                   "links": [], "rel_links": []}
            body_lines = []
            continue
        if cur is None:
            continue
        if line.startswith(">"):
            body_lines.append(line[1:].strip())
            continue
        if not line.strip():
            continue
        toks = line.split()
        i = 0
        while i < len(toks):
            k = toks[i]
            if k in STATUS_KEYS and i + 1 < len(toks):
                cur[k] = toks[i + 1]
                i += 2
                continue
            if k in ("gist", "cue"):
                cur[k] = line.split(None, 1)[1] if len(toks) > 1 else ""
                break
            if k == "link" and len(toks) >= 3:
                cur["rel_links"].append((toks[1], toks[2]))
                cur["links"].append(toks[2])
                break
            i += 1
    flush()
    return cells


class MnemeAdapter:
    name = "mneme"
    extensions = (".mneme", ".mn")

    def load(self, root: str) -> MemoryStore:
        store = MemoryStore(root=root, fmt=self.name, has_index=False)
        for entry in sorted(os.listdir(root)):
            if entry.endswith(self.extensions):
                path = os.path.join(root, entry)
                if os.path.isfile(path):
                    store.units.extend(self._parse_file(path))
        return store

    def _parse_file(self, path: str) -> list[MemUnit]:
        with open(path, encoding="utf-8") as f:
            cells = _parse_cells(f.read())
        file_mtime = os.path.getmtime(path)
        units = []
        for c in cells:
            seen_epoch = _seen_epoch(c.get("seen", "")) or file_mtime
            units.append(MemUnit(
                id=c["id"],
                gist=c.get("gist", "").strip(),
                body=c.get("body", ""),
                path=path,
                type=_bucket(c["id"]),
                state=c.get("state", "live"),
                conf=c.get("conf", "med"),
                links=c["links"],
                rel_links=c["rel_links"],
                topic=c.get("topic", ""),
                mtime=seen_epoch,
            ))
        return units
