#!/bin/bash
# OpenClaw 配置备份脚本
# 在修改配置前运行，创建时间戳备份

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw/backups"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 生成时间戳备份文件名
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/openclaw.json.bak.$TIMESTAMP"

# 复制当前配置
cp "$CONFIG_FILE" "$BACKUP_FILE"

# 保留最近20个备份，删除旧的
ls -t "$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | tail -n +21 | xargs rm -f 2>/dev/null

echo "备份完成: $BACKUP_FILE"
