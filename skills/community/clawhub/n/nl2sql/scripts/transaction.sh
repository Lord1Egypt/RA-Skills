#!/usr/bin/env bash
# Execute multiple SQL statements in a transaction with remote connection support
# Usage: transaction.sh <database> <sql_file> [--host HOST] [--port PORT] [--user USER] [--password PASS]
set -euo pipefail

DB="${1:?Usage: transaction.sh <database> <sql_file> [OPTIONS]}"
SQL_FILE="${2:?SQL file path required}"
CONN_ARGS=()

shift 2
while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) CONN_ARGS+=(-h "$2"); shift 2 ;;
    --port) CONN_ARGS+=(-P "$2"); shift 2 ;;
    --user) CONN_ARGS+=(-u "$2"); shift 2 ;;
    --password) CONN_ARGS+=(-p"$2"); shift 2 ;;
    *) shift ;;
  esac
done

if [[ ! -f "$SQL_FILE" ]]; then
  echo "Error: File not found: $SQL_FILE" >&2
  exit 1
fi

{
  echo "SET autocommit=0;"
  echo "START TRANSACTION;"
  cat "$SQL_FILE"
  echo ""
  echo "COMMIT;"
} | mysql "${CONN_ARGS[@]}" "$DB" --verbose 2>&1

EXIT_CODE=${PIPESTATUS[1]:-$?}
if [[ $EXIT_CODE -ne 0 ]]; then
  echo "Transaction failed, rolled back." >&2
  mysql "${CONN_ARGS[@]}" "$DB" -e "ROLLBACK;" 2>/dev/null
  exit 1
fi

echo "✅ Transaction committed successfully."
