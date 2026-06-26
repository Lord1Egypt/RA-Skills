#!/usr/bin/env python3
import argparse
import os
import re
from pathlib import Path

from _common import coalesce, mask_sensitive, to_json, env_int
from profile_loader import load_profile

READONLY_PATTERN = re.compile(r"^\s*(SELECT|WITH|EXPLAIN\s+SELECT)\b", re.IGNORECASE | re.DOTALL)
DENY_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|REPLACE|UPSERT|MERGE|DROP|TRUNCATE|ALTER|CREATE|RENAME|GRANT|REVOKE)\b",
    re.IGNORECASE,
)


def validate_sql(sql: str):
    if not READONLY_PATTERN.search(sql):
        raise ValueError("Only SELECT/WITH/EXPLAIN SELECT are allowed")
    if DENY_PATTERN.search(sql):
        raise ValueError("SQL contains forbidden keywords")


def main():
    parser = argparse.ArgumentParser(description="Read-only MySQL query executor")
    parser.add_argument("--profile", required=True)
    parser.add_argument("--conn-file")
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--database")
    parser.add_argument("--sql", required=True)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    validate_sql(args.sql)

    conn_file = args.conn_file or str(Path(__file__).resolve().parent / "connections.json")
    conn, meta = load_profile(conn_file, args.profile)
    host = coalesce(args.host, os.getenv("MYSQL_HOST"), conn.get("host"))
    port = coalesce(args.port, env_int("MYSQL_PORT"), conn.get("port"), 3306)
    username = coalesce(args.username, os.getenv("MYSQL_USER"), conn.get("username"))
    password = coalesce(args.password, os.getenv("MYSQL_PASSWORD"), conn.get("password"))
    database = coalesce(args.database, os.getenv("MYSQL_DATABASE"), conn.get("database"))

    if not all([host, port, username, password, database]):
        raise ValueError("Missing required MySQL config: host/port/username/password/database")

    import pymysql

    sql = args.sql.strip().rstrip(";")
    if " limit " not in sql.lower():
        sql = f"{sql} LIMIT {min(args.limit, 1000)}"

    db = pymysql.connect(host=host, port=int(port), user=username, password=password, database=database, connect_timeout=5)
    try:
        with db.cursor() as cur:
            cur.execute(sql)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchall()
            result = [dict(zip(cols, r)) for r in rows]
    finally:
        db.close()

    to_json({
        "datasource": "mysql",
        "profile": args.profile,
        "profile_meta": meta,
        "query": sql,
        "count": len(result),
        "preview": mask_sensitive(result[: min(len(result), args.limit)]),
    })


if __name__ == "__main__":
    main()
