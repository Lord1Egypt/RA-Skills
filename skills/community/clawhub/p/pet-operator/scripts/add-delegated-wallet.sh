#!/usr/bin/env bash
# Add a delegated wallet record to pet-me-master config

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

usage() {
  echo "Usage: $0 <WALLET_ADDRESS> [NAME]"
  exit 1
}

[[ $# -ge 1 ]] || usage
WALLET="$(normalize_wallet "$1")"
NAME="${2:-Delegated Wallet}"

require_read_tools

echo "📋 Add Delegated Wallet"
echo "======================="
echo "Wallet: $WALLET"

echo "Checking pet operator approval..."
if ! check_pet_operator_approved "$WALLET"; then
  err "Wallet $WALLET has not approved AAI as pet operator. Run generate-delegation-tx.sh first."
fi
echo "✅ Wallet approved"

echo "Fetching owned gotchi IDs..."
mapfile -t GOTCHI_IDS < <(fetch_wallet_gotchi_ids "$WALLET")
COUNT="${#GOTCHI_IDS[@]}"

if [ "$COUNT" -eq 0 ]; then
  IDS_JSON='[]'
else
  IDS_JSON="$(printf '%s\n' "${GOTCHI_IDS[@]}" | jq -R . | jq -s '.')"
fi

echo "Found $COUNT gotchi(s)"
if [ "$COUNT" -gt 0 ]; then
  printf 'IDs: %s\n' "$(IFS=,; echo "${GOTCHI_IDS[*]}")"
fi

CONFIG_FILE="$PET_ME_CONFIG_FILE"
[ -f "$CONFIG_FILE" ] || err "Pet-me-master config not found: $CONFIG_FILE"

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ADDR_LC="$(to_lower "$WALLET")"

cp -f "$CONFIG_FILE" "${CONFIG_FILE}.bak.$(date +%Y%m%d-%H%M%S)"

jq \
  --arg name "$NAME" \
  --arg addr "$WALLET" \
  --arg addr_lc "$ADDR_LC" \
  --arg ts "$TS" \
  --argjson ids "$IDS_JSON" \
  '
  .delegatedWallets = ((.delegatedWallets // [])
    | map(select(((.address // "") | ascii_downcase) != $addr_lc))
    + [{name:$name,address:$addr,gotchiIds:$ids,approved:true,updatedAt:$ts}])
  | if has("wallets") then
      .wallets = ((.wallets // [])
        | map(select(((.address // "") | ascii_downcase) != $addr_lc))
        + [{name:$name,address:$addr,gotchiIds:$ids}])
    else
      .
    end
  ' "$CONFIG_FILE" > "${CONFIG_FILE}.tmp"

mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"

echo "✅ Delegated wallet saved"
echo "Config: $CONFIG_FILE"
echo "delegatedWallets count: $(jq '.delegatedWallets | length' "$CONFIG_FILE")"
