"""describe_table tool handler."""

from __future__ import annotations

import json
from typing import Any

from lucid_skill.catalog.store import CatalogStore
from lucid_skill.query.engine import QueryEngine


def _default_serializer(obj: object) -> str:
    """Handle non-serializable types (e.g. Decimal, date, bytes)."""
    return str(obj)


def handle_describe_table(
    params: dict[str, Any],
    catalog: CatalogStore,
    engine: QueryEngine | None = None,
) -> str:
    """Describe a table's columns, profiling data, and optional sample rows.

    Accepts either { table_name } or { source_id, table_name }.
    Also supports camelCase variants (tableName, sourceId).
    """
    # Support both snake_case (MCP convention) and camelCase
    table_name: str | None = params.get("table_name") or params.get("tableName")
    source_id: str | None = params.get("source_id") or params.get("sourceId")

    if not table_name:
        raise ValueError("table_name is required")

    # If no sourceId given, look up the table from catalog
    if not source_id:
        all_tables = catalog.get_tables()
        match = next((t for t in all_tables if t["table_name"] == table_name), None)
        if not match:
            raise ValueError(f'Table "{table_name}" not found in any connected source')
        source_id = match["source_id"]

    columns = catalog.get_columns(source_id, table_name)
    if len(columns) == 0:
        raise ValueError(f'Table "{table_name}" not found in source "{source_id}"')

    # Get sample data if engine available
    sample_data: list[dict[str, Any]] = []
    if engine and params.get("include_sample") is not False:
        sample_rows = int(params.get("sample_rows", 5))
        try:
            sample_data = engine.execute_raw(
                f'SELECT * FROM "{table_name}" LIMIT {sample_rows}'
            )
        except Exception:
            # Sample data is optional -- ignore errors
            pass

    # Find row count for this table
    tables_for_source = catalog.get_tables(source_id)
    row_count = None
    for t in tables_for_source:
        if t["table_name"] == table_name:
            row_count = t.get("row_count")
            break

    return json.dumps(
        {
            "sourceId": source_id,
            "tableName": table_name,
            "rowCount": row_count,
            "columns": [
                {
                    "name": c["column_name"],
                    "dtype": c["dtype"],
                    "nullable": c["nullable"] == 1,
                    "comment": c.get("comment"),
                    "sampleValues": json.loads(c["sample_values"])
                    if c.get("sample_values")
                    else [],
                    "distinctCount": c.get("distinct_count"),
                    "nullRate": c.get("null_rate"),
                    "minValue": c.get("min_value"),
                    "maxValue": c.get("max_value"),
                }
                for c in columns
            ],
            "sampleData": sample_data,
        },
        indent=2,
        default=_default_serializer,
    )
