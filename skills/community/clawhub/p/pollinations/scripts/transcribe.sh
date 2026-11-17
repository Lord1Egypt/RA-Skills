#!/bin/bash
# Pollinations Audio Transcription (Whisper-compatible /v1/audio/transcriptions)
# Usage: ./transcribe.sh "audio_file_or_url" [--model whisper-large-v3] [--language en] [--prompt "..."] [--format json]

set -e

AUDIO_INPUT="$1"
shift || true

# Defaults
MODEL="${MODEL:-whisper-large-v3}"
LANGUAGE="${LANGUAGE:-}"
PROMPT="${PROMPT:-}"
FORMAT="${FORMAT:-json}"
TEMPERATURE="${TEMPERATURE:-}"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      MODEL="$2"
      shift 2
      ;;
    --language|--lang)
      LANGUAGE="$2"
      shift 2
      ;;
    --prompt)
      PROMPT="$2"
      shift 2
      ;;
    --format|--response-format)
      FORMAT="$2"
      shift 2
      ;;
    --temperature|--temp)
      TEMPERATURE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$AUDIO_INPUT" ]]; then
  echo "Usage: transcribe.sh <audio_file_or_url> [options]"
  echo ""
  echo "Options:"
  echo "  --model MODEL          whisper-large-v3 (default), whisper-1, scribe"
  echo "  --language CODE        ISO-639-1 language hint (e.g. en, fr, ja)"
  echo "  --prompt TEXT          Optional context/style prompt"
  echo "  --format FORMAT        json (default), text, srt, vtt, verbose_json"
  echo "  --temperature N        Sampling temperature 0-1"
  echo ""
  echo "Formats: mp3, mp4, mpeg, mpga, m4a, wav, webm"
  exit 1
fi

# If URL, download to temp file
TEMP_AUDIO=""
if [[ ! -f "$AUDIO_INPUT" ]]; then
  # Only fetch http(s) URLs: curl would otherwise read file://, ftp://, etc.
  if [[ ! "$AUDIO_INPUT" =~ ^https?:// ]]; then
    echo "Error: input must be an existing local file or an http(s) URL."
    exit 1
  fi
  echo "Downloading audio..."
  TEMP_AUDIO=$(mktemp "${TMPDIR:-/tmp}/audio_dl_XXXXXX")
  trap 'rm -f "$TEMP_AUDIO"' EXIT
  curl -sSL --proto '=http,https' --proto-redir '=http,https' --max-filesize 26214400 --max-time 120 \
    -o "$TEMP_AUDIO" "$AUDIO_INPUT"
  AUDIO_INPUT="$TEMP_AUDIO"
fi

echo "Transcribing with $MODEL..."

# Build curl form options
FORM_ARGS=( -F "file=@$AUDIO_INPUT" -F "model=$MODEL" -F "response_format=$FORMAT" )
[[ -n "$LANGUAGE" ]] && FORM_ARGS+=( -F "language=$LANGUAGE" )
[[ -n "$PROMPT" ]] && FORM_ARGS+=( -F "prompt=$PROMPT" )
[[ -n "$TEMPERATURE" ]] && FORM_ARGS+=( -F "temperature=$TEMPERATURE" )

RESPONSE=$(curl -s --max-time 600 \
  ${POLLINATIONS_API_KEY:+-H "Authorization: Bearer $POLLINATIONS_API_KEY"} \
  -X POST "https://gen.pollinations.ai/v1/audio/transcriptions" \
  "${FORM_ARGS[@]}")

# For json format, extract .text; otherwise print as-is
if [[ "$FORMAT" == "json" || "$FORMAT" == "verbose_json" ]]; then
  RESULT=$(echo "$RESPONSE" | jq -r '.text // empty' 2>/dev/null)
  if [[ -n "$RESULT" ]]; then
    echo "$RESULT"
  elif echo "$RESPONSE" | jq -e 'has("text")' >/dev/null 2>&1; then
    echo "No speech detected in the audio."
  else
    echo "Error: Failed to transcribe audio"
    echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
    exit 1
  fi
else
  echo "$RESPONSE"
fi
