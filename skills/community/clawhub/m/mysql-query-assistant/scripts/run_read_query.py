#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List
from urllib.parse import urlparse

READ_ONLY_PREFIXES = ("select", "with", "show", "describe", "desc", "explain")
BLOCKED_TOKENS = {
    "insert", "update", "delete", "replace", "alter", "drop", "truncate",
    "create", "grant", "revoke", "lock", "unlock", "set", "rename", "call",
    "load", "handler", "do", "prepare", "execute", "deallocate",
}


def _load_driver():
    try:
        import mysql.connector as driver  # type: ignore
        return "mysql.connector", driver
    except Exception:
        try:
            import pymysql as driver  # type: ignore
            return "pymysql", driver
        except Exception as exc:
            raise RuntimeError(
                "No supported MySQL driver found. Install mysql-connector-python or pymysql."
            ) from exc


def _parse_db_env() -> Dict[str, Any]:
    db_url = os.environ.get("DB_URL")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    if not db_url or not user or password is None:
        raise RuntimeError("DB_URL, DB_USER, and DB_PASSWORD must be set.")

    parsed = urlparse(db_url)
    if parsed.scheme not in {"mysql", "mysql+pymysql", "mysql+mysqlconnector"}:
        raise RuntimeError("DB_URL must use a mysql URL scheme.")
    database = parsed.path.lstrip("/")
    if not parsed.hostname or not database:
        raise RuntimeError("DB_URL must include host and database name.")

    return {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "database": database,
        "user": user,
        "password": password,
        "charset": os.environ.get("DB_CHARSET", "utf8mb4"),
        "ssl_mode": os.environ.get("DB_SSL_MODE"),
    }


def _connect():
    driver_name, driver = _load_driver()
    cfg = _parse_db_env()
    if driver_name == "mysql.connector":
        kwargs = {
            "host": cfg["host"],
            "port": cfg["port"],
            "user": cfg["user"],
            "password": cfg["password"],
            "database": cfg["database"],
            "charset": cfg["charset"],
        }
        if cfg["ssl_mode"]:
            kwargs["ssl_disabled"] = False
        return driver.connect(**kwargs)

    return driver.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        charset=cfg["charset"],
        cursorclass=driver.cursors.DictCursor,
    )


def _normalize_sql(sql: str) -> str:
    return sql.strip().rstrip(";").strip()


def _ensure_single_statement(sql: str) -> None:
    if ";" in _normalize_sql(sql):
        raise ValueError("Only a single statement is allowed.")


def _ensure_read_only(sql: str) -> None:
    normalized = _normalize_sql(sql)
    lowered = normalized.lower()
    if not lowered.startswith(READ_ONLY_PREFIXES):
        raise ValueError("Query must start with a read-only statement.")
    tokens = set(re.findall(r"[a-z_]+", lowered))
    found = BLOCKED_TOKENS & tokens
    if found:
        raise ValueError(f"Blocked non-read-only token(s) found: {', '.join(sorted(found))}")


def _execute(conn, sql: str, limit: int) -> Dict[str, Any]:
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchmany(limit)
        columns = list(cur.column_names) if hasattr(cur, "column_names") else list(rows[0].keys()) if rows else []
    normalized_rows: List[Dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict):
            normalized_rows.append(row)
        else:
            normalized_rows.append({columns[i]: row[i] for i in range(len(columns))})
    return {
        "columns": columns,
        "sample_rows": normalized_rows,
        "sample_row_count": len(normalized_rows),
        "sample_limit": limit,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a read-only MySQL query and return sample rows.")
    parser.add_argument("sql", help="Single read-only SQL statement to execute.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum sample rows to return.")
    args = parser.parse_args()

    sql = _normalize_sql(args.sql)
    _ensure_single_statement(sql)
    _ensure_read_only(sql)

    conn = _connect()
    try:
        payload = _execute(conn, sql, max(1, min(args.limit, 100)))
        payload["sql"] = sql
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
