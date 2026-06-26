"""Search facade for the semantic layer."""

from __future__ import annotations

from lucid_skill.semantic.index import SemanticIndex
from lucid_skill.semantic.layer import read_table_semantic


def search_tables(
    index: SemanticIndex,
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """Search for tables matching a query, enriching results with semantic metadata.

    Args:
        index: SemanticIndex instance to search against.
        query: Search query string.
        top_k: Maximum number of results to return.

    Returns:
        List of SearchResult dicts with source_id, table_name, rank, and semantic.
    """
    results = index.search(query, top_k=top_k)
    enriched = []
    for result in results:
        semantic = read_table_semantic(result["source_id"], result["table_name"])
        enriched.append({
            "source_id": result["source_id"],
            "table_name": result["table_name"],
            "rank": result["rank"],
            "semantic": semantic,
        })
    return enriched
