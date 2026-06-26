#!/bin/bash
# Claude Code 任务脚本 - fix_web_ui_missing_files
# 生成时间: 2026-04-03T10:16:18.722594

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: fix_web_ui_missing_files"
echo "提示: 请修复 /Users/mars/.openclaw/workspace/claude-code-source/web/ 目录下的 Web UI 缺失文件问题。

具体缺失文件：
1. componen..."
echo ""

# 执行 Claude Code
claude -p "请修复 /Users/mars/.openclaw/workspace/claude-code-source/web/ 目录下的 Web UI 缺失文件问题。

具体缺失文件：
1. components/layout/ChatHistory.tsx
2. components/layout/FileExplorer.tsx  
3. components/layout/QuickActions.tsx
4. 字体文件 (JetBrainsMono-Regular.woff2, JetBrainsMono-Medium.woff2)

修复要求：
1. 为每个缺失的 .tsx 文件创建基本的功能组件
2. 使用系统字体替代缺失的 JetBrains Mono 字体
3. 确保组件能够正常导入和渲染
4. 保持与现有代码风格一致

请逐个创建这些文件，确保 Web UI 能够成功启动。" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_web_ui_missing_files.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/fix_web_ui_missing_files.json"

echo "✅ 任务完成: fix_web_ui_missing_files"
