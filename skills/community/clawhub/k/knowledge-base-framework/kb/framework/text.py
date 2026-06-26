"""
KB Text Utilities
================

Text formatting and parsing utilities for the knowledge base library.
"""

import json
from typing import List


def build_embedding_text(
    header: str,
    content: str,
    keywords: List[str]
) -> str:
    """
    Builds optimal text for embedding.

    Structure:
    - Header as title (high weight via repetition)
    - Content preview (first 500 chars)
    - Keywords as bonus context

    Args:
        header: Section header/title
        content: Section content
        keywords: List of keywords to boost relevance

    Returns:
        Formatted text optimized for embedding
    """
    parts = []

    # Header bekommt.extra Weight durch Repetition
    if header:
        parts.append(header)
        parts.append(header)  # Doppelte Gewichtung

    # Content Preview (begrenzt für Performance)
    if content:
        preview = content[:500].strip()
        parts.append(preview)

    # Keywords als Kontext
    if keywords:
        parts.append(" ".join(keywords[:10]))

    return " | ".join(parts)


def parse_keywords(keywords_str: str) -> List[str]:
    """Parse keywords from a JSON string (with comma-separated fallback).

    Handles both JSON arrays and comma-separated strings, as the DB
    contains ~2,353 rows with comma-separated keywords.
    """
    if not keywords_str or keywords_str.strip() in ('', 'null', '[]'):
        return []
    try:
        return json.loads(keywords_str)
    except (json.JSONDecodeError, TypeError):
        return [k.strip() for k in keywords_str.split(',') if k.strip()]