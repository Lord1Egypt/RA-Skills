"""query tool handler."""

from __future__ import annotations

from typing import Any

from lucid_skill.query.engine import QueryEngine
from lucid_skill.query.formatter import format_query_result
from lucid_skill.query.router import QueryRouter
from lucid_skill.types import QueryFormat


def handle_query(
    params: dict[str, Any],
    engine: QueryEngine,
    router: QueryRouter | None = None,
) -> str:
    """Execute a SQL query and return formatted results.

    Routes through QueryRouter for MySQL/PostgreSQL direct execution
    when possible, otherwise falls back to DuckDB via QueryEngine.

    Parameters
    ----------
    params:
        Must contain ``sql``. Optional: ``maxRows`` (default 100),
        ``format`` (default "markdown").
    engine:
        The DuckDB query engine.
    router:
        Optional query router for direct-source execution.
    """
    sql: str | None = params.get("sql")
    max_rows: int = int(params.get("maxRows", 100))
    fmt: QueryFormat = params.get("format", "markdown")

    if not sql:
        raise ValueError("sql parameter is required")

    result = router.route(sql, max_rows) if router else engine.execute(sql, max_rows)

    return format_query_result(result, fmt)
