#!/usr/bin/env bash
# openclaw-version-bug-hunter - 查询 OpenClaw 特定版本的 GitHub bug 报告
# Author: Initiated by Neo Shi and executed by 银月
# License: MIT

set -euo pipefail

REPO="openclaw/openclaw"
VERSION=""

# 颜色定义 (printf-compatible)
RED=$'\033[0;31m'
ORANGE=$'\033[0;33m'
YELLOW=$'\033[1;33m'
GREEN=$'\033[0;32m'
CYAN=$'\033[0;36m'
NC=$'\033[0m'

usage() {
    echo "用法：bug-hunt.sh <版本号>"
    echo ""
    echo "查询 OpenClaw 特定版本的 GitHub bug 报告，帮助升级前避坑。"
    echo ""
    echo "示例:"
    echo "  bug-hunt.sh 2026.4.9"
    echo "  bug-hunt.sh 2026.4.8"
    exit 1
}

[ $# -eq 0 ] && usage
VERSION="$1"

echo "🔍 正在搜索 OpenClaw v${VERSION} 的 bug 报告..."
echo ""

# 一次性获取所有 open issues（含 body）
ALL_ISSUES_JSON=$(gh issue list --repo "$REPO" --state open --search "$VERSION" --limit 100 \
    --json number,title,body,labels 2>/dev/null || echo "[]")

TOTAL=$(echo "$ALL_ISSUES_JSON" | jq 'length')
if [ "$TOTAL" -eq 0 ]; then
    echo "  未找到相关 issue"
    exit 0
fi

# ============================================================
# 一次性 jq 处理：质量评估 + 去重 + 分类
# ============================================================
EVALUATED=$(echo "$ALL_ISSUES_JSON" | jq '
def title_words:
    ascii_downcase
    | gsub("[^a-z0-9 ]"; " ")
    | split(" ")
    | map(select(length > 2));

def similarity(a; b):
    (a | title_words) as $aw |
    (b | title_words) as $bw |
    if ($aw | length) == 0 or ($bw | length) == 0 then 0
    else
        ([$aw[] | select(. as $w | $bw | index($w) != null)] | length) as $overlap |
        ($overlap * 2) / (($aw | length) + ($bw | length))
    end;

def quality_score:
    if . == null or . == "" then "needs-info"
    elif (length < 50) then "vague"
    else
        (if test("(?i)(step|reproduce|repro|how to|to reproduce)") then 2 else 0 end) as $s1 |
        (if test("(?i)(error|exception|stack trace|panic|traceback|segfault|TypeError|ReferenceError)") then 2 else 0 end) as $s2 |
        (if test("(?i)(environment|version|os |platform|node|macos|linux|windows|docker|browser)") then 1 else 0 end) as $s3 |
        (if test("\\.(ts|js|py|rs):|line \\d+|at \\w+\\(|file:") then 2 else 0 end) as $s4 |
        (if test("(?i)(screenshot|log|attached|image|\\.png|\\.jpg|\\.gif|video)") then 1 else 0 end) as $s5 |
        ($s1 + $s2 + $s3 + $s4 + $s5) as $total |
        if $total >= 4 then "actionable"
        elif $total >= 2 then "partial"
        else "needs-info"
        end
    end;

def label_category:
    [.labels[].name] as $ls |
    if ($ls | index("Critical")) then "critical"
    elif ($ls | index("regression")) then "regression"
    else "general"
    end;

. as $all |
reduce range(length) as $i (
    [];
    . as $results |
    $all[$i] as $issue |
    (reduce range($i) as $j (
        null;
        if . != null then .
        else
            (similarity($issue.title; $all[$j].title)) as $sim |
            if $sim > 0.65 and ($issue.title | length) > 15 then
                ($all[$j].number | tostring)
            else . end
        end
    )) as $dup |
    $results + [{
        number: $issue.number,
        title: $issue.title,
        category: ($issue | label_category),
        quality: (($issue.body // "") | quality_score),
        dup_of: ($dup // "")
    }]
)
')

# ============================================================
# 输出分类结果
# ============================================================

emit_section() {
    local category="$1" color="$2"
    local items
    items=$(echo "$EVALUATED" | jq -r --arg cat "$category" '
        [.[] | select(.category == $cat)] |
        map(
            .dup_of as $d |
            .quality as $q |
            (if $d != "" then "🔁 dup of #\($d)"
             elif $q == "actionable" then "✅ actionable"
             elif $q == "partial" then "⚡ partial"
             elif $q == "vague" then "⚠️ vague"
             else "❓ needs info"
             end) as $marker |
            "- #\(.number): \(.title) [\($marker)]"
        ) | .[]
    ' 2>/dev/null)

    local title
    case "$category" in
        critical) title="### 🔴 Critical / 严重问题" ;;
        regression) title="### 🟠 Regression / 回归问题" ;;
        general) title="### 🟡 General Bugs / 一般问题" ;;
    esac
    printf '%b%s%b\n\n' "$color" "$title" "$NC"

    if [ -n "$items" ]; then
        echo "$items"
    else
        echo "  无"
    fi
    echo ""
}

emit_section "critical" "$RED"
emit_section "regression" "$ORANGE"
emit_section "general" "$YELLOW"

# ============================================================
# 质量统计
# ============================================================

printf '%b%s%b\n' "$CYAN" "### 📋 质量评估" "$NC"

echo "$EVALUATED" | jq -r '
    sort_by(.quality) |
    group_by(.quality) |
    map({key: .[0].quality, value: length}) |
    from_entries |
    . as $q |
    [
        "- 总 issue 数: \($q | to_entries | map(.value) | add // 0)",
        "- ✅ actionable: \(.actionable // 0)",
        "- ⚡ partial: \(.partial // 0)",
        "- ❓ needs info: \(.["needs-info"] // 0)",
        "- ⚠️ vague: \(.vague // 0)"
    ] | .[]
' 2>/dev/null

# 重复数单独算
dup_count=$(echo "$EVALUATED" | jq '[.[] | select(.dup_of != "")] | length' 2>/dev/null || echo "0")
echo "- 🔁 duplicate: $dup_count"
echo ""

# 统计各分类数量
critical_count=$(echo "$EVALUATED" | jq '[.[] | select(.category == "critical" and .dup_of == "")] | length')
regression_count=$(echo "$EVALUATED" | jq '[.[] | select(.category == "regression" and .dup_of == "")] | length')
actionable_count=$(echo "$EVALUATED" | jq '[.[] | select(.quality == "actionable" and .dup_of == "")] | length')

# 修复状态
printf '%b%s%b\n' "$GREEN" "### 📊 统计信息" "$NC"
total_closed=$(gh issue list --repo "$REPO" --state closed --search "$VERSION" --limit 100 2>/dev/null | wc -l | tr -d ' ' || echo "0")
echo "- 未解决 issues: $TOTAL"
echo "- 已解决 issues: $total_closed"
echo ""

printf '%b%s%b\n' "$GREEN" "### ✅ 修复状态" "$NC"
pr_count=$(gh pr list --repo "$REPO" --state merged --search "$VERSION" --limit 20 2>/dev/null | wc -l | tr -d ' ' || echo "0")
if [ "$pr_count" -gt 0 ]; then
    echo "已合并的修复 PR: $pr_count"
    gh pr list --repo "$REPO" --state merged --search "$VERSION" --limit 10 \
        --json number,title 2>/dev/null | jq -r '.[] | "  - #\(.number): \(.title)"' 2>/dev/null
else
    echo "  暂无已合并的修复 PR"
fi
echo ""

# Agent 评估提示
echo "---"
echo "💡 升级评估：请结合你的实际配置（渠道/插件/运行时/Node版本/部署方式）"
echo "   关注与你使用场景相关的 actionable issue，忽略无关组件的问题。"
echo ""
echo "搜索完成时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "数据源：https://github.com/$REPO/issues"
