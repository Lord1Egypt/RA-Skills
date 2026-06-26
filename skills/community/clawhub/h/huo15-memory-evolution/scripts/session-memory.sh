#!/usr/bin/env bash
# session-memory.sh - 当前会话笔记

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE_DIR/memory"
SESSION_DIR="$MEMORY_DIR/session"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[SESSION]${NC} $*"; }
log_ok() { echo -e "${GREEN}[OK]${NC} $*"; }

SESSION_FILE="$SESSION_DIR/session-$(date +%Y-%m-%d).md"

init() {
    mkdir -p "$SESSION_DIR"
    if [[ ! -f "$SESSION_FILE" ]]; then
        cat > "$SESSION_FILE" << 'EOF'
---
name: session-YYYY-MM-DD
description: 当前会话笔记
type: session
---

# Session Notes

## 会话摘要

## 关键决策

## 待处理事项

## 重要发现

EOF
        sed -i "s/YYYY-MM-DD/$(date +%Y-%m-%d)/g" "$SESSION_FILE"
        log_info "Session 已创建: $SESSION_FILE"
    fi
}

read_session() {
    init
    cat "$SESSION_FILE"
}

show_help() {
    cat << 'EOF'
session-memory.sh: 当前会话笔记
用法:
  init   初始化今日 session
  read   读取当前 session
  path   显示 session 路径
EOF
}

main() {
    case "${1:-}" in
        -h|--help|help|"") show_help ;;
        init) init ;;
        read|cat) read_session ;;
        path) init; echo "$SESSION_FILE" ;;
        *) echo "未知命令: $1" ;;
    esac
}

main "$@"
