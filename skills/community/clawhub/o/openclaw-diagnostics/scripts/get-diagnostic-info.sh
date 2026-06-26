#!/bin/bash
# OpenClaw Doctor Pro - 获取诊断信息
# 用法: ./get-diagnostic-info.sh [config|logs|all]

CONFIG_PATH="$HOME/.openclaw/openclaw.json"
LOG_LINES=100

get_config() {
    if [ -f "$CONFIG_PATH" ]; then
        echo "=== openclaw.json ==="
        cat "$CONFIG_PATH"
    else
        echo "❌ 配置文件不存在: $CONFIG_PATH"
    fi
}

get_logs() {
    echo "=== OpenClaw 日志 (最近 $LOG_LINES 行) ==="
    if command -v openclaw &> /dev/null; then
        openclaw logs -n $LOG_LINES 2>/dev/null || echo "❌ 无法获取日志（可能 OpenClaw 未运行）"
    else
        echo "❌ openclaw 命令不可用"
    fi
}

get_status() {
    echo "=== OpenClaw 状态 ==="
    if command -v openclaw &> /dev/null; then
        openclaw status 2>/dev/null || echo "❌ 无法获取状态"
    else
        echo "❌ openclaw 命令不可用"
    fi
}

case "${1:-all}" in
    config)
        get_config
        ;;
    logs)
        get_logs
        ;;
    status)
        get_status
        ;;
    all|*)
        get_config
        echo ""
        get_status
        echo ""
        get_logs
        ;;
esac
