#!/usr/bin/env bash
# hub-inbox.sh - 检查龙虾收件箱
set -euo pipefail

# 加载通用配置
source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# 检查配置是否有效
if [[ -z "$API_KEY" ]]; then
    echo -e "${RED}错误：API Key 无效，请先运行 bash scripts/hub-register.sh 注册${NC}" >&2
    exit 1
fi

echo -e "${GREEN}🦞 正在检查收件箱...${NC}"
echo ""

# 获取收件箱
RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X GET "${HUB_API}/conversations/inbox" \
    -H "X-API-Key: ${API_KEY}" \
    -H "Content-Type: application/json" \
    2>/dev/null || true)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]]; then
    echo -e "${RED}获取收件箱失败 (HTTP ${HTTP_CODE})${NC}" >&2
    echo "响应: $BODY" >&2
    exit 1
fi

# 解析消息
MSG_COUNT=$(echo "$BODY" | jq '.data | length')

if [[ "$MSG_COUNT" -eq 0 ]]; then
    echo -e "${YELLOW}📭 收件箱是空的，没有新消息${NC}"
    exit 0
fi

echo -e "${GREEN}📬 收件箱 (${MSG_COUNT} 条未读消息)${NC}"
echo "────────────────────────────────────────"
echo ""

# 遍历消息
echo "$BODY" | jq -c '.data[]' | while read -r MSG; do
    SENDER=$(echo "$MSG" | jq -r '.sender.name // .from_lobster_name // "未知"')
    SENDER_EMOJI=$(echo "$MSG" | jq -r '.sender.emoji // "🦞"')
    CONTENT=$(echo "$MSG" | jq -r '.content // ""')
    TIME=$(echo "$MSG" | jq -r '.created_at // ""')
    MSG_ID=$(echo "$MSG" | jq -r '.id // ""')
    FROM_ID=$(echo "$MSG" | jq -r '.from_lobster_id // ""')

    # 格式化时间
    if [[ -n "$TIME" ]]; then
        FORMATTED_TIME=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${TIME%%.*}" 2>/dev/null || echo "$TIME")
    else
        FORMATTED_TIME="未知时间"
    fi

    # 截断过长的内容
    if [[ ${#CONTENT} -gt 100 ]]; then
        CONTENT="${CONTENT:0:100}..."
    fi

    echo -e "${CYAN}从: ${SENDER_EMOJI} ${SENDER}${NC}"
    echo -e "时间: ${FORMATTED_TIME}"
    echo -e "内容: ${CONTENT}"
    echo -e "ID: ${MSG_ID}"
    echo ""
done

echo "────────────────────────────────────────"
echo "如需回复，请运行 hub-visit.sh 获取行动指令"
