#!/usr/bin/env bash
set -euo pipefail

# gotchi-equip: Show currently equipped wearables on an Aavegotchi
# Usage: show-equipped.sh <gotchi-id>
# Example: show-equipped.sh 9638

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"

usage() {
  cat <<USAGE
Usage: ./scripts/show-equipped.sh <gotchi-id>

Example:
  ./scripts/show-equipped.sh 9638
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

require_bin jq
require_bin curl

GOTCHI_ID="$1"
validate_gotchi_id "$GOTCHI_ID"

echo "Fetching equipped wearables for gotchi #$GOTCHI_ID"
echo

GOTCHI_JSON="$(fetch_gotchi_subgraph_json "$GOTCHI_ID")"
NAME="$(echo "$GOTCHI_JSON" | jq -r '.name // "Unknown"')"
EQUIPPED="$(echo "$GOTCHI_JSON" | jq -c '(.equippedWearables // [])')"

echo "==================================================================="
echo "Gotchi: #$GOTCHI_ID \"$NAME\""
echo
echo "Equipped wearables:"
echo

SLOTS=("Body" "Face" "Eyes" "Head" "Left Hand" "Right Hand" "Pet" "Background")
HAS_ANY=0

for i in {0..7}; do
  WEARABLE_ID="$(echo "$EQUIPPED" | jq -r ".[$i] // 0")"
  if [ "$WEARABLE_ID" != "0" ] && [ "$WEARABLE_ID" != "null" ]; then
    HAS_ANY=1
    echo "  ${SLOTS[$i]}: Wearable ID $WEARABLE_ID"
  fi
done

if [ "$HAS_ANY" -eq 0 ]; then
  echo "  (none equipped)"
fi

echo
echo "==================================================================="
