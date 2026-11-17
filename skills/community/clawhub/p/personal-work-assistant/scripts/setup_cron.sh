#!/bin/bash
# 自动挂载工作日定时任务
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_PATH="$DIR/scripts/run_daily_assistant.sh"

chmod +x "$SCRIPT_PATH"

CRON_JOB="0 10 * * 1-5 $SCRIPT_PATH > /dev/null 2>&1"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -Fq "$SCRIPT_PATH"; then
    echo "⚠️ 定时任务已存在，无需重复添加。"
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ 已成功添加工作日 10:00 定时晨报任务 (Crontab)！"
fi
