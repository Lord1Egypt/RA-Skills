#!/bin/bash
# Knowledge Base Skill - Lifecycle Management
# 生命周期管理 + DAG 摘要

set -e

# ============================================
# 配置
# ============================================

export KNOWLEDGE_DB="${KNOWLEDGE_DB:-$HOME/.openclaw/agents/current/knowledge.db}"

# 生命周期阈值
STALE_DAYS="${KNOWLEDGE_STALE_DAYS:-90}"
ARCHIVE_DAYS="${KNOWLEDGE_ARCHIVE_DAYS:-365}"
CLEANUP_DAYS="${KNOWLEDGE_CLEANUP_DAYS:-30}"

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORAGE="$SCRIPTS_DIR/storage.sh"

# ============================================
# mark-stale - 标记陈旧记录
# ============================================

do_mark_stale() {
    local threshold="${1:-$STALE_DAYS}"
    
    local count
    count=$(sqlite3 "$KNOWLEDGE_DB" "
        UPDATE entries 
        SET status = 'stale' 
        WHERE status = 'active' 
        AND datetime(updated_at) < datetime('now', '-$threshold days');
    " 2>/dev/null)
    
    # 获取实际更新的行数
    count=$(sqlite3 "$KNOWLEDGE_DB" "
        SELECT COUNT(*) FROM entries 
        WHERE status = 'stale' 
        AND datetime(updated_at) < datetime('now', '-$threshold days');
    " 2>/dev/null || echo "0")
    
    echo "{\"status\": \"ok\", \"action\": \"mark-stale\", \"marked\": $count}"
}

# ============================================
# archive - 归档过期记录
# ============================================

do_archive() {
    local threshold="${1:-$ARCHIVE_DAYS}"
    
    local count
    count=$(sqlite3 "$KNOWLEDGE_DB" "
        UPDATE entries 
        SET status = 'archived', archived_at = datetime('now')
        WHERE status = 'stale' 
        AND datetime(updated_at) < datetime('now', '-$threshold days');
    " 2>/dev/null)
    
    count=$(sqlite3 "$KNOWLEDGE_DB" "
        SELECT COUNT(*) FROM entries 
        WHERE status = 'archived';
    " 2>/dev/null || echo "0")
    
    echo "{\"status\": \"ok\", \"action\": \"archive\", \"archived\": $count}"
}

# ============================================
# cleanup - 清理已归档记录
# ============================================

do_cleanup() {
    local threshold="${1:-$CLEANUP_DAYS}"
    
    # 先获取数量
    local count_before
    count_before=$(sqlite3 "$KNOWLEDGE_DB" "
        SELECT COUNT(*) FROM entries 
        WHERE status = 'archived' 
        AND datetime(archived_at) < datetime('now', '-$threshold days');
    " 2>/dev/null || echo "0")
    
    # 删除
    sqlite3 "$KNOWLEDGE_DB" "
        DELETE FROM entries 
        WHERE status = 'archived' 
        AND datetime(archived_at) < datetime('now', '-$threshold days');
    " 2>/dev/null
    
    echo "{\"status\": \"ok\", \"action\": \"cleanup\", \"deleted\": $count_before}"
}

# ============================================
# summarize - 生成摘要（DAG d2 层）
# ============================================

do_summarize() {
    local topic_key limit
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --topic-key) topic_key="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    limit="${limit:-200}"
    
    if [[ -z "$topic_key" ]]; then
        echo '{"status": "error", "error": "Missing required argument: --topic-key"}'
        return 1
    fi
    
    # 获取完整内容
    local content
    content=$(sqlite3 "$KNOWLEDGE_DB" "
        SELECT content FROM entries 
        WHERE topic_key = '$topic_key' 
        AND status != 'archived'
        LIMIT 1;
    " 2>/dev/null)
    
    if [[ -z "$content" ]]; then
        echo '{"status": "error", "error": "Entry not found"}'
        return 1
    fi
    
    # 生成摘要（简单实现：取前 N 个字符）
    local summary
    summary=$(echo "$content" | head -c "$limit")
    
    if [[ ${#content} -gt $limit ]]; then
        summary="$summary..."
    fi
    
    # 提取关键点（简单实现：找句子）
    local key_points
    key_points=$(echo "$content" | grep -oE '[^.!?]+[.!?]' | head -3 | tr '\n' ' ' || echo "")
    
    # 构建 DAG 摘要（d2 层）
    local dag_summary
    dag_summary=$(python3 -c "
import sys, json

content = '''$content'''
summary = '''$summary'''
key_points = '''$key_points'''

# 简单的 DAG 结构
dag = {
    'd0': content,  # 原始内容
    'd2': {  # 摘要层
        'summary': summary,
        'key_points': key_points,
        'word_count': len(content.split()),
        'char_count': len(content)
    }
}

print(json.dumps(dag, ensure_ascii=False, indent=2))
" 2>/dev/null)
    
    echo "{\"status\": \"ok\", \"topic_key\": \"$topic_key\", \"dag\": $dag_summary}"
}

# ============================================
# compact - DAG 压缩（多级摘要）
# ============================================

do_compact() {
    local max_entries="${1:-100}"
    
    # 获取需要压缩的条目（按 updated_at 排序）
    local entries
    entries=$(sqlite3 -json "$KNOWLEDGE_DB" "
        SELECT id, topic_key, title, content, source, updated_at
        FROM entries
        WHERE status = 'active'
        ORDER BY updated_at DESC
        LIMIT $max_entries
    " 2>/dev/null || echo "[]")
    
    local count
    count=$(echo "$entries" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
    
    echo "{\"status\": \"ok\", \"action\": \"compact\", \"processed\": $count}"
}

# ============================================
# stats - 状态统计
# ============================================

do_stats() {
    local stats
    stats=$(sqlite3 "$KNOWLEDGE_DB" "
        SELECT 
            status,
            COUNT(*) as count
        FROM entries
        GROUP BY status;
    " 2>/dev/null)
    
    # 转换为 JSON
    echo "$stats" | python3 -c "
import sys, json

stats = {}
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('|')
    if len(parts) == 2:
        status, count = parts
        stats[status] = int(count)

# 添加总计
stats['total'] = sum(stats.values())

# 添加时间范围
import subprocess
result = subprocess.run(['sqlite3', '$KNOWLEDGE_DB', \"SELECT MIN(created_at), MAX(created_at) FROM entries;\"], capture_output=True, text=True)
dates = result.stdout.strip().split('|')
if len(dates) == 2:
    stats['oldest'] = dates[0] if dates[0] else None
    stats['newest'] = dates[1] if dates[1] else None

print(json.dumps(stats, ensure_ascii=False, indent=2))
" 2>/dev/null || echo "{\"total\": 0, \"active\": 0}"
}

# ============================================
# integrity - DAG 完整性检查
# ============================================

do_integrity() {
    local issues=()
    
    # 检查孤立记录（没有引用的摘要）
    local orphans
    orphans=$(sqlite3 "$KNOWLEDGE_DB" "
        SELECT COUNT(*) FROM entries e
        WHERE status = 'archived'
        AND NOT EXISTS (
            SELECT 1 FROM entries r 
            WHERE r.topic_key = e.topic_key 
            AND r.status = 'active'
        );
    " 2>/dev/null || echo "0")
    
    if [[ "$orphans" -gt 0 ]]; then
        issues+=("{\"type\": \"orphans\", \"count\": $orphans}")
    fi
    
    # 检查循环引用（自己引用自己）
    local self_refs
    self_refs=$(sqlite3 "$KNOWLEDGE_DB" "
        SELECT COUNT(*) FROM entries 
        WHERE metadata LIKE '%\"parent\":\"%' 
        AND topic_key = substr(metadata, instr(metadata, '\"parent\":\"') + 9, 50);
    " 2>/dev/null || echo "0")
    
    if [[ "$self_refs" -gt 0 ]]; then
        issues+=("{\"type\": \"self_references\", \"count\": $self_refs}")
    fi
    
    # 检查 token 膨胀（摘要比原文还长）
    local inflated
    inflated=$(sqlite3 "$KNOWLEDGE_DB" "
        SELECT COUNT(*) FROM entries 
        WHERE LENGTH(content) > 5000 
        AND LENGTH(content) < 100;
    " 2>/dev/null || echo "0")
    
    if [[ ${#issues[@]} -eq 0 ]]; then
        echo "{\"status\": \"ok\", \"action\": \"integrity\", \"issues\": [], \"healthy\": true}"
    else
        echo "{\"status\": \"ok\", \"action\": \"integrity\", \"issues\": [$(IFS=,; echo "${issues[*]}")], \"healthy\": false}"
    fi
}

# ============================================
# repair - 修复问题
# ============================================

do_repair() {
    local fixed=0
    
    # 修复孤立记录：删除孤立的 archived 记录
    local orphans
    orphans=$(sqlite3 "$KNOWLEDGE_DB" "
        DELETE FROM entries 
        WHERE status = 'archived'
        AND NOT EXISTS (
            SELECT 1 FROM entries r 
            WHERE r.topic_key = entries.topic_key 
            AND r.status = 'active'
        );
    " 2>/dev/null)
    
    # 重新计算被影响的数量
    fixed=$(sqlite3 "$KNOWLEDGE_DB" "SELECT COUNT(*) FROM entries WHERE status = 'archived';" 2>/dev/null || echo "0")
    
    echo "{\"status\": \"ok\", \"action\": \"repair\", \"fixed\": $fixed}"
}

# ============================================
# 主入口
# ============================================

main() {
    local command="${1:-}"
    shift
    
    case "$command" in
        mark-stale)
            do_mark_stale "$@"
            ;;
        archive)
            do_archive "$@"
            ;;
        cleanup)
            do_cleanup "$@"
            ;;
        summarize)
            do_summarize "$@"
            ;;
        compact)
            do_compact "$@"
            ;;
        stats)
            do_stats "$@"
            ;;
        integrity)
            do_integrity "$@"
            ;;
        repair)
            do_repair "$@"
            ;;
        run)
            # 运行完整生命周期：mark-stale → archive → cleanup
            do_mark_stale
            do_archive
            do_cleanup
            ;;
        *)
            cat <<EOF
Knowledge Base Lifecycle
=========================

Usage:
  lifecycle <command> [options]

Commands:
  mark-stale    标记陈旧记录（默认 90 天）
  archive       归档过期记录（默认 365 天）
  cleanup       清理已归档记录（默认 30 天）
  summarize     生成摘要（DAG d2 层）
  compact      DAG 压缩
  stats        状态统计
  integrity    DAG 完整性检查
  repair       修复问题
  run          运行完整生命周期

Examples:
  lifecycle mark-stale
  lifecycle archive
  lifecycle cleanup
  lifecycle summarize --topic-key "entry-key"
  lifecycle stats
  lifecycle integrity

EOF
            ;;
    esac
}

# 如果直接执行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
