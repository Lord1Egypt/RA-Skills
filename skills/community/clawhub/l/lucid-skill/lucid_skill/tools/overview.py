"""get_overview tool handler."""

from __future__ import annotations

import json

from lucid_skill.catalog.store import CatalogStore
from lucid_skill.semantic.index import SemanticIndex
from lucid_skill.tools.connect import get_connectors


def handle_get_overview(
    catalog: CatalogStore,
    semantic_index: SemanticIndex,
) -> str:
    """Return a snapshot of all connected sources, tables, and semantic layer status."""
    sources = catalog.get_sources()
    active_connector_ids = set(get_connectors().keys())

    source_list = []
    for s in sources:
        tables = catalog.get_tables(s["id"])
        source_list.append({
            "sourceId": s["id"],
            "type": s["type"],
            "connected": s["id"] in active_connector_ids,
            "tables": [
                {
                    "name": t["table_name"],
                    "rowCount": t["row_count"],
                    "columnCount": t["column_count"],
                    "semanticStatus": t["semantic_status"],
                }
                for t in tables
            ],
        })

    total_tables = sum(len(s["tables"]) for s in source_list)
    semantic_indexed_count = semantic_index.count()

    return json.dumps(
        {
            "sources": source_list,
            "summary": {
                "totalSources": len(source_list),
                "activeSources": sum(1 for s in source_list if s["connected"]),
                "totalTables": total_tables,
                "semanticIndexedTables": semantic_indexed_count,
            },
        },
        indent=2,
    )
