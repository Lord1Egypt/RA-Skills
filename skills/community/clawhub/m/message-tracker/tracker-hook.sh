#!/bin/bash
#===============================================
# tracker-hook.sh - 消息追踪钩子
# 功能: Gateway消息发送后自动调用Tracker追踪
# 日期: 2026-05-11 (v2 - 修复Socket格式)
#===============================================

set -euo pipefail

# Tracker socket路径
TRACKER_SOCK="/run/track-daemon.sock"

# 日志
LOG_FILE="/root/.openclaw/logs/tracker-hook.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [HOOK] $*" >> "${LOG_FILE}"
}

# 追踪单条消息
track_message() {
    local msg_id="$1"
    local content="${2:-}"
    local sender="${3:-}"
    local channel="${4:-feishu}"
    
    if [[ -z "$msg_id" ]]; then
        log "ERROR: Empty message_id"
        return 1
    fi
    
    # 构建内容JSON
    local content_json=""
    if [[ -n "$content" ]]; then
        content_json=$(python3 -c "
import json, sys
data = {
    'content': '''${content}'''[:500],  # 限制内容长度
    'sender_id': '''${sender}''' if [[ '${sender}' != '' ]] else '',
    'channel': '''${channel}'''
}
print(json.dumps(data))
" 2>/dev/null || echo '{}')
    fi
    
    # 直接通过Socket调用Tracker（避免创建临时文件）
    python3 << EOF
import socket
import json
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.settimeout(5)
sock.connect("${TRACKER_SOCK}")

# Socket格式：args[0]=msg_id, args[1]=content_json字符串（可选）
args = ["${msg_id}"]
if ${#content_json} > 2:  # 非空对象
    args.append(${content_json})

request = json.dumps({"cmd": "track", "args": args}).encode()

try:
    sock.sendall(request)
    sock.settimeout(3)
    data = sock.recv(4096)
    result = json.loads(data.decode())
    if "error" in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
    else:
        print(f"Tracked: ${msg_id} -> {result.get('file', 'unknown')}")
finally:
    sock.close()
EOF
    
    log "Tracked: ${msg_id}"
}

# 批量追踪消息
batch_track() {
    local msg_ids="$1"
    
    python3 << EOF
import socket
import json

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.settimeout(10)
sock.connect("${TRACKER_SOCK}")

request = json.dumps({
    "cmd": "batch",
    "args": [${msg_ids}]
}).encode()

try:
    sock.sendall(request)
    sock.settimeout(5)
    data = sock.recv(8192)
    print(data.decode())
finally:
    sock.close()
EOF
    
    log "Batch tracked: ${msg_ids}"
}

# 主入口
case "${1:-}" in
    track)
        track_message "$2" "$3" "$4" "$5"
        ;;
    batch)
        batch_track "$2"
        ;;
    *)
        echo "Usage: tracker-hook.sh track <msg_id> [content] [sender] [channel]"
        echo "       tracker-hook.sh batch <msg_id> [<msg_id>...]"
        exit 1
        ;;
esac