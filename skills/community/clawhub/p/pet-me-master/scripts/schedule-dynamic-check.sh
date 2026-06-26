#!/usr/bin/env bash
# Dynamically schedule next cooldown check at 12h + 1m after last pet

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_read_tools
load_config

WALLET="$(resolve_agent_wallet_address || true)"
[ -n "$WALLET" ] || err "Could not resolve agent wallet address"

mapfile -t TARGET_IDS < <(discover_pettable_gotchi_ids "$WALLET")
[ "${#TARGET_IDS[@]}" -gt 0 ] || err "No gotchis discovered for wallet $WALLET"

LATEST_LAST_PET=0

for GOTCHI_ID in "${TARGET_IDS[@]}"; do
  STATUS="$($SCRIPT_DIR/check-cooldown.sh "$GOTCHI_ID" 2>/dev/null || true)"
  [ -n "$STATUS" ] || continue
  LAST_PET="${STATUS##*:}"
  if is_uint "$LAST_PET" && [ "$LAST_PET" -gt "$LATEST_LAST_PET" ]; then
    LATEST_LAST_PET="$LAST_PET"
  fi
done

if [ "$LATEST_LAST_PET" -le 0 ]; then
  echo "[$(date)] ❌ failed to determine latest last_pet timestamp"
  exit 1
fi

CHECK_AT=$((LATEST_LAST_PET + COOLDOWN_SECONDS))
NOW="$(date +%s)"
SECONDS_UNTIL=$((CHECK_AT - NOW))

if [ "$SECONDS_UNTIL" -lt 60 ]; then
  echo "[$(date)] check time already passed or too soon; running check now"
  bash "$SCRIPT_DIR/check-and-remind.sh"
  exit 0
fi

CHECK_TIME="$(date -d "@$CHECK_AT" +"%H:%M %Y-%m-%d")"

echo "bash $SCRIPT_DIR/check-and-remind.sh" | at "$CHECK_TIME" 2>/dev/null && {
  echo "[$(date)] ✅ scheduled check for $CHECK_TIME (12h + 1m after last pet)"
  exit 0
}

(sleep "$SECONDS_UNTIL" && bash "$SCRIPT_DIR/check-and-remind.sh" >> ~/.openclaw/logs/pet-me-master.log 2>&1) &
echo "[$(date)] ✅ scheduled check via background process (in ${SECONDS_UNTIL}s)"
