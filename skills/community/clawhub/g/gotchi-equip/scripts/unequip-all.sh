#!/usr/bin/env bash
set -euo pipefail

# gotchi-equip: Unequip all wearables from an Aavegotchi
# Usage: unequip-all.sh <gotchi-id>
# Example: unequip-all.sh 9638

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

usage() {
  cat <<USAGE
Usage: ./scripts/unequip-all.sh <gotchi-id>

Example:
  ./scripts/unequip-all.sh 9638
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

require_bin node
require_bin jq
require_bin curl

GOTCHI_ID="$1"
validate_gotchi_id "$GOTCHI_ID"

echo "Gotchi: #$GOTCHI_ID"
echo "Action: Unequip all wearables"
echo

TEMP_SCRIPT="$(mktemp /tmp/gotchi-unequip-script-XXXXXX.js)"
TEMP_TX="$(mktemp /tmp/gotchi-unequip-tx-XXXXXX.json)"
cleanup() {
  rm -f "$TEMP_SCRIPT" "$TEMP_TX"
}
trap cleanup EXIT

cat > "$TEMP_SCRIPT" <<'NODE_EOF'
const { buildUnequipAllTransaction } = require(process.argv[2]);
const fs = require('fs');

const gotchiId = process.argv[3];
const outFile = process.argv[4];

try {
  const txData = buildUnequipAllTransaction(gotchiId);

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
node "$TEMP_SCRIPT" "$SKILL_DIR/lib/equip-lib.js" "$GOTCHI_ID" "$TEMP_TX"

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
  echo "SUCCESS: all wearables unequipped"
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
