#!/bin/bash
# Batch ingest all PDFs from a folder

set -e

FOLDER="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$FOLDER" ]; then
    echo "Usage: $0 <folder-path>"
    exit 1
fi

if [ ! -d "$FOLDER" ]; then
    echo "Error: Folder not found: $FOLDER"
    exit 1
fi

echo "Batch ingesting PDFs from: $FOLDER"
echo ""

COUNT=0
for pdf in "$FOLDER"/*.pdf "$FOLDER"/*.PDF; do
    [ -f "$pdf" ] || continue
    bash "$SCRIPT_DIR/ingest.sh" "$pdf"
    COUNT=$((COUNT + 1))
done

echo ""
echo "✓ Done: $COUNT documents ingested"
