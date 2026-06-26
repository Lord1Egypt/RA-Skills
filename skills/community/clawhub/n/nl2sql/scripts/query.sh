#!/usr/bin/env bash
# nl2sql query executor with remote connection support
# Usage: query.sh <database> <sql|file> [--format table|csv|json] [--host HOST] [--port PORT] [--user USER] [--password PASS]
set -euo pipefail

DB="${1:?Usage: query.sh <database> <sql|file> [OPTIONS]}"
SQL_INPUT="${2:?SQL statement or file path required}"
FORMAT="table"
CONN_ARGS=()

shift 2
while [[ $# -gt 0 ]]; do
  case "$1" in
    --format) FORMAT="${2:-table}"; shift 2 ;;
    --host) CONN_ARGS+=(-h "$2"); shift 2 ;;
    --port) CONN_ARGS+=(-P "$2"); shift 2 ;;
    --user) CONN_ARGS+=(-u "$2"); shift 2 ;;
    --password) CONN_ARGS+=(-p"$2"); shift 2 ;;
    *) shift ;;
  esac
done

if [[ -f "$SQL_INPUT" ]]; then
  SQL=$(cat "$SQL_INPUT")
else
  SQL="$SQL_INPUT"
fi

case "$FORMAT" in
  csv)
    mysql "${CONN_ARGS[@]}" "$DB" -e "$SQL" | sed 's/\t/,/g'
    ;;
  json)
    mysql "${CONN_ARGS[@]}" "$DB" --batch --raw -e "$SQL" 2>/dev/null | python3 -c "
import sys, json
header = None
rows = []
for line in sys.stdin:
    cols = line.rstrip('\n').split('\t')
    if header is None:
        header = cols
    else:
        rows.append(dict(zip(header, cols)))
print(json.dumps(rows, ensure_ascii=False, indent=2))
" 2>/dev/null || mysql "${CONN_ARGS[@]}" "$DB" -e "$SQL"
    ;;
  *)
    mysql "${CONN_ARGS[@]}" "$DB" -e "$SQL"
    ;;
esac
