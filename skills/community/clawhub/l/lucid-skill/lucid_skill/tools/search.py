"""search_tables tool handler."""

from __future__ import annotations

import json
from typing import Any

from lucid_skill.catalog.store import CatalogStore
from lucid_skill.semantic.embedder import Embedder
from lucid_skill.semantic.hybrid import hybrid_search
from lucid_skill.semantic.index import SemanticIndex
from lucid_skill.semantic.layer import read_table_semantic
from lucid_skill.semantic.search import search_tables


def handle_search_tables(
    params: dict[str, Any],
    index: SemanticIndex,
    catalog: CatalogStore | None = None,
    embedder: Embedder | None = None,
) -> str:
    """Search tables using hybrid (BM25 + embedding) or BM25-only search.

    Returns matching tables with full semantic info including relations,
    suggestedJoins, metrics, and suggestedMetricSqls.
    """
    query: str | None = params.get("query")
    top_k = int(params.get("top_k") or params.get("topK") or 5)

    if not query:
        raise ValueError("query is required")

    results: list[dict[str, Any]]

    if embedder and catalog:
        # Hybrid search: BM25 + embedding with RRF fusion
        hybrid_results = hybrid_search(query, catalog, index, embedder, top_k)
        results = [
            {
                "source_id": r["source_id"],
                "table_name": r["table_name"],
                "rank": -r["score"],  # Negative so higher score = lower (better) rank
                "semantic": read_table_semantic(r["source_id"], r["table_name"]),
            }
            for r in hybrid_results
        ]
    else:
        # BM25-only fallback
        results = search_tables(index, query, top_k)

    if len(results) == 0:
        return json.dumps({
            "message": (
                f'No tables found matching "{query}". Try different keywords, '
                "or check if semantic layer has been initialized "
                "(call init_semantic + update_semantic first)."
            ),
            "results": [],
        })

    def _format_result(r: dict[str, Any]) -> dict[str, Any]:
        semantic = r.get("semantic")

        relations = None
        suggested_joins: list[str] = []
        if semantic and semantic.relations:
            relations = [
                {
                    "targetTable": rel.target_table,
                    "joinCondition": rel.join_condition,
                    "relationType": rel.relation_type,
                }
                for rel in semantic.relations
            ]
            suggested_joins = [
                f"JOIN {rel.target_table} ON {rel.join_condition}"
                for rel in semantic.relations
            ]

        suggested_metric_sqls: list[dict[str, str]] = []
        metrics = None
        if semantic and semantic.metrics:
            metrics = [
                {
                    "name": m.name,
                    "expression": m.expression,
                    "group_by": m.group_by,
                    "filter": m.filter,
                }
                for m in semantic.metrics
            ]
            suggested_metric_sqls = []
            for m in semantic.metrics:
                group_by_clause = f" GROUP BY {m.group_by}" if m.group_by else ""
                select_cols = f"{m.group_by}, " if m.group_by else ""
                suggested_metric_sqls.append({
                    "name": m.name,
                    "sql": (
                        f"SELECT {select_cols}{m.expression} AS {m.name} "
                        f"FROM {r['table_name']}{group_by_clause}"
                    ),
                })

        columns = None
        if semantic and semantic.columns:
            columns = [
                {
                    "name": c.name,
                    "semantic": c.semantic,
                    "role": c.role,
                    "unit": c.unit,
                }
                for c in semantic.columns
            ]

        return {
            "sourceId": r["source_id"],
            "tableName": r["table_name"],
            "relevanceRank": r["rank"],
            "description": semantic.description if semantic else None,
            "businessDomain": semantic.business_domain if semantic else None,
            "tags": semantic.tags if semantic else None,
            "columns": columns,
            "relations": relations,
            "suggestedJoins": suggested_joins,
            "metrics": metrics,
            "suggestedMetricSqls": suggested_metric_sqls,
        }

    return json.dumps(
        {
            "message": f'Found {len(results)} table(s) matching "{query}"',
            "results": [_format_result(r) for r in results],
        },
        indent=2,
        default=str,
    )
