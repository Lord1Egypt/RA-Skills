#!/bin/bash
set -euo pipefail

# OpenClaw 恢复脚本（普通备份）

if [ $# -lt 1 ]; then
    echo "用法: $0 /path/to/openclaw_backup_xxx.tar.gz"
    exit 1
fi

ARCHIVE="$1"
RESTORE_TMP="/tmp/openclaw_restore_$(date +"%Y-%m-%d_%H-%M-%S")"

if [ ! -f "$ARCHIVE" ]; then
    echo "❌ 备份文件不存在: $ARCHIVE"
    exit 1
fi

if [ -f "$ARCHIVE.sha256" ]; then
    echo "🔐 验证备份完整性..."
    if ! shasum -c "$ARCHIVE.sha256"; then
        echo "❌ 校验失败！备份文件可能已损坏。"
        echo "是否仍要继续？[y/N]"
        read -p "> " CONFIRM
        if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
            exit 1
        fi
    fi
    echo "✓ 校验通过"
fi

mkdir -p "$RESTORE_TMP"

echo "📦 解压备份文件..."
tar -xzf "$ARCHIVE" -C "$RESTORE_TMP"

echo "🐈‍⬛ 开始恢复..."

if command -v openclaw >/dev/null 2>&1; then
    echo "⏸  停止 OpenClaw 网关..."
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
    echo "▶️  重启 OpenClaw 网关..."
    openclaw gateway restart || true
    sleep 3
    openclaw status || true
fi

echo ""
echo "✅ 恢复完成！"
echo ""
echo "建议立即测试："
echo "1. OpenClaw 是否能正常启动"
echo "2. 记忆是否还在"
echo "3. 渠道登录状态是否保留"
echo "4. API 配置是否正常"
echo ""
if [ -n "${BACKUP_OLD:-}" ]; then
    echo "旧数据已备份到: $BACKUP_OLD"
    echo "确认恢复成功后可删除: rm -rf $BACKUP_OLD"
fi
