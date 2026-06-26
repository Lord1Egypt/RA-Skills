#!/bin/bash
# Omi Webhook Handler
# Processes real-time webhook payloads from Omi devices

set -e

STORAGE_DIR="$HOME/omi_recordings"
WEBHOOK_LOG="$STORAGE_DIR/.webhook.log"

mkdir -p "$STORAGE_DIR"

# Read JSON payload from stdin
PAYLOAD=$(cat)

# Log webhook receipt
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Webhook received" >> "$WEBHOOK_LOG"
echo "$PAYLOAD" | jq '.' >> "$WEBHOOK_LOG"

# Extract event type
EVENT_TYPE=$(echo "$PAYLOAD" | jq -r '.event // .type // "unknown"')

echo "Processing event: $EVENT_TYPE" >> "$WEBHOOK_LOG"

case "$EVENT_TYPE" in
  "recording.created"|"transcript.created")
    # New recording created
    RECORDING_ID=$(echo "$PAYLOAD" | jq -r '.data.id // .recording_id')
    CREATED_AT=$(echo "$PAYLOAD" | jq -r '.data.created_at // .created_at // now | strftime("%Y-%m-%dT%H:%M:%SZ")')
    DATE_DIR=$(echo "$CREATED_AT" | cut -d'T' -f1)
    
    REC_DIR="$STORAGE_DIR/$DATE_DIR/$RECORDING_ID"
    mkdir -p "$REC_DIR"
    
    # Save metadata
    echo "$PAYLOAD" | jq '.data // .' > "$REC_DIR/metadata.json"
    
    # Save transcript if available
    TRANSCRIPT=$(echo "$PAYLOAD" | jq -r '.data.transcript // .transcript // empty')
    if [[ -n "$TRANSCRIPT" ]]; then
      echo "$TRANSCRIPT" > "$REC_DIR/transcript.txt"
    fi
    
    echo "Saved recording: $RECORDING_ID" >> "$WEBHOOK_LOG"
    ;;
    
  "transcript.updated")
    # Transcript updated (real-time streaming)
    RECORDING_ID=$(echo "$PAYLOAD" | jq -r '.data.recording_id // .recording_id')
    TRANSCRIPT=$(echo "$PAYLOAD" | jq -r '.data.transcript // .transcript')
    
    # Find recording directory
    REC_DIR=$(find "$STORAGE_DIR" -type d -name "$RECORDING_ID" | head -1)
    
    if [[ -n "$REC_DIR" ]]; then
      # Update transcript
      echo "$TRANSCRIPT" > "$REC_DIR/transcript.txt"
      echo "Updated transcript: $RECORDING_ID" >> "$WEBHOOK_LOG"
    else
      echo "Warning: Recording not found: $RECORDING_ID" >> "$WEBHOOK_LOG"
    fi
    ;;
    
  "recording.completed")
    # Recording finalized
    RECORDING_ID=$(echo "$PAYLOAD" | jq -r '.data.id // .recording_id')
    
    echo "Recording completed: $RECORDING_ID" >> "$WEBHOOK_LOG"
    
    # Trigger sync to get final version
    # $(dirname "$0")/omi-sync.sh --since "1 hour ago" &
    ;;
    
  *)
    echo "Unknown event type: $EVENT_TYPE" >> "$WEBHOOK_LOG"
    ;;
esac

# Update index
find "$STORAGE_DIR" -name "metadata.json" -exec cat {} \; | jq -s '.' > "$STORAGE_DIR/index.json" 2>/dev/null || true

# Return success
echo '{"status": "ok", "event": "'$EVENT_TYPE'"}'
