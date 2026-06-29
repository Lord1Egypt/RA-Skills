#!/bin/bash
# backup.sh - 备份 Redis（BGSAVE 后复制 RDB 文件，db_name 对 Redis 无意义，忽略）
set -euo pipefail

DEST="${2:-/backup}"
REDIS_PORT="${3:-6379}"
REDIS_PASSWORD="${4:-}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
err() { echo "[ERROR] $*" >&2; exit 1; }

REDIS_AUTH=()
[ -n "$REDIS_PASSWORD" ] && REDIS_AUTH=(-a "$REDIS_PASSWORD")

RDB_DIR=$(redis-cli -p "$REDIS_PORT" "${REDIS_AUTH[@]}" CONFIG GET dir | tail -1)
RDB_FILE=$(redis-cli -p "$REDIS_PORT" "${REDIS_AUTH[@]}" CONFIG GET dbfilename | tail -1)
RDB_PATH="${RDB_DIR}/${RDB_FILE}"

log "触发 BGSAVE..."
redis-cli -p "$REDIS_PORT" "${REDIS_AUTH[@]}" BGSAVE >/dev/null

# 等待 BGSAVE 完成
for _ in $(seq 1 30); do
    [ "$(redis-cli -p "$REDIS_PORT" "${REDIS_AUTH[@]}" INFO persistence | grep -c 'rdb_bgsave_in_progress:0')" = "1" ] && break
    sleep 1
done

[ -f "$RDB_PATH" ] || err "未找到 RDB 文件：$RDB_PATH"

mkdir -p "$DEST"
BACKUP_FILE="$DEST/redis_$(date '+%Y%m%d_%H%M%S').rdb"
cp "$RDB_PATH" "$BACKUP_FILE"

log "备份完成：$BACKUP_FILE（$(du -h "$BACKUP_FILE" | cut -f1)）"
echo "BACKUP_FILE=${BACKUP_FILE}"
exit 0
