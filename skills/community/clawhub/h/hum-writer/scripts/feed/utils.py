"""
utils.py — Shared utilities for the feed pipeline.
"""

STOPWORDS: frozenset[str] = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "it", "its", "was", "are", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "not", "this", "that", "these",
    "those", "we", "i", "you", "he", "she", "they", "our", "my", "your",
    "his", "her", "their", "all", "from", "by", "as", "up", "if", "so", "no",
    "more", "just", "now", "like", "also", "here", "about", "out", "into",
    "how", "what", "why", "when", "where", "who", "which", "than", "then",
    "each", "some", "any", "re", "new", "over", "after", "before", "per",
    "via", "vs", "said", "says", "were", "your",
})


def parse_likes(likes_str) -> int:
    """Parse a human-readable like/view count string into an integer.

    Handles suffixes: K (thousands), M (millions).
    Returns 0 on any parse failure.
    """
    if isinstance(likes_str, int):
        return likes_str
    s = str(likes_str).strip().upper().replace(",", "")
    try:
        if s.endswith("K"):
            return int(float(s[:-1]) * 1_000)
        if s.endswith("M"):
            return int(float(s[:-1]) * 1_000_000)
        return int(s)
    except (ValueError, AttributeError):
        return 0
