#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=scripts/_lib.sh
source "$SCRIPT_DIR/_lib.sh"

if [ "$#" -lt 2 ]; then
  die "usage: $0 <text> <lang> <output_file> [options], or: $0 <lang> <output_file> [options] < text"
fi

READ_TEXT_FROM_STDIN=0
case "$1" in
  mn-Mong|mn-Cyrl|zh-Hans|en|ja|ko|ru)
    LANGUAGE="$1"
    OUTPUT="$2"
    shift 2
    TEXT=""
    READ_TEXT_FROM_STDIN=1
    ;;
  *)
    [ "$#" -ge 3 ] ||
      die "usage: $0 <text> <lang> <output_file> [options], or: $0 <lang> <output_file> [options] < text"
    TEXT="$1"
    LANGUAGE="$2"
    OUTPUT="$3"
    shift 3
    ;;
esac

VOICE="Kore"
SPEED="1.0"
SYNC=0
FORCE=0
POLL_TIMEOUT=900

while [ "$#" -gt 0 ]; do
  case "$1" in
    --voice)
      [ "$#" -ge 2 ] || die "--voice requires a name"
      VOICE="$2"
      shift 2
      ;;
    --speed)
      [ "$#" -ge 2 ] || die "--speed requires a number"
      SPEED="$2"
      shift 2
      ;;
    --sync)
      SYNC=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --timeout)
      [ "$#" -ge 2 ] || die "--timeout requires a number of seconds"
      POLL_TIMEOUT="$2"
      shift 2
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

if [ "$READ_TEXT_FROM_STDIN" -eq 1 ]; then
  TEXT=$(read_text_argument "$@")
fi

[ -n "$TEXT" ] || die "TTS text must not be empty"

case "$LANGUAGE" in
  mn-Mong|mn-Cyrl|zh-Hans|en|ja|ko|ru) ;;
  *) die "unsupported TTS language: $LANGUAGE" ;;
esac

case "$VOICE" in
  Kore|Puck|Zephyr|Charon|Fenrir|Aoede|Leda|Orus|Iapetus|Sulafat|Achird|Achernar) ;;
  *) die "unsupported TTS voice: $VOICE" ;;
esac

python3 - "$SPEED" <<'PY' ||
import sys
try:
    value = float(sys.argv[1])
except ValueError:
    raise SystemExit(1)
raise SystemExit(0 if 0.5 <= value <= 2.0 else 1)
PY
  die "--speed must be a number from 0.5 to 2.0"

case "$POLL_TIMEOUT" in
  *[!0-9]*|'') die "--timeout must be a positive integer" ;;
esac
[ "$POLL_TIMEOUT" -gt 0 ] || die "--timeout must be a positive integer"

if [ -e "$OUTPUT" ] && [ "$FORCE" -ne 1 ]; then
  die "output already exists; use --force to replace it: $OUTPUT"
fi

OUTPUT_DIR=$(dirname "$OUTPUT")
[ -d "$OUTPUT_DIR" ] || die "output directory does not exist: $OUTPUT_DIR"
[ -w "$OUTPUT_DIR" ] || die "output directory is not writable: $OUTPUT_DIR"

require_commands curl python3
load_key

HEADER_FILE=$(mktemp)
BODY_FILE=$(mktemp)
REQUEST_FILE=$(mktemp)
TEMP_OUTPUT=$(mktemp "${OUTPUT}.tmp.XXXXXX")
trap 'rm -f "$HEADER_FILE" "$BODY_FILE" "$REQUEST_FILE" "$TEMP_OUTPUT"' EXIT

commit_output() {
  if [ "$FORCE" -eq 1 ]; then
    mv -f "$TEMP_OUTPUT" "$OUTPUT"
    return 0
  fi
  if ! ln "$TEMP_OUTPUT" "$OUTPUT"; then
    die "output appeared while synthesis was running; use --force to replace it: $OUTPUT"
  fi
  rm -f "$TEMP_OUTPUT"
}

python3 - "$TEXT" "$LANGUAGE" "$VOICE" "$SPEED" > "$REQUEST_FILE" <<'PY'
import json
import sys

print(json.dumps({
    "text": sys.argv[1],
    "lang": sys.argv[2],
    "voice": sys.argv[3],
    "speed": float(sys.argv[4]),
}, ensure_ascii=False))
PY

if [ "$SYNC" -eq 1 ]; then
  perform_request POST "$HEADER_FILE" "$TEMP_OUTPUT" \
    "$BASE_URL/tts/" \
    -H "Authorization: Bearer $KEY" \
    -H "Content-Type: application/json" \
    --data-binary "@$REQUEST_FILE"

  validate_audio_file "$TEMP_OUTPUT" ||
    die "the synchronous TTS response was not recognized as WAV or MP3 audio"
  commit_output
  emit_billing_summary "$HEADER_FILE"
  printf '%s\n' "$OUTPUT"
  exit 0
fi

perform_request POST "$HEADER_FILE" "$BODY_FILE" \
  "$BASE_URL/tts/async/" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  --data-binary "@$REQUEST_FILE"

JOB_ID=$(extract_job_id "$BODY_FILE") ||
  die "the asynchronous TTS response did not contain a job identifier"
validate_job_id "$JOB_ID"

STARTED_AT=$SECONDS
while :; do
  if [ $((SECONDS - STARTED_AT)) -ge "$POLL_TIMEOUT" ]; then
    die "TTS polling timed out after ${POLL_TIMEOUT}s; the job may still be running: $JOB_ID"
  fi

  sleep 3
  perform_request GET "$HEADER_FILE" "$BODY_FILE" \
    "$BASE_URL/tts/async/$JOB_ID/" \
    -H "Authorization: Bearer $KEY"

  STATUS=$(json_status "$BODY_FILE")
  case "$STATUS" in
    done|completed|success)
      AUDIO_BASE64=$(json_extract_first "$BODY_FILE" audioBase64 audio_base64 data.audioBase64 data.audio_base64 2>/dev/null) ||
        die "the completed TTS job did not contain audio"
      python3 - "$AUDIO_BASE64" "$TEMP_OUTPUT" <<'PY'
import base64
import binascii
import sys

try:
    audio = base64.b64decode(sys.argv[1], validate=True)
except (ValueError, binascii.Error):
    raise SystemExit("invalid Base64 audio")
with open(sys.argv[2], "wb") as handle:
    handle.write(audio)
PY
      validate_audio_file "$TEMP_OUTPUT" ||
        die "the asynchronous TTS result was not recognized as WAV or MP3 audio"
      commit_output
      emit_billing_summary "$HEADER_FILE" "$BODY_FILE"
      printf '%s\n' "$OUTPUT"
      exit 0
      ;;
    failed|error)
      die "the asynchronous TTS job failed"
      ;;
    pending|processing|queued|unknown)
      ;;
    *)
      die "the asynchronous TTS job returned an unknown status: $STATUS"
      ;;
  esac
done
