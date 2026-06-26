"""
Search Providers for KB Framework
===================================

Concrete implementations of search provider interfaces.

Providers:
-----------
- ChromaSemanticProvider: Vector similarity search via ChromaDB
- FTS5KeywordProvider: BM25/keyword search via SQLite FTS5

Usage:
------
    from kb.framework.providers import ChromaSemanticProvider, FTS5KeywordProvider

    semantic = ChromaSemanticProvider(chroma_path="/path/to/chroma")
    keyword = FTS5KeywordProvider(db_path=Path("/path/to/biblio.db"))

    results = semantic.search("quantum computing", limit=10)
    results = keyword.search("methylierung", limit=10)
"""

from .chroma_provider import ChromaSemanticProvider
from .fts5_provider import FTS5KeywordProvider

__all__ = [
    "ChromaSemanticProvider",
    "FTS5KeywordProvider",
]


def get_semantic_provider(chroma_path=None) -> ChromaSemanticProvider:
    """Factory: create a semantic search provider (ChromaDB)."""
    kwargs = {}
    if chroma_path:
        kwargs["chroma_path"] = chroma_path
    return ChromaSemanticProvider(**kwargs)


def get_keyword_provider(db_path=None) -> FTS5KeywordProvider:
    """Factory: create a keyword search provider (FTS5)."""
    from pathlib import Path
    kwargs = {}
    if db_path:
        kwargs["db_path"] = Path(db_path)
    return FTS5KeywordProvider(**kwargs)