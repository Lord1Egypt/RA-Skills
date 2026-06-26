#!/usr/bin/env bash
# goal-task.sh — 创建有目标的一次性定时任务
# 用法:
#   source goal-task.sh
#   goal_task "5" "继续处理未完成的事项"
#   echo $job_id  # 获取 jobId 用于后续删除

set -euo pipefail

# ---------- 默认配置 ----------
FEISHU_GROUP_ID="${FEISHU_GROUP_ID:-oc_xxxxxxxxxxxxxxxx}"

# ---------- 获取 token ----------
get_gateway_token() {
    python3 -c "import json,sys; c=json.load(open('$HOME/.openclaw/openclaw.json')); print(c['gateway']['auth']['token'])"
}

# ---------- 解析 session key ----------
parse_agent_from_session_key() {
    local session_key="$1"
    echo "$session_key" | cut -d: -f2
}

# ---------- 构建 sessionTarget ----------
build_session_target() {
    local agent_id="$1"
    echo "session:agent:${agent_id}:feishu:group:${FEISHU_GROUP_ID}"
}

# ---------- 提取 JSON（处理 Config warnings 前缀）----------
extract_json_from_result() {
    python3 -c "
import sys, json, re
text = sys.stdin.read()
text = re.sub(r'^Config warnings:[\n\r]*', '', text)
match = re.search(r'\{[\s\S]*\}', text)
if match:
    d = json.loads(match.group())
    if 'id' in d:
        print(d['id'])
    elif 'ok' in d:
        print('ok' if d['ok'] else 'error')
    else:
        print('UNKNOWN')
else:
    print('ERROR')
" 2>/dev/null
}

# ---------- 创建 goal task ----------
# 用法: goal_task "delay_minutes" "message"
goal_task() {
    local delay_minutes="$1"
    local message="$2"

    local session_key="${AGENT_SESSION_KEY:-}"
    if [ -z "$session_key" ]; then
        echo "ERROR: AGENT_SESSION_KEY not set" >&2
        return 1
    fi

    local agent_id
    agent_id=$(parse_agent_from_session_key "$session_key")
    local session_target
    session_target=$(build_session_target "$agent_id")

    local delay_ms=$((delay_minutes * 60 * 1000))
    local job_name="goal-task-${agent_id}-$(date +%s)"
    local token
    token=$(get_gateway_token)

    # 第一步：创建 cron，message 暂时不加删除提示（jobId 还未知）
    local params
    params=$(python3 << PYEOF
import json
params = {
    "name": "$job_name",
    "schedule": {"kind": "every", "everyMs": $delay_ms},
    "sessionTarget": "$session_target",
    "agentId": "$agent_id",
    "payload": {
        "kind": "agentTurn",
        "message": """$message""",
        "timeoutSeconds": 3600
    },
    "delivery": {"mode": "announce"}
}
print(json.dumps(params))
PYEOF
)

    local result
    result=$(openclaw gateway call cron.add \
        --token "$token" \
        --json \
        --params "$params" 2>&1)

    local job_id
    job_id=$(echo "$result" | extract_json_from_result)

    if [[ "$job_id" == "ERROR" ]]; then
        echo "ERROR: failed to create goal-task" >&2
        return 1
    fi

    # 第二步：更新 cron message，追加删除提示（含 jobId）
    local delete_hint="

---
完成后请删除本 cron：delete_goal_task \"$job_id\"（或 openclaw gateway call cron.remove --token \"\$TOKEN\" --params '{\"jobId\":\"$job_id\"}'）"

    local update_params
    update_params=$(python3 << PYEOF
import json, shlex
# 拼接原消息 + 删除提示（shell 变量在 python 外已经展开，所以 message 已是最终值）
full_msg = """$message""" + """
---
完成后请删除本 cron：delete_goal_task \"$job_id\"（或 openclaw gateway call cron.remove --token \"\$TOKEN\" --params '{\"jobId\":\"$job_id\"}'）"""
patch = {"message": full_msg}
print(json.dumps({"id": "$job_id", "patch": patch}))
PYEOF
)

    openclaw gateway call cron.update \
        --token "$token" \
        --json \
        --params "$update_params" 2>&1 | grep -v "Config warnings\|🦞\|channel plugin\|setup surfaces\|runtime loads" > /dev/null

    echo "$job_id"
}

# ---------- 删除 goal task ----------
# 用法: delete_goal_task "jobId"
delete_goal_task() {
    local job_id="$1"
    local token
    token=$(get_gateway_token)

    local result
    result=$(openclaw gateway call cron.remove \
        --token "$token" \
        --json \
        --params "{\"jobId\":\"$job_id\"}" 2>&1)

    local removed
    removed=$(echo "$result" | extract_json_from_result)
    echo "$removed"
}

# ---------- 测试模式 ----------
if [[ "${1:-}" == "--test" ]]; then
    export AGENT_SESSION_KEY="agent:main:feishu:group:oc_xxxxxxxxxxxxxxxx"
    echo "=== goal-task.sh 测试 ==="
    echo ""
    echo "=== 创建测试任务（1分钟后）==="
    job_id=$(goal_task "1" "goal-task 测试：验证删除提示")
    echo "Created job_id: $job_id"
    echo ""
    echo "=== 等待 2 秒后删除 ==="
    sleep 2
    delete_goal_task "$job_id"
    echo "Delete result: $?"
    echo ""
    echo "=== 验证已删除 ==="
    openclaw gateway call cron.list --json --params "{}" 2>&1 | python3 -c "
import json, sys, re
text = sys.stdin.read()
lines = [l for l in text.split('\n') if not l.startswith('Config') and not l.startswith('-') and not l.startswith('🦞')]
try:
    d = json.loads('\n'.join(lines))
    jobs = d.get('jobs', [])
    target = [j for j in jobs if j['id'] == '$job_id']
    print('Job still exists:', bool(target))
except: pass
" 2>/dev/null
    echo "=== 测试完成 ==="
fi