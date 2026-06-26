#!/bin/bash
# 配置 ControlMemory 定时同步任务
# 每 6 小时同步一次，如果 2 小时内有新记录则同步

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYNC_SCRIPT="$SCRIPT_DIR/clawhub_sync.py"

echo "╔════════════════════════════════════════╗"
echo "║   ControlMemory 定时任务配置           ║"
echo "╚════════════════════════════════════════╝"
echo ""

# 检查脚本是否存在
if [ ! -f "$SYNC_SCRIPT" ]; then
    echo "❌ 同步脚本不存在：$SYNC_SCRIPT"
    exit 1
fi

echo "📋 同步策略:"
echo "   - 每 6 小时自动同步一次"
echo "   - 如果超过 2 小时且有新记录，则同步"
echo ""

# 检测 crontab 是否已配置
existing_cron=$(crontab -l 2>/dev/null | grep "clawhub_sync.py" || true)

if [ -n "$existing_cron" ]; then
    echo "⚠️  已存在定时任务:"
    echo "   $existing_cron"
    echo ""
    read -p "是否重新配置？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "已取消"
        exit 0
    fi
    
    # 删除旧任务
    crontab -l 2>/dev/null | grep -v "clawhub_sync.py" | crontab -
    echo "✅ 已删除旧任务"
fi

# 添加新任务（每 6 小时：0:00, 6:00, 12:00, 18:00）
echo ""
echo "📝 添加新定时任务..."

# 获取当前 crontab
current_crontab=$(crontab -l 2>/dev/null || echo "")

# 添加新任务
new_crontab="$current_crontab
# ControlMemory 同步 - 每 6 小时
0 0,6,12,18 * * * cd $SCRIPT_DIR && /usr/bin/python3 $SYNC_SCRIPT >> $SCRIPT_DIR/sync.log 2>&1
"

# 设置 crontab
echo "$new_crontab" | crontab -

echo ""
echo "✅ 定时任务配置完成！"
echo ""
echo "📋 任务详情:"
echo "   - 执行时间：每天 0:00, 6:00, 12:00, 18:00"
echo "   - 智能检测：2 小时内有新记录则同步"
echo "   - 日志文件：$SCRIPT_DIR/sync.log"
echo ""
echo "🔍 查看任务:"
echo "   crontab -l"
echo ""
echo "📊 查看日志:"
echo "   tail -f $SCRIPT_DIR/sync.log"
echo ""
echo "🗑️  删除任务:"
echo "   crontab -l | grep -v clawhub_sync.py | crontab -"
echo ""
