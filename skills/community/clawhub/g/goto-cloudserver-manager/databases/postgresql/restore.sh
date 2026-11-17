#!/bin/bash
# restore.sh - 从备份文件恢复 PostgreSQL 数据库
set -euo pipefail

DATABASE_NAME="${1:-}"
SOURCE="${2:-}"
PG_USER="${3:-postgres}"

[ -z "$DATABASE_NAME" ] && echo "用法: $0 <数据库名> <备份文件> [用户名]" && exit 1
[ -z "$SOURCE" ] && echo "用法: $0 <数据库名> <备份文件> [用户名]" && exit 1
[ -f "$SOURCE" ] || { echo "[ERROR] 备份文件不存在：$SOURCE"; exit 1; }

log() { echo "[$(date '+%H:%M:%S')] $*"; }

log "确保数据库 $DATABASE_NAME 存在..."
PGPASSWORD="${PGPASSWORD:-}" psql -U "$PG_USER" -d postgres -c \
    "SELECT 'CREATE DATABASE \"${DATABASE_NAME}\"' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${DATABASE_NAME}')\gexec"

log "从 $SOURCE 恢复数据库 $DATABASE_NAME..."
case "$SOURCE" in
    *.dump)
        PGPASSWORD="${PGPASSWORD:-}" pg_restore -U "$PG_USER" -d "$DATABASE_NAME" --clean --if-exists "$SOURCE"
        ;;
    *)
        PGPASSWORD="${PGPASSWORD:-}" psql -U "$PG_USER" -d "$DATABASE_NAME" -f "$SOURCE"
        ;;
esac

log "恢复完成"
exit 0
