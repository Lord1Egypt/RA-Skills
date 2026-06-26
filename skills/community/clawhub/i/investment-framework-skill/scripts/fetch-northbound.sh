#!/bin/bash
# 获取北向资金数据（带缓存）
# 使用 QVeris API - 消耗 1.248 积分/次

set -e

export QVERIS_API_KEY=sk-7E-kK4yDTr61yT8UNiJPAJlUDM3HjzWsBs01-24F5HU

# 配置
CACHE_DIR=~/.openclaw/workspace/data/northbound
LOG_FILE=~/.openclaw/workspace/logs/qveris-usage.log
TODAY=$(date +%Y-%m-%d)
CACHE_FILE=$CACHE_DIR/$TODAY.json

# 创建缓存目录
mkdir -p "$CACHE_DIR"

# 检查缓存
if [ -f "$CACHE_FILE" ]; then
  echo "✅ 使用缓存数据：$CACHE_FILE"
  cat "$CACHE_FILE"
  exit 0
fi

# 获取最新数据
echo "📡 获取北向资金数据（消耗 1.248 积分）..."

RESULT=$(node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs \
  call ths_ifind.hk_connect_stats.v1 \
  --params "{\"sdate\":\"$TODAY\",\"edate\":\"$TODAY\"}" \
  2>&1)

# 检查是否成功
if echo "$RESULT" | grep -q '"status_code": 200'; then
  echo "$RESULT" | jq '.result.data' > "$CACHE_FILE"
  echo "✅ 数据已保存到：$CACHE_FILE"
  
  # 记录日志
  echo "$(date +%Y-%m-%d) | ths_ifind.hk_connect_stats.v1 | 1.248 | 北向资金" >> "$LOG_FILE"
  
  # 输出摘要
  echo ""
  echo "📊 数据摘要:"
  cat "$CACHE_FILE" | jq '.[] | select(.类型 | contains("股通")) | {日期: .交易日期, 类型: .类型, 成交额: ."成交额 (亿元，RMB)"}'
else
  echo "❌ 获取失败:"
  echo "$RESULT"
  exit 1
fi
