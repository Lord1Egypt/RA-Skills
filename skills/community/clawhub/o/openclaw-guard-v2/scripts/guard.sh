#!/bin/bash
# openclaw-guard.sh - OpenClaw 配置修改守护脚本 v2.0
# 用法: ./guard.sh [command]
# 命令: start|stop|status|test|check|clean|notify

set -e

# ===== 配置 =====
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config/settings.yaml"

# 默认配置
GUARD_TIMEOUT=180
BACKUP_DIR="$HOME/.openclaw/backups"
GATEWAY_SERVICE="openclaw-gateway"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
MAX_BACKUPS=5  # 最多保留最近 N 份备份

# 飞书通知配置
FEISHU_OPEN_ID=""  # 接收通知的用户 Open ID
FEISHU_ENABLED=false

# 需要备份的文件
BACKUP_FILES=(
    "$HOME/.openclaw/openclaw.json"
    "$WORKSPACE_DIR/AGENTS.md"
    "$WORKSPACE_DIR/SOUL.md"
    "$WORKSPACE_DIR/USER.md"
    "$WORKSPACE_DIR/MEMORY.md"
    "$WORKSPACE_DIR/TOOLS.md"
)

# 日志文件
LOG_FILE="$BACKUP_DIR/guard.log"
INCIDENT_LOG="$BACKUP_DIR/incident_log.txt"
PID_FILE="$BACKUP_DIR/guard.pid"
BACKUP_LIST="$BACKUP_DIR/backup_list.txt"  # 备份列表

# ===== 颜色 =====
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ===== 函数 =====
log() {
    echo -e "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date +%Y-%m-%d\ %H:%M:%S)] ❌ $1${NC}" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date +%Y-%m-%d\ %H:%M:%S)] ✅ $1${NC}" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[$(date +%Y-%m-%d\ %H:%M:%S)] ⚠️ $1${NC}" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}[$(date +%Y-%m-%d\ %H:%M:%S)] ℹ️ $1${NC}" | tee -a "$LOG_FILE"
}

# 加载配置
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        GUARD_TIMEOUT=$(grep "guard_timeout:" "$CONFIG_FILE" | awk '{print $2}' || echo "180")
        BACKUP_DIR=$(grep "backup_dir:" "$CONFIG_FILE" | awk '{print $2}' | tr -d ' ' || echo "$HOME/.openclaw/backups")
        GATEWAY_SERVICE=$(grep "gateway_service:" "$CONFIG_FILE" | awk '{print $2}' || echo "openclaw-gateway")
        MAX_BACKUPS=$(grep "max_backups:" "$CONFIG_FILE" | awk '{print $2}' || echo "5")
        FEISHU_OPEN_ID=$(grep "feishu_open_id:" "$CONFIG_FILE" | awk '{print $2}' | tr -d ' ' || echo "")
        FEISHU_ENABLED=$(grep "feishu_enabled:" "$CONFIG_FILE" | awk '{print $2}' | tr -d ' ' || echo "false")
    fi
    
    # 更新路径变量
    BACKUP_LIST="$BACKUP_DIR/backup_list.txt"
}

# 创建备份目录
ensure_dirs() {
    mkdir -p "$BACKUP_DIR"
}

# 发送飞书通知
send_feishu() {
    local title="$1"
    local message="$2"
    
    if [ "$FEISHU_ENABLED" != "true" ] || [ -z "$FEISHU_OPEN_ID" ]; then
        log_info "飞书通知未配置，跳过"
        return 0
    fi
    
    openclaw message send \
        --channel feishu \
        --target "$FEISHU_OPEN_ID" \
        --message "$message" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        log_success "飞书通知已发送: $title"
    else
        log_error "飞书通知发送失败"
    fi
}

# 清理旧备份（保留最近 N 份）
cleanup_old_backups() {
    # 确保列表文件存在
    if [ ! -f "$BACKUP_LIST" ]; then
        touch "$BACKUP_LIST"
        return 0
    fi
    
    # 获取备份数量
    local backup_count=$(wc -l < "$BACKUP_LIST" | tr -d ' ')
    
    if [ "$backup_count" -le "$MAX_BACKUPS" ]; then
        log_info "当前备份数 ($backup_count) <= 最大备份数 ($MAX_BACKUPS)，无需清理"
        return 0
    fi
    
    # 计算需要删除的数量
    local to_delete=$((backup_count - MAX_BACKUPS))
    log_info "清理旧备份: 需要删除 $to_delete 份"
    
    # 获取要删除的旧备份（从头开始删除）
    local deleted=0
    while [ "$deleted" -lt "$to_delete" ]; do
        local old_backup=$(head -n 1 "$BACKUP_LIST")
        
        if [ -n "$old_backup" ] && [ -d "$old_backup" ]; then
            rm -rf "$old_backup"
            log "🗑️ 已删除旧备份: $old_backup"
        fi
        
        # 从列表中移除
        tail -n +2 "$BACKUP_LIST" > "$BACKUP_LIST.tmp"
        mv "$BACKUP_LIST.tmp" "$BACKUP_LIST"
        
        deleted=$((deleted + 1))
    done
    
    log_success "清理完成，保留最新 $MAX_BACKUPS 份备份"
}

# 备份配置文件（多级备份）
backup_configs() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_subdir="$BACKUP_DIR/backup_$timestamp"
    mkdir -p "$backup_subdir"
    
    local backed_up=0
    for file in "${BACKUP_FILES[@]}"; do
        if [ -f "$file" ]; then
            cp "$file" "$backup_subdir/"
            backed_up=$((backed_up + 1))
            log "📦 已备份: $file"
        fi
    done
    
    # 记录最新备份
    echo "$backup_subdir" > "$BACKUP_DIR/latest_backup"
    echo "$timestamp" > "$BACKUP_DIR/latest_backup_time"
    
    # 添加到备份列表（新增的在最后）
    echo "$backup_subdir" >> "$BACKUP_LIST"
    
    # 清理旧备份
    cleanup_old_backups
    
    log_success "完成备份: $backed_up 个文件"
    echo "$backup_subdir"
}

# 列出所有可用备份
list_backups() {
    if [ ! -f "$BACKUP_LIST" ]; then
        echo "暂无备份记录"
        return
    fi
    
    echo "=== 可用备份列表 (最新 $MAX_BACKUPS 份) ==="
    local index=1
    tac "$BACKUP_LIST" | while read -r backup; do
        if [ -d "$backup" ]; then
            local time=$(basename "$backup" | sed 's/backup_//')
            echo "  $index. $backup (创建时间: $time)"
            index=$((index + 1))
        fi
    done
}

# 恢复到指定备份
restore_backup() {
    local backup_path="$1"
    
    if [ -z "$backup_path" ] || [ ! -d "$backup_path" ]; then
        log_error "无效的备份路径: $backup_path"
        return 1
    fi
    
    log_warn "🔄 恢复到备份: $backup_path"
    
    # 恢复配置文件
    for file in "$backup_path"/*; do
        if [ -f "$file" ]; then
            local filename=$(basename "$file")
            local target=""
            case "$filename" in
                openclaw.json) target="$HOME/.openclaw/openclaw.json" ;;
                AGENTS.md|SOUL.md|USER.md|MEMORY.md|TOOLS.md) target="$WORKSPACE_DIR/$filename" ;;
                *) target="$BACKUP_DIR/$filename" ;;
            esac
            if [ -n "$target" ]; then
                cp "$file" "$target"
                log "🔄 已恢复: $filename -> $target"
            fi
        fi
    done
    
    # 重启 Gateway
    log "🔁 重启 Gateway..."
    if systemctl --user restart "$GATEWAY_SERVICE" 2>/dev/null; then
        log_success "Gateway 重启完成"
    elif openclaw gateway start 2>/dev/null; then
        log_success "Gateway 启动完成"
    else
        log_error "Gateway 启动失败，需要手动处理"
    fi
    
    log_success "恢复完成"
}

# 启动守护
do_start() {
    local timeout=${1:-$GUARD_TIMEOUT}
    
    # 检查是否已在运行
    if [ -f "$PID_FILE" ]; then
        local old_pid=$(cat "$PID_FILE")
        if kill -0 "$old_pid" 2>/dev/null; then
            log_error "守护进程已在运行 (PID: $old_pid)"
            exit 1
        else
            rm -f "$PID_FILE"
        fi
    fi
    
    ensure_dirs
    
    # 飞书通知：守护启动
    send_feishu "守护启动" "🛡️ 守护脚本已启动
⏱️ 监控时间: ${timeout} 秒
📁 备份目录: $BACKUP_DIR"
    
    # 备份当前配置
    log "🛡️ 守护启动，${timeout}秒后检查..."
    backup_configs
    
    # 记录 PID
    echo $$ > "$PID_FILE"
    echo "$timeout" > "$BACKUP_DIR/guard_timeout"
    echo "$(date +%s)" > "$BACKUP_DIR/guard_start_time"
    
    # trap 确保日志写入
    trap 'handle_signal' SIGTERM SIGINT
    
    # 等待
    log "💤 等待 ${timeout} 秒..."
    sleep $timeout
    
    # 检查是否需要回滚
    if [ -f "$PID_FILE" ]; then
        do_rollback
    else
        log "守护已手动停止"
    fi
}

# 信号处理
handle_signal() {
    # 检查是否已超时
    local current_time=$(date +%s)
    local start_time=$(cat "$BACKUP_DIR/guard_start_time" 2>/dev/null || echo "0")
    local timeout=$(cat "$BACKUP_DIR/guard_timeout" 2>/dev/null || echo "180")
    
    if [ -n "$start_time" ] && [ "$start_time" != "0" ]; then
        local elapsed=$((current_time - start_time))
        # 如果已经过了超时时间，执行回滚
        if [ "$elapsed" -ge "$timeout" ]; then
            log_warn "被外部中断且已超时，执行回滚..."
            echo "$(date +%Y-%m-%d\ %H:%M:%S) - 被外部中断且已超时，执行回滚" >> "$INCIDENT_LOG"
            do_rollback
            exit 0
        fi
    fi
    
    # 否则正常退出
    log_warn "收到中断信号，守护退出"
    
    # 飞书通知：守护停止
    send_feishu "守护停止" "🛡️ 守护脚本已手动停止"
    
    rm -f "$PID_FILE" "$BACKUP_DIR/guard_start_time"
    exit 0
}

# 执行回滚
do_rollback() {
    log_warn "⏰ 时间到，执行回滚..."
    
    # 飞书通知：开始回滚
    send_feishu "⚠️ 触发回滚" "🛡️ 守护脚本检测到超时，准备执行回滚...
📁 备份目录: $(cat "$BACKUP_DIR/latest_backup" 2>/dev/null)"
    
    local latest_backup=$(cat "$BACKUP_DIR/latest_backup" 2>/dev/null)
    
    if [ -z "$latest_backup" ] || [ ! -d "$latest_backup" ]; then
        log_error "找不到备份目录！"
        echo "$(date +%Y-%m-%d\ %H:%M:%S) - 回滚失败：找不到备份" >> "$INCIDENT_LOG"
        
        # 飞书通知：回滚失败
        send_feishu "❌ 回滚失败" "❌ 找不到备份目录，回滚失败！
⏰ 时间: $(date '+%Y-%m-%d %H:%M:%S')"
        
        rm -f "$PID_FILE"
        exit 1
    fi
    
    # 恢复配置文件
    for file in "$latest_backup"/*; do
        if [ -f "$file" ]; then
            local filename=$(basename "$file")
            local target=""
            case "$filename" in
                openclaw.json) target="$HOME/.openclaw/openclaw.json" ;;
                AGENTS.md|SOUL.md|USER.md|MEMORY.md|TOOLS.md) target="$WORKSPACE_DIR/$filename" ;;
                *) target="$BACKUP_DIR/$filename" ;;
            esac
            if [ -n "$target" ]; then
                cp "$file" "$target"
                log "🔄 已恢复: $filename -> $target"
            fi
        fi
    done
    
    # 重启 Gateway
    log "🔁 重启 Gateway..."
    local restart_result="失败"
    if systemctl --user restart "$GATEWAY_SERVICE" 2>/dev/null; then
        restart_result="成功"
        log_success "Gateway 重启完成"
    elif openclaw gateway start 2>/dev/null; then
        restart_result="成功"
        log_success "Gateway 启动完成"
    else
        log_error "Gateway 启动失败，需要手动处理"
    fi
    
    # 记录事件
    echo "$(date +%Y-%m-%d\ %H:%M:%S) - 守护回滚触发，已恢复配置" >> "$INCIDENT_LOG"
    
    # 飞书通知：回滚完成
    send_feishu "✅ 回滚完成" "🛡️ 守护脚本回滚执行完成
📋 恢复结果: $restart_result
📁 备份来源: $latest_backup
⏰ 时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # 清理
    rm -f "$PID_FILE"
    log_success "回滚完成"
}

# 停止守护
do_stop() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            
            # 飞书通知：守护停止
            send_feishu "守护停止" "🛡️ 守护进程已手动停止"
            
            log_success "守护进程已停止"
        fi
        rm -f "$PID_FILE"
    else
        log_warn "守护进程未运行"
    fi
}

# 查看状态
do_status() {
    echo "=== 🛡️ OpenClaw Guard 状态 ==="
    
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            local timeout=$(cat "$BACKUP_DIR/guard_timeout" 2>/dev/null || echo "unknown")
            echo -e "${GREEN}🛡️ 守护运行中 (PID: $pid, 超时: ${timeout}s)${NC}"
        else
            echo -e "${YELLOW}⚠️ PID 文件存在但进程已终止${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo "🛡️ 守护未运行"
    fi
    
    # 显示最近备份
    if [ -f "$BACKUP_DIR/latest_backup" ]; then
        local latest=$(cat "$BACKUP_DIR/latest_backup")
        local time=$(cat "$BACKUP_DIR/latest_backup_time" 2>/dev/null || echo "unknown")
        echo "📦 最近备份: $latest (时间: $time)"
    fi
    
    # 显示备份数量
    if [ -f "$BACKUP_LIST" ]; then
        local backup_count=$(wc -l < "$BACKUP_LIST" | tr -d ' ')
        echo "📊 备份总数: $backup_count / $MAX_BACKUPS"
    fi
    
    # 显示飞书配置
    echo ""
    echo "=== 飞书通知配置 ==="
    if [ "$FEISHU_ENABLED" = "true" ] && [ -n "$FEISHU_OPEN_ID" ]; then
        echo -e "${GREEN}✅ 已启用${NC} (接收者: $FEISHU_OPEN_ID)"
    else
        echo "❌ 未启用"
    fi
    
    # 列出所有备份
    echo ""
    list_backups
}

# 测试回滚功能
do_test() {
    log "🧪 测试模式：10 秒后执行回滚..."
    do_start 10
}

# 健康检查：验证 Gateway 是否真正可用
do_health_check() {
    local url="http://127.0.0.1:18789/health"
    local timeout=5
    
    # 检查端口是否开放
    if ! nc -z localhost 18789 2>/dev/null; then
        echo -e "${RED}❌ Gateway 端口未开放${NC}"
        return 1
    fi
    
    # 检查 API 是否响应
    local response=$(curl -s -m $timeout "$url" 2>/dev/null)
    if echo "$response" | grep -q '"ok":true'; then
        echo -e "${GREEN}✅ Gateway API 正常${NC}"
        return 0
    else
        echo -e "${RED}❌ Gateway API 无响应${NC}"
        return 1
    fi
}

# 检查 Gateway 状态
do_check() {
    if systemctl --user is-active --quiet "$GATEWAY_SERVICE"; then
        echo -e "${GREEN}✅ Gateway 运行正常${NC}"
        exit 0
    else
        echo -e "${RED}❌ Gateway 未运行，尝试重启...${NC}"
        systemctl --user restart "$GATEWAY_SERVICE" 2>/dev/null || openclaw gateway start 2>/dev/null
        exit 1
    fi
}

# 清理旧备份
do_clean() {
    local days=${1:-30}
    log "🧹 清理 ${days} 天前的备份..."
    find "$BACKUP_DIR" -type d -name "backup_*" -mtime +$days -exec rm -rf {} \; 2>/dev/null
    
    # 重建备份列表
    find "$BACKUP_DIR" -type d -name "backup_*" -printf "%T@ %p\n" 2>/dev/null | \
        sort -rn | cut -d' ' -f2- > "$BACKUP_LIST"
    
    log_success "清理完成"
}

# 手动触发通知测试
do_notify_test() {
    send_feishu "🧪 测试通知" "🛡️ 守护脚本通知测试
⏰ 时间: $(date '+%Y-%m-%d %H:%M:%S')"
}

# 恢复到指定备份
do_restore() {
    if [ -z "$2" ]; then
        echo "用法: $0 restore <backup_path>"
        echo ""
        list_backups
        exit 1
    fi
    
    restore_backup "$2"
}

# ===== 主逻辑 =====
load_config
ensure_dirs

case "${1:-}" in
    start)
        do_start "$2"
        ;;
    stop)
        do_stop
        ;;
    status)
        do_status
        ;;
    test)
        do_test
        ;;
    check)
        do_check
        ;;
    clean)
        do_clean "$2"
        ;;
    restore)
        do_restore "$@"
        ;;
    notify)
        do_notify_test
        ;;
    list)
        list_backups
        ;;
    *)
        echo "用法: $0 {start|stop|status|test|check|clean|restore|notify|list}"
        echo ""
        echo "命令:"
        echo "  start [seconds]  启动守护（默认 3 分钟）"
        echo "  stop             停止守护"
        echo "  status           查看状态（含备份列表）"
        echo "  test             测试模式（10 秒后回滚）"
        echo "  check            检查 Gateway 状态"
        echo "  clean [days]     清理旧备份（默认 30 天）"
        echo "  restore <path>   恢复到指定备份"
        echo "  notify           测试飞书通知"
        echo "  list             列出所有可用备份"
        exit 1
        ;;
esac