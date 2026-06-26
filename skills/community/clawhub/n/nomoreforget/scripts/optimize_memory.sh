#!/bin/bash
# No More Forget 记忆优化脚本
# 精简 MEMORY.md，归档旧日志

echo "🔧 记忆优化开始..."
echo ""

WORKSPACE_DIR="$HOME/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE_DIR/memory"
MEMORY_FILE="$WORKSPACE_DIR/MEMORY.md"

# 1. 检查 MEMORY.md 长度
if [ -f "$MEMORY_FILE" ]; then
    LINES=$(wc -l < "$MEMORY_FILE")
    
    if [ $LINES -gt 500 ]; then
        echo "📝 MEMORY.md 当前 $LINES 行，建议精简"
        echo ""
        echo "优化建议："
        echo "  1. 删除过时的项目信息"
        echo "  2. 将详细的决策记录移到 memory/topics/ 目录"
        echo "  3. 保留关键规则和重要决策在 MEMORY.md"
        echo ""
        echo "重要：将最关键的信息放在文件开头和结尾！"
    else
        echo "✅ MEMORY.md 行数正常 ($LINES 行)"
    fi
else
    echo "⚠️  MEMORY.md 不存在"
fi

# 2. 归档旧日志
echo ""
echo "📦 检查 Daily Logs..."

if [ -d "$MEMORY_DIR" ]; then
    ARCHIVE_DIR="$MEMORY_DIR/archive"
    OLD_LOGS=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -mtime +30 2>/dev/null)
    
    if [ -n "$OLD_LOGS" ]; then
        OLD_COUNT=$(echo "$OLD_LOGS" | wc -l)
        echo "发现 $OLD_COUNT 个超过 30 天的日志文件"
        
        read -p "是否归档这些日志？(y/N) " -n 1 -r
        echo
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            mkdir -p "$ARCHIVE_DIR"
            
            for log in $OLD_LOGS; do
                mv "$log" "$ARCHIVE_DIR/"
            done
            
            echo "✅ 已归档 $OLD_COUNT 个日志到 $ARCHIVE_DIR/"
        fi
    else
        echo "✅ 未发现需要归档的旧日志"
    fi
fi

# 3. 显示记忆统计
echo ""
echo "📊 记忆统计："

if [ -f "$MEMORY_FILE" ]; then
    MEMORY_SIZE=$(du -h "$MEMORY_FILE" | cut -f1)
    MEMORY_LINES=$(wc -l < "$MEMORY_FILE")
    echo "  MEMORY.md: $MEMORY_LINES 行, $MEMORY_SIZE"
fi

if [ -d "$MEMORY_DIR" ]; then
    LOG_COUNT=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l)
    TOTAL_SIZE=$(du -sh "$MEMORY_DIR" 2>/dev/null | cut -f1)
    echo "  Daily Logs: $LOG_COUNT 个文件, $TOTAL_SIZE"
    
    if [ -d "$MEMORY_DIR/archive" ]; then
        ARCHIVE_COUNT=$(find "$MEMORY_DIR/archive" -name "*.md" 2>/dev/null | wc -l)
        echo "  归档日志: $ARCHIVE_COUNT 个文件"
    fi
fi

echo ""
echo "✅ 优化检查完成"