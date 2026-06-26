"""
Search Provider Interfaces for KB Framework
=============================================

Defines the abstract interfaces (Protocols) for search providers,
enabling decoupled architecture where HybridSearch can work with
different backends (ChromaDB, SQLite FTS5, TF-IDF, etc.).

Architecture:
-------------
    ┌─────────────────────┐
    │   SearchProvider    │
    │     (Protocol)      │
    └──────────┬──────────┘
               │
              ┌┼────────────────┐
              │                 │
    ┌─────────▼─────────┐  ┌──▼──────────────┐
    │ SemanticSearch     │  │ KeywordSearch   │
    │   Provider         │  │   Provider      │
    │   (Protocol)        │  │   (Protocol)    │
    └─────────┬─────────┘  └──┬──────────────┘
              │                 │
     ┌────────▼────────┐  ┌───▼─────────────┐
     │ChromaSemantic   │  │SQLiteFTS5        │
     │  Provider       │  │  Provider        │
     └─────────────────┘  └──────────────────┘

Usage:
------
    from kb.framework.search_providers import (
        ProviderResult, SemanticSearchProvider, KeywordSearchProvider
    )

    # Type checking works with Protocol
    def search_with(provider: SemanticSearchProvider):
        results = provider.search("quantum computing", limit=10)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, Optional, List


@dataclass
class ProviderResult:
    """Single search result from any search provider.

    Compatible with hybrid_search.SearchResult but simplified
    for the provider interface.
    """
    section_id: str
    content: str
    score: float
    source: str  # "chroma", "fts5", "tfidf", "hybrid"
    metadata: dict = field(default_factory=dict)

    # Optional fields for richer results
    file_id: str = ""
    file_path: str = ""
    section_header: str = ""
    importance_score: float = 0.5
    keywords: List[str] = field(default_factory=list)


@runtime_checkable
class SemanticSearchProvider(Protocol):
    """Interface for semantic/vector search providers.

    Implementations: ChromaSemanticProvider, TFIDFSemanticProvider
    """

    def search(self, query: str, limit: int = 20) -> List[ProviderResult]:
        """Search using embeddings/vector similarity.

        Args:
            query: Natural language query string.
            limit: Maximum number of results to return.

        Returns:
            List of ProviderResult sorted by relevance (best first).
        """
        ...

    def is_available(self) -> bool:
        """Check if the semantic search backend is available.

        Returns:
            True if the provider can accept search requests.
        """
        ...


@runtime_checkable
class KeywordSearchProvider(Protocol):
    """Interface for keyword/BM25 search providers.

    Implementations: FTS5KeywordProvider
    """

    def search(self, query: str, limit: int = 20) -> List[ProviderResult]:
        """Search using keyword matching (BM25, LIKE, etc.).

        Args:
            query: Keyword query string.
            limit: Maximum number of results to return.

        Returns:
            List of ProviderResult sorted by relevance (best first).
        """
        ...

    def is_available(self) -> bool:
        """Check if the keyword search backend is available.

        Returns:
            True if the provider can accept search requests.
        """
        ...