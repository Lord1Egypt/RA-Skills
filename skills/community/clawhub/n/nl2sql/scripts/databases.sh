#!/usr/bin/env bash
# List available databases with optional connection params
# Usage: databases.sh [--host HOST] [--port PORT] [--user USER] [--password PASS]
set -euo pipefail

CONN_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) CONN_ARGS+=(-h "$2"); shift 2 ;;
    --port) CONN_ARGS+=(-P "$2"); shift 2 ;;
    --user) CONN_ARGS+=(-u "$2"); shift 2 ;;
    --password) CONN_ARGS+=(-p"$2"); shift 2 ;;
    *) shift ;;
  esac
done

echo "=== 可用数据库列表 ==="
mysql "${CONN_ARGS[@]}" -e "
SELECT 
  SCHEMA_NAME AS 数据库名,
  DEFAULT_CHARACTER_SET_NAME AS 字符集,
  DEFAULT_COLLATION_NAME AS 排序规则
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME NOT IN ('information_schema', 'performance_schema')
ORDER BY SCHEMA_NAME;
"
