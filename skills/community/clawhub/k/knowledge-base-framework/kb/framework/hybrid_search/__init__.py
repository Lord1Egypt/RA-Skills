"""
Hybrid Search for Knowledge Base
=================================

Phase 1: Vector Search Foundation
Combines SQLite (Keywords) + ChromaDB (Vector) search.

Unified Query Interface for:
- Semantic similarity search (ChromaDB)
- Keyword/LIKE search (SQLite)
- Importance score ranking

Source: KB_Erweiterungs_Plan.md (Phase 1)
"""

# Re-export all public symbols for backward compatibility
from .models import SearchResult, SearchConfig
from .engine import HybridSearch, get_search, search
from .keyword import _keyword_search_fts, _keyword_search
from .semantic import _semantic_search
from .filters import search_with_filters

__all__ = [
    "HybridSearch",
    "SearchResult",
    "SearchConfig",
    "get_search",
    "search",
    "_keyword_search_fts",
    "_keyword_search",
    "_semantic_search",
    "search_with_filters",
]