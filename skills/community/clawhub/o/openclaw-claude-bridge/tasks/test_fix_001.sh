#!/bin/bash
# Claude Code 任务脚本 - test_fix_001
# 生成时间: 2026-04-03T09:20:02.658888

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: test_fix_001"
echo "提示: 检查当前目录下的 README.md 文件是否存在，如果存在则读取前5行内容..."
echo ""

# 执行 Claude Code
claude -p "检查当前目录下的 README.md 文件是否存在，如果存在则读取前5行内容" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/test_fix_001.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/test_fix_001.json"

echo "✅ 任务完成: test_fix_001"
