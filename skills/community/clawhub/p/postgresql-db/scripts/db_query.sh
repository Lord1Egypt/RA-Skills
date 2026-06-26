#!/bin/bash
# PostgreSQL 查询脚本
# 用法：./db_query.sh "SELECT * FROM 表名 LIMIT 10;"

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
if [ -z "$1" ]; then
    echo "用法：$0 \"SQL 查询语句\""
    echo "示例：$0 \"SELECT * FROM users LIMIT 10;\""
    exit 1
fi

# 执行查询
PGPASSWORD="${DB_PASSWORD}" psql \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    -c "$1"
