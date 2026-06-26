#!/usr/bin/env bash
# OpenClaw Backup/Restore Logging Library
# Provides structured logging with levels, rotation, and audit trails

# Default configuration
BACKUP_LOG_LEVEL="${BACKUP_LOG_LEVEL:-INFO}"  # DEBUG, INFO, WARN, ERROR
BACKUP_LOG_FILE="${BACKUP_LOG_FILE:-${HOME}/.openclaw/logs/backup.log}"
BACKUP_LOG_MAX_SIZE="${BACKUP_LOG_MAX_SIZE:-10M}"  # Max log file size
BACKUP_LOG_MAX_FILES="${BACKUP_LOG_MAX_FILES:-5}"  # Number of rotated files
BACKUP_LOG_AUDIT="${BACKUP_LOG_AUDIT:-true}"       # Enable audit logging

# Ensure log directory exists
ensure_log_dir() {
    local log_dir
    log_dir=$(dirname "${BACKUP_LOG_FILE}")
    if [[ ! -d "${log_dir}" ]]; then
        mkdir -p "${log_dir}"
    fi
}

# Get current timestamp in ISO 8601 format
get_timestamp() {
    date +"%Y-%m-%dT%H:%M:%S%z"
}

# Get short timestamp for display
get_short_timestamp() {
    date +"%H:%M:%S"
}

# Log level numeric values
get_level_value() {
    case "${1^^}" in
        DEBUG) echo 0 ;;
        INFO)  echo 1 ;;
        WARN)  echo 2 ;;
        ERROR) echo 3 ;;
        *)     echo 1 ;;  # Default to INFO
    esac
}

# Check if level should be logged
should_log() {
    local msg_level="$1"
    local config_level
    config_level=$(get_level_value "${BACKUP_LOG_LEVEL}")
    local msg_level_val
    msg_level_val=$(get_level_value "${msg_level}")
    
    [[ ${msg_level_val} -ge ${config_level} ]]
}

# Rotate log files if needed (with file locking for concurrent safety)
rotate_logs() {
    if [[ ! -f "${BACKUP_LOG_FILE}" ]]; then
        return 0
    fi
    
    local lock_file="${BACKUP_LOG_FILE}.lock"
    local lock_fd=300
    
    # Try to acquire lock (non-blocking)
    eval "exec ${lock_fd}>\"${lock_file}\"" 2>/dev/null || return 0
    if ! flock -n "${lock_fd}" 2>/dev/null; then
        # Another process is rotating, skip
        eval "exec ${lock_fd}>&-" 2>/dev/null || true
        return 0
    fi
    
    # Check again after acquiring lock (another process might have rotated)
    if [[ ! -f "${BACKUP_LOG_FILE}" ]]; then
        flock -u "${lock_fd}" 2>/dev/null || true
        eval "exec ${lock_fd}>&-" 2>/dev/null || true
        return 0
    fi
    
    # Get current size in bytes
    local size
    size=$(stat -f%z "${BACKUP_LOG_FILE}" 2>/dev/null || stat -c%s "${BACKUP_LOG_FILE}" 2>/dev/null || echo 0)
    
    # Convert max size to bytes (simplified, assumes M)
    local max_size
    max_size=$(echo "${BACKUP_LOG_MAX_SIZE}" | sed 's/M/*1024*1024/' | sed 's/K/*1024/' | bc 2>/dev/null || echo 10485760)
    
    if [[ ${size} -gt ${max_size} ]]; then
        # Rotate existing files
        for i in $(seq $((BACKUP_LOG_MAX_FILES - 1)) -1 1); do
            if [[ -f "${BACKUP_LOG_FILE}.${i}" ]]; then
                mv "${BACKUP_LOG_FILE}.${i}" "${BACKUP_LOG_FILE}.$((i + 1))" 2>/dev/null || true
            fi
        done
        
        # Move current to .1
        mv "${BACKUP_LOG_FILE}" "${BACKUP_LOG_FILE}.1" 2>/dev/null || true
    fi
    
    # Release lock
    flock -u "${lock_fd}" 2>/dev/null || true
    eval "exec ${lock_fd}>&-" 2>/dev/null || true
}

# Write to log file
write_log() {
    local level="$1"
    local message="$2"
    local context="${3:-}"
    
    ensure_log_dir
    rotate_logs
    
    local timestamp
    timestamp=$(get_timestamp)
    
    local log_entry="[${timestamp}] [${level}] ${message}"
    
    # Add context if provided
    if [[ -n "${context}" ]]; then
        log_entry="${log_entry} | context: ${context}"
    fi
    
    # Append to log file
    echo "${log_entry}" >> "${BACKUP_LOG_FILE}"
}

# Core logging functions
log_debug() {
    local message="$1"
    local context="${2:-}"
    
    if should_log "DEBUG"; then
        write_log "DEBUG" "${message}" "${context}"
        echo -e "\033[90m[$(get_short_timestamp)] [DEBUG] ${message}\033[0m" >&2
    fi
}

log_info() {
    local message="$1"
    local context="${2:-}"
    
    if should_log "INFO"; then
        write_log "INFO" "${message}" "${context}"
        echo -e "\033[32m[$(get_short_timestamp)] [INFO] ${message}\033[0m"
    fi
}

log_warn() {
    local message="$1"
    local context="${2:-}"
    
    if should_log "WARN"; then
        write_log "WARN" "${message}" "${context}"
        echo -e "\033[33m[$(get_short_timestamp)] [WARN] ${message}\033[0m" >&2
    fi
}

log_error() {
    local message="$1"
    local context="${2:-}"
    
    if should_log "ERROR"; then
        write_log "ERROR" "${message}" "${context}"
        echo -e "\033[31m[$(get_short_timestamp)] [ERROR] ${message}\033[0m" >&2
    fi
}

# Operation logging - tracks start/end of operations
log_operation_start() {
    local operation="$1"
    local details="${2:-}"
    local op_id
    op_id=$(date +%s%N | cut -b1-13)
    
    export CURRENT_OP_ID="${op_id}"
    export CURRENT_OP_NAME="${operation}"
    export CURRENT_OP_START=$(date +%s)
    
    local context="op_id=${op_id}"
    [[ -n "${details}" ]] && context="${context}, ${details}"
    
    write_log "INFO" "operation_start: ${operation}" "${context}"
    log_info "开始: ${operation}"
    
    echo "${op_id}"
}

log_operation_end() {
    local status="$1"  # success, failed, cancelled
    local message="${2:-}"
    
    local op_id="${CURRENT_OP_ID:-unknown}"
    local op_name="${CURRENT_OP_NAME:-unknown}"
    local start_time="${CURRENT_OP_START:-0}"
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    local context="op_id=${op_id}, duration=${duration}s, status=${status}"
    [[ -n "${message}" ]] && context="${context}, ${message}"
    
    write_log "INFO" "operation_end: ${op_name}" "${context}"
    
    case "${status}" in
        success)
            log_info "完成: ${op_name} (耗时 ${duration}s)"
            ;;
        failed)
            log_error "失败: ${op_name} (耗时 ${duration}s)" "${message}"
            ;;
        cancelled)
            log_warn "取消: ${op_name} (耗时 ${duration}s)"
            ;;
    esac
    
    # Clear operation context
    unset CURRENT_OP_ID CURRENT_OP_NAME CURRENT_OP_START
}

# Audit logging - tracks security-sensitive operations
log_audit() {
    local action="$1"
    local resource="$2"
    local result="$3"
    local details="${4:-}"
    
    if [[ "${BACKUP_LOG_AUDIT}" != "true" ]]; then
        return 0
    fi
    
    local timestamp
    timestamp=$(get_timestamp)
    local user
    user=$(whoami)
    local hostname
    hostname=$(hostname)
    
    local audit_entry="[${timestamp}] [AUDIT] action=${action}, resource=${resource}, result=${result}, user=${user}, host=${hostname}"
    
    if [[ -n "${details}" ]]; then
        audit_entry="${audit_entry}, ${details}"
    fi
    
    # Write to separate audit log
    local audit_log
    audit_log=$(dirname "${BACKUP_LOG_FILE}")/audit.log
    echo "${audit_entry}" >> "${audit_log}"
}

# Log file operations
log_file_operation() {
    local operation="$1"  # create, modify, delete, read
    local file_path="$2"
    local size="${3:-}"
    
    local details="file=${file_path}"
    [[ -n "${size}" ]] && details="${details}, size=${size}"
    
    write_log "DEBUG" "file_${operation}" "${details}"
}

# Export log functions for use in other scripts
export -f log_debug log_info log_warn log_error
export -f log_operation_start log_operation_end
export -f log_audit log_file_operation
export -f ensure_log_dir rotate_logs write_log
export -f get_timestamp get_short_timestamp
export -f get_level_value should_log

# Show log history
show_log_history() {
    local lines="${1:-50}"
    local level_filter="${2:-}"
    
    if [[ ! -f "${BACKUP_LOG_FILE}" ]]; then
        echo "日志文件不存在: ${BACKUP_LOG_FILE}"
        return 1
    fi
    
    echo "══════════════════════════════════════════════════════════"
    echo "      📋 操作日志 (最近 ${lines} 条)"
    echo "══════════════════════════════════════════════════════════"
    echo ""
    
    if [[ -n "${level_filter}" ]]; then
        tail -n "${lines}" "${BACKUP_LOG_FILE}" | grep -E "\[${level_filter}\]" || echo "无匹配记录"
    else
        tail -n "${lines}" "${BACKUP_LOG_FILE}"
    fi
}

# Generate audit report
generate_audit_report() {
    local since="${1:-24h}"
    local audit_log
    audit_log=$(dirname "${BACKUP_LOG_FILE}")/audit.log
    
    echo "══════════════════════════════════════════════════════════"
    echo "      📊 审计报告 (since ${since})"
    echo "══════════════════════════════════════════════════════════"
    echo ""
    
    if [[ ! -f "${audit_log}" ]]; then
        echo "审计日志不存在"
        return 1
    fi
    
    # Count operations by type
    echo "操作统计:"
    grep "action=backup" "${audit_log}" 2>/dev/null | wc -l | xargs -I {} echo "  备份操作: {} 次"
    grep "action=restore" "${audit_log}" 2>/dev/null | wc -l | xargs -I {} echo "  恢复操作: {} 次"
    grep "action=export" "${audit_log}" 2>/dev/null | wc -l | xargs -I {} echo "  导出操作: {} 次"
    grep "result=success" "${audit_log}" 2>/dev/null | wc -l | xargs -I {} echo "  成功: {} 次"
    grep "result=failed" "${audit_log}" 2>/dev/null | wc -l | xargs -I {} echo "  失败: {} 次"
    
    echo ""
    echo "最近审计记录:"
    tail -n 20 "${audit_log}"
}
