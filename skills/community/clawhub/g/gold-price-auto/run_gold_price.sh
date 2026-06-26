#!/bin/bash
# 金价自动汇报脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLAYWRIGHT_DIR="$SCRIPT_DIR/../playwright-scraper-skill"

echo "=== 💰 金价自动汇报 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M')"
echo ""

# 使用playwright获取金价
cd "$PLAYWRIGHT_DIR"
OUTPUT=$(node scripts/playwright-simple.js "http://www.huangjinjiage.cn/jinrijinjia.html" 2>&1)

# 提取关键信息
echo "$OUTPUT" | grep -oE '[0-9]{4}\.[0-9]+元/克' | head -20
echo ""
echo "数据来源: 金价查询网 huangjinjiage.cn"
