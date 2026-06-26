#!/usr/bin/env bash
# Speak into/near the active Mac phone call using local speaker playback.
# Usage: speak.sh "Text to say"
# Prefer sag (ElevenLabs) when an API key is configured; fallback to macOS say.

set -euo pipefail

VOICE_MODEL="${PHONE_CALL_TTS_MODEL:-eleven_flash_v2_5}"
VOICE_ID="${PHONE_CALL_TTS_VOICE:-}"
RATE="${PHONE_CALL_SAY_RATE:-185}"
TEXT="$*"

if [[ -z "$TEXT" && ! -t 0 ]]; then
  TEXT="$(cat)"
fi

if [[ -z "$TEXT" ]]; then
  echo "Usage: $0 <text>" >&2
  exit 1
fi

# Only try sag when it has credentials available. This avoids noisy --help output
# and makes the fallback deterministic on fresh systems.
if command -v sag >/dev/null 2>&1 && { [[ -n "${ELEVENLABS_API_KEY:-}" ]] || [[ -n "${ELEVENLABS_API_KEY_FILE:-}" ]]; }; then
  SAG_ARGS=(speak --model-id "$VOICE_MODEL")
  [[ -n "$VOICE_ID" ]] && SAG_ARGS+=(--voice "$VOICE_ID")
  if sag "${SAG_ARGS[@]}" "$TEXT"; then
    exit 0
  fi
  echo "sag failed; falling back to macOS say" >&2
fi

exec say -r "$RATE" "$TEXT"
