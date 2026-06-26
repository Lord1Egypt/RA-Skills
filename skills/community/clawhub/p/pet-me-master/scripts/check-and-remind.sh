#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

STATE_FILE="${PET_ME_REMINDER_STATE_FILE:-$SKILL_DIR/reminder-state.json}"
REMINDER_FILE="${PET_ME_REMINDER_QUEUE_FILE:-$HOME/.openclaw/workspace/.gotchi-reminder.txt}"
IMMEDIATE_FILE="${PET_ME_IMMEDIATE_REMINDER_FILE:-$HOME/.openclaw/workspace/.pet-reminder-immediate.txt}"

require_tx_tools
load_config

if ! is_daily_reminder_enabled; then
  echo "[$(date)] dailyReminder disabled; skipping reminder check"
  exit 0
fi

WALLET="$(resolve_agent_wallet_address || true)"
[ -n "$WALLET" ] || err "Could not resolve agent wallet address"

mapfile -t GOTCHI_IDS < <(discover_pettable_gotchi_ids "$WALLET")
if [ "${#GOTCHI_IDS[@]}" -eq 0 ]; then
  echo "[$(date)] no owned/delegated gotchis discovered for wallet $WALLET"
  exit 0
fi

ALL_READY=true
READY_COUNT=0
NOW="$(date +%s)"

for GOTCHI_ID in "${GOTCHI_IDS[@]}"; do
  STATUS="$("$SCRIPT_DIR/check-cooldown.sh" "$GOTCHI_ID" 2>/dev/null || true)"
  [ -n "$STATUS" ] || STATUS="error:0:0"

  STATE="${STATUS%%:*}"
  if [ "$STATE" = "ready" ]; then
    READY_COUNT=$((READY_COUNT + 1))
  else
    ALL_READY=false
  fi
done

mkdir -p "$(dirname "$STATE_FILE")" "$(dirname "$REMINDER_FILE")" "$(dirname "$IMMEDIATE_FILE")"

if [ -f "$STATE_FILE" ]; then
  LAST_REMINDER="$(jq -r '.lastReminder // 0' "$STATE_FILE" 2>/dev/null || echo 0)"
  FALLBACK_SCHEDULED="$(jq -r '.fallbackScheduled // false' "$STATE_FILE" 2>/dev/null || echo false)"
else
  LAST_REMINDER=0
  FALLBACK_SCHEDULED=false
  printf '{"lastReminder":0,"fallbackScheduled":false}\n' > "$STATE_FILE"
fi

TIME_SINCE_REMINDER=$((NOW - LAST_REMINDER))
FALLBACK_HOURS="$(resolve_fallback_delay_hours)"
FALLBACK_SECONDS=$((FALLBACK_HOURS * 3600))

if [ "$ALL_READY" = true ] && [ "$READY_COUNT" -gt 0 ] && [ "$TIME_SINCE_REMINDER" -gt 43200 ] && [ "$FALLBACK_SCHEDULED" = false ]; then
  GOTCHI_LIST="$(join_gotchi_ids "${GOTCHI_IDS[@]}")"
  NEXT_AUTO_PET="$(date -u -d "+${FALLBACK_HOURS} hour" '+%H:%M UTC' 2>/dev/null || date -u '+%H:%M UTC')"
  NOTIFY_MSG="fren, pet your gotchi(s)! 👻

All ${#GOTCHI_IDS[@]} gotchis are ready for petting.
Wallet: ${WALLET}
Gotchis: ${GOTCHI_LIST}

Reply with 'pet my gotchis' and I'll batch-pet all. If you don't reply, I'll auto-pet in ${FALLBACK_HOURS} hour(s). 🦞
⏰ Next auto-pet: ${NEXT_AUTO_PET}"

  CHAT_ID="$(resolve_reminder_chat_id || true)"
  if [ -n "$CHAT_ID" ] && send_telegram_message "$CHAT_ID" "$NOTIFY_MSG"; then
    echo "[$(date)] ✅ sent Telegram reminder to chat ${CHAT_ID}"
  else
    printf '%s\n' "$NOTIFY_MSG" > "$IMMEDIATE_FILE"
    printf '%s\n' "$NOTIFY_MSG" > "$REMINDER_FILE"
    if [ -z "$CHAT_ID" ]; then
      echo "[$(date)] ⚠️ no reminder chat ID configured; queued reminder file fallback"
    else
      echo "[$(date)] ⚠️ Telegram send failed; queued reminder file fallback"
    fi
  fi

  jq --argjson now "$NOW" '.lastReminder = $now | .fallbackScheduled = true' "$STATE_FILE" > "${STATE_FILE}.tmp"
  mv "${STATE_FILE}.tmp" "$STATE_FILE"

  if command -v at >/dev/null 2>&1; then
    echo "bash $SCRIPT_DIR/auto-pet-fallback.sh" | at now + "$FALLBACK_HOURS hour" >/dev/null 2>&1 || true
  else
    (sleep "$FALLBACK_SECONDS" && bash "$SCRIPT_DIR/auto-pet-fallback.sh" >> /tmp/auto-pet-fallback.log 2>&1) &
    echo "[$(date)] fallback scheduled via background process (pid $!)"
  fi

  echo "[$(date)] ✅ fallback scheduled for ${FALLBACK_HOURS} hour(s)"
elif [ "$ALL_READY" = false ] && [ "$FALLBACK_SCHEDULED" = true ]; then
  printf '{"lastReminder":0,"fallbackScheduled":false}\n' > "$STATE_FILE"
  rm -f "$REMINDER_FILE" "$IMMEDIATE_FILE"
  echo "[$(date)] gotchis already petted; reminder state reset"
fi

exit 0
