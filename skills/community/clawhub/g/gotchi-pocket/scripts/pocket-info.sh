#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bins

if [ $# -lt 1 ]; then
  echo "Usage: $(basename "$0") <gotchi-id> [--check-bankr]"
  exit 1
fi

GOTCHI_ID="$1"
CHECK_BANKR="${2:-}"

OWNER="$(get_gotchi_owner "$GOTCHI_ID")"
POCKET="$(get_gotchi_pocket "$GOTCHI_ID")"

echo "gotchi_id=$GOTCHI_ID"
echo "owner=$OWNER"
echo "pocket=$POCKET"

if [ "$CHECK_BANKR" = "--check-bankr" ]; then
  BANKR_WALLET="$(get_bankr_wallet_address)"
  echo "bankr_wallet=$BANKR_WALLET"
  if [ "$(to_lower "$OWNER")" = "$(to_lower "$BANKR_WALLET")" ]; then
    echo "bankr_controls_gotchi=true"
  else
    echo "bankr_controls_gotchi=false"
  fi
fi
