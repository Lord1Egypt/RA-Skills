#!/bin/bash
set -euo pipefail

# MiniMax TTS Voice Message Script (Trinity XiaoYe Edition)
#
# Usage:
#   tts-xiaoye.sh "text to speak"
#   tts-xiaoye.sh "text" [voiceID] [target]
#   tts-xiaoye.sh --text "text" [--voice VoiceID] [--target TelegramChatId] [--caption "caption text"]
#   tts-xiaoye.sh --text "text" --feishu [--caption "caption text"]
#   tts-xiaoye.sh --list-voices
#
# Channels:
#   - Default / Telegram: TTS MP3 -> sendVoice (native voice bubble, no transcoding)
#   - --feishu: TTS MP3 -> FFmpeg convert to OGG/Opus -> Feishu native voice bubble
#   - --generate-only: TTS MP3 only, no sending

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="$WORKSPACE/skills/minimax-tts-cn"
TTS_PY="$SKILL_DIR/scripts/tts.py"
AUDIO_DIR="$WORKSPACE/generated/tts-audio"
FFMPEG="$(command -v ffmpeg 2>/dev/null || echo "")"

# Load env vars from .env file (if exists) — required: MINIMAX_API_KEY; optional: TELEGRAM_BOT_TOKEN, TELEGRAM_TARGET
ENV_FILE="$SKILL_DIR/.env"
if [[ -f "$ENV_FILE" ]]; then
  while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" == \#* ]] && continue
    value=$(echo "$value" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")
    [[ -n "$value" ]] && export "$key=$value"
  done < "$ENV_FILE"
fi

DEFAULT_TARGET="${TELEGRAM_TARGET:-}"
DEFAULT_MODEL="${TTS_MODEL:-speech-2.8-hd}"
BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"

TEXT=""
VOICE="Chinese (Mandarin)_Warm_Girl"
TARGET=""
CAPTION=""
GENERATE_ONLY="0"
FEISHU_MODE="0"
POSITIONAL=()

usage() {
  cat <<'EOF'
Usage:
  tts-xiaoye.sh "text to speak"
  tts-xiaoye.sh "text" [voiceID] [target]
  tts-xiaoye.sh --text "text" [--voice VoiceID] [--target TelegramChatId] [--caption "caption text"]
  tts-xiaoye.sh --text "text" --feishu [--caption "caption text"]

Examples:
  # Telegram voice message (MP3, no transcoding)
  bash tts-xiaoye.sh "Voice content"

  # Telegram voice with caption
  bash tts-xiaoye.sh --text "Voice content" --caption "Voice content"

  # Feishu native voice bubble (auto-transcode to OGG/Opus)
  bash tts-xiaoye.sh --text "Feishu voice content" --feishu

  # Generate MP3 only, no sending
  bash tts-xiaoye.sh --text "Voice content" --generate-only
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text)
      TEXT="${2:-}"
      shift 2
      ;;
    --voice)
      VOICE="${2:-}"
      shift 2
      ;;
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --caption)
      CAPTION="${2:-}"
      shift 2
      ;;
    --feishu)
      FEISHU_MODE="1"
      shift
      ;;
    --list-voices)
      python3 "$TTS_PY" --list-voices
      exit 0
      ;;
    --generate-only)
      GENERATE_ONLY="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      while [[ $# -gt 0 ]]; do
        POSITIONAL+=("$1")
        shift
      done
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

# Positional args: text, voice, target
if [[ -z "$TEXT" && ${#POSITIONAL[@]} -gt 0 ]]; then
  TEXT="${POSITIONAL[0]}"
fi
if [[ ${#POSITIONAL[@]} -gt 1 ]]; then
  VOICE="${POSITIONAL[1]}"
fi
if [[ ${#POSITIONAL[@]} -gt 2 ]]; then
  TARGET="${POSITIONAL[2]}"
fi

if [[ -z "$TEXT" ]]; then
  usage
  exit 1
fi

if [[ ! -f "$TTS_PY" ]]; then
  echo "❌ TTS script not found: $TTS_PY" >&2
  exit 1
fi

mkdir -p "$AUDIO_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
AUDIO_FILE="$AUDIO_DIR/tts-xiaoye-${TIMESTAMP}.mp3"

# Generate TTS MP3
python3 "$TTS_PY" \
  "$TEXT" \
  --voice "$VOICE" \
  --model "$DEFAULT_MODEL" \
  --output "$AUDIO_FILE" >/dev/null

# --feishu: transcode to OGG/Opus, return path for openclaw message send
if [[ "$FEISHU_MODE" == "1" ]]; then
  if [[ -z "$FFMPEG" ]]; then
    echo "❌ ffmpeg not found, cannot convert to OGG format" >&2
    exit 1
  fi
  OPUS_FILE="${AUDIO_FILE%.mp3}.opus"
  # Convert MP3 -> OGG/Opus (Feishu native voice bubble format)
  "$FFMPEG" -y -i "$AUDIO_FILE" -acodec libopus -vn "$OPUS_FILE" 2>/dev/null
  printf '{"ok":true,"mode":"feishu","audio_file":"%s","voice":"%s","caption":"%s"}\n' \
    "$OPUS_FILE" "$VOICE" "$CAPTION"
  exit 0
fi

# --generate-only: return MP3 path only
if [[ "$GENERATE_ONLY" == "1" ]]; then
  printf '{"ok":true,"mode":"generate","audio_file":"%s","voice":"%s","caption":"%s"}\n' \
    "$AUDIO_FILE" "$VOICE" "$CAPTION"
  exit 0
fi

# Default: Telegram voice message (MP3 direct send, no transcoding)
TARGET="${TARGET:-$DEFAULT_TARGET}"
if [[ -z "$TARGET" ]]; then
  echo "❌ Telegram target is empty" >&2
  exit 1
fi

# sendVoice: plain voice bubble; with caption = voice + text display
if [[ -n "$CAPTION" ]]; then
  RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendVoice" \
    -F "chat_id=${TARGET}" \
    -F "voice=@${AUDIO_FILE}" \
    -F "caption=${CAPTION}")
else
  RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendVoice" \
    -F "chat_id=${TARGET}" \
    -F "voice=@${AUDIO_FILE}")
fi

printf '{"ok":true,"mode":"send-voice","target":"%s","audio_file":"%s","voice":"%s","caption":"%s"}\n' \
  "$TARGET" "$AUDIO_FILE" "$VOICE" "$CAPTION"
