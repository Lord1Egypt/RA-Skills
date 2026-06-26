"""Table profiler using DuckDB SUMMARIZE."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from lucid_skill.catalog.store import CatalogStore


def profile_table(
    engine: object,
    source_id: str,
    table_name: str,
    store: CatalogStore,
) -> list[dict[str, Any]]:
    """Profile a table using DuckDB ``SUMMARIZE`` and persist results.

    Parameters
    ----------
    engine:
        Any object exposing ``execute_raw(sql)`` that returns a list of
        dicts (i.e. the DuckDB query engine).
    source_id:
        Identifier of the data source that owns *table_name*.
    table_name:
        The table to profile.
    store:
        The :class:`CatalogStore` used to persist profiling data.

    Returns
    -------
    list[dict[str, Any]]
        Raw rows returned by ``SUMMARIZE``.
    """
    rows: list[dict[str, Any]] = engine.execute_raw(  # type: ignore[attr-defined]
        f'SUMMARIZE SELECT * FROM "{table_name}"'
    )

    for row in rows:
        null_pct = row.get("null_percentage")
        store.update_profiling_data(
            source_id,
            table_name,
            row["column_name"],
            {
                "distinct_count": row.get("approx_unique"),
                "null_rate": null_pct / 100 if null_pct is not None else None,
                "min_value": row.get("min"),
                "max_value": row.get("max"),
            },
        )

    return rows
