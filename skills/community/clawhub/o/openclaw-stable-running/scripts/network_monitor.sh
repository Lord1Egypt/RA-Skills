#!/bin/bash
LOG_FILE="/var/log/openclaw/network_monitor.log"
MAIN_IFACE="${MAIN_IFACE:-eth0}"
BACKUP_IFACE="${BACKUP_IFACE:-wlan0}"
CHECK_TARGET="${CHECK_TARGET:-8.8.8.8}"
CHECK_COUNT=3
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"; }
check_iface() { ping -c $CHECK_COUNT -I $1 $CHECK_TARGET > /dev/null 2>&1; }
log "网络监控启动，备用: $MAIN_IFACE -> $BACKUP_IFACE"
while true; do
  if ! check_iface $MAIN_IFACE; then
    log "主网络异常，切换到 $BACKUP_IFACE"
    ip route replace default dev $BACKUP_IFACE 2>> "$LOG_FILE"
  fi
  sleep 30
done
