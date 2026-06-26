#!/usr/bin/env bash
# pipeline_gate.sh -- PPT Pro Skill 管道门禁脚本
#
# 强制执行 Step4→Step5→Step6 的顺序依赖，阻止跳步生成。
# 参考: AgentGuard CI/CD Gate 模式（agentguard.tech）
#
# 用法：
#   bash pipeline_gate.sh check-planning  OUTPUT_DIR  SKILL_DIR
#   bash pipeline_gate.sh check-prompts   OUTPUT_DIR
#   bash pipeline_gate.sh check-slides    OUTPUT_DIR
#   bash pipeline_gate.sh full-check      OUTPUT_DIR  SKILL_DIR
#
# 退出码：
#   0  所有检查通过，可以继续下一步
#   1  检查失败，禁止继续（需修正后重试）

set -euo pipefail

GATE_NAME="PPT Pipeline Gate"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

pass() { echo -e "${GREEN}[GATE ✓]${NC} $1"; }
fail() { echo -e "${RED}[GATE ✗ BLOCKED]${NC} $1" >&2; }
warn() { echo -e "${YELLOW}[GATE ⚠]${NC} $1"; }
info() { echo -e "${BLUE}[GATE →]${NC} $1"; }

# ── check-planning: 验证 planning/ 目录通过 validator ─────────────────────
check_planning() {
    local OUTPUT_DIR="$1"
    local SKILL_DIR="${2:-}"
    local PLANNING_DIR="$OUTPUT_DIR/planning"

    info "检查 planning/ 目录..."

    # 1. planning/ 目录必须存在且含文件
    if [[ ! -d "$PLANNING_DIR" ]]; then
        fail "planning/ 目录不存在: $PLANNING_DIR"
        fail "请先完成 Step 4：为每页写入 planning{n}.json"
        exit 1
    fi

    local count
    count=$(find "$PLANNING_DIR" -name "planning*.json" 2>/dev/null | wc -l)
    if [[ "$count" -eq 0 ]]; then
        fail "planning/ 目录中没有 planning*.json 文件"
        fail "请先完成 Step 4：为每页写入 planning{n}.json"
        exit 1
    fi

    pass "找到 $count 个策划稿文件"

    # 2. 运行 planning_validator
    if [[ -n "$SKILL_DIR" ]]; then
        local VALIDATOR="$SKILL_DIR/scripts/planning_validator.py"
        local REFS="$SKILL_DIR/references"

        if [[ ! -f "$VALIDATOR" ]]; then
            warn "找不到 validator: $VALIDATOR，跳过脚本验证"
            return 0
        fi

        info "运行 planning_validator.py..."
        if ! python3 "$VALIDATOR" "$PLANNING_DIR" --refs "$REFS"; then
            fail "planning_validator.py 验证失败（exit 1）"
            fail "禁止继续到 Step 5（prompt_assembler / HTML 生成）"
            fail "请按照上方 ERROR 修正所有 planning JSON，再重试"
            exit 1
        fi

        pass "planning_validator.py 验证通过"
    else
        warn "未提供 SKILL_DIR，跳过 planning_validator 脚本验证"
    fi
}

# ── check-prompts: 验证 prompts-ready/ 文件与 planning 数量一致 ─────────────
check_prompts() {
    local OUTPUT_DIR="$1"
    local PLANNING_DIR="$OUTPUT_DIR/planning"
    local PROMPTS_DIR="$OUTPUT_DIR/prompts-ready"

    info "检查 prompts-ready/ 目录..."

    # 1. prompts-ready/ 必须存在
    if [[ ! -d "$PROMPTS_DIR" ]]; then
        fail "prompts-ready/ 目录不存在: $PROMPTS_DIR"
        fail "请先运行 prompt_assembler.py 生成所有 prompt-ready-{n}.txt"
        exit 1
    fi

    # 2. planning 文件数 == prompt-ready 文件数
    local planning_count
    planning_count=$(find "$PLANNING_DIR" -name "planning*.json" 2>/dev/null | wc -l)

    local prompt_count
    prompt_count=$(find "$PROMPTS_DIR" -name "prompt-ready-*.txt" 2>/dev/null | wc -l)

    if [[ "$prompt_count" -eq 0 ]]; then
        fail "prompts-ready/ 中没有 prompt-ready-*.txt 文件"
        fail "请运行: python3 SKILL_DIR/scripts/prompt_assembler.py OUTPUT_DIR/planning/ ..."
        exit 1
    fi

    if [[ "$planning_count" -ne "$prompt_count" ]]; then
        fail "planning 文件数（$planning_count）与 prompt-ready 文件数（$prompt_count）不一致"
        fail "请重新运行 prompt_assembler.py 确保所有页面都有对应的 prompt-ready 文件"
        exit 1
    fi

    pass "prompts-ready/ 有 $prompt_count 个文件，与 planning 数量一致"
}

# ── check-slides: 验证 slides/ 文件数量与 planning 一致且非空 ─────────────
check_slides() {
    local OUTPUT_DIR="$1"
    local PLANNING_DIR="$OUTPUT_DIR/planning"
    local SLIDES_DIR="$OUTPUT_DIR/slides"

    info "检查 slides/ 目录..."

    if [[ ! -d "$SLIDES_DIR" ]]; then
        fail "slides/ 目录不存在: $SLIDES_DIR"
        fail "请先完成 Step 5：为每页生成 slide-0{n}.html"
        exit 1
    fi

    local planning_count
    planning_count=$(find "$PLANNING_DIR" -name "planning*.json" 2>/dev/null | wc -l)

    local slide_count
    slide_count=$(find "$SLIDES_DIR" -name "slide-*.html" 2>/dev/null | wc -l)

    if [[ "$slide_count" -eq 0 ]]; then
        fail "slides/ 中没有 slide-*.html 文件"
        exit 1
    fi

    if [[ "$planning_count" -ne "$slide_count" ]]; then
        warn "slides 数（$slide_count）与 planning 数（$planning_count）不一致"
        warn "确保每页都有对应的 HTML，再继续 Step 6"
    else
        pass "slides/ 有 $slide_count 个 HTML 文件，与 planning 数量一致"
    fi

    # 检查每个 slide 是否包含必要的 data-pptx-role 属性
    local missing_roles=0
    for html in "$SLIDES_DIR"/slide-*.html; do
        if ! grep -q 'data-pptx-role' "$html" 2>/dev/null; then
            warn "$(basename $html) 缺少 data-pptx-role 属性（Pipeline B 可编辑 PPTX 需要此属性）"
            ((missing_roles++)) || true
        fi
    done

    if [[ "$missing_roles" -eq 0 ]]; then
        pass "所有 HTML 文件包含 data-pptx-role 属性"
    fi

    # 检查画布尺寸
    local wrong_size=0
    for html in "$SLIDES_DIR"/slide-*.html; do
        if ! grep -qE '1280|width.*1280' "$html" 2>/dev/null; then
            warn "$(basename $html) 可能缺少 1280px 画布宽度设置"
            ((wrong_size++)) || true
        fi
    done

    if [[ "$wrong_size" -eq 0 ]]; then
        pass "所有 HTML 画布宽度已设置"
    fi
}

# ── full-check: 依序执行所有检查 ────────────────────────────────────────────
full_check() {
    local OUTPUT_DIR="$1"
    local SKILL_DIR="${2:-}"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $GATE_NAME -- 全流程检查"
    echo "  OUTPUT_DIR: $OUTPUT_DIR"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    check_planning "$OUTPUT_DIR" "$SKILL_DIR"
    check_prompts  "$OUTPUT_DIR"
    check_slides   "$OUTPUT_DIR"

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  所有门禁检查通过 ✓  可以运行 Step 6 输出 PPTX${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# ── 主入口 ──────────────────────────────────────────────────────────────────
CMD="${1:-help}"
OUTPUT_DIR="${2:-}"
SKILL_DIR="${3:-}"

if [[ -z "$OUTPUT_DIR" && "$CMD" != "help" ]]; then
    echo "用法: $0 <command> <OUTPUT_DIR> [SKILL_DIR]" >&2
    exit 1
fi

case "$CMD" in
    check-planning)  check_planning "$OUTPUT_DIR" "$SKILL_DIR" ;;
    check-prompts)   check_prompts  "$OUTPUT_DIR" ;;
    check-slides)    check_slides   "$OUTPUT_DIR" ;;
    full-check)      full_check     "$OUTPUT_DIR" "$SKILL_DIR" ;;
    help|--help|-h)
        echo "PPT Pipeline Gate -- 门禁检查工具"
        echo ""
        echo "用法:"
        echo "  $0 check-planning  OUTPUT_DIR  SKILL_DIR   # Step4 门禁"
        echo "  $0 check-prompts   OUTPUT_DIR               # Step5a 门禁"
        echo "  $0 check-slides    OUTPUT_DIR               # Step5c 门禁"
        echo "  $0 full-check      OUTPUT_DIR  SKILL_DIR   # 全流程检查"
        ;;
    *)
        echo "未知命令: $CMD" >&2
        echo "运行 '$0 help' 查看用法" >&2
        exit 1
        ;;
esac
