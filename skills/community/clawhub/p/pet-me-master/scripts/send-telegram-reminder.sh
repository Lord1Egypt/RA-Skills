#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_tx_tools
load_config

WALLET="$(resolve_agent_wallet_address || true)"
[ -n "$WALLET" ] || err "Could not resolve agent wallet address"

mapfile -t DISCOVERED_IDS < <(discover_pettable_gotchi_ids "$WALLET")
if [ "${#DISCOVERED_IDS[@]}" -eq 0 ]; then
  err "No gotchis discovered for wallet $WALLET"
fi

GOTCHI_COUNT="${1:-${#DISCOVERED_IDS[@]}}"
GOTCHI_LIST="${2:-$(join_gotchi_ids "${DISCOVERED_IDS[@]}")}"
FALLBACK_HOURS="$(resolve_fallback_delay_hours)"
NEXT_AUTO_PET="$(date -u -d "+${FALLBACK_HOURS} hour" '+%H:%M UTC' 2>/dev/null || date -u '+%H:%M UTC')"

CHAT_ID="$(resolve_reminder_chat_id || true)"
[ -n "$CHAT_ID" ] || err "Reminder chat ID missing (set PET_ME_TELEGRAM_CHAT_ID/TELEGRAM_CHAT_ID or config reminder.telegramChatId)"

MESSAGE="🐾 PET TIME! 👻

All ${GOTCHI_COUNT} discovered gotchis are ready for petting.

Wallet: ${WALLET}
Gotchis: ${GOTCHI_LIST}

Reply with 'pet my gotchis' and I'll batch-pet all. If no reply, auto-pet runs in ${FALLBACK_HOURS} hour(s). 🦞

⏰ Next auto-pet: ${NEXT_AUTO_PET}"

if send_telegram_message "$CHAT_ID" "$MESSAGE"; then
  echo "[$(date)] ✅ Telegram reminder sent to chat ${CHAT_ID}"
  exit 0
fi

echo "[$(date)] ❌ Failed to send Telegram reminder" >&2
exit 1
