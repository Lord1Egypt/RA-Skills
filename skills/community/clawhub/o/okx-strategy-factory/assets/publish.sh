#!/usr/bin/env bash
#
# publish.sh - 验证并发布一个新的 Skill 到 Skills 仓库
#
# 用法:
#   ./publish.sh <skill-name>                    # 验证 + git commit
#   ./publish.sh <skill-name> --push             # 验证 + git commit + push
#   ./publish.sh <skill-name> --dry-run          # 仅验证，不提交
#   ./publish.sh <skill-name> --copy-script <path>  # 复制策略脚本到 Skill 目录后发布
#
# 示例:
#   ./publish.sh grid-trading
#   ./publish.sh momentum-breakout --copy-script ~/scripts/momentum.py --push
#   ./publish.sh new-strategy --dry-run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# --- 颜色 ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- 参数解析 ---
SKILL_NAME=""
PUSH=false
DRY_RUN=false
COPY_SCRIPT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --push)       PUSH=true; shift ;;
        --dry-run)    DRY_RUN=true; shift ;;
        --copy-script) COPY_SCRIPT="$2"; shift 2 ;;
        -h|--help)
            echo "用法: $0 <skill-name> [--push] [--dry-run] [--copy-script <path>]"
            echo ""
            echo "选项:"
            echo "  --push              验证 + commit 后自动 push"
            echo "  --dry-run           仅验证格式，不执行 git 操作"
            echo "  --copy-script PATH  复制策略脚本到 Skill 目录"
            echo ""
            echo "示例:"
            echo "  $0 grid-trading"
            echo "  $0 momentum --copy-script ~/scripts/momentum.py --push"
            exit 0
            ;;
        *)
            if [[ -z "$SKILL_NAME" ]]; then
                SKILL_NAME="$1"
            else
                echo -e "${RED}错误: 未知参数 '$1'${NC}" >&2
                exit 1
            fi
            shift
            ;;
    esac
done

if [[ -z "$SKILL_NAME" ]]; then
    echo -e "${RED}错误: 请指定 skill 名称${NC}" >&2
    echo "用法: $0 <skill-name> [--push] [--dry-run] [--copy-script <path>]"
    exit 1
fi

SKILL_DIR="$REPO_ROOT/$SKILL_NAME"
SKILL_FILE="$SKILL_DIR/SKILL.md"

# --- 辅助函数 ---
pass() { echo -e "  ${GREEN}✓${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo -e "  ${YELLOW}!${NC} $1"; WARNINGS=$((WARNINGS + 1)); }
info() { echo -e "  ${BLUE}→${NC} $1"; }

ERRORS=0
WARNINGS=0

# --- Step 0: 复制脚本（如果指定） ---
if [[ -n "$COPY_SCRIPT" ]]; then
    echo -e "\n${BLUE}[0/4] 复制策略脚本${NC}"
    if [[ ! -f "$COPY_SCRIPT" ]]; then
        fail "脚本不存在: $COPY_SCRIPT"
        exit 1
    fi
    mkdir -p "$SKILL_DIR"
    cp "$COPY_SCRIPT" "$SKILL_DIR/"
    pass "已复制 $(basename "$COPY_SCRIPT") -> $SKILL_DIR/"
fi

# --- Step 1: 检查文件存在 ---
echo -e "\n${BLUE}[1/4] 检查文件结构${NC}"

if [[ ! -d "$SKILL_DIR" ]]; then
    fail "Skill 目录不存在: $SKILL_DIR"
    echo -e "\n${RED}发布失败: 请先创建 Skill 目录和 SKILL.md${NC}"
    exit 1
fi

if [[ ! -f "$SKILL_FILE" ]]; then
    fail "SKILL.md 不存在: $SKILL_FILE"
    echo -e "\n${RED}发布失败: 请先创建 SKILL.md${NC}"
    exit 1
fi

pass "SKILL.md 存在"

# 检查是否有额外的策略文件
EXTRA_FILES=$(find "$SKILL_DIR" -type f ! -name "SKILL.md" ! -name ".*" 2>/dev/null | head -5)
if [[ -n "$EXTRA_FILES" ]]; then
    info "包含额外文件:"
    echo "$EXTRA_FILES" | while read -r f; do
        info "  $(basename "$f")"
    done
fi

# --- Step 2: 验证 YAML frontmatter ---
echo -e "\n${BLUE}[2/4] 验证 YAML frontmatter${NC}"

# 检查是否以 --- 开头
if ! head -1 "$SKILL_FILE" | grep -q '^---$'; then
    fail "SKILL.md 必须以 '---' 开头（YAML frontmatter）"
else
    pass "YAML frontmatter 起始标记"
fi

# 提取 frontmatter（第一个 --- 到第二个 --- 之间）
FRONTMATTER=$(awk 'BEGIN{n=0} /^---$/{n++; if(n==2) exit; next} n==1{print}' "$SKILL_FILE")

# 检查必需字段
check_field() {
    local field="$1"
    local label="$2"
    if echo "$FRONTMATTER" | grep -q "^${field}:"; then
        local value
        value=$(echo "$FRONTMATTER" | grep "^${field}:" | head -1 | sed "s/^${field}:[[:space:]]*//")
        if [[ -z "$value" || "$value" == '""' || "$value" == "''" ]]; then
            fail "$label 为空"
        else
            pass "$label: $value"
        fi
    else
        fail "缺少必需字段: $field"
    fi
}

check_field "name" "名称"
check_field "description" "描述"
check_field "license" "许可证"

# 检查 metadata 子字段
if echo "$FRONTMATTER" | grep -q "^metadata:"; then
    pass "metadata 章节存在"
    if echo "$FRONTMATTER" | grep -q "author:"; then
        pass "metadata.author 存在"
    else
        fail "缺少 metadata.author"
    fi
    if echo "$FRONTMATTER" | grep -q "version:"; then
        VERSION=$(echo "$FRONTMATTER" | grep "version:" | sed 's/.*version:[[:space:]]*//' | tr -d '"' | tr -d "'" | xargs)
        if echo "$VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+'; then
            pass "version 格式正确: $VERSION"
        else
            warn "version 建议使用 semver 格式 (x.y.z)，当前: $VERSION"
        fi
    else
        fail "缺少 metadata.version"
    fi
else
    fail "缺少 metadata 章节"
fi

# 检查 description 长度（至少 50 字符，用于 AI agent 路由）
DESC_LEN=$(echo "$FRONTMATTER" | grep "^description:" | wc -c | tr -d ' ')
if [[ "$DESC_LEN" -lt 60 ]]; then
    warn "description 偏短（<60 字符），建议写详细以改善 AI agent 路由匹配"
fi

# 检查 pattern 字段
VALID_PATTERNS="tool-wrapper generator reviewer inversion pipeline"
PATTERN_VALUE=$(echo "$FRONTMATTER" | grep "pattern:" | sed 's/.*pattern:[[:space:]]*//' | tr -d '"' | tr -d "'" | xargs || true)
if [[ -n "$PATTERN_VALUE" ]]; then
    # 支持复合模式（逗号分隔）
    ALL_VALID=true
    IFS=',' read -ra PATTERNS <<< "$PATTERN_VALUE"
    for p in "${PATTERNS[@]}"; do
        p=$(echo "$p" | xargs)  # trim whitespace
        if echo "$VALID_PATTERNS" | grep -qw "$p"; then
            :
        else
            fail "无效的 pattern: '$p' (允许: $VALID_PATTERNS)"
            ALL_VALID=false
        fi
    done
    if [[ "$ALL_VALID" == true ]]; then
        pass "pattern: $PATTERN_VALUE"
        # 检查 pattern 特有的 metadata 字段
        for p in "${PATTERNS[@]}"; do
            p=$(echo "$p" | xargs)
            case "$p" in
                generator)
                    if ! echo "$FRONTMATTER" | grep -q "output-format:"; then
                        warn "generator 模式建议添加 metadata.output-format 字段"
                    fi
                    ;;
                reviewer)
                    if ! echo "$FRONTMATTER" | grep -q "severity-levels:"; then
                        warn "reviewer 模式建议添加 metadata.severity-levels 字段"
                    fi
                    ;;
                inversion)
                    if ! echo "$FRONTMATTER" | grep -q "interaction:"; then
                        warn "inversion 模式建议添加 metadata.interaction 字段"
                    fi
                    ;;
                pipeline)
                    if ! echo "$FRONTMATTER" | grep -q "steps:"; then
                        warn "pipeline 模式建议添加 metadata.steps 字段"
                    fi
                    ;;
            esac
        done
    fi
else
    warn "未指定 pattern 字段，建议使用: $VALID_PATTERNS"
fi

# --- Step 3: 验证内容结构 ---
echo -e "\n${BLUE}[3/4] 验证内容结构${NC}"

CONTENT=$(cat "$SKILL_FILE")

# 必需章节
check_section() {
    local heading="$1"
    local label="$2"
    local required="${3:-true}"
    if echo "$CONTENT" | grep -qiE "^##+ .*($heading)" 2>/dev/null; then
        pass "章节: $label"
    elif [[ "$required" == "true" ]]; then
        fail "缺少必需章节: $label (需要包含 '$heading' 的标题)"
    else
        warn "建议添加章节: $label"
    fi
}

# 通用必需章节
check_section "Architecture|架构" "Architecture（架构）"
check_section "Instruction|Algorithm|算法|Core|指令" "Instructions / Core Algorithm（指令/核心算法）"

# 按 pattern 检查特有章节
if [[ -n "$PATTERN_VALUE" ]]; then
    for p in "${PATTERNS[@]}"; do
        p=$(echo "$p" | xargs)
        case "$p" in
            tool-wrapper)
                check_section "Trigger|触发|Keyword" "Trigger Keywords（触发关键词）" "false"
                check_section "Context.Load|上下文加载" "Context Loading Rules（上下文加载规则）" "false"
                ;;
            generator)
                check_section "Template|模板|Variable" "Template / Variables（模板/变量）" "false"
                check_section "Style|风格|Output" "Style / Output Format（风格/输出格式）" "false"
                ;;
            reviewer)
                check_section "Checklist|清单|Severity" "Review Checklist / Severity（检查清单/严重程度）" "false"
                ;;
            inversion)
                check_section "Phase|阶段" "Phases（采访阶段）" "false"
                check_section "Synthesis|综合|Gate|门控" "Synthesis / Gates（综合/门控）" "false"
                ;;
            pipeline)
                check_section "Step|步骤" "Pipeline Steps（管道步骤）" "false"
                check_section "Gate|门控|Checkpoint" "Gates / Checkpoints（门控/检查点）" "false"
                check_section "Fail|Rollback|失败|回滚" "Failure Handling（失败处理）" "false"
                ;;
        esac
    done
fi

# 通用推荐章节
check_section "Parameter|参数|Tunable" "Parameters（参数）" "false"
check_section "Risk|风险|风控" "Risk Controls（风险控制）" "false"
check_section "Anti.Pattern|反模式" "Anti-Patterns（反模式）" "false"
check_section "State|状态" "State Schema（状态模式）" "false"
check_section "Execut|执行|Pipeline" "Execution Pipeline（执行流程）" "false"
check_section "Extend|扩展|Adapt" "Extension Points（扩展点）" "false"
check_section "PnL|收益" "PnL Tracking（收益追踪）" "false"

# 检查 pattern 对应的目录结构
if [[ -n "$PATTERN_VALUE" ]]; then
    for p in "${PATTERNS[@]}"; do
        p=$(echo "$p" | xargs)
        case "$p" in
            tool-wrapper)
                if [[ -d "$SKILL_DIR/references" ]] && [[ -n "$(ls -A "$SKILL_DIR/references/" 2>/dev/null)" ]]; then
                    pass "references/ 目录存在且非空（tool-wrapper 必需）"
                else
                    warn "tool-wrapper 模式建议创建 references/ 目录存放 API 规范"
                fi
                ;;
            generator)
                if [[ -d "$SKILL_DIR/assets" ]] && [[ -n "$(ls -A "$SKILL_DIR/assets/" 2>/dev/null)" ]]; then
                    pass "assets/ 目录存在且非空（generator 必需）"
                else
                    warn "generator 模式建议创建 assets/ 目录存放输出模板"
                fi
                ;;
            reviewer)
                if [[ -f "$SKILL_DIR/references/review-checklist.md" ]]; then
                    pass "references/review-checklist.md 存在（reviewer 必需）"
                else
                    warn "reviewer 模式建议创建 references/review-checklist.md"
                fi
                ;;
        esac
    done
fi

# 检查是否有参数表格
if echo "$CONTENT" | grep -q '|.*Parameter\|参数.*|.*Default\|默认.*|'; then
    pass "包含参数表格"
elif echo "$CONTENT" | grep -q '|.*|.*|.*|'; then
    pass "包含表格（请确保参数有 Default 列）"
else
    warn "未发现参数表格，建议使用 | Parameter | Default | Description | 格式"
fi

# 检查是否有代码块
CODE_BLOCKS=$(echo "$CONTENT" | grep -c '```' || true)
if [[ "$CODE_BLOCKS" -ge 4 ]]; then
    pass "包含 $((CODE_BLOCKS / 2)) 个代码块"
elif [[ "$CODE_BLOCKS" -ge 2 ]]; then
    warn "仅有 $((CODE_BLOCKS / 2)) 个代码块，策略类 Skill 建议包含更多代码示例"
else
    warn "几乎没有代码块，策略类 Skill 应包含算法实现和命令示例"
fi

# 文件大小检查
FILE_SIZE=$(wc -c < "$SKILL_FILE" | tr -d ' ')
if [[ "$FILE_SIZE" -lt 500 ]]; then
    warn "SKILL.md 过短（${FILE_SIZE} 字节），可能缺少关键内容"
elif [[ "$FILE_SIZE" -gt 100000 ]]; then
    warn "SKILL.md 过长（${FILE_SIZE} 字节），考虑拆分为主文件 + references/"
else
    pass "文件大小合理: ${FILE_SIZE} 字节"
fi

# --- 验证结果 ---
echo -e "\n${BLUE}━━━ 验证结果 ━━━${NC}"
echo -e "  错误: ${RED}${ERRORS}${NC}  警告: ${YELLOW}${WARNINGS}${NC}"

if [[ $ERRORS -gt 0 ]]; then
    echo -e "\n${RED}验证失败: 请修复以上 ${ERRORS} 个错误后重试${NC}"
    exit 1
fi

if [[ "$DRY_RUN" == true ]]; then
    echo -e "\n${GREEN}验证通过 (dry-run 模式，未执行 git 操作)${NC}"
    exit 0
fi

# --- Step 4: Git commit ---
echo -e "\n${BLUE}[4/4] Git 提交${NC}"

cd "$REPO_ROOT"

# 获取 skill name 和 version 用于 commit message
SKILL_NAME_FM=$(echo "$FRONTMATTER" | grep "^name:" | sed 's/^name:[[:space:]]*//')
SKILL_VERSION=$(echo "$FRONTMATTER" | grep "version:" | sed 's/.*version:[[:space:]]*"\?\([^"]*\)"\?/\1/' | tr -d '"')

# 检查是否有变更
if git diff --quiet "$SKILL_NAME/" 2>/dev/null && \
   git diff --cached --quiet "$SKILL_NAME/" 2>/dev/null && \
   [[ -z "$(git ls-files --others --exclude-standard "$SKILL_NAME/")" ]]; then
    echo -e "${YELLOW}没有检测到变更，跳过提交${NC}"
    exit 0
fi

# Stage skill 目录
git add "$SKILL_NAME/"
pass "已暂存 $SKILL_NAME/"

# 判断是新增还是更新
if git log --oneline -- "$SKILL_NAME/SKILL.md" 2>/dev/null | head -1 | grep -q .; then
    COMMIT_MSG="Update ${SKILL_NAME_FM} skill v${SKILL_VERSION}"
else
    COMMIT_MSG="Add ${SKILL_NAME_FM} skill v${SKILL_VERSION}"
fi

git commit -m "$(cat <<EOF
${COMMIT_MSG}
EOF
)"
pass "已提交: $COMMIT_MSG"

if [[ "$PUSH" == true ]]; then
    BRANCH=$(git branch --show-current)
    git push origin "$BRANCH"
    pass "已推送到 origin/$BRANCH"
fi

echo -e "\n${GREEN}发布完成: $SKILL_NAME/${NC}"
