#!/usr/bin/env bash
# Generate transaction to revoke pet operator approval (approved=false)

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

DATA="$(set_pet_operator_calldata false)"

cat <<OUT
🔓 Revoke Pet Operator Delegation
=================================

Wallet: $WALLET
Revoking operator: $AAI_OPERATOR (AAI)

Transaction Details:
====================
To: $AAVEGOTCHI_DIAMOND
Amount: 0 ETH
Network: Base (8453)
RPC: $BASE_RPC_URL

Hex Data (approved=false):
$DATA

What this does: removes AAI's ability to pet your gotchis.
OUT
