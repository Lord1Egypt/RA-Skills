"""
Semantic Search Implementation
================================

ChromaDB-based semantic search function.
"""

import logging
from typing import Optional

from ..text import parse_keywords

# Logging
logger = logging.getLogger(__name__)


def _semantic_search(
    query: str,
    limit: int = 100,
    semantic_provider=None,
    chroma=None,
) -> list[dict]:
    """
    Semantic search — delegates to provider if available, else ChromaDB.

    Args:
        query: Natural language query
        limit: Max results
        semantic_provider: Optional SemanticSearchProvider (Protocol)
        chroma: ChromaIntegration instance (legacy path)

    Returns:
        List of results with scores
    """
    # DG-2: Use injected provider if available
    if semantic_provider is not None:
        try:
            provider_results = semantic_provider.search(query, limit)
            # Convert SearchResult to dict for compatibility with _merge_and_rank
            return [
                {
                    "section_id": r.section_id,
                    "semantic_score": r.score,
                    "file_id": r.file_id,
                    "file_path": r.file_path,
                    "section_header": r.section_header,
                    "importance_score": r.importance_score,
                    "keywords": r.keywords,
                    "content_preview": r.metadata.get("content_preview", r.content[:200]),
                    "content_full": r.content,
                }
                for r in provider_results
            ]
        except (KeyError, ValueError, AttributeError) as e:
            logger.warning(f"Semantic provider search failed: {e}")
            return []

    # No provider: check if ChromaDB is available
    if chroma is None:
        logger.debug("No semantic provider and no ChromaDB — semantic search disabled")
        return []

    # Legacy ChromaDB path
    collection = chroma.sections_collection

    try:
        results = collection.query(
            query_texts=[query],
            n_results=limit,
            include=["metadatas", "distances"]
        )
    except (ValueError, RuntimeError) as e:
        logger.warning(f"ChromaDB query failed: {e}")
        return []

    search_results = []

    if not results or not results['ids']:
        return []

    for i, section_id in enumerate(results['ids'][0]):
        # Distance to similarity (ChromaDB: cosine distance, 0 = perfect)
        distance = results['distances'][0][i] if results['distances'] else 0.0
        semantic_score = max(0.0, 1.0 - distance)  # Convert to similarity

        metadata = results['metadatas'][0][i] if results['metadatas'] else {}

        search_results.append({
            "section_id": section_id,
            "semantic_score": semantic_score,
            "file_id": metadata.get("file_id", ""),
            "file_path": metadata.get("file_path", ""),
            "section_header": metadata.get("section_header", ""),
            "importance_score": metadata.get("importance_score", 0.5),
            "keywords": parse_keywords(metadata.get("keywords", "[]"))
        })

    return search_results