#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_read_tools
load_config

GOTCHI_ID="${1:-$(default_gotchi_id)}"

if ! is_uint "$GOTCHI_ID"; then
  echo "error:0:0"
  echo "Error: Invalid gotchi ID: $GOTCHI_ID" >&2
  exit 1
fi

DATA="$($CAST_BIN call "$CONTRACT_ADDRESS" "getAavegotchi(uint256)" "$GOTCHI_ID" --rpc-url "$RPC_URL" 2>/dev/null || true)"
if [ -z "$DATA" ]; then
  echo "error:0:0"
  echo "Error: Failed to query gotchi #$GOTCHI_ID" >&2
  exit 1
fi

LAST_PET_HEX="${DATA:2498:64}"
if [ -z "$LAST_PET_HEX" ] || [ "$LAST_PET_HEX" = "0000000000000000000000000000000000000000000000000000000000000000" ]; then
  echo "error:0:0"
  echo "Error: Invalid lastInteracted value for gotchi #$GOTCHI_ID" >&2
  exit 1
fi

LAST_PET_DEC=$((16#$LAST_PET_HEX))
NOW="$(date +%s)"
TIME_SINCE=$((NOW - LAST_PET_DEC))
TIME_LEFT=$((COOLDOWN_SECONDS - TIME_SINCE))

if [ "$TIME_LEFT" -le 0 ]; then
  echo "ready:0:$LAST_PET_DEC"
else
  echo "waiting:$TIME_LEFT:$LAST_PET_DEC"
fi
