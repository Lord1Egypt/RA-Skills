#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

STATE_FILE="${PET_ME_REMINDER_STATE_FILE:-$SKILL_DIR/reminder-state.json}"

echo "[$(date)] auto-pet fallback triggered"

require_tx_tools
load_config

WALLET="$(resolve_agent_wallet_address || true)"
[ -n "$WALLET" ] || err "Could not resolve agent wallet address"

mapfile -t TARGET_IDS < <(discover_pettable_gotchi_ids "$WALLET")
if [ "${#TARGET_IDS[@]}" -eq 0 ]; then
  echo "[$(date)] no owned/delegated gotchis discovered for wallet $WALLET"
  printf '{"lastReminder":0,"fallbackScheduled":false}\n' > "$STATE_FILE"
  exit 0
fi

READY_IDS=()
for GOTCHI_ID in "${TARGET_IDS[@]}"; do
  STATUS="$("$SCRIPT_DIR/check-cooldown.sh" "$GOTCHI_ID" 2>/dev/null || true)"
  [ -n "$STATUS" ] || STATUS="error:0:0"
  STATE="${STATUS%%:*}"
  if [ "$STATE" = "ready" ]; then
    READY_IDS+=("$GOTCHI_ID")
  fi
done

if [ "${#READY_IDS[@]}" -gt 0 ]; then
  READY_LIST="$(join_gotchi_ids "${READY_IDS[@]}")"
  echo "[$(date)] auto fallback: batch petting ready gotchis $READY_LIST"

  if PET_OUTPUT="$("$SCRIPT_DIR/pet-all.sh" 2>&1)"; then
    echo "$PET_OUTPUT"
    TX_HASH="$(printf '%s\n' "$PET_OUTPUT" | sed -n 's/^tx=//p' | head -n1)"

    MSG="🤖 Auto-pet fallback executed.
Wallet: ${WALLET}
Petted: ${READY_LIST}
Kinship +${#READY_IDS[@]}"
    if [ -n "$TX_HASH" ]; then
      MSG+="
Tx: https://basescan.org/tx/${TX_HASH}"
    fi

    CHAT_ID="$(resolve_reminder_chat_id || true)"
    if [ -n "$CHAT_ID" ] && send_telegram_message "$CHAT_ID" "$MSG"; then
      echo "[$(date)] fallback notification sent to Telegram"
    else
      echo "$MSG"
    fi
  else
    echo "[$(date)] ❌ auto batch pet failed"
    echo "$PET_OUTPUT" >&2
  fi
else
  echo "[$(date)] all discovered gotchis already petted; nothing to do"
fi

printf '{"lastReminder":0,"fallbackScheduled":false}\n' > "$STATE_FILE"
echo "[$(date)] reminder state reset"

# Schedule next check at cooldown boundary.
bash "$SCRIPT_DIR/schedule-dynamic-check.sh" &
echo "[$(date)] scheduling next check based on latest pet timestamp"

exit 0
