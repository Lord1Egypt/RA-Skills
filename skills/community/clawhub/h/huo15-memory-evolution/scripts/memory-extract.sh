#!/usr/bin/env bash
# memory-extract.sh - 后台记忆提取

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE_DIR/memory"
EXTRACT_STATE="$MEMORY_DIR/.extract-state.json"

TURNS_BETWEEN_EXTRACT=3

read_state() {
    [ -f "$EXTRACT_STATE" ] && cat "$EXTRACT_STATE" || echo '{"turns_since_last": 999}'
}

write_state() {
    local turns=$1
    python3 - "$EXTRACT_STATE" "$turns" << 'PYEOF'
import json, sys
state_file = sys.argv[1]
turns = int(sys.argv[2])
with open(state_file, 'w') as f:
    json.dump({'turns_since_last': turns}, f)
PYEOF
}

can_extract() {
    local state turns
    state=$(read_state)
    turns=$(echo "$state" | python3 -c "import json,sys; print(json.load(sys.stdin).get('turns_since_last', 999))" 2>/dev/null || echo "999")
    [ "$turns" -lt "$TURNS_BETWEEN_EXTRACT" ] && echo "节流中" && return 1
    echo "可以提取"
    return 0
}

record_turn() {
    local state turns
    state=$(read_state)
    turns=$(echo "$state" | python3 -c "import json,sys; print(json.load(sys.stdin).get('turns_since_last', 0))" 2>/dev/null || echo "0")
    turns=$((turns + 1))
    write_state "$turns"
    echo "$turns"
}

show_status() {
    echo "=== 记忆提取状态 ==="
    [ -f "$EXTRACT_STATE" ] && cat "$EXTRACT_STATE" || echo "从未运行"
    echo "配置: 每 ${TURNS_BETWEEN_EXTRACT} 轮提取一次"
}

main() {
    case "${1:-}" in
        -h|--help|help|"") echo "memory-extract.sh: run|check|status|record" ;;
        run|extract) can_extract >/dev/null && write_state 0 && echo "提取已触发" ;;
        check|can) can_extract ;;
        status) show_status ;;
        record|turn) record_turn ;;
        *) echo "未知命令: $1" ;;
    esac
}

main "$@"
