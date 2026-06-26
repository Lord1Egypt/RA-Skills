"""
ChromaDB Semantic Search Provider
==================================

Wraps ChromaIntegration to implement the SemanticSearchProvider interface.
Enables HybridSearch to use ChromaDB for vector similarity search
without direct coupling.

Usage:
------
    from kb.framework.providers.chroma_provider import ChromaSemanticProvider

    provider = ChromaSemanticProvider(chroma_path="/path/to/chroma_db")
    if provider.is_available():
        results = provider.search("quantum computing", limit=10)
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

from ..exceptions import ChromaConnectionError, SearchError
from ..search_providers import ProviderResult
from ..text import parse_keywords

logger = logging.getLogger(__name__)


class ChromaSemanticProvider:
    """ChromaDB-backed semantic search provider.

    Wraps ChromaIntegration to satisfy the SemanticSearchProvider protocol.
    Uses sentence-transformers embeddings for vector similarity search.

    Args:
        chroma_path: Path to ChromaDB storage directory.
        collection_name: Name of the ChromaDB collection to query.
    """

    def __init__(
        self,
        chroma_path: Optional[str] = None,
        collection_name: str = "kb_sections",
    ):
        self._chroma_path = chroma_path
        self._collection_name = collection_name
        self._chroma = None
        self._chroma_error: Optional[ChromaConnectionError] = None
        self._available: Optional[bool] = None

    def _ensure_chroma(self):
        """Lazy-initialize ChromaIntegration."""
        if self._chroma is not None:
            return

        try:
            from ..chroma_integration import ChromaIntegration, get_chroma

            if self._chroma_path:
                self._chroma = get_chroma(chroma_path=self._chroma_path)
            else:
                self._chroma = get_chroma()
        except Exception as e:
            logger.warning(f"ChromaDB not available: {e}")
            self._chroma = None
            self._chroma_error = ChromaConnectionError(f"ChromaDB init failed: {e}")
            self._chroma_error.__cause__ = e

    def is_available(self) -> bool:
        """Check if ChromaDB is reachable and the collection exists."""
        if self._available is not None:
            return self._available

        try:
            self._ensure_chroma()
            if self._chroma is None:
                self._available = False
                return False

            # Try to access the collection
            collection = self._chroma.sections_collection
            self._available = collection is not None
        except Exception as e:
            logger.debug(f"ChromaDB availability check failed: {e}")
            self._available = False

        return self._available

    def search(self, query: str, limit: int = 20) -> List[ProviderResult]:
        """Search using ChromaDB vector similarity.

        Args:
            query: Natural language query string.
            limit: Maximum number of results.

        Returns:
            List of ProviderResult sorted by semantic relevance.
        """
        self._ensure_chroma()

        if self._chroma is None:
            logger.warning("ChromaDB not initialized, returning empty results")
            return []

        try:
            collection = self._chroma.sections_collection

            results = collection.query(
                query_texts=[query],
                n_results=limit,
                include=["metadatas", "distances"],
            )

            if not results or not results.get("ids") or not results["ids"][0]:
                return []

            search_results = []
            ids = results["ids"][0]
            distances = results.get("distances", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]

            for i, section_id in enumerate(ids):
                distance = distances[i] if i < len(distances) else 0.0
                # ChromaDB cosine distance: 0 = perfect match, 2 = opposite
                # Convert to similarity score: higher = better
                semantic_score = max(0.0, 1.0 - distance)

                metadata = metadatas[i] if i < len(metadatas) else {}

                # Parse keywords from metadata
                keywords_str = metadata.get("keywords", "[]")
                keywords = parse_keywords(keywords_str)

                search_results.append(ProviderResult(
                    section_id=str(section_id),
                    content=metadata.get("content_preview", ""),
                    score=semantic_score,
                    source="chroma",
                    metadata=metadata,
                    file_id=metadata.get("file_id", ""),
                    file_path=metadata.get("file_path", ""),
                    section_header=metadata.get("section_header", ""),
                    importance_score=float(metadata.get("importance_score", 0.5)),
                    keywords=keywords,
                ))

            return search_results

        except Exception as e:
            logger.error(f"ChromaDB search failed: {e}")
            self._last_search_error = SearchError(f"ChromaDB search failed: {e}")
            self._last_search_error.__cause__ = e
            return []