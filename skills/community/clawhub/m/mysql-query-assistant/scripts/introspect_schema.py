#!/usr/bin/env python3
import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from typing import Any, Dict, List
from urllib.parse import urlparse


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


@dataclass
class ColumnInfo:
    table_name: str
    column_name: str
    data_type: str
    column_type: str
    is_nullable: str
    column_key: str
    column_default: Any
    extra: str
    column_comment: str


def list_tables(conn) -> List[str]:
    sql = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = DATABASE() AND table_type = 'BASE TABLE'
    ORDER BY table_name
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    if rows and isinstance(rows[0], dict):
        return [row["table_name"] for row in rows]
    return [row[0] for row in rows]


def describe_tables(conn, tables: List[str]) -> Dict[str, Any]:
    placeholders = ", ".join(["%s"] * len(tables))
    sql = f"""
    SELECT
        table_name,
        column_name,
        data_type,
        column_type,
        is_nullable,
        column_key,
        column_default,
        extra,
        column_comment
    FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name IN ({placeholders})
    ORDER BY table_name, ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(sql, tables)
        rows = cur.fetchall()

    result: Dict[str, Any] = {table: [] for table in tables}
    for row in rows:
        if not isinstance(row, dict):
            row = {
                "table_name": row[0],
                "column_name": row[1],
                "data_type": row[2],
                "column_type": row[3],
                "is_nullable": row[4],
                "column_key": row[5],
                "column_default": row[6],
                "extra": row[7],
                "column_comment": row[8],
            }
        info = ColumnInfo(**row)
        result[info.table_name].append(asdict(info))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect MySQL schema metadata.")
    parser.add_argument("--tables", nargs="*", help="Specific table names to inspect.")
    args = parser.parse_args()

    conn = _connect()
    try:
        tables = args.tables or list_tables(conn)
        payload = {
            "database": _parse_db_env()["database"],
            "tables": tables,
            "columns": describe_tables(conn, tables) if tables else {},
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
