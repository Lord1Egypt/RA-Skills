#!/bin/bash
# daily-task-tracker: 每日任务追踪系统 — Cron 配置输出脚本
# 运行此脚本输出需要添加到 openclaw.json 的 crons 配置段
# 将输出内容复制到 openclaw.json 的 "crons" 数组中

cat << 'CONFIG'
[
  {
    "name": "daily-task-morning",
    "schedule": "0 9 * * *",
    "channel": "feishu",
    "prompt": "现在是早上9点，请根据 daily-task-tracker skill 中定义的早间流程，询问用户今天的任务，并写入 tasks/YYYY-MM-DD.md 文件。"
  },
  {
    "name": "daily-task-noon",
    "schedule": "0 12 * * *",
    "channel": "feishu",
    "prompt": "现在是中午12点，请根据 daily-task-tracker skill 中定义的午间跟进流程，检查今天的任务进度，询问用户哪些已完成、哪些有困难。"
  },
  {
    "name": "daily-task-evening",
    "schedule": "0 18 * * *",
    "channel": "feishu",
    "prompt": "现在是下午6点，请根据 daily-task-tracker skill 中定义的晚间总结流程，汇总今天的完成情况，让用户确认后将未完成任务滚动到明天的文件。"
  }
]
CONFIG
