#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bins

if [ $# -lt 3 ]; then
  echo "Usage: $(basename "$0") <gotchi-id> <token-alias-or-address> <amount> [--raw]"
  exit 1
fi

GOTCHI_ID="$1"
TOKEN_INPUT="$2"
AMOUNT_INPUT="$3"
RAW_FLAG="${4:-}"
TOKEN_ADDRESS="$(resolve_token_address "$TOKEN_INPUT")"
SYMBOL="$(get_token_symbol "$TOKEN_ADDRESS")"
DECIMALS="$(get_token_decimals "$TOKEN_ADDRESS")"
OWNER="$(get_gotchi_owner "$GOTCHI_ID")"
POCKET="$(get_gotchi_pocket "$GOTCHI_ID")"

ensure_bankr_controls_gotchi "$GOTCHI_ID"

if [ "$RAW_FLAG" = "--raw" ]; then
  AMOUNT_RAW="$AMOUNT_INPUT"
  AMOUNT_UNITS="$(raw_to_units "$AMOUNT_RAW" "$DECIMALS")"
else
  AMOUNT_UNITS="$AMOUNT_INPUT"
  AMOUNT_RAW="$(amount_to_raw "$AMOUNT_UNITS" "$DECIMALS")"
fi

is_less_than_bigint "$AMOUNT_RAW" "1" && err "Amount must be greater than zero"

BEFORE_OWNER_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$OWNER")"
BEFORE_POCKET_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$POCKET")"

if is_less_than_bigint "$BEFORE_OWNER_RAW" "$AMOUNT_RAW"; then
  err "Insufficient owner balance. Have $BEFORE_OWNER_RAW, need $AMOUNT_RAW"
fi

CALLDATA="$("$CAST_BIN" calldata "transfer(address,uint256)" "$POCKET" "$AMOUNT_RAW")"
RESPONSE="$(submit_bankr_tx "$TOKEN_ADDRESS" "$CALLDATA" "Deposit $AMOUNT_UNITS $SYMBOL to gotchi #$GOTCHI_ID pocket")"
SUCCESS="$(printf "%s" "$RESPONSE" | jq -r '.success // false')"
TX_HASH="$(printf "%s" "$RESPONSE" | jq -r '.transactionHash // empty')"

[ "$SUCCESS" = "true" ] || {
  printf "%s\n" "$RESPONSE" | jq . >&2
  err "Bankr transaction failed"
}

AFTER_OWNER_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$OWNER")"
AFTER_POCKET_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$POCKET")"
AFTER_OWNER_UNITS="$(raw_to_units "$AFTER_OWNER_RAW" "$DECIMALS")"
AFTER_POCKET_UNITS="$(raw_to_units "$AFTER_POCKET_RAW" "$DECIMALS")"

echo "success=true"
echo "tx_hash=$TX_HASH"
echo "explorer=https://basescan.org/tx/$TX_HASH"
echo "gotchi_id=$GOTCHI_ID"
echo "token=$TOKEN_ADDRESS"
echo "symbol=$SYMBOL"
echo "amount_raw=$AMOUNT_RAW"
echo "amount_units=$AMOUNT_UNITS"
echo "owner=$OWNER"
echo "pocket=$POCKET"
echo "before_owner_raw=$BEFORE_OWNER_RAW"
echo "before_pocket_raw=$BEFORE_POCKET_RAW"
echo "after_owner_raw=$AFTER_OWNER_RAW"
echo "after_owner_units=$AFTER_OWNER_UNITS"
echo "after_pocket_raw=$AFTER_POCKET_RAW"
echo "after_pocket_units=$AFTER_POCKET_UNITS"
