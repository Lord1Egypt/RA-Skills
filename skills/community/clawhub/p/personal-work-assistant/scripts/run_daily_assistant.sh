#!/bin/bash
# 个人工作助理流水线执行入口
# - 工作日 10:00 自动执行（由系统 crontab 触发）
# - 自动跳过周末与中国法定节假日（含调休）
# - 互斥锁保护（防重复运行）

DIR="/home/admin/.openclaw/workspace/skills/personal-work-assistant"
LOG="$DIR/data/cron.log"

mkdir -p "$DIR/data"

echo "========================================" >> "$LOG"
echo "$(date '+%Y-%m-%d %H:%M:%S') 个人工作助理任务触发" >> "$LOG"

cd "$DIR" || { echo "❌ 目录切换失败" >> "$LOG"; exit 1; }

# ========== 互斥检查 ==========
LOCK_FILE="/tmp/personal_assistant.lock"
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "⚠️ 任务已在运行 (PID: $PID)，跳过本次执行" >> "$LOG"
        exit 0
    fi
fi
echo $$ > "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

# ========== 非工作日检查 ==========
DAY_OF_WEEK=$(date +%w)
if [ "$DAY_OF_WEEK" = "0" ] || [ "$DAY_OF_WEEK" = "6" ]; then
    echo "📅 周末跳过（周${DAY_OF_WEEK}）" >> "$LOG"
    exit 0
fi

if command -v python3 &>/dev/null; then
    IS_WORKDAY=$(python3 -c "
import sys
try:
    import chinese_calendar
    from datetime import date
    today = date.today()
    if chinese_calendar.is_holiday(today):
        print('HOLIDAY')
    else:
        print('WORKDAY')
except Exception as e:
    print('CHECK_ERROR:' + str(e), file=sys.stderr)
    print('WORKDAY')
" 2>&1)

    if [ "$IS_WORKDAY" = "HOLIDAY" ]; then
        echo "📅 法定节假日跳过" >> "$LOG"
        exit 0
    fi
fi

# ========== 执行流水线 ==========
echo "🚀 开始执行流水线..." >> "$LOG"
python3 scripts/run_pipeline.py >> "$LOG" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 执行成功 $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG"
else
    echo "❌ 执行失败，exit code: $EXIT_CODE" >> "$LOG"
fi

exit $EXIT_CODE
