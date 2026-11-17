#!/bin/bash
# 每日积分日报自动生成脚本
# 添加到 crontab: 
#   0 0 * * *  - 0 点生成昨天的日报（最终版）
#   0 12 * * * - 中午 12 点更新今天的日报（可选）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/wang/.openclaw/agents/kids-study/workspace"
LOG_FILE="${WORKSPACE}/kids-points/logs/daily-report.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 获取当前小时
CURRENT_HOUR=$(date +%H)

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始生成积分日报..." >> "$LOG_FILE"

# 根据时间决定生成哪天的日报
if [ "$CURRENT_HOUR" -lt 6 ]; then
    # 凌晨 0-5 点：生成昨天的日报（最终版）
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🌙 凌晨时段，生成昨天的日报" >> "$LOG_FILE"
    TARGET="yesterday"
else
    # 6 点以后：生成今天的日报（白天可能会更新）
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ☀️ 白天时段，生成今天的日报" >> "$LOG_FILE"
    TARGET="today"
fi

# 生成日报
cd "$SCRIPT_DIR"
node generate-daily-report.js $TARGET >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 日报生成成功 ($TARGET)" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 日报生成失败 ($TARGET)" >> "$LOG_FILE"
fi
