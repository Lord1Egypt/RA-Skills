#!/usr/bin/env bash
# Remove a delegated wallet record from pet-me-master config

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

usage() {
  echo "Usage: $0 <WALLET_ADDRESS>"
  exit 1
}

[[ $# -eq 1 ]] || usage
WALLET="$(normalize_wallet "$1")"
ADDR_LC="$(to_lower "$WALLET")"

CONFIG_FILE="$PET_ME_CONFIG_FILE"
[ -f "$CONFIG_FILE" ] || err "Pet-me-master config not found: $CONFIG_FILE"

BEFORE_DELEGATED="$(jq --arg addr_lc "$ADDR_LC" '[.delegatedWallets[]? | select(((.address // "") | ascii_downcase) == $addr_lc)] | length' "$CONFIG_FILE")"
BEFORE_WALLETS="$(jq --arg addr_lc "$ADDR_LC" '[.wallets[]? | select(((.address // "") | ascii_downcase) == $addr_lc)] | length' "$CONFIG_FILE")"

if [ "$BEFORE_DELEGATED" -eq 0 ] && [ "$BEFORE_WALLETS" -eq 0 ]; then
  echo "⚠️ Wallet not found in delegatedWallets/wallets: $WALLET"
  exit 1
fi

cp -f "$CONFIG_FILE" "${CONFIG_FILE}.bak.$(date +%Y%m%d-%H%M%S)"

jq --arg addr_lc "$ADDR_LC" '
  if has("delegatedWallets") then
    .delegatedWallets = ((.delegatedWallets // []) | map(select(((.address // "") | ascii_downcase) != $addr_lc)))
  else . end
  | if has("wallets") then
      .wallets = ((.wallets // []) | map(select(((.address // "") | ascii_downcase) != $addr_lc)))
    else . end
' "$CONFIG_FILE" > "${CONFIG_FILE}.tmp"

mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"

echo "✅ Wallet removed: $WALLET"
if jq -e '.delegatedWallets' "$CONFIG_FILE" >/dev/null 2>&1; then
  echo "delegatedWallets count: $(jq '.delegatedWallets | length' "$CONFIG_FILE")"
fi
if jq -e '.wallets' "$CONFIG_FILE" >/dev/null 2>&1; then
  echo "wallets count: $(jq '.wallets | length' "$CONFIG_FILE")"
fi
