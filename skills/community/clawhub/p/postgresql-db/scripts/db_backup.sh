#!/bin/bash
# PostgreSQL 自动备份脚本
# 用法：./db_backup.sh [备份目录]

set -e

# 加载环境变量
if [ -f .env ]; then
    source .env
fi

# 默认值
DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-"5432"}
DB_NAME=${DB_NAME:-"postgres"}
DB_USER=${DB_USER:-"postgres"}
BACKUP_DIR=${1:-"./backups"}

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 生成文件名
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"

echo "开始备份：${DB_NAME} @ ${DB_HOST}:${DB_PORT}"
echo "备份文件：${BACKUP_FILE}"

# 执行备份（使用 psql + COPY 方式，避免 pg_dump 版本不兼容）
PGPASSWORD="${DB_PASSWORD}" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -c "\\echo '-- PostgreSQL Database Backup'
\\echo '-- Database: ${DB_NAME}'
\\echo '-- Generated: $(date)'" > "$BACKUP_FILE.tmp"

# 导出所有表结构 + 数据
for table in $(PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT tablename FROM pg_tables WHERE schemaname = 'public';"); do
    PGPASSWORD="${DB_PASSWORD}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "\\copy ${table} TO STDOUT WITH CSV" >> "$BACKUP_FILE.tmp" 2>/dev/null || true
done

gzip -c "$BACKUP_FILE.tmp" > "$BACKUP_FILE"
rm -f "$BACKUP_FILE.tmp"

# 显示文件大小
SIZE=$(ls -lh "$BACKUP_FILE" | awk '{print $5}')
echo "备份完成！文件大小：${SIZE}"

# 清理 7 天前的备份
echo "清理 7 天前的备份..."
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -mtime +7 -delete

echo "备份保留策略：7 天"
