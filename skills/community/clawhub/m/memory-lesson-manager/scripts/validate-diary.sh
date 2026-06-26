#!/bin/bash
# 日记质量检查脚本
# 检查日记是否符合规范（含反思环节、内容质量等）
# 用法：./validate-diary.sh [日期] [--fix]

set -e

# 配置
# 支持环境变量或自动检测工作区
if [ -n "$OPENCLAW_WORKSPACE" ]; then
    WORKSPACE_DIR="$OPENCLAW_WORKSPACE"
else
    WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi
MEMORY_DIR="$WORKSPACE_DIR/memory"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
用法：$(basename "$0") [日期] [选项]

检查日记是否符合规范（含反思环节、内容质量等）

参数:
  日期            可选，检查指定日期的日记（格式：YYYY-MM-DD）
                  不指定则检查今日日记

选项:
  --fix          自动修复可修复的问题
  --strict       严格模式，P3 日记也要检查内容长度
  --all          检查本周所有日记
  -h, --help     显示帮助信息

检查项目:
  1. 日记文件是否存在
  2. 是否包含反思环节（🔄 自我反思）
  3. 是否包含 P1/P2/P3 重要性标记
  4. 内容长度是否达标（P1>200 字，P2>100 字，P3>50 字）
  5. 是否有学习条目链接（如产生学习）
  6. 是否记录了问题和解决方案

示例:
  $(basename "$0")                    # 检查今日日记
  $(basename "$0") 2026-04-06         # 检查指定日期
  $(basename "$0") --all              # 检查本周所有日记
  $(basename "$0") --fix              # 自动修复问题
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

log_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
}

# 跨平台 sed 函数
sed_inplace() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

# 解析参数
TARGET_DATE=""
FIX_MODE=false
STRICT_MODE=false
CHECK_ALL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --fix)
            FIX_MODE=true
            shift
            ;;
        --strict)
            STRICT_MODE=true
            shift
            ;;
        --all)
            CHECK_ALL=true
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

# 检查单个日记文件
check_diary() {
    local date=$1
    local diary_file="$MEMORY_DIR/$date.md"
    local issues=0
    local warnings=0
    
    echo ""
    log_step "检查日记：$date.md"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 检查 1: 文件是否存在
    if [ ! -f "$diary_file" ]; then
        log_fail "日记文件不存在：$diary_file"
        if [ "$FIX_MODE" = true ]; then
            log_info "正在创建日记文件..."
            cp "$MEMORY_DIR/templates/diary-template.md" "$diary_file"
            log_info "已创建日记文件，请编辑补充内容"
        fi
        return 1
    else
        log_pass "日记文件存在"
    fi
    
    # 读取文件内容
    local content=$(cat "$diary_file")
    local line_count=$(wc -l < "$diary_file")
    local char_count=$(wc -c < "$diary_file")
    
    # 检查 2: 是否包含反思环节
    if echo "$content" | grep -q "🔄 自我反思\|### 自我反思\|## 自我反思"; then
        log_pass "包含反思环节"
    else
        log_fail "缺少反思环节（🔄 自我反思）"
        ((issues++))
        if [ "$FIX_MODE" = true ]; then
            log_info "正在添加反思环节..."
            cat >> "$diary_file" << 'REFLECTION'

### 🔄 自我反思
- **做得好的：** 
- **可改进的：** 
- **学到的：** 
REFLECTION
            log_info "已添加反思环节，请编辑补充内容"
        fi
    fi
    
    # 检查 3: 是否包含重要性标记
    if echo "$content" | grep -qE "\[P1\]|\[P2\]|\[P3\]"; then
        log_pass "包含重要性标记（P1/P2/P3）"
        
        # 检测最高优先级
        local priority="P3"
        if echo "$content" | grep -q "\[P1\]"; then
            priority="P1"
        elif echo "$content" | grep -q "\[P2\]"; then
            priority="P2"
        fi
        
        # 检查 4: 内容长度是否达标
        local min_chars=50
        if [ "$priority" = "P1" ]; then
            min_chars=200
        elif [ "$priority" = "P2" ]; then
            min_chars=100
        fi
        
        if [ "$STRICT_MODE" = true ] || [ "$priority" != "P3" ]; then
            if [ "$char_count" -ge "$min_chars" ]; then
                log_pass "内容长度达标 ($char_count 字符 >= $min_chars)"
            else
                log_fail "内容长度不足 ($char_count 字符 < $min_chars)"
                ((issues++))
            fi
        else
            log_info "内容长度：$char_count 字符（P3 模式，跳过检查）"
        fi
    else
        log_warn "缺少重要性标记（[P1]/[P2]/[P3]）"
        ((warnings++))
        if [ "$FIX_MODE" = true ]; then
            log_info "正在添加重要性标记..."
            sed_inplace 's/## HH:MM - 任务名称/## HH:MM - 任务名称 [P3]/' "$diary_file"
            log_info "已添加 [P3] 标记，请根据实际情况调整"
        fi
    fi
    
    # 检查 3: 是否包含重要性标记
    if echo "$content" | grep -qE "\[P1\]|\[P2\]|\[P3\]"; then
        log_pass "包含重要性标记（P1/P2/P3）"
        
        # 检测最高优先级
        local priority="P3"
        if echo "$content" | grep -q "\[P1\]"; then
            priority="P1"
        elif echo "$content" | grep -q "\[P2\]"; then
            priority="P2"
        fi
        
        # 检查 4: 内容长度是否达标
        local min_chars=50
        if [ "$priority" = "P1" ]; then
            min_chars=200
        elif [ "$priority" = "P2" ]; then
            min_chars=100
        fi
        
        if [ "$STRICT_MODE" = true ] || [ "$priority" != "P3" ]; then
            if [ "$char_count" -ge "$min_chars" ]; then
                log_pass "内容长度达标 ($char_count 字符 >= $min_chars)"
            else
                log_fail "内容长度不足 ($char_count 字符 < $min_chars)"
                ((issues++))
            fi
        else
            log_info "内容长度：$char_count 字符（P3 模式，跳过检查）"
        fi
    else
        log_warn "缺少重要性标记（[P1]/[P2]/[P3]）"
        ((warnings++))
        if [ "$FIX_MODE" = true ]; then
            log_info "正在添加重要性标记..."
            sed_inplace 's/## HH:MM - 任务名称/## HH:MM - 任务名称 [P3]/' "$diary_file"
            rm -f "$diary_file.bak"
            log_info "已添加 [P3] 标记，请根据实际情况调整"
        fi
    fi
    
    # 检查 5: 是否有学习条目链接
    if echo "$content" | grep -qE "LRN-|ERR-|FEAT-|DEC-|PRJ-|PPL-"; then
        log_pass "包含学习条目链接"
    else
        log_info "未检测到学习条目链接（可选）"
    fi
    
    # 检查 6: 是否记录了问题和解决方案
    if echo "$content" | grep -qi "问题\|解决"; then
        log_pass "记录了问题和解决方案"
    else
        log_info "未检测到问题和解决方案记录（可选）"
    fi
    
    # 检查 7: 日记模板内容
    if echo "$content" | grep -q "任务名称 \[P"; then
        log_pass "使用了日记模板格式"
    else
        log_warn "可能未使用日记模板格式"
        ((warnings++))
    fi
    
    # 总结
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "检查结果："
    echo "  行数：$line_count"
    echo "  字符数：$char_count"
    echo "  问题数：$issues"
    echo "  警告数：$warnings"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if [ "$issues" -eq 0 ] && [ "$warnings" -eq 0 ]; then
        log_info "✅ 日记质量优秀！"
        return 0
    elif [ "$issues" -eq 0 ]; then
        log_info "✅ 日记质量合格（有 $warnings 个警告）"
        return 0
    else
        log_error "❌ 日记质量不达标（有 $issues 个问题）"
        return 1
    fi
}

# 主流程
log_step "记忆系统日记质量检查"
echo ""

if [ "$CHECK_ALL" = true ]; then
    # 检查本周所有日记
    log_info "检查本周所有日记..."
    
    local total_issues=0
    local total_warnings=0
    local checked=0
    
    for i in {0..6}; do
        # 跨平台日期处理
        local check_date
        if [[ "$OSTYPE" == "darwin"* ]]; then
            check_date=$(date -v-${i}d +%Y-%m-%d 2>/dev/null)
        else
            check_date=$(date -d "$i days ago" +%Y-%m-%d 2>/dev/null)
        fi
        if [ -z "$check_date" ]; then
            check_date=$(date +%Y-%m-%d)  # 回退到今日
        fi
        if check_diary "$check_date"; then
            ((checked++))
        else
            ((total_issues++))
        fi
    done
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "本周检查总结："
    echo "  检查天数：7"
    echo "  有日记的天数：$checked"
    echo "  问题总数：$total_issues"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
else
    # 检查单个日期
    check_diary "$TARGET_DATE"
    exit_code=$?
    
    if [ "$exit_code" -ne 0 ]; then
        echo ""
        log_info "提示："
        echo "  使用 --fix 自动修复可修复的问题"
        echo "  使用 --all 检查本周所有日记"
        echo "  编辑日记文件：$MEMORY_DIR/$TARGET_DATE.md"
    fi
    
    exit $exit_code
fi
