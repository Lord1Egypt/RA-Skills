#!/usr/bin/env bash
# memory-recall.sh - 记忆检索 v3.6
# 基于 Claude Code findRelevantMemories.ts 实现

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE_DIR/memory"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[RECALL]${NC} $*" >&2; }
log_ok() { echo -e "${GREEN}[OK]${NC} $*" >&2; }

#----------------------------------------------------------
# 主函数
#----------------------------------------------------------
main() {
    case "${1:-}" in
        -h|--help|help|"") 
            echo "memory-recall.sh v3.6 - 记忆检索"
            echo ""
            echo "用法:"
            echo "  memory-recall.sh recall <查询>  召回相关记忆"
            echo "  memory-recall.sh list          列出所有记忆"
            ;;
        recall|query|find)
            recall "${2:-}"
            ;;
        list|ls)
            list_all
            ;;
        scan)
            scan_memories
            ;;
        *)
            echo "未知命令: $1"
            ;;
    esac
}

#----------------------------------------------------------
# 扫描记忆
#----------------------------------------------------------
scan_memories() {
    python3 "$SCRIPT_DIR/memory-recall-helper.py" scan "$MEMORY_DIR"
}

#----------------------------------------------------------
# 列出所有
#----------------------------------------------------------
list_all() {
    python3 "$SCRIPT_DIR/memory-recall-helper.py" list "$MEMORY_DIR"
}

#----------------------------------------------------------
# 召回
#----------------------------------------------------------
recall() {
    local query="${1:-}"
    
    if [ -z "$query" ]; then
        echo "用法: memory-recall.sh recall <查询>"
        return 1
    fi

    log_info "查询: $query"
    
    local count
    count=$(python3 "$SCRIPT_DIR/memory-recall-helper.py" count "$MEMORY_DIR")
    log_info "找到 $count 个记忆文件"
    
    if [ "$count" -eq 0 ]; then
        echo "没有找到记忆文件"
        return
    fi
    
    # 关键词匹配
    log_info "使用关键词匹配"
    python3 "$SCRIPT_DIR/memory-recall-helper.py" recall "$MEMORY_DIR" "$query"
}

main "$@"
