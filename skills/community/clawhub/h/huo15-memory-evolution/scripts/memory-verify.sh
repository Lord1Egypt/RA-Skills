#!/usr/bin/env bash
# memory-verify.sh - 验证记忆引用的有效性
# Claude Code 风格：引用具体文件/函数前必须验证存在性
# Trust 当前代码 > trust 记忆

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_fail() { echo -e "${RED}[FAIL]${NC} $*"; }

usage() {
    cat << EOF
memory-verify.sh - 验证记忆引用的有效性

用法:
  memory-verify.sh <类型> <引用> [工作目录]

类型:
  file      - 验证文件是否存在
  function  - 验证函数/变量是否在代码中存在
  command   - 验证命令是否可执行

示例:
  memory-verify.sh file "skills/huo15-memory-evolution/scripts/session-state.sh"
  memory-verify.sh function "session-state write_state"
  memory-verify.sh command "python3"

返回值:
  0 - 验证通过
  1 - 验证失败（引用已过时）
  2 - 用法错误
EOF
}

verify_file() {
    local file="$1"
    local workdir="${2:-$WORKSPACE_DIR}"

    # 支持绝对路径和相对路径
    if [[ "$file" = /* ]]; then
        # 绝对路径
        if [ -f "$file" ]; then
            log_ok "文件存在: $file"
            return 0
        else
            log_fail "文件不存在: $file"
            return 1
        fi
    else
        # 相对路径，从 workspace 开始查找
        local full_path="$workdir/$file"
        if [ -f "$full_path" ]; then
            log_ok "文件存在: $full_path"
            return 0
        else
            log_fail "文件不存在（可能已移动或删除）: $file"
            return 1
        fi
    fi
}

verify_function() {
    local func_ref="$1"  # 格式: "文件名 函数名" 或 "文件名.函数名"
    local workdir="${2:-$WORKSPACE_DIR}"

    local file func_name
    if [[ "$func_ref" =~ ^(.+)\ (.+)$ ]]; then
        file="${BASH_REMATCH[1]}"
        func_name="${BASH_REMATCH[2]}"
    elif [[ "$func_ref" =~ ^(.+)\.(.+)$ ]]; then
        file="${BASH_REMATCH[1]}"
        func_name="${BASH_REMATCH[2]}"
    else
        log_warn "函数引用格式不正确，请使用: 文件名 函数名 或 文件名.函数名"
        return 2
    fi

    # 先验证文件存在
    local full_path="$workdir/$file"
    if [ ! -f "$full_path" ]; then
        log_fail "文件不存在: $file（函数 $func_name 的引用已过时）"
        return 1
    fi

    # 在文件中搜索函数定义
    if grep -qE "(function\s+)?$func_name\s*[({=]" "$full_path" 2>/dev/null; then
        log_ok "函数存在: $func_name (in $file)"
        return 0
    elif grep -qE "^$func_name\s*=" "$full_path" 2>/dev/null; then
        log_ok "函数/变量存在: $func_name (in $file)"
        return 0
    else
        log_fail "函数/变量不存在: $func_name (in $file)"
        log_warn "此函数可能已被重命名或删除"
        return 1
    fi
}

verify_command() {
    local cmd="$1"

    if command -v "$cmd" >/dev/null 2>&1; then
        local path
        path=$(command -v "$cmd")
        log_ok "命令存在: $cmd -> $path"
        return 0
    else
        log_fail "命令不存在: $cmd"
        return 1
    fi
}

main() {
    local type="${1:-}"
    local ref="${2:-}"

    if [ -z "$type" ] || [ -z "$ref" ]; then
        usage
        return 2
    fi

    case "$type" in
        file)
            verify_file "$ref" "${3:-}"
            ;;
        function|func)
            verify_function "$ref" "${3:-}"
            ;;
        command|cmd)
            verify_command "$ref"
            ;;
        -h|--help|help)
            usage
            ;;
        *)
            log_fail "未知类型: $type"
            usage
            return 2
            ;;
    esac
}

main "$@"
