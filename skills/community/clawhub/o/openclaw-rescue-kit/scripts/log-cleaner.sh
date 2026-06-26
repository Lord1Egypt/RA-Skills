#!/bin/bash
# ~/.openclaw/scripts/log-cleaner.sh
# OpenClaw 智能日志清理脚本
# 功能: 清理过期日志、Session 瘦身、每日日志管理

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
LOG_DIR="$OPENCLAW_HOME/logs"
SESSION_DIR="$OPENCLAW_HOME/agents/main/sessions"
MEMORY_DIR="$OPENCLAW_HOME/memory"
BACKUP_DIR="$OPENCLAW_HOME/backups"
LOG_FILE="$LOG_DIR/cleaner.log"

# 配置
KEEP_DAYS="${CLEANER_KEEP_DAYS:-7}"
KEEP_SESSION_RECORDS=200
SESSION_BACKUP_COUNT=5

mkdir -p "$LOG_DIR" "$BACKUP_DIR"

# 加载核心函数
source "$SCRIPT_DIR/core.sh"

# ==================== 字节格式化函数 ====================
format_bytes() {
    local bytes=$1
    if [ -z "$bytes" ] || ! [[ "$bytes" =~ ^[0-9]+$ ]] || [ "$bytes" -lt 0 ]; then
        echo "0B"
        return
    fi
    
    if command -v numfmt >/dev/null 2>&1; then
        numfmt --to=iec-i --suffix=B "$bytes" 2>/dev/null || echo "${bytes}B"
    else
        if [ "$bytes" -ge 1073741824 ]; then
            echo "$((bytes / 1073741824))GB"
        elif [ "$bytes" -ge 1048576 ]; then
            echo "$((bytes / 1048576))MB"
        elif [ "$bytes" -ge 1024 ]; then
            echo "$((bytes / 1024))KB"
        else
            echo "${bytes}B"
        fi
    fi
}

# ==================== 日志函数 ====================
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ==================== 文件日志清理 ====================
clean_file_logs() {
    log "========== 清理文件日志 =========="
    
    local deleted_count=0
    local freed_space=0
    
    # 查找并删除超过 KEEP_DAYS 天的日志文件
    while IFS= read -r -d '' file; do
        local size
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
        rm -f "$file"
        deleted_count=$((deleted_count + 1))
        freed_space=$((freed_space + size))
        log "  删除: $file ($(format_bytes $size))"
    done < <(find "$LOG_DIR" -maxdepth 1 -type f \( -name "*.log" -o -name "*.log.*" \) -mtime +$KEEP_DAYS -print0 2>/dev/null)
    
    # 压缩剩余的大日志文件
    find "$LOG_DIR" -maxdepth 1 -type f -name "*.log" -size +10M -not -name "*.gz" | while read -r file; do
        log "  压缩: $file"
        gzip -c "$file" > "$file.gz" && rm "$file"
    done
    
    log "文件日志清理完成: 删除 $deleted_count 个文件，释放约 $(format_bytes $freed_space)"
}

# ==================== Session 文件清理 ====================
clean_sessions() {
    log "========== 清理 Session 文件 =========="
    
    if [ ! -d "$SESSION_DIR" ]; then
        log "Session 目录不存在，跳过"
        return
    fi
    
    local total_shrunk=0
    
    # 查找所有 session 文件
    find "$SESSION_DIR" -name "*.jsonl" -type f | while read -r session_file; do
        local size_before size_after
        size_before=$(stat -f%z "$session_file" 2>/dev/null || stat -c%s "$session_file" 2>/dev/null || echo 0)
        
        # 根据文件大小执行不同策略
        local size_mb=$((size_before / 1024 / 1024))
        
        if [ "$size_mb" -lt 1 ]; then
            # < 1MB: 不处理
            continue
        elif [ "$size_mb" -lt 2 ]; then
            # 1-2MB: 保留最近 200 条
            clean_session_keep_recent "$session_file" 200
        elif [ "$size_mb" -lt 5 ]; then
            # 2-5MB: 保留 100 条，移除详细工具输出
            clean_session_summarize "$session_file" 100
        elif [ "$size_mb" -lt 10 ]; then
            # 5-10MB: 保留 50 条，精简
            clean_session_summarize "$session_file" 50
        else
            # > 10MB: 保留 30 条，激进精简
            log "  ⚠️ 超大文件: $(basename "$session_file") (${size_mb}MB)"
            clean_session_summarize "$session_file" 30
        fi
        
        size_after=$(stat -f%z "$session_file" 2>/dev/null || stat -c%s "$session_file" 2>/dev/null || echo 0)
        
        if [ "$size_after" -lt "$size_before" ]; then
            local saved=$((size_before - size_after))
            log "  压缩: $(basename "$session_file") ${size_mb}MB → $((size_after / 1024 / 1024))MB (节省 $(format_bytes $saved))"
            total_shrunk=$((total_shrunk + saved))
        fi
    done
    
    # 清理旧备份
    find "$SESSION_DIR" -name "*.jsonl.bak-*" -type f | \
        sort -t'-' -k4 -rn | \
        tail -n +$((SESSION_BACKUP_COUNT + 1)) | \
        xargs -r rm -f
    
    log "Session 清理完成，总共节省: $(format_bytes $total_shrunk)"
}

# 保留最近 N 条记录
clean_session_keep_recent() {
    local file="$1"
    local keep_count="$2"
    
    # 备份
    local timestamp
    timestamp=$(date '+%Y%m%d_%H%M%S')
    cp "$file" "${file}.bak-$timestamp"
    
    # 验证 JSON 格式
    if ! jq -s '.' "$file" >/dev/null 2>&1; then
        log "  ⚠️ JSON 格式无效，跳过: $file"
        mv "${file}.bak-$timestamp" "$file"
        return 1
    fi
    
    # 保留最近 N 行
    local total_lines
    total_lines=$(wc -l < "$file")
    
    if [ "$total_lines" -le "$keep_count" ]; then
        rm -f "${file}.bak-$timestamp"
        return 0
    fi
    
    local skip_lines=$((total_lines - keep_count))
    tail -n "+$((skip_lines + 1))" "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
    
    # 再次验证
    if ! jq -s '.' "$file" >/dev/null 2>&1; then
        log "  ⚠️ 清理后 JSON 格式无效，恢复备份"
        mv "${file}.bak-$timestamp" "$file"
        return 1
    fi
    
    rm -f "${file}.bak-$timestamp"
}

# 精简 Session（移除详细工具输出）
clean_session_summarize() {
    local file="$1"
    local keep_count="$2"
    
    # 备份
    local timestamp
    timestamp=$(date '+%Y%m%d_%H%M%S')
    cp "$file" "${file}.bak-$timestamp"
    
    # 验证 JSON 格式
    if ! jq -s '.' "$file" >/dev/null 2>&1; then
        log "  ⚠️ JSON 格式无效，跳过"
        mv "${file}.bak-$timestamp" "$file"
        return 1
    fi
    
    # 提取前 N 条消息，只保留关键字段
    local temp_file="/tmp/session_clean_$$.jsonl"
    
    # 读取前 N 条
    head -n "$keep_count" "$file" | while IFS= read -r line; do
        # 尝试简化每条消息
        echo "$line" | jq 'del(.tool_calls, .tool_results, .metadata)' 2>/dev/null || echo "$line"
    done > "$temp_file"
    
    if [ -s "$temp_file" ]; then
        mv "$temp_file" "$file"
    else
        mv "${file}.bak-$timestamp" "$file"
        rm -f "$temp_file"
    fi
    
    # 验证
    if ! jq -s '.' "$file" >/dev/null 2>&1; then
        log "  ⚠️ 清理后 JSON 格式无效，恢复备份"
        mv "${file}.bak-$timestamp" "$file"
        return 1
    fi
    
    rm -f "${file}.bak-$timestamp"
}

# ==================== 每日日志管理 ====================
clean_daily_logs() {
    log "========== 清理每日日志 =========="
    
    if [ ! -d "$MEMORY_DIR" ]; then
        log "Memory 目录不存在，跳过"
        return
    fi
    
    local archived=0
    
    # 只保留今天和昨天的 memory 文件
    local today yesterday
    today=$(date '+%Y-%m-%d')
    yesterday=$(date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d '1 day ago' '+%Y-%m-%d' 2>/dev/null)
    
    find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f | while read -r file; do
        local filename
        filename=$(basename "$file" .md)
        
        # 跳过保留的文件
        if [[ "$filename" == "$today" ]] || [[ "$filename" == "$yesterday" ]]; then
            continue
        fi
        
        # 跳过 MEMORY.md 等特殊文件
        if [[ "$filename" == "MEMORY" ]]; then
            continue
        fi
        
        # 压缩归档
        gzip -c "$file" > "${file}.gz" && rm "$file"
        archived=$((archived + 1))
        log "  归档: $filename.md"
    done
    
    # 检查 MEMORY.md 大小
    local memory_file="$MEMORY_DIR/MEMORY.md"
    if [ -f "$memory_file" ]; then
        local memory_size
        memory_size=$(stat -f%z "$memory_file" 2>/dev/null || stat -c%s "$memory_file" 2>/dev/null || echo 0)
        
        if [ "$memory_size" -gt 51200 ]; then
            log "  ⚠️ MEMORY.md 超过 50KB ($(format_bytes $memory_size))，建议手动整理"
        fi
    fi
    
    log "每日日志清理完成: 归档 $archived 个文件"
}

# ==================== 清理回滚备份 ====================
clean_rollback_backups() {
    local dry_run="${1:-false}"
    log "========== 清理回滚备份 =========="
    
    local rollback_dir="$BACKUP_DIR"
    local keep_count=10
    
    if [ ! -d "$rollback_dir" ]; then
        log "备份目录不存在，跳过"
        return
    fi
    
    # 统计 rollback 备份文件
    local rollback_files
    rollback_files=$(find "$rollback_dir" -maxdepth 1 -name "openclaw.json.rollback_*" -type f 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$rollback_files" -le "$keep_count" ]; then
        log "回滚备份: $rollback_files 个 (<= $keep_count)，无需清理"
        return
    fi
    
    local deleted_count=0
    local freed_space=0
    
    # 按时间排序，保留最新的 N 个，删除其余
    local to_delete
    to_delete=$(find "$rollback_dir" -maxdepth 1 -name "openclaw.json.rollback_*" -type f -print0 2>/dev/null | \
        xargs -0 stat -f "%m %N" 2>/dev/null | \
        sort -rn | \
        tail -n +$((keep_count + 1)) | \
        cut -d' ' -f2-)
    
    if [ -n "$to_delete" ]; then
        while IFS= read -r file; do
            if [ -f "$file" ]; then
                local size
                size=$(stat -f%z "$file" 2>/dev/null || echo 0)
                freed_space=$((freed_space + size))
                deleted_count=$((deleted_count + 1))
                if [ "$dry_run" = "true" ]; then
                    log "  [试运行] 删除: $(basename "$file")"
                else
                    log "  删除: $(basename "$file")"
                    rm -f "$file"
                fi
            fi
        done <<< "$to_delete"
    fi
    
    log "回滚备份清理完成: 保留 $keep_count 个，删除约 $deleted_count 个，释放 $(format_bytes $freed_space)"
    log "提示: Git 快照才是配置的真正安全网 (git-tag.sh)"
}

# ==================== 清理临时文件 ====================
clean_temp_files() {
    log "========== 清理临时文件 =========="
    
    local deleted=0
    
    # 清理 /tmp 中的 openclaw 临时文件
    find /tmp -name "openclaw*" -type f -mtime +1 -delete 2>/dev/null && deleted=$((deleted + 1)) || true
    
    # 清理浏览器缓存（可选）
    local browser_cache="$OPENCLAW_HOME/browser/openclaw/user-data/Default/Cache"
    if [ -d "$browser_cache" ]; then
        local cache_size
        cache_size=$(du -sb "$browser_cache" 2>/dev/null | awk '{print $1}')
        
        if [ -n "$cache_size" ] && [ "$cache_size" -gt 104857600 ] 2>/dev/null; then
            log "  浏览器缓存较大: $(format_bytes $cache_size)"
            # 不自动清理，让用户决定
        fi
    fi
    
    log "临时文件清理完成"
}

# ==================== 清理锁文件 ====================
clean_lock_files() {
    log "========== 清理过期锁文件 =========="
    
    find "$LOG_DIR" -maxdepth 1 -name "*.lock" -type f -mtime +1 -delete 2>/dev/null || true
    
    log "锁文件清理完成"
}

# ==================== 生成清理报告 ====================
generate_report() {
    local total_freed="${1:-0}"
    
    log "========== 清理报告 =========="
    log "总释放空间: $(format_bytes $total_freed)"
    log "=========================="
}

# ==================== 主函数 ====================
main() {
    local dry_run=false
    
    # 解析参数
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --dry-run)
                dry_run=true
                shift
                ;;
            --keep-days)
                KEEP_DAYS="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
    
    if [ "$dry_run" = true ]; then
        log "========== 试运行模式 (不实际删除) =========="
    fi
    
    log "========== 智能日志清理开始 =========="
    log "保留最近 ${KEEP_DAYS} 天的日志"
    
    # 执行各项清理
    clean_lock_files
    clean_file_logs
    clean_sessions
    clean_rollback_backups "$dry_run"
    clean_daily_logs
    clean_temp_files
    
    log "========== 智能日志清理完成 =========="
}

main "$@"
