#!/usr/bin/env bash
# ========== gc-agent.sh ==========
# GC Agent - 自动化的垃圾收集与记忆归档
# 支持 --daemon（后台常驻）和 --once（单次执行）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS_DIR="${HARNESS_DIR:-.harness}"
CONFIG_FILE="${HARNESS_DIR}/config.json"

# GC Agent 配置（默认，可被 config.json 覆盖）
DAEMON_INTERVAL="${DAEMON_INTERVAL:-3600}"   # daemon 模式轮询间隔（秒）
GC_ENABLED="${GC_ENABLED:-1}"
GC_LOG_FILE="${HARNESS_DIR}/gc-agent.log"
LOCK_FILE="${HARNESS_DIR}/.gc-agent.lock"
DRY_RUN=1
VERBOSE=0
MODE="once"

# ---- 帮助 ----
usage() {
    cat <<EOF
gc-agent.sh - GC Agent 自动垃圾收集与记忆归档

Usage: gc-agent.sh [options]

Options:
  --once              单次执行 GC（默认）
  --daemon            后台常驻模式（按 interval 循环）
  --dry-run           干运行，不实际执行清理
  --run               实际执行（不加 --dry-run 时默认也是干运行）
  --verbose           显示详细日志
  --interval <secs>   daemon 模式轮询间隔（默认 3600 秒）
  --no-compress       跳过 memory 压缩
  --no-checkpoint     跳过检查点清理
  --no-report         跳过报告清理
  --no-trash          跳过 .trash 清理
  -h, --help          显示本帮助

Examples:
  gc-agent.sh --once                    # 单次干运行预览
  gc-agent.sh --once --dry-run          # 单次干运行（显式）
  gc-agent.sh --once --run              # 单次实际执行
  gc-agent.sh --daemon --interval 1800  # 后台常驻，每30分钟执行
  gc-agent.sh --daemon --run &          # 以后台守护进程启动（&可选）

GC 规则（config.json）:
  gc.enabled              是否启用 GC（默认 1）
  gc.max_checkpoints      每任务最大检查点数（默认 10）
  gc.max_age_days         检查点最大保留天数（默认 7）
  gc.report_retention     报告保留数量（默认 20）
  gc.compress_trigger_lines  memory 压缩触发行数（默认 200）
  gc.daemon_interval      daemon 轮询间隔秒数（默认 3600）
  gc.trash_retention_days .trash 永久删除天数（默认 30）
  gc.archive_priority     归档优先级：memory-palace | local（默认 memory-palace）
  gc.skip_compress        跳过 memory 压缩（默认 false）
  gc.skip_checkpoint       跳过检查点清理（默认 false）
  gc.skip_report           跳过报告清理（默认 false）

GC 日志: ${GC_LOG_FILE}
EOF
}

# ---- 解析参数 ----
while [[ $# -gt 0 ]]; do
    case "$1" in
        --once)       MODE="once"; shift ;;
        --daemon)     MODE="daemon"; shift ;;
        --dry-run)    DRY_RUN=1; shift ;;
        --run)        DRY_RUN=0; shift ;;
        --verbose)    VERBOSE=1; shift ;;
        --interval)   DAEMON_INTERVAL="$2"; shift 2 ;;
        --no-compress)   SKIP_COMPRESS=1; shift ;;
        --no-checkpoint) SKIP_CP=1; shift ;;
        --no-report)     SKIP_REPORT=1; shift ;;
        --no-trash)      SKIP_TRASH=1; shift ;;
        -h|--help)    usage; exit 0 ;;
        *)            shift ;;
    esac
done

# ---- 加载公共库 ----
source "${SCRIPT_DIR}/../lib/harness-core.sh"
require_init

# ---- 从 config.json 读取 GC 规则 ----
# 优先级：环境变量 > config.json > 硬编码默认值
get_gc_config() {
    local key="$1"
    local default="$2"
    local config_file="${HARNESS_DIR}/config.json"
    if [[ -f "$config_file" ]] && has_jq; then
        local val=$(jq -r ".$key // \"$default\"" "$config_file" 2>/dev/null)
        echo "${val:-$default}"
    else
        echo "$default"
    fi
}

GC_ENABLED=$(get_gc_config "gc.enabled" "$GC_ENABLED")
[[ "$GC_ENABLED" != "1" ]] && {
    [[ "$VERBOSE" == "1" ]] && log_info "GC disabled in config (gc.enabled=0)"
    exit 0
}

MAX_CP=$(get_gc_config "gc.max_checkpoints" 10)
MAX_AGE=$(get_gc_config "gc.max_age_days" 7)
REPORT_RETENTION=$(get_gc_config "gc.report_retention_count" 20)
COMPRESS_TRIGGER=$(get_gc_config "gc.compress_trigger_lines" 200)
TRASH_RETENTION=$(get_gc_config "gc.trash_retention_days" 30)
ARCHIVE_PRIORITY=$(get_gc_config "gc.archive_priority" "memory-palace")
SKIP_COMPRESS="${SKIP_COMPRESS:-$(get_gc_config "gc.skip_compress" "false")}"
SKIP_CP="${SKIP_CP:-$(get_gc_config "gc.skip_checkpoint" "false")}"
SKIP_REPORT="${SKIP_REPORT:-$(get_gc_config "gc.skip_report" "false")}"
SKIP_TRASH="${SKIP_TRASH:-$(get_gc_config "gc.skip_trash" "false")}"

# ---- 日志函数 ----
gc_agent_log() {
    local level="$1"
    local msg="$2"
    local ts=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$ts] [$level] $msg" >> "$GC_LOG_FILE"
    [[ "$VERBOSE" == "1" ]] && echo "[$level] $msg" || true
}

info()    { gc_agent_log "INFO" "$*"; }
warn()    { gc_agent_log "WARN" "$*" >&2; }
debug()   { [[ "$VERBOSE" == "1" ]] && gc_agent_log "DEBUG" "$*" || true; }

# ---- 分布式锁（防止多实例同时运行） ----
acquire_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        local pid=$(cat "$LOCK_FILE" 2>/dev/null)
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            warn "GC Agent already running (PID $pid), skipping this run"
            return 1
        else
            warn "Stale lock file found (PID $pid), removing..."
            rm -f "$LOCK_FILE"
        fi
    fi
    echo $$ > "$LOCK_FILE"
    return 0
}

release_lock() {
    rm -f "$LOCK_FILE"
}

# ---- Memory Palce 可用性检测 ----
MEMORY_PALACE_BIN="${MEMORY_PALACE_BIN:-/root/.openclaw/workspace/skills/memory-palace/bin/memory-palace.js}"

check_memory_palace() {
    if [[ ! -x "$MEMORY_PALACE_BIN" ]]; then
        debug "memory-palace not found at $MEMORY_PALACE_BIN"
        return 1
    fi
    OPENCLAW_WORKSPACE=/root/.openclaw/workspace node "$MEMORY_PALACE_BIN" stats &>/dev/null
    return $?
}

# ---- 触发 Memory 压缩 ----
# 返回 0 = 已压缩或无需压缩，1 = 执行了压缩
trigger_memory_compress() {
    [[ "$SKIP_COMPRESS" == "true" ]] || [[ "$SKIP_COMPRESS" == "1" ]] && {
        debug "Memory compression skipped (config)"
        return 0
    }

    local memory_file="${OPENCLAW_WORKSPACE:-/root/.openclaw/workspace}/MEMORY.md"
    [[ ! -f "$memory_file" ]] && {
        debug "MEMORY.md not found at $memory_file"
        return 0
    }

    local line_count=$(wc -l < "$memory_file" 2>/dev/null || echo 0)
    [[ $line_count -lt $COMPRESS_TRIGGER ]] && {
        debug "MEMORY.md is $line_count lines (threshold: $COMPRESS_TRIGGER), no compression needed"
        return 0
    }

    info "MEMORY.md has $line_count lines (threshold: $COMPRESS_TRIGGER), triggering compression..."

    if [[ "$DRY_RUN" == "1" ]]; then
        info "[DRY-RUN] Would compress MEMORY.md via $ARCHIVE_PRIORITY (${line_count} lines)"
        return 0
    fi

    # 按 ARCHIVE_PRIORITY 路由：优先 memory-palace，回退 local
    if [[ "$ARCHIVE_PRIORITY" == "memory-palace" ]]; then
        if check_memory_palace; then
            _compress_via_memory_palace "$memory_file" && return 1
            warn "memory-palace compress failed, falling back to local"
        fi
    fi

    # Local 回退压缩
    source "${SCRIPT_DIR}/../lib/harness-compress.sh" 2>/dev/null || true
    if declare -f compress_memory &>/dev/null; then
        compress_memory "$memory_file" 2>&1 | while IFS= read -r line; do
            [[ -n "$line" ]] && debug "compress: $line"
        done
        info "MEMORY.md compression completed (local)"
        return 1
    else
        warn "compress_memory function not available"
        return 0
    fi
}

# ---- 通过 memory-palace 归档 ----
# 使用 write action 实现归档语义：
# 1. 读取 MEMORY.md 内容
# 2. 写入 memory-palace (location=archive, type=memory-archive)
# 3. 成功则截断 MEMORY.md 到前 50 行（保留安全锚点）
# 4. 失败返回 1，触发回退到 local compress_memory
_compress_via_memory_palace() {
    local memory_file="$1"

    # 读取 MEMORY.md 内容
    local content
    content=$(cat "$memory_file" 2>/dev/null || echo "")
    [[ -z "$content" ]] && {
        debug "MEMORY.md is empty, nothing to archive"
        return 0
    }

    debug "Archiving MEMORY.md to memory-palace ($(echo "$content" | wc -l) lines)"

    # 写入 memory-palace 归档
    # 格式: write <content> <location> <tags> <importance> <type>
    local mp_result
    mp_result=$(OPENCLAW_WORKSPACE=/root/.openclaw/workspace node "$MEMORY_PALACE_BIN" write \
        "$content" \
        "archive" \
        '["memory-archive","gc-agent"]' \
        "0.5" \
        "memory-archive" 2>&1)

    # 检查是否成功（write 成功时返回 JSON 对象，含 id 字段）
    if echo "$mp_result" | grep -q '"id"'; then
        local mp_id
        mp_id=$(echo "$mp_result" | grep '"id"' | head -1 | sed 's/.*"id"[:" ]*\([0-9a-f-]\+\).*/\1/' | tr -d ' ,')
        debug "Archived MEMORY.md to memory-palace (id=$mp_id)"
        info "MEMORY.md archived to memory-palace (id=$mp_id)"

        # 截断 MEMORY.md 到前 50 行作为安全锚点
        local kept_lines=50
        head -n "$kept_lines" "$memory_file" > "${memory_file}.tmp" && mv "${memory_file}.tmp" "$memory_file"
        debug "MEMORY.md truncated to $kept_lines lines"
        return 0
    else
        warn "memory-palace write failed: $mp_result"
        return 1
    fi
}

# ---- GC 执行核心（单次） ----
run_gc_cycle() {
    local cycle_start=$(date +%s)
    info "=== GC Cycle Start (dry-run=$DRY_RUN) ==="

    # 1. Memory 压缩检查
    trigger_memory_compress || true

    # 2. 清理过期检查点（按时间）
    if [[ "$SKIP_CP" != "true" ]] && [[ "$SKIP_CP" != "1" ]]; then
        cleanup_old_checkpoints || true
    else
        debug "Checkpoint cleanup skipped"
    fi

    # 3. 清理超数量限制的检查点
    if [[ "$SKIP_CP" != "true" ]] && [[ "$SKIP_CP" != "1" ]]; then
        cleanup_excess_checkpoints || true
    fi

    # 4. 清理旧报告
    if [[ "$SKIP_REPORT" != "true" ]] && [[ "$SKIP_REPORT" != "1" ]]; then
        cleanup_old_reports || true
    else
        debug "Report cleanup skipped"
    fi

    # 5. 清理 .trash（永久删除超过 N 天的）
    if [[ "$SKIP_TRASH" != "true" ]] && [[ "$SKIP_TRASH" != "1" ]]; then
        cleanup_trash || true
    else
        debug "Trash cleanup skipped"
    fi

    local cycle_duration=$(($(date +%s) - cycle_start))
    info "=== GC Cycle End (${cycle_duration}s) ==="
    echo ""
    echo "=== GC Agent Summary ==="
    echo "Mode:       $MODE"
    echo "Dry-run:    $DRY_RUN"
    echo "Max CP:     $MAX_CP"
    echo "Max Age:    $MAX_AGE days"
    echo "Compressed: $ARCHIVE_PRIORITY"
    [[ "$DRY_RUN" == "1" ]] && echo ""
    [[ "$DRY_RUN" == "1" ]] && echo "Run with --run to execute cleanup."
}

# ---- 清理过期检查点 ----
cleanup_old_checkpoints() {
    local cp_dir="$HARNESS_DIR/checkpoints"
    [[ ! -d "$cp_dir" ]] && { debug "No checkpoints directory"; return; }

    local now=$(date +%s)
    local age_seconds=$((MAX_AGE * 86400))
    local deleted=0

    for dir in "$cp_dir"/*/; do
        [[ -d "$dir" ]] || continue
        local manifest="$dir/manifest.json"
        [[ ! -f "$manifest" ]] && continue

        local created_at=$(has_jq && jq -r '.created_at' "$manifest" 2>/dev/null || echo "")
        [[ -z "$created_at" ]] && continue

        local created_ts
        created_ts=$(date -d "$created_at" +%s 2>/dev/null) || continue

        local age=$((now - created_ts))
        if [[ $age -gt $age_seconds ]]; then
            local cp_id=$(basename "$dir")
            debug "Expiring checkpoint: $cp_id (${age}s old)"
            if [[ "$DRY_RUN" == "0" ]]; then
                mkdir -p "${HARNESS_DIR}/.trash"
                mv "$dir" "${HARNESS_DIR}/.trash/"
                gc_log "DELETE_CP" "$cp_id" "age_exceeded:${age}s"
            fi
            deleted=$((deleted + 1))
        fi
    done

    [[ $deleted -gt 0 ]] && info "Expired checkpoints: $deleted"
}

# ---- 清理超数量限制的检查点 ----
cleanup_excess_checkpoints() {
    local cp_dir="$HARNESS_DIR/checkpoints"
    [[ ! -d "$cp_dir" ]] && { debug "No checkpoints directory"; return; }

    declare -A task_cps_map

    for cp in "$cp_dir"/*/; do
        [[ -d "$cp" ]] || continue
        local manifest="$cp/manifest.json"
        [[ ! -f "$manifest" ]] && continue

        local task_id=$(has_jq && jq -r '.task_id' "$manifest" 2>/dev/null || echo "default")
        local cp_id=$(basename "$cp")
        local created_at=$(has_jq && jq -r '.created_at' "$manifest" 2>/dev/null || echo "")

        if [[ -z "${task_cps_map[$task_id]}" ]]; then
            task_cps_map[$task_id]="$cp_id:$created_at"
        else
            task_cps_map[$task_id]="${task_cps_map[$task_id]}"$'\n'"$cp_id:$created_at"
        fi
    done

    local total_deleted=0
    for task_id in "${!task_cps_map[@]}"; do
        local cps_list="${task_cps_map[$task_id]}"
        local cps_count=$(echo "$cps_list" | wc -l)

        if [[ $cps_count -gt $MAX_CP ]]; then
            local excess=$(($cps_count - MAX_CP))
            local to_delete=$(echo "$cps_list" | sort -t: -k2 | head -$excess)

            for line in $to_delete; do
                local cp_id="${line%%:*}"
                local cp_path="$cp_dir/$cp_id"
                if [[ -d "$cp_path" ]]; then
                    debug "Removing checkpoint $cp_id (task=$task_id, max_cp=$MAX_CP)"
                    if [[ "$DRY_RUN" == "0" ]]; then
                        mkdir -p "${HARNESS_DIR}/.trash"
                        mv "$cp_path" "${HARNESS_DIR}/.trash/"
                        gc_log "DELETE_CP" "$cp_id" "max_cp_exceeded:task=$task_id"
                    fi
                    total_deleted=$((total_deleted + 1))
                fi
            done
        fi
    done

    [[ $total_deleted -gt 0 ]] && info "Excess checkpoints removed: $total_deleted"
}

# ---- 清理旧报告 ----
cleanup_old_reports() {
    local reports_dir="$HARNESS_DIR/reports"
    [[ ! -d "$reports_dir" ]] && { debug "No reports directory"; return; }

    local reports=()
    for r in "$reports_dir"/*.json; do
        [[ -f "$r" ]] && reports+=("$r")
    done

    if [[ ${#reports[@]} -gt $REPORT_RETENTION ]]; then
        local excess_count=$((${#reports[@]} - REPORT_RETENTION))
        local sorted=($(ls -t "${reports[@]}" 2>/dev/null | tail -n $excess_count))
        local deleted=0

        for r in "${sorted[@]}"; do
            [[ -f "$r" ]] || continue
            debug "Removing old report: $(basename "$r")"
            if [[ "$DRY_RUN" == "0" ]]; then
                rm -f "$r"
                gc_log "DELETE_REPORT" "$(basename "$r")" "retention_exceeded"
            fi
            deleted=$((deleted + 1))
        done
        [[ $deleted -gt 0 ]] && info "Old reports removed: $deleted"
    fi
}

# ---- 清理 .trash（永久删除超期项） ----
cleanup_trash() {
    local trash_dir="${HARNESS_DIR}/.trash"
    [[ ! -d "$trash_dir" ]] && { debug "No trash directory"; return; }

    local now=$(date +%s)
    local max_age_seconds=$((TRASH_RETENTION * 86400))
    local deleted=0

    for item in "$trash_dir"/*/; do
        [[ -d "$item" ]] || continue
        local mtime=$(stat -c %Y "$item" 2>/dev/null || echo $now)
        local age=$((now - mtime))
        if [[ $age -gt $max_age_seconds ]]; then
            debug "Permanently removing trash: $(basename "$item") (${age}s old)"
            if [[ "$DRY_RUN" == "0" ]]; then
                rm -rf "$item"
            fi
            deleted=$((deleted + 1))
        fi
    done

    [[ $deleted -gt 0 ]] && info "Trash items permanently removed: $deleted"
}

# ---- Daemon 模式 ----
run_daemon() {
    info "GC Agent starting in daemon mode (interval=${DAEMON_INTERVAL}s, pid=$$)"

    local _shutdown=0
    # 只 trap SIGINT/SIGTERM；EXIT 由 exit 0 触发，但 flag 防止重复
    trap 'if [[ $_shutdown -eq 0 ]]; then _shutdown=1; info "GC Agent received signal, shutting down..."; release_lock; fi; exit 0' SIGINT SIGTERM

    while true; do
        if acquire_lock; then
            run_gc_cycle || true
            release_lock
        fi

        sleep "$DAEMON_INTERVAL" &
        wait $! || true
    done
}

# ---- 主入口 ----
main() {
    mkdir -p "$(dirname "$GC_LOG_FILE")"

    if [[ "$MODE" == "daemon" ]]; then
        run_daemon
    else
        acquire_lock || exit 0
        run_gc_cycle || true
        release_lock
    fi
}

main
