#!/usr/bin/env bash
# system-log.sh — 統一系統運作 log（idle-ping 機制 + 出貨口）
# 用法：system-log.sh "<事件描述>"
# Log 檔預設：<workspace>/curiosity/system-activity.log（可用 IDLE_PING_LOG 覆寫）
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/idle-ping.env" ]; then
  # shellcheck disable=SC1091  # optional config file; may not exist on first run
  . "$SCRIPT_DIR/idle-ping.env"
fi
WS="${IDLE_PING_WS:-$(cd "$SCRIPT_DIR/.." && pwd)}"
LOG="${IDLE_PING_LOG:-$WS/curiosity/system-activity.log}"
echo "$(date '+%Y-%m-%d %H:%M:%S') | $*" >> "$LOG"
