"""Hybrid search with RRF (Reciprocal Rank Fusion)."""

from __future__ import annotations

from lucid_skill.semantic.embedder import Embedder
from lucid_skill.semantic.index import SemanticIndex

# Module-level embedding cache: key = "sourceId::tableName", value = vector bytes
_embedding_cache: dict[str, bytes] = {}


def load_embedding_cache(catalog) -> None:
    """Load all embeddings from the catalog into the in-memory cache."""
    global _embedding_cache
    _embedding_cache.clear()
    rows = catalog.get_all_embeddings()
    for row in rows:
        key = f"{row['source_id']}::{row['table_name']}"
        _embedding_cache[key] = row["vector"]


def update_cache_entry(source_id: str, table_name: str, vector: bytes) -> None:
    """Update a single entry in the embedding cache."""
    key = f"{source_id}::{table_name}"
    _embedding_cache[key] = vector


def hybrid_search(
    query: str,
    catalog,
    semantic_index: SemanticIndex,
    embedder: Embedder,
    top_k: int = 5,
) -> list[dict]:
    """Perform hybrid search combining BM25/LIKE and embedding similarity with RRF fusion.

    Args:
        query: Search query string.
        catalog: Catalog instance for embedding retrieval.
        semantic_index: SemanticIndex instance for text-based search.
        embedder: Embedder instance for vector similarity.
        top_k: Number of results to return.

    Returns:
        List of dicts with source_id, table_name, and score.
    """
    k = 60  # RRF constant

    # ── Path 1: BM25/LIKE search ──
    bm25_results = semantic_index.search(query, top_k=10000)
    bm25_scores: dict[str, float] = {}
    for rank_idx, result in enumerate(bm25_results):
        key = f"{result['source_id']}::{result['table_name']}"
        bm25_scores[key] = 1.0 / (k + rank_idx + 1)

    # ── Path 2: Embedding similarity ──
    embed_scores: dict[str, float] = {}
    if embedder.is_ready() and _embedding_cache:
        try:
            query_vector = embedder.embed(query)
            similarities: list[tuple[str, float]] = []
            for cache_key, cached_vector in _embedding_cache.items():
                sim = Embedder.cosine_similarity(query_vector, cached_vector)
                similarities.append((cache_key, sim))
            # Sort by similarity descending
            similarities.sort(key=lambda x: -x[1])
            for rank_idx, (cache_key, _sim) in enumerate(similarities):
                embed_scores[cache_key] = 1.0 / (k + rank_idx + 1)
        except Exception:
            pass

    # ── RRF Fusion ──
    all_keys = set(bm25_scores.keys()) | set(embed_scores.keys())
    fused: list[tuple[str, float]] = []
    for key in all_keys:
        score = bm25_scores.get(key, 0.0) + embed_scores.get(key, 0.0)
        fused.append((key, score))

    fused.sort(key=lambda x: -x[1])

    results = []
    for key, score in fused[:top_k]:
        source_id, table_name = key.split("::", 1)
        results.append({
            "source_id": source_id,
            "table_name": table_name,
            "score": score,
        })

    return results
