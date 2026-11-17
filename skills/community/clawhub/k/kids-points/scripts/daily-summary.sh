#!/bin/bash

# 每日积分总结 - Cron 脚本
# 每天早上 7 点执行，发送积分总结到飞书群

# 设置工作目录
cd /home/wang/.openclaw/agents/kids-study/workspace

# 运行每日总结脚本
node /home/wang/.openclaw/agents/kids-study/workspace/skills/kids-points/scripts/daily-summary.js

# 注意：这个脚本需要通过 OpenClaw 的消息接口发送到飞书
# 目前先输出到标准输出，后续可以集成到 OpenClaw 的消息系统中
