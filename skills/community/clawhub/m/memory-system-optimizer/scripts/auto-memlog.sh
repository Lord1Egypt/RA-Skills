#!/bin/bash
# auto-memlog.sh - 自动记忆工具
# 用法: ./auto-memlog.sh "标题" "内容"

TITLE="$1"
CONTENT="$2"
DATE=$(date +%Y-%m-%d)
MEMORY_FILE="$HOME/.openclaw/workspace/memory/${DATE}.md"

if [ -z "$TITLE" ]; then
    echo "用法: auto-memlog.sh \"标题\" \"内容\""
    exit 1
fi

# 如果今天的记忆文件不存在，创建它
if [ ! -f "$MEMORY_FILE" ]; then
    echo "# ${DATE} 工作日志" > "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
    echo "## 完成事项" >> "$MEMORY_FILE"
fi

# 追加内容
TIME=$(date +%H:%M)
echo "### ${TIME} — ${TITLE}" >> "$MEMORY_FILE"
echo "${CONTENT}" >> "$MEMORY_FILE"
echo "" >> "$MEMORY_FILE"

echo "✅ 已记录到 ${MEMORY_FILE}"
