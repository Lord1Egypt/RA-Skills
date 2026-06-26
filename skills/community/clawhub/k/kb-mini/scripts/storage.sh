#!/bin/bash
# Knowledge Base Skill - Storage Core
# 提供 store, search, retrieve 等核心 API

set -e

# ============================================
# 配置
# ============================================

# 数据库路径
# 1. 显式环境变量（最高优先）
# 2. 共享 KB 模式（通过 KNOWLEDGE_SHARED_NAME 指定）
# 3. Skill 内部目录（默认，安装后即用）
SKILL_DIR="${KNOWLEDGE_SKILL_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
if [[ -n "$KNOWLEDGE_SHARED_NAME" ]]; then
    export KNOWLEDGE_DB="${KNOWLEDGE_DB:-$HOME/.openclaw/shared/knowledge-bases/$KNOWLEDGE_SHARED_NAME/knowledge.db}"
else
    export KNOWLEDGE_DB="${KNOWLEDGE_DB:-$SKILL_DIR/data/knowledge.db}"
fi

# FTS5 权重配置
FTS_WEIGHT_TITLE="${KNOWLEDGE_FTS_WEIGHT_TITLE:-2.0}"
FTS_WEIGHT_CONTENT="${KNOWLEDGE_FTS_WEIGHT_CONTENT:-1.0}"

# ============================================
# 工具函数
# ============================================

# 生成 UUID
gen_uuid() {
    if command -v uuidgen &> /dev/null; then
        uuidgen | tr '[:upper:]' '[:lower:]'
    else
        # macOS fallback
        printf '%s' "$(date +%s)-$$-$(head -c 16 /dev/urandom | xxd -p)"
    fi
}

# 生成 topic_key
gen_topic_key() {
    local title="$1"
    echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//' | cut -c1-50
}

# 格式化 JSON（简单实现）
json_escape() {
    echo "$1" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' 2>/dev/null | tr -d '"' || echo "$1"
}

# ============================================
# init - 初始化数据库
# ============================================

do_init() {
    local db="${KNOWLEDGE_DB}"
    
    # 确保目录存在
    mkdir -p "$(dirname "$db")"
    
    # 创建表
    sqlite3 "$db" "
        CREATE TABLE IF NOT EXISTS entries (
            id TEXT PRIMARY KEY,
            topic_key TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT NOT NULL,
            tags TEXT,
            access_level INTEGER DEFAULT 2,
            status TEXT DEFAULT 'active',
            created_at TEXT,
            updated_at TEXT,
            archived_at TEXT,
            metadata TEXT
        );
        
        CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_entries USING fts5(
            id,
            topic_key,
            title,
            content,
            source,
            tags,
            access_level,
            created_at,
            updated_at,
            content='entries',
            content_rowid='rowid'
        );
        
        CREATE INDEX IF NOT EXISTS idx_entries_status ON entries(status);
        CREATE INDEX IF NOT EXISTS idx_entries_created_at ON entries(created_at);
        CREATE INDEX IF NOT EXISTS idx_entries_topic_key ON entries(topic_key);
    "
    
    :
}

# ============================================
# store - 存入数据
# ============================================

do_store() {
    local db="${KNOWLEDGE_DB}"
    local id topic_key title content source tags access_level metadata
    local created_at updated_at
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --id) id="$2"; shift 2 ;;
            --topic-key) topic_key="$2"; shift 2 ;;
            --title) title="$2"; shift 2 ;;
            --content) content="$2"; shift 2 ;;
            --source) source="$2"; shift 2 ;;
            --tags) tags="$2"; shift 2 ;;
            --level) access_level="$2"; shift 2 ;;
            --metadata) metadata="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    # 必填检查
    if [[ -z "$title" || -z "$content" ]]; then
        echo '{"status": "error", "error": "Missing required arguments: --title and --content"}'
        return 1
    fi
    
    # 默认值
    id="${id:-$(gen_uuid)}"
    topic_key="${topic_key:-$(gen_topic_key "$title")}"
    source="${source:-manual}"
    access_level="${access_level:-2}"
    created_at="${created_at:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
    updated_at="${updated_at:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
    tags="${tags:-[]}"
    metadata="${metadata:-{}}"
    
    # 检查是否存在
    local existing
    existing=$(sqlite3 "$db" "SELECT id FROM entries WHERE topic_key = '$topic_key' LIMIT 1" 2>/dev/null || true)
    
    local action
    if [[ -n "$existing" ]]; then
        # Update - 追加内容
        action="update"
        sqlite3 "$db" "
            UPDATE entries 
            SET content = content || char(10) || '$content',
                updated_at = '$updated_at',
                metadata = '$metadata'
            WHERE topic_key = '$topic_key'
        "
    else
        # Insert
        action="insert"
        sqlite3 "$db" "
            INSERT INTO entries (id, topic_key, title, content, source, tags, access_level, created_at, updated_at, metadata)
            VALUES ('$id', '$topic_key', '$title', '$content', '$source', '$tags', $access_level, '$created_at', '$updated_at', '$metadata')
        "
        
        # 更新 FTS 索引
        sqlite3 "$db" "
            INSERT INTO knowledge_entries (id, topic_key, title, content, source, tags, access_level, created_at, updated_at)
            VALUES ('$id', '$topic_key', '$title', '$content', '$source', '$tags', $access_level, '$created_at', '$updated_at')
        " 2>/dev/null || true
    fi
    
    echo "{\"status\": \"ok\", \"id\": \"$id\", \"topic_key\": \"$topic_key\", \"action\": \"$action\"}"
}

# ============================================
# search - 检索
# ============================================

do_search() {
    local db="${KNOWLEDGE_DB}"
    local query limit source level time_decay format
    local where_conditions="status != 'archived'"
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --query) query="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            --source) source="$2"; shift 2 ;;
            --level) level="$2"; shift 2 ;;
            --since) since="$2"; shift 2 ;;
            --time-decay) time_decay="$2"; shift 2 ;;
            --format) format="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    limit="${limit:-5}"
    level="${level:-2}"
    format="${format:-json}"
    
    if [[ -z "$query" ]]; then
        echo '{"status": "error", "error": "Missing required argument: --query"}'
        return 1
    fi
    
    # 构建 WHERE 条件
    if [[ -n "$source" ]]; then
        where_conditions="$where_conditions AND source = '$source'"
    fi
    
    # 简单 FTS5 搜索
    # 注意：这里使用 LIKE 简化，实际生产应该用 FTS5 MATCH
    local search_term="%$query%"
    
    local results
    results=$(sqlite3 -json "$db" "
        SELECT 
            id,
            topic_key,
            title,
            CASE 
                WHEN access_level <= 1 THEN substr(content, 1, 200)
                ELSE substr(content, 1, 500)
            END as summary,
            source,
            tags,
            updated_at,
            1.0 as relevance_score
        FROM entries
        WHERE ($where_conditions)
        AND (title LIKE '$search_term' OR content LIKE '$search_term' OR tags LIKE '$search_term')
        ORDER BY updated_at DESC
        LIMIT $limit
    " 2>/dev/null || echo "[]")
    
    local total_hits
    total_hits=$(echo "$results" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
    
    if [[ "$format" == "json" ]]; then
        echo "{\"results\": $results, \"total_hits\": $total_hits}"
    elif [[ "$format" == "compact" ]]; then
        echo "$results" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data:
    print(f\"[{item['relevance_score']}] {item['title']} - {item['source']} - {item['updated_at']}\")
" 2>/dev/null || echo "$results"
    else
        echo "$results"
    fi
}

# ============================================
# retrieve - 按 topic_key 获取
# ============================================

do_retrieve() {
    local db="${KNOWLEDGE_DB}"
    local topic_key level
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --topic-key) topic_key="$2"; shift 2 ;;
            --level) level="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    level="${level:-2}"
    
    if [[ -z "$topic_key" ]]; then
        echo '{"status": "error", "error": "Missing required argument: --topic-key"}'
        return 1
    fi
    
    local result
    result=$(sqlite3 -json "$db" "
        SELECT 
            id,
            topic_key,
            title,
            content,
            source,
            tags,
            access_level as level,
            created_at,
            updated_at,
            metadata
        FROM entries
        WHERE topic_key = '$topic_key' AND status != 'archived'
        LIMIT 1
    " 2>/dev/null || echo "[]")
    
    # 提取单个结果
    echo "$result" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data:
    item = data[0]
    # 返回非 JSON 格式，方便使用
    print(f\"Title: {item['title']}\")
    print(f\"Content: {item['content']}\")
    print(f\"Source: {item['source']}\")
    print(f\"Updated: {item['updated_at']}\")
else:
    print('Not found')
" 2>/dev/null || echo "$result"
}

# ============================================
# batch_store - 批量存入
# ============================================

do_batch_store() {
    local db="${KNOWLED_DB}"
    local file source
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --file) file="$2"; shift 2 ;;
            --source) source="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    if [[ -z "$file" ]]; then
        echo '{"status": "error", "error": "Missing required argument: --file"}'
        return 1
    fi
    
    source="${source:-manual}"
    
    local processed=0
    local errors=0
    
    while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        
        # 解析 JSONL
        title=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin).get('title',''))" 2>/dev/null || true)
        content=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin).get('content',''))" 2>/dev/null || true)
        tags=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tags',''))" 2>/dev/null || true)
        
        if [[ -n "$title" && -n "$content" ]]; then
            do_store --title "$title" --content "$content" --tags "$tags" --source "$source"
            ((processed++)) || true
        else
            ((errors++)) || true
        fi
    done < "$file"
    
    echo "{\"status\": \"ok\", \"processed\": $processed, \"errors\": $errors}"
}

# ============================================
# config - 配置管理
# ============================================

do_config() {
    local subcommand="$1"
    shift
    
    case "$subcommand" in
        show)
            cat <<EOF
{
  "kb_mode": "${KNOWLEDGE_KB_MODE:-private}",
  "db_path": "${KNOWLEDGE_DB}",
  "fts_weight_title": ${FTS_WEIGHT_TITLE},
  "fts_weight_content": ${FTS_WEIGHT_CONTENT}
}
EOF
            ;;
        mode)
            local mode="$1"
            if [[ -z "$mode" ]]; then
                echo "${KNOWLEDGE_KB_MODE:-private}"
            else
                export KNOWLEDGE_KB_MODE="$mode"
                echo "Mode set to: $mode"
            fi
            ;;
        *)
            echo "Unknown config command: $subcommand"
            return 1
            ;;
    esac
}

# ============================================
# 主入口
# ============================================

main() {
    local command="${1:-}"
    shift
    
    case "$command" in
        init)
            do_init "$@"
            ;;
        store)
            do_store "$@"
            ;;
        search)
            do_search "$@"
            ;;
        retrieve)
            do_retrieve "$@"
            ;;
        batch_store)
            do_batch_store "$@"
            ;;
        config)
            do_config "$@"
            ;;
        *)
            cat <<EOF
Knowledge Base Storage API
===========================

Usage:
  kb <command> [options]

Commands:
  init           初始化数据库
  store          存入数据
  search         检索
  retrieve       按 topic_key 获取
  batch_store    批量存入
  config         配置管理

Examples:
  kb init
  kb store --title "..." --content "..."
  kb search --query "..."
  kb retrieve --topic-key "..."
  kb config show

EOF
            ;;
    esac
}

# 如果直接执行此脚本
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

# 如果被 source（用于测试）
if [[ "$0" != "${BASH_SOURCE[0]}" ]] || [[ "$KB_SOURCED" == "1" ]]; then
    # 只导出函数，不执行
    :
else
    main "$@"
fi
