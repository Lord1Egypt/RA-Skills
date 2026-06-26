#!/bin/bash
# 记忆系统测试脚本
# 验证目录结构、模板文件、脚本权限等
# 用法：./test-memory-system.sh

# 不使用 set -e，让测试继续运行完所有检查

# 配置
# 支持环境变量或自动检测工作区
if [ -n "$OPENCLAW_WORKSPACE" ]; then
    WORKSPACE_DIR="$OPENCLAW_WORKSPACE"
elif [ -n "$CLAW_WORKSPACE" ]; then
    WORKSPACE_DIR="$CLAW_WORKSPACE"
else
    # 从 skill 目录向上两级找到 workspace
    # skills/memory-lesson-manager/scripts/ → workspace/
    WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
    # 验证是否包含 skills/memory-lesson-manager
    if [ ! -d "$WORKSPACE_DIR/skills/memory-lesson-manager" ]; then
        # 尝试从当前工作目录
        WORKSPACE_DIR="$(pwd)"
    fi
fi

SKILL_DIR="$WORKSPACE_DIR/skills/memory-lesson-manager"
MEMORY_DIR="$WORKSPACE_DIR/memory"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# 统计
TOTAL=0
PASSED=0
FAILED=0

check() {
    local desc="$1"
    local cmd="$2"
    ((TOTAL++))
    if eval "$cmd" >/dev/null 2>&1; then
        ((PASSED++))
        log_pass "$desc"
        return 0
    else
        ((FAILED++))
        log_fail "$desc"
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "记忆系统 V2.0 测试"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 检查目录结构
log_info "检查目录结构..."

check "HOT 目录存在" "[ -d \"$MEMORY_DIR/lessons/HOT\" ]"
check "WARM/errors 目录存在" "[ -d \"$MEMORY_DIR/lessons/WARM/errors\" ]"
check "WARM/corrections 目录存在" "[ -d \"$MEMORY_DIR/lessons/WARM/corrections\" ]"
check "WARM/best-practices 目录存在" "[ -d \"$MEMORY_DIR/lessons/WARM/best-practices\" ]"
check "WARM/feature-requests 目录存在" "[ -d \"$MEMORY_DIR/lessons/WARM/feature-requests\" ]"
check "WARM/decisions 目录存在" "[ -d \"$MEMORY_DIR/lessons/WARM/decisions\" ]"
check "WARM/projects 目录存在" "[ -d \"$MEMORY_DIR/lessons/WARM/projects\" ]"
check "WARM/people 目录存在" "[ -d \"$MEMORY_DIR/lessons/WARM/people\" ]"
check "COLD/archive 目录存在" "[ -d \"$MEMORY_DIR/lessons/COLD/archive\" ]"

echo ""

# 2. 检查模板文件
log_info "检查模板文件..."

TEMPLATES=(
    "diary-template.md"
    "lesson-error-template.md"
    "lesson-correction-template.md"
    "lesson-feature-template.md"
    "lesson-best-practice-template.md"
    "lesson-decision-template.md"
    "lesson-project-template.md"
    "lesson-people-template.md"
    "memory-hot-template.md"
    "session-state-template.md"
    "working-buffer-template.md"
)

for template in "${TEMPLATES[@]}"; do
    if [[ "$template" == "session-state"* ]] || [[ "$template" == "working-buffer"* ]]; then
        check "$template 存在" "[ -f \"$WORKSPACE_DIR/state/$template\" ]"
    else
        check "$template 存在" "[ -f \"$MEMORY_DIR/templates/$template\" ]"
    fi
done

echo ""

# 3. 检查脚本文件
log_info "检查脚本文件..."

SCRIPTS=(
    "init-memory-system.sh"
    "validate-diary.sh"
    "extract-skill.sh"
    "promote-lesson.sh"
    "archive-cold.sh"
)

for script in "${SCRIPTS[@]}"; do
    SCRIPT_PATH="$SKILL_DIR/scripts/$script"
    check "$script 存在" "[ -f \"$SCRIPT_PATH\" ]"
    check "$script 有执行权限" "[ -x \"$SCRIPT_PATH\" ]"
done

echo ""

# 4. 检查索引文件
log_info "检查索引文件..."

check "lessons/README.md 存在" "[ -f \"$MEMORY_DIR/lessons/README.md\" ]"
check "lessons/INDEX.md 存在" "[ -f \"$MEMORY_DIR/lessons/INDEX.md\" ]"

echo ""

# 5. 检查 SKILL.md
log_info "检查 SKILL.md..."

check "SKILL.md 存在" "[ -f \"$SKILL_DIR/SKILL.md\" ]"
check "版本号正确 (2.0.0)" "grep -q \"version: 2.0.0\" \"$SKILL_DIR/SKILL.md\""
check "引用详细文档" "grep -q \"references/usage-guide.md\" \"$SKILL_DIR/SKILL.md\""

echo ""

# 6. 日期兼容性测试
log_info "测试日期处理兼容性..."

# 日期兼容性测试
if [[ "$OSTYPE" == "darwin"* ]]; then
    if date -v-1d +%Y-%m-%d >/dev/null 2>&1; then
        log_pass "macOS 日期语法支持"
        ((TOTAL++))
        ((PASSED++))
    else
        log_fail "macOS 日期语法不支持"
        ((TOTAL++))
        ((FAILED++))
    fi
else
    if date -d "1 days ago" +%Y-%m-%d >/dev/null 2>&1; then
        log_pass "Linux 日期语法支持"
        ((TOTAL++))
        ((PASSED++))
    else
        log_info "Linux 日期语法不支持（正常，当前系统是 macOS）"
    fi
fi

echo ""

# 总结
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "测试结果："
echo "  总计：$TOTAL"
echo "  通过：$PASSED"
echo "  失败：$FAILED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$FAILED" -eq 0 ]; then
    log_info "✅ 所有测试通过！"
    exit 0
else
    log_warn "❌ 有 $FAILED 个测试失败，请检查上述输出"
    exit 1
fi
