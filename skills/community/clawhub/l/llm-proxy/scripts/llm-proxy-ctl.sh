#!/bin/bash
# 协作者邮箱：394286006@qq.com
# LLM Proxy 启动脚本 v2 - 配置外部化

# 加载公共配置
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/llm-proxy-common.sh"
_ensure_config

PROXY_SCRIPT="$SCRIPT_DIR/llm-proxy.py"
PID_FILE="/tmp/llm-proxy.pid"
LOG_FILE="$LOG_DIR/ctl-service.log"


start() {
    # 检查是否已在运行
    if curl -s --max-time 3 "$PROXY_URL" > /dev/null 2>&1; then
        echo "✅ 代理已在运行"
        curl -s "$PROXY_URL" | python3 -m json.tool
        return 0
    fi

    # 清理残留进程
    kill_by_port "$PROXY_PORT" 2>/dev/null
    sleep 1

    echo "🚀 启动 LLM Proxy..."
    echo "📋 配置: $LISTEN_HOST:$PROXY_PORT"
    mkdir -p "$(dirname "$LOG_FILE")"

    # 后台启动
    python3 -u "$PROXY_SCRIPT" >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "✅ 代理 PID: $(cat "$PID_FILE")"

    sleep 3
    if curl -s --max-time 5 "$PROXY_URL" > /dev/null 2>&1; then
        echo "✅ 健康检查通过"
        curl -s "$PROXY_URL" | python3 -m json.tool
    else
        echo "⚠️ 启动可能失败，检查日志: $LOG_FILE"
    fi
}

kill_by_port() {
    local port=$1
    local pids
    pids=$(lsof -ti ":$port" 2>/dev/null)
    if [ -n "$pids" ]; then
        echo "🔍 发现占用端口 $port 的进程: $pids"
        for pid in $pids; do
            echo " → 终止 PID: $pid"
            kill -9 "$pid" 2>/dev/null
        done
        return 0
    fi
    return 1
}

is_port_in_use() {
    local port=$1
    lsof -ti ":$port" >/dev/null 2>&1
    return $?
}

wait_for_port_release() {
    local port=$1
    local max_attempts=${2:-15}
    local attempt=0

    echo "⏳ 等待端口 $port 释放..."
    while [ $attempt -lt $max_attempts ]; do
        if ! is_port_in_use "$port"; then
            echo "✅ 端口 $port 已释放"
            return 0
        fi
        attempt=$((attempt + 1))
        local wait_interval=$(( RANDOM % 5 + 2 ))
        echo " → 端口仍被占用 (尝试 $attempt/$max_attempts)，等待 ${wait_interval}s..."
        kill_by_port "$port" 2>/dev/null
        sleep $wait_interval
    done
    echo "❌ 端口 $port 释放超时"
    return 1
}

stop() {
    echo "🛑 停止 LLM Proxy..."

    # 通过 PID 文件停止
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        echo "🛑 停止守护进程 (PID: $pid)..."
        kill -9 -- -"$pid" 2>/dev/null || kill -9 "$pid" 2>/dev/null
        sleep 1
    fi

    # 清理端口进程
    echo "🧹 清理端口 $PROXY_PORT..."
    kill_by_port "$PROXY_PORT" 2>/dev/null
    sleep 2

    # 清理临时文件
    rm -f "$PID_FILE"
    rm -f /tmp/llm-proxy-wrapper.sh
    echo "✅ 已完全停止"
}

status() {
    if curl -s --max-time 2 "$PROXY_URL" > /dev/null 2>&1; then
        echo "✅ 代理运行中 ($LISTEN_HOST:$PROXY_PORT)"
        curl -s "$PROXY_URL" | python3 -m json.tool
    else
        echo "❌ 代理无响应"
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo "⚠️ 守护进程在运行 (PID: $(cat "$PID_FILE")), 但代理无响应"
        else
            echo "❌ 守护进程也未运行"
        fi
    fi
}

logs() {
    tail -f "$LOG_FILE"
}

case "$1" in
    start)   start ;;
    stop)    stop ;;
    restart) stop; sleep 1; start ;;
    status)  status ;;
    logs)    logs ;;
    *)       echo "用法: $0 {start|stop|restart|status|logs}" ;;
esac
