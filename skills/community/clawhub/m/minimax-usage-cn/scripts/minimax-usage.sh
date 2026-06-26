#!/bin/bash
# Minimax Coding Plan Usage Check (国内版)
# Usage: ./minimax-usage.sh [--json]
# Requires: MINIMAX_API_KEY in environment

API_KEY="${MINIMAX_API_KEY}"
JSON_MODE=false
if [ "$1" = "--json" ] || [ "$1" = "-j" ]; then
  JSON_MODE=true
fi

if [ -z "$API_KEY" ]; then
  echo "❌ Error: MINIMAX_API_KEY required in environment"
  exit 1
fi

echo "🔍 Checking Minimax Coding Plan usage..." >&2

RESPONSE=$(curl -s --location "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains" \
  --header "Authorization: Bearer $API_KEY" \
  --header "Content-Type: application/json")

# 检查是否返回了有效数据
if ! echo "$RESPONSE" | grep -q '"status_code":0'; then
  ERROR_MSG=$(echo "$RESPONSE" | grep -o '"status_msg":"[^"]*"' | cut -d'"' -f4)
  echo "❌ API Error: $ERROR_MSG" >&2
  exit 1
fi

# 检查是否有 model_remains
if ! echo "$RESPONSE" | grep -q '"model_remains"'; then
  echo "❌ API Error: model_remains not found in response" >&2
  echo "$RESPONSE" >&2
  exit 1
fi

# 解析 model_remains 数组中的每个条目
# 格式: {"start_time":xxx,"end_time":xxx,...,"model_name":"xxx",...}
# 提取每个 model_name 和关键数值

parse_model_entry() {
  local entry="$1"
  local model_name=$(echo "$entry" | grep -o '"model_name":"[^"]*"' | cut -d'"' -f4)
  local total=$(echo "$entry" | grep -o '"current_interval_total_count":[0-9]*' | head -1 | cut -d: -f2)
  local remains=$(echo "$entry" | grep -o '"current_interval_usage_count":[0-9]*' | head -1 | cut -d: -f2)
  local weekly_total=$(echo "$entry" | grep -o '"current_weekly_total_count":[0-9]*' | head -1 | cut -d: -f2)
  local weekly_remains=$(echo "$entry" | grep -o '"current_weekly_usage_count":[0-9]*' | head -1 | cut -d: -f2)
  local start_ts=$(echo "$entry" | grep -o '"start_time":[0-9]*' | head -1 | cut -d: -f2)
  local end_ts=$(echo "$entry" | grep -o '"end_time":[0-9]*' | head -1 | cut -d: -f2)

  echo "${model_name}|${total}|${remains}|${weekly_total}|${weekly_remains}|${start_ts}|${end_ts}"
}

# 提取每个模型条目（用 } 分割）
entries=$(echo "$RESPONSE" | tr '}' '\n' | grep '"model_name"' | while read line; do
  # 补上末尾可能的引号和逗号
  echo "$line}" | sed 's/,$//'
done)

# 模型名称别名映射
get_display_name() {
  case "$1" in
    "MiniMax-M*") echo "MiniMax-M2.7 (对话)" ;;
    "speech-hd") echo "Speech-2.8-HD (语音)" ;;
    "image-01") echo "Image-01 (生图)" ;;
    "MiniMax-Hailuo-2.3-Fast-6s-768p") echo "Hailuo-2.3-Fast (视频)" ;;
    "MiniMax-Hailuo-2.3-6s-768p") echo "Hailuo-2.3 (视频)" ;;
    "music-2.5") echo "Music-2.5 (音乐)" ;;
    *) echo "$1" ;;
  esac
}

# 计算百分比
calc_percent() {
  local used=$1
  local total=$2
  if [ "$total" = "0" ] || [ -z "$total" ]; then
    echo "0"
  else
    echo $((used * 100 / total))
  fi
}

# 计算窗口剩余时间
get_window_reset() {
  local end_ts="$1"
  local NOW_TS=$(date +%s000)
  if [ -n "$end_ts" ] && [ "$end_ts" -gt "$NOW_TS" ]; then
    local REMAIN_MS=$((end_ts - NOW_TS))
    local WIN_HOURS=$((REMAIN_MS / 3600000))
    local WIN_MINS=$(((REMAIN_MS % 3600000) / 60000))
    echo "约 ${WIN_HOURS}h ${WIN_MINS}m"
  else
    echo "< 1h"
  fi
}

# 收集所有模型数据用于 JSON
all_models_json="["
first=true

if $JSON_MODE; then
  while IFS='|' read -r model_name total remains weekly_total weekly_remains start_ts end_ts; do
    [ -z "$model_name" ] && continue
    used=$((total - remains))
    percent=$(calc_percent $used $total)
    weekly_used=$((weekly_total - weekly_remains))
    weekly_percent=$(calc_percent $weekly_used $weekly_total)
    window_reset=$(get_window_reset $end_ts)

    if [ "$first" = true ]; then
      first=false
    else
      all_models_json+=","
    fi
    all_models_json+="{\"model\":\"$model_name\",\"used\":$used,\"total\":$total,\"remaining\":$remains,\"percent\":$percent,\"weekly_used\":$weekly_used,\"weekly_total\":$weekly_total,\"weekly_remaining\":$weekly_remains,\"weekly_percent\":$weekly_percent,\"window_reset\":\"$window_reset\"}"
  done <<< "$(echo "$entries" | while IFS= read -r entry; do parse_model_entry "$entry"; done 2>/dev/null)"

  all_models_json+="]"
  echo "$all_models_json"
  exit 0
fi

# 人类可读输出
echo ""
echo "✅ Usage retrieved successfully:"
echo ""

while IFS='|' read -r model_name total remains weekly_total weekly_remains start_ts end_ts; do
  [ -z "$model_name" ] && continue
  [ "$total" = "0" ] && [ "$weekly_total" = "0" ] && continue

  display_name=$(get_display_name "$model_name")
  used=$((total - remains))
  percent=$(calc_percent $used $total)
  weekly_used=$((weekly_total - weekly_remains))
  weekly_percent=$(calc_percent $weekly_used $weekly_total)
  window_reset=$(get_window_reset "$end_ts")

  # 判断状态
  if [ "$percent" -gt 90 ]; then
    status="🚨 CRITICAL"
  elif [ "$percent" -gt 75 ]; then
    status="⚠️  WARNING"
  elif [ "$percent" -gt 60 ]; then
    status="⚠️  CAUTION"
  else
    status="💚 GREEN"
  fi

  echo "📊 ${display_name}:"
  echo "   5h窗口:  ${used} / ${total} (${percent}%) | 剩余: ${remains} | 重置: ${window_reset}"
  if [ "$weekly_total" != "0" ]; then
    echo "   周配额:   ${weekly_used} / ${weekly_total} (${weekly_percent}%) | 剩余: ${weekly_remains}"
  fi
  echo "   ${status}"
  echo ""

done <<< "$(echo "$entries" | while IFS= read -r entry; do parse_model_entry "$entry"; done 2>/dev/null)"
