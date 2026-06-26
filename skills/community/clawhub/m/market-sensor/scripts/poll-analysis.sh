#!/bin/bash
# MarketSensor 分析状态轮询脚本
# 用法: ./poll-analysis.sh <SYMBOL> [max_retries]
#
# 触发分析并轮询直到完成，然后输出报告内容。

set -e

SYMBOL="${1:?用法: $0 <SYMBOL> [max_retries]}"
MAX_RETRIES="${2:-10}"
INTERVAL=30

if [ -z "$MARKETSENSOR_API_KEY" ]; then
  echo "错误: 未设置 MARKETSENSOR_API_KEY 环境变量" >&2
  exit 1
fi

BASE_URL="https://api.marketsensor.ai"
AUTH="Authorization: Bearer $MARKETSENSOR_API_KEY"

echo "==> 触发 $SYMBOL 分析..."
TRIGGER_RESP=$(curl -s -X POST -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d "{\"symbol\": \"$SYMBOL\"}" \
  "$BASE_URL/api/open/analyze")

STATUS=$(echo "$TRIGGER_RESP" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)
REPORT_ID=$(echo "$TRIGGER_RESP" | grep -o '"reportId":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ "$STATUS" = "completed" ] && [ -n "$REPORT_ID" ]; then
  echo "==> 已有报告，直接获取..."
else
  echo "==> 状态: $STATUS，开始轮询..."
  for i in $(seq 1 "$MAX_RETRIES"); do
    sleep "$INTERVAL"
    echo "==> 轮询 #$i / $MAX_RETRIES ..."
    STATUS_RESP=$(curl -s -H "$AUTH" "$BASE_URL/api/open/analysis/status/$SYMBOL")
    STATUS=$(echo "$STATUS_RESP" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)
    REPORT_ID=$(echo "$STATUS_RESP" | grep -o '"reportId":"[^"]*"' | head -1 | cut -d'"' -f4)

    if [ "$STATUS" = "completed" ] && [ -n "$REPORT_ID" ]; then
      echo "==> 分析完成！"
      break
    fi
    echo "    状态: $STATUS"
  done
fi

if [ "$STATUS" != "completed" ] || [ -z "$REPORT_ID" ]; then
  echo "错误: 轮询超时或分析失败 (status=$STATUS)" >&2
  exit 1
fi

echo ""
echo "========== $SYMBOL 分析报告 =========="
echo ""
curl -s -H "$AUTH" "$BASE_URL/api/open/report/$REPORT_ID"
