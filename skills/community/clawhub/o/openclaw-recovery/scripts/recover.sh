#!/bin/bash
# OpenClaw 健康监控与自动恢复脚本
# 每5分钟运行一次检查

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw/backups"
LOG_FILE="$HOME/.openclaw/logs/recovery.log"
SAFE_CONFIG="$HOME/.openclaw/safe-mode.json"
MAX_RETRIES=10

# 创建日志目录
mkdir -p "$HOME/.openclaw/logs"

# 检查 OpenClaw 是否运行
if pgrep -f "openclaw.*gateway" > /dev/null; then
    # 运行正常，退出
    exit 0
fi

echo "[$(date)] OpenClaw 未运行，开始恢复流程" >> "$LOG_FILE"

# 检查配置文件是否有效
if python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
    echo "[$(date)] 配置文件格式正确，尝试直接重启" >> "$LOG_FILE"
    openclaw gateway restart 2>&1 >> "$LOG_FILE"
    sleep 5
    
    if pgrep -f "openclaw.*gateway" > /dev/null; then
        echo "[$(date)] 重启成功" >> "$LOG_FILE"
        exit 0
    fi
fi

echo "[$(date)] 配置文件可能损坏，开始回滚" >> "$LOG_FILE"

# 尝试回滚到最近的备份
RETRY_COUNT=0
for BACKUP in $(ls -t "$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | head -$MAX_RETRIES); do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    
    # 验证备份文件是否有效
    if ! python3 -c "import json; json.load(open('$BACKUP'))" 2>/dev/null; then
        echo "[$(date)] 备份文件无效，跳过: $BACKUP" >> "$LOG_FILE"
        continue
    fi
    
    # 尝试回滚
    cp "$BACKUP" "$CONFIG_FILE"
    echo "[$(date)] 尝试回滚到: $BACKUP" >> "$LOG_FILE"
    
    # 测试启动
    if openclaw gateway start 2>&1 >> "$LOG_FILE"; then
        sleep 5
        if pgrep -f "openclaw.*gateway" > /dev/null; then
            echo "[$(date)] 回滚成功，使用备份: $BACKUP" >> "$LOG_FILE"
            exit 0
        fi
    fi
    
    echo "[$(date)] 回滚失败，尝试下一个备份" >> "$LOG_FILE"
done

# 所有备份都失败，使用保底配置
if [ -f "$SAFE_CONFIG" ]; then
    echo "[$(date)] 所有备份都失败，使用保底配置" >> "$LOG_FILE"
    cp "$SAFE_CONFIG" "$CONFIG_FILE"
    openclaw gateway start 2>&1 >> "$LOG_FILE"
    sleep 5
    
    if pgrep -f "openclaw.*gateway" > /dev/null; then
        echo "[$(date)] 保底配置启动成功" >> "$LOG_FILE"
        exit 0
    fi
fi

echo "[$(date)] 恢复失败，需要人工干预" >> "$LOG_FILE"
exit 1
