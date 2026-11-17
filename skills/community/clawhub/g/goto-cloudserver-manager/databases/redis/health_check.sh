#!/bin/bash
# databases/redis/health_check.sh - Redis 健康检查
set -euo pipefail

REDIS_PORT="${1:-6379}"
REDIS_PASSWORD="${2:-}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }

CLI_ARGS="-p $REDIS_PORT"
[ -n "$REDIS_PASSWORD" ] && CLI_ARGS="$CLI_ARGS -a $REDIS_PASSWORD"

log "Redis 健康检查（端口：$REDIS_PORT）"

# Ping
PONG=$(redis-cli $CLI_ARGS ping 2>/dev/null)
if [ "$PONG" != "PONG" ]; then
    echo '{"healthy": false, "error": "Redis ping 失败"}'
    exit 1
fi

# INFO 统计
INFO=$(redis-cli $CLI_ARGS info 2>/dev/null)

USED_MEM=$(echo "$INFO" | grep "^used_memory_human:" | cut -d: -f2 | tr -d '\r')
CONN=$(echo "$INFO" | grep "^connected_clients:" | cut -d: -f2 | tr -d '\r')
KEYS=$(redis-cli $CLI_ARGS dbsize 2>/dev/null || echo "0")
UPTIME=$(echo "$INFO" | grep "^uptime_in_seconds:" | cut -d: -f2 | tr -d '\r')
VERSION=$(echo "$INFO" | grep "^redis_version:" | cut -d: -f2 | tr -d '\r')
EVICTED=$(echo "$INFO" | grep "^evicted_keys:" | cut -d: -f2 | tr -d '\r')

cat << EOF
{
  "healthy": true,
  "version": "${VERSION}",
  "used_memory": "${USED_MEM}",
  "connected_clients": ${CONN},
  "total_keys": ${KEYS},
  "uptime_seconds": ${UPTIME},
  "evicted_keys": ${EVICTED:-0}
}
EOF
exit 0
