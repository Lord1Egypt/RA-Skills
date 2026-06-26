#!/bin/bash
# MySQL Database Backup
# Creates timestamped backups of MySQL databases

set -e

# Default values
HOST=""
PORT="3306"
USER=""
PASSWORD=""
DATABASE=""
OUTPUT=""
COMPRESS=false

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
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --compress)
      COMPRESS=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [[ -z "$HOST" || -z "$USER" || -z "$PASSWORD" || -z "$DATABASE" || -z "$OUTPUT" ]]; then
  echo "Usage: $0 --host HOST --user USER --password PASSWORD --database DATABASE --output OUTPUT [--compress]"
  exit 1
fi

# Create output directory if needed
OUTPUT_DIR=$(dirname "$OUTPUT")
mkdir -p "$OUTPUT_DIR"

# Generate timestamp if output is a directory
if [[ -d "$OUTPUT" ]]; then
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  OUTPUT="$OUTPUT/${DATABASE}_${TIMESTAMP}.sql"
fi

# Build mysqldump command
MYSQLDUMP_CMD="mysqldump -h $HOST -P $PORT -u $USER -p$PASSWORD $DATABASE"

# Add compression if requested
if [[ "$COMPRESS" == true ]]; then
  MYSQLDUMP_CMD="$MYSQLDUMP_CMD | gzip > ${OUTPUT}.gz"
  OUTPUT="${OUTPUT}.gz"
else
  MYSQLDUMP_CMD="$MYSQLDUMP_CMD > $OUTPUT"
fi

# Execute backup
echo "Backing up database: $DATABASE"
echo "Output file: $OUTPUT"
eval $MYSQLDUMP_CMD

# Verify backup
if [[ -f "$OUTPUT" ]]; then
  SIZE=$(du -h "$OUTPUT" | cut -f1)
  echo "Backup completed successfully!"
  echo "File size: $SIZE"
else
  echo "Backup failed!"
  exit 1
fi