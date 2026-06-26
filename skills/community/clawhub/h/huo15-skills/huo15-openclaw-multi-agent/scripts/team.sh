#!/bin/bash
#===============================================================================
# 团队管理脚本
#
# 功能：
#   1. 创建团队
#   2. 加入/离开团队
#   3. 启动工作 Agent
#   4. 查看团队状态
#
# 使用方式：
#   ./team.sh create <team-name>
#   ./team.sh spawn <worker-id> <任务描述>
#   ./team.sh list
#   ./team.sh leave <worker-id>
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.openclaw/workspace/memory/activity/multi-agent"
TEAM_DIR="$DATA_DIR"
mkdir -p "$TEAM_DIR/workers"

#===============================================================================
# 创建团队
#===============================================================================
create_team() {
    local team_name="${1:-default}"
    
    echo "👥 创建团队: $team_name"
    
    cat > "$TEAM_DIR/team.json" << EOF
{
  "teamName": "$team_name",
  "createdAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "members": [],
  "status": "active"
}
EOF
    
    echo "✅ 团队已创建: $team_name"
}

#===============================================================================
# 启动工作 Agent
#===============================================================================
spawn_worker() {
    local worker_id="$1"
    local task_desc="${2:-未指定任务}"
    
    if [ -z "$worker_id" ]; then
        echo "用法: team.sh spawn <worker-id> <任务描述>"
        return 1
    fi
    
    echo "🤖 启动工作 Agent: $worker_id"
    echo "任务: $task_desc"
    echo ""
    
    # 创建 worker 配置
    mkdir -p "$TEAM_DIR/workers/$worker_id"
    cat > "$TEAM_DIR/workers/$worker_id/worker.json" << EOF
{
  "workerId": "$worker_id",
  "task": "$task_desc",
  "status": "running",
  "startedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "result": null
}
EOF
    
    # 记录到团队成员
    python3 << PYEOF
import json

team_file = "$TEAM_DIR/team.json"
try:
    with open(team_file, 'r') as f:
        team = json.load(f)
    
    if 'members' not in team:
        team['members'] = []
    
    # 检查是否已存在
    exists = any(m.get('workerId') == '$worker_id' for m in team['members'])
    if not exists:
        team['members'].append({
            'workerId': '$worker_id',
            'task': '$task_desc',
            'status': 'running',
            'startedAt': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
        })
        with open(team_file, 'w') as f:
            json.dump(team, f, indent=2)
        print("✅ Worker 已添加到团队")
    else:
        print("⚠️ Worker 已存在: $worker_id")
except Exception as e:
    print(f"错误: {e}")
PYEOF
    
    echo ""
    echo "✅ Worker 已启动: $worker_id"
    echo ""
    echo "📝 下一步："
    echo "  1. Agent 执行任务..."
    echo "  2. 使用 ./team.sh status 查看进度"
    echo "  3. 任务完成后使用 ./team.sh complete $worker_id <结果> 标记完成"
}

#===============================================================================
# 标记任务完成
#===============================================================================
complete_worker() {
    local worker_id="$1"
    local result="${2:-任务完成}"
    
    if [ -z "$worker_id" ]; then
        echo "用法: team.sh complete <worker-id> <结果>"
        return 1
    fi
    
    local worker_file="$TEAM_DIR/workers/$worker_id/worker.json"
    
    if [ ! -f "$worker_file" ]; then
        echo "❌ Worker 不存在: $worker_id"
        return 1
    fi
    
    # 更新 worker 状态
    python3 << PYEOF
import json

worker_file = "$worker_file"
result = """$result"""

try:
    with open(worker_file, 'r') as f:
        worker = json.load(f)
    
    worker['status'] = 'completed'
    worker['result'] = result
    worker['completedAt'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
    
    with open(worker_file, 'w') as f:
        json.dump(worker, f, indent=2)
    
    print(f"✅ Worker 完成: $worker_id")
except Exception as e:
    print(f"错误: {e}")
PYEOF
    
    # 更新团队成员状态
    python3 << 'PYEOF'
import json

team_file = "$TEAM_DIR/team.json"
try:
    with open(team_file, 'r') as f:
        team = json.load(f)
    
    for member in team.get('members', []):
        if member.get('workerId') == '$worker_id':
            member['status'] = 'completed'
            member['result'] = '$result'
            break
    
    with open(team_file, 'w') as f:
        json.dump(team, f, indent=2)
except:
    pass
PYEOF
}

#===============================================================================
# 查看团队状态
#===============================================================================
list_team() {
    echo "👥 团队状态"
    echo "=" * 40
    
    if [ ! -f "$TEAM_DIR/team.json" ]; then
        echo "暂无团队"
        echo "使用 ./team.sh create <team-name> 创建"
        return 0
    fi
    
    cat "$TEAM_DIR/team.json"
    echo ""
    
    # 显示 worker 状态
    if [ -d "$TEAM_DIR/workers" ]; then
        echo "🤖 Workers:"
        for worker_dir in "$TEAM_DIR/workers"/*; do
            if [ -d "$worker_dir" ]; then
                worker_id=$(basename "$worker_dir")
                status=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$worker_dir/worker.json" 2>/dev/null | cut -d'"' -f4)
                task=$(grep -o '"task"[[:space:]]*:[[:space:]]*"[^"]*"' "$worker_dir/worker.json" 2>/dev/null | cut -d'"' -f4 | cut -c1-50)
                
                if [ "$status" = "running" ]; then
                    echo "  ⚡ $worker_id: $task"
                elif [ "$status" = "completed" ]; then
                    echo "  ✅ $worker_id: 已完成"
                else
                    echo "  ⏳ $worker_id: $status"
                fi
            fi
        done
    fi
}

#===============================================================================
# 离开团队
#===============================================================================
leave_team() {
    local worker_id="$1"
    
    if [ -z "$worker_id" ]; then
        echo "用法: team.sh leave <worker-id>"
        return 1
    fi
    
    rm -rf "$TEAM_DIR/workers/$worker_id"
    
    # 从团队成员中移除
    python3 << PYEOF
import json

team_file = "$TEAM_DIR/team.json"
try:
    with open(team_file, 'r') as f:
        team = json.load(f)
    
    team['members'] = [m for m in team.get('members', []) if m.get('workerId') != '$worker_id']
    
    with open(team_file, 'w') as f:
        json.dump(team, f, indent=2)
    
    print("✅ 已离开团队: $worker_id")
except Exception as e:
    print(f"错误: {e}")
PYEOF
}

#===============================================================================
# 清理团队
#===============================================================================
cleanup() {
    echo "🧹 清理团队..."
    
    # 停止所有 running 的 worker
    for worker_dir in "$TEAM_DIR/workers"/*; do
        if [ -d "$worker_dir" ]; then
            worker_id=$(basename "$worker_dir")
            status=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$worker_dir/worker.json" 2>/dev/null | cut -d'"' -f4)
            
            if [ "$status" = "running" ]; then
                echo "  停止: $worker_id"
                # 这里应该发送停止信号给 worker
            fi
        fi
    done
    
    # 清理目录
    rm -rf "$TEAM_DIR/workers"
    mkdir -p "$TEAM_DIR/workers"
    
    echo "✅ 清理完成"
}

#===============================================================================
# 主程序
#===============================================================================
main() {
    local action="${1:-list}"
    
    case "$action" in
        create)
            create_team "$2"
            ;;
        spawn)
            spawn_worker "$2" "$3"
            ;;
        complete)
            complete_worker "$2" "$3"
            ;;
        list|status)
            list_team
            ;;
        leave)
            leave_worker "$2"
            ;;
        cleanup)
            cleanup
            ;;
        help|--help|-h)
            echo "用法:"
            echo "  $0 create <team-name>   # 创建团队"
            echo "  $0 spawn <id> <任务>    # 启动 worker"
            echo "  $0 complete <id> <结果> # 标记完成"
            echo "  $0 list                # 查看团队"
            echo "  $0 leave <id>          # 离开团队"
            echo "  $0 cleanup             # 清理团队"
            ;;
        *)
            echo "未知命令: $action"
            echo "用法: $0 create|spawn|complete|list|leave|cleanup"
            exit 1
            ;;
    esac
}

main "$@"
