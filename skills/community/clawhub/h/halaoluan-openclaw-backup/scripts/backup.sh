#!/bin/bash
set -euo pipefail

# OpenClaw 备份脚本（无加密版）
# 用途：快速备份 ~/.openclaw 数据

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"
DATE_STR="$(date +"%Y-%m-%d_%H-%M-%S")"
TMP_DIR="/tmp/openclaw_backup_$DATE_STR"
ARCHIVE_NAME="openclaw_backup_$DATE_STR.tar.gz"

STATE_DIR_NEW="$HOME/.openclaw"
STATE_DIR_OLD="$HOME/.clawdbot"

mkdir -p "$BACKUP_ROOT"
mkdir -p "$TMP_DIR"

echo "🐈‍⬛ OpenClaw 备份开始..."
echo "备份目标: $BACKUP_ROOT"

FOUND_ANY=0

if [ -d "$STATE_DIR_NEW" ]; then
    echo "✓ 发现: $STATE_DIR_NEW"
    cp -a "$STATE_DIR_NEW" "$TMP_DIR/"
    FOUND_ANY=1
fi

if [ -d "$STATE_DIR_OLD" ]; then
    echo "✓ 发现: $STATE_DIR_OLD"
    cp -a "$STATE_DIR_OLD" "$TMP_DIR/"
    FOUND_ANY=1
fi

if [ "$FOUND_ANY" -eq 0 ]; then
    echo "❌ 未找到 OpenClaw 数据目录"
    rm -rf "$TMP_DIR"
    exit 1
fi

if command -v openclaw >/dev/null 2>&1; then
    echo "⏸  停止 OpenClaw 网关..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
fi

echo "📦 打包中..."
tar -czf "$BACKUP_ROOT/$ARCHIVE_NAME" -C "$TMP_DIR" .

echo "🔐 生成 SHA256 校验..."
shasum -a 256 "$BACKUP_ROOT/$ARCHIVE_NAME" > "$BACKUP_ROOT/$ARCHIVE_NAME.sha256"

rm -rf "$TMP_DIR"

if command -v openclaw >/dev/null 2>&1; then
    echo "▶️  重启 OpenClaw 网关..."
    openclaw gateway start 2>/dev/null || true
fi

echo ""
echo "✅ 备份完成！"
echo "📁 位置: $BACKUP_ROOT/$ARCHIVE_NAME"
echo "🔐 校验: $BACKUP_ROOT/$ARCHIVE_NAME.sha256"
echo ""
echo "建议操作："
echo "1. 复制到移动硬盘"
echo "2. 上传到云盘（建议加密）"
echo "3. 定期验证备份完整性"
