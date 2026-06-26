#!/bin/bash
# Auto-Heal 通用守护脚本
# 用法: ./guard.sh services.json
# 依赖: jq (解析JSON)

set -e

CONFIG_FILE="${1:-services.json}"
LOG_FILE="/var/log/auto-heal.log"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_info()  { log "${GREEN}[INFO]${NC} $1"; }
log_warn()  { log "${YELLOW}[WARN]${NC} $1"; }
log_error() { log "${RED}[ERROR]${NC} $1"; }

# 检查依赖
check_deps() {
    if ! command -v jq &> /dev/null; then
        log_error "需要 jq，请先安装: apt install jq"
        exit 1
    fi
}

# 解析配置
parse_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        log_error "配置文件不存在: $CONFIG_FILE"
        exit 1
    fi
    
    SERVICE_COUNT=$(jq '.services | length' "$CONFIG_FILE")
    if [[ "$SERVICE_COUNT" -eq 0 ]]; then
        log_error "配置文件中没有定义服务"
        exit 1
    fi
    log_info "加载配置: $CONFIG_FILE ($SERVICE_COUNT 个服务)"
}

# 检测服务
check_service() {
    local name="$1"
    local check_type="$2"
    local check_config="$3"
    local timeout="${4:-5}"
    
    case "$check_type" in
        port)
            local port=$(echo "$check_config" | jq -r '.target')
            if ss -tlnp 2>/dev/null | grep -q ":${port} "; then
                return 0
            fi
            ;;
        process)
            local proc_name=$(echo "$check_config" | jq -r '.name')
            if pgrep -x "$proc_name" > /dev/null 2>&1; then
                return 0
            fi
            ;;
        http)
            local url=$(echo "$check_config" | jq -r '.url')
            local expected=$(echo "$check_config" | jq -r '.expected // "200"')
            local code=$(curl -s --connect-timeout "$timeout" --max-time "$timeout" -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
            if [[ "$code" == "$expected" ]]; then
                return 0
            fi
            ;;
        cmd)
            local cmd=$(echo "$check_config" | jq -r '.command')
            eval "$cmd" > /dev/null 2>&1
            return $?
            ;;
        *)
            log_warn "未知检测类型: $check_type"
            return 1
            ;;
    esac
    return 1
}

# 执行修复
do_fix() {
    local name="$1"
    local fix_cmd="$2"
    
    log_info "[$name] 执行修复..."
    eval "$fix_cmd" 2>&1 | while read line; do
        log "       $line"
    done
}

# 执行回滚
do_rollback() {
    local name="$1"
    local rollback_cmd="$2"
    local backup_dir="$3"
    
    # 自动备份（如果指定了备份目录）
    if [[ -n "$backup_dir" && -f "$CONFIG_FILE" ]]; then
        mkdir -p "$backup_dir"
        # 这里需要根据实际情况备份对应服务的配置文件
        # 通用回滚依赖用户自定义 rollback 命令
    fi
    
    if [[ -z "$rollback_cmd" ]]; then
        log_warn "[$name] 未定义回滚命令，跳过"
        return 1
    fi
    
    log_warn "[$name] 执行回滚..."
    eval "$rollback_cmd" 2>&1 | while read line; do
        log "       $line"
    done
}

# 自动备份
auto_backup() {
    local backup_dir="$1"
    local service_name="$2"
    local config_file="$3"
    
    if [[ -z "$backup_dir" ]]; then
        return
    fi
    
    mkdir -p "$backup_dir"
    local backup_file="${backup_dir}/${service_name}_$(date '+%Y%m%d_%H%M%S').json"
    if [[ -f "$config_file" ]]; then
        cp "$config_file" "$backup_file"
        log_info "[$service_name] 备份已保存: $backup_file"
        
        # 保留最近10份
        ls -1t "$backup_dir"/${service_name}_*.json 2>/dev/null | tail -n +11 | xargs -r rm -f
    fi
}

# 主流程
main() {
    check_deps
    parse_config
    
    log "=========================================="
    log_info "开始守护检查 ($(date '+%Y-%m-%d %H:%M:%S'))"
    log "=========================================="
    
    for i in $(seq 0 $((SERVICE_COUNT - 1))); do
        local service=$(jq ".services[$i]" "$CONFIG_FILE")
        local name=$(echo "$service" | jq -r '.name')
        local enabled=$(echo "$service" | jq -r '.enabled // true')
        
        # 跳过禁用的服务
        if [[ "$enabled" != "true" ]]; then
            log_info "[$name] 已禁用，跳过"
            continue
        fi
        
        local check_type=$(echo "$service" | jq -r '.check.type')
        local check_config=$(echo "$service" | jq -r '.check | to_entries | map("\(.key)=\(.value|tostring)") | join(" ")')
        local fix_cmd=$(echo "$service" | jq -r '.fix')
        local rollback_cmd=$(echo "$service" | jq -r '.rollback // empty')
        local timeout=$(echo "$service" | jq -r '.timeout // 5')
        local backup_dir=$(echo "$service" | jq -r '.backup_dir // empty')
        
        log_info "[$name] 检测中..."
        
        if check_service "$name" "$check_type" "$service" "$timeout"; then
            log_info "[$name] ✓ 检测正常"
        else
            log_warn "[$name] ✗ 检测失败，开始修复流程"
            
            # 修复
            do_fix "$name" "$fix_cmd"
            sleep 2
            
            if check_service "$name" "$check_type" "$service" "$timeout"; then
                log_info "[$name] ✓ 修复成功，服务已恢复"
            else
                # 修复失败，尝试回滚
                log_error "[$name] ✗ 修复失败，尝试回滚..."
                
                if [[ -n "$rollback_cmd" ]]; then
                    do_rollback "$name" "$rollback_cmd" "$backup_dir"
                    sleep 2
                    
                    if check_service "$name" "$check_type" "$service" "$timeout"; then
                        log_info "[$name] ✓ 回滚成功，服务已恢复"
                    else
                        log_error "[$name] ✗ 回滚失败，请人工介入！"
                    fi
                else
                    log_error "[$name] ✗ 无回滚命令，请人工介入！"
                fi
            fi
        fi
    done
    
    log "=========================================="
    log_info "守护检查完成"
    log "=========================================="
}

# 运行
main "$@"
