#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_read_tools
load_config

WALLET="$(resolve_agent_wallet_address || true)"
[ -n "$WALLET" ] || err "Could not resolve agent wallet address"

mapfile -t TARGET_IDS < <(discover_pettable_gotchi_ids "$WALLET")
if [ "${#TARGET_IDS[@]}" -eq 0 ]; then
  echo "No gotchis discovered for wallet $WALLET"
  exit 0
fi

echo "Aavegotchi pet status"
echo "wallet: $WALLET"
echo "targets: $(join_gotchi_ids "${TARGET_IDS[@]}")"
echo

READY_COUNT=0
WAITING_COUNT=0
ERROR_COUNT=0
NOW="$(date +%s)"

for GOTCHI_ID in "${TARGET_IDS[@]}"; do
  STATUS="$($SCRIPT_DIR/check-cooldown.sh "$GOTCHI_ID" 2>/dev/null || true)"
  [ -n "$STATUS" ] || STATUS="error:0:0"

  STATE="${STATUS%%:*}"
  REST="${STATUS#*:}"
  TIME_LEFT="${REST%%:*}"
  LAST_PET="${REST##*:}"

  echo "#$GOTCHI_ID"

  case "$STATE" in
    ready)
      READY_COUNT=$((READY_COUNT + 1))
      TIME_AGO=$((NOW - LAST_PET))
      echo "  status: ready"
      echo "  last_pet: $(format_utc "$LAST_PET") ($(format_duration "$TIME_AGO") ago)"
      ;;
    waiting)
      WAITING_COUNT=$((WAITING_COUNT + 1))
      NEXT_PET=$((LAST_PET + COOLDOWN_SECONDS))
      TIME_AGO=$((NOW - LAST_PET))
      echo "  status: waiting"
      echo "  time_left: $(format_duration "$TIME_LEFT")"
      echo "  last_pet: $(format_utc "$LAST_PET") ($(format_duration "$TIME_AGO") ago)"
      echo "  next_pet: $(format_utc "$NEXT_PET")"
      ;;
    *)
      ERROR_COUNT=$((ERROR_COUNT + 1))
      echo "  status: error"
      ;;
  esac

  echo
done

echo "Summary: total=${#TARGET_IDS[@]} ready=$READY_COUNT waiting=$WAITING_COUNT error=$ERROR_COUNT"
