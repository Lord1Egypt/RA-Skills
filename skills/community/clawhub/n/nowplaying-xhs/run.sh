#!/bin/bash
# NowPlaying - 院线电影推荐 Cron 执行脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_FILE="/tmp/nowplaying_$(date +%Y%m%d).md"

echo "🎬 开始执行 NowPlaying 院线推荐..."
echo "📅 日期：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 执行 Python 脚本
cd "$SCRIPT_DIR"
python3 nowplaying.py > "$OUTPUT_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 电影推荐生成成功"
    echo "📄 报告路径：$OUTPUT_FILE"
    
    # 显示前 20 行预览
    echo ""
    echo "📋 预览:"
    head -20 "$OUTPUT_FILE"
else
    echo "❌ 执行失败"
    cat "$OUTPUT_FILE"
    exit 1
fi
