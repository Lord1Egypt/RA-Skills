#!/bin/bash
# Omi Recording Sync Script
# Syncs recordings from Omi API to local storage

set -e

# Configuration
CONFIG_DIR="$HOME/.config/omi"
API_KEY_FILE="$CONFIG_DIR/api_key"
BACKEND_URL_FILE="$CONFIG_DIR/backend_url"
STORAGE_DIR="$HOME/omi_recordings"
LOG_FILE="$STORAGE_DIR/.sync.log"

# Default backend URL
BACKEND_URL="https://api.omi.me/v1"

# Parse arguments
DAYS=30  # Default: sync last 30 days
SINCE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --days)
      DAYS="$2"
      shift 2
      ;;
    --since)
      SINCE="$2"
      shift 2
      ;;
    --help)
      echo "Usage: omi-sync [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --days N       Sync recordings from last N days (default: 30)"
      echo "  --since TIME   Sync recordings since timestamp (ISO 8601)"
      echo "  --help         Show this help"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Load configuration
if [[ ! -f "$API_KEY_FILE" ]]; then
  echo "Error: API key not found. Please run:"
  echo "  mkdir -p $CONFIG_DIR"
  echo "  echo 'YOUR_API_KEY' > $API_KEY_FILE"
  echo "  chmod 600 $API_KEY_FILE"
  exit 1
fi

API_KEY=$(cat "$API_KEY_FILE")

if [[ -f "$BACKEND_URL_FILE" ]]; then
  BACKEND_URL=$(cat "$BACKEND_URL_FILE")
fi

# Create storage directory
mkdir -p "$STORAGE_DIR"

# Calculate time range
if [[ -n "$SINCE" ]]; then
  TIME_FILTER="since=$SINCE"
else
  # Calculate Unix timestamp for N days ago
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SINCE_TIMESTAMP=$(date -u -v-${DAYS}d +%s)
  else
    # Linux
    SINCE_TIMESTAMP=$(date -u -d "$DAYS days ago" +%s)
  fi
  SINCE_ISO=$(date -u -d "@$SINCE_TIMESTAMP" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -r "$SINCE_TIMESTAMP" +%Y-%m-%dT%H:%M:%SZ)
  TIME_FILTER="since=$SINCE_ISO"
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Starting Omi sync..." | tee -a "$LOG_FILE"
echo "Backend: $BACKEND_URL" | tee -a "$LOG_FILE"
echo "Time filter: $TIME_FILTER" | tee -a "$LOG_FILE"

# Fetch recordings list
RESPONSE=$(curl -s -H "Authorization: Bearer $API_KEY" \
  "$BACKEND_URL/recordings?$TIME_FILTER")

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
  echo "Error from API: $(echo "$RESPONSE" | jq -r '.error')" | tee -a "$LOG_FILE"
  exit 1
fi

# Parse recordings
RECORDING_COUNT=$(echo "$RESPONSE" | jq -r '.recordings | length')
echo "Found $RECORDING_COUNT recordings to sync" | tee -a "$LOG_FILE"

if [[ "$RECORDING_COUNT" -eq 0 ]]; then
  echo "No new recordings to sync" | tee -a "$LOG_FILE"
  exit 0
fi

# Process each recording
echo "$RESPONSE" | jq -c '.recordings[]' | while read -r recording; do
  RECORDING_ID=$(echo "$recording" | jq -r '.id')
  CREATED_AT=$(echo "$recording" | jq -r '.created_at')
  DATE_DIR=$(echo "$CREATED_AT" | cut -d'T' -f1)
  
  REC_DIR="$STORAGE_DIR/$DATE_DIR/$RECORDING_ID"
  mkdir -p "$REC_DIR"
  
  echo "Syncing: $RECORDING_ID" | tee -a "$LOG_FILE"
  
  # Save metadata
  echo "$recording" | jq '.' > "$REC_DIR/metadata.json"
  
  # Fetch full transcript
  TRANSCRIPT=$(curl -s -H "Authorization: Bearer $API_KEY" \
    "$BACKEND_URL/recordings/$RECORDING_ID/transcript")
  
  if [[ -n "$TRANSCRIPT" ]] && [[ "$TRANSCRIPT" != "null" ]]; then
    echo "$TRANSCRIPT" | jq -r '.transcript // .text // .' > "$REC_DIR/transcript.txt"
  fi
  
  # Fetch summary if available
  SUMMARY=$(curl -s -H "Authorization: Bearer $API_KEY" \
    "$BACKEND_URL/recordings/$RECORDING_ID/summary")
  
  if [[ -n "$SUMMARY" ]] && [[ "$SUMMARY" != "null" ]]; then
    echo "$SUMMARY" | jq -r '.summary // .' > "$REC_DIR/summary.md"
  fi
  
  # Fetch audio if available (optional, usually large)
  # AUDIO_URL=$(echo "$recording" | jq -r '.audio_url // empty')
  # if [[ -n "$AUDIO_URL" ]]; then
  #   curl -s -o "$REC_DIR/audio.wav" "$AUDIO_URL"
  # fi
done

# Update index
find "$STORAGE_DIR" -name "metadata.json" -exec cat {} \; | jq -s '.' > "$STORAGE_DIR/index.json"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Sync complete: $RECORDING_COUNT recordings" | tee -a "$LOG_FILE"
