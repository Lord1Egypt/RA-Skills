#!/bin/bash
# 学习归档脚本 - Archive Cold Lessons
# 将 90 天未使用的 WARM 条目归档到 COLD/archive/
# 支持恢复已归档的条目

set -e

# 配置
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LESSONS_DIR="$WORKSPACE_DIR/memory/lessons"
WARM_DIR="$LESSONS_DIR/WARM"
COLD_DIR="$LESSONS_DIR/COLD/archive"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    cat << EOF
用法：$(basename "$0") [选项]

将 90 天未使用的学习条目归档到 COLD/archive/

选项:
  --dry-run        预览模式，不实际执行归档
  --days N         设置天数阈值（默认：90）
  --restore ID     从 COLD 恢复指定 ID 的条目到 WARM
  --list-cold      列出所有已归档的条目
  -h, --help       显示帮助信息

归档条件:
  - 最后出现日期 > days 天前（默认 90 天）
  - 状态不是 in_progress

示例:
  $(basename "$0")                    # 自动检测并归档
  $(basename "$0") --dry-run          # 预览模式
  $(basename "$0") --days 60          # 60 天未用就归档
  $(basename "$0") --restore ERR-xxx  # 恢复已归档条目
  $(basename "$0") --list-cold        # 查看已归档列表
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

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

log_dry() {
    echo -e "${YELLOW}[DRY-RUN]${NC} $1"
}

# 跨平台 sed 函数
sed_inplace() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# 默认参数
DRY_RUN=false
DAYS=90
RESTORE_ID=""
LIST_COLD=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --days)
            DAYS="$2"
            shift 2
            ;;
        --restore)
            RESTORE_ID="$2"
            shift 2
            ;;
        --list-cold)
            LIST_COLD=true
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
            log_error "意外参数：$1"
            usage
            exit 1
            ;;
    esac
done

# 处理 --list-cold
if [ "$LIST_COLD" = true ]; then
    if [ ! -d "$COLD_DIR" ]; then
        log_info "COLD 归档目录为空"
        exit 0
    fi
    
    log_info "已归档的学习条目："
    echo ""
    
    COUNT=0
    while IFS= read -r -d '' file; do
        FILE_ID=$(basename "$file" .md)
        ARCHIVE_DATE=$(grep -E "归档日期:" "$file" 2>/dev/null | head -1 | sed 's/.*归档日期： *//' || echo "未知")
        echo "  - $FILE_ID (归档于：$ARCHIVE_DATE)"
        ((COUNT++)) || true
    done < <(find "$COLD_DIR" -name "*.md" -type f -print0 2>/dev/null)
    
    echo ""
    log_info "共 $COUNT 个归档条目"
    exit 0
fi

# 处理 --restore
if [ -n "$RESTORE_ID" ]; then
    log_step "恢复归档条目：$RESTORE_ID"
    
    # 在 COLD 目录中查找
    SOURCE_FILE=$(find "$COLD_DIR" -name "*${RESTORE_ID}*.md" -type f 2>/dev/null | head -1)
    
    if [ -z "$SOURCE_FILE" ]; then
        log_error "未找到归档条目：$RESTORE_ID"
        log_error "使用 --list-cold 查看已归档列表"
        exit 1
    fi
    
    # 确定目标目录类型
    FILE_TYPE=""
    if [[ "$RESTORE_ID" == ERR-* ]]; then
        FILE_TYPE="errors"
    elif [[ "$RESTORE_ID" == LRN-* ]]; then
        # 检查原类别
        if grep -q "类别：.*best_practice" "$SOURCE_FILE" 2>/dev/null; then
            FILE_TYPE="best-practices"
        else
            FILE_TYPE="corrections"
        fi
    elif [[ "$RESTORE_ID" == FEAT-* ]]; then
        FILE_TYPE="feature-requests"
    elif [[ "$RESTORE_ID" == DEC-* ]]; then
        FILE_TYPE="decisions"
    elif [[ "$RESTORE_ID" == PRJ-* ]]; then
        FILE_TYPE="projects"
    elif [[ "$RESTORE_ID" == PPL-* ]]; then
        FILE_TYPE="people"
    else
        FILE_TYPE="corrections"
    fi
    
    TARGET_DIR="$WARM_DIR/$FILE_TYPE"
    mkdir -p "$TARGET_DIR"
    
    if [ "$DRY_RUN" = true ]; then
        log_dry "将恢复：$(basename "$SOURCE_FILE")"
        log_dry "目标目录：$TARGET_DIR"
    else
        # 移动文件
        mv "$SOURCE_FILE" "$TARGET_DIR/"
        
        # 更新文件，移除归档标记
        TARGET_FILE="$TARGET_DIR/$(basename "$SOURCE_FILE")"
        if grep -q "## 归档记录" "$TARGET_FILE" 2>/dev/null; then
            # 使用 sed 删除归档记录部分
            sed_inplace '/^## 归档记录/,$d' "$TARGET_FILE"
        fi
        
        # 更新状态为 pending（如果是 wont_fix 则保持）
        if ! grep -q "状态：.*wont_fix" "$TARGET_FILE" 2>/dev/null; then
            sed_inplace "s/状态：\*\* archived/状态：** pending/" "$TARGET_FILE"
        fi
        
        log_info "✅ 已恢复：$(basename "$SOURCE_FILE")"
        log_info "   目标目录：$TARGET_DIR"
    fi
    
    exit 0
fi

# 检查目录是否存在
if [ ! -d "$WARM_DIR" ]; then
    log_error "WARM 目录不存在：$WARM_DIR"
    log_error "请先运行目录结构调整脚本"
    exit 1
fi

# 创建 COLD 目录
if [ "$DRY_RUN" = false ]; then
    mkdir -p "$COLD_DIR"
fi

# 获取当前日期（遗忘曲线：根据引用频率动态调整）
# 高频引用（≥5 次）→ 180 天
# 中频引用（2-4 次）→ 90 天
# 低频引用（0-1 次）→ 30 天
CUTOFF_DATE=$(date -v-${DAYS}d +%Y-%m-%d 2>/dev/null || date -d "${DAYS} days ago" +%Y-%m-%d)

log_step "1/3 扫描 WARM 目录中的过期条目..."

# 查找所有学习文件
ARCHIVE_CANDIDATES=()

for type_dir in "$WARM_DIR"/*/; do
    [ -d "$type_dir" ] || continue
    
    while IFS= read -r -d '' file; do
        [ -f "$file" ] || continue
        
        # 跳过 memory-hot.md
        [[ "$(basename "$file")" == "memory-hot.md" ]] && continue
        
        # 提取 ID
        FILE_ID=$(basename "$file" .md)
        
        # 检查状态，跳过 in_progress
        STATUS=$(grep -E "^\*\*状态：\*\*" "$file" 2>/dev/null | head -1 | sed 's/.*状态：\*\* *//' | sed 's/ *\*\*//' || echo "")
        if [[ "$STATUS" == *"in_progress"* ]]; then
            continue
        fi
        
        # 计算引用次数
        REF_COUNT=$(grep -r --include="*.md" "$(basename "$file" .md)" "$WARM_DIR" 2>/dev/null | wc -l | tr -d ' ')
        
        # 根据引用频率动态调整归档时间
        if [ "$REF_COUNT" -ge 5 ]; then
            # 高频引用：180 天
            FILE_CUTOFF=$(date -v-180d +%Y-%m-%d 2>/dev/null || date -d "180 days ago" +%Y-%m-%d)
        elif [ "$REF_COUNT" -ge 2 ]; then
            # 中频引用：90 天
            FILE_CUTOFF=$(date -v-90d +%Y-%m-%d 2>/dev/null || date -d "90 days ago" +%Y-%m-%d)
        else
            # 低频引用：30 天
            FILE_CUTOFF=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d "30 days ago" +%Y-%m-%d)
        fi
        
        # 提取最后修改时间
        LAST_MODIFIED=$(stat -f %Sm -t %Y-%m-%d "$file" 2>/dev/null || stat -c %y "$file" 2>/dev/null | cut -d' ' -f1 || echo "")
        
        # 检查是否超过动态阈值
        if [ -n "$LAST_MODIFIED" ] && [[ "$LAST_MODIFIED" < "$FILE_CUTOFF" ]]; then
            ARCHIVE_CANDIDATES+=("$file")
        fi
        
    done < <(find "$type_dir" -maxdepth 1 -name "*.md" -type f -print0 2>/dev/null)
done

if [ ${#ARCHIVE_CANDIDATES[@]} -eq 0 ]; then
    log_info "没有找到需要归档的过期条目"
    exit 0
fi

log_info "找到 ${#ARCHIVE_CANDIDATES[@]} 个归档候选（${DAYS}天未使用）"

log_step "2/3 处理归档..."

for file in "${ARCHIVE_CANDIDATES[@]}"; do
    FILE_ID=$(basename "$file" .md)
    TITLE=$(head -1 "$file" | sed 's/^# \[.*\] //')
    TYPE=$(basename "$(dirname "$file")")
    
    # 提取最后出现日期
    LAST_SEEN=$(grep -E "^\*\*最后出现：\*\*" "$file" 2>/dev/null | head -1 | sed 's/.*最后出现：\*\* *//' | sed 's/ *\*\*//' || echo "未知")
    
    if [ "$DRY_RUN" = true ]; then
        log_dry "将归档：$FILE_ID"
        echo "       标题：$TITLE"
        echo "       类型：$TYPE"
        echo "       最后使用：$LAST_SEEN"
        echo ""
    else
        log_info "归档：$FILE_ID"
        
        # 移动文件到 COLD
        mv "$file" "$COLD_DIR/"
        
        # 更新文件，添加归档标记
        TARGET_FILE="$COLD_DIR/$(basename "$file")"
        cat >> "$TARGET_FILE" << ARCHIVED

---

## 归档记录
- **归档日期:** $(date +%Y-%m-%d)
- **归档原因:** ${DAYS}天未使用
- **原位置:** $WARM_DIR/$TYPE/$FILE_ID.md
- **恢复命令:** \`./scripts/archive-cold.sh --restore $FILE_ID\`
ARCHIVED
        
        # 更新状态为 archived
        sed_inplace "s/状态：\*\* [a-z_]*/状态：** archived/" "$TARGET_FILE"
        rm -f "$TARGET_FILE.bak"
    fi
done

log_step "3/3 完成"

if [ "$DRY_RUN" = true ]; then
    echo ""
    log_info "预览模式 - 未执行实际归档"
    echo "运行不带 --dry-run 的参数执行实际归档"
    echo ""
    echo "恢复已归档条目："
    echo "  ./scripts/archive-cold.sh --restore <条目 ID>"
else
    echo ""
    log_info "✅ 归档完成！"
    echo "  归档目录：$COLD_DIR"
    echo "  本次归档：${#ARCHIVE_CANDIDATES[@]} 个条目"
    echo ""
    echo "恢复已归档条目："
    echo "  ./scripts/archive-cold.sh --restore <条目 ID>"
    echo "  ./scripts/archive-cold.sh --list-cold"
fi
