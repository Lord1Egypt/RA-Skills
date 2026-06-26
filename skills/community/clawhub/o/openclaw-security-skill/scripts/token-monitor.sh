#!/bin/bash

# OpenClaw Token消耗监控工具
# Version: 1.0.0
# 监控OpenClaw的Token使用情况，预警异常消耗

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 配置参数
CONFIG_DIR="${HOME}/.openclaw/security"
CONFIG_FILE="${CONFIG_DIR}/token-monitor.conf"
LOG_FILE="${CONFIG_DIR}/openclaw-token-monitor.log"
ALERT_THRESHOLD=10000  # 默认告警阈值：单次请求超过10000 tokens
DAILY_LIMIT=100000     # 默认每日限额：100000 tokens
CHECK_INTERVAL=300     # 默认检查间隔：5分钟

# 日志函数
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "INFO") color=$BLUE ;;
        "SUCCESS") color=$GREEN ;;
        "WARNING") color=$YELLOW ;;
        "ERROR") color=$RED ;;
        "ALERT") color=$PURPLE ;;
        "DEBUG") color=$CYAN ;;
        *) color=$NC ;;
    esac
    
    echo -e "${color}[$level]${NC} $timestamp - $message"
    
    # 确保日志目录存在
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "[$level] $timestamp - $message" >> "$LOG_FILE"
}

# 加载配置文件
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        log "INFO" "加载配置文件: $CONFIG_FILE"
        source "$CONFIG_FILE"
    else
        log "INFO" "使用默认配置"
        # 创建默认配置文件
        create_default_config
    fi
}

# 创建默认配置文件
create_default_config() {
    # 创建配置目录
    mkdir -p "$CONFIG_DIR"
    
    cat > "$CONFIG_FILE" << EOF
# OpenClaw Token监控配置
# 修改后重启监控服务生效

# 告警阈值（单次请求tokens）
ALERT_THRESHOLD=10000

# 每日限额（每日总tokens）
DAILY_LIMIT=100000

# 检查间隔（秒）
CHECK_INTERVAL=300

# 告警方式
# email: 邮件告警
# webhook: Webhook告警  
# log: 仅记录日志
ALERT_METHOD="log"

# 邮件配置（如果使用邮件告警）
EMAIL_RECIPIENT="admin@example.com"
EMAIL_SENDER="openclaw-monitor@$(hostname)"

# Webhook配置（如果使用Webhook告警）
WEBHOOK_URL=""
WEBHOOK_SECRET=""

# 监控的日志文件路径
LOG_PATHS=(
    "/var/log/openclaw.log"
    "/var/log/syslog"
    "/tmp/openclaw*.log"
)
EOF
    log "SUCCESS" "已创建默认配置文件: $CONFIG_FILE"
}

# 解析日志中的Token使用信息
parse_token_usage() {
    local log_file=$1
    local since=$2
    
    # 从系统日志中提取Token信息
    local token_data=$(journalctl -u openclaw --since "$since" 2>/dev/null | \
        grep -E "(tokens|token|cost|消耗|用量)" | \
        tail -50)
    
    if [[ -z "$token_data" ]]; then
        # 尝试从应用日志中提取
        token_data=$(grep -E "(tokens|token|cost|消耗|用量)" "$log_file" 2>/dev/null | tail -50)
    fi
    
    echo "$token_data"
}

# 提取Token数量
extract_token_count() {
    local line=$1
    
    # 尝试多种匹配模式
    local patterns=(
        '([0-9,]+)\s*tokens'
        'tokens:\s*([0-9,]+)'
        '消耗.*?([0-9,]+)\s*token'
        '用量.*?([0-9,]+)'
        'cost.*?([0-9,]+)'
    )
    
    for pattern in "${patterns[@]}"; do
        if echo "$line" | grep -q -E "$pattern"; then
            local count=$(echo "$line" | grep -o -E "$pattern" | head -1 | grep -o -E '[0-9,]+' | tr -d ',')
            echo "$count"
            return 0
        fi
    done
    
    echo "0"
}

# 分析Token使用情况
analyze_token_usage() {
    local token_data=$1
    local analysis_file="/tmp/openclaw-token-analysis-$(date +%Y%m%d).txt"
    
    local total_tokens=0
    local request_count=0
    local high_usage_count=0
    local max_tokens=0
    local high_usage_requests=()
    
    # 逐行分析
    while IFS= read -r line; do
        local token_count=$(extract_token_count "$line")
        
        if [[ "$token_count" != "0" ]]; then
            total_tokens=$((total_tokens + token_count))
            request_count=$((request_count + 1))
            
            # 记录最大使用量
            if [[ $token_count -gt $max_tokens ]]; then
                max_tokens=$token_count
            fi
            
            # 检查是否超过告警阈值
            if [[ $token_count -gt $ALERT_THRESHOLD ]]; then
                high_usage_count=$((high_usage_count + 1))
                high_usage_requests+=("$line")
            fi
        fi
    done <<< "$token_data"
    
    # 生成分析报告
    {
        echo "=== OpenClaw Token使用分析报告 ==="
        echo "生成时间: $(date)"
        echo "分析周期: 最近检查间隔"
        echo ""
        echo "统计摘要:"
        echo "  总请求数: $request_count"
        echo "  总Token消耗: $total_tokens"
        echo "  平均每次请求: $((request_count > 0 ? total_tokens / request_count : 0))"
        echo "  最大单次请求: $max_tokens"
        echo "  超过阈值请求: $high_usage_count"
        echo ""
        echo "告警阈值: $ALERT_THRESHOLD tokens/请求"
        echo "每日限额: $DAILY_LIMIT tokens"
        echo ""
        
        if [[ $high_usage_count -gt 0 ]]; then
            echo "=== 高Token消耗请求 ==="
            for ((i=0; i<${#high_usage_requests[@]}; i++)); do
                echo "$((i+1)). ${high_usage_requests[$i]}"
            done
            echo ""
        fi
        
        # 检查每日限额
        local daily_usage=$(get_daily_usage)
        local remaining=$((DAILY_LIMIT - daily_usage))
        
        echo "=== 每日限额状态 ==="
        echo "  今日已用: $daily_usage tokens"
        echo "  剩余额度: $remaining tokens"
        echo "  使用比例: $((daily_usage * 100 / DAILY_LIMIT))%"
        
        if [[ $daily_usage -gt $((DAILY_LIMIT * 80 / 100)) ]]; then
            echo "  ⚠️  警告: 今日使用量已超过80%"
        fi
        
        if [[ $daily_usage -ge $DAILY_LIMIT ]]; then
            echo "  🚨 警报: 今日使用量已达限额！"
        fi
        
    } > "$analysis_file"
    
    # 输出摘要
    log "INFO" "Token分析完成: $request_count 次请求, 总消耗 $total_tokens tokens"
    
    if [[ $high_usage_count -gt 0 ]]; then
        log "WARNING" "发现 $high_usage_count 次请求超过告警阈值 ($ALERT_THRESHOLD tokens)"
    fi
    
    if [[ $max_tokens -gt 0 ]]; then
        log "INFO" "最大单次请求: $max_tokens tokens"
    fi
    
    # 检查是否需要告警
    check_alerts "$total_tokens" "$high_usage_count" "$max_tokens"
    
    # 返回分析文件路径
    echo "$analysis_file"
}

# 获取今日总使用量
get_daily_usage() {
    local today=$(date +%Y-%m-%d)
    local daily_log="/var/log/openclaw-token-daily-$today.log"
    
    if [[ -f "$daily_log" ]]; then
        local total=$(awk '{sum+=$1} END {print sum}' "$daily_log" 2>/dev/null || echo "0")
        echo "${total:-0}"
    else
        echo "0"
    fi
}

# 记录每日使用量
record_daily_usage() {
    local usage=$1
    local today=$(date +%Y-%m-%d)
    local daily_log="${CONFIG_DIR}/openclaw-token-daily-$today.log"
    
    echo "$usage" >> "$daily_log"
}

# 检查并发送告警
check_alerts() {
    local total_tokens=$1
    local high_usage_count=$2
    local max_tokens=$3
    
    local alerts=()
    
    # 检查单次请求超限
    if [[ $max_tokens -gt $ALERT_THRESHOLD ]]; then
        alerts+=("单次请求使用 $max_tokens tokens，超过阈值 $ALERT_THRESHOLD")
    fi
    
    # 检查高频超限请求
    if [[ $high_usage_count -gt 5 ]]; then
        alerts+=("发现 $high_usage_count 次请求超过阈值，可能存在异常")
    fi
    
    # 检查今日总额度
    local daily_usage=$(get_daily_usage)
    local new_daily_usage=$((daily_usage + total_tokens))
    record_daily_usage "$total_tokens"
    
    if [[ $new_daily_usage -gt $((DAILY_LIMIT * 80 / 100)) ]]; then
        alerts+=("今日使用量 $new_daily_usage/$DAILY_LIMIT tokens，已超过80%")
    fi
    
    if [[ $new_daily_usage -ge $DAILY_LIMIT ]]; then
        alerts+=("🚨 今日使用量 $new_daily_usage/$DAILY_LIMIT tokens，已达限额！")
    fi
    
    # 发送告警
    if [[ ${#alerts[@]} -gt 0 ]]; then
        for alert in "${alerts[@]}"; do
            log "ALERT" "$alert"
            send_alert "$alert"
        done
    fi
}

# 发送告警
send_alert() {
    local message=$1
    
    case $ALERT_METHOD in
        "email")
            send_email_alert "$message"
            ;;
        "webhook")
            send_webhook_alert "$message"
            ;;
        "log")
            # 仅记录日志，不发送外部告警
            ;;
        *)
            log "WARNING" "未知的告警方式: $ALERT_METHOD"
            ;;
    esac
}

# 发送邮件告警
send_email_alert() {
    local message=$1
    local subject="OpenClaw Token使用告警 - $(hostname)"
    
    # 这里需要配置邮件发送
    log "INFO" "邮件告警功能需要配置邮件服务器"
    # echo "$message" | mail -s "$subject" "$EMAIL_RECIPIENT"
}

# 发送Webhook告警
send_webhook_alert() {
    local message=$1
    
    if [[ -n "$WEBHOOK_URL" ]]; then
        local payload=$(cat << EOF
{
    "text": "OpenClaw Token告警",
    "attachments": [{
        "color": "danger",
        "text": "$message",
        "ts": $(date +%s)
    }]
}
EOF
        )
        
        curl -s -X POST -H "Content-Type: application/json" \
             -d "$payload" "$WEBHOOK_URL" > /dev/null 2>&1
    fi
}

# 监控循环
monitor_loop() {
    log "INFO" "开始Token监控，检查间隔: ${CHECK_INTERVAL}秒"
    
    while true; do
        local start_time=$(date -d "$CHECK_INTERVAL seconds ago" '+%Y-%m-%d %H:%M:%S')
        
        # 获取Token使用数据
        local token_data=$(parse_token_usage "/var/log/openclaw.log" "$start_time")
        
        if [[ -n "$token_data" ]]; then
            # 分析Token使用情况
            local analysis_file=$(analyze_token_usage "$token_data")
            
            # 显示摘要
            log "DEBUG" "分析报告已保存: $analysis_file"
        else
            log "INFO" "未发现Token使用记录"
        fi
        
        # 等待下一个检查周期
        sleep "$CHECK_INTERVAL"
    done
}

# 单次检查模式
single_check() {
    log "INFO" "执行单次Token使用检查"
    
    local since=$(date -d "1 hour ago" '+%Y-%m-%d %H:%M:%S')
    local token_data=$(parse_token_usage "/var/log/openclaw.log" "$since")
    
    if [[ -n "$token_data" ]]; then
        local analysis_file=$(analyze_token_usage "$token_data")
        log "SUCCESS" "检查完成，报告: $analysis_file"
        
        # 显示报告内容
        echo ""
        cat "$analysis_file"
    else
        log "SUCCESS" "最近1小时未发现Token使用记录"
    fi
}

# 显示使用帮助
show_help() {
    cat << EOF
OpenClaw Token消耗监控工具 v1.0.0

使用方法:
  $0 [选项]

选项:
  start     启动监控服务（后台运行）
  stop      停止监控服务
  status    查看监控状态
  check     执行单次检查
  config    编辑配置文件
  help      显示此帮助信息
  version   显示版本信息

示例:
  $0 start    # 启动监控服务
  $0 check    # 执行单次检查
  $0 config   # 编辑配置文件

配置文件: $CONFIG_FILE
日志文件: $LOG_FILE
EOF
}

# 主函数
main() {
    local command=${1:-"help"}
    
    # 加载配置
    load_config
    
    case $command in
        "start")
            log "INFO" "启动Token监控服务..."
            monitor_loop &
            echo $! > /var/run/openclaw-token-monitor.pid
            log "SUCCESS" "监控服务已启动，PID: $(cat /var/run/openclaw-token-monitor.pid)"
            ;;
        "stop")
            if [[ -f /var/run/openclaw-token-monitor.pid ]]; then
                local pid=$(cat /var/run/openclaw-token-monitor.pid)
                log "INFO" "停止监控服务，PID: $pid"
                kill "$pid" 2>/dev/null
                rm -f /var/run/openclaw-token-monitor.pid
                log "SUCCESS" "监控服务已停止"
            else
                log "WARNING" "未找到监控服务PID文件"
            fi
            ;;
        "status")
            if [[ -f /var/run/openclaw-token-monitor.pid ]]; then
                local pid=$(cat /var/run/openclaw-token-monitor.pid)
                if kill -0 "$pid" 2>/dev/null; then
                    log "SUCCESS" "监控服务正在运行，PID: $pid"
                else
                    log "ERROR" "监控服务进程不存在"
                fi
            else
                log "INFO" "监控服务未运行"
            fi
            ;;
        "check")
            single_check
            ;;
        "config")
            ${EDITOR:-vi} "$CONFIG_FILE"
            ;;
        "help")
            show_help
            ;;
        "version")
            echo "OpenClaw Token消耗监控工具 v1.0.0"
            ;;
        *)
            log "ERROR" "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"