#!/usr/bin/env bash
# git_init.sh — Step 7: 本地 git init + main 分支 + user.name/email
# Usage: ./git_init.sh <fork-path> ["<user.name>"] ["<user.email>"]
# user.name/email 优先级: 命令行参数 > OSG_AUTHOR_NAME/EMAIL > profile.env > 报错
set -euo pipefail

. "$(dirname "$0")/_lib_profile.sh"
osg_resolve_identity

FORK="${1:-}"
USER_NAME="${2:-${OSG_AUTHOR_NAME:-}}"
USER_EMAIL="${3:-${OSG_AUTHOR_EMAIL:-}}"

if [[ -z "$FORK" ]]; then
  cat <<EOF >&2
Usage: $0 <fork-path> ["<user.name>"] ["<user.email>"]

身份字段不传时自动从 OSG_AUTHOR_NAME / OSG_AUTHOR_EMAIL 或 profile.env 读取。
首次配置: bash $(dirname "$0")/setup_profile.sh

⚠️  user.name / user.email 必须用对外身份（如 "Jane Doe" + "jane@users.noreply.github.com"），
   推荐 GitHub noreply 邮箱避免真实邮箱在公开 commit log 暴露。
EOF
  exit 1
fi

if [[ -z "$USER_NAME" || -z "$USER_EMAIL" ]]; then
  cat <<EOF >&2
❌ 未指定 git 身份且 OSG_* / profile.env 未配置
   请任选一种：
     ① 一次性配置（推荐）: bash $(dirname "$0")/setup_profile.sh
     ② 命令行显式传:        $0 $FORK "Jane Doe" "jane@users.noreply.github.com"
EOF
  exit 1
fi

[[ -d "$FORK" ]] || { echo "❌ fork-path not a directory: $FORK" >&2; exit 2; }

# 立即把 FORK 解析成绝对路径，避免后续 cd 进 FORK 后再用相对路径解析失败
# （bug 复现：传相对路径时，cd "$FORK" 之后 EXPECTED_GITDIR 里的 cd "$FORK" 会
#  从新 CWD 再次解析相对路径 → "没有那个文件或目录" → 二次校验崩溃，commit 未执行）
FORK="$(cd "$FORK" && pwd -P)"

cd "$FORK"

# git init 带默认分支 main（新 git ≥ 2.28 支持）
# ⚠️ 关键：只认 FORK 目录「自己的」.git，绝不能用 `git rev-parse --git-dir`——
#    该命令会向上递归探到父目录的 .git（当 fork 位于某个已是 git repo 的工作区内时，
#    会误判「已是 repo」跳过 init，导致 commit 落到父仓库而非独立仓库）。
#    fork 必须是独立 repo，否则 github_push.sh 的 [[ -d "$FORK/.git" ]] 检查会失败。
if [[ -d "$FORK/.git" ]]; then
  echo "ℹ️  $FORK/.git already exists (独立 repo)，skip init"
else
  if git init -b main 2>/dev/null; then
    echo "✅ git init -b main (独立 repo)"
  else
    # 老 git 兜底
    git init
    git symbolic-ref HEAD refs/heads/main
    echo "✅ git init + symbolic-ref HEAD refs/heads/main (old git fallback)"
  fi
fi

# 二次确认：确保 .git 真的在 FORK 目录内（防御父仓库穿透）
ACTUAL_GITDIR="$(git rev-parse --absolute-git-dir 2>/dev/null || echo '')"
EXPECTED_GITDIR="$(cd "$FORK" && pwd -P)/.git"
if [[ "$ACTUAL_GITDIR" != "$EXPECTED_GITDIR" ]]; then
  echo "❌ git 仓库不在 fork 目录内！" >&2
  echo "   期望: $EXPECTED_GITDIR" >&2
  echo "   实际: ${ACTUAL_GITDIR:-<无>}" >&2
  echo "   原因：fork 位于某个已是 git repo 的父目录内，init 被父仓库吞并。" >&2
  echo "   已在 fork 目录强制建立独立 repo，请重跑本脚本。" >&2
  exit 5
fi

# user.name / user.email（local，不污染全局）
git config user.name "$USER_NAME"
git config user.email "$USER_EMAIL"
echo "✅ git config user.name=\"$USER_NAME\" user.email=\"$USER_EMAIL\""

# core.autocrlf
git config core.autocrlf input
echo "✅ git config core.autocrlf=input"

# 首次 commit
git add .
if git diff --cached --quiet; then
  echo "ℹ️  Nothing to commit"
else
  # 从 SKILL.md 提 version（如果有）
  VERSION="$(grep -m1 -o '\*\*Version\*\*:[[:space:]]*[0-9.]*' SKILL.md 2>/dev/null | sed 's/.*Version\*\*:[[:space:]]*//' || echo "1.0.0")"
  VERSION="${VERSION:-1.0.0}"
  git commit -m "Initial open-source release: v$VERSION" \
             -m "Forked from internal version, scrubbed per opensource-skill-to-github workflow."
  echo "✅ Initial commit: v$VERSION"
fi

echo ""
echo "📝 Next steps:"
echo "   1. (Optional) Run UGLIC check: glic-check skill in UGLIC mode"
echo "   2. Create GitHub repo manually: https://github.com/new"
echo "   3. Get GitHub PAT: https://github.com/settings/tokens"
echo "   4. Run: scripts/github_push.sh $FORK <handle>/<repo-name>"
echo "      Token source: GITHUB_TOKEN / OSG_GITHUB_TOKEN / OSG_GITHUB_TOKEN_CMD / gh auth token"
