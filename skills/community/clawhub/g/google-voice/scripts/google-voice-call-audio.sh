#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)
export NODE_PATH="$SKILL_DIR/node_modules:${NODE_PATH:-}"
NUMBER=""; TEXT=""; AUDIO_PATH=""; DURATION="60"; AUTHUSER="${GV_AUTHUSER:-0}"; DRY_RUN="0"
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --number) NUMBER="$2"; shift ;;
    --text) TEXT="$2"; shift ;;
    --audio) AUDIO_PATH="$2"; shift ;;
    --duration) DURATION="$2"; shift ;;
    --authuser) AUTHUSER="$2"; shift ;;
    --dry-run) DRY_RUN="1" ;;
    --help|-h) cat <<'EOF'
Usage:
  GV_COOKIE_PATH=/private/google_voice_cookies.json scripts/google-voice-call-audio.sh --number '+1234567890' --text 'message' --duration 60 --authuser 0
  GV_COOKIE_PATH=/private/google_voice_cookies.json scripts/google-voice-call-audio.sh --number '+1234567890' --audio /path/audio.wav --duration 60
Options: --number, --text, --audio, --duration, --authuser, --dry-run
Safety: outbound calls are external actions. Confirm exact number and message/audio before use.
EOF
      exit 0 ;;
    *) if [[ -z "$NUMBER" ]]; then NUMBER="$1"; else echo "Unknown argument: $1" >&2; exit 2; fi ;;
  esac
  shift
done
if [[ -z "$NUMBER" ]]; then echo "--number is required" >&2; exit 2; fi
if [[ -z "$AUDIO_PATH" && -z "$TEXT" ]]; then echo "Either --text or --audio is required" >&2; exit 2; fi
if [[ -z "${GV_COOKIE_PATH:-}" && "$DRY_RUN" != "1" ]]; then echo "GV_COOKIE_PATH must point to a private cookie export outside the repo" >&2; exit 2; fi
if [[ -n "$AUDIO_PATH" && -z "$TEXT" && ! -f "$AUDIO_PATH" ]]; then echo "Audio file does not exist: $AUDIO_PATH" >&2; exit 2; fi
if [[ -n "$TEXT" ]]; then
  command -v edge-tts >/dev/null || { echo "edge-tts is required for --text" >&2; exit 2; }
  command -v ffmpeg >/dev/null || { echo "ffmpeg is required for --text" >&2; exit 2; }
  TIMESTAMP=$(date +%s); GREET_WAV="/tmp/gv_greet_$TIMESTAMP.wav"; SILENCE_WAV="/tmp/gv_silence_$TIMESTAMP.wav"; FINAL_WAV="/tmp/gv_call_final_$TIMESTAMP.wav"
  edge-tts --text "$TEXT" --write-media "/tmp/gv_tts_$TIMESTAMP.mp3" >/dev/null
  ffmpeg -i "/tmp/gv_tts_$TIMESTAMP.mp3" -ar 16000 -ac 1 "$GREET_WAV" -y >/dev/null 2>&1
  ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 600 "$SILENCE_WAV" -y >/dev/null 2>&1
  ffmpeg -i "$GREET_WAV" -i "$SILENCE_WAV" -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1" "$FINAL_WAV" -y >/dev/null 2>&1
  AUDIO_PATH="$FINAL_WAV"
fi
if [[ "$DRY_RUN" == "1" ]]; then printf '{"dryRun":true,"number":"%s","authuser":"%s","audioPath":"%s","duration":%s}\n' "$NUMBER" "$AUTHUSER" "$AUDIO_PATH" "$DURATION"; exit 0; fi
RECORDING_WEB="/tmp/gv_recorded_incoming.webm"; RECORDING_MP3="/tmp/gv_call_$(date +%Y%m%d_%H%M%S).mp3"; rm -f "$RECORDING_WEB"
node "$SKILL_DIR/scripts/google-voice-call-audio-engine.js" "$NUMBER" "$AUDIO_PATH" "$DURATION" "$AUTHUSER"
if [[ -f "$RECORDING_WEB" ]]; then ffmpeg -i "$RECORDING_WEB" -q:a 0 -map a "$RECORDING_MP3" -y >/dev/null 2>&1 || true; echo "FINISHED_FILE:$RECORDING_MP3"; fi
