#!/bin/sh
# 一个完整周期：抓取 → 检测提醒 → 发送提醒。
# 任何调度器（cron / systemd timer / CI / Agent 平台定时任务）都可调用本脚本。
# 设计为幂等、可重复执行，建议每 30 分钟一次（见 config.general.expected_run_interval_minutes）。
set -eu

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_ROOT"

python3 scripts/fetch.py
python3 scripts/alert_manager.py detect
python3 scripts/notify.py send alerts
