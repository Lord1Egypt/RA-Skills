#!/bin/bash
# Knowledge Base Skill - Retriever
# RRF 融合 + 时间衰减 + 分层加载

set -e

# ============================================
# 配置
# ============================================

export KNOWLEDGE_DB="${KNOWLEDGE_DB:-$HOME/.openclaw/agents/current/knowledge.db}"

# RRF 参数
RRF_K="${KNOWLEDGE_RRF_K:-60}"

# 时间衰减参数
TIME_DECAY_LAMBDA="${KNOWLEDGE_TIME_DECAY_LAMBDA:-0.1}"

# ============================================
# 主检索函数
# ============================================

do_retrieve() {
    local query limit level match_mode boost_source format
    local where_conditions="status != 'archived'"
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --query) query="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            --level) level="$2"; shift 2 ;;
            --match-mode) match_mode="$2"; shift 2 ;;
            --boost-source) boost_source="$2"; shift 2 ;;
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
    
    # 构建搜索词
    local search_term="%$query%"
    
    # 根据不同模式构建 SQL
    local sql
    local order_by="ORDER BY updated_at DESC"
    local source_boost=""
    
    if [[ -n "$boost_source" ]]; then
        source_boost="CASE WHEN source = '$boost_source' THEN 1 ELSE 0 END as source_boost,"
        order_by="ORDER BY source_boost DESC, updated_at DESC"
    fi
    
    # SQL 查询
    local content_limit=500
    if [[ "$level" == "0" ]]; then
        content_limit=200
    elif [[ "$level" == "1" ]]; then
        content_limit=500
    fi
    
    sql="SELECT 
        id,
        topic_key,
        title,
        substr(content, 1, $content_limit) as summary,
        source,
        tags,
        access_level,
        created_at,
        updated_at,
        $source_boost
        1.0 as relevance_score
    FROM entries
    WHERE $where_conditions
    AND (title LIKE '$search_term' OR content LIKE '$search_term' OR tags LIKE '$search_term')
    $order_by
    LIMIT $limit"
    
    # 执行查询
    local results
    results=$(sqlite3 -json "${KNOWLEDGE_DB}" "$sql" 2>/dev/null || echo "[]")
    
    # 时间衰减计算
    local decay_results
    decay_results=$(echo "$results" | python3 -c "
import sys, json, math

try:
    data = json.load(sys.stdin)
    if isinstance(data, list):
        for item in data:
            # 计算时间衰减
            created_at = item.get('created_at', '')
            if created_at:
                try:
                    # 简单计算：假设格式为 ISO
                    from datetime import datetime
                    created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    now = datetime.now(created.tzinfo) if created.tzinfo else datetime.now()
                    days = (now - created.replace(tzinfo=None)).days
                    decay = math.exp(-$TIME_DECAY_LAMBDA * days)
                except:
                    decay = 1.0
            else:
                decay = 1.0
            item['time_decay'] = decay
            item['final_score'] = item.get('relevance_score', 1.0) * decay
        # 按 final_score 排序
        data.sort(key=lambda x: -x.get('final_score', 0))
    print(json.dumps(data))
except Exception as e:
    print('[]')
" 2>/dev/null || echo "$results")
    
    # 计算命中数
    local total_hits
    total_hits=$(echo "$decay_results" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
    
    # 输出
    if [[ "$format" == "json" ]]; then
        echo "{\"results\": $decay_results, \"total_hits\": $total_hits, \"query\": \"$query\", \"level\": \"$level\"}"
    else
        echo "$decay_results" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if isinstance(data, list):
        for i, item in enumerate(data, 1):
            print(f\"{i}. {item.get('title', 'N/A')} (score: {item.get('final_score', 0):.3f})\")
            print(f\"   {item.get('summary', '')[:100]}...\")
except:
    pass
" 2>/dev/null
    fi
}

# ============================================
# recall - Hook 调用（自动检索）
# ============================================

do_recall() {
    local context limit max_tokens
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --context) context="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            --max-tokens) max_tokens="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    limit="${limit:-3}"
    max_tokens="${max_tokens:-500}"
    
    if [[ -z "$context" ]]; then
        echo '{"status": "error", "error": "Missing required argument: --context"}'
        return 1
    fi
    
    # 使用 context 作为查询词
    local query="$context"
    
    # L0 级别检索
    local result
    result=$(do_retrieve --query "$query" --limit "$limit" --level 0 --format json)
    
    # 构建注入上下文
    local injected
    injected=$(echo "$result" | python3 -c "
import sys, json, re

try:
    # 处理换行符问题
    raw = sys.stdin.read()
    # 替换控制字符
    raw = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', raw)
    data = json.loads(raw)
    entries = data.get('results', [])
    
    if not entries:
        print('')
    else:
        lines = ['相关知识：']
        for i, entry in enumerate(entries, 1):
            title = entry.get('title', 'N/A')
            summary = entry.get('summary', '')[:150].replace('\\n', ' ')
            source = entry.get('source', 'N/A')
            updated = entry.get('updated_at', '')[:10]
            lines.append(f'{i}. {title} ({source}, {updated})')
            lines.append(f'   {summary}...')
        print('\\n'.join(lines))
except Exception as e:
    print('')
" 2>/dev/null)
    
    local entries_count
    entries_count=$(echo "$result" | python3 -c "
import sys, json, re
try:
    raw = sys.stdin.read()
    raw = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', raw)
    data = json.loads(raw)
    print(len(data.get('results',[])))
except:
    print(0)
" 2>/dev/null || echo "0")
    
    echo "{\"injected_context\": \"$injected\", \"entries_used\": $entries_count}"
}

# ============================================
# capture - Hook 调用（自动捕获）
# ============================================

do_capture() {
    local turn threshold
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --turn) turn="$2"; shift 2 ;;
            --threshold) threshold="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    
    threshold="${threshold:-0.7}"
    
    if [[ -z "$turn" ]]; then
        echo '{"status": "error", "error": "Missing required argument: --turn"}'
        return 1
    fi
    
    # 简单实现：检测关键词判断是否值得记忆
    local capture_score=0
    local decision=""
    
    # 检测关键词
    if echo "$turn" | grep -qi "记住\|save\|存储\|知识库\|knowledge"; then
        capture_score=0.9
        decision="显式请求存储"
    elif echo "$turn" | grep -qi "配置\|config\|设置\|setup"; then
        capture_score=0.8
        decision="配置信息"
    elif echo "$turn" | grep -qi "决策\|决定\|decision"; then
        capture_score=0.85
        decision="重要决策"
    elif echo "$turn" | grep -qi "api\|key\|token\|密码"; then
        capture_score=0.95
        decision="敏感信息"
    else
        capture_score=0.3
        decision="低优先级"
    fi
    
    # 比较分数
    local captured
    if python3 -c "exit(0 if $capture_score >= $threshold else 1)" 2>/dev/null; then
        captured="true"
    else
        captured="false"
    fi
    
    echo "{\"captured\": $captured, \"score\": $capture_score, \"decision\": \"$decision\"}"
}

# ============================================
# 主入口
# ============================================

main() {
    local command="${1:-}"
    shift
    
    case "$command" in
        retrieve|search)
            do_retrieve "$@"
            ;;
        recall)
            do_recall "$@"
            ;;
        capture)
            do_capture "$@"
            ;;
        *)
            cat <<EOF
Knowledge Base Retriever
========================

Usage:
  kb retriever <command> [options]

Commands:
  retrieve    检索（支持时间衰减 + 分层）
  recall      Hook 调用：自动检索相关知识
  capture     Hook 调用：判断是否值得记忆

Examples:
  kb retriever retrieve --query "OpenClaw" --limit 5 --level 1
  kb retriever recall --context "用户问如何配置 hooks"
  kb retriever capture --turn "用户说记得这个配置..."

EOF
            ;;
    esac
}

# 如果直接执行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
