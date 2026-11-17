#!/bin/bash
# Pollinations Text-to-Speech (OpenAI-compatible /v1/audio/speech)
# Usage: ./tts.sh "text" [--voice voice] [--format format] [--speed N] [--output file]

set -e

TEXT="$1"
shift || true

# Defaults
VOICE="${VOICE:-nova}"
FORMAT="${FORMAT:-mp3}"
MODEL="${MODEL:-tts-1}"
SPEED="${SPEED:-}"
OUTPUT="${OUTPUT:-}"
SEED="${SEED:-}"
INSTRUCT="${INSTRUCT:-}"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --voice)
      VOICE="$2"
      shift 2
      ;;
    --format)
      FORMAT="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --speed)
      SPEED="$2"
      shift 2
      ;;
    --seed)
      SEED="$2"
      shift 2
      ;;
    --instruct)
      INSTRUCT="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$TEXT" ]]; then
  echo "Usage: tts.sh \"text\" [--voice nova] [--format mp3] [--speed 1.0] [--output file]"
  echo ""
  echo "Voices (35): alloy echo fable onyx nova shimmer ash ballad coral sage verse"
  echo "             rachel domi bella elli charlotte dorothy sarah emily lily matilda"
  echo "             adam antoni arnold josh sam daniel charlie james fin callum liam"
  echo "             george brian bill"
  echo "Formats: mp3 (default), opus, aac, flac, wav, pcm"
  echo "Models:  tts-1 (default), elevenmusic, acestep, qwen-tts-instruct"
  exit 1
fi

# Determine output filename
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="speech_$(date +%s).$FORMAT"
fi

# Build request body
BODY=$(jq -n -c \
  --arg model "$MODEL" \
  --arg input "$TEXT" \
  --arg voice "$VOICE" \
  --arg format "$FORMAT" \
  '{model: $model, input: $input, voice: $voice, response_format: $format}')

if [[ -n "$SPEED" ]]; then
  BODY=$(echo "$BODY" | jq -c --arg v "$SPEED" '. + {speed: ($v | tonumber)}')
fi
if [[ -n "$SEED" ]]; then
  BODY=$(echo "$BODY" | jq -c --arg v "$SEED" '. + {seed: ($v | tonumber)}')
fi
if [[ -n "$INSTRUCT" ]]; then
  BODY=$(echo "$BODY" | jq -c --arg v "$INSTRUCT" '. + {instruct: $v}')
fi

echo "Generating audio with $MODEL ($VOICE, $FORMAT)..."

curl -s --max-time 300 -H "Content-Type: application/json" \
  ${POLLINATIONS_API_KEY:+-H "Authorization: Bearer $POLLINATIONS_API_KEY"} \
  -X POST "https://gen.pollinations.ai/v1/audio/speech" \
  -d "$BODY" -o "$OUTPUT"

# Check if file was created and is binary audio (not a JSON error)
if [[ -s "$OUTPUT" ]]; then
  # If response is small and starts with '{', it's likely a JSON error
  if [[ $(stat -c%s "$OUTPUT" 2>/dev/null || stat -f%z "$OUTPUT") -lt 1024 ]] && head -c1 "$OUTPUT" | grep -q '{'; then
    echo "Error response:"
    cat "$OUTPUT"
    rm "$OUTPUT"
    exit 1
  fi
  FILE_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
  echo "Saved to: $OUTPUT ($FILE_SIZE)"
else
  echo "Failed to generate audio"
  exit 1
fi
