#!/bin/bash
# ~/.openclaw/scripts/core.sh
# OpenClaw 核心诊断脚本
# 包含：日志记录、告警通知、配置验证、网关状态检查、僵尸状态检测

set -euo pipefail

# ==================== 配置 ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
LOG_DIR="${OPENCLAW_LOG_DIR:-$OPENCLAW_HOME/logs}"
LOG_FILE="$LOG_DIR/core.log"
CONFIG_FILE="$OPENCLAW_HOME/openclaw.json"
GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"

# 告警配置
NOTIFY_CONF="$OPENCLAW_HOME/notify.conf"
FEISHU_WEBHOOK_URL=""
TELEGRAM_BOT_TOKEN=""
TELEGRAM_CHAT_ID=""

# 创建日志目录
mkdir -p "$LOG_DIR"

# ==================== 加载配置 ====================
load_notify_config() {
    if [ -f "$NOTIFY_CONF" ]; then
        source "$NOTIFY_CONF"
    fi
    # 环境变量覆盖
    FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-${FEISHU_WEBHOOK:-}}"
    TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-${TELEGRAM_TOKEN:-}}"
    TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-${TELEGRAM_CHAT_ID:-}}"
}

# ==================== 日志函数 ====================
log() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" | tee -a "$LOG_FILE"
}

log_info() { log "INFO" "$1"; }
log_warn() { log "WARN" "$1"; }
log_error() { log "ERROR" "$1"; }

# ==================== 告警通知函数 ====================
notify() {
    local level="${1:-INFO}"
    local message="$2"
    
    log "$level" "发送告警: $message"
    
    # 发送飞书
    if [ -n "$FEISHU_WEBHOOK_URL" ]; then
        local feishu_msg="{\"msg_type\":\"text\",\"content\":{\"text\":\"[$level] OpenClaw 告警\n$(date '+%Y-%m-%d %H:%M:%S')\n$message\"}}"
        curl -s -X POST "$FEISHU_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "$feishu_msg" >> "$LOG_FILE" 2>&1 || true
    fi
    
    # 发送Telegram
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        local telegram_msg="[$level] OpenClaw 告警\n$(date '+%Y-%m-%d %H:%M:%S')\n$message"
        curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
            -d "chat_id=$TELEGRAM_CHAT_ID" \
            -d "text=$telegram_msg" \
            -d "parse_mode=Markdown" >> "$LOG_FILE" 2>&1 || true
    fi
    
    # 写入未发送告警日志
    if [ -z "$FEISHU_WEBHOOK_URL" ] && [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$LOG_DIR/unsent_alerts.log"
    fi
}

# ==================== 配置验证函数 ====================
validate_config() {
    local config_path="${1:-$CONFIG_FILE}"
    
    if [ ! -f "$config_path" ]; then
        log_error "配置文件不存在: $config_path"
        return 1
    fi
    
    # 使用 openclaw 命令验证
    if command -v openclaw >/dev/null 2>&1; then
        if openclaw gateway call config.get --json >/dev/null 2>&1; then
            log_info "配置验证通过 (openclaw 命令)"
            return 0
        fi
    fi
    
    # 备用: 使用 jq 验证 JSON 格式
    if command -v jq >/dev/null 2>&1; then
        if jq empty "$config_path" 2>/dev/null; then
            log_info "配置验证通过 (JSON 格式)"
            return 0
        fi
    fi
    
    log_error "配置验证失败: $config_path"
    return 1
}

# ==================== 网关状态检查 ====================
check_gateway_status() {
    local check_port="${1:-true}"
    local check_process="${2:-true}"
    local process_ok=0
    local port_ok=0
    local status_cmd_ok=0
    
    # 检查进程（辅助参考，可能因权限限制失败）
    if [ "$check_process" = "true" ]; then
        if pgrep -f "openclaw.*gateway" >/dev/null 2>&1; then
            log_info "网关进程运行中 (pgrep)"
            process_ok=1
        else
            log_warn "网关进程未通过 pgrep 检测（可能受权限限制，不影响实际判断）"
        fi
    fi
    
    # 检查端口
    if [ "$check_port" = "true" ]; then
        local port_listening=0
        if command -v lsof >/dev/null 2>&1; then
            if lsof -i :$GATEWAY_PORT -sTCP:LISTEN >/dev/null 2>&1; then
                port_listening=1
            fi
        elif command -v netstat >/dev/null 2>&1; then
            if netstat -tlnp 2>/dev/null | grep -q ":$GATEWAY_PORT "; then
                port_listening=1
            fi
        elif command -v ss >/dev/null 2>&1; then
            if ss -tlnp 2>/dev/null | grep -q ":$GATEWAY_PORT "; then
                port_listening=1
            fi
        fi
        
        if [ "$port_listening" -eq 1 ]; then
            log_info "端口 $GATEWAY_PORT 监听正常"
            port_ok=1
        else
            log_error "端口 $GATEWAY_PORT 未监听"
        fi
    else
        # 不检查端口时视为通过
        port_ok=1
    fi
    
    # 使用 openclaw gateway status 命令检查（权威判断）
    if command -v openclaw >/dev/null 2>&1; then
        local gateway_output
        gateway_output=$(openclaw gateway status 2>&1)
        if echo "$gateway_output" | grep -qi "running\|started\|listening\|ok\|reachable"; then
            log_info "openclaw gateway status 命令确认运行中"
            status_cmd_ok=1
        else
            log_warn "openclaw gateway status 未确认运行"
        fi
    fi
    
    # 综合判断：status 命令或端口监听任一通过即认为网关正常
    # pgrep 仅作辅助参考，不参与最终判断（可能受权限限制）
    if [ "$status_cmd_ok" -eq 1 ] || [ "$port_ok" -eq 1 ]; then
        return 0
    else
        log_error "网关异常：status 命令和端口检查均未通过"
        return 1
    fi
}

# ==================== 僵尸状态检测 ====================
check_zombie_state() {
    local threshold_hours="${1:-6}"
    local sessions_dir="$OPENCLAW_HOME/agents/main/sessions"
    local latest_activity=0
    
    if [ ! -d "$sessions_dir" ]; then
        log_warn "sessions 目录不存在: $sessions_dir"
        return 0
    fi
    
    # 查找最新的 session 文件修改时间（使用 find -printf 避免 ps 解析问题）
    local newest_file
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS: 使用 stat 代替 find -printf
        newest_file=$(find "$sessions_dir" -name "*.jsonl" -type f -print0 2>/dev/null | \
                      xargs -0 stat -f "%m %N" 2>/dev/null | sort -rn | head -1 | awk '{print $2}')
    else
        newest_file=$(find "$sessions_dir" -name "*.jsonl" -type f -printf "%T@ %p\n" 2>/dev/null | \
                      sort -rn | head -1 | cut -d' ' -f2-)
    fi
    
    if [ -z "$newest_file" ]; then
        log_warn "未找到 session 文件"
        return 0
    fi
    
    # 计算文件修改时间与当前时间的差值（小时）
    local file_mtime file_age_hours
    if [[ "$OSTYPE" == "darwin"* ]]; then
        file_mtime=$(stat -f "%m" "$newest_file" 2>/dev/null)
    else
        file_mtime=$(stat -c "%Y" "$newest_file" 2>/dev/null)
    fi
    
    if [ -z "$file_mtime" ] || [ "$file_mtime" = "0" ]; then
        log_warn "无法获取 session 文件修改时间"
        return 0
    fi
    
    file_age_hours=$(( ($(date +%s) - file_mtime) / 3600 ))
    
    log_info "最新 session 文件: $(basename "$newest_file"), 修改时间: ${file_age_hours}小时前"
    
    if [ "$file_age_hours" -gt "$threshold_hours" ]; then
        log_warn "检测到僵尸状态: 超过 ${threshold_hours} 小时无活动"
        return 1
    fi
    
    return 0
}

# ==================== OpenClaw 诊断命令 ====================
run_openclaw_doctor() {
    log_info "运行 openclaw doctor 诊断..."
    
    if command -v openclaw >/dev/null 2>&1; then
        openclaw doctor 2>&1 | tee -a "$LOG_FILE"
        return $?
    else
        log_error "openclaw 命令不存在"
        return 1
    fi
}

run_openclaw_status_deep() {
    log_info "运行 openclaw gateway status --deep 深度检查..."
    
    if command -v openclaw >/dev/null 2>&1; then
        openclaw gateway status 2>&1 | tee -a "$LOG_FILE"
        return $?
    else
        log_error "openclaw 命令不存在"
        return 1
    fi
}

run_openclaw_logs() {
    local lines="${1:-50}"
    log_info "获取最近 ${lines} 行日志..."
    
    local log_file
    log_file=$(ls -t "$OPENCLAW_HOME"/logs/openclaw-*.log 2>/dev/null | head -1)
    
    if [ -z "$log_file" ]; then
        log_file=$(ls -t /tmp/openclaw/openclaw-*.log 2>/dev/null | head -1)
    fi
    
    if [ -n "$log_file" ] && [ -f "$log_file" ]; then
        tail -n "$lines" "$log_file" | tee -a "$LOG_FILE"
        return 0
    else
        log_warn "未找到日志文件"
        return 1
    fi
}

# ==================== 重复服务检测 ====================
check_duplicate_services() {
    local conflicts=0
    
    # 检查 systemd 用户级服务
    if command -v systemctl >/dev/null 2>&1; then
        local user_services
        user_services=$(systemctl --user list-units --type=service 2>/dev/null | grep -i openclaw || true)
        
        if [ -n "$user_services" ]; then
            log_warn "检测到用户级 systemd 服务:"
            echo "$user_services" | tee -a "$LOG_FILE"
            ((conflicts++))
        fi
    fi
    
    # 检查 launchctl (macOS)
    if command -v launchctl >/dev/null 2>&1; then
        local launchctl_services
        launchctl_services=$(launchctl list 2>/dev/null | grep -i openclaw || true)
        
        if [ -n "$launchctl_services" ]; then
            log_warn "检测到 launchctl 服务:"
            echo "$launchctl_services" | tee -a "$LOG_FILE"
            ((conflicts++))
        fi
    fi
    
    # 检查系统级 systemd
    if [ -f /etc/systemd/system/openclaw*.service ]; then
        log_warn "检测到系统级 systemd 服务"
        ((conflicts++))
    fi
    
    if [ "$conflicts" -gt 1 ]; then
        log_error "检测到重复服务冲突: $conflicts 个服务同时运行"
        return 1
    fi
    
    log_info "未检测到重复服务"
    return 0
}

# ==================== 主函数（用于测试） ====================
main() {
    load_notify_config
    
    echo "========================================"
    echo "    OpenClaw 核心诊断报告"
    echo "========================================"
    echo ""
    
    echo "1. 检查网关状态..."
    check_gateway_status && echo "   ✅ 网关运行正常" || echo "   ❌ 网关异常"
    echo ""
    
    echo "2. 检查配置..."
    validate_config && echo "   ✅ 配置有效" || echo "   ❌ 配置无效"
    echo ""
    
    echo "3. 检测僵尸状态..."
    check_zombie_state && echo "   ✅ 状态正常" || echo "   ⚠️ 僵尸状态"
    echo ""
    
    echo "4. 检测重复服务..."
    check_duplicate_services && echo "   ✅ 无重复服务" || echo "   ⚠️ 存在冲突"
    echo ""
    
    echo "========================================"
    echo "诊断完成，详细日志: $LOG_FILE"
}

# 如果直接运行脚本，执行主函数；否则作为库被 source
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
