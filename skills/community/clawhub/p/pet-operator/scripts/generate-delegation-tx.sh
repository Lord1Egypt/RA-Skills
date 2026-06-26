#!/usr/bin/env bash
# Generate pet operator delegation transaction details (approved=true)

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

DATA="$(set_pet_operator_calldata true)"

cat <<OUT
🔑 Pet Operator Delegation
==========================

Wallet: $WALLET
Operator: $AAI_OPERATOR (AAI)

Transaction Details:
====================
To: $AAVEGOTCHI_DIAMOND
Amount: 0 ETH
Network: Base (8453)
RPC: $BASE_RPC_URL

Hex Data:
$DATA

What this does: approves AAI to pet your gotchis (you keep ownership).
OUT
