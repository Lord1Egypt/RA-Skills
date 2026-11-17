#!/bin/bash
# backup.sh - 备份 MySQL 数据库
set -euo pipefail

DATABASE_NAME="${1:-}"
DEST="${2:-/backup}"
MYSQL_USER="${3:-root}"
MYSQL_PASSWORD="${4:-}"

[ -z "$DATABASE_NAME" ] && echo "用法: $0 <数据库名> <备份目录> [用户名] [密码]" && exit 1

log() { echo "[$(date '+%H:%M:%S')] $*"; }

mkdir -p "$DEST"
BACKUP_FILE="$DEST/${DATABASE_NAME}_$(date '+%Y%m%d_%H%M%S').sql.gz"

log "备份数据库 $DATABASE_NAME 到 $BACKUP_FILE..."
if [ -n "$MYSQL_PASSWORD" ]; then
    mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --single-transaction --routines --triggers "$DATABASE_NAME" | gzip > "$BACKUP_FILE"
else
    mysqldump -u"$MYSQL_USER" --single-transaction --routines --triggers "$DATABASE_NAME" | gzip > "$BACKUP_FILE"
fi

log "备份完成：$BACKUP_FILE（$(du -h "$BACKUP_FILE" | cut -f1)）"
echo "BACKUP_FILE=${BACKUP_FILE}"
exit 0
