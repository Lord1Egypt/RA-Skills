#!/usr/bin/env bash
set -euo pipefail

# gotchi-equip: Equip wearables on an Aavegotchi
# Usage: equip.sh <gotchi-id> <slot1=wearableId1> [slot2=wearableId2] ...
# Example: equip.sh 9638 right-hand=64 left-hand=65 head=90

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

usage() {
  cat <<USAGE
Usage: ./scripts/equip.sh <gotchi-id> <slot=wearableId> [slot2=wearableId2] ...

Valid slots: body, face, eyes, head, left-hand, right-hand, pet, background

Examples:
  ./scripts/equip.sh 9638 right-hand=64
  ./scripts/equip.sh 9638 head=90 pet=151 right-hand=64
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -lt 2 ]; then
  usage
  exit 1
fi

require_bin node
require_bin jq
require_bin curl

GOTCHI_ID="$1"
shift
validate_gotchi_id "$GOTCHI_ID"

# Build wearables JSON object safely
WEARABLES_JSON='{}'
for arg in "$@"; do
  if [[ ! "$arg" =~ ^([a-z-]+)=([0-9]+)$ ]]; then
    echo "Invalid format: $arg"
    echo "Expected: slot=wearableId (e.g., right-hand=64)"
    exit 1
  fi

  SLOT="${BASH_REMATCH[1]}"
  WEARABLE_ID="${BASH_REMATCH[2]}"

  WEARABLES_JSON="$(echo "$WEARABLES_JSON" | jq -c --arg slot "$SLOT" --argjson id "$WEARABLE_ID" '. + {($slot): $id}')"
done

# Preserve existing loadout: fetch current 16-slot wearables first.
CURRENT_WEARABLES_JSON="$(fetch_current_wearables "$GOTCHI_ID")"

echo "Gotchi: #$GOTCHI_ID"
echo "Requested updates: $WEARABLES_JSON"
echo

TEMP_SCRIPT="$(mktemp /tmp/gotchi-equip-script-XXXXXX.js)"
TEMP_TX="$(mktemp /tmp/gotchi-equip-tx-XXXXXX.json)"
cleanup() {
  rm -f "$TEMP_SCRIPT" "$TEMP_TX"
}
trap cleanup EXIT

cat > "$TEMP_SCRIPT" <<'NODE_EOF'
const { buildEquipTransaction } = require(process.argv[2]);
const fs = require('fs');

const gotchiId = process.argv[3];
const wearables = JSON.parse(process.argv[4]);
const currentWearables = JSON.parse(process.argv[5]);
const outFile = process.argv[6];

try {
  const txData = buildEquipTransaction(gotchiId, wearables, currentWearables);

  console.log('Transaction prepared:');
  console.log('  To:', txData.transaction.to);
  console.log('  Chain:', txData.transaction.chainId);
  console.log('  Description:', txData.description);
  console.log('');

  fs.writeFileSync(outFile, JSON.stringify(txData, null, 2));
  console.log('Saved transaction payload to temp file');
} catch (error) {
  console.error('Error:', error.message);
  process.exit(1);
}
NODE_EOF

cd "$SKILL_DIR"
node "$TEMP_SCRIPT" "$SKILL_DIR/lib/equip-lib.js" "$GOTCHI_ID" "$WEARABLES_JSON" "$CURRENT_WEARABLES_JSON" "$TEMP_TX"

echo "Submitting transaction via Bankr..."
API_KEY="$(resolve_bankr_api_key)"

RESPONSE="$(curl -sS -X POST "https://api.bankr.bot/agent/submit" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d @"$TEMP_TX")"

if ! echo "$RESPONSE" | jq -e . >/dev/null 2>&1; then
  echo "Non-JSON response from Bankr:"
  echo "$RESPONSE"
  exit 1
fi

echo "$RESPONSE" | jq '.'

SUCCESS="$(echo "$RESPONSE" | jq -r '.success // false')"
if [ "$SUCCESS" = "true" ]; then
  TX_HASH="$(echo "$RESPONSE" | jq -r '.transactionHash // empty')"
  echo
  echo "SUCCESS: wearables equipped"
  if [ -n "$TX_HASH" ]; then
    echo "Transaction: $TX_HASH"
    echo "BaseScan: https://basescan.org/tx/$TX_HASH"
  fi
else
  ERR_MSG="$(echo "$RESPONSE" | jq -r '.error // .message // "Transaction failed"')"
  echo
  echo "Transaction failed: $ERR_MSG"
  exit 1
fi
