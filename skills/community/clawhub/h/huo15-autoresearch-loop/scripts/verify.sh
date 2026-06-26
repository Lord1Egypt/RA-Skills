#!/bin/bash
# verify.sh - 验证命令执行器

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config.json"

verify() {
    local verify_cmd="$1"
    local timeout="${2:-300}"

    if [[ -z "$verify_cmd" ]]; then
        echo "❌ 未提供验证命令"
        return 1
    fi

    echo "🔍 执行验证: $verify_cmd"

    # 执行验证命令，带超时
    local result=0
    local output
    output=$(timeout "$timeout" bash -c "$verify_cmd" 2>&1) || result=$?

    echo "$output"

    if [[ $result -eq 0 ]]; then
        echo "✅ 验证通过"
        return 0
    elif [[ $result -eq 124 ]]; then
        echo "⏰ 验证超时 (${timeout}s)"
        return 2
    else
        echo "❌ 验证失败 (exit code: $result)"
        return 1
    fi
}

# 快速验证（不输出详情）
verify_quick() {
    local verify_cmd="$1"
    timeout 60 bash -c "$verify_cmd" > /dev/null 2>&1
    return $?
}

# 从配置读取默认验证命令
verify_default() {
    local default_cmd=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('verify_command', ''))" 2>/dev/null || echo "")
    if [[ -n "$default_cmd" ]]; then
        verify "$default_cmd"
    else
        echo "❌ config.json 中未设置 verify_command"
        return 1
    fi
}

case "$1" in
    run)
        verify "$2" "${3:-300}"
        ;;
    quick)
        verify_quick "$2"
        ;;
    default)
        verify_default
        ;;
    *)
        echo "Usage: verify.sh {run|quick|default} [command] [timeout]"
        exit 1
        ;;
esac
