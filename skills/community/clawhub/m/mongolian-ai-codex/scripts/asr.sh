#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=scripts/_lib.sh
source "$SCRIPT_DIR/_lib.sh"

if [ "$#" -lt 1 ]; then
  die "usage: $0 <audio_path> [language=mw] [--sync] [--timeout SECONDS]"
fi

AUDIO="$1"
shift
LANGUAGE="mw"
SYNC=0
POLL_TIMEOUT=900

if [ "$#" -gt 0 ] && [ "${1#--}" = "$1" ]; then
  LANGUAGE="$1"
  shift
fi

while [ "$#" -gt 0 ]; do
  case "$1" in
    --sync)
      SYNC=1
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

case "$POLL_TIMEOUT" in
  *[!0-9]*|'') die "--timeout must be a positive integer" ;;
esac
[ "$POLL_TIMEOUT" -gt 0 ] || die "--timeout must be a positive integer"

validate_file "$AUDIO"
validate_ocr_language "$LANGUAGE"

EXTENSION="${AUDIO##*.}"
EXTENSION=$(printf '%s' "$EXTENSION" | tr '[:upper:]' '[:lower:]')
case "$EXTENSION" in
  wav|mp3|m4a|aac|ogg|flac|pcm) ;;
  *) die "unsupported audio extension: $EXTENSION" ;;
esac

require_commands curl python3
load_key

HEADER_FILE=$(mktemp)
BODY_FILE=$(mktemp)
trap 'rm -f "$HEADER_FILE" "$BODY_FILE"' EXIT

if [ "$SYNC" -eq 1 ]; then
  perform_request POST "$HEADER_FILE" "$BODY_FILE" \
    "$BASE_URL/audio/" \
    -H "Authorization: Bearer $KEY" \
    -F "language=$LANGUAGE" \
    -F "sample_rate=16000" \
    -F "file=@$AUDIO"

  extract_business_value "$BODY_FILE" data.text
  emit_billing_summary "$HEADER_FILE" "$BODY_FILE"
  exit 0
fi

perform_request POST "$HEADER_FILE" "$BODY_FILE" \
  "$BASE_URL/audio/async/" \
  -H "Authorization: Bearer $KEY" \
  -F "language=$LANGUAGE" \
  -F "sample_rate=16000" \
  -F "file=@$AUDIO"

JOB_ID=$(extract_job_id "$BODY_FILE") ||
  die "the asynchronous ASR response did not contain a job identifier"
validate_job_id "$JOB_ID"

STARTED_AT=$SECONDS
while :; do
  if [ $((SECONDS - STARTED_AT)) -ge "$POLL_TIMEOUT" ]; then
    die "ASR polling timed out after ${POLL_TIMEOUT}s; the job may still be running: $JOB_ID"
  fi

  sleep 3
  perform_request GET "$HEADER_FILE" "$BODY_FILE" \
    "$BASE_URL/audio/async/$JOB_ID/" \
    -H "Authorization: Bearer $KEY"

  STATUS=$(json_status "$BODY_FILE")
  case "$STATUS" in
    done|completed|success)
      extract_business_value "$BODY_FILE" data.text
      emit_billing_summary "$HEADER_FILE" "$BODY_FILE"
      exit 0
      ;;
    failed|error)
      die "the asynchronous ASR job failed"
      ;;
    pending|processing|queued|unknown)
      if [ "$HTTP_STATUS" = "200" ]; then
        if json_extract_first "$BODY_FILE" data.text >/dev/null 2>&1; then
          extract_business_value "$BODY_FILE" data.text
          emit_billing_summary "$HEADER_FILE" "$BODY_FILE"
          exit 0
        fi
      fi
      ;;
    *)
      die "the asynchronous ASR job returned an unknown status: $STATUS"
      ;;
  esac
done
