#!/bin/bash
# verify_workspace.sh - 验证 Agent workspace 文件完整性 + 内容质量
# 用法:bash verify_workspace.sh <agentId> [--type human|functional]
#
# Phase 4 收尾时调用,确认 workspace 不只是空骨架。
# 检查必须文件是否存在、是否有实质内容、是否通过内容特征验证。

set -e

AGENT_ID="${1}"
if [ -z "$AGENT_ID" ]; then
  echo "❌ 用法:bash verify_workspace.sh <agentId> [--type human|functional]"
  exit 1
fi

AGENT_TYPE="human"
shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      AGENT_TYPE="$2"
      shift 2
      ;;
    *)
      echo "❌ 未知参数:$1"
      exit 1
      ;;
  esac
done

WORKSPACE="$HOME/.openclaw/agency-agents/$AGENT_ID"

if [ ! -d "$WORKSPACE" ]; then
  echo "❌ workspace 不存在:$WORKSPACE"
  exit 1
fi

echo "=== 验证 workspace: $WORKSPACE ==="
echo "=== Agent 类型: $AGENT_TYPE ==="
echo ""

PASS=0
FAIL=0

# ── 基础检查:文件存在 + 有效行数 ──────────────────────────────

check_file() {
  local filepath="$1"
  local label="$2"
  local min_lines="${3:-3}"

  if [ ! -f "$filepath" ]; then
    echo "  ❌ 缺失:$label"
    FAIL=$((FAIL + 1))
    return 1
  fi

  local content_lines
  content_lines=$(grep -cv '^\s*$\|^\s*#\|^\s*>\|^---' "$filepath" 2>/dev/null || true)

  if [ "$content_lines" -lt "$min_lines" ]; then
    echo "  ⚠️  疑似空骨架(有效行 ${content_lines} < ${min_lines}):$label"
    FAIL=$((FAIL + 1))
    return 1
  else
    echo "  ✅ $label(有效行 ${content_lines})"
    PASS=$((PASS + 1))
    return 0
  fi
}

# ── 内容特征检查 ───────────────────────────────────────────────

# 检查文件中是否存在未填充的占位符
check_no_placeholder() {
  local filepath="$1"
  local label="$2"
  local skip_for_human="$3"  # 设为 true 时，人伴型跳过此文件的占位检查

  # 人伴型 Agent：某些文件在 BOOTSTRAP 之前有合法占位
  if [ "$AGENT_TYPE" = "human" ] && [ "$skip_for_human" = "true" ]; then
    # BOOTSTRAP.md 存在时这些文件的占位是合法的
    if [ -f "$WORKSPACE/BOOTSTRAP.md" ]; then
      echo "  ⊘  跳过占位检查（BOOTSTRAP 前合法占位）:$label"
      return 0
    fi
  fi

  if grep -qE '\[FILL\]|\[FILL:|\[AUTO\]|\[TODO\]' "$filepath" 2>/dev/null; then
    echo "  ❌ 含未填充占位符 [FILL]/[AUTO]/[TODO]:$label"
    FAIL=$((FAIL + 1))
    return 1
  else
    echo "  ✅ 无未填充占位符:$label"
    PASS=$((PASS + 1))
    return 0
  fi
}

# 检查 SOUL.md:第一行是否包含 Agent 名字(从 IDENTITY.md 提取)
check_soul_name() {
  local soul_path="$WORKSPACE/SOUL.md"
  local identity_path="$WORKSPACE/IDENTITY.md"

  if [ ! -f "$soul_path" ] || [ ! -f "$identity_path" ]; then
    return 0  # 文件缺失已由 check_file 报告,这里跳过
  fi

  # 从 IDENTITY.md 提取名字(兼容 "- **Name:** 小审" 和 "**Name:** 小审" 两种格式)
  local agent_name
  agent_name=$(grep -m1 '\*\*Name:\*\*' "$identity_path" 2>/dev/null | sed 's/.*\*\*Name:\*\* *//' | tr -d '[]' | xargs)

  if [ -z "$agent_name" ] || [[ "$agent_name" == *"FILL"* ]]; then
    echo "  ⚠️  IDENTITY.md 名字未填写,跳过 SOUL.md 名字检查"
    return 0
  fi

  # 检查 SOUL.md 第一段(前5行)是否包含名字
  if head -5 "$soul_path" | grep -q "$agent_name"; then
    echo "  ✅ SOUL.md 包含 Agent 名字($agent_name)"
    PASS=$((PASS + 1))
  else
    echo "  ❌ SOUL.md 前5行未找到名字「$agent_name」(SOUL.md 第一句话必须有名字)"
    FAIL=$((FAIL + 1))
  fi
}

# 检查 SOUL.md:叙事质量基本检查(启发式,不阻断流程)
check_soul_structure() {
  local filepath="$WORKSPACE/SOUL.md"

  if [ ! -f "$filepath" ]; then
    return 0
  fi

  # 检查是否包含“厌恶/皱眉头/受不了/讨厌”类关键词（第四层）
  if grep -qE '厌恶|皱眉头|受不了|讨厌|不能容忍|最让我' "$filepath" 2>/dev/null; then
    echo "  ✅ SOUL.md 包含具体厌恶点"
    PASS=$((PASS + 1))
  else
    echo "  ❌ SOUL.md 缺少具体厌恶点（第四层缺失，按 file-formats.md 标准属于未写好）"
    FAIL=$((FAIL + 1))
  fi

  # 检查是否包含"规则句式"泄露
  if grep -qE '^我(会|将|要|不|不会)(做|执行|处理|完成|进行)' "$filepath" 2>/dev/null; then
    echo "  ⚠️  SOUL.md 可能包含规则句式(应移到 AGENTS.md)"
  fi
}

# 检查 AGENTS.md:是否包含边界/否定声明
check_agents_boundary() {
  local filepath="$WORKSPACE/AGENTS.md"

  if [ ! -f "$filepath" ]; then
    return 0
  fi

  if grep -qE '不做|不处理|边界|不会|禁止|超出范围' "$filepath" 2>/dev/null; then
    echo "  ✅ AGENTS.md 包含边界声明"
    PASS=$((PASS + 1))
  else
    echo "  ❌ AGENTS.md 缺少边界声明(必须有"不做/不处理/边界"等否定条款)"
    FAIL=$((FAIL + 1))
  fi
}

# 检查 MEMORY.md:是否有公司信息(不是空占位符)
check_memory_company() {
  local filepath="$WORKSPACE/MEMORY.md"

  if [ ! -f "$filepath" ]; then
    return 0
  fi

  # 人伴型 + BOOTSTRAP 存在：MEMORY.md 占位是合法的
  if [ "$AGENT_TYPE" = "human" ] && [ -f "$WORKSPACE/BOOTSTRAP.md" ]; then
    echo "  ⊘  跳过公司信息检查（BOOTSTRAP 前合法占位）"
    return 0
  fi

  local company_val
  company_val=$(grep -m1 '^- 公司:' "$filepath" 2>/dev/null | sed 's/^- 公司://' | xargs)

  # 判断:为空、含FILL占位符、含"填写/执行后"提示文本 → 失败
  if [ -z "$company_val" ] \
    || echo "$company_val" | grep -qE '\[FILL|FILL\]' \
    || echo "$company_val" | grep -qF '填写' \
    || echo "$company_val" | grep -qF '执行后'; then
    echo "  ❌ MEMORY.md \"公司:\"字段未填写(当前值:${company_val:-空})"
    FAIL=$((FAIL + 1))
  else
    echo "  ✅ MEMORY.md 公司信息已填写:$company_val"
    PASS=$((PASS + 1))
  fi
}

# ── 执行检查 ───────────────────────────────────────────────────

echo "[ 公共文件 - 存在性 + 行数 ]"
check_file "$WORKSPACE/IDENTITY.md"   "IDENTITY.md"  2
check_file "$WORKSPACE/SOUL.md"       "SOUL.md"       5
check_file "$WORKSPACE/AGENTS.md"     "AGENTS.md"     8
check_file "$WORKSPACE/TOOLS.md"      "TOOLS.md"      3
check_file "$WORKSPACE/MEMORY.md"     "MEMORY.md"     4
check_file "$WORKSPACE/HEARTBEAT.md"  "HEARTBEAT.md"  3

echo ""
echo "[ 内容特征检查 ]"
check_no_placeholder "$WORKSPACE/IDENTITY.md"  "IDENTITY.md"
check_no_placeholder "$WORKSPACE/SOUL.md"      "SOUL.md"          true
check_no_placeholder "$WORKSPACE/AGENTS.md"    "AGENTS.md"
check_no_placeholder "$WORKSPACE/TOOLS.md"     "TOOLS.md"
check_no_placeholder "$WORKSPACE/MEMORY.md"    "MEMORY.md"        true
check_soul_name
check_soul_structure
check_agents_boundary
check_memory_company

# ── 人伴型专属 ────────────────────────────────────────────────

if [ "$AGENT_TYPE" = "human" ]; then
  echo ""
  echo "[ 人伴型专属 ]"
  check_file "$WORKSPACE/USER.md" "USER.md" 3

  if [ -f "$WORKSPACE/BOOTSTRAP.md" ]; then
    # BOOTSTRAP.md 存在时检查是否仍是占位符
    if grep -q "此文件是占位符" "$WORKSPACE/BOOTSTRAP.md" 2>/dev/null; then
      echo "  ⚠️  BOOTSTRAP.md 仍是占位符,Phase 2 A-8 步骤尚未执行"
      FAIL=$((FAIL + 1))
    else
      echo "  i️  BOOTSTRAP.md 已生成(首次对话尚未完成,属正常)"
      PASS=$((PASS + 1))
    fi

    # 检查进度文件
    if [ -f "$WORKSPACE/memory/.bootstrap-progress.json" ]; then
      echo "  i️  断点进度文件存在:memory/.bootstrap-progress.json"
    fi
  else
    echo "  ✅ BOOTSTRAP.md 已删除(首次对话已完成)"
    PASS=$((PASS + 1))
  fi
fi

# ── 目录结构 ──────────────────────────────────────────────────

echo ""
echo "[ 目录结构 ]"
if [ -d "$WORKSPACE/memory" ]; then
  echo "  ✅ memory/ 目录存在"
  PASS=$((PASS + 1))
else
  echo "  ❌ memory/ 目录缺失"
  FAIL=$((FAIL + 1))
fi

# ── 汇总 ─────────────────────────────────────────────────────

echo ""
echo "=== 验证结果 ==="
echo "  通过:$PASS 失败/警告:$FAIL"
echo ""

if [ "$FAIL" -eq 0 ]; then
  echo "✅ workspace 完整,可以继续 Phase 4 重启验证。"
  exit 0
else
  echo "❌ 有 $FAIL 项未通过,请补充缺失内容后重新验证。"
  exit 1
fi
