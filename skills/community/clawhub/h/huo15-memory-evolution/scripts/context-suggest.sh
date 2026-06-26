#!/usr/bin/env bash
# context-suggest.sh - Context 建议生成器

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE_DIR/memory"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

NEAR_CAPACITY_PERCENT=80
MEMORY_HIGH_TOKENS=5000

get_usage() {
    local mem_size mem_files
    mem_size=$(du -s "$MEMORY_DIR" 2>/dev/null | cut -f1 || echo "0")
    mem_files=$(find "$MEMORY_DIR" -name "*.md" 2>/dev/null | wc -l | tr -d ' ' || echo "0")
    python3 - "$mem_size" "$mem_files" << 'PYEOF'
import json, sys
mem_size = int(sys.argv[1])
mem_files = int(sys.argv[2])
print(json.dumps({
    'memory_size_kb': mem_size,
    'memory_files': mem_files,
    'estimated_tokens': int(mem_size * 750 / 1024)
}))
PYEOF
}

check() {
    local override_percent="${1:-}"
    local override_tokens="${2:-}"

    local usage context_percent memory_tokens
    usage=$(get_usage)

    if [ -n "$override_percent" ]; then
        context_percent="$override_percent"
    else
        context_percent=$(echo "$usage" | python3 -c "import json,sys; d=json.load(sys.stdin); print(min(100, int(d.get('memory_size_kb',0)/50)))" 2>/dev/null || echo "0")
    fi

    if [ -n "$override_tokens" ]; then
        memory_tokens="$override_tokens"
    else
        memory_tokens=$(echo "$usage" | python3 -c "import json,sys; print(json.load(sys.stdin).get('estimated_tokens', 0))" 2>/dev/null || echo "0")
    fi

    local suggestions=()

    if [ "$context_percent" -ge "$NEAR_CAPACITY_PERCENT" ]; then
        suggestions+=("${RED}[警告]${NC} 上下文已达 ${context_percent}%，接近容量上限")
        suggestions+=("建议：使用 /compact 释放空间")
        suggestions+=("")
    fi

    if [ "$memory_tokens" -ge "$MEMORY_HIGH_TOKENS" ]; then
        suggestions+=("${YELLOW}[建议]${NC} 记忆占用过多（约 ${memory_tokens} tokens）")
        suggestions+=("建议：运行 dream.sh 提炼记忆")
        suggestions+=("")
    fi

    if [ ${#suggestions[@]} -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} 上下文状态良好"
        return 0
    fi

    echo ""
    echo "━━━ Context 建议 ━━━"
    echo ""
    for s in "${suggestions[@]}"; do echo -e "$s"; done
}

main() {
    case "${1:-}" in
        -h|--help|help|"") echo "context-suggest.sh: check [percent] [tokens]" ;;
        check|suggest) check "${2:-}" "${3:-}" ;;
        status) get_usage | python3 -m json.tool ;;
        *) echo "未知命令: $1" ;;
    esac
}

main "$@"
