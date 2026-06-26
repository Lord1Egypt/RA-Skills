#!/usr/bin/env bash
# format.sh — local checksum verification + formatting (no API call, no key needed).
#
# Usage:
#   scripts/format.sh <bno> [<bno> ...]
#
# Reads from $@; if none given, reads one b_no per line from stdin.
# Output: JSONL with {input, normalized, formatted, valid_checksum}.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

require_bin jq

emit_one() {
  local raw="$1" norm fmt valid
  norm=$(strip_bno "$raw")
  fmt=$(format_bno "$norm")
  if checksum_bno "$norm"; then
    valid=true
  else
    valid=false
  fi
  jq -nc \
    --arg input "$raw" \
    --arg norm "$norm" \
    --arg fmt "$fmt" \
    --argjson valid "$valid" \
    '{input:$input, normalized:$norm, formatted:$fmt, valid_checksum:$valid}'
}

if [[ $# -gt 0 ]]; then
  for arg in "$@"; do emit_one "$arg"; done
else
  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    emit_one "$line"
  done
fi
