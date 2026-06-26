#!/bin/bash
#===============================================================================
# Plan Mode 核心脚本
# 
# 功能：
#   1. 检测危险操作
#   2. 发送确认消息
#   3. 执行或取消操作
#   4. 记录操作日志
#
# 使用方式：
#   ./plan-mode.sh check "rm -rf /tmp/test"
#   ./plan-mode.sh confirm "rm -rf /tmp/test"
#   ./plan-mode.sh execute "rm -rf /tmp/test"
#   ./plan-mode.sh is-dangerous "rm -rf /tmp/test"
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/config"
LOG_DIR="$HOME/.openclaw/workspace/memory/activity"

# 默认配置
MODE="normal"  # strict, normal, off
AUTO_CONFIRM_LOW_RISK=true

#===============================================================================
# 加载配置
#===============================================================================
load_config() {
    if [ -f "$CONFIG_DIR/plan-mode.json" ]; then
        MODE=$(grep -o '"mode"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG_DIR/plan-mode.json" 2>/dev/null | cut -d'"' -f4)
        AUTO_CONFIRM_LOW_RISK=$(grep -o '"autoConfirmLowRisk"[[:space:]]*:[[:space:]]*[^,}]*' "$CONFIG_DIR/plan-mode.json" 2>/dev/null | grep -o 'true\|false')
    fi
}

#===============================================================================
# 日志记录
#===============================================================================
log_action() {
    local action="$1"
    local command="$2"
    local result="$3"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    mkdir -p "$LOG_DIR"
    echo "## $timestamp | $action | $command | $result" >> "$LOG_DIR/plan-mode-log.md"
}

#===============================================================================
# 检测危险操作
#===============================================================================
is_dangerous() {
    local cmd="$1"
    
    # 空命令
    [ -z "$cmd" ] && { echo "low"; return 0; }
    
    # 高危操作
    local high_risk_patterns=(
        "rm[[:space:]]*-rf"
        "rm[[:space:]]*-r"
        "trash"
        "unlink"
        "kill[[:space:]]"
        "pkill"
        "git[[:space:]]push[[:space:]]*--force"
        "git[[:space:]]push[[:space:]]*-f"
        "shutdown"
        "reboot"
        "init[[:space:]]*0"
        "init[[:space:]]*6"
        ">~/.zshrc"
        ">~/.bashrc"
        "chmod[[:space:]]*777"
        "chown[[:space:]]*root"
    )
    
    for pattern in "${high_risk_patterns[@]}"; do
        if echo "$cmd" | grep -iqE "$pattern"; then
            echo "high"
            return 0
        fi
    done
    
    # 中危操作
    local medium_risk_patterns=(
        "curl[[:space:]]"
        "wget[[:space:]]"
        "npm[[:space:]]install"
        "pip[[:space:]]install"
        "apt[[:space:]]install"
        "yum[[:space:]]install"
        "docker[[:space:]]rm"
        "docker[[:space:]]rmi"
        "git[[:space:]]push"
        "git[[:space:]]commit"
        "ssh[[:space:]]"
        "scp[[:space:]]"
    )
    
    for pattern in "${medium_risk_patterns[@]}"; do
        if echo "$cmd" | grep -iqE "$pattern"; then
            echo "medium"
            return 0
        fi
    done
    
    echo "low"
    return 0
}

#===============================================================================
# 获取风险描述
#===============================================================================
get_risk_description() {
    local cmd="$1"
    local risk="$2"
    
    case "$risk" in
        high)
            echo "高危操作，可能导致数据永久丢失"
            ;;
        medium)
            echo "中危操作，可能影响系统状态"
            ;;
        *)
            echo "低危操作，风险较小"
            ;;
    esac
}

#===============================================================================
# 检查操作
#===============================================================================
check_operation() {
    local cmd="$1"
    
    load_config
    
    # Plan Mode 关闭
    [ "$MODE" = "off" ] && echo "mode:off" && return 1
    
    # 检测风险级别
    risk=$(is_dangerous "$cmd")
    
    if [ "$risk" = "high" ]; then
        echo "risk:high|confirm:yes"
        return 0
    elif [ "$risk" = "medium" ]; then
        if [ "$MODE" = "strict" ]; then
            echo "risk:medium|confirm:yes"
            return 0
        else
            echo "risk:medium|confirm:no"
            return 1
        fi
    else
        if [ "$AUTO_CONFIRM_LOW_RISK" = "true" ]; then
            echo "risk:low|confirm:auto"
            return 0
        else
            echo "risk:low|confirm:no"
            return 1
        fi
    fi
}

#===============================================================================
# 生成确认消息
#===============================================================================
generate_confirm_message() {
    local cmd="$1"
    local risk="$2"
    
    cat << EOF
⚠️ 危险操作检测

操作: $cmd
风险: $risk

是否确认执行？

回复 "是" 执行
回复 "否" 取消
EOF
}

#===============================================================================
# 主程序
#===============================================================================
main() {
    local action="${1:-check}"
    local command="${2:-}"
    
    case "$action" in
        check)
            check_operation "$command"
            ;;
        is-dangerous)
            is_dangerous "$command"
            ;;
        confirm)
            risk=$(is_dangerous "$command")
            generate_confirm_message "$command" "$risk"
            ;;
        log)
            log_action "$@"
            ;;
        enable)
            cat > "$CONFIG_DIR/plan-mode.json" << 'EOF'
{
  "version": "1.0",
  "mode": "strict",
  "autoConfirmLowRisk": false,
  "notifyOnCancel": true
}
EOF
            echo "Plan Mode 已开启（strict 模式）"
            ;;
        disable)
            cat > "$CONFIG_DIR/plan-mode.json" << 'EOF'
{
  "version": "1.0",
  "mode": "off",
  "autoConfirmLowRisk": true,
  "notifyOnCancel": true
}
EOF
            echo "Plan Mode 已关闭"
            ;;
        status)
            load_config
            echo "当前模式: $MODE"
            ;;
        *)
            echo "用法:"
            echo "  $0 check <command>       # 检查操作"
            echo "  $0 is-dangerous <cmd>   # 是否危险"
            echo "  $0 confirm <cmd>        # 生成确认消息"
            echo "  $0 enable               # 开启严格模式"
            echo "  $0 disable              # 关闭"
            echo "  $0 status               # 查看状态"
            ;;
    esac
}

main "$@"
