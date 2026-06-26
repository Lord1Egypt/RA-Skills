#!/bin/bash
# 会话检查脚本 - 最终完善版
# 功能: 定期检查未提炼的会话，通知用户并触发提炼
# 特点: 
# - 从sessions.json获取所有活跃会话ID（私聊+群聊）
# - 跳过所有活跃会话
# - 跳过已提炼会话
# - 进程锁防止多个实例同时运行
# - 会话去重（避免同一个会话被处理多次）
# - 防重复调用：新增 "正在处理中" 标记，解决频繁检查导致的重复调用问题

# 加载环境变量
WORKSPACE="/root/.openclaw/workspace"
if [ -f "$WORKSPACE/.env" ]; then
    source "$WORKSPACE/.env"
fi

# 配置
SESSIONS_DIR="/root/.openclaw/agents/main/sessions"
EXTRACTED_FILE="$WORKSPACE/memory/.extracted_sessions"
PROCESSING_FILE="$WORKSPACE/memory/.processing_sessions"
SCRIPT_DIR="$WORKSPACE/scripts"
DO_EXTRACT_SCRIPT="$SCRIPT_DIR/do_extract_and_write.sh"
SESSIONS_JSON="$SESSIONS_DIR/sessions.json"
LOCK_FILE="/tmp/session_check.lock"
PROCESSED_SESSIONS="/tmp/processed_sessions.tmp"

# 消息发送目标（从环境变量读取，默认发送给 FEISHU_USER_OPEN_ID）
NOTIFY_TARGET="${NOTIFY_TARGET:-user:${FEISHU_USER_OPEN_ID}}"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 进程锁函数（使用mkdir原子操作）
acquire_lock() {
    # 尝试创建锁目录（原子操作）
    if ! mkdir "$LOCK_FILE" 2>/dev/null; then
        # 锁已存在，检查是否过期（超过10分钟认为是死锁）
        local lock_mtime=$(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0)
        local now=$(date +%s)
        local lock_age=$((now - lock_mtime))
        
        if [ "$lock_age" -gt 600 ]; then
            log "警告: 锁文件已过期（${lock_age}秒），强制删除"
            rm -rf "$LOCK_FILE"
            if ! mkdir "$LOCK_FILE" 2>/dev/null; then
                log "错误: 无法获取锁，另一个进程正在运行"
                return 1
            fi
        else
            log "跳过: 另一个进程正在运行（锁年龄: ${lock_age}秒）"
            return 1
        fi
    fi
    
    # 记录锁创建时间
    touch "$LOCK_FILE"
    log "已获取进程锁"
    return 0
}

# 释放锁函数
release_lock() {
    rm -rf "$LOCK_FILE"
    rm -f "$PROCESSED_SESSIONS" 2>/dev/null
    log "已释放进程锁"
}

# 确保脚本退出时释放锁
trap 'release_lock' EXIT

# 从sessions.json获取所有活跃会话ID（包括私聊和群聊，只保留最近24小时更新的，排除heartbeat会话）
get_active_sessions() {
    if [ ! -f "$SESSIONS_JSON" ]; then
        log "错误: sessions.json不存在: $SESSIONS_JSON"
        return 1
    fi
    
    python3 -c "
import json
import time
try:
    data = json.load(open('$SESSIONS_JSON'))
    now = time.time() * 1000  # 当前时间（毫秒）
    one_day = 24 * 60 * 60 * 1000  # 24小时（毫秒）
    # 遍历所有key，提取最近24小时更新的sessionId，排除heartbeat会话
    for key in data:
        if key == 'agent:main:main':
            continue  # 跳过heartbeat会话
        if 'sessionId' in data[key] and 'updatedAt' in data[key]:
            updated_at = data[key]['updatedAt']
            if now - updated_at < one_day:
                print(data[key]['sessionId'])
except Exception as e:
    print(f'Error: {e}')
" 2>/dev/null
}

# 发送通知（直接用 openclaw CLI 发送）
send_notification() {
    local message="$1"
    log "通知: $message"
    
    # 用 openclaw CLI 发送消息
    if command -v openclaw &>/dev/null; then
        log "使用 openclaw CLI 发送消息到: $NOTIFY_TARGET"
        openclaw message send --channel feishu --target "$NOTIFY_TARGET" --message "$message" 2>&1 || {
            log "警告: openclaw CLI 发送失败"
        }
    else
        log "警告: openclaw CLI 不可用，无法发送通知"
    fi
}

# ============== 主程序开始 ==============

# 获取进程锁
if ! acquire_lock; then
    exit 1
fi

# 确保目录和文件存在
mkdir -p "$(dirname "$EXTRACTED_FILE")"
touch "$EXTRACTED_FILE"
touch "$PROCESSING_FILE"
rm -f "$PROCESSED_SESSIONS" 2>/dev/null
touch "$PROCESSED_SESSIONS"

# 获取所有活跃会话ID
ACTIVE_SESSIONS=$(get_active_sessions)
if [ -z "$ACTIVE_SESSIONS" ]; then
    log "提示: 未检测到活跃会话"
else
    log "活跃会话ID:"
    echo "$ACTIVE_SESSIONS" | while read -r session_id; do
        [ -n "$session_id" ] && log "  - $session_id"
    done
fi

# 检查提炼脚本是否存在
if [ ! -f "$DO_EXTRACT_SCRIPT" ]; then
    log "错误: 提炼脚本不存在: $DO_EXTRACT_SCRIPT"
    exit 1
fi
chmod +x "$DO_EXTRACT_SCRIPT"

# 遍历所有会话文件（包括 .jsonl、.jsonl.reset.*、.jsonl.deleted.*）
for session_file in "$SESSIONS_DIR"/*.jsonl "$SESSIONS_DIR"/*.jsonl.*; do
    # 跳过不存在的文件（避免*.jsonl匹配失败）
    [ -e "$session_file" ] || continue
    
    # 获取session_id（去掉路径和所有后缀：.jsonl、.jsonl.reset.*、.jsonl.deleted.*等）
    session_id=$(basename "$session_file" | sed -E 's/\.jsonl(\..*)?$//')
    
    # 跳过空的session_id
    [ -z "$session_id" ] && continue
    
    # 去重：检查是否已经处理过这个session_id
    if grep -q "^${session_id}$" "$PROCESSED_SESSIONS" 2>/dev/null; then
        log "跳过重复会话（同一session_id多个文件）: $session_id -> $session_file"
        continue
    fi
    
    # 标记为已处理（同一个session_id只处理一次，不管有多少个后缀文件）
    echo "$session_id" >> "$PROCESSED_SESSIONS"
    
    # 获取当前 heartbeat 会话的 sessionFile，并跳过对应的文件
    HEARTBEAT_SESSION_FILE=$(python3 -c "
import json
import os
try:
    data = json.load(open('$SESSIONS_JSON'))
    if 'agent:main:main' in data:
        session_file = data['agent:main:main'].get('sessionFile', '')
        if session_file:
            # 从完整路径中提取 session_id
            filename = os.path.basename(session_file)
            # 去掉 .jsonl 后缀（如果文件是 /path/to/xxx.jsonl）
            if filename.endswith('.jsonl'):
                print(filename[:-6])
            else:
                # 如果已经是 session_id 格式（没有 .jsonl 后缀）
                print(filename)
        else:
            print('')
    else:
        print('')
except:
    print('')
" 2>/dev/null)
    
    # 跳过 heartbeat 会话（当前和历史）
    # 1. 跳过当前 heartbeat 会话
    if [ -n "$HEARTBEAT_SESSION_FILE" ] && [ "$session_id" = "$HEARTBEAT_SESSION_FILE" ]; then
        log "跳过 heartbeat 会话: $session_id"
        # 把当前 heartbeat 会话标记为已提炼，这样下次它被重置后就不会被处理
        if ! grep -q "^agent:main:session:${session_id}$" "$EXTRACTED_FILE" 2>/dev/null; then
            echo "agent:main:session:${session_id}" >> "$EXTRACTED_FILE"
            log "已将历史 heartbeat 会话标记为已提炼: $session_id"
        fi
        continue
    fi
    
    # 跳过所有活跃会话
    if echo "$ACTIVE_SESSIONS" | grep -q "^${session_id}$" 2>/dev/null; then
        log "跳过活跃会话: $session_id"
        continue
    fi
    
    # 检查是否已提炼过
    if grep -q "^agent:main:session:${session_id}$" "$EXTRACTED_FILE" 2>/dev/null; then
        log "跳过已提炼会话: $session_id"
        continue
    fi
    
    # 检查是否正在处理中（已经有提炼进程在运行）
    if grep -q "^agent:main:session:${session_id}$" "$PROCESSING_FILE" 2>/dev/null; then
        # 检查处理是否超时（超过30分钟认为是死锁，清理掉）
        # 读取行最后记录的时间戳，格式: agent:main:session:xxx timestamp
        # 如果文件中没有时间戳，默认600秒（10分钟）超时
        local processing_age=600
        if [ -n "$(grep "^agent:main:session:${session_id} [0-9]\+$" "$PROCESSING_FILE" 2>/dev/null)" ]; then
            local timestamp=$(grep "^agent:main:session:${session_id} [0-9]\+$" "$PROCESSING_FILE" | awk '{print $2}')
            local now=$(date +%s)
            processing_age=$((now - timestamp))
        fi
        if [ "$processing_age" -lt 1800 ]; then  # 30分钟超时
            log "跳过正在处理中的会话: $session_id (已处理 ${processing_age} 秒)"
            continue
        else
            log "警告: 会话处理超时（${processing_age} 秒），清理标记后重试"
            sed -i "/^agent:main:session:${session_id}/d" "$PROCESSING_FILE" 2>/dev/null
        fi
    fi
    
    # 发现未提炼会话！
    log "发现未提炼会话: $session_id"
    # 标记为正在处理中，防止其他检查进程重复处理
    echo "agent:main:session:${session_id} $(date +%s)" >> "$PROCESSING_FILE"
    
    # 发送通知（只在第一次发现时）
    send_notification "发现未提炼会话: $session_id，正在处理..."
    
    # ========== 真实调用 ==========
    # 后台运行提炼脚本，避免阻塞检查流程导致重复调用
    # 问题根源：AI提炼需要很长时间，如果同步调用/同进程等待，下一次检查会在提炼完成前触发，导致重复调用
    # 日志由cron统一记录到系统log，不在/tmp留存敏感的会话日志
    log "后台启动提炼脚本处理会话: $session_id"
    (
        # 执行提炼脚本
        "$DO_EXTRACT_SCRIPT" "$session_file"
        extract_exit_code=$?
        # 无论成功失败，都先从「正在处理」列表移除
        sed -i "/^agent:main:session:${session_id}/d" "$PROCESSING_FILE" 2>/dev/null
        # 提炼成功（含过滤跳过），标记到「已提炼」列表，下次直接跳过
        if [ $extract_exit_code -eq 0 ]; then
            echo "agent:main:session:${session_id}" >> "$EXTRACTED_FILE"
            log "会话处理完成: $session_id"
        else
            # 提炼失败，不标记到「已提炼」，下次检查会重试
            log "会话处理失败，下次重试: $session_id (退出码: $extract_exit_code)"
        fi
    ) &
    # 短暂等待，避免CPU争抢
    sleep 0.2
    # =============================

    # 注意：这里不等待提炼完成，标记工作交给后台进程
    # 通过「PROCESSING_FILE」保证同一个会话同一时间只会有一个提炼进程在运行
done

log "会话检查完成"
exit 0
