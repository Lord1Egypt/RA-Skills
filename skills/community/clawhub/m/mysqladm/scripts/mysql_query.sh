#!/bin/bash
# MySQL Query Executor
# Executes SQL queries with formatted output

set -e

# Default values
HOST=""
PORT="3306"
USER=""
PASSWORD=""
DATABASE=""
QUERY=""
FORMAT="table"  # table, json, csv

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --host)
      HOST="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --user)
      USER="$2"
      shift 2
      ;;
    --password)
      PASSWORD="$2"
      shift 2
      ;;
    --database)
      DATABASE="$2"
      shift 2
      ;;
    --query)
      QUERY="$2"
      shift 2
      ;;
    --format)
      FORMAT="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [[ -z "$HOST" || -z "$USER" || -z "$PASSWORD" || -z "$DATABASE" || -z "$QUERY" ]]; then
  echo "Usage: $0 --host HOST --user USER --password PASSWORD --database DATABASE --query QUERY [--format FORMAT]"
  exit 1
fi

# Build mysql command
MYSQL_CMD="mysql -h $HOST -P $PORT -u $USER -p$PASSWORD $DATABASE"

# Add format flags
case $FORMAT in
  table)
    MYSQL_CMD="$MYSQL_CMD -t"
    ;;
  json)
    MYSQL_CMD="$MYSQL_CMD --json"
    ;;
  csv)
    MYSQL_CMD="$MYSQL_CMD --batch --raw"
    ;;
esac

# Execute query
echo "Executing query..."
echo "$MYSQL_CMD" -e "$QUERY" | sed 's/p'"$PASSWORD"'//' | eval $MYSQL_CMD -e "$QUERY"