#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SUBMIT_SCRIPT="$SCRIPT_DIR/manus_submit.sh"

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 'Manus, generate an image of a rainy forest'" >&2
  exit 1
fi

INPUT="$*"

normalize() {
  local s="$1"
  s="${s#manus}"
  s="${s#Manus}"
  s="${s#MANUS}"
  s="${s#,}"
  s="${s#:}"
  while [[ "$s" == ' '* ]]; do s="${s# }"; done
  printf '%s' "$s"
}

PROMPT="$(normalize "$INPUT")"

if [[ -z "$PROMPT" ]]; then
  echo "Empty Manus prompt after normalization" >&2
  exit 1
fi

exec "$SUBMIT_SCRIPT" "$PROMPT"
