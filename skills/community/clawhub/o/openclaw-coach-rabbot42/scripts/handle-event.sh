#!/bin/bash
# OpenClaw 系统事件处理脚本

EVENT="$1"

case "$EVENT" in
    "sync")
        ~/.openclaw/skills/openclaw-coach/scripts/sync-docs.sh
        ;;
    "pick-tip")
        ~/.openclaw/skills/openclaw-coach/scripts/pick-daily-tip.sh
        ;;
    "send-tip")
        ~/.openclaw/skills/openclaw-coach/scripts/send-daily-tip.sh
        ;;
    *)
        echo "未知事件: $EVENT"
        ;;
esac
