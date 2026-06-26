#!/bin/bash
# OpenClaw 看门狗程序
# 功能：
# 1. 每次修改 openclaw.json 前自动备份上一次成功的配置
# 2. 每分钟检查 gateway 状态，宕机时自动恢复并重启

set -e

CONFIG_DIR="/root/.openclaw"
CONFIG_FILE="$CONFIG_DIR/openclaw.json"
BACKUP_DIR="$CONFIG_DIR/backups"
LOG_FILE="$CONFIG_DIR/watchdog.log"
MAX_BACKUPS=5

# 初始化
mkdir -p "$BACKUP_DIR"
touch "$LOG_FILE"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 备份当前配置（在修改前调用）
backup_config() {
    if [ -f "$CONFIG_FILE" ]; then
        local timestamp=$(date '+%Y%m%d_%H%M%S')
        local backup_file="$BACKUP_DIR/openclaw.${timestamp}.json"
        cp "$CONFIG_FILE" "$backup_file"
        log "备份完成：$backup_file"
        
        # 清理旧备份，保留最近 MAX_BACKUPS 个
        ls -t "$BACKUP_DIR"/openclaw.*.json 2>/dev/null | tail -n +$((MAX_BACKUPS + 1)) | xargs -r rm
        log "旧备份已清理，保留最近 $MAX_BACKUPS 个"
    fi
}

# 检查 gateway 状态
check_gateway() {
    if command -v openclaw &> /dev/null; then
        openclaw gateway status &> /dev/null
        return $?
    else
        log "错误：openclaw 命令未找到"
        return 1
    fi
}

# 恢复配置并重启 gateway
recover_and_restart() {
    log "检测到 gateway 宕机，开始恢复..."
    
    # 找到最新的备份
    local latest_backup=$(ls -t "$BACKUP_DIR"/openclaw.*.json 2>/dev/null | head -1)
    
    if [ -z "$latest_backup" ]; then
        log "错误：未找到备份文件"
        return 1
    fi
    
    log "使用备份：$latest_backup"
    
    # 停止 gateway
    openclaw gateway stop 2>/dev/null || true
    sleep 2
    
    # 恢复配置
    cp "$latest_backup" "$CONFIG_FILE"
    log "配置已恢复"
    
    # 重启 gateway
    openclaw gateway start
    if [ $? -eq 0 ]; then
        log "gateway 重启成功"
        return 0
    else
        log "错误：gateway 重启失败"
        return 1
    fi
}

# 包装 openclaw 命令，在修改配置前自动备份
wrap_openclaw() {
    # 这些命令可能会修改配置
    local modify_commands="wizard|config|auth|models|acp|gateway"
    
    if echo "$@" | grep -qE "$modify_commands"; then
        backup_config
    fi
    
    # 执行原始命令
    command openclaw "$@"
}

# 主循环 - 每分钟检查
monitor_loop() {
    log "看门狗启动"
    
    while true; do
        if ! check_gateway; then
            log "警告：gateway 无响应"
            sleep 5
            
            # 再次确认
            if ! check_gateway; then
                recover_and_restart
            fi
        fi
        
        sleep 60
    done
}

# 命令行接口
case "${1:-monitor}" in
    backup)
        backup_config
        ;;
    check)
        if check_gateway; then
            echo "gateway 运行正常"
            exit 0
        else
            echo "gateway 无响应"
            exit 1
        fi
        ;;
    recover)
        recover_and_restart
        ;;
    monitor)
        monitor_loop
        ;;
    wrap)
        shift
        wrap_openclaw "$@"
        ;;
    *)
        echo "用法：$0 {backup|check|recover|monitor|wrap <command>}"
        echo ""
        echo "  backup   - 手动备份当前配置"
        echo "  check    - 检查 gateway 状态"
        echo "  recover  - 从备份恢复并重启"
        echo "  monitor  - 持续监控（默认）"
        echo "  wrap     - 包装 openclaw 命令，自动备份"
        exit 1
        ;;
esac
