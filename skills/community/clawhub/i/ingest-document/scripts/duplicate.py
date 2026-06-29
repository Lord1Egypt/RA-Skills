from __future__ import annotations

import difflib

from utils import normalize_for_match

COMMON_MODULE_VERSION = "paperkb-v3.0"


def find_duplicate(catalog: dict, title: str, source_id: str = "", source_path: str = "") -> dict:
    norm = normalize_for_match(title)
    best = None
    best_score = 0.0
    for doc in catalog.get("documents", []):
        if source_id and source_path and doc.get("source_id") == source_id and doc.get("source_path") == source_path:
            return {"duplicate": True, "match_type": "same_source_path", "existing": doc}
        if normalize_for_match(doc.get("title", "")) == norm:
            return {"duplicate": True, "match_type": "title", "existing": doc}
        score = difflib.SequenceMatcher(None, norm, normalize_for_match(doc.get("title", ""))).ratio()
        if score > best_score:
            best, best_score = doc, score
    if best and best_score > 0.92:
        return {"duplicate": False, "possible_duplicate": True, "similarity": round(best_score, 3), "existing": best}
    return {"duplicate": False}
