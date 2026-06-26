#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--dry-run]

Discovers all pettable gotchis (owned + delegated to agent wallet), then submits
one interact([...]) transaction for only those currently ready.
USAGE
}

DRY_RUN=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

require_tx_tools
load_config

WALLET="$(resolve_agent_wallet_address || true)"
[ -n "$WALLET" ] || err "Could not resolve agent wallet address"

mapfile -t TARGET_IDS < <(discover_pettable_gotchi_ids "$WALLET")
if [ "${#TARGET_IDS[@]}" -eq 0 ]; then
  echo "No gotchis found for wallet $WALLET (owned or delegated)."
  exit 0
fi

echo "Wallet: $WALLET"
echo "Discovered gotchis: $(join_gotchi_ids "${TARGET_IDS[@]}")"
echo "Checking cooldowns..."

READY_IDS=()
WAITING_IDS=()
ERROR_IDS=()

for GOTCHI_ID in "${TARGET_IDS[@]}"; do
  STATUS="$($SCRIPT_DIR/check-cooldown.sh "$GOTCHI_ID" 2>/dev/null || true)"
  [ -n "$STATUS" ] || STATUS="error:0:0"

  STATE="${STATUS%%:*}"
  REST="${STATUS#*:}"
  TIME_LEFT="${REST%%:*}"

  case "$STATE" in
    ready)
      READY_IDS+=("$GOTCHI_ID")
      echo "  ready #$GOTCHI_ID"
      ;;
    waiting)
      WAITING_IDS+=("$GOTCHI_ID")
      echo "  wait  #$GOTCHI_ID ($(format_duration "$TIME_LEFT"))"
      ;;
    *)
      ERROR_IDS+=("$GOTCHI_ID")
      echo "  error #$GOTCHI_ID"
      ;;
  esac
done

echo
READY_COUNT="${#READY_IDS[@]}"
WAITING_COUNT="${#WAITING_IDS[@]}"
ERROR_COUNT="${#ERROR_IDS[@]}"

echo "Summary: total=${#TARGET_IDS[@]} ready=$READY_COUNT waiting=$WAITING_COUNT error=$ERROR_COUNT"

if [ "$READY_COUNT" -eq 0 ]; then
  echo "No discovered gotchis are ready right now."
  exit 0
fi

CALLDATA="$(encode_interact_calldata "${READY_IDS[@]}")"
READY_LIST="$(join_gotchi_ids "${READY_IDS[@]}")"
DESCRIPTION="Batch pet gotchis: ${READY_LIST}"

if [ "$DRY_RUN" -eq 1 ]; then
  jq -n \
    --arg wallet "$WALLET" \
    --arg to "$CONTRACT_ADDRESS" \
    --arg chainId "$CHAIN_ID" \
    --arg data "$CALLDATA" \
    --arg ready "$READY_LIST" \
    '{mode:"dry-run",action:"pet-batch",wallet:$wallet,ready:$ready,transaction:{to:$to,chainId:($chainId|tonumber),value:"0",data:$data}}'
  exit 0
fi

echo "Submitting batch pet transaction for $READY_LIST"
RESPONSE="$(submit_bankr_tx "$CONTRACT_ADDRESS" "$CALLDATA" "$DESCRIPTION")"

if bankr_is_success "$RESPONSE"; then
  TX_HASH="$(bankr_tx_hash "$RESPONSE")"
  echo "OK: batch pet submitted"
  if [ -n "$TX_HASH" ]; then
    echo "tx=$TX_HASH"
    echo "url=https://basescan.org/tx/$TX_HASH"
  fi
  exit 0
fi

echo "ERROR: $(bankr_error "$RESPONSE")" >&2
printf '%s\n' "$RESPONSE" | jq '.' >&2 || true
exit 1
