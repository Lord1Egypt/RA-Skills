#!/bin/bash
# Claude Code 任务脚本 - optimize_web_components
# 生成时间: 2026-04-03T10:17:41.221574

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: optimize_web_components"
echo "提示: 请优化 /Users/mars/.openclaw/workspace/claude-code-source/web/components/layout/ 目录下的组件文件：

1. ChatHist..."
echo ""

# 执行 Claude Code
claude -p "请优化 /Users/mars/.openclaw/workspace/claude-code-source/web/components/layout/ 目录下的组件文件：

1. ChatHistory.tsx - 添加聊天历史功能，支持显示会话列表
2. FileExplorer.tsx - 添加文件浏览功能，支持目录树结构  
3. QuickActions.tsx - 添加实际的快速操作功能

使用现有的 Claude Code 组件库和样式，保持代码风格一致。
确保组件能够正常工作并集成到现有布局中。" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/optimize_web_components.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/optimize_web_components.json"

echo "✅ 任务完成: optimize_web_components"
