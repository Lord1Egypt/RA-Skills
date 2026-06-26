#!/bin/bash
# 获取行业资金流向数据（带缓存）
# 使用 QVeris API - 消耗 1.56 积分/次

set -e

export QVERIS_API_KEY=sk-7E-kK4yDTr61yT8UNiJPAJlUDM3HjzWsBs01-24F5HU

# 配置
CACHE_DIR=~/.openclaw/workspace/data/industry
LOG_FILE=~/.openclaw/workspace/logs/qveris-usage.log
WEEK=$(date +%Y-W%W)
CACHE_FILE=$CACHE_DIR/$WEEK.json

# 创建缓存目录
mkdir -p "$CACHE_DIR"

# 检查缓存
if [ -f "$CACHE_FILE" ]; then
  echo "✅ 使用缓存数据：$CACHE_FILE"
  cat "$CACHE_FILE"
  exit 0
fi

# 计算本周起止日期
START_DATE=$(date -d "monday this week" +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

# 获取数据
echo "📡 获取行业资金流向数据（消耗 1.56 积分）..."

# 注意：scope=sector 可能失败，用 scope=stock 获取个股后聚合
RESULT=$(node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs \
  call ths_ifind.money_flow.v1 \
  --params "{\"scope\":\"stock\",\"codes\":\"600519.SH,000858.SZ,000001.SZ,601318.SH,600036.SH\",\"startdate\":\"$START_DATE\",\"enddate\":\"$END_DATE\"}" \
  2>&1)

# 检查是否成功
if echo "$RESULT" | grep -q '"status_code": 200'; then
  echo "$RESULT" | jq '.result.data' > "$CACHE_FILE"
  echo "✅ 数据已保存到：$CACHE_FILE"
  
  # 记录日志
  echo "$(date +%Y-%m-%d) | ths_ifind.money_flow.v1 | 1.56 | 行业资金流向" >> "$LOG_FILE"
  
  # 输出摘要
  echo ""
  echo "📊 数据摘要:"
  cat "$CACHE_FILE" | jq '.[0][] | {日期：.date, 代码：.code, 主力净流入：.main_net_inflow, 净流入占比：.main_net_inflow_pct}'
else
  echo "❌ 获取失败:"
  echo "$RESULT"
  exit 1
fi
