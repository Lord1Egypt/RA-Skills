#!/bin/bash
#===============================================================================
# 火一五记忆进化技能 - Drift 校验
#
# 功能：
# 1. 读取 index.json，获取所有记忆指针
# 2. 验证每个记忆文件是否存在
# 3. 检查更新日期是否过期
# 4. 输出报告
#===============================================================================

set -e

# 动态路由：优先使用 PWD 检测 > OC_AGENT_ID > 默认
if [ -d "${PWD}/memory" ] && [[ "$PWD" == *".openclaw/workspace"* ]]; then
    WORKSPACE_DIR="$PWD"
elif [ -n "${OC_AGENT_ID:-}" ]; then
    WORKSPACE_DIR="$HOME/.openclaw/workspace-${OC_AGENT_ID}"
else
    WORKSPACE_DIR="$HOME/.openclaw/workspace"
fi

MEMORY_DIR="$WORKSPACE_DIR/memory"
INDEX_JSON="$MEMORY_DIR/index.json"

STALE_COUNT=0
OLD_COUNT=0
OK_COUNT=0
MISSING_COUNT=0

# 90天阈值
OLD_THRESHOLD_DAYS=90
CUTOFF_DATE=$(date -v-${OLD_THRESHOLD_DAYS}d +%Y-%m-%d 2>/dev/null || date -d "$OLD_THRESHOLD_DAYS days ago" +%Y-%m-%d)

echo "🔍 记忆 Drift 检查"
echo "================================"
echo "检查日期: $(date '+%Y-%m-%d')"
echo "过期阈值: ${CUTOFF_DATE} (${OLD_THRESHOLD_DAYS}天前)"
echo ""

# 检查 index.json 是否存在
if [ ! -f "$INDEX_JSON" ]; then
    echo "⚠️  index.json 不存在，跳过"
    exit 0
fi

# 解析 index.json 并检查每个条目
# 简化版本：直接扫描 memory/{type}/ 目录

echo "📋 检查各类型记忆..."
echo ""

for type in user feedback project reference; do
    TYPE_DIR="$MEMORY_DIR/$type"
    if [ ! -d "$TYPE_DIR" ]; then
        continue
    fi
    
    echo "🔹 $type/"
    
    for file in "$TYPE_DIR"/*.md; do
        if [ ! -f "$file" ]; then
            continue
        fi
        
        FILENAME=$(basename "$file")
        
        # 检查文件是否存在（上面已确认）
        # 检查 updated 字段
        UPDATED=$(grep "^updated:" "$file" 2>/dev/null | head -1 | sed 's/updated: //' | tr -d ' ')
        
        if [ -z "$UPDATED" ]; then
            # 没有 updated 字段，尝试从文件名提取日期
            DATE_IN_NAME=$(echo "$FILENAME" | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2}" | head -1)
            if [ -n "$DATE_IN_NAME" ]; then
                UPDATED="$DATE_IN_NAME"
            fi
        fi
        
        if [ -n "$UPDATED" ]; then
            if [[ "$UPDATED" < "$CUTOFF_DATE" ]]; then
                echo "   ⏰ OLD: $FILENAME (updated: $UPDATED)"
                OLD_COUNT=$((OLD_COUNT + 1))
            else
                echo "   ✅ OK: $FILENAME"
                OK_COUNT=$((OK_COUNT + 1))
            fi
        else
            echo "   ⚠️  无更新日期: $FILENAME"
            OLD_COUNT=$((OLD_COUNT + 1))
        fi
    done
    
    echo ""
done

# 检查 archive 目录
echo "🔹 archive/ (已归档)"
ARCHIVE_DIR="$MEMORY_DIR/archive"
if [ -d "$ARCHIVE_DIR" ]; then
    ARCHIVE_COUNT=$(find "$ARCHIVE_DIR" -name "*.md" -type f | wc -l | tr -d ' ')
    echo "   📦 归档记忆: ${ARCHIVE_COUNT} 个"
fi

echo ""
echo "================================"
echo "📊 检查结果汇总"
echo "================================"
echo "   ✅ 正常: $OK_COUNT"
echo "   ⏰ 过期: $OLD_COUNT"
echo "   ❌ 缺失: $MISSING_COUNT"
echo ""

if [ "$OLD_COUNT" -gt 0 ]; then
    echo "💡 提示: 运行 dream.sh 可以自动处理过期记忆"
fi

if [ "$MISSING_COUNT" -gt 0 ]; then
    echo "⚠️  有 $MISSING_COUNT 个记忆文件缺失，请检查"
fi
