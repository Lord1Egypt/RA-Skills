#!/bin/bash
set -euo pipefail

# OpenClaw 恢复脚本（加密备份）

if [ $# -lt 1 ]; then
    echo "用法: $0 /path/to/openclaw_backup_xxx.tar.gz.enc"
    exit 1
fi

ENCRYPTED_ARCHIVE="$1"
RESTORE_TMP="/tmp/openclaw_restore_$(date +"%Y-%m-%d_%H-%M-%S")"
DECRYPTED_ARCHIVE="$RESTORE_TMP/backup.tar.gz"

if [ ! -f "$ENCRYPTED_ARCHIVE" ]; then
    echo "❌ 加密备份不存在: $ENCRYPTED_ARCHIVE"
    exit 1
fi

if [ -f "$ENCRYPTED_ARCHIVE.sha256" ]; then
    echo "🔐 验证备份完整性..."
    if ! shasum -c "$ENCRYPTED_ARCHIVE.sha256"; then
        echo "❌ 校验失败！"
        exit 1
    fi
    echo "✓ 校验通过"
fi

mkdir -p "$RESTORE_TMP"

if [ -z "${OPENCLAW_BACKUP_PASSWORD:-}" ]; then
    echo "请输入备份密码:"
    read -s BACKUP_PASSWORD
    echo ""
else
    BACKUP_PASSWORD="$OPENCLAW_BACKUP_PASSWORD"
fi

echo "🔓 解密中..."
if ! openssl enc -aes-256-cbc -d -pbkdf2 -iter 100000 \
    -in "$ENCRYPTED_ARCHIVE" \
    -out "$DECRYPTED_ARCHIVE" \
    -pass pass:"$BACKUP_PASSWORD"; then
    echo "❌ 解密失败！密码错误或文件已损坏。"
    rm -rf "$RESTORE_TMP"
    exit 1
fi

echo "✓ 解密成功"

echo "📦 解压备份..."
tar -xzf "$DECRYPTED_ARCHIVE" -C "$RESTORE_TMP"

echo "🐈‍⬛ 开始恢复..."

if command -v openclaw >/dev/null 2>&1; then
    echo "⏸  停止网关..."
    openclaw gateway stop 2>/dev/null || true
    sleep 2
fi

if [ -d "$HOME/.openclaw" ]; then
    BACKUP_OLD="$HOME/.openclaw.backup.$(date +"%Y%m%d_%H%M%S")"
    echo "💾 备份当前数据到: $BACKUP_OLD"
    mv "$HOME/.openclaw" "$BACKUP_OLD"
fi

if [ -d "$RESTORE_TMP/.openclaw" ]; then
    cp -a "$RESTORE_TMP/.openclaw" "$HOME/"
    echo "✓ 已恢复: ~/.openclaw"
fi

if [ -d "$RESTORE_TMP/.clawdbot" ]; then
    cp -a "$RESTORE_TMP/.clawdbot" "$HOME/"
    echo "✓ 已恢复: ~/.clawdbot"
fi

rm -rf "$RESTORE_TMP"

if command -v openclaw >/dev/null 2>&1; then
    echo "🔧 执行修复检查..."
    openclaw doctor || true
    echo "▶️  重启网关..."
    openclaw gateway restart || true
    sleep 3
    openclaw status || true
fi

echo ""
echo "✅ 恢复完成！"
echo ""
if [ -n "${BACKUP_OLD:-}" ]; then
    echo "旧数据已备份到: $BACKUP_OLD"
    echo "确认恢复成功后可删除: rm -rf $BACKUP_OLD"
fi
