---
name: openclaw-session-cleaner
description: OpenClaw 会话清理助手，自动清理旧会话文件、重建 sessions.json、解决文件膨胀问题
version: 1.0.1
author: openclaw
license: MIT
requires: []
tools: ["Bash"]
---

# OpenClaw Session Cleaner

## 触发指令
用户提及：清理OpenClaw会话、删除旧cron会话、压缩sessions.json、重建sessions.json、会话文件膨胀

## 自动执行流程（安全无风险）
1. **检查会话文件状态**
执行命令：统计会话文件数量 + 查看 sessions.json 大小
```bash
cd /home/ubuntu/.openclaw/agents/main/sessions/
echo "当前会话文件数量：$(ls -l *.jsonl 2>/dev/null | wc -l)"
echo "sessions.json 大小：$(du -h sessions.json 2>/dev/null | cut -f1)"