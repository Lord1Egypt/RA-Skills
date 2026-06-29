#!/bin/bash
# apply_schema.sh - 在 PostgreSQL 上执行建表 DDL
set -euo pipefail

DATABASE_NAME="${1:-}"
SQL_FILE="${2:-}"
PG_USER="${3:-postgres}"

[ -z "$DATABASE_NAME" ] && echo "用法: $0 <数据库名> <SQL文件> [用户名]" && exit 1
[ -z "$SQL_FILE" ] && echo "用法: $0 <数据库名> <SQL文件> [用户名]" && exit 1
[ -f "$SQL_FILE" ] || { echo "[ERROR] SQL 文件不存在：$SQL_FILE"; exit 1; }

log() { echo "[$(date '+%H:%M:%S')] $*"; }

log "在 PostgreSQL 数据库 $DATABASE_NAME 上执行 Schema..."
PGPASSWORD="${PGPASSWORD:-}" psql -U "$PG_USER" -d "$DATABASE_NAME" -f "$SQL_FILE"

log "Schema 执行完成"
exit 0
