#!/bin/bash
# OpenClaw 安全配置修改脚本
# 原子写入 + Git 快照 + 事前通知 + 事后验证

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
CONFIG_FILE="$OPENCLAW_HOME/openclaw.json"
LOG_DIR="$OPENCLAW_HOME/logs"
LOG_FILE="$LOG_DIR/config-modify.log"
STATE_FILE="$LOG_DIR/modify-state.json"

mkdir -p "$LOG_DIR"

# 加载核心函数
source "$SCRIPT_DIR/core.sh"
load_notify_config

# ==================== 日志 ====================
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }

# ==================== 记录操作状态 ====================
save_state() {
    local action="$1"
    local description="$2"
    cat > "$STATE_FILE" << EOF
{
    "action": "$action",
    "description": "$description",
    "timestamp": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
    "config_file": "$CONFIG_FILE",
    "backup_tag": "${3:-}"
}
EOF
}

clear_state() {
    rm -f "$STATE_FILE"
}

# ==================== 原子写入配置 ====================
atomic_write_config() {
    local content="$1"
    local tmp_file="${CONFIG_FILE}.tmp.$$"
    
    # 写入临时文件
    echo "$content" > "$tmp_file"
    
    # 验证 JSON 合法性
    if ! jq empty "$tmp_file" 2>/dev/null; then
        log_error "JSON 格式验证失败"
        rm -f "$tmp_file"
        return 1
    fi
    
    # 原子替换
    mv "$tmp_file" "$CONFIG_FILE"
    log_info "配置已原子写入"
    return 0
}

# ==================== 安全修改流程 ====================
safe_modify() {
    local action="$1"
    local description="$2"
    local modify_cmd="$3"
    
    log_info "========== 安全修改开始 =========="
    log_info "操作: $action"
    log_info "描述: $description"
    
    # Step 1: 先通知用户
    notify "INFO" "正在修改配置: $description"
    log_info "已发送事前通知"
    
    # Step 2: Git 快照
    log_info "创建 Git 快照..."
    local backup_tag
    backup_tag=$("$SCRIPT_DIR/git-tag.sh" save-working 2>&1 | grep "已保存标记" | awk '{print $NF}')
    log_info "Git 快照: $backup_tag"
    
    # Step 3: 记录操作状态（用于重启后恢复）
    save_state "$action" "$description" "$backup_tag"
    log_info "操作状态已记录"
    
    # Step 4: 执行修改
    log_info "执行修改命令..."
    if ! eval "$modify_cmd"; then
        log_error "修改命令执行失败"
        notify "ERROR" "配置修改失败: $description"
        clear_state
        return 1
    fi
    
    # Step 5: 验证配置
    log_info "验证配置..."
    if ! validate_config; then
        log_error "配置验证失败，执行回滚..."
        if [ -n "$backup_tag" ]; then
            "$SCRIPT_DIR/git-tag.sh" rollback "$backup_tag"
            notify "ERROR" "配置验证失败，已回滚到: $backup_tag"
        fi
        clear_state
        return 1
    fi
    
    # Step 6: 重启网关
    log_info "重启网关..."
    if command -v openclaw >/dev/null 2>&1; then
        openclaw gateway stop 2>/dev/null || true
        sleep 2
        openclaw gateway start 2>/dev/null || true
        sleep 5
    fi
    
    # Step 7: 验证网关
    if check_gateway_port; then
        log_info "网关重启成功"
        notify "INFO" "配置修改完成: ${description}，网关已恢复正常"
        clear_state
        log_info "========== 安全修改完成 =========="
        return 0
    else
        log_error "网关重启失败，执行回滚..."
        if [ -n "$backup_tag" ]; then
            "$SCRIPT_DIR/git-tag.sh" rollback "$backup_tag"
            notify "ERROR" "网关重启失败，已回滚到: $backup_tag"
        fi
        clear_state
        return 1
    fi
}

# ==================== 检查端口 ====================
check_gateway_port() {
    local port="${OPENCLAW_GATEWAY_PORT:-18789}"
    if command -v lsof >/dev/null 2>&1; then
        lsof -i :$port -sTCP:LISTEN >/dev/null 2>&1
    else
        sleep 3
        command -v openclaw >/dev/null 2>&1 && openclaw gateway status 2>/dev/null | grep -qi "running"
    fi
}

# ==================== 重启后恢复检查 ====================
post_restart_recovery() {
    if [ ! -f "$STATE_FILE" ]; then
        log_info "无待恢复的操作状态"
        return 0
    fi
    
    log_info "检测到上次操作状态，执行恢复检查..."
    
    local action description backup_tag
    action=$(jq -r '.action' "$STATE_FILE" 2>/dev/null)
    description=$(jq -r '.description' "$STATE_FILE" 2>/dev/null)
    backup_tag=$(jq -r '.backup_tag' "$STATE_FILE" 2>/dev/null)
    
    log_info "上次操作: $action - $description"
    
    # 验证当前配置
    if validate_config && check_gateway_port; then
        log_info "配置验证通过，网关运行正常"
        notify "INFO" "网关已恢复，上次操作成功: $description"
        clear_state
        return 0
    else
        log_warn "配置验证失败，执行自动回滚..."
        if [ -n "$backup_tag" ] && [ "$backup_tag" != "null" ]; then
            "$SCRIPT_DIR/git-tag.sh" rollback "$backup_tag"
            notify "WARNING" "网关恢复后配置异常，已自动回滚到: $backup_tag"
        else
            "$SCRIPT_DIR/git-tag.sh" quick-rollback
            notify "WARNING" "网关恢复后配置异常，已回滚到最近安全版本"
        fi
        clear_state
        return 1
    fi
}

# ==================== 使用说明 ====================
show_usage() {
    cat << EOF
OpenClaw 安全配置修改脚本

用法: $(basename "$0") <命令> [选项]

命令:
    modify <操作> <描述> <命令>   安全执行配置修改
    recovery                      重启后恢复检查
    state                         查看当前操作状态
    help                          显示帮助信息

示例:
    # 安全修改配置（自动处理通知、备份、验证、回滚）
    $(basename "$0") modify "添加模型" "添加 GPT-4 模型配置" \\
        'jq \".models.providers.test = {...}\" openclaw.json > tmp && mv tmp openclaw.json'

    # 重启后检查
    $(basename "$0") recovery

EOF
}

# ==================== 主函数 ====================
case "${1:-help}" in
    modify)
        if [ $# -lt 4 ]; then
            echo "❌ 参数不足"
            show_usage
            exit 1
        fi
        safe_modify "$2" "$3" "$4"
        ;;
    recovery)
        post_restart_recovery
        ;;
    state)
        if [ -f "$STATE_FILE" ]; then
            cat "$STATE_FILE"
        else
            echo "无待恢复的操作"
        fi
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo "未知命令: $1"
        show_usage
        exit 1
        ;;
esac
