#!/usr/bin/env bash
# HTTP状态码查询 - Get Result
# Usage: ./get_result.sh <orderNo> <credential> <question>

ORDER_NO="${1:?Usage: ./get_result.sh <orderNo> <credential> <question>}"
CREDENTIAL="${2:?Missing credential}"
QUESTION="${3:-Analyze the provided data}"
SERVICE_ID="${4:-http状态码查询}"
API_BASE="${XIAOMENG_API_BASE:-https://xiaomeng-api.qisir.com}"

echo "Getting result for order: $ORDER_NO"

RESULT=$(curl -s -X POST "$API_BASE/api/getResult" \
  -H "Content-Type: application/json" \
  -d "{\"reqData\": {\"orderNo\": \"$ORDER_NO\", \"credential\": \"$CREDENTIAL\", \"question\": \"$QUESTION\", \"serviceId\": \"$SERVICE_ID\"}}")

echo "$RESULT" | python3 -m json.tool 2>/dev/null || echo "$RESULT"
