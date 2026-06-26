#!/bin/bash
# Video/Audio Transcription using Gladia API
# Part of video-transcription skill
# Usage: ./youtube_transcribe.sh "AUDIO_VIDEO_URL" [output_file]

set -e

# Get API key from environment - MUST be set before running
if [ -z "$GLADIA_API_KEY" ]; then
    echo "Error: GLADIA_API_KEY environment variable not set"
    echo "Please set it before running: export GLADIA_API_KEY='your-api-key'"
    exit 1
fi

AUDIO_URL="${1:-}"
OUTPUT_FILE="${2:-}"

if [ -z "$AUDIO_URL" ]; then
    echo "Usage: $0 <audio/video_url> [output_file]"
    echo "Example: $0 \"https://youtube.com/watch?v=xxx\""
    echo "Example: $0 \"https://example.com/audio.mp3\" /path/to/output.txt"
    exit 1
fi

# Get script directory for relative paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create transcripts directory if needed
TRANSCRIPT_DIR="${SCRIPT_DIR}/transcripts"
mkdir -p "$TRANSCRIPT_DIR"

echo "Submitting transcription job..."
RESPONSE=$(curl -s -X POST "https://api.gladia.io/v2/pre-recorded" \
    -H "x-gladia-key: $GLADIA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"audio_url\": \"$AUDIO_URL\"}")

JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id', ''))")

if [ -z "$JOB_ID" ]; then
    echo "Error: Failed to get job ID"
    echo "$RESPONSE"
    exit 1
fi

echo "Job ID: $JOB_ID"
echo "Waiting for transcription..."

# Poll for result (max 5 minutes)
for i in {1..30}; do
    RESULT=$(curl -s -X GET "https://api.gladia.io/v2/pre-recorded/$JOB_ID" \
        -H "x-gladia-key: $GLADIA_API_KEY")
    
    STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status', ''))")
    
    if [ "$STATUS" = "done" ]; then
        echo "Transcription complete!"
        TRANSCRIPT=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result', {}).get('transcription', {}).get('full_transcript', 'N/A'))")
        
        if [ -n "$OUTPUT_FILE" ]; then
            echo "$TRANSCRIPT" > "$OUTPUT_FILE"
            echo "Saved to: $OUTPUT_FILE"
        else
            echo "$TRANSCRIPT"
        fi
        exit 0
    elif [ "$STATUS" = "error" ]; then
        echo "Error during transcription"
        echo "$RESULT"
        exit 1
    fi
    
    echo "Status: $STATUS - waiting..."
    sleep 10
done

echo "Timeout waiting for transcription"
exit 1
