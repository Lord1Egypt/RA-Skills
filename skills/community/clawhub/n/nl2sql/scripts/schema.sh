#!/usr/bin/env bash
# Discover database schema with remote connection support
# Usage: schema.sh <database> [table_name] [--host HOST] [--port PORT] [--user USER] [--password PASS]
set -euo pipefail

DB="${1:?Usage: schema.sh <database> [table_name] [OPTIONS]}"
TABLE="${2:-}"
CONN_ARGS=()

# If TABLE looks like a flag, treat it as option
if [[ "$TABLE" == --* ]]; then
  set -- "$DB" "" "$TABLE" "${@:3}"
  TABLE=""
fi

shift
[[ -n "$TABLE" ]] && shift

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) CONN_ARGS+=(-h "$2"); shift 2 ;;
    --port) CONN_ARGS+=(-P "$2"); shift 2 ;;
    --user) CONN_ARGS+=(-u "$2"); shift 2 ;;
    --password) CONN_ARGS+=(-p"$2"); shift 2 ;;
    *) shift ;;
  esac
done

if [[ -n "$TABLE" ]]; then
  mysql "${CONN_ARGS[@]}" "$DB" -e "SHOW CREATE TABLE \`$TABLE\`\G"
else
  echo "=== Database: $DB ==="
  echo ""
  TABLES=$(mysql "${CONN_ARGS[@]}" "$DB" -N -e "SHOW TABLES")
  for T in $TABLES; do
    echo "--- Table: $T ---"
    mysql "${CONN_ARGS[@]}" "$DB" -e "SHOW CREATE TABLE \`$T\`\G" | grep -v '^\*\*\*'
    echo ""
  done
fi
