"""profile_data tool handler."""

from __future__ import annotations

import json
from typing import Any

from lucid_skill.catalog.store import CatalogStore
from lucid_skill.query.engine import QueryEngine


def _default_serializer(obj: object) -> str:
    """Handle non-serializable types (e.g. Decimal, date, bytes)."""
    return str(obj)


def handle_profile_data(
    params: dict[str, Any],
    catalog: CatalogStore,
    engine: QueryEngine,
) -> str:
    """Run DuckDB SUMMARIZE on a table and store profiling results.

    Accepts table_name (required) and source_id (optional, auto-detected).
    Also supports camelCase variants (tableName, sourceId).
    """
    # Support both snake_case and camelCase
    table_name: str | None = params.get("table_name") or params.get("tableName")
    source_id: str | None = params.get("source_id") or params.get("sourceId")

    if not table_name:
        raise ValueError("table_name is required")

    # If no sourceId given, look up from catalog
    if not source_id:
        all_tables = catalog.get_tables()
        match = next((t for t in all_tables if t["table_name"] == table_name), None)
        if match:
            source_id = match["source_id"]

    try:
        rows: list[dict[str, Any]] = engine.execute_raw(
            f'SUMMARIZE SELECT * FROM "{table_name}"'
        )
    except Exception as err:
        raise ValueError(
            f'Failed to profile table "{table_name}": {err}'
        ) from err

    # Store profiling results if sourceId is known
    if source_id:
        for row in rows:
            col_name = str(row.get("column_name") or row.get("column") or "")
            if col_name:
                catalog.update_profiling_data(source_id, table_name, col_name, {
                    "distinct_count": int(row["approx_unique"])
                    if row.get("approx_unique") is not None
                    else None,
                    "null_rate": float(row["null_percentage"]) / 100
                    if row.get("null_percentage") is not None
                    else None,
                    "min_value": str(row["min"])
                    if row.get("min") is not None
                    else None,
                    "max_value": str(row["max"])
                    if row.get("max") is not None
                    else None,
                })

    return json.dumps(
        {
            "sourceId": source_id or "unknown",
            "tableName": table_name,
            "profiledColumns": len(rows),
            "summary": [
                {
                    "column": r.get("column_name") or r.get("column"),
                    "type": r.get("column_type") or r.get("type"),
                    "min": r.get("min"),
                    "max": r.get("max"),
                    "approxUnique": r.get("approx_unique"),
                    "nullPercentage": r.get("null_percentage"),
                    "avg": r.get("avg"),
                    "std": r.get("std"),
                    "q25": r.get("q25"),
                    "q50": r.get("q50"),
                    "q75": r.get("q75"),
                }
                for r in rows
            ],
        },
        indent=2,
        default=_default_serializer,
    )
