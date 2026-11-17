#!/bin/bash
# Pollinations Image-to-Image Editing
# Usage: ./image-edit.sh "edit instructions" --source "image_url_or_file" [--model kontext] [--seed N] [--output file]

set -e

PROMPT="$1"
shift || true

# Defaults
MODEL="${MODEL:-kontext}"
SEED="${SEED:-}"
OUTPUT="${OUTPUT:-}"
SOURCE=""
NEGATIVE=""

# URL encode function
urlencode() {
  local string="$1"
  local encoded=""
  local length="${#string}"
  for ((i = 0; i < length; i++)); do
    local c="${string:$i:1}"
    case $c in
      [a-zA-Z0-9.~_-]) encoded+="$c" ;;
      *) encoded+="%$(printf '%X' "'$c")" ;;
    esac
  done
  echo "$encoded"
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --source|--image)
      SOURCE="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --seed)
      SEED="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --negative)
      NEGATIVE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$PROMPT" || -z "$SOURCE" ]]; then
  echo "Usage: image-edit.sh \"edit instructions\" --source <image_url_or_file> [options]"
  echo ""
  echo "Options:"
  echo "  --source URL/FILE  Source image (URL or local file)"
  echo "  --model MODEL      Model (default: kontext)"
  echo "  --seed N           Seed for reproducibility"
  echo "  --negative TEXT    Negative prompt"
  echo "  --output FILE      Output filename"
  echo ""
  echo "Note: Local files are uploaded to https://media.pollinations.ai (10MB max). URL sources are faster."
  exit 1
fi

# Determine output filename
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="edited_$(date +%s).jpg"
fi

# Sanitize prompt
SANITIZED_PROMPT=$(echo "$PROMPT" | sed 's/%/percent/g')
ENCODED_PROMPT=$(urlencode "$SANITIZED_PROMPT")

if [[ -f "$SOURCE" ]]; then
  # Local file: upload to first-party media host (returns content-addressed hash URL)
  echo "Uploading local file to media.pollinations.ai..."
  UPLOAD_RESP=$(curl -s --max-time 120 \
    ${POLLINATIONS_API_KEY:+-H "Authorization: Bearer $POLLINATIONS_API_KEY"} \
    -X POST "https://media.pollinations.ai/upload" \
    -F "file=@$SOURCE")
  TEMP_URL=$(echo "$UPLOAD_RESP" | jq -r '.url // empty' 2>/dev/null)

  if [[ -z "$TEMP_URL" || ! "$TEMP_URL" =~ ^https?:// ]]; then
    echo "Error: Failed to upload local file."
    echo "$UPLOAD_RESP" | jq . 2>/dev/null || echo "$UPLOAD_RESP"
    exit 1
  fi

  echo "Uploaded: $TEMP_URL"
  SOURCE="$TEMP_URL"
fi

# Build GET URL with query params
PARAMS="model=$MODEL&image=$(urlencode "$SOURCE")"

if [[ -n "$SEED" ]]; then
  PARAMS="$PARAMS&seed=$SEED"
fi
if [[ -n "$NEGATIVE" ]]; then
  PARAMS="$PARAMS&negative_prompt=$(urlencode "$NEGATIVE")"
fi

URL="https://gen.pollinations.ai/image/$ENCODED_PROMPT?$PARAMS"

echo "Editing image: $PROMPT"
echo "Model: $MODEL"

curl -s --max-time 300 \
  ${POLLINATIONS_API_KEY:+-H "Authorization: Bearer $POLLINATIONS_API_KEY"} \
  -o "$OUTPUT" "$URL"

# Check if file was created
if [[ -s "$OUTPUT" ]]; then
  FILE_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
  echo "Saved to: $OUTPUT ($FILE_SIZE)"
else
  echo "Failed to edit image"
  exit 1
fi
