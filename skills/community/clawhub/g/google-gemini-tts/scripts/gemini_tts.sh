#!/usr/bin/env bash
# gemini_tts.sh — Gemini TTS via REST API
# Usage: gemini_tts.sh [options] "text to speak"
#
# Options:
#   -v, --voice VOICE     Voice name (default: Kore)
#   -m, --model MODEL     TTS model (default: gemini-3.1-flash-tts-preview)
#   -o, --output FILE     Output file path (default: /tmp/gemini-tts-<timestamp>.wav)
#   -s, --style STYLE     Style/mood prompt prefix (e.g. "Say cheerfully:")
#   --multi SPEC          Multi-speaker: "Speaker1:Voice1,Speaker2:Voice2"
#   -h, --help            Show this help
#
# Auth: GEMINI_API_KEY env var (GOOGLE_API_KEY is also accepted as an alternative name).
#       Get one at https://aistudio.google.com/apikey. No ambient cloud credentials are used.
# Env:  GEMINI_API_VERSION (default: v1beta) — override when the endpoint is promoted to v1
# Requires: curl, jq, base64, ffmpeg (for PCM→WAV conversion)

set -euo pipefail

# --- defaults ---
VOICE="Kore"
MODEL="gemini-3.1-flash-tts-preview"
OUTPUT=""
STYLE=""
MULTI=""
TEXT=""

usage() {
  sed -n '2,/^$/s/^# //p' "$0"
  exit 0
}

die() { echo "ERROR: $*" >&2; exit 1; }

# --- parse args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    -v|--voice)  VOICE="$2";  shift 2 ;;
    -m|--model)  MODEL="$2";  shift 2 ;;
    -o|--output) OUTPUT="$2"; shift 2 ;;
    -s|--style)  STYLE="$2";  shift 2 ;;
    --multi)     MULTI="$2";  shift 2 ;;
    -h|--help)   usage ;;
    --)          shift; TEXT="$*"; break ;;
    -*)          die "Unknown option: $1" ;;
    *)           TEXT="$*"; break ;;
  esac
done

[[ -z "$TEXT" ]] && die "No text provided. Usage: gemini_tts.sh [options] \"text\""

# --- auth check ---
if [[ -z "${GEMINI_API_KEY:-}" && -n "${GOOGLE_API_KEY:-}" ]]; then
  GEMINI_API_KEY="$GOOGLE_API_KEY"
fi

if [[ -z "${GEMINI_API_KEY:-}" ]]; then
  die "GEMINI_API_KEY is not set. Get one at https://aistudio.google.com/apikey (GOOGLE_API_KEY is also accepted)."
fi

# --- deps check ---
for cmd in curl jq base64 ffmpeg; do
  command -v "$cmd" &>/dev/null || die "Required command not found: $cmd"
done

# --- output path ---
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="/tmp/gemini-tts-$(date +%s).wav"
fi

# Ensure output dir exists
mkdir -p "$(dirname "$OUTPUT")"

# --- build prompt ---
PROMPT="$TEXT"
if [[ -n "$STYLE" ]]; then
  PROMPT="${STYLE} ${TEXT}"
fi

# --- build speech config ---
if [[ -n "$MULTI" ]]; then
  # Multi-speaker mode: parse "Speaker1:Voice1,Speaker2:Voice2"
  SPEAKER_CONFIGS="[]"
  IFS=',' read -ra PAIRS <<< "$MULTI"
  for pair in "${PAIRS[@]}"; do
    IFS=':' read -r spk vce <<< "$pair"
    spk="$(echo "$spk" | xargs)"
    vce="$(echo "$vce" | xargs)"
    [[ -z "$spk" || -z "$vce" ]] && die "Invalid multi-speaker format. Use: Speaker1:Voice1,Speaker2:Voice2"
    SPEAKER_CONFIGS=$(echo "$SPEAKER_CONFIGS" | jq --arg s "$spk" --arg v "$vce" \
      '. + [{"speaker": $s, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": $v}}}]')
  done

  SPEECH_CONFIG=$(jq -n --argjson sc "$SPEAKER_CONFIGS" \
    '{"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": $sc}}')
else
  # Single-speaker mode
  SPEECH_CONFIG=$(jq -n --arg v "$VOICE" \
    '{"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": $v}}}')
fi

# --- build request body ---
BODY=$(jq -n \
  --arg model "$MODEL" \
  --arg text "$PROMPT" \
  --argjson speech "$SPEECH_CONFIG" \
  '{
    "model": $model,
    "contents": [{"parts": [{"text": $text}]}],
    "generationConfig": {
      "responseModalities": ["AUDIO"],
      "speechConfig": $speech
    }
  }')

# --- API call ---
TMPDIR_LOCAL="${TMPDIR:-/tmp}"
WORKDIR="$(mktemp -d "$TMPDIR_LOCAL/gemini-tts.XXXXXX")"
TMPFILE="$WORKDIR/response.json"
RAW_PCM="$WORKDIR/raw.pcm"
trap 'rm -rf "$WORKDIR" 2>/dev/null' EXIT

API_VERSION="${GEMINI_API_VERSION:-v1beta}"
API_URL="https://generativelanguage.googleapis.com/${API_VERSION}/models/${MODEL}:generateContent"

AUTH_HEADER="x-goog-api-key: $GEMINI_API_KEY"

# Retry on transient failures (5xx, 429). Max 3 attempts, 1s -> 2s -> 4s backoff.
MAX_ATTEMPTS=3
BACKOFF=1
ATTEMPT=1
HTTP_CODE=""
while (( ATTEMPT <= MAX_ATTEMPTS )); do
  HTTP_CODE=$(curl -s -w "%{http_code}" -o "$TMPFILE" \
    --connect-timeout 10 --max-time 60 \
    -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -H "$AUTH_HEADER" \
    -d "$BODY")

  if [[ "$HTTP_CODE" == "200" ]]; then
    break
  fi

  # Retry on 429 and 5xx; fail fast on 4xx (bad auth, malformed request, etc.)
  if [[ "$HTTP_CODE" == "429" || "$HTTP_CODE" =~ ^5[0-9][0-9]$ ]]; then
    if (( ATTEMPT < MAX_ATTEMPTS )); then
      echo "API error (HTTP $HTTP_CODE), retry ${ATTEMPT}/${MAX_ATTEMPTS} in ${BACKOFF}s..." >&2
      sleep "$BACKOFF"
      BACKOFF=$(( BACKOFF * 2 ))
      ATTEMPT=$(( ATTEMPT + 1 ))
      continue
    fi
  fi

  echo "API error (HTTP $HTTP_CODE):" >&2
  cat "$TMPFILE" >&2
  exit 1
done

# --- extract audio ---
AUDIO_B64=$(jq -r '.candidates[0].content.parts[0].inlineData.data // empty' "$TMPFILE")
[[ -z "$AUDIO_B64" ]] && die "No audio data in response. Response: $(cat "$TMPFILE")"

# Decode base64 to raw PCM
echo "$AUDIO_B64" | base64 --decode > "$RAW_PCM"

# Convert PCM (s16le, 24kHz, mono) to WAV. Surface ffmpeg failures instead of silently producing a broken file.
if ! ffmpeg -y -loglevel error \
  -f s16le -ar 24000 -ac 1 \
  -i "$RAW_PCM" \
  "$OUTPUT"; then
  die "ffmpeg conversion failed (raw PCM: $(wc -c < "$RAW_PCM") bytes at $RAW_PCM)"
fi

echo "$OUTPUT"
