#!/bin/bash
#===============================================================================
# Cost Tracker - 记录 API 调用统计
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/config"
DATA_DIR="$HOME/.openclaw/workspace/memory/activity"
STATS_FILE="$DATA_DIR/cost-stats.json"

#===============================================================================
# 初始化统计文件
#===============================================================================
init_stats() {
    mkdir -p "$DATA_DIR"
    
    if [ ! -f "$STATS_FILE" ]; then
        cat > "$STATS_FILE" << 'EOF'
{
  "version": "1.0",
  "created": "TIMESTAMP",
  "resetAt": "TIMESTAMP",
  "totalCalls": 0,
  "totalInputTokens": 0,
  "totalOutputTokens": 0,
  "totalCacheReadTokens": 0,
  "totalCacheWriteTokens": 0,
  "totalDuration": 0,
  "totalCostUSD": 0,
  "calls": []
}
EOF
        sed -i '' "s/TIMESTAMP/$(date -u +%Y-%m-%dT%H:%M:%SZ)/" "$STATS_FILE"
    fi
}

#===============================================================================
# 获取模型定价
#===============================================================================
get_model_pricing() {
    local model="$1"
    
    python3 - "$model" << 'PYEOF'
import json
import sys
model = sys.argv[1]
try:
    with open("/Users/jobzhao/.openclaw/workspace/skills/huo15-cost-tracker/config/pricing.json") as f:
        config = json.load(f)
    if "models" in config and model in config["models"]:
        inp = config["models"][model].get("inputTokens", 0.01)
        out = config["models"][model].get("outputTokens", 0.01)
        print(f"{inp} {out}")
    else:
        print("0.01 0.01")
except:
    print("0.01 0.01")
PYEOF
}

#===============================================================================
# 计算成本
#===============================================================================
calculate_cost() {
    local input_tokens=$1
    local output_tokens=$2
    local model=$3
    
    local pricing=$(get_model_pricing "$model")
    local input_price=$(echo "$pricing" | cut -d' ' -f1)
    local output_price=$(echo "$pricing" | cut -d' ' -f2)
    
    local input_cost=$(echo "scale=10; $input_tokens / 1000000 * $input_price" | bc)
    local output_cost=$(echo "scale=10; $output_tokens / 1000000 * $output_price" | bc)
    local total_cost=$(echo "scale=10; $input_cost + $output_cost" | bc)
    
    echo "$total_cost"
}

#===============================================================================
# 记录 API 调用
#===============================================================================
record_call() {
    local input_tokens=0
    local output_tokens=0
    local cache_read=0
    local cache_write=0
    local model="unknown"
    local duration=0
    
    while [ $# -gt 0 ]; do
        case "$1" in
            --input-tokens)
                input_tokens=$2
                shift 2
                ;;
            --output-tokens)
                output_tokens=$2
                shift 2
                ;;
            --cache-read-tokens)
                cache_read=$2
                shift 2
                ;;
            --cache-write-tokens)
                cache_write=$2
                shift 2
                ;;
            --model)
                model=$2
                shift 2
                ;;
            --duration)
                duration=$2
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
    
    init_stats
    
    local cost=$(calculate_cost $input_tokens $output_tokens "$model")
    
    python3 - "$STATS_FILE" "$input_tokens" "$output_tokens" "$cache_read" "$cache_write" "$model" "$duration" "$cost" << 'PYEOF'
import json
import sys
from datetime import datetime

stats_file = sys.argv[1]
input_tokens = int(sys.argv[2])
output_tokens = int(sys.argv[3])
cache_read = int(sys.argv[4])
cache_write = int(sys.argv[5])
model = sys.argv[6]
duration = int(sys.argv[7])
cost = float(sys.argv[8])

try:
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    
    stats['totalCalls'] += 1
    stats['totalInputTokens'] += input_tokens
    stats['totalOutputTokens'] += output_tokens
    stats['totalCacheReadTokens'] += cache_read
    stats['totalCacheWriteTokens'] += cache_write
    stats['totalDuration'] += duration
    stats['totalCostUSD'] += cost
    
    stats['calls'].append({
        'timestamp': datetime.now().isoformat(),
        'inputTokens': input_tokens,
        'outputTokens': output_tokens,
        'cacheReadTokens': cache_read,
        'cacheWriteTokens': cache_write,
        'model': model,
        'duration': duration,
        'costUSD': cost
    })
    
    if len(stats['calls']) > 1000:
        stats['calls'] = stats['calls'][-1000:]
    
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 记录成功: {input_tokens} in / {output_tokens} out, ${cost:.6f}")
    
except Exception as e:
    print(f"❌ 记录失败: {e}")
PYEOF
}

#===============================================================================
# 生成报表
#===============================================================================
generate_report() {
    init_stats
    
    python3 - "$STATS_FILE" << 'PYEOF'
import json
from datetime import datetime
from collections import Counter
import sys

stats_file = sys.argv[1]

try:
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    
    print("=" * 50)
    print("💰 成本追踪报表")
    print("=" * 50)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"统计开始: {stats.get('resetAt', stats.get('created', '未知'))}")
    print("-" * 50)
    print(f"总 API 调用: {stats['totalCalls']} 次")
    print(f"总 Input Tokens: {stats['totalInputTokens']:,}")
    print(f"总 Output Tokens: {stats['totalOutputTokens']:,}")
    print(f"总 Cache Read: {stats.get('totalCacheReadTokens', 0):,}")
    print(f"总 Cache Write: {stats.get('totalCacheWriteTokens', 0):,}")
    print("-" * 50)
    print(f"💵 预估总成本: ${stats['totalCostUSD']:.6f} USD")
    print("-" * 50)
    
    if stats['calls']:
        model_counts = Counter(call['model'] for call in stats['calls'][-100:])
        print("📊 模型使用分布 (近100次):")
        total = sum(model_counts.values())
        for model, count in model_counts.most_common(5):
            pct = count / total * 100 if total > 0 else 0
            print(f"  {model}: {count} 次 ({pct:.1f}%)")
    
    if stats['calls']:
        durations = [call['duration'] for call in stats['calls'] if call['duration'] > 0]
        if durations:
            avg_duration = sum(durations) / len(durations)
            max_duration = max(durations)
            print("-" * 50)
            print(f"⏱️  平均响应时间: {avg_duration:.0f}ms")
            print(f"⏱️  最长响应时间: {max_duration}ms")
    
    print("=" * 50)
    
    total_tokens = stats['totalInputTokens'] + stats['totalOutputTokens']
    if total_tokens > 0:
        input_ratio = stats['totalInputTokens'] / total_tokens * 100
        output_ratio = stats['totalOutputTokens'] / total_tokens * 100
        print(f"📈 Token 利用率: 输入 {input_ratio:.1f}% / 输出 {output_ratio:.1f}%")
    
except Exception as e:
    print(f"❌ 生成报表失败: {e}")
PYEOF
}

#===============================================================================
# 重置统计
#===============================================================================
reset_stats() {
    init_stats
    
    python3 - "$STATS_FILE" << 'PYEOF'
import json
from datetime import datetime
import sys

stats_file = sys.argv[1]

try:
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    
    backup_file = stats_file + f".backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    with open(backup_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    stats['totalCalls'] = 0
    stats['totalInputTokens'] = 0
    stats['totalOutputTokens'] = 0
    stats['totalCacheReadTokens'] = 0
    stats['totalCacheWriteTokens'] = 0
    stats['totalDuration'] = 0
    stats['totalCostUSD'] = 0
    stats['resetAt'] = datetime.now().isoformat()
    stats['calls'] = []
    
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 统计已重置")
    print(f"📁 旧数据备份: {backup_file}")
    
except Exception as e:
    print(f"❌ 重置失败: {e}")
PYEOF
}

#===============================================================================
# 主程序
#===============================================================================
main() {
    local action="${1:-}"
    
    case "$action" in
        record)
            shift
            record_call "$@"
            ;;
        report)
            generate_report
            ;;
        reset)
            reset_stats
            ;;
        help|--help|-h)
            echo "用法:"
            echo "  $0 record --input-tokens N --output-tokens N --model M --duration MS"
            echo "  $0 report"
            echo "  $0 reset"
            echo "  $0 set-threshold <USD>"
            echo "  $0 get-threshold"
            ;;
        set-threshold)
            local threshold="${2:-1.0}"
            python3 - "$threshold" "$CONFIG_DIR/threshold.json" << 'PYEOF'
import json
import sys
threshold = float(sys.argv[1])
config_file = sys.argv[2]
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    config['thresholdUSD'] = threshold
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"✅ 阈值已设置为 ${threshold:.2f} USD")
except Exception as e:
    print(f"❌ 设置失败: {e}")
PYEOF
            ;;
        get-threshold)
            python3 - "$CONFIG_DIR/threshold.json" << 'PYEOF'
import json
import sys
config_file = sys.argv[1]
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    print(f"💰 当前阈值: ${config.get('thresholdUSD', 1.0):.2f} USD")
    print(f"🔔 警告状态: {'开启' if config.get('alertEnabled', True) else '关闭'}")
except:
    print("💰 当前阈值: $1.00 USD (默认)")
PYEOF
            ;;
        check-threshold)
            # 检查是否超过阈值
            python3 - "$STATS_FILE" "$CONFIG_DIR/threshold.json" << 'PYEOF'
import json
import sys
from datetime import datetime

stats_file = sys.argv[1]
config_file = sys.argv[2]

try:
    with open(stats_file, 'r') as f:
        stats = json.load(f)
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    threshold = config.get('thresholdUSD', 1.0)
    if stats['totalCostUSD'] >= threshold:
        print(f"⚠️ 成本警告: ${stats['totalCostUSD']:.4f} USD (阈值 ${threshold:.2f})")
        # 可以在这里触发通知
    else:
        print(f"✅ 成本正常: ${stats['totalCostUSD']:.4f} USD (阈值 ${threshold:.2f})")
except Exception as e:
    print(f"❌ 检查失败: {e}")
PYEOF
            ;;
        *)
            if [ -z "$action" ]; then
                generate_report
            else
                echo "未知命令: $action"
                echo "用法: $0 record|report|reset|set-threshold|get-threshold"
                exit 1
            fi
            ;;
    esac
}

main "$@"
