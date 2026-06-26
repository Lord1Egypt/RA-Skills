from __future__ import annotations

import re

_ARXIV_PATTERNS = [
    re.compile(r"arxiv\s*[:：]?\s*(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE),
    re.compile(r"\b(\d{4}\.\d{4,5})(?:v\d+)?\b"),
]


def sort_arxiv_ids(ids: set[str] | list[str]) -> list[str]:
    return sorted(set(ids), key=lambda x: (x[:4], int(x[5:])))


def extract_arxiv_ids_from_text(text: str) -> list[str]:
    found: set[str] = set()
    for pattern in _ARXIV_PATTERNS:
        found.update(match.group(1) for match in pattern.finditer(text))
    return sort_arxiv_ids(found)
