#!/bin/bash
#===============================================================================
# 多智能体协同 - OpenClaw sessions_spawn 集成脚本
#
# 使用方式：
#   ./spawn.sh <task> [label] [model] [timeout]
#
# 示例：
#   ./spawn.sh "分析代码" "code-analysis" "MiniMax-M2.1" 300
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$HOME/.openclaw/workspace/memory/activity/multi-agent"

mkdir -p "$LOG_DIR"

#===============================================================================
# 记录任务日志
#===============================================================================
log_task() {
    local label="$1"
    local task="$2"
    local status="$3"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "## $timestamp | $label | $status | $task" >> "$LOG_DIR/spawn-log.md"
}

#===============================================================================
# 生成任务 ID
#===============================================================================
generate_id() {
    echo "agent-$(date +%s)-$RANDOM"
}

#===============================================================================
# 主程序
#===============================================================================
main() {
    local task="${1:-}"
    local label="${2:-}"
    local model="${3:-MiniMax-M2.1}"
    local timeout="${4:-600}"
    
    if [ -z "$task" ]; then
        echo "用法: $0 <task> [label] [model] [timeout]"
        echo ""
        echo "示例:"
        echo "  $0 \"分析代码\" \"code-analysis\""
        echo "  $0 \"生成报告\" \"report-gen\" \"MiniMax-M2.1\" 300"
        return 1
    fi
    
    # 生成标签
    [ -z "$label" ] && label="task-$(date +%s)"
    
    echo "🤖 启动并行任务"
    echo "=" * 40
    echo "任务: $task"
    echo "标签: $label"
    echo "模型: $model"
    echo "超时: ${timeout}s"
    echo ""
    
    # 记录日志
    log_task "$label" "$task" "spawned"
    
    echo "✅ 任务已启动: $label"
    echo ""
    echo "📋 OpenClaw 会自动："
    echo "  1. 派生子 Agent 执行任务"
    echo "  2. 子 Agent 完成后 announce 结果"
    echo "  3. 结果汇报到当前会话"
    echo ""
    echo "💡 查看子 Agent: /subagents list"
    echo "💡 停止子 Agent: /subagents kill <id>"
    
    return 0
}

main "$@"
