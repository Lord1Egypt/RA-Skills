#!/bin/bash
# OpenClaw 网关启动包装脚本
# 功能：启动前自动清理端口冲突，防止 LaunchAgent 重启失败
# 用法：在 ai.openclaw.gateway.plist 的 ProgramArguments 中调用此脚本

set -euo pipefail

GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
LOCK_FILE="/tmp/openclaw-gateway.lock"
STALE_PID_FILE="$OPENCLAW_HOME/.gateway.pid"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

# ==================== 清理端口占用 ====================
cleanup_port() {
    local port="$1"
    local pids=""

    # 方法 1: lsof（macOS 推荐）
    if command -v lsof >/dev/null 2>&1; then
        pids=$(lsof -ti:"$port" 2>/dev/null || true)
    fi

    # 方法 2: netstat 备用
    if [ -z "$pids" ] && command -v netstat >/dev/null 2>&1; then
        pids=$(netstat -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d/ -f1 || true)
    fi

    # 方法 3: ss 备用
    if [ -z "$pids" ] && command -v ss >/dev/null 2>&1; then
        pids=$(ss -tlnp 2>/dev/null | grep ":$port " | grep -oP 'pid=\K[0-9]+' || true)
    fi

    if [ -n "$pids" ]; then
        log "发现端口 $port 被占用 (PID: $pids)，尝试清理..."
        for pid in $pids; do
            # 先发 SIGTERM，等待优雅退出
            if kill -0 "$pid" 2>/dev/null; then
                log "发送 SIGTERM 到 PID $pid"
                kill "$pid" 2>/dev/null || true
            fi
        done

        # 等待 5 秒，给进程足够的优雅退出时间
        sleep 5

        # 还没退出的发 SIGKILL
        for pid in $pids; do
            if kill -0 "$pid" 2>/dev/null; then
                log "PID $pid 未退出，发送 SIGKILL"
                kill -9 "$pid" 2>/dev/null || true
            fi
        done

        # 最后再确认一次
        sleep 1
        if command -v lsof >/dev/null 2>&1; then
            local remaining
            remaining=$(lsof -ti:"$port" 2>/dev/null || true)
            if [ -n "$remaining" ]; then
                log "警告: 端口 $port 仍被占用 (PID: $remaining)"
                return 1
            fi
        fi

        log "端口 $port 已清理"
    else
        log "端口 $port 空闲"
    fi

    return 0
}

# ==================== 清理锁文件 ====================
cleanup_locks() {
    # 清理 OpenClaw gateway lock
    if [ -f "$LOCK_FILE" ]; then
        local lock_pid
        lock_pid=$(cat "$LOCK_FILE" 2>/dev/null || true)
        if [ -n "$lock_pid" ] && ! kill -0 "$lock_pid" 2>/dev/null; then
            log "清理过期锁文件: $LOCK_FILE (PID $lock_pid 不存在)"
            rm -f "$LOCK_FILE"
        fi
    fi

    # 清理可能的其他 lock 文件
    for lock in /tmp/openclaw-gateway*.lock /tmp/openclaw*.lock; do
        [ -f "$lock" ] || continue
        local lock_pid
        lock_pid=$(cat "$lock" 2>/dev/null || true)
        if [ -n "$lock_pid" ] && ! kill -0 "$lock_pid" 2>/dev/null; then
            log "清理过期锁文件: $lock"
            rm -f "$lock"
        fi
    done
}

# ==================== 清理旧 PID 文件 ====================
cleanup_pid_file() {
    if [ -f "$STALE_PID_FILE" ]; then
        local old_pid
        old_pid=$(cat "$STALE_PID_FILE" 2>/dev/null || true)
        if [ -n "$old_pid" ] && ! kill -0 "$old_pid" 2>/dev/null; then
            log "清理过期 PID 文件: $STALE_PID_FILE"
            rm -f "$STALE_PID_FILE"
        fi
    fi
}

# ==================== 主函数 ====================
main() {
    log "========== OpenClaw 网关启动 =========="
    log "端口: $GATEWAY_PORT"
    log "工作目录: $OPENCLAW_HOME"

    # 步骤 1: 先用官方 stop 命令优雅关闭
    if command -v openclaw >/dev/null 2>&1; then
        log "执行 openclaw gateway stop..."
        openclaw gateway stop 2>/dev/null || true
        sleep 5
    fi

    # 步骤 2: 清理端口（兜底处理残留进程）
    cleanup_port "$GATEWAY_PORT" || {
        log "错误: 端口清理失败，无法启动"
        exit 1
    }

    # 步骤 3: 清理锁文件
    cleanup_locks

    # 步骤 4: 清理旧 PID 文件
    cleanup_pid_file

    # 步骤 5: 确保日志目录存在
    mkdir -p "$OPENCLAW_HOME/logs"

    # 步骤 6: 记录本次启动 PID
    echo $$ > "$STALE_PID_FILE" 2>/dev/null || true

    # 步骤 7: 启动网关（exec 替换当前进程）
    log "启动 OpenClaw Gateway..."
    log "========== 启动日志结束 =========="

    # 保留原始参数传递
    if [ $# -gt 0 ]; then
        exec "$@"
    else
        # 默认启动命令（注意：openclaw gateway start 不支持 --port 参数）
        # 端口通过 openclaw.json 或环境变量 OPENCLAW_GATEWAY_PORT 配置
        if command -v openclaw >/dev/null 2>&1; then
            exec openclaw gateway start
        else
            # 回退到直接调用 node
            local node_bin
            if command -v node >/dev/null 2>&1; then
                node_bin="node"
            elif [ -x "/opt/homebrew/opt/node@22/bin/node" ]; then
                node_bin="/opt/homebrew/opt/node@22/bin/node"
            else
                log "错误: 找不到 node"
                exit 1
            fi
            local openclaw_path
            openclaw_path=$(npm root -g 2>/dev/null)/openclaw/dist/index.js
            if [ ! -f "$openclaw_path" ]; then
                openclaw_path="/opt/homebrew/lib/node_modules/openclaw/dist/index.js"
            fi
            exec "$node_bin" "$openclaw_path" gateway --port "$GATEWAY_PORT"
        fi
    fi
}

main "$@"
