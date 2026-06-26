#!/bin/bash
set -euo pipefail

# OpenClaw 定时备份配置

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="${OPENCLAW_BACKUP_SCRIPT:-$SCRIPT_DIR/backup_encrypted.sh}"

echo "🐈‍⬛ 配置 OpenClaw 定时备份"
echo ""
echo "选择备份频率："
echo "1. 每天 23:00"
echo "2. 每周日 21:00"
echo "3. 每月1日 20:00"
echo "4. 自定义"
echo ""
read -p "请选择 [1-4]: " CHOICE

case $CHOICE in
    1)
        CRON_EXPR="0 23 * * *"
        DESC="每天 23:00"
        ;;
    2)
        CRON_EXPR="0 21 * * 0"
        DESC="每周日 21:00"
        ;;
    3)
        CRON_EXPR="0 20 1 * *"
        DESC="每月1日 20:00"
        ;;
    4)
        echo "请输入 cron 表达式（如 '0 2 * * *' 代表每天凌晨2点）:"
        read -p "> " CRON_EXPR
        DESC="自定义: $CRON_EXPR"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

if crontab -l 2>/dev/null | grep -q "openclaw.*backup"; then
    echo ""
    echo "⚠️  发现已有 OpenClaw 备份任务，是否覆盖？[y/N]"
    read -p "> " CONFIRM
    if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
        echo "取消操作"
        exit 0
    fi
    
    crontab -l 2>/dev/null | grep -v "openclaw.*backup" | crontab -
fi

(crontab -l 2>/dev/null; echo "$CRON_EXPR $BACKUP_SCRIPT >> /tmp/openclaw_backup.log 2>&1") | crontab -

echo ""
echo "✅ 定时备份已配置"
echo "📅 频率: $DESC"
echo "📜 脚本: $BACKUP_SCRIPT"
echo ""
echo "查看所有定时任务: crontab -l"
echo "查看备份日志: tail -f /tmp/openclaw_backup.log"
