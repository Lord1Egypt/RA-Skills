#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR=""
TOOLS=()
OPENCLAW_CONFIG=""
DEFAULT_TOOLS=(imsg remindctl memo things peekaboo)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-dir) TARGET_DIR="${2:-}"; shift 2 ;;
    --tool) TOOLS+=("${2:-}"); shift 2 ;;
    --openclaw-config) OPENCLAW_CONFIG="${2:-}"; shift 2 ;;
    -h|--help)
      echo "usage: verify-macos-pack.sh --target-dir DIR [--tool name] [--openclaw-config FILE]"
      echo "If --openclaw-config is provided, only enabled macOS-backed channels are verified."
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

[[ -n "$TARGET_DIR" ]] || { echo "missing --target-dir" >&2; exit 1; }
if [[ -z "$OPENCLAW_CONFIG" && -f "${HOME}/.openclaw/openclaw.json" ]]; then
  OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
fi

if [[ "${#TOOLS[@]}" -eq 0 && -n "$OPENCLAW_CONFIG" && -f "$OPENCLAW_CONFIG" ]] && command -v python3 >/dev/null 2>&1; then
  while IFS= read -r tool; do
    [[ -n "$tool" ]] || continue
    TOOLS+=("$tool")
  done < <(python3 - "$OPENCLAW_CONFIG" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
cfg = json.loads(config_path.read_text())
channels = cfg.get("channels") or {}

channel_by_tool = {
    "imsg": "imessage",
    "remindctl": "reminders",
    "memo": "notes",
    "things": "things",
    "peekaboo": "peekaboo",
}

def channel_enabled(channel):
    if not isinstance(channel, dict):
        return False
    enabled = channel.get("enabled")
    if isinstance(enabled, bool):
        return enabled
    return bool(channel)

for tool, channel_name in channel_by_tool.items():
    if channel_enabled(channels.get(channel_name)):
        print(tool)
PY
)
fi

if [[ "${#TOOLS[@]}" -eq 0 && -n "$OPENCLAW_CONFIG" && -f "$OPENCLAW_CONFIG" ]]; then
  echo "No enabled macOS bridge tools discovered in $OPENCLAW_CONFIG"
  exit 0
fi

if [[ "${#TOOLS[@]}" -eq 0 ]]; then
  TOOLS=("${DEFAULT_TOOLS[@]}")
fi

printf "%-14s %-10s %-10s %s\n" "TOOL" "STATE" "WOL" "PATH"
for tool in "${TOOLS[@]}"; do
  wrapper="$TARGET_DIR/$tool"
  if [[ -x "$wrapper" ]]; then
    wake_mac="$(sed -n 's/^WAKE_MAC=//p' "$wrapper" | head -n 1)"
    if [[ -n "$wake_mac" && "$wake_mac" != "''" ]]; then
      wol_state="ENABLED"
    else
      wol_state="DISABLED"
    fi
    printf "%-14s %-10s %-10s %s\n" "$tool" "READY" "$wol_state" "$wrapper"
  else
    printf "%-14s %-10s %-10s %s\n" "$tool" "MISSING" "-" "$wrapper"
  fi
done
