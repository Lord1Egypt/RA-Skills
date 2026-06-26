#!/bin/bash
# 获取宏观经济数据（带缓存）
# 使用 QVeris API - 消耗 1 积分/次

set -e

export QVERIS_API_KEY=sk-7E-kK4yDTr61yT8UNiJPAJlUDM3HjzWsBs01-24F5HU

# 配置
CACHE_DIR=~/.openclaw/workspace/data/macro
LOG_FILE=~/.openclaw/workspace/logs/qveris-usage.log
CACHE_FILE=$CACHE_DIR/latest.json
CACHE_AGE_DAYS=7  # 缓存 7 天

# 创建缓存目录
mkdir -p "$CACHE_DIR"

# 检查缓存是否过期
if [ -f "$CACHE_FILE" ]; then
  CACHE_TIME=$(stat -c %Y "$CACHE_FILE")
  CURRENT_TIME=$(date +%s)
  AGE_SECONDS=$((CURRENT_TIME - CACHE_TIME))
  AGE_DAYS=$((AGE_SECONDS / 86400))
  
  if [ $AGE_DAYS -lt $CACHE_AGE_DAYS ]; then
    echo "✅ 使用缓存数据（更新于 $(date -d @$CACHE_TIME +%Y-%m-%d)，${AGE_DAYS}天前）"
    cat "$CACHE_FILE"
    exit 0
  else
    echo "⚠️  缓存已过期（${AGE_DAYS}天 > ${CACHE_AGE_DAYS}天），重新获取..."
  fi
fi

# 获取最新数据
echo "📡 获取宏观经济数据（消耗 1 积分）..."

# GDP 数据
echo "  - 获取 GDP 数据..."
GDP_RESULT=$(node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs \
  call ths_ifind.macro_china.v1 \
  --params '{"indicator":"gdp","sdate":"2025-01-01","edate":"2026-12-31"}' \
  2>&1)

# CPI 数据
echo "  - 获取 CPI 数据..."
CPI_RESULT=$(node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs \
  call ths_ifind.macro_china.v1 \
  --params '{"indicator":"cpi","sdate":"2026-01-01","edate":"2026-03-23"}' \
  2>&1)

# PMI 数据（如果可用）
echo "  - 获取 PMI 数据..."
PMI_RESULT=$(node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs \
  call ths_ifind.macro_china.v1 \
  --params '{"indicator":"pmi","sdate":"2026-01-01","edate":"2026-03-23"}' \
  2>&1 || echo '{"status_code": 500, "data": null}')

# 整合数据
jq -n \
  --argjson gdp "$(echo "$GDP_RESULT" | jq '.result.data // null')" \
  --argjson cpi "$(echo "$CPI_RESULT" | jq '.result.data // null')" \
  --argjson pmi "$(echo "$PMI_RESULT" | jq '.result.data // null')" \
  --arg updated "$(date +%Y-%m-%d)" \
  '{
    gdp: $gdp,
    cpi: $cpi,
    pmi: $pmi,
    metadata: {
      updated: $updated,
      source: "QVeris - ths_ifind.macro_china.v1"
    }
  }' > "$CACHE_FILE"

echo "✅ 数据已保存到：$CACHE_FILE"

# 记录日志
echo "$(date +%Y-%m-%d) | ths_ifind.macro_china.v1 | 1.0 | 宏观经济" >> "$LOG_FILE"

# 输出摘要
echo ""
echo "📊 数据摘要:"
echo "  GDP (2025Q4): $(cat "$CACHE_FILE" | jq -r '.gdp[0]["GDP:现价：累计值"] // "N/A"') 亿元"
echo "  CPI (2026-02): $(cat "$CACHE_FILE" | jq -r '.cpi[0]["CPI:当月同比"] // "N/A"')%"
echo "  更新时间：$(cat "$CACHE_FILE" | jq -r '.metadata.updated')"
