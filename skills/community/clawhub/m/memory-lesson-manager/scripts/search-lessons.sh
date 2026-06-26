#!/bin/bash
# 学习条目语义搜索脚本
# 基于内容相似度的模糊匹配
# 用法：./search-lessons.sh <关键词> [--fuzzy]

set -e

# 配置
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LESSONS_DIR="$WORKSPACE_DIR/memory/lessons"
WARM_DIR="$LESSONS_DIR/WARM"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
用法：$(basename "$0") <关键词> [选项]

基于内容相似度的模糊搜索学习条目

参数:
  关键词          搜索关键词（支持中文）

选项:
  --fuzzy        模糊匹配（同义词、近义词）
  --type TYPE    指定类型（errors/corrections/best-practices 等）
  --limit N      限制结果数量（默认：10）
  -h, --help     显示帮助信息

模糊匹配规则:
- "Git 认证" 匹配 "GitHub 登录"、"认证失败"
- "API 设计" 匹配 "接口规范"、"REST"
- "部署" 匹配 "上线"、"发布"

示例:
  $(basename "$0") "Git 认证"
  $(basename "$0") "API 设计" --fuzzy
  $(basename "$0") "部署" --type errors --limit 5
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

log_result() {
    echo -e "${BLUE}[RESULT]${NC} $1"
}

# 解析参数
QUERY=""
FUZZY=false
TYPE=""
LIMIT=10

while [[ $# -gt 0 ]]; do
    case $1 in
        --fuzzy)
            FUZZY=true
            shift
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --limit)
            LIMIT="$2"
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
            if [ -z "$QUERY" ]; then
                QUERY="$1"
            else
                log_error "意外参数：$1"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$QUERY" ]; then
    log_error "搜索关键词不能为空"
    usage
    exit 1
fi

# 同义词映射（模糊匹配）
declare -A SYNONYMS
SYNONYMS["Git"]="GitHub|认证|登录|auth"
SYNONYMS["API"]="接口|REST|HTTP|端点"
SYNONYMS["部署"]="上线|发布|deploy|publish"
SYNONYMS["错误"]="报错|失败|error|fail"
SYNONYMS["认证"]="auth|登录|login|credential"
SYNONYMS["设计"]="规范|架构|pattern"

# 构建搜索模式
SEARCH_PATTERN="$QUERY"

if [ "$FUZZY" = true ]; then
    # 扩展同义词
    for key in "${!SYNONYMS[@]}"; do
        if [[ "$QUERY" == *"$key"* ]]; then
            SEARCH_PATTERN="$SEARCH_PATTERN|${SYNONYMS[$key]}"
        fi
    done
fi

log_info "搜索关键词：$QUERY"
log_info "搜索模式：$SEARCH_PATTERN"
log_info "模糊匹配：$FUZZY"
echo ""

# 确定搜索目录
if [ -n "$TYPE" ]; then
    SEARCH_DIR="$WARM_DIR/$TYPE"
    if [ ! -d "$SEARCH_DIR" ]; then
        log_error "类型目录不存在：$SEARCH_DIR"
        exit 1
    fi
else
    SEARCH_DIR="$WARM_DIR"
fi

# 执行搜索
RESULTS=()
MATCH_COUNT=0

while IFS= read -r -d '' file; do
    [ -f "$file" ] || continue
    
    # 搜索标题和内容
    if grep -qiE "$SEARCH_PATTERN" "$file" 2>/dev/null; then
        RESULTS+=("$file")
        ((MATCH_COUNT++))
        
        # 达到限制则停止
        if [ "$MATCH_COUNT" -ge "$LIMIT" ]; then
            break
        fi
    fi
done < <(find "$SEARCH_DIR" -name "*.md" -type f -print0 2>/dev/null)

# 输出结果
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "找到 $MATCH_COUNT 个匹配结果"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ ${#RESULTS[@]} -eq 0 ]; then
    log_warn "未找到匹配的结果"
    echo ""
    echo "建议："
    echo "  1. 尝试使用 --fuzzy 模糊匹配"
    echo "  2. 使用更通用的关键词"
    echo "  3. 检查关键词拼写"
    exit 0
fi

# 显示结果
for i in "${!RESULTS[@]}"; do
    file="${RESULTS[$i]}"
    FILE_ID=$(basename "$file" .md)
    TITLE=$(head -1 "$file" | sed 's/^# \[.*\] //' | head -c 60)
    TYPE_DIR=$(basename "$(dirname "$file")")
    
    # 计算匹配度（基于匹配次数）
    MATCH_SCORE=$(grep -ciE "$SEARCH_PATTERN" "$file" 2>/dev/null || echo "1")
    
    echo "$((i+1)). [$FILE_ID] $TITLE"
    echo "   类型：$TYPE_DIR"
    echo "   匹配度：$MATCH_SCORE 次"
    echo "   路径：$file"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "提示："
echo "  查看详细：cat <文件路径>"
echo "  模糊搜索：$(basename "$0") \"$QUERY\" --fuzzy"
echo "  指定类型：$(basename "$0") \"$QUERY\" --type errors"
