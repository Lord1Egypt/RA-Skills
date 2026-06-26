#!/bin/bash
# LifeLog Daily Summary v5.0
# 第一步：从 Notion 拉取当天原文
# 第二步：输出原文供 LLM 分析（由 cron agentTurn 调用）
# 第三步：LLM 分析后调用 lifelog-update.sh 回写
# 使用前请配置下方的 NOTION_KEY 和 DATABASE_ID

# ===== 配置区域 =====
NOTION_KEY="YOUR_NOTION_API_KEY"
DATABASE_ID="YOUR_DATABASE_ID"
# ====================

# 支持指定日期，默认昨天（因为凌晨5点跑的是昨天的汇总）
if [ -n "$1" ]; then
    TARGET_DATE="$1"
else
    TARGET_DATE=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
fi

echo "📅 拉取 $TARGET_DATE 的 LifeLog 原文..."

RESPONSE=$(curl -s -X POST "https://api.notion.com/v1/databases/$DATABASE_ID/query" \
    -H "Authorization: Bearer $NOTION_KEY" \
    -H "Notion-Version: $API_VERSION" \
    -H "Content-Type: application/json" \
    -d "{\"filter\": { \"property\": \"日期\", \"title\": { \"equals\": \"$TARGET_DATE\" } }}")

TOTAL=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])))")

if [ "$TOTAL" -eq 0 ]; then
    echo "该日期无记录"
    exit 0
fi

# 提取 page_id 和原文
PAGE_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['id'])")
ORIGINAL=$(echo "$RESPONSE" | python3 -c "
import sys,json
d=json.load(sys.stdin)
props=d['results'][0]['properties']
txt=''
if '原文' in props and props['原文'].get('rich_text'):
    txt=props['原文']['rich_text'][0].get('plain_text','')
print(txt)
")

echo "PAGE_ID=$PAGE_ID"
echo "---原文开始---"
echo "$ORIGINAL"
echo "---原文结束---"
