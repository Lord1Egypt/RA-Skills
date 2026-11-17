#!/usr/bin/env bash
# strip_scan.sh — Step 3: 11 条剔除清单扫描（非破坏性，只报告）
# Usage: ./strip_scan.sh <fork-path> [--strict]
#
# Exit codes:
#   0  无字面命中 / 或有命中但默认模式（命中需用户拍板，不算失败）
#   1  参数错误
#   2  fork-path 不存在
#   3  --strict 模式下有字面命中（CI / 链式调用强约束时用）
set -euo pipefail

FORK="${1:-}"
STRICT=0
shift || true
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
  esac
done

if [[ -z "$FORK" ]]; then
  cat <<EOF >&2
Usage: $0 <fork-path> [--strict]
  --strict  字面命中时以 exit 3 退出（默认 exit 0，命中等用户拍板）
EOF
  exit 1
fi
[[ -d "$FORK" ]] || { echo "❌ fork-path not a directory: $FORK" >&2; exit 2; }

cd "$FORK"

echo "🔍 Strip Scan Report: $FORK"
echo "============================================"
echo ""

# ─── 文件层扫描 ─────────────────────────────────
echo "## ① 文件层（必删项当前状态）"
echo ""

check_file() {
  local pattern="$1"
  local desc="$2"
  local matches
  matches=$(find . -path ./.git -prune -o \( -name "$pattern" -print \) 2>/dev/null | grep -v "^./.git" || true)
  if [[ -n "$matches" ]]; then
    echo "❌ $desc 残留："
    echo "$matches" | sed 's/^/     /'
  else
    echo "✅ $desc 已清"
  fi
}

check_file "sign.key" "sign.key（内部签名）"
check_file ".install-source.json" ".install-source.json（内部安装来源）"
check_file "skill_meta.json" "skill_meta.json（agent 产物）"
check_file "*.json.md" "*.json.md（agent 产物）"
check_file "*.pyc" "*.pyc（Python 字节码）"
check_file "__pycache__" "__pycache__/（Python 缓存）"
check_file ".skill-data" ".skill-data/（运行时缓存）"

if [[ -f "$FORK/USAGE.md" ]] && [[ -f "$FORK/SKILL.md" ]]; then
  echo "⚠️  USAGE.md 与 SKILL.md 并存（请检查是否重复，重复建议删 USAGE.md）"
fi

# Changelog 惯例检查：版本历史应放独立 CHANGELOG.md，不放 SKILL.md
# （SKILL.md 是 agent 每次触发都读的运行时文档，历史记录浪费上下文；开源惯例也是独立文件）
if [[ -f "$FORK/SKILL.md" ]]; then
  _CL_HDR="$(grep -inE '^#{2,3} *(changelog|版本历史|版本记录|更新日志|变更记录|version history)' "$FORK/SKILL.md" 2>/dev/null | head -3 || true)"
  _CL_VER="$(grep -cE '^#{2,4} *v?[0-9]+\.[0-9]+\.[0-9]+' "$FORK/SKILL.md" 2>/dev/null || true)"
  _CL_VER="${_CL_VER:-0}"
  if [[ -n "$_CL_HDR" && "$_CL_VER" -ge 2 ]]; then
    echo "⚠️  SKILL.md 内嵌 changelog（$_CL_VER 条版本记录），建议拆到独立 CHANGELOG.md："
    echo "$_CL_HDR" | sed 's/^/     L/'
    echo "     SKILL.md/README 留一行指针: See [CHANGELOG.md](./CHANGELOG.md)"
  else
    echo "✅ SKILL.md 无内嵌 changelog（惯例：独立 CHANGELOG.md）"
  fi
fi

# ─── 字面层扫描 ─────────────────────────────────
echo ""
echo "## ② 字面层（内网关键词 grep）"
echo ""

# 主关键词清单（优先级：OSG_STRIP_KEYWORDS 环境变量 > 外置文件 > 默认内置表）
# 外置文件位置（任选其一，先到先用）：
#   $OSG_STRIP_KEYWORDS_FILE / ./strip_keywords.txt / ~/.config/opensource-skill-to-github/strip_keywords.txt
#   文件格式：每行一个关键词，# 开头为注释，空行忽略。
_KW_FILE=""
for f in "${OSG_STRIP_KEYWORDS_FILE:-}" \
         "./strip_keywords.txt" \
         "$HOME/.config/opensource-skill-to-github/strip_keywords.txt"; do
  [[ -n "$f" && -f "$f" ]] && { _KW_FILE="$f"; break; }
done

if [[ -n "${OSG_STRIP_KEYWORDS:-}" ]]; then
  IFS=',' read -ra KEYWORDS <<< "$OSG_STRIP_KEYWORDS"
  echo "ℹ️  关键词来源: OSG_STRIP_KEYWORDS 环境变量"
elif [[ -n "$_KW_FILE" ]]; then
  # macOS 默认 bash 3.2 没有 mapfile，用 while read 兼容
  KEYWORDS=()
  while IFS= read -r _kw; do KEYWORDS+=("$_kw"); done \
    < <(grep -vE '^\s*(#|$)' "$_KW_FILE" | sed 's/[[:space:]]*$//')
  echo "ℹ️  关键词来源: $_KW_FILE (${#KEYWORDS[@]} 词)"
else
  echo "ℹ️  关键词来源: 内置通用默认表"
  echo "   （公司专有词请用 setup_profile.sh 配置，或 OSG_STRIP_KEYWORDS / strip_keywords.txt）"
  # 内置表只保留【跨公司通用】的敏感/内网痕迹词。
  # 公司专有词（内网域名 / 平台代号 / 组织名等）不硬编码——由用户配置。
  KEYWORDS=(
    # 凭证 / 密钥痕迹
    "sso_token"
    "access_token"
    "id_rsa"
    "BEGIN RSA PRIVATE KEY"
    "BEGIN OPENSSH PRIVATE KEY"
    "AWS_SECRET"
    "PRIVATE KEY"
    # 本机 / 容器绝对路径痕迹
    "/home/"
    "/Users/"
    "/root/"
    # 常见内网 host 形态（提示核查，不代表一定要删）
    ".internal"
    ".corp"
    ".lan"
    "localhost:"
    "127.0.0.1"
    "10.0."
    "192.168."
    # 常见内网协作/凭证文件名
    ".netrc"
    ".npmrc"
  )
fi

# 白名单（允许命中），用户可通过 OSG_STRIP_WHITELIST 追加自己的名字/handle/邮箱
DEFAULT_WHITELIST='example\.com|<your-name>|<your-github-handle>'
EXTRA_WHITELIST="${OSG_STRIP_WHITELIST:-}"
if [[ -n "$EXTRA_WHITELIST" ]]; then
  WHITELIST_REGEX="${DEFAULT_WHITELIST}|${EXTRA_WHITELIST}"
else
  WHITELIST_REGEX="$DEFAULT_WHITELIST"
fi

total_hits=0

# 排除目录：默认 + 从 .gitignore 派生顶层目录条目
EXCLUDE_DIRS=(.git __pycache__ node_modules)
if [[ -f .gitignore ]]; then
  while IFS= read -r line; do
    [[ -z "$line" || "$line" =~ ^# ]] && continue
    case "$line" in
      */)  d="${line%/}" ;;
      *)   continue ;;
    esac
    [[ "$d" == *"*"* || "$d" == /* ]] && continue
    EXCLUDE_DIRS+=("$d")
  done < .gitignore
fi
# 去重并构造 grep --exclude-dir 参数。macOS 默认 bash 3.2 没有 mapfile。
DEDUPED_EXCLUDE_DIRS=()
while IFS= read -r d; do
  DEDUPED_EXCLUDE_DIRS+=("$d")
done < <(printf '%s\n' "${EXCLUDE_DIRS[@]}" | awk '!seen[$0]++')
EXCLUDE_DIRS=("${DEDUPED_EXCLUDE_DIRS[@]}")
EXCLUDE_ARGS=()
for d in "${EXCLUDE_DIRS[@]}"; do
  EXCLUDE_ARGS+=("--exclude-dir=$d")
done

for kw in "${KEYWORDS[@]}"; do
  hits=$(grep -rEn "$kw" . \
    "${EXCLUDE_ARGS[@]}" \
    --exclude="strip_scan.sh" \
    2>/dev/null | grep -Ev "$WHITELIST_REGEX" || true)
  if [[ -n "$hits" ]]; then
    count=$(echo "$hits" | wc -l)
    total_hits=$((total_hits + count))
    echo "❌ '$kw' 命中 $count 处："
    echo "$hits" | head -10 | sed 's/^/     /'
    if [[ $count -gt 10 ]]; then
      echo "     ... ($((count - 10)) more)"
    fi
    echo ""
  fi
done

echo "============================================"

# ─── ③ token 字面扫描 ─────────────────────────
echo ""
echo "## ③ Token 字面扫描（防止真实 token 残留）"
echo ""
token_hits=$(grep -rEn \
  '(ghp_|gho_|ghu_|ghs_|ghr_|clh_|npm_|sk-[A-Za-z0-9]|xoxb-|xoxp-|AKIA)[A-Za-z0-9_-]{20,}' \
  . "${EXCLUDE_ARGS[@]}" \
  --exclude="strip_scan.sh" 2>/dev/null || true)
if [[ -n "$token_hits" ]]; then
  hcount=$(echo "$token_hits" | wc -l)
  echo "❌ 疑似 token 字面命中 $hcount 处："
  # 显示行号但脱敏 token 本身
  echo "$token_hits" | sed -E 's/(ghp_|gho_|ghu_|ghs_|ghr_|clh_|npm_|sk-|xoxb-|xoxp-|AKIA)[A-Za-z0-9_-]{20,}/\1***REDACTED***/g' | sed 's/^/     /'
  total_hits=$((total_hits + hcount))
else
  echo "✅ 无 token 字面命中"
fi

echo ""
echo "============================================"
if [[ $total_hits -eq 0 ]]; then
  echo "✅ 字面层零命中，可继续 Step 4"
  exit 0
else
  echo "⚠️  字面层共 $total_hits 处命中，需逐处处理："
  echo "   - 由用户拍板每处「保留 / 删除 / 改写」（AI 不自决）"
  echo "   - 字面替换映射见 references/strip_checklist.md"
  echo "   - 复杂场景见 openclaw-skill-opensource-fork-strip-internal-and-token-hygiene skill"
  if [[ $STRICT -eq 1 ]]; then
    echo ""
    echo "🛑 --strict 模式：以 exit 3 终止"
    exit 3
  fi
  exit 0  # 默认不当失败，命中报告是给用户/agent 读的，不是 CI 信号
fi
