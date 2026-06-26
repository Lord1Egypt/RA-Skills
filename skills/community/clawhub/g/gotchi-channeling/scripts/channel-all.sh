#!/usr/bin/env bash
# Channel all configured gotchis

set -euo pipefail

usage() {
  cat <<USAGE
Usage: ./scripts/channel-all.sh

Reads config.json channeling entries and channels all ready gotchis.
USAGE
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -gt 0 ]; then
  usage
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

require_bin jq
load_config

if ! jq -e '.channeling | type == "array" and length > 0' "$CONFIG_FILE" >/dev/null 2>&1; then
  err "No channeling entries in $CONFIG_FILE"
fi

ENTRIES="$(jq -r '.channeling[] | "\(.gotchiId // "")\t\(.parcelId // "")\t\(.description // "")"' "$CONFIG_FILE")"

echo "🔮 Channeling All Gotchis"
echo "========================="
echo

echo "📊 Checking gotchis..."
echo

TOTAL=0
READY=0
WAITING=0
CHANNELED=0
FAILED=0

while IFS=$'\t' read -r GOTCHI_ID PARCEL_ID DESCRIPTION; do
  [ -n "$GOTCHI_ID" ] || continue

  TOTAL=$((TOTAL + 1))
  echo "👻 Gotchi #$GOTCHI_ID (Parcel #$PARCEL_ID)"
  if [ -n "$DESCRIPTION" ]; then
    echo "   📝 $DESCRIPTION"
  fi

  if [[ ! "$GOTCHI_ID" =~ ^[0-9]+$ ]] || [[ ! "$PARCEL_ID" =~ ^[0-9]+$ ]]; then
    echo "   ❌ Invalid gotchiId/parcelId in config"
    FAILED=$((FAILED + 1))
    echo
    continue
  fi

  if ! COOLDOWN_RESULT="$($SCRIPT_DIR/check-cooldown.sh "$GOTCHI_ID" 2>&1)"; then
    echo "   ❌ Cooldown check failed: $COOLDOWN_RESULT"
    FAILED=$((FAILED + 1))
    echo
    continue
  fi

  if [[ "$COOLDOWN_RESULT" =~ ^ready: ]]; then
    READY=$((READY + 1))
    echo "   ✅ Ready to channel"

    LOG_FILE="$(mktemp "/tmp/channel-${GOTCHI_ID}-XXXX.log")"
    if "$SCRIPT_DIR/channel.sh" "$GOTCHI_ID" "$PARCEL_ID" >"$LOG_FILE" 2>&1; then
      CHANNELED=$((CHANNELED + 1))
      echo "   ✅ Channeled successfully"

      REWARDS_LINE="$(grep -E "Total:" "$LOG_FILE" | tail -1 || true)"
      if [ -n "$REWARDS_LINE" ]; then
        echo "   💎 $REWARDS_LINE"
      fi
    else
      FAILED=$((FAILED + 1))
      echo "   ❌ Channeling failed (log: $LOG_FILE)"
    fi
  elif [[ "$COOLDOWN_RESULT" =~ ^waiting:([0-9]+)$ ]]; then
    WAITING=$((WAITING + 1))
    WAIT_TIME="${BASH_REMATCH[1]}"
    echo "   ⏰ Wait $(format_wait "$WAIT_TIME")"
  else
    FAILED=$((FAILED + 1))
    echo "   ❌ Unexpected cooldown output: $COOLDOWN_RESULT"
  fi

  echo
done <<< "$ENTRIES"

echo "============================================"
echo "📊 CHANNELING SUMMARY"
echo "============================================"
echo "Total gotchis: $TOTAL"
echo "Ready: $READY"
echo "Channeled: $CHANNELED"
echo "Failed: $FAILED"
echo "Still waiting: $WAITING"
echo

if [ "$FAILED" -gt 0 ]; then
  echo "⚠️  Completed with failures"
  exit 1
fi

if [ "$CHANNELED" -gt 0 ]; then
  echo "✅ Successfully channeled $CHANNELED gotchi(s)!"
elif [ "$READY" -eq 0 ]; then
  echo "⏰ No gotchis ready to channel yet"
else
  echo "⚠️  No channels were submitted"
fi

echo

echo "LFGOTCHi!"
