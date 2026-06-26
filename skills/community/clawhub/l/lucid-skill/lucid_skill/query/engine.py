from __future__ import annotations

import re

import duckdb

from lucid_skill.config import get_config
from lucid_skill.query.safety import check_sql_safety
from lucid_skill.types import QueryResult


class QueryEngine:
    def __init__(self, db=None):
        self._db = db or duckdb.connect(":memory:")

    def get_database(self):
        return self._db

    def execute(self, sql: str, max_rows: int | None = None) -> QueryResult:
        config = get_config()
        limit = max_rows or config.query.max_rows

        safe, reason = check_sql_safety(sql)
        if not safe:
            raise ValueError(f"SQL safety check failed: {reason}")

        wrapped = self._wrap_with_limit(sql, limit)
        rows = self._db.execute(wrapped).fetchall()
        desc = self._db.description or []
        columns = [d[0] for d in desc]
        typed_rows = [dict(zip(columns, row)) for row in rows]

        total_count = len(typed_rows)
        truncated = False
        if len(typed_rows) == limit:
            try:
                count_result = self._db.execute(
                    f"SELECT COUNT(*) FROM ({sql}) AS _count_subquery"
                ).fetchone()
                total_count = count_result[0]
                truncated = total_count > limit
            except Exception:
                truncated = True

        return QueryResult(
            columns=columns,
            rows=typed_rows,
            row_count=total_count,
            truncated=truncated,
        )

    def execute_raw(self, sql: str) -> list[dict]:
        result = self._db.execute(sql)
        desc = result.description or []
        columns = [d[0] for d in desc]
        return [dict(zip(columns, row)) for row in result.fetchall()]

    def run(self, sql: str) -> None:
        self._db.execute(sql)

    def close(self) -> None:
        self._db.close()

    def _wrap_with_limit(self, sql: str, limit: int) -> str:
        if re.search(r'\bLIMIT\s+\d+\s*$', sql.strip(), re.IGNORECASE):
            return sql
        return f"{sql.strip()} LIMIT {limit}"
