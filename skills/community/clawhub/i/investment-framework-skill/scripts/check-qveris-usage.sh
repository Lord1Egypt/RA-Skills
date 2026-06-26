#!/bin/bash
# 检查 QVeris 使用情况和缓存状态

echo "=== 🔍 QVeris 使用情况检查 ==="
echo ""

# 检查宏观数据缓存
MACRO_CACHE=~/.openclaw/workspace/data/investment/macro-latest.json
if [ -f "$MACRO_CACHE" ]; then
  MACRO_DATE=$(jq -r '.metadata.updated' "$MACRO_CACHE" 2>/dev/null || stat -c %y "$MACRO_CACHE" | cut -d' ' -f1)
  echo "✅ 宏观数据缓存：$MACRO_DATE"
else
  echo "⚠️  宏观数据缓存：不存在（市场扫描时自动获取）"
fi

# 检查北向资金缓存
TODAY=$(date +%Y-%m-%d)
NORTHBOUND_CACHE=~/.openclaw/workspace/data/investment/northbound-${TODAY}.json
if [ -f "$NORTHBOUND_CACHE" ]; then
  echo "✅ 北向资金缓存：今日数据已获取"
else
  echo "⚠️  北向资金缓存：今日数据未获取（09:00 自动获取）"
fi

# 检查行业资金流向缓存
WEEK=$(date +%Y-W%W)
INDUSTRY_CACHE=~/.openclaw/workspace/data/investment/industry-flow-${WEEK}.json
if [ -f "$INDUSTRY_CACHE" ]; then
  echo "✅ 行业资金流向缓存：本周数据已获取"
else
  echo "⚠️  行业资金流向缓存：本周数据未获取（周一 10:00 自动获取）"
fi

# 检查实际数据文件（市场扫描生成）
MARKET_DATA=~/.openclaw/workspace/data/investment/market-data.json
if [ -f "$MARKET_DATA" ]; then
  MARKET_TIME=$(stat -c %y "$MARKET_DATA" | cut -d' ' -f1-2 | sed 's/ / /')
  echo "✅ 市场数据文件：$MARKET_TIME"
else
  echo "⚠️  市场数据文件：不存在（09:00 自动生成）"
fi

# 检查 QVeris API Key
if [ -n "$QVERIS_API_KEY" ]; then
  echo "✅ QVeris API Key: 已配置"
else
  echo "❌ QVeris API Key: 未配置"
fi

# 显示本月积分消耗
LOG_FILE=~/.openclaw/workspace/logs/qveris-usage.log
if [ -f "$LOG_FILE" ]; then
  echo ""
  echo "=== 📊 本月积分消耗 ==="
  MONTH=$(date +%Y-%m)
  TOTAL=$(grep "^$MONTH" "$LOG_FILE" | awk -F'|' '{sum += $3} END {print sum}')
  
  if [ -n "$TOTAL" ]; then
    echo "本月已消耗：${TOTAL:-0} 积分"
    echo "月度目标：< 50 积分"
    
    if (( $(echo "$TOTAL > 50" | bc -l 2>/dev/null || echo 0) )); then
      echo "⚠️  警告：已超预算！"
    else
      echo "✅ 状态：正常"
    fi
    
    echo ""
    echo "详细记录:"
    grep "^$MONTH" "$LOG_FILE" | tail -10
  else
    echo "本月暂无消耗记录"
  fi
else
  echo ""
  echo "📝 使用日志：不存在（首次使用后创建）"
fi

echo ""
echo "=== 💡 建议 ==="
if [ ! -f "$NORTHBOUND_CACHE" ]; then
  echo "- 获取今日北向资金数据（消耗 1.248 积分）"
  echo "  命令：~/.openclaw/workspace/scripts/fetch-northbound.sh"
fi
if [ ! -f "$MACRO_CACHE" ] || [ $(find "$MACRO_CACHE" -mtime +7 2>/dev/null) ]; then
  echo "- 更新宏观数据缓存（消耗 1 积分）"
  echo "  命令：~/.openclaw/workspace/scripts/fetch-macro.sh"
fi
