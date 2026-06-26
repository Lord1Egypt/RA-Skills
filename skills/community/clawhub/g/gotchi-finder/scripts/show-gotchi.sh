#!/usr/bin/env bash
# show-gotchi.sh - Display gotchi with image + stats in Telegram format

set -euo pipefail

usage() {
  echo "Usage: bash show-gotchi.sh <gotchi-id>"
  exit 1
}

require_bin() {
  local bin="$1"
  command -v "$bin" >/dev/null 2>&1 || { echo "❌ Missing required binary: $bin"; exit 1; }
}

GOTCHI_ID="${1:-}"
[[ -n "$GOTCHI_ID" ]] || usage
[[ "$GOTCHI_ID" =~ ^[0-9]+$ ]] || { echo "❌ Invalid gotchi ID: $GOTCHI_ID"; exit 1; }

require_bin jq

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

cd "$SKILL_DIR"
bash scripts/find-gotchi.sh "$GOTCHI_ID"

JSON_FILE="./gotchi-$GOTCHI_ID.json"
PNG_FILE="./gotchi-$GOTCHI_ID.png"

[[ -f "$JSON_FILE" && -f "$PNG_FILE" ]] || { echo "❌ Failed to generate gotchi files"; exit 1; }

NAME="$(jq -r '.name // "Unnamed"' "$JSON_FILE")"
BRS="$(jq -r '.brs // "0"' "$JSON_FILE")"
KINSHIP="$(jq -r '.kinship // "0"' "$JSON_FILE")"
LEVEL="$(jq -r '.level // "0"' "$JSON_FILE")"
XP="$(jq -r '.experience // "0"' "$JSON_FILE")"
HAUNT="$(jq -r '.hauntId // "0"' "$JSON_FILE")"
COLLATERAL="$(jq -r '.collateral // ""' "$JSON_FILE")"

NRG="$(jq -r '.modifiedTraits.energy // "0"' "$JSON_FILE")"
AGG="$(jq -r '.modifiedTraits.aggression // "0"' "$JSON_FILE")"
SPK="$(jq -r '.modifiedTraits.spookiness // "0"' "$JSON_FILE")"
BRN="$(jq -r '.modifiedTraits.brainSize // "0"' "$JSON_FILE")"

TIER="COMMON"
if [[ "$BRS" -ge 580 ]]; then
  TIER="GODLIKE"
elif [[ "$BRS" -ge 525 ]]; then
  TIER="MYTHICAL"
elif [[ "$BRS" -ge 475 ]]; then
  TIER="UNCOMMON"
fi

EQUIPPED_COUNT="$(jq -r '.equippedWearables | length' "$JSON_FILE" 2>/dev/null || echo "0")"
if [[ "$EQUIPPED_COUNT" == "0" ]]; then
  WEARABLES="None equipped"
else
  WEARABLES="$EQUIPPED_COUNT equipped"
fi

case "${COLLATERAL,,}" in
  "0x20d3922b4a1a8560e1ac99fba4fade0c849e2142") COLLATERAL="WETH" ;;
  "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913") COLLATERAL="USDC" ;;
  "0x4200000000000000000000000000000000000006") COLLATERAL="WETH" ;;
esac

echo "PNG_PATH=$PNG_FILE"
echo "CAPTION<<EOF
👻 **Gotchi #$GOTCHI_ID - $NAME**

**📊 Stats:**
⭐ BRS: **$BRS** ($TIER tier)
💜 Kinship: **$KINSHIP**
🎮 Level: **$LEVEL** (XP: $XP)
👻 Haunt: **$HAUNT**
💎 Collateral: **$COLLATERAL**

**🎭 Traits:**
⚡ Energy: **$NRG**
👊 Aggression: **$AGG**
👻 Spookiness: **$SPK**
🧠 Brain Size: **$BRN**

**👔 Wearables:** $WEARABLES

LFGOTCHi! 🦞🚀
EOF"
