#!/bin/bash
# 消费统计脚本 - 简化版

LOG_DIR="$HOME/.openclaw/cost_logs"
mkdir -p "$LOG_DIR"

# 获取当前日期
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/cost_${TODAY}.txt"
JSON_FILE="$LOG_DIR/cost_${TODAY}.json"

# 初始化日志文件
init_log() {
    if [ ! -f "$JSON_FILE" ]; then
        cat > "$JSON_FILE" << EOF
{
  "date": "$TODAY",
  "total_cost": 0.0,
  "total_tokens": 0,
  "sessions": []
}
EOF
    fi
}

# 记录一次使用
log_usage() {
    local model="$1"
    local task="$2"
    local input_tokens="$3"
    local output_tokens="$4"
    local notes="$5"
    
    # 成本计算（简化版）
    local input_cost=0
    local output_cost=0
    
    if [ "$model" = "moonshot/kimi-k2.5" ]; then
        # Kimi: 输入0.3分/千token, 输出1.2分/千token
        input_cost=$(echo "scale=6; $input_tokens * 0.003 / 1000" | bc)
        output_cost=$(echo "scale=6; $output_tokens * 0.012 / 1000" | bc)
    fi
    # DeepSeek 免费
    
    local total_cost=$(echo "scale=6; $input_cost + $output_cost" | bc)
    local total_tokens=$((input_tokens + output_tokens))
    
    # 添加到日志
    local timestamp=$(date -Iseconds)
    local session_json=$(cat << EOF
    {
      "timestamp": "$timestamp",
      "model": "$model",
      "task": "$task",
      "input_tokens": $input_tokens,
      "output_tokens": $output_tokens,
      "total_cost": $total_cost,
      "total_tokens": $total_tokens,
      "notes": "$notes"
    }
EOF
)
    
    # 使用 jq 更新 JSON 文件
    if command -v jq &> /dev/null; then
        jq --argjson session "$session_json" \
           '.sessions += [$session] | 
            .total_cost += $session.total_cost | 
            .total_tokens += $session.total_tokens' \
           "$JSON_FILE" > "${JSON_FILE}.tmp" && mv "${JSON_FILE}.tmp" "$JSON_FILE"
    else
        # 简化版：追加到文本日志
        echo "[$timestamp] $model - $task: ${input_tokens}+${output_tokens} tokens, cost: ¥$total_cost" >> "$LOG_FILE"
    fi
    
    echo "记录成功: $task - 成本: ¥$total_cost"
}

# 显示今日统计
show_today() {
    echo "="*60
    echo "今日消费统计 ($TODAY)"
    echo "="*60
    
    if [ -f "$JSON_FILE" ] && command -v jq &> /dev/null; then
        local total_cost=$(jq '.total_cost' "$JSON_FILE")
        local total_tokens=$(jq '.total_tokens' "$JSON_FILE")
        local session_count=$(jq '.sessions | length' "$JSON_FILE")
        
        echo "总成本: ¥$total_cost"
        echo "总Token数: $total_tokens"
        echo "会话次数: $session_count"
        
        if [ $session_count -gt 0 ]; then
            echo ""
            echo "最近会话:"
            jq -r '.sessions[-3:] | .[] | "  [\(.timestamp[11:19])] \(.model) - \(.task): \(.total_tokens) tokens (¥\(.total_cost))"' "$JSON_FILE"
        fi
    elif [ -f "$LOG_FILE" ]; then
        echo "文本日志:"
        tail -10 "$LOG_FILE"
    else
        echo "暂无记录"
    fi
    
    echo "="*60
}

# 主函数
main() {
    case "$1" in
        "log")
            if [ $# -lt 5 ]; then
                echo "用法: $0 log <模型> <任务> <输入token> <输出token> [备注]"
                echo "示例: $0 log deepseek/deepseek-chat 代码开发 500 300 \"开发脚本\""
                exit 1
            fi
            init_log
            log_usage "$2" "$3" "$4" "$5" "${6:-}"
            ;;
        "show")
            show_today
            ;;
        "report")
            show_today
            echo ""
            echo "💡 成本建议:"
            if [ -f "$JSON_FILE" ] && command -v jq &> /dev/null; then
                local total_cost=$(jq '.total_cost' "$JSON_FILE")
                if (( $(echo "$total_cost == 0" | bc -l) )); then
                    echo "  ✅ 今日无成本消耗"
                elif (( $(echo "$total_cost < 0.1" | bc -l) )); then
                    echo "  ✅ 成本控制良好 (< ¥0.1)"
                elif (( $(echo "$total_cost < 1.0" | bc -l) )); then
                    echo "  ⚠️  成本适中 (< ¥1.0)"
                else
                    echo "  🔴 成本较高 (> ¥1.0)"
                fi
            fi
            ;;
        *)
            echo "AI 消费统计系统"
            echo "用法:"
            echo "  $0 log <模型> <任务> <输入> <输出> [备注] - 记录使用"
            echo "  $0 show - 显示今日统计"
            echo "  $0 report - 生成详细报告"
            echo ""
            echo "模型选项:"
            echo "  deepseek/deepseek-chat - 免费"
            echo "  moonshot/kimi-k2.5 - 较贵"
            ;;
    esac
}

main "$@"