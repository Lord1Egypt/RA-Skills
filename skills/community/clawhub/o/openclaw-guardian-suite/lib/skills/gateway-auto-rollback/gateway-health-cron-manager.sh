#!/bin/bash
# Gateway 健康检查 Cron 管理器
# 功能: 启动一个轻量级 cron 健康检查任务，连续3次健康后自动禁用
# 用途: 配置修改后启动，确认配置稳定后自动退出
# 创建: 2026-03-01
# 依赖: openclaw CLI

set -euo pipefail

CRON_NAME="Gateway-Health-AutoDisable"
STATE_FILE="$HOME/.openclaw/logs/gateway-health-state.json"
LOG_FILE="$HOME/.openclaw/logs/gateway-rollback.log"
GATEWAY_URL="http://127.0.0.1:18789/api/health"

# 默认参数
INTERVAL_MS=300000   # 5分钟
THRESHOLD=3          # 连续健康次数阈值

log() {
    local ts
    ts=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$ts] $1" | tee -a "$LOG_FILE"
}

usage() {
    cat <<EOF
Gateway 健康检查 Cron 管理器

用法:
  $0 start [--interval <分钟>] [--threshold <次数>]
    启动健康检查 cron 任务
    --interval   检查间隔(分钟), 默认 5
    --threshold  连续健康次数阈值, 默认 3

  $0 stop
    停止并禁用健康检查 cron 任务

  $0 status
    查看当前状态

  $0 reset
    重置连续健康计数器

示例:
  $0 start                    # 默认: 5分钟间隔, 3次阈值
  $0 start --interval 3 --threshold 5  # 3分钟间隔, 5次阈值
  $0 status
  $0 stop
EOF
}

# 初始化/读取状态文件
init_state() {
    mkdir -p "$(dirname "$STATE_FILE")"
    if [ ! -f "$STATE_FILE" ]; then
        echo '{"consecutive_healthy":0,"threshold":3,"cron_job_id":null,"last_check":null}' > "$STATE_FILE"
    fi
}

get_state() {
    python3 -c "
import json
with open('$STATE_FILE') as f:
    s = json.load(f)
print(s.get('$1', ''))
"
}

set_state() {
    python3 -c "
import json
with open('$STATE_FILE') as f:
    s = json.load(f)
s['$1'] = $2
with open('$STATE_FILE', 'w') as f:
    json.dump(s, f, indent=2)
"
}

# 查找已有的健康检查 cron 任务
find_existing_job() {
    # 通过 openclaw cron 列表查找
    local job_id
    job_id=$(get_state "cron_job_id")
    if [ -n "$job_id" ] && [ "$job_id" != "None" ] && [ "$job_id" != "null" ]; then
        echo "$job_id"
    fi
}

cmd_start() {
    local interval_min=5
    local threshold=3

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --interval) interval_min="$2"; shift 2 ;;
            --threshold) threshold="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    local interval_ms=$((interval_min * 60 * 1000))

    init_state
    set_state "threshold" "$threshold"
    set_state "consecutive_healthy" "0"

    # 检查是否已有任务在运行
    local existing_id
    existing_id=$(find_existing_job)
    if [ -n "$existing_id" ]; then
        log "⚠️ 已有健康检查任务 ($existing_id)，先停止"
        # 不直接操作 cron，由调用方处理
    fi

    log "🚀 启动 Gateway 健康检查 Cron (间隔: ${interval_min}分钟, 阈值: ${threshold}次)"
    echo "INTERVAL_MS=$interval_ms"
    echo "THRESHOLD=$threshold"
    echo "STATE_FILE=$STATE_FILE"
}

cmd_stop() {
    init_state
    local job_id
    job_id=$(find_existing_job)
    if [ -n "$job_id" ]; then
        log "🛑 停止健康检查 cron 任务: $job_id"
        echo "JOB_ID=$job_id"
    else
        log "ℹ️ 没有找到运行中的健康检查任务"
    fi
    set_state "consecutive_healthy" "0"
    set_state "cron_job_id" "null"
}

cmd_status() {
    init_state
    local healthy threshold job_id last_check
    healthy=$(get_state "consecutive_healthy")
    threshold=$(get_state "threshold")
    job_id=$(get_state "cron_job_id")
    last_check=$(get_state "last_check")

    echo "=== Gateway 健康检查状态 ==="
    echo "连续健康次数: $healthy / $threshold"
    echo "Cron 任务 ID: ${job_id:-无}"
    echo "上次检查: ${last_check:-从未}"
    echo "状态文件: $STATE_FILE"

    if [ "$healthy" -ge "$threshold" ] 2>/dev/null; then
        echo "结论: ✅ 已达阈值，任务应已自动禁用"
    else
        echo "结论: 🔄 检查进行中"
    fi
}

cmd_reset() {
    init_state
    set_state "consecutive_healthy" "0"
    log "🔄 已重置连续健康计数器"
    echo "已重置"
}

case "${1:-help}" in
    start)  shift; cmd_start "$@" ;;
    stop)   cmd_stop ;;
    status) cmd_status ;;
    reset)  cmd_reset ;;
    help|--help|-h) usage ;;
    *)      echo "未知命令: $1"; usage; exit 1 ;;
esac
