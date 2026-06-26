#!/usr/bin/env bash
# team-memory-sync.sh - Team Memory 实时同步

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE_DIR/memory"
TEAM_DIR="$MEMORY_DIR/../team-memory"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[TEAM-SYNC]${NC} $*"; }
log_ok() { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

init_team_dir() {
    mkdir -p "$TEAM_DIR"
    if [ ! -f "$TEAM_DIR/MEMORY.md" ]; then
        cat > "$TEAM_DIR/MEMORY.md" << 'EOF'
# Team Memory Index

## user/ — 用户偏好

## feedback/ — 团队反馈

## project/ — 项目进展

## reference/ — 外部引用

---
EOF
    fi
    log_ok "团队目录已初始化: $TEAM_DIR"
}

scan_secrets() {
    local filepath="$1"
    for pattern in "api[_-]?key" "secret" "password" "token" "credential" "sk-[a-zA-Z0-9]"; do
        if grep -iE "$pattern" "$filepath" 2>/dev/null | grep -v "^#" > /dev/null; then
            log_warn "检测到敏感信息: $filepath"
            return 1
        fi
    done
    return 0
}

share_memory() {
    local filepath="$1"
    local type="${2:-}"

    [ ! -f "$filepath" ] && echo "文件不存在" && return 1

    if ! scan_secrets "$filepath"; then
        echo "包含敏感信息，不能共享"
        return 1
    fi

    [ -z "$type" ] && type=$(basename "$(dirname "$filepath")")

    mkdir -p "$TEAM_DIR/$type"
    local filename=$(basename "$filepath")

    [ -L "$TEAM_DIR/$type/$filename" ] && rm "$TEAM_DIR/$type/$filename"
    ln -s "$filepath" "$TEAM_DIR/$type/$filename"

    log_ok "已共享: $type/$filename"
}

unshare_memory() {
    local filename="$1"
    local type="${2:-}"

    if [ -z "$type" ]; then
        for td in "$TEAM_DIR"/*/; do
            [ -d "$td" ] || continue
            [ -L "$td/$filename" ] && rm "$td/$filename" && log_ok "已取消共享: $(basename "$td")/$filename"
        done
    else
        [ -L "$TEAM_DIR/$type/$filename" ] && rm "$TEAM_DIR/$type/$filename" && log_ok "已取消共享: $type/$filename"
    fi
}

show_shared() {
    echo "━━━ 团队共享记忆 ━━━"
    [ ! -d "$TEAM_DIR" ] && echo "团队目录不存在" && return

    local total=0
    for td in "$TEAM_DIR"/*/; do
        [ -d "$td" ] || continue
        local type=$(basename "$td")
        local count=$(find "$td" -type l 2>/dev/null | wc -l | tr -d ' ')
        [ "$count" -gt 0 ] && echo -e "${GREEN}[$type]${NC} $count 个" && total=$((total + count))
    done
    echo "总计: $total 个共享记忆"
}

main() {
    case "${1:-}" in
        -h|--help|help|"") echo "team-memory-sync.sh: init|share|unshare|list" ;;
        init) init_team_dir ;;
        share) share_memory "${2:-}" "${3:-}" ;;
        unshare) unshare_memory "${2:-}" "${3:-}" ;;
        list|ls) show_shared ;;
        *) echo "未知命令: $1" ;;
    esac
}

main "$@"
