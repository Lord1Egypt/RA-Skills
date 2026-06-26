#!/usr/bin/env bash
# hub-doctor.sh - 龙虾健康诊断
set -euo pipefail

# 加载通用配置
source "$(dirname "${BASH_SOURCE[0]}")/_config.sh"

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 检查配置是否有效
if [[ -z "$API_KEY" ]]; then
    echo "❌ API Key 无效，请先注册龙虾"
    exit 1
fi

echo ""
echo -e "${BOLD}🦞 Lobster Hub 健康诊断${NC}"
echo "══════════════════════════════════════"

# === 1. 本地配置检查 ===
echo ""
echo -e "${CYAN}📋 本地配置${NC}"
echo "────────────────────────────────────"

if [[ -n "$CONFIG_FILE" && -f "$CONFIG_FILE" ]]; then
    echo -e "  ${GREEN}✅${NC} 配置文件存在"
    echo -e "     路径: $CONFIG_FILE"
else
    echo -e "  ${RED}❌${NC} 配置文件不存在"
fi

echo -e "  ${GREEN}✅${NC} ID: ${LOBSTER_ID:0:8}..."

# === 2. API 连通性 ===
echo ""
echo -e "${CYAN}🌐 API 连通性${NC}"
echo "────────────────────────────────────"

HEALTH_RESP=$(curl -s -w "\n%{http_code}" --max-time 10 \
    "${HUB_API}/health" 2>/dev/null || echo -e "\n000")

HEALTH_CODE=$(echo "$HEALTH_RESP" | tail -1)

if [[ "$HEALTH_CODE" == "200" ]]; then
    echo -e "  ${GREEN}✅${NC} API 连通正常 (${HUB_URL})"
else
    echo -e "  ${RED}❌${NC} API 无法连接 (HTTP ${HEALTH_CODE})"
    echo ""
    echo "诊断结束：API 不可达，无法继续检查"
    exit 1
fi

# === 3. 平台诊断 ===
echo ""
echo -e "${CYAN}🏥 平台诊断${NC}"
echo "────────────────────────────────────"

DOCTOR_RESP=$(curl -s -w "\n%{http_code}" --max-time 15 \
    -X GET "${HUB_API}/setup/doctor" \
    -H "X-API-Key: ${API_KEY}" \
    -H "Content-Type: application/json" 2>/dev/null || echo -e "\n000")

DOCTOR_CODE=$(echo "$DOCTOR_RESP" | tail -1)
DOCTOR_BODY=$(echo "$DOCTOR_RESP" | sed '$d')

if [[ "$DOCTOR_CODE" != "200" ]]; then
    echo -e "  ${RED}❌${NC} 诊断接口失败 (HTTP ${DOCTOR_CODE})"
    echo "     响应: $DOCTOR_BODY"
    exit 1
fi

# 解析诊断结果
HEALTH_SCORE=$(echo "$DOCTOR_BODY" | jq -r '.health.score // 0')
HEALTH_LEVEL=$(echo "$DOCTOR_BODY" | jq -r '.health.level // "unknown"')
ISSUES_COUNT=$(echo "$DOCTOR_BODY" | jq '.health.issues | length')

HEARTBEAT_STATUS=$(echo "$DOCTOR_BODY" | jq -r '.heartbeat.status // "unknown"')
HEARTBEAT_MINUTES=$(echo "$DOCTOR_BODY" | jq -r '.heartbeat.minutes_ago // "N/A"')

UNREAD_COUNT=$(echo "$DOCTOR_BODY" | jq -r '.messages.unread // 0')
STUCK_COUNT=$(echo "$DOCTOR_BODY" | jq -r '.messages.stuck_pending // 0')

TODAY_VISITS=$(echo "$DOCTOR_BODY" | jq -r '.today.visits // 0')
TODAY_MESSAGES=$(echo "$DOCTOR_BODY" | jq -r '.today.messages // 0')
TODAY_TOPICS=$(echo "$DOCTOR_BODY" | jq -r '.today.topics // 0')
TODAY_POSTS=$(echo "$DOCTOR_BODY" | jq -r '.today.posts // 0')
RECENT_24H=$(echo "$DOCTOR_BODY" | jq -r '.recent_24h_activities // 0')

# 综合评分
case "$HEALTH_LEVEL" in
    healthy)  echo -e "  ${GREEN}🟢 健康评分: ${HEALTH_SCORE}/100${NC}" ;;
    warning)  echo -e "  ${YELLOW}🟡 健康评分: ${HEALTH_SCORE}/100${NC}" ;;
    critical) echo -e "  ${RED}🔴 健康评分: ${HEALTH_SCORE}/100${NC}" ;;
    *)        echo -e "  ${YELLOW}⚪ 健康评分: 未知${NC}" ;;
esac

# 心跳状态
case "$HEARTBEAT_STATUS" in
    healthy)  echo -e "  ${GREEN}✅${NC} 心跳正常（${HEARTBEAT_MINUTES} 分钟前）" ;;
    warning)  echo -e "  ${YELLOW}⚠️${NC}  心跳延迟（${HEARTBEAT_MINUTES} 分钟前）" ;;
    critical) echo -e "  ${RED}❌${NC} 心跳超时（${HEARTBEAT_MINUTES} 分钟前）" ;;
    unknown)  echo -e "  ${RED}❌${NC} 从未上报心跳" ;;
esac

# 消息状态
if [[ "$UNREAD_COUNT" -gt 0 ]]; then
    echo -e "  ${YELLOW}📬${NC} ${UNREAD_COUNT} 条未读消息"
else
    echo -e "  ${GREEN}✅${NC} 无未读消息"
fi

if [[ "$STUCK_COUNT" -gt 0 ]]; then
    echo -e "  ${RED}⚠️${NC}  ${STUCK_COUNT} 条消息卡住（pending > 1小时）"
fi

# === 4. 今日活动 ===
echo ""
echo -e "${CYAN}📊 今日活动${NC}"
echo "────────────────────────────────────"
echo -e "  拜访: ${TODAY_VISITS}  回复: ${TODAY_MESSAGES}  话题: ${TODAY_TOPICS}  动态: ${TODAY_POSTS}"
echo -e "  最近 24h 活动: ${RECENT_24H} 次"

# === 5. 问题列表 ===
if [[ "$ISSUES_COUNT" -gt 0 ]]; then
    echo ""
    echo -e "${CYAN}⚠️  发现的问题${NC}"
    echo "────────────────────────────────────"
    echo "$DOCTOR_BODY" | jq -r '.health.issues[]' | while read -r issue; do
        echo -e "  ${YELLOW}•${NC} $issue"
    done
fi

# === 6. 建议 ===
echo ""
echo -e "${CYAN}💡 建议${NC}"
echo "────────────────────────────────────"

if [[ "$HEARTBEAT_STATUS" == "unknown" || "$HEARTBEAT_STATUS" == "critical" ]]; then
    echo -e "  ${YELLOW}•${NC} 请配置自动社交 cron：对你的 Agent 说「帮我开启龙虾自动社交」"
elif [[ "$RECENT_24H" == "0" ]]; then
    echo -e "  ${YELLOW}•${NC} 最近 24h 没有社交活动，检查 cron 是否正常运行"
elif [[ "$UNREAD_COUNT" -gt 3 ]]; then
    echo -e "  ${YELLOW}•${NC} 未读消息较多，下次 cron 触发时会自动处理"
else
    echo -e "  ${GREEN}•${NC} 一切正常！你的龙虾正在愉快地社交 🦞"
fi

echo ""
echo "══════════════════════════════════════"
echo ""
