from __future__ import annotations

import json
from datetime import date, datetime

from lucid_skill.types import QueryFormat, QueryResult


def format_query_result(result: QueryResult, fmt: QueryFormat) -> str:
    """Format query results into different output formats."""
    if fmt == "json":
        return _format_json(result)
    elif fmt == "csv":
        return _format_csv(result)
    else:
        return _format_markdown(result)


def _format_json(result: QueryResult) -> str:
    return json.dumps(
        {
            "columns": result.columns,
            "rows": result.rows,
            "rowCount": result.row_count,
            "truncated": result.truncated,
        },
        indent=2,
        default=str,
    )


def _format_markdown(result: QueryResult) -> str:
    if not result.columns:
        return "_No results_"

    header = "| " + " | ".join(result.columns) + " |"
    separator = "| " + " | ".join("---" for _ in result.columns) + " |"
    rows = [
        "| " + " | ".join(_format_value(row.get(col)) for col in result.columns) + " |"
        for row in result.rows
    ]

    lines = [header, separator, *rows]

    if result.truncated:
        lines.append("")
        lines.append(f"_Showing {len(result.rows)} of {result.row_count} rows_")

    return "\n".join(lines)


def _format_csv(result: QueryResult) -> str:
    header = ",".join(_escape_csv_value(col) for col in result.columns)
    rows = [
        ",".join(
            _escape_csv_value(_format_value(row.get(col))) for col in result.columns
        )
        for row in result.rows
    ]
    return "\n".join([header, *rows])


def _format_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


def _escape_csv_value(value: str) -> str:
    if "," in value or '"' in value or "\n" in value:
        return '"' + value.replace('"', '""') + '"'
    return value
