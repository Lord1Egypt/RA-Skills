#!/usr/bin/env bash
# heartbeat.sh — production 監察心跳
# 用途：由 cron job 定期執行（install.sh 會建立 idle-ping-heartbeat job）；
#       每次執行更新心跳檔（+ 可選 ping 外部監察服務）。
# 原理：如果 gateway / cron 死咗，心跳檔會停止更新 → watchdog.sh 偵測到過期 → alert。
# 支援外部監察服務（Healthchecks.io / Cronitor / 任何 GET-ping URL）：
#   設定 IDLE_PING_HEARTBEAT_URL 之後，每次心跳會 ping 一次，服務端會記錄「仲生」。
#
# 2026-08-27 建立（里程碑 9：Production 監察）
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/idle-ping.env" ]; then
  # shellcheck disable=SC1091  # optional config file; may not exist on first run
  . "$SCRIPT_DIR/idle-ping.env"
fi
WS="${IDLE_PING_WS:-$(cd "$SCRIPT_DIR/.." && pwd)}"
HEARTBEAT_FILE="${IDLE_PING_HEARTBEAT_FILE:-$WS/curiosity/heartbeat.txt}"
HEARTBEAT_URL="${IDLE_PING_HEARTBEAT_URL:-}"

# 1. 更新本地心跳檔（epoch 秒，watchdog.sh 直接讀）
mkdir -p "$(dirname "$HEARTBEAT_FILE")"
date +%s > "$HEARTBEAT_FILE"

# 2. 外部監察 ping（可選）— 失敗唔好炸，淨係記低
if [ -n "$HEARTBEAT_URL" ]; then
  if ! curl -fsS -m 10 -o /dev/null "$HEARTBEAT_URL" 2>/dev/null; then
    echo "$(date +%s) heartbeat ping failed" >> "$HEARTBEAT_FILE"
    exit 1
  fi
fi
exit 0
