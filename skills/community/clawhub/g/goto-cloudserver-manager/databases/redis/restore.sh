#!/bin/bash
# restore.sh - 从 RDB 备份文件恢复 Redis（db_name 对 Redis 无意义，忽略）
set -euo pipefail

SOURCE="${2:-}"
REDIS_PORT="${3:-6379}"
REDIS_PASSWORD="${4:-}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
err() { echo "[ERROR] $*" >&2; exit 1; }

[ -z "$SOURCE" ] && err "用法: $0 <忽略> <备份文件> [端口] [密码]"
[ -f "$SOURCE" ] || err "备份文件不存在：$SOURCE"

REDIS_AUTH=()
[ -n "$REDIS_PASSWORD" ] && REDIS_AUTH=(-a "$REDIS_PASSWORD")

detect_service() {
    systemctl is-active redis-server &>/dev/null && echo "redis-server" && return
    systemctl is-active redis &>/dev/null && echo "redis" && return
    err "未找到运行中的 Redis 服务"
}

SERVICE=$(detect_service)
RDB_DIR=$(redis-cli -p "$REDIS_PORT" "${REDIS_AUTH[@]}" CONFIG GET dir | tail -1)
RDB_FILE=$(redis-cli -p "$REDIS_PORT" "${REDIS_AUTH[@]}" CONFIG GET dbfilename | tail -1)
RDB_PATH="${RDB_DIR}/${RDB_FILE}"

log "停止 $SERVICE..."
systemctl stop "$SERVICE"

log "用 $SOURCE 覆盖 $RDB_PATH..."
cp "$SOURCE" "$RDB_PATH"
chown redis:redis "$RDB_PATH" 2>/dev/null || true

log "启动 $SERVICE..."
systemctl start "$SERVICE"
sleep 2

redis-cli -p "$REDIS_PORT" "${REDIS_AUTH[@]}" ping | grep -q "PONG" && \
    log "恢复完成，Redis 已启动" || \
    err "Redis 启动验证失败"

exit 0
