#!/bin/bash
# Lite 反馈收集脚本
# 安全设计：不收集用户原始输入

OPTIMIZER_PATH="$HOME/.openclaw/workspace/skills/promptbuddy-optimizer"

# 从 Lite 结果中提取安全元数据
extract_metadata() {
    local result="$1"
    echo "$result" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    # 只提取结构化数据，不包含用户输入
    print(json.dumps({
        'intent': d.get('intent', 'unknown'),
        'variant': d.get('variant', 0),
        'role': d.get('role', ''),
        'industry': d.get('industry', ''),
        'domain': d.get('domain', '')
    }))
except:
    print('{}')
"
}

# 记录反馈
record_feedback() {
    local metadata="$1"
    local feedback="$2"  # helpful / needs_improve
    
    python3 "$OPTIMIZER_PATH/scripts/collect_feedback_safe.py" \
        --metadata "$metadata" \
        --feedback "$feedback" 2>/dev/null
}

# 主函数
main() {
    local action="$1"
    shift
    
    case "$action" in
        "extract")
            extract_metadata "$1"
            ;;
        "record")
            record_feedback "$1" "$2"
            ;;
        *)
            echo "用法: $0 {extract|record} [参数]"
            ;;
    esac
}

main "$@"