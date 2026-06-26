#!/bin/bash
# ping-me-config: View and change ping-me settings.
# All python operations use stdin for data — no inline string embedding.
#
# Usage:
#   ping-me-config.sh                          # Show current settings
#   ping-me-config.sh --set key=value          # Change a setting
#   ping-me-config.sh --reset                  # Reset to defaults

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$(dirname "$SCRIPT_DIR")/config.json"

DEFAULT_CONFIG='{"tz":"","channel":"auto","to":"","emoji":"⏰","lang":"auto"}'

ensure_config() {
  if [ ! -f "$CONFIG_FILE" ]; then
    echo "$DEFAULT_CONFIG" | python3 -c '
import json, sys
data = json.load(sys.stdin)
json.dump(data, open(sys.argv[1], "w"), indent=2, ensure_ascii=False)
' "$CONFIG_FILE"
  fi
}

show_config() {
  ensure_config

  # Detect system timezone
  local sys_tz="${TZ:-}"
  if [ -z "$sys_tz" ] && command -v timedatectl &>/dev/null; then
    sys_tz=$(timedatectl show -p Timezone --value 2>/dev/null || echo "")
  fi
  if [ -z "$sys_tz" ] && [ -f /etc/timezone ]; then
    sys_tz=$(cat /etc/timezone)
  fi
  [ -z "$sys_tz" ] && sys_tz="UTC"

  python3 -c '
import json, sys
sys_tz = sys.argv[1]
cfg = json.load(sys.stdin)
tz = cfg.get("tz", "")
channel = cfg.get("channel", "auto")
to = cfg.get("to", "")
emoji = cfg.get("emoji", "⏰")
lang = cfg.get("lang", "auto")
print("⚙️  ping-me settings")
print()
print(f"  tz       = {tz if tz else f\"(auto: {sys_tz})\"}")
print(f"  channel  = {channel}")
print(f"  to       = {to if to else \"(not set — will auto-detect)\"}")
print(f"  emoji    = {emoji}")
print(f"  lang     = {lang}")
print()
print(f"System timezone: {sys_tz}")
print()
print("Change: ping-me-config.sh --set key=value")
print("Reset:  ping-me-config.sh --reset")
' "$sys_tz" < "$CONFIG_FILE"
}

set_value() {
  ensure_config
  local pair="$1"
  local key="${pair%%=*}"
  local val="${pair#*=}"

  # Validate key
  case "$key" in
    tz|channel|to|emoji|lang) ;;
    *)
      echo "❌ Invalid key: $key. Valid keys: tz, channel, to, emoji, lang"
      exit 1
      ;;
  esac

  # Validate style-specific values
  if [ "$key" = "lang" ]; then
    case "$val" in
      auto|zh|en|ja|fr|es|de|ko) ;;
      *)
        echo "❌ Invalid language: $val. Valid: auto, zh, en, ja, fr, es, de, ko"
        exit 1
        ;;
    esac
  fi

  if [ "$key" = "channel" ]; then
    case "$val" in
      auto|qqbot|telegram|discord|whatsapp|slack|feishu|dingtalk|wecom|imessage|last) ;;
      *)
        echo "⚠️  Warning: '$val' is not a recognized channel. Setting anyway."
        ;;
    esac
  fi

  # Validate timezone via python (safe — argv, not inline)
  if [ "$key" = "tz" ] && [ -n "$val" ]; then
    python3 -c '
import sys
try:
    import zoneinfo
    zoneinfo.ZoneInfo(sys.argv[1])
except Exception:
    print(f"⚠️  Warning: \"{sys.argv[1]}\" may not be a valid IANA timezone. Setting anyway.", file=sys.stderr)
' "$val" 2>&1 || true
  fi

  # Update config safely: read from file via stdin, write back
  python3 -c '
import json, sys
key = sys.argv[1]
val = sys.argv[2]
config_path = sys.argv[3]
cfg = json.load(sys.stdin)
cfg[key] = val
with open(config_path, "w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
print(f"✅ {key} = {val}")
' "$key" "$val" "$CONFIG_FILE" < "$CONFIG_FILE"
}

reset_config() {
  echo "$DEFAULT_CONFIG" | python3 -c '
import json, sys
data = json.load(sys.stdin)
with open(sys.argv[1], "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
' "$CONFIG_FILE"
  echo "✅ Settings reset to defaults."
}

# Parse args
case "${1:-}" in
  -h|--help)
    echo "Usage: ping-me-config.sh [--set key=value] [--reset]"
    echo "Keys: tz, channel, to, emoji, lang"
    exit 0
    ;;
  --set)
    if [ -z "${2:-}" ]; then
      echo "Usage: ping-me-config.sh --set key=value"
      exit 1
    fi
    set_value "$2"
    ;;
  --reset)
    reset_config
    ;;
  "")
    show_config
    ;;
  *)
    echo "Unknown option: $1. Use --help."
    exit 1
    ;;
esac
