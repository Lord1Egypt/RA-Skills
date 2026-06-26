#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCK_FILE="/tmp/pet-me-master-auto-pet.lock"
RUN_LOG="$HOME/.openclaw/logs/pet-me-master-auto-pet.log"

# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Another auto-pet run is already active" >> "$RUN_LOG"
  exit 0
fi

cd "$SKILL_DIR"
load_config

COOLDOWN=43260
MIN_RECHECK_WAIT=15
ERROR_RECHECK_WAIT=300
POST_PET_SETTLE_WAIT=120

WALLET="$(resolve_agent_wallet_address || true)"
if [ -z "$WALLET" ]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Auto-pet scheduler failed: could not resolve wallet" >> "$RUN_LOG"
  exit 1
fi

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Auto-pet scheduler started wallet=$WALLET mode=all-ready-gate recurring=true" >> "$RUN_LOG"

CYCLE=0
while :; do
  CYCLE=$((CYCLE + 1))
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Cycle $CYCLE started" >> "$RUN_LOG"

  TOTAL_GOTCHIS=0
  while :; do
    mapfile -t TARGET_IDS < <(discover_pettable_gotchi_ids "$WALLET")
    TOTAL_GOTCHIS="${#TARGET_IDS[@]}"

    NOW="$(date +%s)"
    READY_COUNT=0
    WAITING_COUNT=0
    ERROR_COUNT=0
    MAX_TARGET="$NOW"

    if [ "$TOTAL_GOTCHIS" -eq 0 ]; then
      WAIT="$ERROR_RECHECK_WAIT"
      NEXT_TARGET=$((NOW + WAIT))
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] No discovered gotchis for wallet=$WALLET; retrying at $(date -u -d @${NEXT_TARGET} +%Y-%m-%dT%H:%M:%SZ)" >> "$RUN_LOG"
      sleep "$WAIT"
      continue
    fi

    for GOTCHI_ID in "${TARGET_IDS[@]}"; do
      STATUS="$(bash scripts/check-cooldown.sh "$GOTCHI_ID" 2>/dev/null || true)"
      [ -n "$STATUS" ] || STATUS="error:0:0"

      STATE="${STATUS%%:*}"
      REST="${STATUS#*:}"
      LAST="${REST##*:}"

      if [[ "$LAST" =~ ^[0-9]+$ ]]; then
        TARGET_CANDIDATE=$((LAST + COOLDOWN))
      else
        TARGET_CANDIDATE=$((NOW + ERROR_RECHECK_WAIT))
      fi
      if [ "$TARGET_CANDIDATE" -gt "$MAX_TARGET" ]; then
        MAX_TARGET="$TARGET_CANDIDATE"
      fi

      case "$STATE" in
        ready) READY_COUNT=$((READY_COUNT + 1)) ;;
        waiting) WAITING_COUNT=$((WAITING_COUNT + 1)) ;;
        *) ERROR_COUNT=$((ERROR_COUNT + 1)) ;;
      esac
    done

    if [ "$READY_COUNT" -eq "$TOTAL_GOTCHIS" ]; then
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] All discovered gotchis ready total=$TOTAL_GOTCHIS; proceeding to pet-all.sh" >> "$RUN_LOG"
      break
    fi

    WAIT=$((MAX_TARGET - NOW))
    if [ "$WAIT" -lt "$MIN_RECHECK_WAIT" ]; then
      WAIT="$MIN_RECHECK_WAIT"
    fi
    NEXT_TARGET=$((NOW + WAIT))
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Waiting for full readiness total=$TOTAL_GOTCHIS ready=$READY_COUNT waiting=$WAITING_COUNT error=$ERROR_COUNT next_check_utc=$(date -u -d @${NEXT_TARGET} +%Y-%m-%dT%H:%M:%SZ)" >> "$RUN_LOG"
    sleep "$WAIT"
  done

  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Running pet-me-master batch pet (cycle $CYCLE)" >> "$RUN_LOG"

  if OUT="$(bash scripts/pet-all.sh 2>&1)"; then
    {
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] pet-all.sh completed"
      echo "$OUT"
    } >> "$RUN_LOG"

    TX="$(printf '%s\n' "$OUT" | sed -n 's/^tx=//p' | head -n1 || true)"
    if [ -n "$TX" ]; then
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] tx=https://basescan.org/tx/$TX" >> "$RUN_LOG"
    fi

    PETTED_LIST="$(printf '%s\n' "$OUT" | sed -n 's/^Submitting batch pet transaction for //p' | tail -n1 || true)"
    if ! [[ "$TOTAL_GOTCHIS" =~ ^[0-9]+$ ]]; then
      TOTAL_GOTCHIS=0
    fi

    CHAT_ID="$(resolve_reminder_chat_id || true)"
    MSG="fren, i petted your ${TOTAL_GOTCHIS} gotchi(s)! 👻"
    if [ -n "$PETTED_LIST" ]; then
      MSG="$MSG
gotchis: $PETTED_LIST"
    else
      MSG="$MSG
gotchis: none"
    fi
    if [ -n "$TX" ]; then
      MSG="$MSG
https://basescan.org/tx/$TX"
    fi

    if [ -n "$CHAT_ID" ]; then
      if send_telegram_message "$CHAT_ID" "$MSG"; then
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Telegram confirmation sent to chat $CHAT_ID" >> "$RUN_LOG"
      else
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Telegram confirmation failed (chat $CHAT_ID)" >> "$RUN_LOG"
      fi
    else
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Telegram chat id not configured; skipped confirmation message" >> "$RUN_LOG"
    fi
  else
    {
      echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] pet-all.sh failed (cycle $CYCLE)"
      echo "$OUT"
    } >> "$RUN_LOG"

    CHAT_ID="$(resolve_reminder_chat_id || true)"
    if [ -n "$CHAT_ID" ]; then
      send_telegram_message "$CHAT_ID" "fren, petting failed - please check logs" >/dev/null 2>&1 || true
    fi
  fi

  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Cycle $CYCLE complete; settle_wait_seconds=$POST_PET_SETTLE_WAIT" >> "$RUN_LOG"
  sleep "$POST_PET_SETTLE_WAIT"
done
