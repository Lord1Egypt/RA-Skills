#!/usr/bin/env bash
# run_all.sh — 一键串联开源前 6 步（precheck → fork → strip_scan → license → scaffold → git_init）
# push / clawhub / skillhub.cn 因需 token + 人工确认，本脚本【不】自动执行，只打印下一步指引。
#
# Usage:
#   ./run_all.sh <source-skill-name-or-abs-path> [<new-slug>]
# 环境变量（可选）：
#   OSG_LICENSE           默认 MIT（MIT|Apache-2.0|GPL-3.0）
#   OSG_AUTHOR_NAME / OSG_GITHUB_HANDLE / OSG_AUTHOR_EMAIL  身份（缺则读 profile.env）
#   OPENSOURCE_OUT_DIR    副本输出目录（默认 ./opensourceskills）
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SOURCE="${1:-}"
NEW_SLUG="${2:-}"

if [[ -z "$SOURCE" ]]; then
  echo "Usage: $0 <source-skill-name-or-abs-path> [<new-slug>]" >&2
  exit 1
fi

. "$HERE/_lib_profile.sh" 2>/dev/null || true
type osg_resolve_identity >/dev/null 2>&1 && osg_resolve_identity || true

LICENSE_TYPE="${OSG_LICENSE:-MIT}"
AUTHOR="${OSG_AUTHOR_NAME:-}"
EMAIL="${OSG_AUTHOR_EMAIL:-}"

step() { echo ""; echo "━━━━━━━━━━ $* ━━━━━━━━━━"; }

# ---- Step 1: precheck ----
step "Step 1/6: precheck"
SLUG_FOR_CHECK="${NEW_SLUG:-$(basename "$SOURCE")}"
set +e
bash "$HERE/precheck.sh" "$SLUG_FOR_CHECK"
PRECHECK_RC=$?
set -e
# precheck 退出码语义：0=可用 / 2=CLI未装 / 3=slug已注册(需拍板) / 4=网络异常
case "$PRECHECK_RC" in
  0) echo "✅ slug 可用，继续。" ;;
  3)
    echo ""
    echo "⚠️  slug '$SLUG_FOR_CHECK' 已在 clawhub 注册（见上）。"
    echo "    这【不一定】是错误——若同 owner 只是更新版本，可继续；若他人占用需换 slug。"
    if [[ "${OSG_ASSUME_YES:-}" == "1" ]]; then
      echo "    OSG_ASSUME_YES=1，按「继续」处理。"
    else
      echo "❌ 需人工拍板后再跑：确认可继续则设 OSG_ASSUME_YES=1 重跑，或换 <new-slug>。" >&2
      exit 3
    fi
    ;;
  2|4)
    echo "❌ precheck 前置条件不满足（rc=${PRECHECK_RC}：CLI 未装或网络异常），终止。" >&2
    exit 2
    ;;
  *)
    echo "❌ precheck 未知退出码 ${PRECHECK_RC}，终止。" >&2
    exit 2
    ;;
esac

# ---- Step 2: fork ----
step "Step 2/6: fork"
FORK_OUT="$(bash "$HERE/fork.sh" "$SOURCE" "$NEW_SLUG" 2>&1)"
echo "$FORK_OUT"
# 优先解析机器可读行 FORK_DIR=<abspath>（不依赖中文文案）
FORK="$(echo "$FORK_OUT" | grep -o '^FORK_DIR=.*' | head -1 | sed 's/^FORK_DIR=//')"
if [[ -z "$FORK" ]]; then
  echo "❌ fork.sh 未输出 FORK_DIR（可能目标已存在或 fork 失败），终止。" >&2
  exit 3
fi
[[ -d "$FORK" ]] || { echo "❌ fork 目录不存在: $FORK" >&2; exit 3; }
echo "ℹ️  FORK=$FORK"

# ---- Step 3: strip_scan（仅扫描报告，命中需人工拍板，不自动删）----
step "Step 3/6: strip_scan（扫描内网信息）"
bash "$HERE/strip_scan.sh" "$FORK" || true
echo ""
echo "⚠️  以上字面命中需【人工逐条拍板】保留/删除/改写后，再继续 push。"
echo "    run_all 不自动脱敏（避免误删）。"

# ---- Step 4: license ----
step "Step 4/6: license ($LICENSE_TYPE)"
if [[ -n "$AUTHOR" ]]; then
  bash "$HERE/gen_license.sh" "$FORK" "$LICENSE_TYPE" "$AUTHOR" "$(date +%Y)" || true
else
  echo "⚠️  未配置 OSG_AUTHOR_NAME，跳过 license 生成。请手动："
  echo "    bash $HERE/gen_license.sh \"$FORK\" $LICENSE_TYPE \"<Your Name>\" $(date +%Y)"
fi

# ---- Step 5: scaffold（README + .gitignore）----
step "Step 5/6: scaffold（README + .gitignore）"
bash "$HERE/scaffold.sh" "$FORK" || true

# ---- Step 6: git_init ----
step "Step 6/6: git_init（独立 repo + main 分支）"
if [[ -n "$AUTHOR" && -n "$EMAIL" ]]; then
  bash "$HERE/git_init.sh" "$FORK" "$AUTHOR" "$EMAIL" || true
else
  echo "⚠️  未配置身份，跳过 git_init。请手动："
  echo "    bash $HERE/git_init.sh \"$FORK\" \"<Name>\" \"<handle>@users.noreply.github.com\""
fi

# ---- 收尾指引 ----
cat <<EOF

━━━━━━━━━━ ✅ 前 6 步完成 ━━━━━━━━━━
FORK: $FORK

接下来【需人工】的步骤：
  1. 逐条处理 strip_scan 命中（保留/删除/改写）
  2. 完善 README.md 的 Features / 一句话描述
  3. frontmatter 校验:  python3 $HERE/check_frontmatter.py "$FORK"
  4. GitHub 建空 repo（https://github.com/new）+ 拿 PAT，然后：
       bash $HERE/github_push.sh "$FORK" <handle>/<repo>
       # token source: GITHUB_TOKEN / OSG_GITHUB_TOKEN / OSG_GITHUB_TOKEN_CMD / gh auth token
  5.（可选）clawhub:       bash $HERE/clawhub_publish.sh "$FORK"
  6.（可选）skillhub.cn:   SKILLHUB_CN_TOKEN=skh_xxx bash $HERE/skillhub_cn_publish.sh "$FORK"

⚠️  所有 token 只走环境变量，publish 完立即撤销。
EOF
