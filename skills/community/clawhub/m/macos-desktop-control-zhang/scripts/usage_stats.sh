#!/bin/bash
# 查看本地技能使用统计

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_FILE="$SCRIPT_DIR/controlmemory.md"

echo "╔════════════════════════════════════════╗"
echo "║   macOS Desktop Control 使用统计       ║"
echo "╚════════════════════════════════════════╝"
echo ""

if [ ! -f "$MEMORY_FILE" ]; then
    echo "❌ ControlMemory 文件不存在"
    exit 1
fi

# 统计总操作数
total_ops=$(grep -c "^#### " "$MEMORY_FILE")
echo "📊 总操作数：$total_ops"

# 统计总借鉴次数
total_usage=$(grep -oP '👁️ \K\d+' "$MEMORY_FILE" | awk '{sum+=$1} END {print sum}')
echo "👁️ 总借鉴次数：${total_usage:-0}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 按应用统计
echo "📱 按应用统计:"
echo ""

# 提取应用名称和借鉴次数
grep -E "^### |👁️" "$MEMORY_FILE" | while read -r line; do
    if [[ $line == "### "* ]]; then
        app_name="${line//### /}"
        app_usage=0
    elif [[ $line == *"👁️"* ]]; then
        usage=$(echo "$line" | grep -oP '👁️ \K\d+')
        app_usage=$((app_usage + usage))
        echo "  $app_name: 👁️ $app_usage 次"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 显示最热门操作
echo "🔥 最热门操作（借鉴次数前 5）:"
echo ""

grep -B5 "👁️" "$MEMORY_FILE" | grep -E "^#### |👁️" | paste - - | sort -t'👁️' -k2 -rn | head -5 | while read -r line; do
    op_name=$(echo "$line" | cut -f1 | sed 's/#### //')
    usage=$(echo "$line" | grep -oP '👁️ \K\d+')
    echo "  $op_name 👁️ $usage 次"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "统计时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "💡 提示："
echo "   这些是本地使用统计"
echo "   ClawHub 社区统计功能开发中..."
