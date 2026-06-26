#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 4 ]]; then
  echo "usage: $0 <voiceId> [languageCode] [modelId] [apiKey]" >&2
  exit 1
fi

VOICE_ID="$1"
LANGUAGE_CODE="${2:-zh}"
MODEL_ID="${3:-eleven_multilingual_v2}"
API_KEY="${4:-}"
CONFIG_PATH="${HOME}/.openclaw/openclaw.json"
BACKUP_PATH="${HOME}/.openclaw/openclaw.json.bak.voice-switch"

if [[ ! -f "$CONFIG_PATH" ]]; then
  echo "config not found: $CONFIG_PATH" >&2
  exit 1
fi

cp "$CONFIG_PATH" "$BACKUP_PATH"

tmp_file="$(mktemp)"
jq --arg voiceId "$VOICE_ID" --arg languageCode "$LANGUAGE_CODE" --arg modelId "$MODEL_ID" --arg apiKey "$API_KEY" '
  .messages.tts as $existingTts |
  .messages.tts = {
    "auto": (($existingTts.auto // "always")),
    "provider": "elevenlabs",
    "elevenlabs": (
      ($existingTts.elevenlabs // {})
      + {
        "modelId": $modelId,
        "languageCode": $languageCode,
        "voiceId": $voiceId
      }
      + (if ($apiKey | length) > 0 then {"apiKey": $apiKey} else {} end)
    )
  }
' "$CONFIG_PATH" > "$tmp_file"

mv "$tmp_file" "$CONFIG_PATH"
openclaw gateway restart >/dev/null

echo "updated $CONFIG_PATH"
echo "messages.tts.elevenlabs.voiceId=$VOICE_ID"
echo "messages.tts.elevenlabs.languageCode=$LANGUAGE_CODE"
echo "messages.tts.elevenlabs.modelId=$MODEL_ID"
if [[ -n "$API_KEY" ]]; then
  echo "messages.tts.elevenlabs.apiKey=<updated>"
fi
