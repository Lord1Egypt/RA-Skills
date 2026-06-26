#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <target> <message> [media_path]" >&2
  exit 1
fi

TARGET="$1"
MESSAGE="$2"
MEDIA_PATH="${3:-}"
MAX_RETRIES="${MAX_RETRIES:-6}"
SLEEP_SECONDS="${SLEEP_SECONDS:-5}"
CHANNEL="${CHANNEL:-telegram}"

attempt=1
while [[ $attempt -le $MAX_RETRIES ]]; do
  echo "[retry-send] attempt ${attempt}/${MAX_RETRIES}" >&2
  set +e
  if [[ -n "$MEDIA_PATH" ]]; then
    output=$(openclaw message send --channel "$CHANNEL" --target "$TARGET" --message "$MESSAGE" --media "$MEDIA_PATH" --json 2>&1)
    status=$?
  else
    output=$(openclaw message send --channel "$CHANNEL" --target "$TARGET" --message "$MESSAGE" --json 2>&1)
    status=$?
  fi
  set -e
  echo "$output"
  if [[ $status -eq 0 ]]; then
    exit 0
  fi
  if [[ $attempt -lt $MAX_RETRIES ]]; then
    sleep "$SLEEP_SECONDS"
  fi
  attempt=$((attempt + 1))
done

exit 1
