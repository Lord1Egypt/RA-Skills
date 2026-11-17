#!/bin/bash
# backup.sh - 备份 PostgreSQL 数据库
set -euo pipefail

DATABASE_NAME="${1:-}"
DEST="${2:-/backup}"
PG_USER="${3:-postgres}"

[ -z "$DATABASE_NAME" ] && echo "用法: $0 <数据库名> <备份目录> [用户名]" && exit 1

log() { echo "[$(date '+%H:%M:%S')] $*"; }

mkdir -p "$DEST"
BACKUP_FILE="$DEST/${DATABASE_NAME}_$(date '+%Y%m%d_%H%M%S').dump"

log "备份数据库 $DATABASE_NAME 到 $BACKUP_FILE..."
PGPASSWORD="${PGPASSWORD:-}" pg_dump -U "$PG_USER" -d "$DATABASE_NAME" -F c -f "$BACKUP_FILE"

log "备份完成：$BACKUP_FILE（$(du -h "$BACKUP_FILE" | cut -f1)）"
echo "BACKUP_FILE=${BACKUP_FILE}"
exit 0
