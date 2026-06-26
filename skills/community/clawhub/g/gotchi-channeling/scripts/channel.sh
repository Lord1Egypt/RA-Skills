#!/usr/bin/env bash
# Channel Alchemica for a single Gotchi via Bankr

set -euo pipefail

usage() {
  cat <<USAGE
Usage: ./scripts/channel.sh <gotchi-id> <parcel-id>

Examples:
  ./scripts/channel.sh 9638 867
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -ne 2 ]; then
  usage
  exit 1
fi

GOTCHI_ID="$1"
PARCEL_ID="$2"
TRANSFER_TOPIC="0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

FUD_ADDR="0x2028b4043e6722ea164946c82fe806c4a43a0ff4"
FOMO_ADDR="0xa32137bfb57d2b6a9fd2956ba4b54741a6d54b58"
ALPHA_ADDR="0x15e7cac885e3730ce6389447bc0f7ac032f31947"
KEK_ADDR="0xe52b9170ff4ece4c35e796ffd74b57dec68ca0e5"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bin cast
require_bin curl
require_bin jq
load_config
require_numeric "$GOTCHI_ID" "gotchi-id"
require_numeric "$PARCEL_ID" "parcel-id"

API_KEY="$(resolve_bankr_api_key)"

echo "🔮 Gotchi Channeling"
echo "===================="
echo "👻 Gotchi: #$GOTCHI_ID"
echo "🏰 Parcel: #$PARCEL_ID"
echo

echo "⏰ Checking cooldown..."
if ! COOLDOWN_RESULT="$($SCRIPT_DIR/check-cooldown.sh "$GOTCHI_ID")"; then
  echo "❌ Cooldown check failed; aborting channel attempt"
  exit 1
fi

if [[ "$COOLDOWN_RESULT" =~ ^ready: ]]; then
  echo "✅ Cooldown ready!"
elif [[ "$COOLDOWN_RESULT" =~ ^waiting:([0-9]+)$ ]]; then
  WAIT_TIME="${BASH_REMATCH[1]}"
  echo "⏰ Not ready yet!"
  echo "   Wait: $(format_wait "$WAIT_TIME")"
  exit 1
else
  err "Unexpected cooldown response: $COOLDOWN_RESULT"
fi

echo
echo "📦 Building transaction..."
CALLDATA="$(cast calldata \
  "channelAlchemica(uint256,uint256,uint256,bytes)" \
  "$PARCEL_ID" \
  "$GOTCHI_ID" \
  0 \
  "0x")"

echo "   Function: channelAlchemica"
echo "   Parcel: $PARCEL_ID"
echo "   Gotchi: $GOTCHI_ID"
echo "   Calldata: ${CALLDATA:0:66}..."
echo

echo "🦞 Submitting to Bankr..."
REQUEST_PAYLOAD="$(jq -n \
  --arg to "$REALM_DIAMOND" \
  --argjson chainId "$CHAIN_ID" \
  --arg data "$CALLDATA" \
  --arg description "Channel Alchemica: Gotchi #$GOTCHI_ID on Parcel #$PARCEL_ID" \
  '{
    transaction: {
      to: $to,
      chainId: $chainId,
      value: "0",
      data: $data
    },
    description: $description,
    waitForConfirmation: true
  }')"

RESPONSE="$(curl -sS -X POST "https://api.bankr.bot/agent/submit" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$REQUEST_PAYLOAD")"

SUCCESS="$(echo "$RESPONSE" | jq -r '.success // false')"

if [ "$SUCCESS" != "true" ]; then
  ERROR_MSG="$(echo "$RESPONSE" | jq -r '.error // .message // "Unknown error"')"
  echo
  echo "============================================"
  echo "❌ CHANNELING FAILED"
  echo "============================================"
  echo "Error: $ERROR_MSG"
  echo
  echo "$RESPONSE" | jq '.'
  exit 1
fi

TX_HASH="$(echo "$RESPONSE" | jq -r '.transactionHash // empty')"
BLOCK="$(echo "$RESPONSE" | jq -r '.blockNumber // "pending"')"

echo

echo "============================================"
echo "✅ CHANNELING SUCCESSFUL!"
echo "============================================"
echo

echo "👻 Gotchi #$GOTCHI_ID channeled on Parcel #$PARCEL_ID"
echo "📦 Block: $BLOCK"
if [ -n "$TX_HASH" ]; then
  echo "🔗 Transaction: $TX_HASH"
  echo "🌐 View: https://basescan.org/tx/$TX_HASH"
fi

echo

echo "💰 Fetching rewards..."

# Reward parsing is best-effort and should never flip a successful tx to failure.
if [ -n "$TX_HASH" ] && RECEIPT="$(cast receipt "$TX_HASH" --rpc-url "$RPC_URL" --json 2>/dev/null)"; then
  extract_amount_hex() {
    local token_addr="$1"
    echo "$RECEIPT" | jq -r --arg topic "$TRANSFER_TOPIC" --arg token "$token_addr" '
      .logs[]? |
      select((.topics[0] // "" | ascii_downcase) == ($topic | ascii_downcase)) |
      select((.address // "" | ascii_downcase) == ($token | ascii_downcase)) |
      .data
    ' | head -1
  }

  to_token_dec() {
    local hex="$1"
    local dec
    if [ -z "$hex" ] || [ "$hex" = "null" ]; then
      printf '0.00'
      return
    fi
    dec="$(cast --to-dec "$hex" 2>/dev/null || echo 0)"
    awk -v n="$dec" 'BEGIN { printf "%.2f", n/1e18 }'
  }

  FUD_HEX="$(extract_amount_hex "$FUD_ADDR")"
  FOMO_HEX="$(extract_amount_hex "$FOMO_ADDR")"
  ALPHA_HEX="$(extract_amount_hex "$ALPHA_ADDR")"
  KEK_HEX="$(extract_amount_hex "$KEK_ADDR")"

  FUD_DEC="$(to_token_dec "$FUD_HEX")"
  FOMO_DEC="$(to_token_dec "$FOMO_HEX")"
  ALPHA_DEC="$(to_token_dec "$ALPHA_HEX")"
  KEK_DEC="$(to_token_dec "$KEK_HEX")"

  TOTAL_DEC="$(awk -v a="$FUD_DEC" -v b="$FOMO_DEC" -v c="$ALPHA_DEC" -v d="$KEK_DEC" 'BEGIN { printf "%.2f", a+b+c+d }')"

  if [ "$TOTAL_DEC" != "0.00" ]; then
    echo "💎 Alchemica Earned:"
    echo "   🔥 FUD:   $FUD_DEC"
    echo "   😱 FOMO:  $FOMO_DEC"
    echo "   🧠 ALPHA: $ALPHA_DEC"
    echo "   💚 KEK:   $KEK_DEC"
    echo "   💰 Total: $TOTAL_DEC Alchemica"
  else
    echo "💎 Alchemica minted! (reward amounts unavailable from receipt parsing)"
  fi
else
  echo "💎 Alchemica minted! (receipt unavailable for reward parsing)"
fi

echo

echo "⏰ Next channel: $(date -u -d '+24 hours' '+%Y-%m-%d %H:%M UTC' 2>/dev/null || echo '24 hours from now')"
echo

echo "LFGOTCHi!"
