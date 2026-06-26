#!/bin/bash
# 简报系统定时任务配置脚本

# 确保 download 目录存在
mkdir -p ~/my-project/download

# 输出配置说明
echo "=========================================="
echo "简报系统定时任务配置"
echo "=========================================="
echo ""
echo "需要在 OpenClaw 中手动创建以下三个 cron 任务："
echo ""
echo "1. 早间简报 - 每天 07:00"
echo "   名称: intel-briefing-morning"
echo "   表达式: 0 7 * * *"
echo "   Prompt 文件: ~/.openclaw/workspace/skills/intel-briefing/references/cron-morning.md"
echo ""
echo "2. 午间简报 - 每天 12:00"
echo "   名称: intel-briefing-noon"
echo "   表达式: 0 12 * * *"
echo "   Prompt 文件: ~/.openclaw/workspace/skills/intel-briefing/references/cron-noon.md"
echo ""
echo "3. 晚间简报 - 每天 19:00"
echo "   名称: intel-briefing-evening"
echo "   表达式: 0 19 * * *"
echo "   Prompt 文件: ~/.openclaw/workspace/skills/intel-briefing/references/cron-evening.md"
echo ""
echo "=========================================="
echo "创建命令示例:"
echo "openclaw cron create --name intel-briefing-morning --schedule '0 7 * * *' --prompt-file ~/.openclaw/workspace/skills/intel-briefing/references/cron-morning.md"
echo "=========================================="
