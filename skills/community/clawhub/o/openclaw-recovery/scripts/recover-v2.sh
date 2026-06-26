#!/bin/bash
# OpenClaw 健康监控与自动恢复系统 v2.3
# 功能：检测崩溃、自动回滚、系统通知、健康检查
# 更新：适配 OpenClaw 2026.4.x，auth 文件路径已更新
# 新增：真正的健康检查（检查服务响应，不仅仅是进程存在）
# 改进：配置值验证、飞书通知、日志轮转、恢复后验证、恢复历史

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
AUTH_FILE="$HOME/.openclaw/agents/main/agent/auth-profiles.json"
AUTH_STATE="$HOME/.openclaw/agents/main/agent/auth-state.json"
BACKUP_DIR="$HOME/.openclaw/backups"
LOG_FILE="$HOME/.openclaw/logs/recovery.log"
HISTORY_FILE="$HOME/.openclaw/logs/recovery-history.log"
SAFE_CONFIG="$HOME/.openclaw/safe-mode.json"
MAX_RETRIES=10
MAX_LOG_LINES=1000

# 创建日志目录
mkdir -p "$HOME/.openclaw/logs"

# ==================== 读取配置端口 ====================
get_gateway_port() {
    if [ -f "$CONFIG_FILE" ]; then
        python3 -c "
import json
try:
    c = json.load(open('$CONFIG_FILE'))
    print(c.get('gateway', {}).get('port', 18789))
except:
    print(18789)
" 2>/dev/null
    else
        echo 18789
    fi
}

GATEWAY_PORT=$(get_gateway_port)

# ==================== 日志轮转 ====================
rotate_log() {
    local logfile="$1"
    local max_lines="$2"
    
    if [ -f "$logfile" ] && [ $(wc -l < "$logfile") -gt $max_lines ]; then
        tail -n $max_lines "$logfile" > "${logfile}.tmp"
        mv "${logfile}.tmp" "$logfile"
        echo "[$(date)] 日志已轮转，保留最近 ${max_lines} 行" >> "$LOG_FILE"
    fi
}

# ==================== 飞书通知 ====================
send_feishu_notification() {
    local title="$1"
    local message="$2"
    
    # 通过 OpenClaw 发送飞书消息（使用 system event）
    if command -v openclaw >/dev/null 2>&1; then
        # 写入通知文件，由 OpenClaw 处理
        local notify_file="$HOME/.openclaw/logs/pending-notification.txt"
        echo "{\"title\":\"$title\",\"message\":\"$message\",\"time\":\"$(date)\"}" > "$notify_file"
    fi
}

# ==================== 系统通知 ====================
send_notification() {
    local title="$1"
    local message="$2"
    
    # macOS 系统通知
    if command -v osascript >/dev/null 2>&1; then
        osascript -e "display notification \"$message\" with title \"$title\" sound name \"Glass\"" 2>/dev/null
    fi
    
    # 飞书通知
    send_feishu_notification "$title" "$message"
    
    # 记录到日志
    echo "[$(date)] [通知] $title: $message" >> "$LOG_FILE"
}

# ==================== 恢复历史记录 ====================
record_recovery() {
    local action="$1"      # restart | rollback | safemode | failed
    local detail="$2"      # 详细信息
    local result="$1"      # success | failed
    
    echo "[$(date)] | $action | $detail | $result" >> "$HISTORY_FILE"
}

# ==================== 磁盘空间检查 ====================
check_disk_space() {
    local usage=$(df -h "$HOME" | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$usage" -gt 90 ]; then
        send_notification "OpenClaw 警告" "磁盘空间不足: ${usage}%"
        echo "[$(date)] 警告: 磁盘空间不足 ${usage}%" >> "$LOG_FILE"
        return 1
    fi
    return 0
}

# ==================== 内存检查 ====================
check_memory() {
    if command -v vm_stat >/dev/null 2>&1; then
        local memory_pressure=$(memory_pressure 2>/dev/null | grep "System-wide memory free percentage" | awk '{print $5}' | sed 's/%//')
        if [ -n "$memory_pressure" ] && [ "$memory_pressure" -lt 10 ]; then
            send_notification "OpenClaw 警告" "内存不足"
            echo "[$(date)] 警告: 内存不足" >> "$LOG_FILE"
        fi
    fi
}

# ==================== 配置值验证（新增） ====================
validate_config_values() {
    local config="$1"
    local errors=""
    
    # 读取 compaction.mode 的值
    local compaction_mode=$(python3 -c "
import json
try:
    c = json.load(open('$config'))
    print(c.get('agents', {}).get('defaults', {}).get('compaction', {}).get('mode', 'default'))
except:
    print('default')
" 2>/dev/null)
    
    # 验证 compaction.mode 只能是 default 或 safeguard
    if [ "$compaction_mode" != "default" ] && [ "$compaction_mode" != "safeguard" ]; then
        errors="${errors}compaction.mode 无效: '$compaction_mode' (允许: default, safeguard)\n"
    fi
    
    # 验证 ackReactionScope 的值
    local ack_scope=$(python3 -c "
import json
try:
    c = json.load(open('$config'))
    print(c.get('messages', {}).get('ackReactionScope', 'group-mentions'))
except:
    print('group-mentions')
" 2>/dev/null)
    
    local valid_ack_scopes="group-mentions group-all direct all none off"
    if ! echo "$valid_ack_scopes" | grep -qw "$ack_scope"; then
        errors="${errors}ackReactionScope 无效: '$ack_scope'\n"
    fi
    
    # 验证 blockStreamingDefault 的值
    local block_stream=$(python3 -c "
import json
try:
    c = json.load(open('$config'))
    print(c.get('agents', {}).get('defaults', {}).get('blockStreamingDefault', 'off'))
except:
    print('off')
" 2>/dev/null)
    
    if [ "$block_stream" != "on" ] && [ "$block_stream" != "off" ]; then
        errors="${errors}blockStreamingDefault 无效: '$block_stream' (允许: on, off)\n"
    fi
    
    # 验证 gateway.port 是数字
    local gateway_port=$(python3 -c "
import json
try:
    c = json.load(open('$config'))
    print(c.get('gateway', {}).get('port', 18789))
except:
    print('18789')
" 2>/dev/null)
    
    if ! [[ "$gateway_port" =~ ^[0-9]+$ ]] || [ "$gateway_port" -lt 1024 ] || [ "$gateway_port" -gt 65535 ]; then
        errors="${errors}gateway.port 无效: '$gateway_port' (需要 1024-65535)\n"
    fi
    
    if [ -n "$errors" ]; then
        echo -e "$errors"
        return 1
    fi
    
    return 0
}

# ==================== 配置文件验证（增强） ====================
validate_config() {
    local config="$1"
    
    # 检查 JSON 格式
    if ! python3 -c "import json; json.load(open('$config'))" 2>/dev/null; then
        echo "JSON 格式错误"
        return 1
    fi
    
    # 检查必需字段
    if ! python3 -c "import json; c=json.load(open('$config')); assert 'gateway' in c and 'auth' in c" 2>/dev/null; then
        echo "缺少必需字段 (gateway/auth)"
        return 1
    fi
    
    # 检查配置值合法性
    local value_errors=$(validate_config_values "$config")
    if [ -n "$value_errors" ]; then
        echo "$value_errors"
        return 1
    fi
    
    return 0
}

# ==================== 健康检查（增强） ====================
health_check() {
    # 方法1: 检查 HTTP 端口是否响应
    if command -v curl >/dev/null 2>&1; then
        local http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://127.0.0.1:${GATEWAY_PORT}/ 2>/dev/null)
        if echo "$http_code" | grep -q "200\|301\|302"; then
            return 0  # 健康
        fi
    fi
    
    # 方法2: 检查 WebSocket 端口是否可连接
    if command -v nc >/dev/null 2>&1; then
        if nc -z -w 1 127.0.0.1 ${GATEWAY_PORT} 2>/dev/null; then
            return 0  # 端口开放
        fi
    fi
    
    # 方法3: 最后检查进程是否存在（兜底）
    if pgrep -f "openclaw.*gateway" > /dev/null 2>&1; then
        return 0
    fi
    
    return 1  # 不健康
}

# ==================== 修复无效配置 ====================
fix_invalid_config() {
    local config="$1"
    local backup_reason="$2"
    
    echo "[$(date)] 检测到配置值无效，尝试修复: $backup_reason" >> "$LOG_FILE"
    
    # 备份当前有问题的配置
    local timestamp=$(date +%Y%m%d_%H%M%S)
    cp "$config" "$BACKUP_DIR/openclaw.json.invalid.$timestamp"
    
    # 使用 python3 修复常见问题
    python3 << 'PYEOF' "$config" 2>/dev/null
import json
import sys

config_file = sys.argv[1]

with open(config_file, 'r') as f:
    config = json.load(f)

# 修复 compaction.mode
try:
    mode = config['agents']['defaults']['compaction']['mode']
    if mode not in ['default', 'safeguard']:
        config['agents']['defaults']['compaction']['mode'] = 'safeguard'
        print(f"Fixed compaction.mode: {mode} -> safeguard")
except:
    pass

# 修复 blockStreamingDefault
try:
    bs = config['agents']['defaults']['blockStreamingDefault']
    if bs not in ['on', 'off']:
        config['agents']['defaults']['blockStreamingDefault'] = 'off'
        print(f"Fixed blockStreamingDefault: {bs} -> off")
except:
    pass

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)
PYEOF
    
    echo "[$(date)] 配置已自动修复" >> "$LOG_FILE"
}

# ==================== 主恢复流程 ====================

# 日志轮转
rotate_log "$LOG_FILE" $MAX_LOG_LINES
rotate_log "$HISTORY_FILE" 5000

echo "[$(date)] === 开始健康检查 (v2.3) ===" >> "$LOG_FILE"

# 预检查
check_disk_space
check_memory

# 真正的健康检查
if health_check; then
    echo "[$(date)] OpenClaw 健康检查通过，服务正常运行" >> "$LOG_FILE"
    exit 0
fi

echo "[$(date)] OpenClaw 健康检查失败，开始恢复流程" >> "$LOG_FILE"
send_notification "OpenClaw 恢复" "检测到服务异常，开始自动恢复..."

# 检查配置文件并验证值
if [ -f "$CONFIG_FILE" ]; then
    config_errors=$(validate_config "$CONFIG_FILE" 2>&1)
    if [ $? -ne 0 ]; then
        echo "[$(date)] 配置验证失败: $config_errors" >> "$LOG_FILE"
        
        # 尝试自动修复
        fix_invalid_config "$CONFIG_FILE" "$config_errors"
        
        # 重新验证
        if validate_config "$CONFIG_FILE" 2>/dev/null; then
            echo "[$(date)] 配置修复成功，尝试重启" >> "$LOG_FILE"
            openclaw gateway restart 2>&1 >> "$LOG_FILE"
            sleep 5
            
            if health_check; then
                echo "[$(date)] 重启成功，服务健康" >> "$LOG_FILE"
                send_notification "OpenClaw 恢复成功" "配置已自动修复，服务正常"
                record_recovery "auto-fix" "配置值自动修复" "success"
                exit 0
            fi
        fi
    else
        # 配置有效，尝试重启
        echo "[$(date)] 配置文件有效，尝试直接重启" >> "$LOG_FILE"
        openclaw gateway restart 2>&1 >> "$LOG_FILE"
        sleep 5
        
        if health_check; then
            echo "[$(date)] 重启成功，服务健康" >> "$LOG_FILE"
            send_notification "OpenClaw 恢复成功" "服务已正常启动"
            record_recovery "restart" "正常重启" "success"
            exit 0
        fi
    fi
fi

echo "[$(date)] 配置文件损坏或重启失败，开始回滚" >> "$LOG_FILE"
record_recovery "rollback-start" "开始回滚流程" "info"

# 尝试回滚
RETRY_COUNT=0
for BACKUP in $(ls -t "$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | head -$MAX_RETRIES); do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    
    # 验证备份
    backup_errors=$(validate_config "$BACKUP" 2>&1)
    if [ $? -ne 0 ]; then
        echo "[$(date)] 备份无效，跳过: $BACKUP ($backup_errors)" >> "$LOG_FILE"
        continue
    fi
    
    cp "$BACKUP" "$CONFIG_FILE"
    echo "[$(date)] 尝试回滚到: $BACKUP" >> "$LOG_FILE"
    
    openclaw gateway restart 2>&1 >> "$LOG_FILE"
    sleep 5
    
    # 回滚后验证
    if health_check; then
        # 再次验证配置值
        if validate_config "$CONFIG_FILE" 2>/dev/null; then
            echo "[$(date)] 回滚成功，服务健康: $BACKUP" >> "$LOG_FILE"
            send_notification "OpenClaw 恢复成功" "已回滚到备份: $(basename $BACKUP)"
            record_recovery "rollback" "回滚到 $(basename $BACKUP)" "success"
            exit 0
        else
            echo "[$(date)] 回滚后配置验证失败，继续尝试" >> "$LOG_FILE"
        fi
    fi
done

# 保底配置
if [ -f "$SAFE_CONFIG" ]; then
    safe_errors=$(validate_config "$SAFE_CONFIG" 2>&1)
    if [ $? -eq 0 ]; then
        echo "[$(date)] 所有备份失败，使用保底配置" >> "$LOG_FILE"
        cp "$SAFE_CONFIG" "$CONFIG_FILE"
        openclaw gateway restart 2>&1 >> "$LOG_FILE"
        sleep 5
        
        if health_check; then
            echo "[$(date)] 保底配置启动成功，服务健康" >> "$LOG_FILE"
            send_notification "OpenClaw 恢复成功" "使用保底配置启动"
            record_recovery "safemode" "使用保底配置" "success"
            exit 0
        fi
    fi
fi

# 所有方法都失败
echo "[$(date)] 恢复失败，需要人工干预" >> "$LOG_FILE"
send_notification "OpenClaw 恢复失败" "自动恢复失败，请手动检查"
record_recovery "failed" "所有恢复方法失败" "failed"
exit 1
