#!/bin/bash
# 日记与学习条目自动关联脚本
# 自动检测日记中提到的学习 ID，建立双向链接
# 用法：./link-diary-lessons.sh [日期]

set -e

# 配置
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MEMORY_DIR="$WORKSPACE_DIR/memory"
LESSONS_DIR="$MEMORY_DIR/lessons"
WARM_DIR="$LESSONS_DIR/WARM"
HOT_DIR="$LESSONS_DIR/HOT"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
用法：$(basename "$0") [日期] [选项]

自动检测日记中提到的学习 ID，建立双向链接

参数:
  日期            可选，指定日期（格式：YYYY-MM-DD）
                  不指定则处理今日日记

选项:
  --all          处理本周所有日记
  --dry-run      预览模式，不实际修改
  -h, --help     显示帮助信息

功能:
1. 扫描日记中提到的学习 ID（ERR-*, LRN-*, DEC-*, PRJ-*, PPL-*, FEAT-*）
2. 在学习条目中添加"日记引用"字段
3. 在日记中添加"相关学习"章节

示例:
  $(basename "$0")                    # 处理今日日记
  $(basename "$0") 2026-04-06         # 处理指定日期
  $(basename "$0") --all              # 处理本周所有日记
EOF
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_dry() {
    echo -e "${YELLOW}[DRY-RUN]${NC} $1"
}

# 解析参数
TARGET_DATE=""
PROCESS_ALL=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            PROCESS_ALL=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            log_error "未知选项：$1"
            usage
            exit 1
            ;;
        *)
            if [ -z "$TARGET_DATE" ]; then
                TARGET_DATE="$1"
            else
                log_error "意外参数：$1"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

# 获取目标日期
if [ -z "$TARGET_DATE" ]; then
    TARGET_DATE=$(date +%Y-%m-%d)
fi

# 学习 ID 模式
ID_PATTERN="(ERR|LRN|DEC|PRJ|PPL|FEAT)-[0-9]{8}-[a-zA-Z0-9]{4}"

log_info "扫描日期：$TARGET_DATE"
log_info "学习 ID 模式：$ID_PATTERN"
echo ""

# 处理日记文件
DIARY_FILE="$MEMORY_DIR/$TARGET_DATE.md"

if [ ! -f "$DIARY_FILE" ]; then
    log_warn "日记文件不存在：$DIARY_FILE"
    exit 0
fi

# 提取日记中提到的学习 ID
MENTIONED_IDS=$(grep -oE "$ID_PATTERN" "$DIARY_FILE" 2>/dev/null | sort -u || echo "")

if [ -z "$MENTIONED_IDS" ]; then
    log_info "日记中未检测到学习 ID 引用"
    exit 0
fi

log_info "检测到 ${MENTIONED_IDS// / } 个学习 ID 引用"
echo ""

# 处理每个 ID
for lesson_id in $MENTIONED_IDS; do
    log_info "处理：$lesson_id"
    
    # 查找学习文件
    LESSON_FILE=$(find "$WARM_DIR" "$HOT_DIR" -name "*$lesson_id*.md" 2>/dev/null | head -1)
    
    if [ -z "$LESSON_FILE" ]; then
        log_warn "  未找到学习文件：$lesson_id"
        continue
    fi
    
    log_info "  找到学习文件：$LESSON_FILE"
    
    # 检查是否已有日记引用
    if grep -q "日记引用" "$LESSON_FILE" 2>/dev/null; then
        log_info "  已有日记引用，跳过"
    else
        if [ "$DRY_RUN" = true ]; then
            log_dry "  将添加日记引用到：$LESSON_FILE"
        else
            # 添加日记引用
            cat >> "$LESSON_FILE" << LINK

---

## 日记引用
- [$TARGET_DATE]($DIARY_FILE)
LINK
            log_info "  ✅ 已添加日记引用"
        fi
    fi
done

# 检查日记是否已有相关学习章节
if grep -q "## 📚 相关学习" "$DIARY_FILE" 2>/dev/null; then
    log_info "日记已有相关学习章节"
else
    if [ "$DRY_RUN" = true ]; then
        log_dry "  将添加相关学习章节到日记"
    else
        # 添加相关学习章节到日记
        cat >> "$DIARY_FILE" << LESSONS

---

## 📚 相关学习
LESSONS
        
        for lesson_id in $MENTIONED_IDS; do
            echo "- [$lesson_id](lessons/WARM/*/$lesson_id*.md)" >> "$DIARY_FILE"
        done
        
        log_info "✅ 已添加相关学习章节"
    fi
fi

echo ""
log_info "自动关联完成！"
