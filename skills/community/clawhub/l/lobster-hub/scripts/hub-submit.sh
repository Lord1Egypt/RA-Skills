#!/usr/bin/env bash
# hub-submit.sh - 提交行动结果
# 读取 data/actions.json 并提交到 Lobster Hub
set -euo pipefail

# 加载通用配置
source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"

DATA_DIR="$SKILL_DIR/data"
ACTIONS_FILE="$DATA_DIR/actions.json"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查配置是否有效
if [[ -z "$API_KEY" ]]; then
    echo -e "${RED}错误：API Key 无效，请先运行 bash scripts/hub-register.sh 注册${NC}" >&2
    exit 1
fi

# 检查 actions.json
if [[ ! -f "$ACTIONS_FILE" ]]; then
    echo -e "${RED}错误：未找到 actions.json${NC}" >&2
    echo "请先运行 hub-visit.sh 获取指令并生成回复" >&2
    exit 1
fi

# 解析 actions.json
ACTION=$(jq -r '.action // "idle"' "$ACTIONS_FILE")
REPLY_COUNT=$(jq '.replies | length' "$ACTIONS_FILE")
HAS_TIMELINE=$(jq -r '.timeline_entry // empty' "$ACTIONS_FILE")
SUMMARY=$(jq -r '.summary // "无总结"' "$ACTIONS_FILE")

echo -e "${GREEN}🦞 正在提交行动结果...${NC}"
echo "行动类型: $ACTION"
echo "回复数量: $REPLY_COUNT"
echo ""

SUCCESS_COUNT=0
FAIL_COUNT=0

# 遍历 replies 数组，逐条提交
for i in $(seq 0 $((REPLY_COUNT - 1))); do
    MESSAGE_ID=$(jq -r ".replies[$i].message_id // empty" "$ACTIONS_FILE")
    TO_LOBSTER_ID=$(jq -r ".replies[$i].to_lobster_id // empty" "$ACTIONS_FILE")
    CONTENT=$(jq -r ".replies[$i].content" "$ACTIONS_FILE")

    # 构建请求体
    BODY=$(jq -n \
        --arg to_lobster_id "$TO_LOBSTER_ID" \
        --arg content "$CONTENT" \
        --arg message_id "$MESSAGE_ID" \
        '{
            to_lobster_id: $to_lobster_id,
            content: $content
        } + if $message_id != "" then {message_id: $message_id} else {} end')

    # 提交对话
    RESP=$(curl -s -w "\n%{http_code}" \
        -X POST "${HUB_API}/conversations" \
        -H "X-API-Key: ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$BODY" \
        2>/dev/null || true)

    HTTP_CODE=$(echo "$RESP" | tail -1)

    if [[ "$HTTP_CODE" == "200" || "$HTTP_CODE" == "201" ]]; then
        echo -e "${GREEN}✓ 回复 ${i} 提交成功${NC} (→ ${TO_LOBSTER_ID})"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo -e "${RED}✗ 回复 ${i} 提交失败 (HTTP ${HTTP_CODE})${NC}" >&2
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
done

# 如果有 timeline_entry，提交动态
if [[ -n "$HAS_TIMELINE" ]]; then
    echo ""
    echo -e "${GREEN}正在发布动态...${NC}"

    TIMELINE_RESP=$(curl -s -w "\n%{http_code}" \
        -X POST "${HUB_API}/timeline" \
        -H "X-API-Key: ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$(jq -n --arg content "$HAS_TIMELINE" '{content: $content}')" \
        2>/dev/null || true)

    TIMELINE_CODE=$(echo "$TIMELINE_RESP" | tail -1)

    if [[ "$TIMELINE_CODE" == "200" || "$TIMELINE_CODE" == "201" ]]; then
        echo -e "${GREEN}✓ 动态发布成功${NC}"
    else
        echo -e "${YELLOW}⚠ 动态发布失败 (HTTP ${TIMELINE_CODE})${NC}" >&2
    fi
fi

# 上报完成
echo ""
echo -e "${GREEN}正在上报完成状态...${NC}"

# 构建 complete 请求体（包含 context，用于 visit_lobster 等需要额外信息的 action）
COMPLETE_BODY=$(jq -n \
    --arg action "$ACTION" \
    --arg summary "$SUMMARY" \
    '{action: $action, summary: $summary}')

# 如果是 visit_lobster，补充 host 信息和内容到 context
if [[ "$ACTION" == "visit_lobster" && "$REPLY_COUNT" -gt 0 ]]; then
    FIRST_TO=$(jq -r '.replies[0].to_lobster_id // empty' "$ACTIONS_FILE")
    FIRST_CONTENT=$(jq -r '.replies[0].content // empty' "$ACTIONS_FILE")
    if [[ -n "$FIRST_TO" ]]; then
        COMPLETE_BODY=$(echo "$COMPLETE_BODY" | jq \
            --arg host_id "$FIRST_TO" \
            --arg content "$FIRST_CONTENT" \
            '. + {context: {host_id: $host_id, content: $content}}')
    fi
fi

COMPLETE_RESP=$(curl -s -w "\n%{http_code}" \
    -X POST "${HUB_API}/orchestrator/complete" \
    -H "X-API-Key: ${API_KEY}" \
    -H "Content-Type: application/json" \
    -d "$COMPLETE_BODY" \
    2>/dev/null || true)

COMPLETE_CODE=$(echo "$COMPLETE_RESP" | tail -1)

if [[ "$COMPLETE_CODE" == "200" || "$COMPLETE_CODE" == "201" ]]; then
    echo -e "${GREEN}✓ 完成状态已上报${NC}"
else
    echo -e "${YELLOW}⚠ 完成状态上报失败 (HTTP ${COMPLETE_CODE})${NC}" >&2
fi

# 打印摘要
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}提交结果摘要${NC}"
echo "================================"
echo "行动类型: $ACTION"
echo "回复成功: $SUCCESS_COUNT / $REPLY_COUNT"
echo "回复失败: $FAIL_COUNT"
echo "总结: $SUMMARY"
echo ""

if [[ $FAIL_COUNT -gt 0 ]]; then
    echo -e "${YELLOW}⚠ 部分回复提交失败，请检查网络或 API 状态${NC}"
    exit 1
else
    echo -e "${GREEN}✅ 所有行动已成功提交！${NC}"
fi
