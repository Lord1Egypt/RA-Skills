#!/bin/bash
# Claude Code 任务脚本 - fix_web_ui_full_access
# 生成时间: 2026-04-03T10:25:29.096160

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: fix_web_ui_full_access"
echo "提示: 你现在有完全的文件系统访问权限。请修复 /Users/mars/.openclaw/workspace/claude-code-source/web/ 目录下的 Web UI 使其能够正常运行。

具..."
echo ""

# 执行 Claude Code
claude -p "你现在有完全的文件系统访问权限。请修复 /Users/mars/.openclaw/workspace/claude-code-source/web/ 目录下的 Web UI 使其能够正常运行。

具体任务：
1. 检查所有缺失的组件文件
2. 创建或修复 ChatHistory.tsx, FileExplorer.tsx, QuickActions.tsx
3. 修复字体和样式问题  
4. 确保所有导入路径正确
5. 测试并验证 Web UI 能在 http://localhost:3000 正常访问

使用 --allowedTools \"Read,Edit,Bash\" 参数，你可以读取、编辑文件和执行 shell 命令。
直接修改文件并启动服务器验证修复效果。" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_web_ui_full_access.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_web_ui_full_access.json"

echo "✅ 任务完成: fix_web_ui_full_access"
