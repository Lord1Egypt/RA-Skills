#!/usr/bin/env bash
# lz-skill-vetter-plus v2.1.0 — Bash 包装
# 优先调 Python audit.py；若无 Python3 + PyYAML 则回退到 grep 基础扫描

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/audit.py"

# ─────────── 参数解析 ───────────
FORMAT="text"
SEVERITY_FILTER=""
EXIT_CODE=0
QUIET=0
SKILL_PATH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)        FORMAT="$2"; shift 2 ;;
    --severity)      SEVERITY_FILTER="$2"; shift 2 ;;
    --exit-code)     EXIT_CODE=1; shift ;;
    --quiet)         QUIET=1; shift ;;
    -h|--help)
      echo "skill-vetter v2.0 scan.sh — Bash 包装"
      echo ""
      echo "用法: $0 <skill-path> [--format text|json] [--severity <level>] [--exit-code] [--quiet]"
      echo ""
      echo "参数透传给 audit.py；优先用 Python，回退到 grep。"
      exit 0
      ;;
    -*)
      echo "未知选项: $1" >&2
      exit 2
      ;;
    *)
      SKILL_PATH="$1"; shift ;;
  esac
done

if [[ -z "$SKILL_PATH" ]]; then
  echo "用法: $0 <skill-path> [--format text|json] [--severity <level>] [--exit-code] [--quiet]" >&2
  exit 2
fi

if [[ ! -d "$SKILL_PATH" ]]; then
  echo "❌ 路径不存在或不是目录: $SKILL_PATH" >&2
  exit 2
fi

# ─────────── 优先 Python ───────────
ARGS=("$SKILL_PATH" "--format" "$FORMAT")
[[ -n "$SEVERITY_FILTER" ]] && ARGS+=("--severity" "$SEVERITY_FILTER")
[[ $EXIT_CODE -eq 1 ]] && ARGS+=("--exit-code")
[[ $QUIET -eq 1 ]] && ARGS+=("--quiet")

if command -v python3 >/dev/null 2>&1; then
  if python3 -c "import yaml" 2>/dev/null; then
    exec python3 "$PYTHON_SCRIPT" "${ARGS[@]}"
  fi
fi

# ─────────── Fallback：grep 基础扫描 ───────────
echo "⚠️  Python3 + PyYAML 不可用，回退到 grep 基础扫描（仅红线 6 类）" >&2

findings=0
scan() {
  local label="$1" pattern="$2"
  local hits
  hits=$(grep -rnE "$pattern" "$SKILL_PATH" --include="*.sh" --include="*.py" --include="*.js" --include="*.ts" --include="*.md" 2>/dev/null || true)
  if [[ -n "$hits" ]]; then
    echo ""
    echo "🔴 [$label]"
    echo "$hits" | head -10
    findings=$((findings + $(echo "$hits" | wc -l)))
  fi
}

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  SKILL VETTING REPORT (fallback mode)"
echo "═══════════════════════════════════════════════════════"
echo "Skill: $(basename "$SKILL_PATH")"
echo "Mode:  grep fallback (no PyYAML)"
echo "═══════════════════════════════════════════════════════"

# 红线 6 类（与 v1.0 一致）# safe-pattern: rule-description: 这些是模式定义本身，仅用于 fallback grep
scan "eval/exec 调用"        '\beval\s*\(|exec(?:Sync)?\s*\('  # safe-pattern: rule-description
scan "硬编码凭据"             '(api[_-]?key|secret|password|token)\s*[:=]\s*["\x27][^"\x27\s]{8,}'  # safe-pattern: rule-description
scan "外发 curl/wget"         '\b(curl|wget)\s+'  # safe-pattern: rule-description
scan "base64 解码"            '\bbase64\s*(-d|--decode|decode)\b'  # safe-pattern: rule-description
scan "rm -rf / sudo"          '\brm\s+-[rRf]+|sudo\s'  # safe-pattern: rule-description
scan "硬编码 IP"              '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'  # safe-pattern: rule-description

echo ""
echo "═══════════════════════════════════════════════════════"
echo "Findings (grep): $findings"
echo "═══════════════════════════════════════════════════════"

[[ $EXIT_CODE -eq 1 && $findings -gt 0 ]] && exit 2 || exit 0