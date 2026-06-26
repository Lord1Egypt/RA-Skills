#!/bin/bash
#
# OpenClaw 看门狗脚本
# 监控 OpenClaw Gateway 状态、通道状态、网络状态
# 支持：飞书、企业微信、微信 等通道的错误检测与恢复
#

LOG_FILE="${LOG_FILE:-/tmp/openclaw_watchdog.log}"
PID_FILE="${PID_FILE:-/tmp/openclaw_gateway.pid}"
MAX_RESTARTS="${MAX_RESTARTS:-2}"
RESTART_WINDOW="${RESTART_WINDOW:-600}"
OPENCLAW_PORT="${OPENCLAW_PORT:-18789}"
PROXY_DISABLED_FILE="/tmp/openclaw_proxy_disabled"
COUNT_FILE="/tmp/openclaw_restart_count"
TIME_FILE="/tmp/openclaw_restart_time"

# 通道暂停状态文件
WECOM_PAUSED_FILE="/tmp/openclaw_wecom_paused"
FEISHU_PAUSED_FILE="/tmp/openclaw_feishu_paused"
WEIXIN_PAUSED_FILE="/tmp/openclaw_weixin_paused"

# ============================================
# 日志函数
# ============================================
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# ============================================
# 进程存活检测（修复误报）
# ============================================
is_process_alive() {
    # 方法1：检查 systemd 服务状态
    if systemctl --user is-active openclaw-gateway >/dev/null 2>&1; then
        return 0
    fi

    # 方法2：检查端口是否监听
    if ss -tlnp 2>/dev/null | grep -q ":$OPENCLAW_PORT"; then
        return 0
    fi

    # 方法3：检查 gateway 相关进程
    if pgrep -f "openclaw.*gateway" >/dev/null 2>&1; then
        return 0
    fi

    return 1
}

# ============================================
# 网络检测
# ============================================
check_network() {
    ping -c 1 -W 3 www.baidu.com > /dev/null 2>&1 && return 0
    ping -c 1 -W 3 223.5.5.5 > /dev/null 2>&1 && return 0
    return 1
}

# ============================================
# WebSocket 错误检测
# ============================================
has_ws_errors() {
    local log_file="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    if [ ! -f "$log_file" ]; then
        return 1
    fi

    # 检测最近 3 分钟的 WebSocket 错误
    journalctl --user -u openclaw-gateway -n 200 --since "3 minutes ago" 2>/dev/null | \
        grep -qE "protocol mismatch|connect failed|system busy|Cannot read properties.*undefined|auto-restart attempt [0-9]+/[0-9]+" && return 0

    return 1
}

# ============================================
# 飞书通道状态检测
# ============================================
check_feishu_channel() {
    local log_file="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    if [ ! -f "$log_file" ]; then
        return 0
    fi

    # 检测飞书错误
    if grep -qE "feishu.*error|feishu.*fail|lark.*error|lark.*fail" "$log_file" 2>/dev/null; then
        log "⚠️ 飞书通道异常"
        touch "$FEISHU_PAUSED_FILE"
    fi

    # 检测 session 过期
    if grep -qE "feishu.*session.*expired|feishu.*pausing|lark.*session.*expired" "$log_file" 2>/dev/null; then
        log "⚠️ 飞书 session 过期"
        touch "$FEISHU_PAUSED_FILE"
    fi

    # 检测恢复
    if [ -f "$FEISHU_PAUSED_FILE" ]; then
        if grep -qE "feishu.*reconnect|feishu.*resume|feishu.*connected|lark.*reconnect|lark.*resume|lark.*connected" "$log_file" 2>/dev/null; then
            log "✅ 飞书通道已恢复"
            rm -f "$FEISHU_PAUSED_FILE"
        fi
    fi
}

# ============================================
# 企业微信通道状态检测
# ============================================
check_wecom_channel() {
    local log_file="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    if [ ! -f "$log_file" ]; then
        return 0
    fi

    # 检测企业微信错误
    if grep -qE "wecom.*error|wecom.*fail|wechat.*work.*error" "$log_file" 2>/dev/null; then
        log "⚠️ 企业微信通道异常"
        touch "$WECOM_PAUSED_FILE"
    fi

    # 检测 session 过期
    if grep -qE "wecom.*session.*expired|wecom.*pausing|wechat.*work.*session.*expired" "$log_file" 2>/dev/null; then
        log "⚠️ 企业微信 session 过期"
        touch "$WECOM_PAUSED_FILE"
    fi

    # 检测恢复
    if [ -f "$WECOM_PAUSED_FILE" ]; then
        if grep -qE "wecom.*reconnect|wecom.*resume|wecom.*connected|wechat.*work.*reconnect" "$log_file" 2>/dev/null; then
            log "✅ 企业微信通道已恢复"
            rm -f "$WECOM_PAUSED_FILE"
        fi
    fi
}

# ============================================
# 微信通道状态检测
# ============================================
check_weixin_channel() {
    local log_file="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    if [ ! -f "$log_file" ]; then
        return 0
    fi

    # 检测微信错误（openclaw-weixin 通道）
    if grep -qE "weixin.*error|weixin.*fail|getUpdates.*failed" "$log_file" 2>/dev/null; then
        log "⚠️ 微信通道异常"
        touch "$WEIXIN_PAUSED_FILE"
    fi

    # 检测 session 过期 (errcode -14)
    if grep -qE "weixin.*session.*expired|weixin.*pausing|errcode.*-14|session.*expired.*pausing" "$log_file" 2>/dev/null; then
        log "⚠️ 微信 session 过期（errcode -14，暂停 60 分钟）"
        touch "$WEIXIN_PAUSED_FILE"
    fi

    # 检测恢复
    if [ -f "$WEIXIN_PAUSED_FILE" ]; then
        if grep -qE "weixin.*reconnect|weixin.*resume|weixin.*connected|inbound.*message.*success" "$log_file" 2>/dev/null; then
            log "✅ 微信通道已恢复"
            rm -f "$WEIXIN_PAUSED_FILE"
        fi
    fi
}

# ============================================
# 禁用代理（网络异常时）
# ============================================
disable_proxy() {
    [ -f "$PROXY_DISABLED_FILE" ] && return 0
    log "⚠️ 网络异常，关闭系统代理..."

    # 禁用系统代理
    [ -f /etc/profile.d/proxy.sh ] && sudo mv /etc/profile.d/proxy.sh /etc/profile.d/proxy.sh.disabled 2>/dev/null

    # 清除环境变量
    systemctl --user set-environment http_proxy= https_proxy= all_proxy= HTTP_PROXY= HTTPS_PROXY= ALL_PROXY= 2>/dev/null

    # 注释掉 bashrc 中的代理配置
    sed -i 's/^export \(http\|https\|all\)_proxy=/#DISABLED: export \1_proxy=/' ~/.bashrc 2>/dev/null

    touch "$PROXY_DISABLED_FILE"
    log "✅ 代理已禁用"
}

# ============================================
# 重启次数限制检测
# ============================================
can_restart() {
    local now=$(date +%s)
    local last_time=0
    local count=0

    [ -f "$TIME_FILE" ] && last_time=$(cat "$TIME_FILE")

    # 超过窗口时间，重置计数器
    if [ $((now - last_time)) -gt $RESTART_WINDOW ]; then
        count=0
        echo 0 > "$COUNT_FILE"
        echo $now > "$TIME_FILE"
        return 0
    fi

    [ -f "$COUNT_FILE" ] && count=$(cat "$COUNT_FILE")
    count=$((count + 1))
    echo $count > "$COUNT_FILE"
    echo $now > "$TIME_FILE"

    if [ $count -gt $MAX_RESTARTS ]; then
        log "❌ 已重启 ${count} 次仍异常，停止自动重启（窗口：${RESTART_WINDOW}s）"
        return 1
    fi

    log "⚠️ 重启尝试 ${count}/${MAX_RESTARTS}"
    return 0
}

# ============================================
# 重启 Gateway
# ============================================
restart_gateway() {
    log "=== 重启 Gateway ==="

    # 杀掉现有进程
    pkill -f "openclaw-gateway" 2>/dev/null

    sleep 3

    # 启动新进程（清除代理环境变量）
    nohup env -u http_proxy -u https_proxy -u all_proxy \
        -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY \
        openclaw gateway start > /tmp/openclaw_gateway.log 2>&1 &

    local new_pid=$!
    echo $new_pid > "$PID_FILE"

    log "启动完成，PID: $new_pid"

    sleep 10

    if is_process_alive; then
        log "✅ Gateway 启动成功"
    else
        log "❌ Gateway 启动失败"
    fi
}

# ============================================
# 主检测逻辑
# ============================================
main_check() {
    log "=== 检测开始 ==="

    # 检测各通道状态
    check_feishu_channel
    check_wecom_channel
    check_weixin_channel

    # 检查进程是否存活
    if ! is_process_alive; then
        log "⚠️ 进程未运行"

        if ! check_network; then
            log "⚠️ 网络异常"
            [ ! -f "$PROXY_DISABLED_FILE" ] && disable_proxy
            check_network && log "✅ 网络恢复" || { log "❌ 网络无法恢复"; return; }
        fi

        can_restart && restart_gateway
        return
    fi

    # 检查 WebSocket 错误
    if has_ws_errors; then
        log "⚠️ 检测到 WebSocket 错误"

        if ! check_network; then
            log "⚠️ 网络异常"
            [ ! -f "$PROXY_DISABLED_FILE" ] && disable_proxy
            check_network && log "✅ 网络恢复" || { log "❌ 网络问题"; return; }
        fi

        can_restart && restart_gateway
        return
    fi

    log "✅ WebSocket 连接正常"

    # 报告通道状态
    if [ -f "$FEISHU_PAUSED_FILE" ]; then
        log "📌 飞书通道：暂停中"
    else
        log "📌 飞书通道：正常"
    fi

    if [ -f "$WECOM_PAUSED_FILE" ]; then
        log "📌 企业微信通道：暂停中"
    else
        log "📌 企业微信通道：正常"
    fi

    if [ -f "$WEIXIN_PAUSED_FILE" ]; then
        log "📌 微信通道：暂停中（session 过期，等 60 分钟自动恢复）"
    else
        log "📌 微信通道：正常"
    fi
}

# ============================================
# 启动看门狗
# ============================================
main() {
    local interval="${1:-300}"

    log "看门狗启动，PID: $$，检测间隔: ${interval}s"
    log "日志文件: $LOG_FILE"

    while true; do
        main_check
        sleep "$interval"
    done
}

# 直接运行
main "$@"
