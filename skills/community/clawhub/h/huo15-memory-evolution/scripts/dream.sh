#!/bin/bash
#===============================================================================
# 火一五记忆进化技能 - Dream Agent
#
# 4阶段记忆提炼：
# 1. Orient - 读取昨日日志，理解发生了什么
# 2. Gather - 收集值得记忆的内容
# 3. Consolidate - 将内容写入记忆文件
# 4. Prune - 检查并标记过时记忆
#===============================================================================

set -e

# 获取脚本所在目录
# 脚本路径: skills/huo15-memory-evolution/scripts/dream.sh
# 实际路径: /path/to/skills/huo15-memory-evolution/scripts/dream.sh
# 需要得到: /path/to/skills/huo15-memory-evolution
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"  # = .../scripts
SKILL_DIR="$(dirname "$SCRIPT_DIR")"  # = .../huo15-memory-evolution

# 动态路由：优先使用 PWD 检测 > OC_AGENT_ID > 默认
if [ -d "${PWD}/memory" ] && [[ "$PWD" == *".openclaw/workspace"* ]]; then
    WORKSPACE_DIR="$PWD"
elif [ -n "${OC_AGENT_ID:-}" ]; then
    WORKSPACE_DIR="$HOME/.openclaw/workspace-${OC_AGENT_ID}"
else
    WORKSPACE_DIR="$HOME/.openclaw/workspace"
fi

MEMORY_DIR="$WORKSPACE_DIR/memory"
DAILY_DIR="$MEMORY_DIR"
LOG_FILE="/tmp/dream-agent-$(date +%Y%m%d).log"

# 昨天的日期
YESTERDAY=$(date -v-1d +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "🚀 Dream Agent 开始执行..."

#===========================================
# Stage 1: Orient - 读取昨日日志
#===========================================
log "📖 Stage 1: Orient - 读取日志..."

YESTERDAY_LOG="$DAILY_DIR/${YESTERDAY}.md"

if [ ! -f "$YESTERDAY_LOG" ]; then
    log "⚠️  昨日日志不存在: $YESTERDAY_LOG"
    log "尝试查找其他日志..."
    # 查找最新的日志
    LATEST=$(find "$DAILY_DIR" -name "*.md" -type f | sort -r | head -1)
    if [ -n "$LATEST" ]; then
        YESTERDAY_LOG="$LATEST"
        log "使用最新日志: $LATEST"
    else
        log "❌ 没有找到任何日志，退出"
        exit 0
    fi
fi

log "读取日志: $YESTERDAY_LOG"
LOG_CONTENT=$(cat "$YESTERDAY_LOG")
LOG_LINES=$(echo "$LOG_CONTENT" | wc -l)
log "日志行数: $LOG_LINES"

if [ "$LOG_LINES" -lt 5 ]; then
    log "⚠️  日志内容太少，跳过提炼"
    exit 0
fi

#===========================================
# Stage 2: Gather - 分析日志提取记忆
#===========================================
log "🔍 Stage 2: Gather - 分析日志提取记忆..."

# 调用 Python API 进行 LLM 分析
API_SCRIPT="$SKILL_DIR/scripts/dream-api.py"

if [ -f "$API_SCRIPT" ]; then
    # 使用 Python API（更可靠的 JSON 处理）
    log "调用 LLM API 分析...（最多等待30秒）"
    
    # 添加30秒超时保护
    if command -v timeout >/dev/null 2>&1; then
        MEMORIES_JSON=$(timeout 30 python3 "$API_SCRIPT" "$LOG_CONTENT" 2>/dev/null) || MEMORIES_JSON=""
    else
        # macOS 没有 timeout，用 gtimeout 或直接调用
        MEMORIES_JSON=$(python3 "$API_SCRIPT" "$LOG_CONTENT" 2>/dev/null) || MEMORIES_JSON=""
    fi
    
    if [ -n "$MEMORIES_JSON" ] && [ "$MEMORIES_JSON" != "{}" ]; then
        log "✅ LLM 分析完成"
        echo "$MEMORIES_JSON" > /tmp/dream-analysis-result.json
    else
        log "⚠️  API 调用超时或失败，使用简化模式"
        MEMORIES_JSON="{}"
    fi
else
    log "⚠️  API 脚本不存在，使用简化模式"
    MEMORIES_JSON="{}"
fi

#===========================================
# Stage 3: Consolidate - 写入记忆
#===========================================
log "💾 Stage 3: Consolidate - 写入记忆..."

# 如果有 LLM 分析结果，创建独立的记忆文件
if [ -n "$MEMORIES_JSON" ] && [ "$MEMORIES_JSON" != "{}" ]; then
    CONSOLIDATE_SCRIPT="$SKILL_DIR/scripts/dream-consolidate.py"
    
    if [ -f "$CONSOLIDATE_SCRIPT" ]; then
        log "调用记忆文件生成器..."
        python3 "$CONSOLIDATE_SCRIPT" 2>&1
        CONSOLIDATE_RESULT=$?
        
        if [ $CONSOLIDATE_RESULT -eq 0 ]; then
            log "✅ 记忆文件创建完成"
        else
            log "⚠️ 记忆文件创建失败，使用摘要模式"
        fi
    else
        log "⚠️ 记忆文件生成器不存在，使用摘要模式"
    fi
fi

# 创建昨日日志的摘要记忆
SUMMARY_FILE="$MEMORY_DIR/project/daily-summary-${YESTERDAY}.md"

cat << EOF > "$SUMMARY_FILE"
---
name: daily-summary-${YESTERDAY}
type: project
description: ${YESTERDAY} 日志摘要
created: ${TODAY}
updated: ${TODAY}
---

# ${YESTERDAY} 日志摘要

## 概述
- 日志行数: ${LOG_LINES}
- 提炼时间: ${TODAY}

## 主要内容
$(echo "$LOG_CONTENT" | head -100)

EOF

log "✅ 已创建日志摘要: $SUMMARY_FILE"

# 更新 MEMORY.md 索引
update_index() {
    local type="$1"
    local name="$2"
    local summary="$3"
    local memory_path="$4"
    
    local index_file="$WORKSPACE_DIR/MEMORY.md"
    
    # 检查是否已经在索引中
    if grep -q "$memory_path" "$index_file" 2>/dev/null; then
        log "   ↩  已在索引中: $name"
        return
    fi
    
    # 构建新条目
    local new_entry="- [${name}](${memory_path}) — ${summary}"
    
    # 找到对应的类型 section 的结束位置
    local insert_after=""
    case "$type" in
        user)
            insert_after='^## user$'
            ;;
        feedback)
            insert_after='^## feedback$'
            ;;
        project)
            insert_after='^## project$'
            ;;
        reference)
            insert_after='^## reference$'
            ;;
    esac
    
    if [ -n "$insert_after" ]; then
        awk -v pattern="$insert_after" -v entry="$new_entry" '
            $0 ~ pattern { found=1; print; next }
            found && /^$/ { print entry; print; found=0; next }
            { print }
        ' "$index_file" > "$index_file.tmp" && mv "$index_file.tmp" "$index_file"
        log "   ✅ 已更新索引: $type/$name"
    fi
}

log "📝 更新 MEMORY.md 索引..."
update_index "project" "daily-summary-${YESTERDAY}" "日志摘要" "memory/project/daily-summary-${YESTERDAY}.md"

#===========================================
# Stage 4: Prune - 修剪过时记忆
#===========================================
log "✂️ Stage 4: Prune - 修剪过时记忆..."

# 检查过时的记忆（90天未更新）
OLD_THRESHOLD_DAYS=90
CUTOFF_DATE=$(date -v-${OLD_THRESHOLD_DAYS}d +%Y-%m-%d 2>/dev/null || date -d "$OLD_THRESHOLD_DAYS days ago" +%Y-%m-%d)

log "检查 ${CUTOFF_DATE} 之前的记忆..."

PRUNED_COUNT=0
for type in user feedback project reference; do
    TYPE_DIR="$MEMORY_DIR/$type"
    if [ -d "$TYPE_DIR" ]; then
        for file in "$TYPE_DIR"/*.md; do
            if [ -f "$file" ]; then
                # 读取 updated 字段
                UPDATED=$(grep "^updated:" "$file" 2>/dev/null | head -1 | sed 's/updated: //' | tr -d ' ')
                if [ -n "$UPDATED" ]; then
                    if [[ "$UPDATED" < "$CUTOFF_DATE" ]]; then
                        log "标记过时: $file (updated: $UPDATED)"
                        if ! grep -q "status: stale" "$file"; then
                            sed -i '' "s/^---$/---\nstatus: stale/" "$file"
                        fi
                        PRUNED_COUNT=$((PRUNED_COUNT + 1))
                    fi
                fi
            fi
        done
    fi
done

log "✂️ 标记了 ${PRUNED_COUNT} 个过时记忆"

#===========================================
# 完成
#===========================================
log "✅ Dream Agent 执行完成"
log "   日期: $YESTERDAY"
log "   日志行数: $LOG_LINES"
log "   提炼时间: $(date '+%Y-%m-%d %H:%M:%S')"
