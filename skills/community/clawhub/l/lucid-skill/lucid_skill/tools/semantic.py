"""init_semantic / update_semantic tool handlers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from lucid_skill.catalog.store import CatalogStore
from lucid_skill.query.engine import QueryEngine
from lucid_skill.semantic.embedder import Embedder
from lucid_skill.semantic.index import SemanticIndex
from lucid_skill.semantic.layer import write_table_semantic
from lucid_skill.tools.connect import get_connectors
from lucid_skill.types import (
    ColumnSemantic,
    MetricDefinition,
    RelationSemantic,
    TableSemantic,
)


def _default_serializer(obj: object) -> str:
    """Handle non-serializable types (e.g. Decimal, date, bytes)."""
    return str(obj)


def handle_init_semantic(
    params: dict[str, Any],
    catalog: CatalogStore,
    engine: QueryEngine,
) -> str:
    """Return all connected table schemas, sample data, and FK info
    in a format optimized for the host Agent to infer business semantics.
    """
    filter_source_id: str | None = params.get("source_id") or params.get("sourceId")
    sample_rows = int(params.get("sample_rows") or params.get("sampleRows") or 5)

    all_tables = catalog.get_tables(filter_source_id)

    if len(all_tables) == 0:
        return json.dumps({
            "message": "No tables found. Please connect a data source first using connect_source.",
            "tables": [],
        })

    result: list[dict[str, Any]] = []

    for table_meta in all_tables:
        columns = catalog.get_columns(table_meta["source_id"], table_meta["table_name"])

        # Get sample data from DuckDB
        sample_data: list[dict[str, Any]] = []
        try:
            sample_data = engine.execute_raw(
                f'SELECT * FROM "{table_meta["table_name"]}" LIMIT {sample_rows}'
            )
        except Exception:
            # Table might not be in DuckDB (e.g., MySQL-only)
            pass

        # Get foreign keys from connector if available
        connector = get_connectors().get(table_meta["source_id"])
        foreign_keys: list[dict[str, str]] = []
        if connector:
            try:
                info = connector.get_table_info(table_meta["table_name"])
                if info.foreign_keys:
                    foreign_keys = [
                        {"column": fk.column, "references": fk.references}
                        for fk in info.foreign_keys
                    ]
            except Exception:
                # Ignore
                pass

        result.append({
            "source": table_meta["source_id"],
            "table": table_meta["table_name"],
            "rowCount": table_meta["row_count"],
            "semanticStatus": table_meta["semantic_status"],
            "columns": [
                {
                    "name": c["column_name"],
                    "dtype": c["dtype"],
                    "nullable": c["nullable"] == 1,
                    "comment": c.get("comment"),
                    "sampleValues": json.loads(c["sample_values"])
                    if c.get("sample_values")
                    else [],
                }
                for c in columns
            ],
            "foreignKeys": foreign_keys,
            "sampleData": sample_data,
        })

    return json.dumps(
        {
            "message": (
                f"Found {len(result)} table(s) ready for semantic inference. "
                "Please analyze each table and call update_semantic with the results."
            ),
            "tables": result,
        },
        indent=2,
        default=_default_serializer,
    )


def handle_update_semantic(
    params: dict[str, Any],
    catalog: CatalogStore,
    index: SemanticIndex,
    embedder: Embedder | None = None,
) -> str:
    """Write semantic definitions to YAML and update the BM25 index."""
    tables = params.get("tables")

    if not tables or not isinstance(tables, list) or len(tables) == 0:
        raise ValueError("tables array is required and must not be empty")

    results: list[dict[str, str]] = []

    for table_input in tables:
        table_name: str | None = (
            table_input.get("table_name") or table_input.get("tableName")
        )

        if not table_name:
            results.append({"tableName": "unknown", "status": "error: table_name is required"})
            continue

        # Find the source_id for this table
        source_id: str | None = (
            table_input.get("source_id") or table_input.get("sourceId")
        )
        if not source_id:
            all_tables = catalog.get_tables()
            match = next(
                (t for t in all_tables if t["table_name"] == table_name), None
            )
            if not match:
                results.append({
                    "tableName": table_name,
                    "status": f'error: table "{table_name}" not found in any connected source',
                })
                continue
            source_id = match["source_id"]

        # Build TableSemantic from input
        columns_input: list[dict[str, Any]] = table_input.get("columns") or []
        columns_semantic = [
            ColumnSemantic(
                name=col.get("name", ""),
                semantic=col.get("semantic"),
                role=col.get("role"),
                unit=col.get("unit"),
                aggregation=col.get("aggregation"),
                references=col.get("references"),
                enum_values=col.get("enum_values") or col.get("enumValues"),
                granularity=col.get("granularity"),
                confirmed=col.get("confirmed", False),
            )
            for col in columns_input
        ]

        relations_input: list[dict[str, Any]] = table_input.get("relations") or []
        relations_semantic = [
            RelationSemantic(
                target_table=rel.get("target_table") or rel.get("targetTable", ""),
                join_condition=rel.get("join_condition") or rel.get("joinCondition", ""),
                relation_type=rel.get("relation_type") or rel.get("relationType", "one_to_many"),
                confirmed=rel.get("confirmed", False),
            )
            for rel in relations_input
        ]

        metrics_input: list[dict[str, Any]] = table_input.get("metrics") or []
        metrics_defs = [
            MetricDefinition(
                name=m.get("name", ""),
                expression=m.get("expression", ""),
                group_by=m.get("group_by") or m.get("groupBy"),
                filter=m.get("filter"),
            )
            for m in metrics_input
        ]

        semantic = TableSemantic(
            source=source_id,
            table=table_name,
            description=table_input.get("description"),
            business_domain=table_input.get("business_domain") or table_input.get("businessDomain"),
            tags=table_input.get("tags"),
            confirmed=False,
            updated_at=datetime.now(timezone.utc).isoformat(),
            columns=columns_semantic,
            relations=relations_semantic if relations_semantic else None,
            metrics=metrics_defs if metrics_defs else None,
        )

        # Write YAML
        write_table_semantic(source_id, table_name, semantic)

        # Update search index (+ embedding if enabled)
        index.index_table(
            source_id,
            table_name,
            semantic,
            catalog,
            embedder if embedder else None,
        )

        # Update semantic status in catalog
        catalog.update_semantic_status(source_id, table_name, "inferred")

        results.append({"tableName": table_name, "status": "updated"})

    updated = sum(1 for r in results if r["status"] == "updated")
    errors = sum(1 for r in results if r["status"].startswith("error"))

    return json.dumps(
        {
            "message": f"Semantic layer updated: {updated} table(s) written, {errors} error(s).",
            "indexedCount": index.count(),
            "results": results,
        },
        indent=2,
    )
