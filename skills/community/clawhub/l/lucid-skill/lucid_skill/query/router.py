from __future__ import annotations

import re

from lucid_skill.connectors.base import Connector
from lucid_skill.query.engine import QueryEngine
from lucid_skill.query.safety import check_sql_safety
from lucid_skill.types import QueryResult


class QueryRouter:
    """Query router -- decides whether to execute via MySQL/PostgreSQL directly or DuckDB.

    Routing logic:
    - Pure DuckDB tables (Excel/CSV) -> DuckDB engine
    - Pure MySQL query (all referenced tables from same MySQL source) -> MySQL direct
    - Pure PostgreSQL query (all referenced tables from same PG source) -> PostgreSQL direct
    - Mixed / unknown -> DuckDB (data already loaded at connect time)
    """

    def __init__(self, engine: QueryEngine) -> None:
        self._connectors: dict[str, Connector] = {}
        self._engine = engine
        self._table_source_map: dict[str, str] = {}

    def register_connector(
        self, source_id: str, connector: Connector, tables: list[str]
    ) -> None:
        self._connectors[source_id] = connector
        for t in tables:
            self._table_source_map[t.lower()] = source_id

    def route(self, sql: str, max_rows: int | None = None) -> QueryResult:
        """Route and execute a query."""
        safe, reason = check_sql_safety(sql)
        if not safe:
            raise ValueError(f"SQL safety check failed: {reason}")

        direct_source = self._detect_direct_source(sql)
        if direct_source:
            return self._execute_on_direct_source(direct_source, sql, max_rows)

        return self._engine.execute(sql, max_rows)

    def get_engine(self) -> QueryEngine:
        return self._engine

    def _detect_direct_source(self, sql: str) -> str | None:
        """Detect if all referenced tables belong to the same direct-query source
        (MySQL or PostgreSQL). Returns the source_id if yes, None otherwise."""
        table_pattern = re.compile(r'(?:FROM|JOIN)\s+[`"]?(\w+)[`"]?', re.IGNORECASE)
        mentioned = [m.group(1).lower() for m in table_pattern.finditer(sql)]

        if not mentioned:
            return None

        candidate_source: str | None = None
        for table_name in mentioned:
            source_id = self._table_source_map.get(table_name)
            if not source_id:
                return None  # Unknown table, fall back to DuckDB
            if not source_id.startswith("mysql:") and not source_id.startswith(
                "postgresql:"
            ):
                return None

            if candidate_source is None:
                candidate_source = source_id
            elif candidate_source != source_id:
                return None  # Tables from different sources -- need DuckDB

        return candidate_source

    def _execute_on_direct_source(
        self, source_id: str, sql: str, max_rows: int | None = None
    ) -> QueryResult:
        """Execute a query directly on the source database (MySQL or PostgreSQL)
        and wrap result in QueryResult format."""
        connector = self._connectors.get(source_id)
        if connector is None or not hasattr(connector, "execute_query"):
            # Fallback to DuckDB
            return self._engine.execute(sql, max_rows)

        limit = max_rows if max_rows is not None else 1000
        # Append LIMIT if not already present
        if re.search(r'\bLIMIT\s+\d+\s*$', sql.strip(), re.IGNORECASE):
            limited_sql = sql
        else:
            limited_sql = f"{sql.strip()} LIMIT {limit}"

        result = connector.execute_query(limited_sql)  # type: ignore[attr-defined]
        columns = result["columns"]
        rows = result["rows"]

        return QueryResult(
            columns=columns,
            rows=rows,
            row_count=len(rows),
            truncated=len(rows) == limit,
        )
