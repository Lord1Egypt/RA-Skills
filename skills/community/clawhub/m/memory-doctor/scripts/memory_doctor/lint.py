"""Deterministic, safe repairs (v0.1).

Only index reconciliation: the MEMORY.md index drifts constantly (new memory files
added without an index line, or stale lines pointing at deleted files). Reconciliation
is 100% deterministic and reversible, so it is the one auto-fix v0.1 performs.

Deliberately NOT auto-fixed in v0.1 (flagged in `report` instead, fixed in v0.2):
  - dead [[links]]   (removing them could lose intent)
  - duplicates       (merge needs an LLM judge)
  - oversized        (compaction needs an LLM + a fact-diff guardrail)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from .model import IndexEntry, MemoryStore


@dataclass
class IndexPlan:
    keep: list = field(default_factory=list)      # existing IndexEntry kept as-is
    add: list = field(default_factory=list)       # new IndexEntry to append
    remove: list = field(default_factory=list)    # IndexEntry dropped (dangling)

    @property
    def changed(self) -> bool:
        return bool(self.add or self.remove)


def plan_index(store: MemoryStore) -> IndexPlan:
    plan = IndexPlan()
    ids = {u.id for u in store.units}
    files = {os.path.basename(u.path): u for u in store.units}

    # keep valid existing entries (preserve their hand-written hooks & order); drop dangling
    indexed = set()
    for e in store.index:
        if e.target in files or e.id in ids:
            plan.keep.append(e)
            indexed.add(e.id)
        else:
            plan.remove.append(e)

    # append units that have no index line yet, sorted for stable output
    for u in sorted(store.units, key=lambda x: x.id):
        if u.id not in indexed:
            plan.add.append(IndexEntry(
                id=u.id,
                target=os.path.basename(u.path),
                hook=u.gist or "",
            ))
    return plan


def render_index(plan: IndexPlan) -> str:
    lines = []
    for e in plan.keep + plan.add:
        hook = f" — {e.hook}" if e.hook else ""
        lines.append(f"- [{e.id}]({e.target}){hook}")
    return "\n".join(lines) + "\n"


def apply_index(store: MemoryStore, plan: IndexPlan) -> None:
    path = store.index_path or os.path.join(store.root, "MEMORY.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_index(plan))
