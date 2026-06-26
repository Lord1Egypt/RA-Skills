#!/bin/bash
# 学习晋升脚本 - Promote Lesson to HOT
# 将符合条件的 WARM 条目晋升到 HOT/memory-hot.md
# 晋升条件：7 天内使用 ≥3 次，状态为 resolved 或 promoted

set -e

# 配置
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LESSONS_DIR="$WORKSPACE_DIR/memory/lessons"
WARM_DIR="$LESSONS_DIR/WARM"
HOT_DIR="$LESSONS_DIR/HOT"
HOT_FILE="$HOT_DIR/memory-hot.md"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    cat << EOF
用法：$(basename "$0") [选项] [学习 ID]

将符合条件的学习条目晋升到 HOT/memory-hot.md

参数:
  学习 ID          可选，指定要晋升的条目 ID（如 LRN-20260406-001）
                   不指定则自动检测所有符合条件的条目

选项:
  --dry-run        预览模式，不实际执行晋升
  --force          强制晋升，忽略使用次数检查
  --threshold N    设置使用次数阈值（默认：3）
  --days N         设置天数窗口（默认：7）
  -h, --help       显示帮助信息

晋升条件:
  - 使用次数 ≥ threshold（默认 3 次）
  - 在最近 days 天内使用过（默认 7 天）
  - 状态为 resolved 或 promoted

示例:
  $(basename "$0")                          # 自动检测并晋升
  $(basename "$0") LRN-20260406-001         # 指定条目晋升
  $(basename "$0") --dry-run                # 预览模式
  $(basename "$0") --threshold 5            # 使用 5 次以上才晋升
  $(basename "$0") --force LRN-xxx          # 强制晋升
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

# Bash 版本检查
if [[ ${BASH_VERSINFO[0]} -lt 3 ]]; then
    log_error "需要 Bash 3.0 或更高版本"
    log_error "当前版本：${BASH_VERSION}"
    exit 1
fi

# 默认参数
DRY_RUN=false
FORCE=false
THRESHOLD=3
DAYS=7
SPECIFIC_ID=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --threshold)
            THRESHOLD="$2"
            shift 2
            ;;
        --days)
            DAYS="$2"
            shift 2
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
            if [ -z "$SPECIFIC_ID" ]; then
                SPECIFIC_ID="$1"
            else
                log_error "意外参数：$1"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

# 检查目录是否存在
if [ ! -d "$WARM_DIR" ]; then
    log_error "WARM 目录不存在：$WARM_DIR"
    log_error "请先运行目录结构调整脚本"
    exit 1
fi

# 创建 HOT 目录
if [ "$DRY_RUN" = false ]; then
    mkdir -p "$HOT_DIR"
fi

# 获取当前日期（7 天前）
CUTOFF_DATE=$(date -v-${DAYS}d +%Y-%m-%d 2>/dev/null || date -d "${DAYS} days ago" +%Y-%m-%d)

log_step "1/3 扫描 WARM 目录中的学习条目..."

# 查找所有学习文件
PROMOTE_CANDIDATES=()

if [ -n "$SPECIFIC_ID" ]; then
    # 指定 ID 模式
    PATTERN="*${SPECIFIC_ID}*"
else
    PATTERN="*.md"
fi

# 遍历所有子目录
for type_dir in "$WARM_DIR"/*/; do
    [ -d "$type_dir" ] || continue
    
    while IFS= read -r -d '' file; do
        [ -f "$file" ] || continue
        
        # 跳过 memory-hot.md 本身
        [[ "$(basename "$file")" == "memory-hot.md" ]] && continue
        
        # 提取 ID（从文件名）
        FILE_ID=$(basename "$file" .md)
        
        # 检查状态
        STATUS=$(grep -E "^\*\*状态：\*\*" "$file" 2>/dev/null | head -1 | sed 's/.*状态：\*\* *//' | sed 's/ *\*\*//' || echo "")
        
        # 跳过非 resolved/promoted 状态（除非强制）
        if [ "$FORCE" = false ]; then
            if [[ "$STATUS" != *"resolved"* && "$STATUS" != *"promoted"* ]]; then
                continue
            fi
        fi
        
        # 计算引用次数（被其他条目引用的次数）
        REFERENCE_COUNT=$(grep -r --include="*.md" "$FILE_ID" "$WARM_DIR" 2>/dev/null | wc -l | tr -d ' ')
        REFERENCE_COUNT=${REFERENCE_COUNT:-0}
        
        # 提取最后出现日期
        LAST_SEEN=$(grep -E "^\*\*最后出现：\*\*" "$file" 2>/dev/null | head -1 | sed 's/.*最后出现：\*\* *//' | sed 's/ *\*\*//' || echo "")
        
        # 检查是否在时间窗口内
        if [ -n "$LAST_SEEN" ] && [ "$FORCE" = false ]; then
            if [[ "$LAST_SEEN" < "$CUTOFF_DATE" ]]; then
                continue
            fi
        fi
        
        # 检查引用次数（被其他条目引用≥2 次）
        if [ "$FORCE" = false ] && [ "$REFERENCE_COUNT" -lt 2 ]; then
            continue
        fi
        
        PROMOTE_CANDIDATES+=("$file")
        
    done < <(find "$type_dir" -maxdepth 1 -name "$PATTERN" -type f -print0 2>/dev/null)
done

if [ ${#PROMOTE_CANDIDATES[@]} -eq 0 ]; then
    log_info "没有找到符合条件的晋升候选"
    exit 0
fi

log_info "找到 ${#PROMOTE_CANDIDATES[@]} 个晋升候选"

# 初始化 HOT 文件（如果不存在）
if [ "$DRY_RUN" = false ] && [ ! -f "$HOT_FILE" ]; then
    cat > "$HOT_FILE" << 'HEADER'
# HOT Memory

**最后更新：** TIMESTAMP
**条目数量：** 0/20
**自动刷新：** 每周五

---

> 本文件包含高频使用的规则和偏好，每次会话自动加载。
> 条目按使用频率排序，最多保留 20 条。
> 
> **晋升条件：** 7 天内使用 ≥3 次  
> **降级条件：** 30 天未使用

---

## 🎯 行为规则

## 🛠️ 技术偏好

## 📋 项目约定

---

> **自动维护规则：**
> - 新条目从 WARM/ 晋升（7 天内≥3 次使用）
> - 30 天 未使用的条目自动降级回 WARM/
> - 始终保持 ≤20 条
> - 每周五自动整理排序
HEADER
fi

log_step "2/3 处理晋升候选..."

for file in "${PROMOTE_CANDIDATES[@]}"; do
    FILE_ID=$(basename "$file" .md)
    TITLE=$(head -1 "$file" | sed 's/^# \[.*\] //')
    TYPE=$(basename "$(dirname "$file")")
    
    # 提取关键信息（带默认值）
    USAGE_COUNT=$(grep -E "^\*\*出现次数：\*\*" "$file" 2>/dev/null | head -1 | sed 's/.*出现次数：\*\* *//' | sed 's/ *\*\*//' || echo "1")
    USAGE_COUNT=${USAGE_COUNT:-1}
    LAST_SEEN=$(grep -E "^\*\*最后出现：\*\*" "$file" 2>/dev/null | head -1 | sed 's/.*最后出现：\*\* *//' | sed 's/ *\*\*//' || echo "未知")
    
    if [ "$DRY_RUN" = true ]; then
        log_dry "将晋升：$FILE_ID"
        echo "       标题：$TITLE"
        echo "       类型：$TYPE"
        echo "       引用次数：$REFERENCE_COUNT"
        echo "       最后修改：$LAST_MODIFIED"
        echo ""
    else
        log_info "晋升：$FILE_ID"
        
        # 创建临时文件，新条目放在开头
        TEMP_FILE=$(mktemp)
        cat > "$TEMP_FILE" << ENTRY
### $TITLE
- **ID:** $FILE_ID
- **类型:** $TYPE
- **来源:** $file
- **引用次数:** $REFERENCE_COUNT
- **最后修改:** $LAST_MODIFIED
- **晋升时间:** $(date +%Y-%m-%dT%H:%M:%S+08:00)

---

ENTRY
        # 追加原有内容（跳过 header）
        tail -n +12 "$HOT_FILE" >> "$TEMP_FILE" 2>/dev/null || true
        mv "$TEMP_FILE" "$HOT_FILE"
        
        # 更新原文件，添加晋升标记
        if grep -q "晋升到 HOT" "$file" 2>/dev/null; then
            log_warn "  $FILE_ID 已有晋升标记，跳过更新"
        else
            if ! cat >> "$file" << PROMOTED

---

## 晋升记录
- **晋升到 HOT:** $(date +%Y-%m-%d)
- **来源文件:** $file
PROMOTED
            then
                log_error "更新文件失败：$file"
                continue
            fi
        fi
    fi
done

log_step "3/3 完成"

if [ "$DRY_RUN" = true ]; then
    echo ""
    log_info "预览模式 - 未执行实际晋升"
    echo "运行不带 --dry-run 的参数执行实际晋升"
else
    # 更新 HOT 文件头部
    ENTRY_COUNT=$(grep -c "^### " "$HOT_FILE" 2>/dev/null || echo "0")
    sed_inplace "s/\*\*条目数量：\*\* [0-9]*\/20/**条目数量：** $ENTRY_COUNT\/20/" "$HOT_FILE"
    sed_inplace "s/\*\*最后更新：\*\*.*/**最后更新：** $(date +%Y-%m-%dT%H:%M:%S+08:00)/" "$HOT_FILE"
    
    echo ""
    log_info "✅ 晋升完成！"
    echo "  HOT 文件：$HOT_FILE"
    echo "  当前条目数：$ENTRY_COUNT/20"
fi
