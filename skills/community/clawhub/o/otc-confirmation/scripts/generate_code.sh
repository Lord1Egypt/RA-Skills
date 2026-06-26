#!/bin/bash
# generate_code.sh — Generate a random OTC confirmation code
# Usage: bash generate_code.sh [prefix] [length]
# Default: cf-XXXX (prefix="cf", length=4)
#
# The code is written to a secure state file (mode 600).
# It is NEVER printed to stdout to prevent leakage.
# Other scripts (send_otc_email.sh, verify_code.sh) read from the state file.

set -eu

PREFIX="${1:-${OTC_CODE_PREFIX:-cf}}"
LENGTH="${2:-${OTC_CODE_LENGTH:-4}}"

# Use a per-user state directory
STATE_DIR="${OTC_STATE_DIR:-${TMPDIR:-/tmp}/otc_state_$(id -u)}"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR"

STATE_FILE="$STATE_DIR/pending"

# Generate cryptographically secure random code using /dev/urandom
# Use dd to read a fixed block (avoids SIGPIPE with infinite /dev/urandom stream)
RAW_BYTES=$(dd if=/dev/urandom bs=64 count=1 2>/dev/null | base64 | tr -dc 'a-z0-9')
CODE=$(printf '%s' "$RAW_BYTES" | head -c "$LENGTH")

if [ ${#CODE} -lt "$LENGTH" ]; then
  echo "Error: Failed to generate random code of sufficient length." >&2
  exit 1
fi

FULL_CODE="${PREFIX}-${CODE}"

# Write to secure state file (not stdout!)
printf '%s' "$FULL_CODE" > "$STATE_FILE"
chmod 600 "$STATE_FILE"

echo "OTC code generated and stored securely." >&2
