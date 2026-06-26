#!/bin/bash
# verify_code.sh — Verify OTC confirmation code
# Usage: bash verify_code.sh <user_input>
#
# Reads the expected code from the secure state file.
# On successful match, the state file is deleted (single-use enforcement).
# Only exit codes are used — no code is ever printed to stdout.

set -euo pipefail

USER_INPUT="${1:-}"

STATE_DIR="${OTC_STATE_DIR:-${TMPDIR:-/tmp}/otc_state_$(id -u)}"
STATE_FILE="$STATE_DIR/pending"

if [ -z "$USER_INPUT" ]; then
  echo "Error: Missing user input argument." >&2
  exit 1
fi

if [ ! -f "$STATE_FILE" ]; then
  echo "Error: No pending OTC code found. Code may have expired or already been used." >&2
  exit 1
fi

EXPECTED=$(cat "$STATE_FILE")

if [ -z "$EXPECTED" ]; then
  echo "Error: State file is empty or corrupted." >&2
  rm -f "$STATE_FILE"
  exit 1
fi

# Exact match only — timing-safe comparison is not critical for
# short human-entered codes, but we use exit codes only (no echo).
if [ "$EXPECTED" = "$USER_INPUT" ]; then
  # Single-use: delete state file immediately after successful verification
  rm -f "$STATE_FILE"
  echo "VERIFIED" >&2
  exit 0
else
  echo "MISMATCH" >&2
  exit 1
fi
