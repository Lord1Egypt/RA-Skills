#!/bin/bash
# 日报执行包装脚本
# 由 OpenClaw Cron 调用

cd /home/wang/.openclaw/agents/kids-study/workspace/skills/kids-points
node scripts/daily-report.js >> /home/wang/.openclaw/agents/kids-study/workspace/kids-points/logs/daily-cron.log 2>&1
