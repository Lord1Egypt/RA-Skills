#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bins

if [ $# -lt 4 ]; then
  echo "Usage: $(basename "$0") <gotchi-id> <token-alias-or-address> <to-address> <amount> [--raw]"
  exit 1
fi

GOTCHI_ID="$1"
TOKEN_INPUT="$2"
TO_ADDRESS="$3"
AMOUNT_INPUT="$4"
RAW_FLAG="${5:-}"

is_valid_address "$TO_ADDRESS" || err "Invalid destination address: $TO_ADDRESS"

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

BEFORE_POCKET_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$POCKET")"
BEFORE_TO_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$TO_ADDRESS")"

if is_less_than_bigint "$BEFORE_POCKET_RAW" "$AMOUNT_RAW"; then
  err "Insufficient pocket balance. Have $BEFORE_POCKET_RAW, need $AMOUNT_RAW"
fi

CALLDATA="$("$CAST_BIN" calldata "transferEscrow(uint256,address,address,uint256)" "$GOTCHI_ID" "$TOKEN_ADDRESS" "$TO_ADDRESS" "$AMOUNT_RAW")"
RESPONSE="$(submit_bankr_tx "$AAVEGOTCHI_DIAMOND" "$CALLDATA" "Withdraw $AMOUNT_UNITS $SYMBOL from gotchi #$GOTCHI_ID pocket to $TO_ADDRESS")"
SUCCESS="$(printf "%s" "$RESPONSE" | jq -r '.success // false')"
TX_HASH="$(printf "%s" "$RESPONSE" | jq -r '.transactionHash // empty')"

[ "$SUCCESS" = "true" ] || {
  printf "%s\n" "$RESPONSE" | jq . >&2
  err "Bankr transaction failed"
}

AFTER_POCKET_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$POCKET")"
AFTER_TO_RAW="$(balance_of_raw "$TOKEN_ADDRESS" "$TO_ADDRESS")"
AFTER_POCKET_UNITS="$(raw_to_units "$AFTER_POCKET_RAW" "$DECIMALS")"
AFTER_TO_UNITS="$(raw_to_units "$AFTER_TO_RAW" "$DECIMALS")"

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
echo "to=$TO_ADDRESS"
echo "before_pocket_raw=$BEFORE_POCKET_RAW"
echo "before_to_raw=$BEFORE_TO_RAW"
echo "after_pocket_raw=$AFTER_POCKET_RAW"
echo "after_pocket_units=$AFTER_POCKET_UNITS"
echo "after_to_raw=$AFTER_TO_RAW"
echo "after_to_units=$AFTER_TO_UNITS"
