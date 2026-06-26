#!/bin/bash
# Lobster Guardian Terminator
# 核心逻辑：一条指令彻底卸载守护进程，停止监控，清理日志与残留，防止误触导致重启

echo "🦞 [LOBSTER-TERMINATOR] 正在执行全量清理指令脉冲..."

# 1. 卸载 LaunchAgent (停止系统级常驻)
launchctl unload ~/Library/LaunchAgents/ai.openclaw.lobster.guardian.plist 2>/dev/null
rm -f ~/Library/LaunchAgents/ai.openclaw.lobster.guardian.plist

# 2. 强制杀死正在运行的脚本进程与心跳检测循环
pkill -f "lobster-guardian.sh"
pkill -f "ai.openclaw.lobster.guardian"

# 3. 清理缓存日志与诊断文件
rm -f "$HOME/.openclaw/lobster-guardian.log"
rm -f "$HOME/.openclaw/lobster-guardian-stdout.log"
rm -f "$HOME/.openclaw/lobster-guardian-stderr.log"

echo "✅ [LOBSTER-TERMINATOR] 全量清理完成。守护进程已停止，LaunchAgent 已注销，缓存已排空。🦞"
