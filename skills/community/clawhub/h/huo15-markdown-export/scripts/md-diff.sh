#!/usr/bin/env bash
# md-diff.sh — 把 git 两个 ref 之间的 commits 渲染成 changelog PDF
#
# 用法:
#   ./md-diff.sh <from-ref> <to-ref> [output.pdf] [--theme huo15-brand] [--repo /path/to/repo]
#
# 例:
#   ./md-diff.sh v1.2.0 HEAD changelog.pdf
#   ./md-diff.sh v1.2.0 v1.3.0 release-notes.pdf --theme huo15-brand

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

FROM="${1:-}"; TO="${2:-}"
[[ -z "$FROM" || -z "$TO" ]] && {
  echo "用法: md-diff.sh <from-ref> <to-ref> [output.pdf] [--theme huo15-brand] [--repo path]"
  exit 1
}
shift 2

OUT=""
THEME="huo15-brand"
REPO="."

while [[ $# -gt 0 ]]; do
  case "$1" in
    --theme) THEME="$2"; shift 2 ;;
    --repo) REPO="$2"; shift 2 ;;
    --*) echo "未知选项: $1"; exit 1 ;;
    *) OUT="$1"; shift ;;
  esac
done

OUT="${OUT:-changelog-${FROM}-${TO}.pdf}"

cd "$REPO"
git rev-parse --git-dir >/dev/null 2>&1 || { echo "× 不是 git 仓库: $REPO"; exit 2; }

REPO_NAME="$(basename "$(git rev-parse --show-toplevel)")"
TODAY="$(date +%F)"
TMP_MD="$(mktemp -t huo15-md-diff.XXXXXX.md)"
trap 'rm -f "$TMP_MD"' EXIT

{
  echo "# Changelog: ${REPO_NAME}"
  echo
  echo "> ${FROM} → ${TO}  ·  ${TODAY}"
  echo
  echo "## 概览"
  echo
  STATS=$(git diff --shortstat "${FROM}..${TO}" 2>/dev/null || echo "(stat 计算失败)")
  COMMITS=$(git rev-list --count "${FROM}..${TO}" 2>/dev/null || echo "?")
  echo "- 提交数: **${COMMITS}**"
  echo "- 变更: ${STATS}"
  echo
  echo "## 提交列表"
  echo
  git log --reverse --pretty=format:"- \`%h\` %s _(%an, %ad)_" --date=short "${FROM}..${TO}" 2>/dev/null || echo "(log 失败)"
  echo
  echo
  echo "## 文件变更"
  echo
  echo '```'
  git diff --stat "${FROM}..${TO}" 2>/dev/null | head -200
  echo '```'
} > "$TMP_MD"

bash "$SCRIPT_DIR/md2pdf.sh" "$TMP_MD" "$OUT" --theme "$THEME" --header "${REPO_NAME} Changelog" --footer "{pageNumber} / {totalPages}  ·  huo15.com"
echo "✓ $OUT  (${FROM}..${TO}  ${COMMITS} commits)"
