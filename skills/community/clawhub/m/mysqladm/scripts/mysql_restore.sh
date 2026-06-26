#!/bin/bash
# MySQL Database Restore
# Restores MySQL databases from backup files

set -e

# Default values
HOST=""
PORT="3306"
USER=""
PASSWORD=""
DATABASE=""
INPUT=""
DROP_BEFORE_RESTORE=false

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
    --input)
      INPUT="$2"
      shift 2
      ;;
    --drop-before-restore)
      DROP_BEFORE_RESTORE=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [[ -z "$HOST" || -z "$USER" || -z "$PASSWORD" || -z "$DATABASE" || -z "$INPUT" ]]; then
  echo "Usage: $0 --host HOST --user USER --password PASSWORD --database DATABASE --input INPUT [--drop-before-restore]"
  exit 1
fi

# Check if input file exists
if [[ ! -f "$INPUT" ]]; then
  echo "Error: Input file not found: $INPUT"
  exit 1
fi

# Build mysql command
MYSQL_CMD="mysql -h $HOST -P $PORT -u $USER -p$PASSWORD"

# Drop database if requested
if [[ "$DROP_BEFORE_RESTORE" == true ]]; then
  echo "Dropping existing database: $DATABASE"
  $MYSQL_CMD -e "DROP DATABASE IF EXISTS $DATABASE;"
  $MYSQL_CMD -e "CREATE DATABASE $DATABASE;"
fi

# Determine if input is compressed
if [[ "$INPUT" == *.gz ]]; then
  RESTORE_CMD="gunzip -c $INPUT | $MYSQL_CMD $DATABASE"
else
  RESTORE_CMD="$MYSQL_CMD $DATABASE < $INPUT"
fi

# Execute restore
echo "Restoring database: $DATABASE"
echo "From file: $INPUT"
eval $RESTORE_CMD

echo "Restore completed successfully!"