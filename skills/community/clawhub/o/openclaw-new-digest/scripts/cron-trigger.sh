#!/usr/bin/env bash
#
# Cron trigger for News Digest skill.
# Loads .env, reads config.json for dynamic slot definitions, and spawns
# an OpenClaw session.
#
# Usage:
#   bash cron-trigger.sh [--slot <name>] [--dry-run]
#
# Slots are read from data/config.json. If --slot is omitted, the script
# auto-detects the active slot based on the current hour.
#
# Crontab example (times should match your config.json):
#   0 8 * * *  /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot morning
#   0 12 * * * /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot noon
#   0 18 * * * /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot evening

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DATA_DIR="${NEWS_DIGEST_DATA_DIR:-$SKILL_ROOT/data}"
CONFIG_FILE="$DATA_DIR/config.json"
LOG_DIR="$DATA_DIR/logs"

SLOT=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --slot)   SLOT="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help)
      echo "Usage: cron-trigger.sh [--slot <name>] [--dry-run]"
      echo "Slots are defined in $CONFIG_FILE"
      exit 0 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

# --- Load .env ---
ENV_CANDIDATES=(
  "$HOME/.openclaw/workspace/.env"
  "$SKILL_ROOT/.env"
  "$HOME/.env"
)

ENV_LOADED=""
for candidate in "${ENV_CANDIDATES[@]}"; do
  if [[ -f "$candidate" ]]; then
    set -a
    source "$candidate"
    set +a
    ENV_LOADED="$candidate"
    break
  fi
done

# --- Read config.json ---
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "[$(date -Iseconds)] ERROR: Config file not found: $CONFIG_FILE"
  echo "Run 'node $SCRIPT_DIR/manage-config.mjs init' to create default config."
  exit 1
fi

# Use node to extract slot info from config (avoids jq dependency)
read_slot_info() {
  node -e "
    const config = JSON.parse(require('fs').readFileSync('$CONFIG_FILE', 'utf-8'));
    const slot = config.slots.find(s => s.name === '$1');
    if (!slot) { process.exit(1); }
    console.log(JSON.stringify(slot));
  " 2>/dev/null
}

list_slots() {
  node -e "
    const config = JSON.parse(require('fs').readFileSync('$CONFIG_FILE', 'utf-8'));
    config.slots.forEach(s => console.log(s.name + '|' + (s.hour ?? 0) + '|' + (s.window ? s.window[0] : 0) + '|' + (s.window ? s.window[1] : 23) + '|' + (s.label ?? s.name) + '|' + (s.topic ?? '')));
  " 2>/dev/null
}

# --- Auto-detect slot from current hour if not specified ---
if [[ -z "$SLOT" ]]; then
  HOUR=$(date +%H)
  FOUND=""
  while IFS='|' read -r sname shour swin_start swin_end slabel stopic; do
    if (( HOUR >= swin_start && HOUR <= swin_end )); then
      FOUND="$sname"
      break
    fi
  done < <(list_slots)

  if [[ -z "$FOUND" ]]; then
    echo "[$(date -Iseconds)] No active slot for hour $HOUR. Exiting."
    exit 0
  fi
  SLOT="$FOUND"
fi

# --- Get slot details from config ---
SLOT_JSON=$(read_slot_info "$SLOT" 2>/dev/null) || {
  echo "Error: slot '$SLOT' not found in config."
  echo "Available slots:"
  list_slots | while IFS='|' read -r sname shour sws swe slabel stopic; do
    echo "  $sname ($slabel) at hour $shour"
  done
  exit 1
}

TOPIC_LABEL=$(node -e "console.log(JSON.parse(process.argv[1]).label ?? '')" "$SLOT_JSON" 2>/dev/null)
TOPIC=$(node -e "console.log(JSON.parse(process.argv[1]).topic ?? '')" "$SLOT_JSON" 2>/dev/null)

MESSAGE="Execute news digest push for slot \"$SLOT\" ($TOPIC_LABEL — $TOPIC). Read config first with: node $SCRIPT_DIR/manage-config.mjs show"

# --- Ensure log directory ---
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -Iseconds)
LOG_ENTRY="[$TIMESTAMP] slot=$SLOT env=$ENV_LOADED"

if $DRY_RUN; then
  echo "$LOG_ENTRY [DRY RUN]"
  echo "  Config: $CONFIG_FILE"
  echo "  Slot: $SLOT ($TOPIC_LABEL)"
  echo "  Topic: $TOPIC"
  echo "  Would run: openclaw run --message \"$MESSAGE\""
  echo "  TAVILY_API_KEY: ${TAVILY_API_KEY:+set}"
  echo "  XPOZ_API_KEY: ${XPOZ_API_KEY:+set}"
  exit 0
fi

echo "$LOG_ENTRY" >> "$LOG_DIR/cron.log"

# --- Trigger OpenClaw ---
if command -v openclaw &>/dev/null; then
  openclaw run --message "$MESSAGE" 2>&1 | tee -a "$LOG_DIR/cron.log" || {
    echo "[$TIMESTAMP] ERROR: openclaw run failed (exit $?)" >> "$LOG_DIR/cron.log"
    exit 1
  }
else
  echo "[$TIMESTAMP] ERROR: openclaw not found in PATH" >> "$LOG_DIR/cron.log"
  echo "Error: openclaw command not found. Ensure OpenClaw is installed and in PATH."
  exit 1
fi

echo "[$TIMESTAMP] Completed: $SLOT ($TOPIC_LABEL)" >> "$LOG_DIR/cron.log"
