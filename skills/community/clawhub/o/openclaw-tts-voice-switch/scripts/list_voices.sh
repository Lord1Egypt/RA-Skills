#!/usr/bin/env bash
set -euo pipefail

LANGUAGE_FILTER="${1:-}"
CONFIG_PATH="${HOME}/.openclaw/openclaw.json"

api_key=""

if [[ -f "$CONFIG_PATH" ]]; then
  api_key="$(jq -r '.messages.tts.elevenlabs.apiKey // empty' "$CONFIG_PATH")"
fi

if [[ -z "$api_key" && -n "${ELEVENLABS_API_KEY:-}" ]]; then
  api_key="$ELEVENLABS_API_KEY"
fi

if [[ -z "$api_key" && -n "${XI_API_KEY:-}" ]]; then
  api_key="$XI_API_KEY"
fi

if [[ -z "$api_key" ]]; then
  echo "missing ElevenLabs API key in ~/.openclaw/openclaw.json or ELEVENLABS_API_KEY/XI_API_KEY" >&2
  exit 1
fi

raw="$(curl -sS https://api.elevenlabs.io/v1/voices -H "xi-api-key: $api_key")"

if [[ -z "$LANGUAGE_FILTER" ]]; then
  jq -r '
    .voices[]
    | {
        name,
        voice_id,
        langs: ([.verified_languages[]? | .language] | unique | sort | join(",")),
        locales: ([.verified_languages[]? | .locale // empty] | map(select(length > 0)) | unique | sort | join(",")),
        models: ([.verified_languages[]? | .model_id] | unique | sort | join(","))
      }
    | [.name, .voice_id, .langs, .locales, .models]
    | @tsv
  ' <<<"$raw"
else
  jq -r --arg lang "$LANGUAGE_FILTER" '
    .voices[]
    | select(any(.verified_languages[]?; .language == $lang))
    | {
        name,
        voice_id,
        locales: ([.verified_languages[]? | select(.language == $lang) | .locale // empty] | map(select(length > 0)) | unique | sort | join(",")),
        models: ([.verified_languages[]? | select(.language == $lang) | .model_id] | unique | sort | join(","))
      }
    | [.name, .voice_id, $lang, .locales, .models]
    | @tsv
  ' <<<"$raw"
fi
