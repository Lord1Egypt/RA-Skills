#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bins

if [ $# -lt 2 ]; then
  echo "Usage: $(basename "$0") <gotchi-id> <token-alias-or-address>"
  exit 1
fi

GOTCHI_ID="$1"
TOKEN_INPUT="$2"
TOKEN_ADDRESS="$(resolve_token_address "$TOKEN_INPUT")"
OWNER="$(get_gotchi_owner "$GOTCHI_ID")"
POCKET="$(get_gotchi_pocket "$GOTCHI_ID")"
SYMBOL="$(get_token_symbol "$TOKEN_ADDRESS")"
DECIMALS="$(get_token_decimals "$TOKEN_ADDRESS")"
OWNER_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$OWNER")"
POCKET_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$POCKET")"
OWNER_UNITS="$(raw_to_units "$OWNER_RAW" "$DECIMALS")"
POCKET_UNITS="$(raw_to_units "$POCKET_RAW" "$DECIMALS")"

echo "gotchi_id=$GOTCHI_ID"
echo "token=$TOKEN_ADDRESS"
echo "symbol=$SYMBOL"
echo "decimals=$DECIMALS"
echo "owner=$OWNER"
echo "pocket=$POCKET"
echo "owner_balance_raw=$OWNER_RAW"
echo "owner_balance_units=$OWNER_UNITS"
echo "pocket_balance_raw=$POCKET_RAW"
echo "pocket_balance_units=$POCKET_UNITS"
