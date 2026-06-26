#!/bin/bash
# state.sh - 状态读写脚本
# 调用 session-state.sh 或直接操作状态文件

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config.json"
STATE_FILE="${STATE_FILE:-$HOME/.openclaw/tmp/autoresearch-loop-state.json}"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/tmp/autoresearch-loop.log}"

mkdir -p "$(dirname "$STATE_FILE")"
mkdir -p "$(dirname "$LOG_FILE")"

# 初始化状态
init_state() {
    local goal="$1"
    local verify_cmd="$2"
    local scope_globs="${3:-**}"

    cat > "$STATE_FILE" <<EOF
{
  "goal": "$goal",
  "verify_command": "$verify_cmd",
  "scope_globs": "$scope_globs",
  "iteration": 0,
  "successes": 0,
  "failures": 0,
  "consecutive_failures": 0,
  "last_success": null,
  "last_fail": null,
  "history": [],
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "running"
}
EOF
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INIT] 状态初始化完成 - 目标: $goal" >> "$LOG_FILE"
    echo "✅ 状态已初始化 - 目标: $goal"
}

# 读取当前迭代次数
get_iteration() {
    if [[ -f "$STATE_FILE" ]]; then
        python3 -c "import json; print(json.load(open('$STATE_FILE'))['iteration'])" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# 读取状态
get_state() {
    if [[ -f "$STATE_FILE" ]]; then
        cat "$STATE_FILE"
    else
        echo "{}"
    fi
}

# 更新状态
update_state() {
    local iteration="$1"
    local result="$2"  # success | failure
    local message="$3"
    local changes="$4"

    local successes=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('successes',0))" 2>/dev/null || echo "0")
    local failures=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('failures',0))" 2>/dev/null || echo "0")
    local consecutive=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('consecutive_failures',0))" 2>/dev/null || echo "0")
    local history=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(json.dumps(d.get('history',[])))" 2>/dev/null || echo "[]")

    if [[ "$result" == "success" ]]; then
        successes=$((successes + 1))
        consecutive=0
        last_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    else
        failures=$((failures + 1))
        consecutive=$((consecutive + 1))
        last_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    fi

    local entry=$(cat <<EOF
{
  "iteration": $iteration,
  "result": "$result",
  "message": "$message",
  "changes": "$changes",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)

    # 更新状态
    python3 <<PYEOF
import json

state_file = '$STATE_FILE'
with open(state_file, 'r') as f:
    state = json.load(f)

state['iteration'] = $iteration
state['successes'] = $successes
state['failures'] = $failures
state['consecutive_failures'] = $consecutive
state['last_success'] = '$result' == 'success' and '$(date -u +%Y-%m-%dT%H:%M:%SZ)' or state.get('last_success')
state['last_fail'] = '$result' == 'failure' and '$(date -u +%Y-%m-%dT%H:%M:%SZ)' or state.get('last_fail')

entry = json.loads('''$entry''')
state['history'].append(entry)

with open(state_file, 'w') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)
PYEOF

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$result.to_upper()] 迭代 $iteration - $message" >> "$LOG_FILE"
}

# 检查是否应该停止
should_stop() {
    local max_iterations=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('max_iterations', 50))" 2>/dev/null || echo "50")
    local convergence=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('convergence_threshold', 3))" 2>/dev/null || echo "3")
    local iteration=$(get_iteration)
    local consecutive=$(python3 -c "import json; print(json.load(open('$STATE_FILE')).get('consecutive_failures', 0))" 2>/dev/null || echo "0")

    if [[ $iteration -ge $max_iterations ]]; then
        echo "max_iterations"
        return 0
    fi

    if [[ $consecutive -ge $convergence ]]; then
        echo "convergence"
        return 0
    fi

    return 1
}

# 获取摘要
get_summary() {
    if [[ -f "$STATE_FILE" ]]; then
        python3 -c "
import json
d = json.load(open('$STATE_FILE'))
print(f\"\"\"迭代摘要:
- 目标: {d['goal']}
- 总迭代: {d['iteration']}
- 成功: {d['successes']}
- 失败: {d['failures']}
- 连续失败: {d['consecutive_failures']}
- 状态: {d['status']}
\"\"\")
"
    fi
}

# 标记完成
mark_complete() {
    python3 <<PYEOF
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
state['status'] = 'completed'
state['completed_at'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
PYEOF
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [COMPLETE] 自动迭代完成" >> "$LOG_FILE"
}

# 命令路由
case "$1" in
    init)
        init_state "$2" "$3" "$4"
        ;;
    get)
        get_state
        ;;
    iteration)
        get_iteration
        ;;
    update)
        update_state "$2" "$3" "$4" "$5"
        ;;
    should_stop)
        should_stop
        ;;
    summary)
        get_summary
        ;;
    complete)
        mark_complete
        ;;
    *)
        echo "Usage: state.sh {init|get|iteration|update|should_stop|summary|complete}"
        exit 1
        ;;
esac
