#!/bin/bash
# IronClaw Guardian Evolved - 守护脚本
# 融合 IronClaw + Guardian + Security Guard 核心能力

set -e

# 配置
GUARDIAN_CHECK_INTERVAL=${GUARDIAN_CHECK_INTERVAL:-30}
GUARDIAN_MAX_FIX_ATTEMPTS=${GUARDIAN_MAX_FIX_ATTEMPTS:-3}
GUARDIAN_COOLDOWN=${GUARDIAN_COOLDOWN:-300}
LOG_FILE="/tmp/openclaw-guardian.log"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
AUDIT_LOG="$HOME/.openclaw/logs/ironclaw.audit.jsonl"

# 确保日志目录存在
mkdir -p "$(dirname "$AUDIT_LOG")"

# 日志函数
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

audit_log() {
  local event="$1"
  local details="$2"
  echo "{\"timestamp\":\"$(date -u '+%Y-%m-%dT%H:%M:%SZ')\",\"event\":\"$event\",\"details\":\"$details\"}" >> "$AUDIT_LOG"
}

# 检查 Gateway 状态
check_gateway() {
  if pgrep -f "openclaw.*gateway" > /dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

# 运行 doctor --fix
run_doctor_fix() {
  log "运行 openclaw doctor --fix..."
  if openclaw doctor --fix 2>&1 | tee -a "$LOG_FILE"; then
    return 0
  else
    return 1
  fi
}

# Git 回滚
git_rollback() {
  log "执行 git 回滚..."
  cd "$WORKSPACE_DIR"
  
  # 获取第 2 个新的非自动 commit
  local target_commit
  target_commit=$(git log --oneline --grep="auto" --invert-grep | sed -n '2p' | awk '{print $1}')
  
  if [ -z "$target_commit" ]; then
    log "未找到合适的回滚 commit，尝试回退到上一个"
    target_commit=$(git log --oneline | sed -n '2p' | awk '{print $1}')
  fi
  
  if [ -n "$target_commit" ]; then
    log "回滚到 commit: $target_commit"
    git reset --hard "$target_commit"
    audit_log "git_rollback" "rolled back to $target_commit"
    return 0
  else
    log "Git 回滚失败：未找到 commit"
    audit_log "git_rollback_failed" "no suitable commit found"
    return 1
  fi
}

# 重启 Gateway
restart_gateway() {
  log "重启 Gateway..."
  openclaw gateway restart
  audit_log "gateway_restart" "gateway restarted"
}

# 主监控循环
monitor_loop() {
  log "IronClaw Guardian Evolved 启动"
  log "检查间隔：${GUARDIAN_CHECK_INTERVAL}s, 最大修复：${GUARDIAN_MAX_FIX_ATTEMPTS}, 冷却：${GUARDIAN_COOLDOWN}s"
  
  local fix_attempts=0
  local cooldown_active=false
  
  while true; do
    if check_gateway; then
      # Gateway 正常运行
      fix_attempts=0
      cooldown_active=false
      sleep "$GUARDIAN_CHECK_INTERVAL"
      continue
    fi
    
    # Gateway 宕机
    log "⚠️ Gateway 宕机检测!"
    audit_log "gateway_down" "gateway detected as down"
    
    if [ "$cooldown_active" = true ]; then
      log "冷却期中，跳过修复"
      sleep "$GUARDIAN_CHECK_INTERVAL"
      continue
    fi
    
    # 尝试修复
    fix_attempts=$((fix_attempts + 1))
    log "修复尝试 #$fix_attempts / $GUARDIAN_MAX_FIX_ATTEMPTS"
    audit_log "doctor_fix_attempt" "attempt $fix_attempts"
    
    if run_doctor_fix; then
      log "✅ 修复成功"
      audit_log "doctor_fix_success" "fix succeeded on attempt $fix_attempts"
      fix_attempts=0
      sleep "$GUARDIAN_CHECK_INTERVAL"
      continue
    fi
    
    # 修复失败
    if [ "$fix_attempts" -ge "$GUARDIAN_MAX_FIX_ATTEMPTS" ]; then
      log "❌ 修复尝试耗尽，执行 git 回滚"
      audit_log "doctor_fix_exhausted" "exhausted $fix_attempts attempts, rolling back"
      
      if git_rollback; then
        restart_gateway
        fix_attempts=0
      else
        log "❌ 回滚失败，进入冷却期"
        audit_log "rollback_failed" "entering cooldown"
        cooldown_active=true
        sleep "$GUARDIAN_COOLDOWN"
      fi
    else
      sleep "$GUARDIAN_CHECK_INTERVAL"
    fi
  done
}

# 启动
monitor_loop
