#!/bin/bash
# Claude Code 任务脚本 - analyze_query_engine
# 生成时间: 2026-04-03T09:54:28.234498

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: analyze_query_engine"
echo "提示: 请分析 /Users/mars/.openclaw/workspace/claude-code-source/src/QueryEngine.ts 文件。

重点关注：
1. Query Engine..."
echo ""

# 执行 Claude Code
claude -p "请分析 /Users/mars/.openclaw/workspace/claude-code-source/src/QueryEngine.ts 文件。

重点关注：
1. Query Engine 的核心架构
2. 消息处理流程  
3. 工具调用机制
4. 权限控制设计
5. 与 OpenClaw 的对比优势

输出简洁的技术分析，不超过500字。" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/analyze_query_engine.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/analyze_query_engine.json"

echo "✅ 任务完成: analyze_query_engine"
