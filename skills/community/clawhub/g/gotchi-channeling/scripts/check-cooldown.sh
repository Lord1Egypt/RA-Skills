#!/usr/bin/env bash
# Check Gotchi channeling cooldown status
# Returns: ready:0 or waiting:SECONDS

set -euo pipefail

usage() {
  cat <<USAGE
Usage: ./scripts/check-cooldown.sh <gotchi-id>

Prints one machine-readable line:
  ready:0
  waiting:<seconds>
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -ne 1 ]; then
  usage
  exit 1
fi

GOTCHI_ID="$1"
COOLDOWN_SECONDS=86400

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bin cast
require_bin jq
load_config
require_numeric "$GOTCHI_ID" "gotchi-id"

if ! LAST_CHANNELED_HEX="$(cast call "$REALM_DIAMOND" \
  "s_gotchiChannelings(uint256)" \
  "$GOTCHI_ID" \
  --rpc-url "$RPC_URL" 2>/dev/null)"; then
  err "Failed to query cooldown from RPC"
fi

LAST_CHANNELED_DEC="$(cast --to-dec "$LAST_CHANNELED_HEX" 2>/dev/null || true)"
[[ "$LAST_CHANNELED_DEC" =~ ^[0-9]+$ ]] || err "Unexpected cooldown value from contract"

CURRENT_TIME="$(date +%s)"
TIME_SINCE=$((CURRENT_TIME - LAST_CHANNELED_DEC))
TIME_REMAINING=$((COOLDOWN_SECONDS - TIME_SINCE))

if [ "$TIME_REMAINING" -le 0 ]; then
  echo "ready:0"
else
  echo "waiting:$TIME_REMAINING"
fi
