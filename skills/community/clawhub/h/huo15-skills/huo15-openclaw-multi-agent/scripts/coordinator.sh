#!/bin/bash
#===============================================================================
# 多智能体协同 - 主协调脚本
#
# 功能：
#   1. 启动协调者模式
#   2. 分配任务给工作 Agent
#   3. 收集结果
#   4. 汇报给用户
#
# 使用方式：
#   ./coordinator.sh start                    # 启动协调者模式
#   ./coordinator.sh assign <task> <desc>    # 分配任务
#   ./coordinator.sh status                  # 查看状态
#   ./coordinator.sh collect                 # 收集结果
#   ./coordinator.sh stop                    # 停止协调
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/config"
DATA_DIR="$HOME/.openclaw/workspace/memory/activity"
TEAM_DIR="$DATA_DIR/multi-agent"

# 加载配置
load_config() {
    mkdir -p "$TEAM_DIR"
    
    if [ -f "$TEAM_DIR/config.json" ]; then
        TEAM_NAME=$(grep -o '"teamName"[[:space:]]*:[[:space:]]*"[^"]*"' "$TEAM_DIR/config.json" 2>/dev/null | cut -d'"' -f4)
        COORDINATOR=$(grep -o '"coordinator"[[:space:]]*:[[:space:]]*"[^"]*"' "$TEAM_DIR/config.json" 2>/dev/null | cut -d'"' -f4)
    fi
    
    TEAM_NAME="${TEAM_NAME:-default}"
    COORDINATOR="${COORDINATOR:-main}"
}

#===============================================================================
# 启动协调者模式
#===============================================================================
start_coordinator() {
    load_config
    
    echo "🤖 启动协调者模式"
    echo "=" * 40
    echo "团队名称: $TEAM_NAME"
    echo "协调者: $COORDINATOR"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # 创建团队配置
    cat > "$TEAM_DIR/config.json" << EOF
{
  "teamName": "$TEAM_NAME",
  "coordinator": "$COORDINATOR",
  "startedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "active",
  "tasks": []
}
EOF
    
    echo "✅ 协调者模式已启动"
    echo ""
    echo "下一步："
    echo "  1. 使用 ./team.sh spawn <worker-id> <任务> 启动工作 Agent"
    echo "  2. 使用 ./coordinator.sh status 查看状态"
    echo "  3. 使用 ./coordinator.sh collect 收集结果"
}

#===============================================================================
# 分配任务
#===============================================================================
assign_task() {
    local task_id="$1"
    local task_desc="${2:-}"
    
    if [ -z "$task_id" ]; then
        echo "用法: coordinator.sh assign <task-id> <任务描述>"
        return 1
    fi
    
    load_config
    
    echo "📋 分配任务: $task_id"
    echo "描述: ${task_desc:-无}"
    echo ""
    
    # 创建任务文件
    mkdir -p "$TEAM_DIR/tasks"
    cat > "$TEAM_DIR/tasks/$task_id.json" << EOF
{
  "taskId": "$task_id",
  "description": "$task_desc",
  "status": "pending",
  "assignedTo": null,
  "result": null,
  "createdAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "completedAt": null
}
EOF
    
    echo "✅ 任务已分配: $task_id"
    
    # 更新团队配置中的任务列表
    python3 << PYEOF
import json

config_file = "$TEAM_DIR/config.json"
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    if 'tasks' not in config:
        config['tasks'] = []
    
    config['tasks'].append({
        'taskId': '$task_id',
        'status': 'pending'
    })
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
except Exception as e:
    print(f"更新配置失败: {e}")
PYEOF
    
    return 0
}

#===============================================================================
# 查看状态
#===============================================================================
show_status() {
    load_config
    
    echo "🤖 协调者状态"
    echo "=" * 40
    echo "团队: $TEAM_NAME"
    echo "协调者: $COORDINATOR"
    echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    if [ -f "$TEAM_DIR/config.json" ]; then
        echo "配置:"
        cat "$TEAM_DIR/config.json"
        echo ""
    fi
    
    # 显示任务状态
    if [ -d "$TEAM_DIR/tasks" ]; then
        echo "📋 任务状态:"
        for task_file in "$TEAM_DIR/tasks"/*.json; do
            if [ -f "$task_file" ]; then
                task_id=$(basename "$task_file" .json)
                status=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$task_file" 2>/dev/null | cut -d'"' -f4)
                assigned=$(grep -o '"assignedTo"[[:space:]]*:[[:space:]]*"[^"]*"' "$task_file" 2>/dev/null | cut -d'"' -f4)
                echo "  - $task_id: $status ${assigned:+(assigned to: $assigned)}"
            fi
        done
    fi
}

#===============================================================================
# 收集结果
#===============================================================================
collect_results() {
    load_config
    
    echo "📊 收集任务结果"
    echo "=" * 40
    echo ""
    
    if [ ! -d "$TEAM_DIR/tasks" ]; then
        echo "暂无任务"
        return 0
    fi
    
    completed=0
    pending=0
    
    for task_file in "$TEAM_DIR/tasks"/*.json; do
        if [ -f "$task_file" ]; then
            task_id=$(basename "$task_file" .json)
            status=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$task_file" 2>/dev/null | cut -d'"' -f4)
            
            if [ "$status" = "completed" ]; then
                ((completed++))
                echo "✅ $task_id (已完成)"
                
                # 显示结果摘要
                result=$(grep -o '"result"[[:space:]]*:[[:space:]]*"[^"]*"' "$task_file" 2>/dev/null | cut -d'"' -f4 | cut -c1-100)
                if [ -n "$result" ]; then
                    echo "   结果: ${result}..."
                fi
            elif [ "$status" = "pending" ] || [ "$status" = "running" ]; then
                ((pending++))
                echo "⏳ $task_id (${status})"
            fi
        fi
    done
    
    echo ""
    echo "总计: $completed 已完成, $pending 待处理"
    
    return 0
}

#===============================================================================
# 停止协调
#===============================================================================
stop_coordinator() {
    load_config
    
    echo "🛑 停止协调者模式"
    
    if [ -f "$TEAM_DIR/config.json" ]; then
        python3 << PYEOF
import json

config_file = "$TEAM_DIR/config.json"
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    config['status'] = 'stopped'
    config['stoppedAt'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ 协调者模式已停止")
except Exception as e:
    print(f"停止失败: {e}")
PYEOF
    else
        echo "协调者未启动"
    fi
}

#===============================================================================
# 主程序
#===============================================================================
main() {
    local action="${1:-status}"
    
    case "$action" in
        start)
            start_coordinator
            ;;
        assign)
            assign_task "$2" "$3"
            ;;
        status)
            show_status
            ;;
        collect)
            collect_results
            ;;
        stop)
            stop_coordinator
            ;;
        help|--help|-h)
            echo "用法:"
            echo "  $0 start              # 启动协调者模式"
            echo "  $0 assign <task> <desc>  # 分配任务"
            echo "  $0 status             # 查看状态"
            echo "  $0 collect            # 收集结果"
            echo "  $0 stop              # 停止协调"
            ;;
        *)
            echo "未知命令: $action"
            echo "用法: $0 start|assign|status|collect|stop"
            exit 1
            ;;
    esac
}

main "$@"
