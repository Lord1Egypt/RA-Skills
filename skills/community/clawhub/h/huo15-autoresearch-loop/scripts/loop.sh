#!/bin/bash
# loop.sh - 自主研究循环主脚本
# Modify → Verify → Keep/Discard → Repeat forever

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$SKILL_DIR/config.json"

source "$SCRIPT_DIR/state.sh"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
log_ok()     { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn()   { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()  { echo -e "${RED}[ERROR]${NC} $1"; }

# 主循环
run_loop() {
    local goal="$1"
    local verify_cmd="$2"
    local scope_globs="${3:-**}"

    log_info "🚀 启动自动迭代 - 目标: $goal"
    log_info "📋 验证命令: $verify_cmd"

    # 初始化状态
    state init "$goal" "$verify_cmd" "$scope_globs"

    local iteration=0
    local max_iterations=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('max_iterations', 50))" 2>/dev/null || echo "50")
    local commit_each=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('commit_each_success', True))" 2>/dev/null || echo "true")
    local revert_on_fail=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('revert_on_fail', True))" 2>/dev/null || echo "true")

    # 保存初始 git 状态
    local initial_commit=$(git rev-parse HEAD 2>/dev/null || echo "")

    while true; do
        iteration=$((iteration + 1))
        log_info "━━━ 迭代 $iteration / $max_iterations ━━━"

        # 检查停止条件
        if state should_stop; then
            local reason=$(state should_stop 2>/dev/null || echo "unknown")
            log_warn "⏹ 停止条件触发: $reason"
            break
        fi

        # 记录当前 git 状态
        local pre_commit=$(git rev-parse HEAD 2>/dev/null || echo "")

        # 执行一次修改
        log_info "🔧 执行修改..."
        local modify_result=0
        local changes=""

        # 调用 AI 进行一次修改（通过环境变量传递上下文）
        # 这里需要主 Agent 介入，实际由 OpenClaw sessions_spawn 调用子 agent
        if [[ -n "$CLAUDE_TASK" ]]; then
            # 子 agent 模式：执行修改
            eval "$CLAUDE_TASK" || modify_result=$?
            changes=$(git diff --stat HEAD 2>/dev/null || echo "")
        else
            log_warn "⚠ CLAUDE_TASK 未设置，请在 OpenClaw 中使用 sessions_spawn 调用"
            break
        fi

        if [[ $modify_result -ne 0 ]]; then
            log_error "修改执行失败，跳过验证"
            state update "$iteration" "failure" "修改执行失败" "$changes"
            continue
        fi

        # 验证
        log_info "🔍 执行验证..."
        if verify.sh run "$verify_cmd"; then
            log_ok "✅ 验证通过"

            # git commit
            if [[ "$commit_each" == "true" ]] && [[ -n "$(git status --porcelain)" ]]; then
                git add -A
                git commit -m "autoresearch iter $iteration: $goal" 2>/dev/null || true
            fi

            state update "$iteration" "success" "验证通过" "$changes"
        else
            log_error "❌ 验证失败"

            # git revert
            if [[ "$revert_on_fail" == "true" ]] && [[ -n "$pre_commit" ]]; then
                log_info "↩ 回滚更改..."
                git reset --hard HEAD > /dev/null 2>&1 || true
                git clean -fd > /dev/null 2>&1 || true
            fi

            state update "$iteration" "failure" "验证失败" "$changes"
        fi

        echo ""
    done

    # 输出最终摘要
    state complete
    echo ""
    log_info "━━━ 最终摘要 ━━━"
    state summary
}

# 停止运行中的循环
stop_loop() {
    local state_file="$HOME/.openclaw/tmp/autoresearch-loop-state.json"
    if [[ -f "$state_file" ]]; then
        python3 <<PYEOF
import json
with open('$state_file', 'r') as f:
    state = json.load(f)
state['status'] = 'stopped_by_user'
state['stopped_at'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
with open('$state_file', 'w') as f:
    json.dump(state, f, indent=2)
PYEOF
        log_ok "循环已停止"
    else
        log_error "没有正在运行的循环"
    fi
}

# 查看状态
status() {
    state get
}

# 命令路由
case "$1" in
    start|run)
        run_loop "$2" "$3" "$4"
        ;;
    stop)
        stop_loop
        ;;
    status)
        status
        ;;
    summary)
        state summary
        ;;
    *)
        echo "Usage: loop.sh {start|stop|status|summary} [goal] [verify_cmd] [scope]"
        echo ""
        echo "示例:"
        echo "  loop.sh start '优化性能' 'make test'"
        echo "  loop.sh status"
        echo "  loop.sh stop"
        exit 1
        ;;
esac
