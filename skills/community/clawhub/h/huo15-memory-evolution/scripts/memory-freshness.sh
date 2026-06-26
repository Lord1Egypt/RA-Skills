#!/usr/bin/env bash
# memory-freshness.sh - 记忆新鲜度检查

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE_DIR/memory"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

age_days() {
    local filepath="$1"
    [ ! -f "$filepath" ] && echo "-1" && return
    local mtime
    mtime=$(stat -f %m "$filepath" 2>/dev/null || stat -c %Y "$filepath" 2>/dev/null)
    echo "$(( ($(date +%s) - mtime) / 86400 ))"
}

age_string() {
    local filepath="$1"
    local age
    age=$(age_days "$filepath")
    [ "$age" -eq 0 ] && echo "今天" && return
    [ "$age" -eq 1 ] && echo "昨天" && return
    [ "$age" -lt 0 ] && echo "未知" && return
    echo "${age} 天前"
}

scan() {
    echo "=== 记忆新鲜度检查 ==="
    echo ""
    local count=0 stale=0
    for type_dir in user feedback project reference; do
        [ ! -d "$MEMORY_DIR/$type_dir" ] && continue
        for f in "$MEMORY_DIR/$type_dir"/*.md; do
            [ -f "$f" ] || continue
            count=$((count + 1))
            local age
            age=$(age_days "$f")
            [ "$age" -gt 90 ] && stale=$((stale + 1))
        done
    done
    echo "总计: $count 个记忆, $stale 个过期（>90天）"
}

main() {
    case "${1:-}" in
        -h|--help|help|"") echo "memory-freshness.sh: check [file]|scan|age [file]" ;;
        check) [ -f "${2:-}" ] && echo "$(basename "$2"): $(age_string "$2")" ;;
        scan) scan ;;
        age) [ -f "${2:-}" ] && age_string "$2" ;;
        *) [ -f "${1:-}" ] && echo "$(basename "$1"): $(age_string "$1")" ;;
    esac
}

main "$@"
