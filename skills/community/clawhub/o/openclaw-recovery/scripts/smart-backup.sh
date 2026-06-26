#!/bin/bash
# OpenClaw 智能备份系统 v2.1
# 功能：1.监控文件变化自动备份 2.每日凌晨自动备份
# 更新：适配 OpenClaw 2026.4.x，auth 文件路径已更新

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
AUTH_FILE="$HOME/.openclaw/agents/main/agent/auth-profiles.json"
AUTH_STATE="$HOME/.openclaw/agents/main/agent/auth-state.json"
BACKUP_DIR="$HOME/.openclaw/backups"
LOG_FILE="$HOME/.openclaw/logs/backup.log"

# 创建目录
mkdir -p "$BACKUP_DIR" "$HOME/.openclaw/logs"

# 备份函数
backup_config() {
    local reason="$1"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    # 备份 openclaw.json
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "$BACKUP_DIR/openclaw.json.bak.$timestamp"
        echo "[$(date)] 备份 openclaw.json - 原因: $reason" >> "$LOG_FILE"
    fi
    
    # 备份 auth-profiles.json (API Keys)
    if [ -f "$AUTH_FILE" ]; then
        cp "$AUTH_FILE" "$BACKUP_DIR/auth-profiles.json.bak.$timestamp"
        echo "[$(date)] 备份 auth-profiles.json - 原因: $reason" >> "$LOG_FILE"
    fi
    
    # 备份 auth-state.json
    if [ -f "$AUTH_STATE" ]; then
        cp "$AUTH_STATE" "$BACKUP_DIR/auth-state.json.bak.$timestamp"
        echo "[$(date)] 备份 auth-state.json - 原因: $reason" >> "$LOG_FILE"
    fi
    
    # 清理旧备份：保留最近20个 + 每天最新1个（保留7天）
    cleanup_backups
}

# 清理备份函数
cleanup_backups() {
    # 保留最近20个
    ls -t "$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null
    ls -t "$BACKUP_DIR"/auth-profiles.json.bak.* 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null
    ls -t "$BACKUP_DIR"/auth-state.json.bak.* 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null
    
    # 删除7天前的备份（保留每天最新的一个）
    find "$BACKUP_DIR" -name "*.bak.*" -mtime +7 -type f -delete 2>/dev/null
}

# 检查是否需要每日备份
should_daily_backup() {
    local today=$(date +%Y%m%d)
    local last_daily=$(ls -t "$BACKUP_DIR"/openclaw.json.bak.${today}_* 2>/dev/null | head -1)
    
    if [ -z "$last_daily" ]; then
        return 0  # 需要备份
    else
        return 1  # 已备份
    fi
}

# 主逻辑
if [ "$1" == "daily" ]; then
    # 每日备份模式
    if should_daily_backup; then
        backup_config "每日自动备份"
    fi
elif [ "$1" == "watch" ]; then
    # 监控模式（需要 fswatch）
    if command -v fswatch >/dev/null 2>&1; then
        echo "开始监控配置文件变化..."
        fswatch -o "$CONFIG_FILE" "$AUTH_FILE" "$AUTH_STATE" 2>/dev/null | while read; do
            sleep 1  # 防抖
            backup_config "文件变化自动备份"
        done
    else
        echo "未安装 fswatch，请先安装: brew install fswatch"
        exit 1
    fi
else
    # 手动备份
    backup_config "手动备份"
    echo "备份完成！"
fi
