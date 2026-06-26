"""Global connector registry + connect/list handlers."""

from __future__ import annotations

from typing import Any

from lucid_skill.catalog.schema import collect_schema
from lucid_skill.catalog.store import CatalogStore
from lucid_skill.connectors.base import Connector
from lucid_skill.query.engine import QueryEngine
from lucid_skill.query.router import QueryRouter
from lucid_skill.types import TableInfo

_connectors: dict[str, Connector] = {}


def get_connectors() -> dict[str, Connector]:
    """Return the global connector registry."""
    return _connectors


def get_connector(source_id: str) -> Connector | None:
    """Return a connector by source ID, or None if not found."""
    return _connectors.get(source_id)


def handle_connect_source(
    params: dict[str, Any],
    catalog: CatalogStore,
    engine: QueryEngine | None = None,
    router: QueryRouter | None = None,
) -> dict[str, Any]:
    """Connect a data source. Returns {source_id, tables}."""
    from lucid_skill.connectors.csv_conn import CsvConnector
    from lucid_skill.connectors.excel_conn import ExcelConnector

    src_type = params.get("type")

    connector_map: dict[str, type] = {
        "csv": CsvConnector,
        "excel": ExcelConnector,
    }

    try:
        from lucid_skill.connectors.mysql_conn import MySQLConnector

        connector_map["mysql"] = MySQLConnector
    except ImportError:
        pass

    try:
        from lucid_skill.connectors.postgres_conn import PostgresConnector

        connector_map["postgresql"] = PostgresConnector
    except ImportError:
        pass

    cls = connector_map.get(src_type)
    if not cls:
        raise ValueError(f"Unsupported source type: {src_type}")

    connector: Connector = cls()
    connector.connect(params)

    source_id = connector.source_id
    _connectors[source_id] = connector

    # Persist source to catalog
    catalog.upsert_source(source_id, connector.source_type, params)

    # Collect schema
    tables: list[TableInfo] = collect_schema(connector, catalog)

    # Register tables into the shared query engine DuckDB (for Excel/CSV)
    if engine:
        connector.register_to_duckdb(engine.get_database())

    # Register connector in query router for routing decisions
    if router:
        router.register_connector(source_id, connector, [t.name for t in tables])

    return {"source_id": source_id, "tables": tables}


def handle_list_tables(
    params: dict[str, Any],
    catalog: CatalogStore,
) -> list[dict[str, Any]]:
    """List tables, optionally filtered by sourceId."""
    source_id = params.get("sourceId") or params.get("source_id")
    return catalog.get_tables(source_id)
