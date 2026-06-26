#!/bin/bash
set -euo pipefail

# OpenClaw 加密备份脚本
# 用途：创建 AES-256 加密的备份文件

BACKUP_ROOT="${OPENCLAW_BACKUP_DIR:-$HOME/Desktop/OpenClaw_Backups}"
DATE_STR="$(date +"%Y-%m-%d_%H-%M-%S")"
TMP_DIR="/tmp/openclaw_backup_$DATE_STR"
ARCHIVE_NAME="openclaw_backup_$DATE_STR.tar.gz"
ENCRYPTED_NAME="openclaw_backup_$DATE_STR.tar.gz.enc"

STATE_DIR_NEW="$HOME/.openclaw"
STATE_DIR_OLD="$HOME/.clawdbot"

mkdir -p "$BACKUP_ROOT"
mkdir -p "$TMP_DIR"

echo "🐈‍⬛ OpenClaw 加密备份开始..."

# 检查密码
if [ -z "${OPENCLAW_BACKUP_PASSWORD:-}" ]; then
    echo "请输入备份密码（至少8位）:"
    read -s BACKUP_PASSWORD
    echo ""
    echo "请再次输入密码:"
    read -s BACKUP_PASSWORD_CONFIRM
    echo ""
    
    if [ "$BACKUP_PASSWORD" != "$BACKUP_PASSWORD_CONFIRM" ]; then
        echo "❌ 密码不匹配"
        exit 1
    fi
    
    if [ ${#BACKUP_PASSWORD} -lt 8 ]; then
        echo "❌ 密码至少8位"
        exit 1
    fi
else
    BACKUP_PASSWORD="$OPENCLAW_BACKUP_PASSWORD"
fi

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
    echo "❌ 未找到数据目录"
    rm -rf "$TMP_DIR"
    exit 1
fi

if command -v openclaw >/dev/null 2>&1; then
    echo "⏸  停止网关..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
fi

echo "📦 打包中..."
tar -czf "/tmp/$ARCHIVE_NAME" -C "$TMP_DIR" .

echo "🔐 加密中..."
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 \
    -in "/tmp/$ARCHIVE_NAME" \
    -out "$BACKUP_ROOT/$ENCRYPTED_NAME" \
    -pass pass:"$BACKUP_PASSWORD"

shasum -a 256 "$BACKUP_ROOT/$ENCRYPTED_NAME" > "$BACKUP_ROOT/$ENCRYPTED_NAME.sha256"

rm -f "/tmp/$ARCHIVE_NAME"
rm -rf "$TMP_DIR"

if command -v openclaw >/dev/null 2>&1; then
    echo "▶️  重启网关..."
    openclaw gateway start 2>/dev/null || true
fi

echo ""
echo "✅ 加密备份完成！"
echo "📁 位置: $BACKUP_ROOT/$ENCRYPTED_NAME"
echo "🔐 校验: $BACKUP_ROOT/$ENCRYPTED_NAME.sha256"
echo ""
echo "⚠️  请妥善保管密码！丢失密码将无法恢复数据。"
echo ""
echo "解密方法："
echo "openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 \\"
echo "  -in $ENCRYPTED_NAME \\"
echo "  -out openclaw_backup.tar.gz \\"
echo "  -pass pass:YOUR_PASSWORD"
