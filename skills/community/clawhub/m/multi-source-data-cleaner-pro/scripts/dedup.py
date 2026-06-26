"""Fuzzy deduplication using blocking + simple similarity."""
from __future__ import annotations
from typing import Any, Dict, List
from difflib import SequenceMatcher


def similarity(a: str, b: str) -> float:
    if not a or not b: return 0.0
    return SequenceMatcher(None, a, b).ratio()


def dedup(rows: List[Dict[str, Any]], keys: List[str], threshold: float = 0.85) -> Dict[str, Any]:
    groups: List[List[int]] = []
    assigned = [-1] * len(rows)
    for i, r in enumerate(rows):
        if assigned[i] != -1: continue
        group = [i]
        for j in range(i + 1, len(rows)):
            if assigned[j] != -1: continue
            sims = [similarity(str(r.get(k, "")), str(rows[j].get(k, ""))) for k in keys]
            if sims and sum(sims) / len(sims) >= threshold:
                group.append(j); assigned[j] = len(groups)
        assigned[i] = len(groups)
        groups.append(group)

    canonical = [rows[g[0]] for g in groups]
    return {
        "deduplicated_rows": canonical,
        "merge_groups": [g for g in groups if len(g) > 1],
        "input_count": len(rows),
        "output_count": len(canonical),
        "duplicate_pairs_removed": len(rows) - len(canonical),
    }
