#!/bin/bash
#===============================================================================
# Plan Mode 集成到 OpenClaw 的示例
#
# 用法: 在 HEARTBEAT.md 或 Agent 启动时 source 此脚本
#
# 功能:
#   1. 定义危险命令检测函数
#   2. 定义确认发送函数
#   3. 定义执行拦截函数
#===============================================================================

# Plan Mode 状态
PLAN_MODE_ENABLED="${PLAN_MODE_ENABLED:-false}"
PLAN_MODE_STRICT="${PLAN_MODE_STRICT:-false}"

#===============================================================================
# 危险命令检测
#===============================================================================
plan_mode_is_dangerous() {
    local cmd="$1"
    
    # 高危命令
    [[ "$cmd" =~ rm[[:space:]]+-rf ]] && return 0
    [[ "$cmd" =~ rm[[:space:]]+-r ]] && return 0
    [[ "$cmd" =~ trash ]] && return 0
    [[ "$cmd" =~ kill[[:space:]] ]] && return 0
    [[ "$cmd" =~ pkill ]] && return 0
    [[ "$cmd" =~ "git push --force" ]] && return 0
    [[ "$cmd" =~ "git push -f" ]] && return 0
    [[ "$cmd" =~ shutdown ]] && return 0
    [[ "$cmd" =~ reboot ]] && return 0
    
    # 中危命令（严格模式下也危险）
    if [ "$PLAN_MODE_STRICT" = "true" ]; then
        [[ "$cmd" =~ curl[[:space:]] ]] && return 0
        [[ "$cmd" =~ wget[[:space:]] ]] && return 0
        [[ "$cmd" =~ "npm install" ]] && return 0
        [[ "$cmd" =~ "pip install" ]] && return 0
        [[ "$cmd" =~ "docker rm" ]] && return 0
    fi
    
    return 1
}

#===============================================================================
# 发送确认消息（需要适配企微 API）
#===============================================================================
plan_mode_send_confirm() {
    local cmd="$1"
    local risk="$2"
    
    # 这里应该调用企微 API 发送消息
    # 示例实现，实际使用时需要替换
    echo "⚠️ Plan Mode 确认"
    echo "命令: $cmd"
    echo "风险: $risk"
    echo "请回复 是 执行 / 否 取消"
    
    # 返回确认ID（用于后续判断）
    echo "confirm_$(date +%s)"
}

#===============================================================================
# 拦截执行（主要入口）
#===============================================================================
plan_mode_exec() {
    local cmd="$1"
    
    # Plan Mode 关闭
    [ "$PLAN_MODE_ENABLED" = "false" ] && {
        eval "$cmd"
        return $?
    }
    
    # 非危险命令，直接执行
    plan_mode_is_dangerous "$cmd" || {
        eval "$cmd"
        return $?
    }
    
    # 危险命令，需要确认
    local risk="high"
    local confirm_id=$(plan_mode_send_confirm "$cmd" "$risk")
    
    # 这里需要等待用户回复
    # 在实际实现中，应该将 confirm_id 存储，等待用户回复
    # 用户回复后根据结果决定是否执行
    
    echo "[Plan Mode] 等待用户确认..."
    return 1
}

#===============================================================================
# 在 HEARTBEAT 中调用
#===============================================================================
plan_mode_heartbeat_check() {
    # 检查是否有待确认的操作
    # 如果有，发送提醒
    
    local pending_confirms=$(ls ~/.openclaw/workspace/memory/activity/pending-*.json 2>/dev/null | wc -l)
    
    if [ "$pending_confirms" -gt 0 ]; then
        echo "⚠️ 有 $pending_confirms 个操作等待确认"
    fi
}

# 示例：在命令执行前调用
# plan_mode_exec "rm -rf /tmp/test" && echo "执行成功" || echo "执行失败或已取消"
