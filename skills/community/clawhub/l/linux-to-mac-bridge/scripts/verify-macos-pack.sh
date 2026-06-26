#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR=""
TOOLS=(imsg remindctl memo things peekaboo brew gh)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-dir) TARGET_DIR="${2:-}"; shift 2 ;;
    --tool) TOOLS+=("${2:-}"); shift 2 ;;
    -h|--help)
      echo "usage: verify-macos-pack.sh --target-dir DIR [--tool name]"
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

[[ -n "$TARGET_DIR" ]] || { echo "missing --target-dir" >&2; exit 1; }

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
