#!/usr/bin/env python3
"""
Domain Classifier
=================
Domain taxonomy and classification for dream consolidation.

Maps memory text to semantic domains (technical, personal, creative, etc.)
and provides keyword extraction utilities.

Author: Lilu / nima-core
"""

from __future__ import annotations

import re
from typing import Dict, List
from collections import Counter

__all__ = [
    "DOMAINS",
    "classify_domain",
    "extract_keywords",
]


# ── Domain taxonomy (same as lilu_core) ──────────────────────────────────────

DOMAINS: Dict[str, List[str]] = {
    "technical":     ["code", "system", "algorithm", "architecture", "api",
                      "database", "nima", "memory", "deploy", "server", "bug"],
    "personal":      ["family", "children", "home", "life", "feeling",
                      "emotion", "friend", "myself", "my"],
    "creative":      ["idea", "design", "art", "story", "imagination",
                      "dream", "write", "create", "build"],
    "philosophical": ["meaning", "purpose", "consciousness", "existence",
                      "truth", "believe", "why", "soul"],
    "practical":     ["task", "todo", "plan", "schedule", "project",
                      "work", "deadline", "done", "finish"],
    "relational":    ["relationship", "trust", "love", "connect", "care",
                      "share", "talk", "together"],
}


# ── Classification functions ──────────────────────────────────────────────────

def classify_domain(text: str) -> List[str]:
    """Return all matching domains for a text fragment."""
    t = text.lower()
    matched = [d for d, kws in DOMAINS.items() if any(kw in t for kw in kws)]
    return matched if matched else ["general"]


def extract_keywords(texts: List[str], top_n: int = 12) -> List[str]:
    """Extract the most common keywords from a list of texts, excluding stopwords."""
    stop = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
        "for", "of", "with", "is", "was", "are", "be", "been", "i",
        "you", "it", "this", "that", "my", "me", "we", "they", "have",
        "has", "had", "not", "so", "just", "can", "will", "do", "did",
    }
    counts: Counter = Counter()
    for text in texts:
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        counts.update(w for w in words if w not in stop)
    return [w for w, _ in counts.most_common(top_n)]
