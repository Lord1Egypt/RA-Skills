#!/usr/bin/env bash
# Transcribe audio files using Groq Whisper API
# Usage: transcribe.sh <audio_file> [language]
# Requires: GROQ_API_KEY env var or ~/.config/groq/credentials.json

set -euo pipefail

AUDIO_FILE="${1:?Usage: transcribe.sh <audio_file> [language]}"
LANGUAGE="${2:-en}"

# Resolve API key: env var first, then credentials file
GROQ_API_KEY="${GROQ_API_KEY:-}"
if [[ -z "$GROQ_API_KEY" ]]; then
    CREDS="$HOME/.config/groq/credentials.json"
    if [[ -f "$CREDS" ]] && command -v jq &>/dev/null; then
        GROQ_API_KEY=$(jq -r '.api_key // empty' "$CREDS" 2>/dev/null)
    fi
fi

if [[ -z "$GROQ_API_KEY" ]]; then
    echo "Error: No Groq API key found." >&2
    echo "Set GROQ_API_KEY env var or create ~/.config/groq/credentials.json:" >&2
    echo '  {"api_key":"gsk_your_key_here"}' >&2
    exit 1
fi

if [[ ! -f "$AUDIO_FILE" ]]; then
    echo "Error: File not found: $AUDIO_FILE" >&2
    exit 1
fi

result=$(curl -s -X POST "https://api.groq.com/openai/v1/audio/transcriptions" \
    -H "Authorization: Bearer $GROQ_API_KEY" \
    -F "file=@${AUDIO_FILE}" \
    -F "model=whisper-large-v3" \
    -F "response_format=json" \
    -F "language=${LANGUAGE}" 2>&1)

# Check for errors
error=$(echo "$result" | jq -r '.error.message // empty' 2>/dev/null)
if [[ -n "$error" ]]; then
    echo "Groq API error: $error" >&2
    exit 1
fi

text=$(echo "$result" | jq -r '.text // empty' 2>/dev/null)
if [[ -z "$text" ]]; then
    echo "Error: No transcription returned" >&2
    echo "$result" >&2
    exit 1
fi

echo "$text"
