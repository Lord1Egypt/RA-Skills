"""Schema collector -- gathers table/column metadata from connectors
and persists to the catalog store."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lucid_skill.catalog.store import CatalogStore

from lucid_skill.types import TableInfo


def collect_schema(connector: object, store: CatalogStore) -> list[TableInfo]:
    """Gather table/column metadata from *connector* and persist to catalog.

    Parameters
    ----------
    connector:
        Any object exposing ``source_id``, ``list_tables()`` and
        ``get_table_info(table_name)`` (i.e. a concrete ``Connector``).
    store:
        The :class:`CatalogStore` used to persist the metadata.

    Returns
    -------
    list[TableInfo]
        One :class:`TableInfo` per table discovered.
    """
    tables: list[str] = connector.list_tables()  # type: ignore[attr-defined]
    result: list[TableInfo] = []

    for table_name in tables:
        info: TableInfo = connector.get_table_info(table_name)  # type: ignore[attr-defined]
        result.append(info)

        store.upsert_table_meta(
            connector.source_id,  # type: ignore[attr-defined]
            table_name,
            info.row_count,
            len(info.columns),
        )

        for col in info.columns:
            store.upsert_column_meta(
                connector.source_id,  # type: ignore[attr-defined]
                table_name,
                col.name,
                col.dtype,
                col.nullable,
                col.comment,
                col.sample_values,
            )

    return result
