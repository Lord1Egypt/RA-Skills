#!/bin/bash
# restore.sh - 从备份文件恢复 MySQL 数据库
set -euo pipefail

DATABASE_NAME="${1:-}"
SOURCE="${2:-}"
MYSQL_USER="${3:-root}"
MYSQL_PASSWORD="${4:-}"

[ -z "$DATABASE_NAME" ] && echo "用法: $0 <数据库名> <备份文件> [用户名] [密码]" && exit 1
[ -z "$SOURCE" ] && echo "用法: $0 <数据库名> <备份文件> [用户名] [密码]" && exit 1
[ -f "$SOURCE" ] || { echo "[ERROR] 备份文件不存在：$SOURCE"; exit 1; }

log() { echo "[$(date '+%H:%M:%S')] $*"; }

MYSQL_AUTH=(-u"$MYSQL_USER")
[ -n "$MYSQL_PASSWORD" ] && MYSQL_AUTH+=(-p"$MYSQL_PASSWORD")

log "确保数据库 $DATABASE_NAME 存在..."
mysql "${MYSQL_AUTH[@]}" -e "CREATE DATABASE IF NOT EXISTS \`${DATABASE_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

log "从 $SOURCE 恢复数据库 $DATABASE_NAME..."
case "$SOURCE" in
    *.gz)
        gunzip -c "$SOURCE" | mysql "${MYSQL_AUTH[@]}" "$DATABASE_NAME"
        ;;
    *)
        mysql "${MYSQL_AUTH[@]}" "$DATABASE_NAME" < "$SOURCE"
        ;;
esac

log "恢复完成"
exit 0
