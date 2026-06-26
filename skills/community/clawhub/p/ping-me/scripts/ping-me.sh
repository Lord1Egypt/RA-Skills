#!/bin/bash
# ping-me: Create a one-shot reminder via openclaw cron.
# Auto-detects channel and delivery target from environment/config.
#
# Usage:
#   ping-me.sh [options] <time> <message>
#
# Time formats:
#   Relative:  30m, 2h, 1d
#   Absolute:  2026-03-11T15:00  (uses configured timezone)
#              2026-03-11T15:00+0800  (explicit timezone)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$(dirname "$SCRIPT_DIR")/config.json"

show_help() {
  cat << 'EOF'
ping-me — Set a one-shot reminder

Usage: ping-me.sh [options] <time> <message>

Arguments:
  time       When to remind. Relative (30m, 2h, 1d) or ISO 8601
  message    What to remind about

Options:
  --tz <tz>        Override timezone (IANA, e.g. Asia/Shanghai)
  --channel <ch>   Override delivery channel (default: auto-detect)
  --to <dest>      Delivery target (e.g. qqbot:c2c:<openid>, telegram:<chatid>)
  --emoji <e>      Custom emoji prefix (default: from config or ⏰)
  -h, --help       Show this help

Delivery target (--to):
  Some channels (e.g. QQ Bot) require a full delivery target for announce mode.
  The script tries to auto-detect from session context or config.
  If auto-detection fails, set it via config:
    ping-me-config.sh --set to=qqbot:c2c:<your-openid>

Examples:
  ping-me.sh 30m "Take a break"
  ping-me.sh 2h "Call mom"
  ping-me.sh "2026-03-11T15:00" "Submit homework"
  ping-me.sh --channel telegram 1d "Renew subscription"
EOF
  exit 0
}

# ── Load config value safely via stdin ──
load_config_value() {
  local key="$1" default="$2"
  if [ -f "$CONFIG_FILE" ]; then
    local val
    val=$(python3 -c '
import json, sys
key = sys.argv[1]
default = sys.argv[2]
try:
    cfg = json.load(sys.stdin)
    print(cfg.get(key, default))
except Exception:
    print(default)
' "$key" "$default" < "$CONFIG_FILE" 2>/dev/null) || val="$default"
    echo "$val"
  else
    echo "$default"
  fi
}

# ── Detect system timezone ──
detect_system_tz() {
  local tz="${TZ:-}"
  if [ -z "$tz" ] && command -v timedatectl &>/dev/null; then
    tz=$(timedatectl show -p Timezone --value 2>/dev/null || echo "")
  fi
  if [ -z "$tz" ] && [ -f /etc/timezone ]; then
    tz=$(cat /etc/timezone)
  fi
  echo "${tz:-UTC}"
}

# ── Resolve timezone ──
resolve_tz() {
  local flag_tz="$1"
  if [ -n "$flag_tz" ]; then echo "$flag_tz"; return; fi
  local cfg_tz
  cfg_tz=$(load_config_value "tz" "")
  if [ -n "$cfg_tz" ]; then echo "$cfg_tz"; return; fi
  detect_system_tz
}

# ── Resolve channel ──
resolve_channel() {
  local flag_channel="$1"
  if [ -n "$flag_channel" ]; then echo "$flag_channel"; return; fi

  # Try gateway-injected env var
  local env_channel="${OPENCLAW_CHANNEL:-}"
  if [ -n "$env_channel" ] && [ "$env_channel" != "unknown" ]; then
    echo "$env_channel"; return
  fi

  # Try config
  local cfg_channel
  cfg_channel=$(load_config_value "channel" "auto")
  if [ "$cfg_channel" != "auto" ] && [ -n "$cfg_channel" ]; then
    echo "$cfg_channel"; return
  fi

  # Try session channel env
  local session_channel="${OPENCLAW_SESSION_CHANNEL:-}"
  if [ -n "$session_channel" ]; then echo "$session_channel"; return; fi

  # Empty — let openclaw cron decide (or fail with a clear message)
  echo ""
}

# ── Resolve delivery target (--to) ──
# Channels like QQ Bot require a full target for announce delivery.
# Priority: flag → env → session key extraction → config → empty
resolve_to() {
  local flag_to="$1"
  if [ -n "$flag_to" ]; then echo "$flag_to"; return; fi

  # Gateway may set this for the current conversation
  local env_to="${OPENCLAW_TO:-}"
  if [ -n "$env_to" ]; then echo "$env_to"; return; fi

  # Try to extract from session key (format: agent:main:<channel>:direct:<id>)
  local session_key="${OPENCLAW_SESSION_KEY:-}"
  if [ -n "$session_key" ]; then
    local extracted
    extracted=$(echo "$session_key" | python3 -c '
import sys
key = sys.stdin.read().strip()
parts = key.split(":")
# agent:main:qqbot:direct:<openid> → qqbot:c2c:<openid>
# agent:main:feishu:direct:<userid> → feishu:<userid>
# agent:main:telegram:direct:<chatid> → telegram:<chatid>
if len(parts) >= 5 and parts[2] and parts[3] == "direct" and parts[4]:
    ch = parts[2]
    uid = parts[4]
    if ch == "qqbot":
        print(f"qqbot:c2c:{uid}")
    else:
        print(f"{ch}:{uid}")
else:
    print("")
' 2>/dev/null) || extracted=""
    if [ -n "$extracted" ]; then echo "$extracted"; return; fi
  fi

  # Read from config
  local cfg_to
  cfg_to=$(load_config_value "to" "")
  if [ -n "$cfg_to" ]; then echo "$cfg_to"; return; fi

  echo ""
}

# ── Defaults from config ──
CFG_EMOJI=$(load_config_value "emoji" "⏰")

# ── Parse options ──
TZ_OPT=""
CHANNEL_OPT=""
TO_OPT=""
EMOJI="$CFG_EMOJI"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) show_help ;;
    --tz) TZ_OPT="$2"; shift 2 ;;
    --channel) CHANNEL_OPT="$2"; shift 2 ;;
    --to) TO_OPT="$2"; shift 2 ;;
    --emoji) EMOJI="$2"; shift 2 ;;
    -*) echo "Unknown option: $1"; exit 1 ;;
    *) break ;;
  esac
done

AT="${1:-}"
shift 2>/dev/null || true
MSG="$*"

if [ -z "$AT" ] || [ -z "$MSG" ]; then
  echo "Error: both <time> and <message> are required."
  echo "Run with --help for usage."
  exit 1
fi

# ── Resolve timezone, channel, and delivery target ──
RESOLVED_TZ=$(resolve_tz "$TZ_OPT")
RESOLVED_CHANNEL=$(resolve_channel "$CHANNEL_OPT")
RESOLVED_TO=$(resolve_to "$TO_OPT")

# ── Append timezone to absolute times if not already present ──
if [[ "$AT" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2} ]] && [[ ! "$AT" =~ [+-][0-9]{4}$ ]] && [[ ! "$AT" =~ Z$ ]]; then
  TZ_OFFSET=$(python3 -c '
import sys, zoneinfo
from datetime import datetime
try:
    tz = zoneinfo.ZoneInfo(sys.argv[1])
    print(datetime.now(tz).strftime("%z"))
except Exception:
    print("+0000")
' "$RESOLVED_TZ" 2>/dev/null) || TZ_OFFSET="+0000"
  AT="${AT}${TZ_OFFSET}"
fi

# ── Find openclaw binary ──
OPENCLAW=$(which openclaw 2>/dev/null || echo "openclaw")

# ── Build cron add command ──
CMD=("$OPENCLAW" cron add \
  --name "ping-me" \
  --description "${MSG}" \
  --at "$AT" \
  --message "${EMOJI} ${MSG}" \
  --announce \
  --timeout-seconds 30 \
  --delete-after-run \
  --json)

if [ -n "$RESOLVED_CHANNEL" ]; then
  CMD+=(--channel "$RESOLVED_CHANNEL")
fi

# --to is critical: without it, channels like QQ Bot fail with
# "requires target" error because announce mode needs a specific recipient
if [ -n "$RESOLVED_TO" ]; then
  CMD+=(--to "$RESOLVED_TO")
fi

if [ -n "$RESOLVED_TZ" ]; then
  CMD+=(--tz "$RESOLVED_TZ")
fi

# ── Execute and parse result safely via stdin ──
RESULT=$("${CMD[@]}" 2>&1)

JOB_ID=$(echo "$RESULT" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get("id", ""))
except Exception:
    print("")
' 2>/dev/null) || JOB_ID=""

if [ -n "$JOB_ID" ]; then
  echo "✅ Reminder set (ID: ${JOB_ID})"
  echo "${EMOJI} Time: ${AT}"
  echo "📝 Message: ${MSG}"
  [ -n "$RESOLVED_CHANNEL" ] && echo "📢 Channel: ${RESOLVED_CHANNEL}"
  [ -n "$RESOLVED_TO" ] && echo "📬 Target: ${RESOLVED_TO}"
  echo "🌐 Timezone: ${RESOLVED_TZ}"
else
  echo "❌ Failed to create reminder"
  echo "$RESULT"
  if echo "$RESULT" | grep -qi "channel.*required\|multiple channels"; then
    echo ""
    echo "💡 Hint: Set a default channel:"
    echo "   bash $(dirname "$0")/ping-me-config.sh --set channel=qqbot"
  fi
  if echo "$RESULT" | grep -qi "requires target\|目标格式"; then
    echo ""
    echo "💡 Hint: This channel needs a delivery target. Set it:"
    echo "   bash $(dirname "$0")/ping-me-config.sh --set to=qqbot:c2c:<your-openid>"
  fi
  exit 1
fi
