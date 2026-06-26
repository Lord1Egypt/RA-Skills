#!/bin/bash
# PostgreSQL 导出 CSV 脚本
# 用法：./db_export_csv.sh 表名 输出文件.csv

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

# 检查参数
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "用法：$0 表名 输出文件.csv"
    echo "示例：$0 users users_export.csv"
    exit 1
fi

TABLE=$1
OUTPUT=$2

echo "导出表：${TABLE}"
echo "输出文件：${OUTPUT}"

# 执行导出
PGPASSWORD="${DB_PASSWORD}" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -c "\\copy ${TABLE} TO '${OUTPUT}' WITH CSV HEADER"

# 显示行数
LINES=$(wc -l < "$OUTPUT")
echo "导出完成！共 ${LINES} 行"
