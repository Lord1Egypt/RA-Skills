#!/bin/bash
# OpenClaw 自救系统安装脚本
# 由主人运行，完成最后的配置

echo "=== OpenClaw 自救系统安装 ==="
echo ""

# 1. 创建必要的目录
echo "[1/4] 创建备份目录..."
mkdir -p "$HOME/.openclaw/backups"
mkdir -p "$HOME/.openclaw/logs"

# 2. 复制保底配置
echo "[2/4] 安装保底配置..."
cp "$HOME/.openclaw/workspace/scripts/safe-mode-config.json" "$HOME/.openclaw/safe-mode.json"

# 3. 创建首次备份
echo "[3/4] 创建首次备份..."
"$HOME/.openclaw/workspace/scripts/backup-config.sh"

# 4. 设置定时任务
echo "[4/4] 设置定时任务..."
CRON_JOB="*/5 * * * * $HOME/.openclaw/workspace/scripts/health-monitor.sh"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "health-monitor.sh"; then
    echo "定时任务已存在，跳过"
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "定时任务已添加: 每5分钟检查一次"
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "功能说明:"
echo "- 每5分钟自动检查 OpenClaw 运行状态"
echo "- 崩溃时自动尝试回滚到最近的有效备份"
echo "- 保留最近20个配置备份"
echo "- 所有备份失败时使用保底配置启动"
echo ""
echo "日志位置: $HOME/.openclaw/logs/recovery.log"
echo "备份位置: $HOME/.openclaw/backups/"
echo ""
echo "如需手动备份配置，运行:"
echo "  $HOME/.openclaw/workspace/scripts/backup-config.sh"
