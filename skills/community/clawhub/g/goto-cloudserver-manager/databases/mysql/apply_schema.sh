#!/bin/bash
# apply_schema.sh - 在 MySQL 上执行建表 DDL
set -euo pipefail

DATABASE_NAME="${1:-}"
SQL_FILE="${2:-}"
MYSQL_USER="${3:-root}"
MYSQL_PASSWORD="${4:-}"

[ -z "$DATABASE_NAME" ] && echo "用法: $0 <数据库名> <SQL文件> [用户名] [密码]" && exit 1
[ -z "$SQL_FILE" ] && echo "用法: $0 <数据库名> <SQL文件> [用户名] [密码]" && exit 1
[ -f "$SQL_FILE" ] || { echo "[ERROR] SQL 文件不存在：$SQL_FILE"; exit 1; }

log() { echo "[$(date '+%H:%M:%S')] $*"; }

log "在数据库 $DATABASE_NAME 上执行 Schema..."
if [ -n "$MYSQL_PASSWORD" ]; then
    mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$DATABASE_NAME" < "$SQL_FILE"
else
    mysql -u"$MYSQL_USER" "$DATABASE_NAME" < "$SQL_FILE"
fi

log "Schema 执行完成"
exit 0
