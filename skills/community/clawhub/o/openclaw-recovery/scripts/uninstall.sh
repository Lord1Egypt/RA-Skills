#!/bin/bash
# OpenClaw 自救系统卸载脚本（跨平台）

set -e

echo "=== OpenClaw 自救系统卸载 ==="
echo ""

INSTALL_DIR="$HOME/.openclaw/workspace/skills/openclaw-recovery"

# 检测 OS
case "$(uname -s)" in
    Darwin*)  OS="macos" ;;
    Linux*)   OS="linux" ;;
    MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
    *)        OS="unknown" ;;
esac

echo "[系统] $OS"

# 移除 cron（macOS/Linux）
case "$OS" in
    macos|linux)
        if crontab -l 2>/dev/null | grep -q "openclaw-recovery\\|recover.sh\\|backup.sh"; then
            crontab -l 2>/dev/null | grep -v "openclaw-recovery" | grep -v "recover.sh" | grep -v "backup.sh" | crontab - 2>/dev/null || true
            echo "✅ 已移除 cron 定时任务"
        fi
        ;;
    windows)
        echo "  如有定时任务，请在「任务计划程序」中手动删除 OpenClaw-Recovery"
        ;;
esac

# 停止可能运行的进程
pkill -f "smart-backup.sh watch" 2>/dev/null || true
pkill -f "recover.sh" 2>/dev/null || true
rm -f "$HOME/.openclaw/backup-watch.pid" 2>/dev/null || true
echo "✅ 已停止后台进程"

# 询问删除备份和日志
echo ""
read -p "是否删除备份文件和日志？(y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.openclaw/backups"
    rm -f "$HOME/.openclaw/logs/recovery.log"
    rm -f "$HOME/.openclaw/logs/recovery-history.log"
    rm -f "$HOME/.openclaw/logs/backup.log"
    rm -f "$HOME/.openclaw/logs/backup-watch.log"
    echo "✅ 已删除备份和日志"
else
    echo "📁 备份和日志已保留"
fi

# 保底配置
if [ -f "$HOME/.openclaw/safe-mode.json" ]; then
    read -p "是否删除保底配置 (safe-mode.json)？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f "$HOME/.openclaw/safe-mode.json"
        echo "✅ 已删除"
    else
        echo "📁 已保留"
    fi
fi

echo ""
echo "=== 卸载完成 ==="
echo "如需完全移除，可删除:"
echo "  rm -rf $INSTALL_DIR"
