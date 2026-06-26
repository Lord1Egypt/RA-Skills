#!/bin/bash
# sync-daily.sh - 同步每日日志到 CortexGraph
# 用法: ./sync-daily.sh [YYYY-MM-DD] [--dry-run]

set -e

DATE="${1:-$(date +%Y-%m-%d)}"
DRY_RUN="${2:-}"
MEMORY_DIR="$HOME/.openclaw/workspace/memory"
DAILY_FILE="$MEMORY_DIR/$DATE.md"

echo "🧠 同步每日日志 → CortexGraph"
echo "   日期: $DATE"
echo "   文件: $DAILY_FILE"

if [[ ! -f "$DAILY_FILE" ]]; then
    echo "❌ 日志文件不存在: $DAILY_FILE"
    exit 1
fi

# 读取文件内容
CONTENT=$(cat "$DAILY_FILE")

# 检查是否为空
if [[ -z "${CONTENT// /}" ]]; then
    echo "⚠️  日志为空"
    exit 0
fi

# 转义内容
CONTENT_ESCAPED=$(echo "$CONTENT" | sed 's/"/\\"/g')

# 确定标签
DAY_TAG="daily-$DATE"

echo "  📌 导入每日日志 ($DATE)"

if [[ "$DRY_RUN" != "--dry-run" ]]; then
    mcporter call cortexgraph.save_memory \
        --config ~/.openclaw/workspace/config/mcporter.json \
        content="[$DATE] $CONTENT_ESCAPED" \
        tags='["daily-log","'"$DAY_TAG"'"]' \
        source="memory/$DATE.md" \
        strength=1.0
    echo "✅ 同步完成"
else
    echo "  [DRY RUN] 跳过保存"
    echo "---"
    echo "内容预览:"
    echo "$CONTENT" | head -20
fi
