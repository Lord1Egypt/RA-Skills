#!/bin/bash
# 保险费率表生成工具
# 
# 使用方法：
#   ./generate-rate-table.sh "产品名称"
# 
# 示例：
#   ./generate-rate-table.sh "星海赢家朱雀版"

PRODUCT_NAME="${1:-费率表}"
SCRIPT_DIR="$(dirname "$0")"

cd "$SCRIPT_DIR/.."

node scripts/generate-rate-table.js "$PRODUCT_NAME" \
  --plans="计划一,计划二" \
  --payment-years="趸交,10年,20年" \
  --payment-methods="一次交清,月交,年交,半年交,季交,不定期交" \
  --receive-ages="自55周岁,自60周岁" \
  --age-range="0-70"
