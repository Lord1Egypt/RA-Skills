#!/bin/bash
# ~/.openclaw/scripts/health-check.sh
# OpenClaw 健康检查脚本

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
LOG_DIR="$OPENCLAW_HOME/logs"
LOG_FILE="$LOG_DIR/health-check.log"
ALERT_FILE="$LOG_DIR/alerts.log"
GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"

# 阈值配置
DISK_THRESHOLD=90
MEMORY_THRESHOLD=85
SESSION_INACTIVE_HOURS=6
PROVIDER_UPTIME_HOURS=6
HEALTH_CHECK_TIMEOUT=10

mkdir -p "$LOG_DIR"

# 加载核心函数
source "$SCRIPT_DIR/core.sh"

# ==================== 检查项: Gateway 响应 ====================
check_gateway_health() {
    local url="http://localhost:$GATEWAY_PORT/health"
    
    if command -v curl >/dev/null 2>&1; then
        if curl -sf --max-time "$HEALTH_CHECK_TIMEOUT" "$url" >/dev/null 2>&1; then
            log_info "Gateway 健康检查通过"
            return 0
        fi
    elif command -v wget >/dev/null 2>&1; then
        if wget -q -T "$HEALTH_CHECK_TIMEOUT" -O - "$url" >/dev/null 2>&1; then
            log_info "Gateway 健康检查通过"
            return 0
        fi
    fi
    
    log_error "Gateway 健康检查失败: $url"
    return 1
}

# ==================== 检查项: 提供者存活 ====================
check_provider_uptime() {
    local threshold_hours="$PROVIDER_UPTIME_HOURS"
    
    # 检测配置中启用的 channel
    local channels=""
    if [ -f "$OPENCLAW_HOME/openclaw.json" ] && command -v jq >/dev/null 2>&1; then
        channels=$(jq -r '.channels // {} | keys[]' "$OPENCLAW_HOME/openclaw.json" 2>/dev/null | tr '\n' ' ')
    fi
    
    # 如果配置了 channels，只检查存在的 channel；否则检查所有
    local provider_pid=""
    local found_channel=""
    if [ -n "$channels" ]; then
        for ch in $channels; do
            provider_pid=$(pgrep -f "openclaw.*provider.*$ch" 2>/dev/null | head -1)
            if [ -n "$provider_pid" ]; then
                found_channel="$ch"
                break
            fi
        done
    fi
    
    # 备用：检查 gateway 主进程作为 provider 代理（feishu 等内置 channel 无独立进程）
    if [ -z "$provider_pid" ]; then
        provider_pid=$(pgrep -f "openclaw.*gateway" 2>/dev/null | head -1)
    fi
    # pgrep 在 macOS 沙箱中可能失败，使用 ps 作为兜底
    if [ -z "$provider_pid" ]; then
        provider_pid=$(ps -eo pid,comm 2>/dev/null | awk '/openclaw-gateway/ {print $1; exit}')
        if [ -n "$provider_pid" ]; then
            found_channel="gateway (内置 channel)"
        fi
    fi
    
    if [ -z "$provider_pid" ]; then
        log_warn "未找到任何 provider 或 gateway 进程"
        return 1
    fi
    
    # 获取进程运行时间（使用 etime 代替 lstart，避免 date 解析问题）
    local etime start_time current_time uptime_hours
    etime=$(ps -p "$provider_pid" -o etime= 2>/dev/null | xargs)
    
    if [ -z "$etime" ]; then
        log_warn "无法获取进程运行时间"
        return 0
    fi
    
    # 解析 etime 格式: [[DD-]HH:]MM:SS 或 [DDD-]HH:MM:SS
    # 转换为秒数
    local total_seconds=0
    if echo "$etime" | grep -q '-'; then
        # 包含天数: D-HH:MM:SS
        local days rest
        days=$(echo "$etime" | cut -d'-' -f1)
        rest=$(echo "$etime" | cut -d'-' -f2)
        local hours minutes seconds
        hours=$(echo "$rest" | cut -d':' -f1)
        minutes=$(echo "$rest" | cut -d':' -f2)
        seconds=$(echo "$rest" | cut -d':' -f3)
        total_seconds=$((days * 86400 + hours * 3600 + minutes * 60 + seconds))
    else
        # 无天数: HH:MM:SS 或 MM:SS
        local parts count
        parts=$(echo "$etime" | tr ':' ' ')
        count=$(echo "$parts" | wc -w)
        if [ "$count" -eq 3 ]; then
            # HH:MM:SS
            local h m s
            h=$(echo "$parts" | awk '{print $1}')
            m=$(echo "$parts" | awk '{print $2}')
            s=$(echo "$parts" | awk '{print $3}')
            total_seconds=$((h * 3600 + m * 60 + s))
        elif [ "$count" -eq 2 ]; then
            # MM:SS
            local m s
            m=$(echo "$parts" | awk '{print $1}')
            s=$(echo "$parts" | awk '{print $2}')
            total_seconds=$((m * 60 + s))
        fi
    fi
    
    uptime_hours=$((total_seconds / 3600))
    log_info "Provider ($found_channel) 运行时间: ${uptime_hours}小时 (${etime})"
    
    if [ "$uptime_hours" -gt "$threshold_hours" ]; then
        log_warn "Provider 超过 ${threshold_hours} 小时无重启"
        return 1
    fi
    
    return 0
}

# ==================== 检查项: 消息活动 ====================
check_message_activity() {
    local threshold_hours="$SESSION_INACTIVE_HOURS"
    local sessions_dir="$OPENCLAW_HOME/agents/main/sessions"
    
    if [ ! -d "$sessions_dir" ]; then
        log_warn "sessions 目录不存在，跳过消息活动检查"
        return 0
    fi
    
    # 查找最新的 session 文件
    local newest_file newest_time
    newest_file=$(find "$sessions_dir" -name "*.jsonl" -type f -exec stat -f "%m %N" {} + 2>/dev/null | \
                  sort -rn | head -1 | awk '{print $2}')
    
    if [ -z "$newest_file" ]; then
        log_warn "未找到 session 文件"
        return 0
    fi
    
    # 获取文件修改时间
    local file_mtime file_age_hours
    if [[ "$OSTYPE" == "darwin"* ]]; then
        file_mtime=$(stat -f "%m" "$newest_file" 2>/dev/null)
    else
        file_mtime=$(stat -c "%Y" "$newest_file" 2>/dev/null)
    fi
    
    file_age_hours=$(( ($(date +%s) - $file_mtime) / 3600 ))
    
    log_info "最新 session: $(basename "$newest_file"), ${file_age_hours}小时前"
    
    if [ "$file_age_hours" -gt "$threshold_hours" ]; then
        log_error "检测到僵尸状态: 超过 ${threshold_hours} 小时无消息活动"
        return 1
    fi
    
    return 0
}

# ==================== 检查项: 配置有效性 ====================
check_config_validity() {
    if validate_config; then
        log_info "配置有效性检查通过"
        return 0
    else
        log_error "配置有效性检查失败"
        return 1
    fi
}

# ==================== 检查项: 资源使用 ====================
check_disk_usage() {
    local usage
    usage=$(df -h "$OPENCLAW_HOME" | awk 'NR==2 {gsub(/%/,""); print $5}')
    
    log_info "磁盘使用率: ${usage}%"
    
    if [ "$usage" -gt "$DISK_THRESHOLD" ]; then
        log_error "磁盘使用率超过阈值: ${usage}% > ${DISK_THRESHOLD}%"
        return 1
    fi
    
    return 0
}

check_memory_usage() {
    local usage
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        usage=$(vm_stat | awk '
            /Pages free/ { free=$3 }
            /Pages active/ { active=$3 }
            /Pages inactive/ { inactive=$3 }
            /Pages wired/ { wired=$3 }
            END {
                gsub(/\\/,"",free)
                gsub(/\\/,"",active)
                gsub(/\\/,"",inactive)
                gsub(/\\/,"",wired)
                total = free + active + inactive + wired
                if (total > 0) printf "%.0f", (active + wired) * 100 / total
            }'
        )
    else
        usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    fi
    
    log_info "内存使用率: ${usage}%"
    
    if [ -n "$usage" ] && [ "$usage" -gt "$MEMORY_THRESHOLD" ]; then
        log_error "内存使用率超过阈值: ${usage}% > ${MEMORY_THRESHOLD}%"
        return 1
    fi
    
    return 0
}

# ==================== 记录告警 ====================
record_alert() {
    local check_name="$1"
    local message="$2"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$check_name] $message" >> "$ALERT_FILE"
    notify "WARNING" "[$check_name] $message"
}

# ==================== 主函数 ====================
main() {
    load_notify_config
    
    log_info "========== 健康检查开始 =========="
    
    local check_results=()
    local issues=0
    
    echo ""
    echo "========================================"
    echo "    OpenClaw 健康检查报告"
    echo "========================================"
    echo ""
    
    # 1. Gateway 响应检查
    echo -n "1. Gateway 响应检查 ... "
    if check_gateway_health; then
        echo "✅ 通过"
    else
        echo "❌ 失败"
        record_alert "GATEWAY_HEALTH" "Gateway 健康检查失败"
        issues=$((issues + 1))
        check_results+=("❌ Gateway 响应")
    fi
    
    # 2. Telegram 提供者存活检查
    echo -n "2. Telegram 提供者检查 ... "
    if check_provider_uptime; then
        echo "✅ 通过"
    else
        echo "⚠️ 警告"
        record_alert "PROVIDER_UPTIME" "Telegram provider 超过 ${PROVIDER_UPTIME_HOURS} 小时无重启"
        issues=$((issues + 1))
        check_results+=("⚠️ Provider 存活")
    fi
    
    # 3. 消息活动检查
    echo -n "3. 消息活动检查 ... "
    if check_message_activity; then
        echo "✅ 通过"
    else
        echo "❌ 失败"
        record_alert "MESSAGE_ACTIVITY" "检测到僵尸状态，超过 ${SESSION_INACTIVE_HOURS} 小时无消息"
        issues=$((issues + 1))
        check_results+=("❌ 消息活动")
    fi
    
    # 4. 配置有效性检查
    echo -n "4. 配置有效性检查 ... "
    if check_config_validity; then
        echo "✅ 通过"
    else
        echo "❌ 失败"
        record_alert "CONFIG_VALIDITY" "配置文件无效或损坏"
        issues=$((issues + 1))
        check_results+=("❌ 配置有效性")
    fi
    
    # 5. 资源检查
    echo -n "5. 磁盘使用检查 ... "
    if check_disk_usage; then
        echo "✅ 通过"
    else
        echo "❌ 失败"
        record_alert "DISK_USAGE" "磁盘使用率超过 ${DISK_THRESHOLD}%"
        issues=$((issues + 1))
        check_results+=("❌ 磁盘使用")
    fi
    
    echo -n "6. 内存使用检查 ... "
    if check_memory_usage; then
        echo "✅ 通过"
    else
        echo "⚠️ 警告"
        record_alert "MEMORY_USAGE" "内存使用率超过 ${MEMORY_THRESHOLD}%"
        issues=$((issues + 1))
        check_results+=("⚠️ 内存使用")
    fi
    
    echo ""
    echo "========================================"
    
    if [ "$issues" -eq 0 ]; then
        echo "   ✅ 所有检查通过 (问题: $issues)"
    else
        echo "   ⚠️ 发现 $issues 项异常"
        echo ""
        echo "异常项目:"
        for item in "${check_results[@]}"; do
            echo "   - $item"
        done
    fi
    
    echo "========================================"
    echo ""
    log_info "========== 健康检查完成 (问题: $issues) =========="
    
    exit $issues
}

main "$@"
