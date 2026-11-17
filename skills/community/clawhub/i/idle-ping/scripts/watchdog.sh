#!/usr/bin/env bash
# watchdog.sh — 心跳過期偵測（cron 靜靜雞死 alert）
# 用途：檢查心跳檔幾耐冇更新；超過 IDLE_PING_WATCHDOG_STALE_MIN 分鐘 → alert。
#       alert = 寫入 system-activity.log + （可選）ping 外部監察服務嘅 /fail 端點。
# 建議由 cron job 定期執行（install.sh 會建立 idle-ping-watchdog job，預設每 1 小時）。
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
STALE_MIN="${IDLE_PING_WATCHDOG_STALE_MIN:-60}"
HEARTBEAT_URL="${IDLE_PING_HEARTBEAT_URL:-}"
LOG_FILE="$WS/curiosity/system-activity.log"
NOW="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

if [ ! -f "$HEARTBEAT_FILE" ]; then
  echo "$NOW | 🚨 watchdog: heartbeat file missing — idle-ping cron may be dead" >> "$LOG_FILE"
  exit 1
fi

LAST_EPOCH="$(head -1 "$HEARTBEAT_FILE")"
# 心跳檔第一行應該係 epoch 數字；解析失敗當 0（= 極度過期）
case "$LAST_EPOCH" in
  ''|*[!0-9]*) LAST_EPOCH=0 ;;
esac
NOW_EPOCH="$(date +%s)"
AGE_MIN=$(( (NOW_EPOCH - LAST_EPOCH) / 60 ))

if [ "$AGE_MIN" -gt "$STALE_MIN" ]; then
  echo "$NOW | 🚨 watchdog: heartbeat stale ${AGE_MIN}min (> ${STALE_MIN}min) — idle-ping cron may be dead" >> "$LOG_FILE"
  if [ -n "$HEARTBEAT_URL" ]; then
    # Healthchecks.io 等服務支援 /fail 端點 → 即刻 send alert 通知
    curl -fsS -m 10 -o /dev/null "$HEARTBEAT_URL/fail" 2>/dev/null || true
  fi
  exit 1
fi
exit 0
