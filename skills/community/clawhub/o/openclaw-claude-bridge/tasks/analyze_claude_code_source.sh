#!/bin/bash
# Claude Code 任务脚本 - analyze_claude_code_source
# 生成时间: 2026-04-03T09:41:38.775492

cd "/Users/mars/.openclaw/workspace/skills/claude-bridge"

echo "🚀 执行任务: analyze_claude_code_source"
echo "提示: 请深度分析 /Users/mars/.openclaw/workspace/claude-code-source/ 目录下的 Claude Code 源码。

分析要求：

1. **架构概览**
 ..."
echo ""

# 执行 Claude Code
claude -p "请深度分析 /Users/mars/.openclaw/workspace/claude-code-source/ 目录下的 Claude Code 源码。

分析要求：

1. **架构概览**
   - 整体项目结构
   - 核心模块划分
   - 技术栈分析 (Bun, TypeScript, React, etc.)

2. **核心子系统解构**
   - Query Engine (查询引擎)
   - Tool System (工具系统)
   - Command System (命令系统)
   - Permission System (权限系统)
   - Memory System (记忆系统)
   - MCP System (MCP集成)

3. **关键设计模式**
   - 提取可借鉴的架构模式
   - 代码组织方式
   - 扩展性设计

4. **与 OpenClaw 的对比**
   - 优势分析
   - 可移植组件
   - 改进建议

5. **输出格式**
   - 结构化报告
   - 关键代码片段
   - 架构图描述

请生成详细的分析报告，保存到 /Users/mars/.openclaw/workspace/claude-code-analysis.md" --allowedTools "Read,Edit,Bash" > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/analyze_claude_code_source.txt" 2>&1

# 标记完成
echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > "/Users/mars/.openclaw/workspace/skills/claude-bridge/results/analyze_claude_code_source.json"

echo "✅ 任务完成: analyze_claude_code_source"
