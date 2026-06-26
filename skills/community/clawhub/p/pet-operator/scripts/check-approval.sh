#!/usr/bin/env bash
# Check if a wallet has approved AAI as pet operator

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

require_read_tools

if check_pet_operator_approved "$WALLET"; then
  echo "approved"
  exit 0
fi

echo "not_approved"
exit 1
