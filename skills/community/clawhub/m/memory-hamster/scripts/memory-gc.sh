#!/bin/bash

# 记忆垃圾回收脚本 - 每周日 00:00 执行
# 功能：主动遗忘 + 冷存储归档 + 温度模型
# 
# 用法：./memory-gc.sh [--dry-run]
#   --dry-run: 仅显示将要执行的操作，不实际移动文件

set -e

DRY_RUN="${1:-}"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
ARCHIVE_DIR="$WORKSPACE/memory/.archive"
CURRENT_MONTH=$(date +%Y-%m)

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_section() {
    echo ""
    echo -e "${BLUE}=== $1 ===${NC}"
}

echo "========================================"
echo "  记忆 GC 开始 - $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

if [ "$DRY_RUN" = "--dry-run" ]; then
    log_warn "DRY RUN 模式 - 不会实际移动文件"
fi

# 1. 确保归档目录存在
if [ "$DRY_RUN" != "--dry-run" ]; then
    mkdir -p "$ARCHIVE_DIR/$CURRENT_MONTH"
fi

# 2. 找出超过 30 天的每日日志（冷数据）
log_section "扫描冷数据（超过 30 天的日志）"

COLD_FILES=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f -mtime +30 2>/dev/null | grep -v "INDEX.md" | grep -v "MEMORY.md" || true)

if [ -z "$COLD_FILES" ]; then
    log_info "没有需要归档的冷数据"
    ARCHIVED_COUNT=0
else
    log_info "发现冷数据："
    echo "$COLD_FILES" | while read -r file; do
        if [ -n "$file" ]; then
            filename=$(basename "$file")
            echo "  - $filename"
        fi
    done
    
    ARCHIVED_COUNT=$(echo "$COLD_FILES" | grep -c ".md" 2>/dev/null || echo "0")
    
    if [ "$DRY_RUN" != "--dry-run" ]; then
        for file in $COLD_FILES; do
            if [ -n "$file" ] && [ -f "$file" ]; then
                filename=$(basename "$file")
                log_info "归档：$filename → .archive/$CURRENT_MONTH/"
                mv "$file" "$ARCHIVE_DIR/$CURRENT_MONTH/$filename"
            fi
        done
        log_info "冷数据已归档到：$ARCHIVE_DIR/$CURRENT_MONTH/"
    else
        log_warn "DRY RUN: 将归档 $ARCHIVED_COUNT 个文件到 .archive/$CURRENT_MONTH/"
    fi
fi

# 3. 温度统计
log_section "温度统计"

# 热数据（最近 7 天）
HOT_COUNT=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f -mtime -7 2>/dev/null | grep -v "INDEX.md" | grep -v "MEMORY.md" | wc -l)
echo "🔥 热数据（<7 天）: $HOT_COUNT 个"

# 温数据（7-30 天）
WARM_COUNT=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f -mtime +7 -mtime -30 2>/dev/null | wc -l)
echo "🟡 温数据（7-30 天）: $WARM_COUNT 个"

# 冷数据（>30 天，已归档）
COLD_COUNT=$(find "$ARCHIVE_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
echo "❄️ 冷数据（已归档）: $COLD_COUNT 个"

# 4. 结构化目录统计
log_section "结构化目录"

count_files() {
    local dir="$1"
    if [ -d "$dir" ]; then
        find "$dir" -name "*.md" -type f 2>/dev/null | wc -l
    else
        echo "0"
    fi
}

LESSONS_COUNT=$(count_files "$MEMORY_DIR/lessons")
DECISIONS_COUNT=$(count_files "$MEMORY_DIR/decisions")
PEOPLE_COUNT=$(count_files "$MEMORY_DIR/people")
REFLECTIONS_COUNT=$(count_files "$MEMORY_DIR/reflections")

echo "📚 Lessons: $LESSONS_COUNT 个"
echo "🎯 Decisions: $DECISIONS_COUNT 个"
echo "👤 People: $PEOPLE_COUNT 个"
echo "💭 Reflections: $REFLECTIONS_COUNT 个"

# 5. 磁盘空间统计
log_section "磁盘空间"

if [ -d "$MEMORY_DIR" ]; then
    MEMORY_SIZE=$(du -sh "$MEMORY_DIR" 2>/dev/null | cut -f1)
    echo "memory/ 目录：$MEMORY_SIZE"
else
    echo "memory/ 目录：不存在"
fi

if [ -d "$ARCHIVE_DIR" ]; then
    ARCHIVE_SIZE=$(du -sh "$ARCHIVE_DIR" 2>/dev/null | cut -f1)
    echo ".archive/ 目录：$ARCHIVE_SIZE"
else
    echo ".archive/ 目录：不存在"
fi

# 6. 生成 GC 报告
if [ "$DRY_RUN" != "--dry-run" ]; then
    GC_REPORT="$ARCHIVE_DIR/gc-report-$CURRENT_MONTH.md"
    
    # 追加模式，同月多次运行会更新
    cat > "$GC_REPORT" << EOF
# GC 报告 - $CURRENT_MONTH

**执行时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 归档统计
- 本次归档文件数：$ARCHIVED_COUNT
- 累计归档文件数：$COLD_COUNT

## 温度分布
| 温度 | 数量 | 说明 |
|------|------|------|
| 🔥 热 | $HOT_COUNT | 最近 7 天 |
| 🟡 温 | $WARM_COUNT | 7-30 天 |
| ❄️ 冷 | $COLD_COUNT | 已归档 |

## 结构化知识
- Lessons: $LESSONS_COUNT
- Decisions: $DECISIONS_COUNT
- People: $PEOPLE_COUNT
- Reflections: $REFLECTIONS_COUNT

## 磁盘使用
- memory/: $MEMORY_SIZE
- .archive/: $ARCHIVE_SIZE

---
*自动生成 by agent-memory-skill*
EOF

    log_info "GC 报告已生成：$GC_REPORT"
fi

echo ""
echo "========================================"
echo "  记忆 GC 完成"
echo "========================================"