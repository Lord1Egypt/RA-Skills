#!/bin/bash
#
# Good-Memory: Tracker 维护脚本 v2.1.0
# 优化：重置检测优先查找reset文件，不需要等待新session生成
#

set -e

# 支持环境变量自定义路径
OPENCLAW_BASE="${OPENCLAW_BASE:-/root/.openclaw}"
TRACKER_FILE="${TRACKER_FILE:-${OPENCLAW_BASE}/workspace/session-tracker.json}"
# 所有session默认存储在main的sessions目录，这是OpenClaw的默认行为
SESSIONS_DIR="${SESSIONS_DIR:-${OPENCLAW_BASE}/agents/main/sessions}"

# 从文件名提取 UUID 前缀
get_file_uuid() {
    local filepath="$1"
    basename "$filepath" | cut -d'.' -f1
}

# 初始化tracker文件
init_tracker() {
    if [[ ! -f "$TRACKER_FILE" ]]; then
        mkdir -p "$(dirname "$TRACKER_FILE")"
        cat > "$TRACKER_FILE" << 'EOF'
{
  "description": "Session tracker - maps agent+chat to session files",
  "last_updated": "",
  "agents": {}
}
EOF
    fi
}

# 更新tracker核心逻辑
update_tracker() {
    local agent="$1"
    local chat_id="$2"

    init_tracker

    # 1. 找到当前活跃的session文件（最新的非.reset/.deleted文件）
    local current_session=$(ls -t "${SESSIONS_DIR}"/*.jsonl 2>/dev/null | grep -vE '\.(reset|deleted|lock)' | head -1)
    local current_uuid=""
    if [[ -n "$current_session" ]]; then
        current_uuid=$(get_file_uuid "$current_session")
    fi

    # 2. 读取并更新tracker
    python3 << PYEOF
import json
import os
from datetime import datetime, timezone

tracker_file = "$TRACKER_FILE"
agent = "$agent"
chat_id = "$chat_id"
current_session = "$current_session"
current_uuid = "$current_uuid"
sessions_dir = "$SESSIONS_DIR"

with open(tracker_file, 'r') as f:
    tracker = json.load(f)

# 确保agent和chat_id存在
if agent not in tracker["agents"]:
    tracker["agents"][agent] = {}
if chat_id not in tracker["agents"][agent]:
    tracker["agents"][agent][chat_id] = {
        "session_key": "",
        "active": "",
        "active_uuid": "",
        "last_history": "",
        "history": []
    }

info = tracker["agents"][agent][chat_id]
old_uuid = info.get("active_uuid", "")
reset_detected = False
reset_file = ""

# 检测逻辑：
# 1. 优先检测是否有旧UUID对应的reset文件（显式重置）
# 2. 如果没有reset文件但旧UUID≠新UUID，说明是隐式会话切换
reset_file = ""
reset_detected = False
if old_uuid:
    # 1. 检查显式重置
    reset_pattern = f"{old_uuid}.jsonl.reset."
    for f in os.listdir(sessions_dir):
        if reset_pattern in f:
            reset_file = os.path.join(sessions_dir, f)
            reset_detected = True
            break
    
    # 2. 检查隐式会话切换
    if not reset_detected and current_uuid and old_uuid != current_uuid:
        # 旧会话还存在，直接用它作为last_history
        old_session_file = os.path.join(sessions_dir, f"{old_uuid}.jsonl")
        if os.path.exists(old_session_file):
            reset_file = old_session_file
            reset_detected = True
            print(f"IMPLICIT_SWITCH_DETECTED: Session switched from {old_uuid} to {current_uuid}", file=sys.stderr)
    
    if reset_detected and reset_file:
        # 更新last_history
        info["last_history"] = reset_file
        # 加入history数组，最多保留10条
        info["history"].insert(0, reset_file)
        if len(info["history"]) > 10:
            info["history"] = info["history"][:10]

# 如果有当前session，更新active信息
if current_session and current_uuid:
    info["active"] = current_session
    info["active_uuid"] = current_uuid

# 更新时间
tracker["last_updated"] = datetime.now(timezone.utc).isoformat()

# 写回tracker
with open(tracker_file, 'w') as f:
    json.dump(tracker, f, indent=2, ensure_ascii=False)

# 输出结果
if reset_detected:
    if reset_pattern in reset_file:
        print(f"RESET_DETECTED: Old session reset")
    else:
        print(f"RESET_DETECTED: Implicit session switch")
    print(f"last_history: {reset_file}")
else:
    print("OK: session unchanged")
    print(f"last_history: {info.get('last_history', '')}")
PYEOF
}

# 主入口
main() {
    [[ $# -lt 2 ]] && { 
        echo "Usage: $0 detect <agent> <chat_id>"
        echo "Simplified version: only detect and update tracker"
        exit 1
    }

    local command="$1"
    local agent="$2"
    local chat_id="$3"

    case "$command" in
        detect)
            # 现在detect就是update，二合一，简化流程
            update_tracker "$agent" "$chat_id"
            ;;
        *)
            echo "Unknown command: $command"
            echo "Only 'detect' command is supported in simplified version"
            exit 1
            ;;
    esac
}

main "$@"
