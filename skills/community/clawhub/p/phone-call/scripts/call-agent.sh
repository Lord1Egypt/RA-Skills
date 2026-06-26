#!/usr/bin/env bash
# Start a macOS Phone/FaceTime call, optionally speak an intro, then speak each
# line received on stdin. Useful for OpenClaw agents that generate text replies.
#
# Examples:
#   scripts/call-agent.sh +491234567890 --intro "Hallo, ich bin der Agent."
#   printf 'Satz eins\nSatz zwei\n' | scripts/call-agent.sh --no-call +491234567890

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NUMBER=""
INTRO=""
NO_CALL=0
CALL_ARGS=()

usage() {
  cat <<EOF
Usage: $0 [--no-call] [--intro text] [call.sh options] <phone-number>

Starts a Mac phone call using call.sh, speaks --intro if provided, then reads
stdin line-by-line and speaks each line with speak.sh until EOF.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --intro)
      INTRO="${2:-}"; shift 2 ;;
    --no-call)
      NO_CALL=1; shift ;;
    --dry-run|--no-confirm|--confirm)
      CALL_ARGS+=("$1"); shift ;;
    --scheme|--timeout)
      CALL_ARGS+=("$1" "${2:-}"); shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      NUMBER="$1"; shift ;;
  esac
done

if [[ -z "$NUMBER" ]]; then
  usage >&2
  exit 1
fi

if [[ "$NO_CALL" != "1" ]]; then
  "$SCRIPT_DIR/call.sh" "${CALL_ARGS[@]}" "$NUMBER"
  sleep "${PHONE_CALL_SETTLE_SECONDS:-2}"
fi

if [[ -n "$INTRO" ]]; then
  "$SCRIPT_DIR/speak.sh" "$INTRO"
fi

if [[ ! -t 0 ]]; then
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    "$SCRIPT_DIR/speak.sh" "$line"
  done
fi
