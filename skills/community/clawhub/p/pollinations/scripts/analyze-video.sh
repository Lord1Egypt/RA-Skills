#!/bin/bash
# Pollinations Video Analysis
# Usage: ./analyze-video.sh "video_url_or_file" [--prompt "describe this"] [--model gemini]

set -e

VIDEO_INPUT="$1"
shift || true

# Defaults
PROMPT="${PROMPT:-Describe this video in detail}"
MODEL="${MODEL:-gemini}"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --prompt)
      PROMPT="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$VIDEO_INPUT" ]]; then
  echo "Usage: analyze-video.sh <video_url_or_file> [--prompt \"...\"] [--model gemini]"
  echo "Models: gemini (default, paid), gemini-large (needs a model with video input)"
  echo "Formats: MP4, MOV, AVI"
  exit 1
fi

# Build JSON body using temp files to avoid ARG_MAX limits with large base64 data
BODY_FILE=$(mktemp "${TMPDIR:-/tmp}/video_body_XXXXXX")
trap "rm -f '$BODY_FILE'" EXIT

if [[ -f "$VIDEO_INPUT" ]]; then
  # Local file: send as a data URI in a video_url part (input_video is ignored by the API)
  case "$VIDEO_INPUT" in
    *.mov|*.MOV) MIME="video/quicktime" ;;
    *.avi|*.AVI) MIME="video/x-msvideo" ;;
    *.webm|*.WEBM) MIME="video/webm" ;;
    *) MIME="video/mp4" ;;
  esac

  BASE64_FILE=$(mktemp "${TMPDIR:-/tmp}/video_b64_XXXXXX")
  trap "rm -f '$BODY_FILE' '$BASE64_FILE'" EXIT
  { printf 'data:%s;base64,' "$MIME"; base64 < "$VIDEO_INPUT" | tr -d '\n'; } > "$BASE64_FILE"

  # Build JSON from a file to avoid shell arg limits
  jq -n -c --rawfile data "$BASE64_FILE" \
    --arg model "$MODEL" \
    --arg prompt "$PROMPT" \
    '{
      model: $model,
      messages: [{
        role: "user",
        content: [
          {type: "text", text: $prompt},
          {type: "video_url", video_url: {url: $data}}
        ]
      }]
    }' > "$BODY_FILE"
else
  # URL input
  jq -n -c \
    --arg model "$MODEL" \
    --arg prompt "$PROMPT" \
    --arg url "$VIDEO_INPUT" \
    '{
      model: $model,
      messages: [{
        role: "user",
        content: [
          {type: "text", text: $prompt},
          {type: "video_url", video_url: {url: $url}}
        ]
      }]
    }' > "$BODY_FILE"
fi

# Make request (longer timeout for video processing)
echo "Analyzing video with $MODEL..."

RESPONSE=$(curl -s --max-time 300 -H "Content-Type: application/json" \
  ${POLLINATIONS_API_KEY:+-H "Authorization: Bearer $POLLINATIONS_API_KEY"} \
  -X POST "https://gen.pollinations.ai/v1/chat/completions" \
  -d @"$BODY_FILE")

# Extract result
RESULT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // empty')

if [[ -n "$RESULT" ]]; then
  echo "$RESULT"
else
  echo "Error: Failed to analyze video"
  echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
  exit 1
fi
