#!/bin/bash
# extract_kettle_sql_simple.sh
# Kettle SQL提取脚本（只要SQL文件模式）
# 用法：./extract_kettle_sql_simple.sh <源目录> <目标目录>

set -e

# 检查参数
if [ $# -lt 2 ]; then
    echo "用法: $0 <源目录> <目标目录>"
    echo "示例: $0 /path/to/kettle/jobs /path/to/sql/output"
    echo ""
    echo "功能："
    echo "  1. 提取源目录中所有Kettle作业(.kjb/.ktr)的SQL"
    echo "  2. 只生成SQL文件，不生成其他文件"
    echo "  3. 将SQL文件保存到目标目录"
    exit 1
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"

# 检查源目录是否存在
if [ ! -d "$SOURCE_DIR" ]; then
    echo "错误：源目录不存在: $SOURCE_DIR"
    exit 1
fi

# 创建目标目录
mkdir -p "$TARGET_DIR"

# 切换到目标目录
cd "$TARGET_DIR"

# 查找Kettle文件
KETTLE_FILES=$(find "$SOURCE_DIR" -name "*.kjb" -o -name "*.ktr" | head -20)

if [ -z "$KETTLE_FILES" ]; then
    echo "在目录 $SOURCE_DIR 中未找到Kettle文件(.kjb/.ktr)"
    exit 1
fi

# 统计文件数量
FILE_COUNT=$(echo "$KETTLE_FILES" | wc -l)
echo "找到 $FILE_COUNT 个Kettle文件"

# 处理每个文件
SUCCESS_COUNT=0
FAIL_COUNT=0

for FILE in $KETTLE_FILES; do
    FILENAME=$(basename "$FILE")
    echo "处理: $FILENAME"
    
    # 使用简化输出模式提取SQL
    if python3 ~/.openclaw/workspace/skills/kettle-sql-extractor/merge_kettle_sql.py "$FILE" --simple-output 2>/dev/null; then
        echo "  ✅ 成功"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "  ❌ 失败"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
done

# 统计生成的SQL文件
SQL_FILES=$(find . -name "*_merged_detailed.sql" | wc -l)

echo ""
echo "================================"
echo "提取完成！"
echo "================================"
echo "源目录: $SOURCE_DIR"
echo "目标目录: $TARGET_DIR"
echo "处理文件: $FILE_COUNT 个"
echo "成功: $SUCCESS_COUNT 个"
echo "失败: $FAIL_COUNT 个"
echo "生成的SQL文件: $SQL_FILES 个"
echo ""
echo "生成的SQL文件列表:"
find . -name "*_merged_detailed.sql" -exec basename {} \; | sort
echo ""
echo "注意事项:"
echo "1. 只生成了SQL文件，没有HTML报告、JSON总结等额外文件"
echo "2. SQL保持原样，未做任何修改"
echo "3. 每个Kettle作业对应一个SQL文件"
echo "4. 文件名格式: job_作业名称_merged_detailed.sql"