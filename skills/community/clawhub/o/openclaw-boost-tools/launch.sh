#!/bin/bash
# OpenClaw Boost 工具集启动器
# 用法: ./launch.sh <command>

# 自动检测工具目录（相对于脚本位置）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/tools"

show_help() {
    echo "📦 OpenClaw Boost 工具集"
    echo ""
    echo "用法: ./launch.sh <command>"
    echo ""
    echo "可用命令:"
    echo "  help              - 显示帮助"
    echo "  cost             - 成本追踪"
    echo "  memory           - 记忆管理"
    echo "  compaction        - 压缩管理"
    echo "  tools            - 工具追踪"
    echo "  permission       - 权限管理"
    echo "  coordinator      - Agent协调"
    echo "  dream            - 自动整理"
    echo "  slash            - 斜杠命令"
    echo "  budget           - Token预算"
    echo "  flags            - 功能开关"
    echo "  all-status       - 所有状态"
    echo ""
}

case "$1" in
    help)
        show_help
        ;;
    cost)
        python3 "$TOOLS_DIR/cost_tracker.py"
        ;;
    memory)
        python3 "$TOOLS_DIR/memory_relevance.py" scan
        ;;
    compaction)
        python3 "$TOOLS_DIR/compaction_manager.py" status
        ;;
    tools)
        python3 "$TOOLS_DIR/tool_tracker.py" summary
        ;;
    permission)
        python3 "$TOOLS_DIR/permission_manager.py" list
        ;;
    coordinator)
        python3 "$TOOLS_DIR/coordinator.py" list
        ;;
    dream)
        python3 "$TOOLS_DIR/dream_consolidation.py" status
        ;;
    slash)
        python3 "$TOOLS_DIR/slash_commands.py" help
        ;;
    budget)
        python3 "$TOOLS_DIR/token_budget.py" status
        ;;
    flags)
        python3 "$TOOLS_DIR/feature_flags.py" list
        ;;
    all-status)
        echo "=== 成本追踪 ===" && python3 "$TOOLS_DIR/cost_tracker.py" | head -10
        echo ""
        echo "=== Token预算 ===" && python3 "$TOOLS_DIR/token_budget.py" status
        echo ""
        echo "=== 功能开关 ===" && python3 "$TOOLS_DIR/feature_flags.py" status
        ;;
    *)
        show_help
        ;;
esac
