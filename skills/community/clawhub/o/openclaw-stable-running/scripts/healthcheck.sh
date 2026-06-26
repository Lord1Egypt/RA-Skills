#!/bin/bash
#
# OpenClaw 健康检查脚本
# 用法: */5 * * * * /home/openclaw/scripts/healthcheck.sh
#
# 功能:
#   1. 检查 Gateway 进程是否存在
#   2. 检查健康端点是否响应
#   3. 两者任一失败 → 自动重启 + 记录日志
#

LOG_FILE="/var/log/openclaw/healthcheck.log"
GATEWAY_URL="http://localhost:9527/health"
LOGDIR="$(dirname "$LOG_FILE")"

# 确保日志目录存在
mkdir -p "$LOGDIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Uptime Kuma 心跳上报（可选，填入 URL 即可启用）
UPTIME_KUMA_URL=""

report_uptime_kuma() {
    if [ -n "$UPTIME_KUMA_URL" ]; then
        curl -s -m 10 "$UPTIME_KUMA_URL" > /dev/null 2>&1
    fi
}

# 检查进程是否存在
check_process() {
    if pgrep -f "openclaw gateway" > /dev/null 2>&1; then
        return 0
    else
        log "[WARN] Gateway 进程不存在"
        return 1
    fi
}

# 检查健康端点
check_gateway() {
    if curl -sf "$GATEWAY_URL" > /dev/null 2>&1; then
        log "[OK] Gateway 健康检查通过"
        return 0
    else
        log "[WARN] Gateway 健康端点无响应: $GATEWAY_URL"
        return 1
    fi
}

# 重启 Gateway
restart_gateway() {
    log "[INFO] 开始重启 Gateway..."

    # 优先用 systemd
    if command -v systemctl > /dev/null 2>&1 && systemctl list-unit-files openclaw.service > /dev/null 2>&1; then
        systemctl restart openclaw
        RESTART_CMD="systemctl restart openclaw"
    # 其次用 PM2
    elif command -v pm2 > /dev/null 2>&1 && pm2 list | grep -q openclaw; then
        pm2 restart openclaw-gateway 2>/dev/null || pm2 restart openclaw 2>/dev/null
        RESTART_CMD="pm2 restart openclaw"
    # 最后直接启动
    else
        cd /home/openclaw/.openclaw && openclaw gateway start > /dev/null 2>&1 &
        RESTART_CMD="直接启动"
    fi

    log "[INFO] 执行重启命令: $RESTART_CMD"
    sleep 10

    if check_gateway; then
        log "[OK] Gateway 重启成功"
        report_uptime_kuma
    else
        log "[ERROR] Gateway 重启失败！需要人工介入"
    fi
}

# 主逻辑
main() {
    log "[INFO] ===== 健康检查开始 ====="

    PROCESS_OK=0
    HEALTH_OK=0

    check_process && PROCESS_OK=1 || PROCESS_OK=0
    check_gateway && HEALTH_OK=1 || HEALTH_OK=0

    if [ "$PROCESS_OK" -eq 0 ] || [ "$HEALTH_OK" -eq 0 ]; then
        log "[WARN] 检测异常，进程=$PROCESS_OK 健康=$HEALTH_OK"
        restart_gateway
    else
        log "[INFO] 全部检查通过"
        report_uptime_kuma
    fi

    log "[INFO] ===== 健康检查结束 ====="
}

main
