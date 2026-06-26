#!/bin/bash
# 心情周报定时发送脚本
# 每周日早上 9:00 执行

cd /home/loong/.openclaw/workspace

# 生成周报
REPORT=$(python3 ~/.openclaw/workspace/skills/mood-logger/scripts/weekly_mood_report.py 2>/dev/null)

# 发送到微信（通过 OpenClaw 消息系统）
# 注意：需要配置 webhook 或消息代理
echo "$REPORT" > /tmp/weekly_mood_report.txt

# 输出生成的报告
cat /tmp/weekly_mood_report.txt
