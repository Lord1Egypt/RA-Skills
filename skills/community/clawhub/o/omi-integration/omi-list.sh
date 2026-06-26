#!/bin/bash
# List Omi recordings from local storage

STORAGE_DIR="$HOME/omi_recordings"
DAYS=7

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --days)
      DAYS="$2"
      shift 2
      ;;
    --all)
      DAYS=9999
      shift
      ;;
    *)
      shift
      ;;
  esac
done

if [[ ! -d "$STORAGE_DIR" ]]; then
  echo "No recordings found. Run omi-sync first."
  exit 1
fi

echo "📼 Recent Omi Recordings (Last $DAYS days)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Find recordings from last N days
if [[ "$OSTYPE" == "darwin"* ]]; then
  CUTOFF_DATE=$(date -u -v-${DAYS}d +%Y-%m-%d)
else
  CUTOFF_DATE=$(date -u -d "$DAYS days ago" +%Y-%m-%d)
fi

find "$STORAGE_DIR" -name "metadata.json" -type f | while read -r meta_file; do
  DATE_DIR=$(basename $(dirname $(dirname "$meta_file")))
  
  # Skip if older than cutoff
  if [[ "$DATE_DIR" < "$CUTOFF_DATE" ]]; then
    continue
  fi
  
  RECORDING_ID=$(basename $(dirname "$meta_file"))
  CREATED_AT=$(jq -r '.created_at // .timestamp' "$meta_file")
  DEVICE=$(jq -r '.device_name // .device_id // "Unknown"' "$meta_file")
  TITLE=$(jq -r '.title // "Untitled"' "$meta_file")
  DURATION=$(jq -r '.duration // "?"' "$meta_file")
  
  echo ""
  echo "🎙️  $TITLE"
  echo "   ID: $RECORDING_ID"
  echo "   Device: $DEVICE"
  echo "   Date: $CREATED_AT"
  echo "   Duration: ${DURATION}s"
  
  # Show transcript preview if available
  TRANSCRIPT_FILE=$(dirname "$meta_file")/transcript.txt
  if [[ -f "$TRANSCRIPT_FILE" ]]; then
    PREVIEW=$(head -c 100 "$TRANSCRIPT_FILE")
    echo "   Preview: ${PREVIEW}..."
  fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOTAL=$(find "$STORAGE_DIR" -name "metadata.json" -type f | wc -l | tr -d ' ')
echo "Total recordings: $TOTAL"
