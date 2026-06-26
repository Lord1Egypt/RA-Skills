#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"
REMOTE="${OBSIDIAN_GIT_REMOTE:-origin}"
ALLOW_FORCE_LEASE="${OBSIDIAN_SOP_FORCE_LEASE:-0}"
REBASE_PULL="${OBSIDIAN_PULL_REBASE:-0}"

usage() {
	echo "用法: $0 [VAULT_DIR]" >&2
	echo "环境: OBSIDIAN_VAULT | CURSOR_WORKSPACE | 当前目录 .obsidian | 默认 ~/.openclaw/workspace/obsidian-git-vault" >&2
	echo "      OBSIDIAN_GIT_REMOTE (默认 origin)" >&2
	echo "      OBSIDIAN_SOP_FORCE_LEASE=1  push 被拒时尝试 --force-with-lease" >&2
	echo "      OBSIDIAN_PULL_REBASE=1  落后时使用 pull --rebase" >&2
	echo "退出码: 0 无需同步或已 push/pull 成功 | 1 参数错误 | 2 分叉 | 3 无远程 | 4 无上游 | 5 工作区未提交 | 其它 git 失败" >&2
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then usage; exit 0; fi

V="$(resolve_vault "${1:-}")" || { usage; exit 1; }
V="$(cd "$V" && pwd)"

if ! require_git_repo "$V"; then
	echo "不是 Git 仓库: $V" >&2
	exit 1
fi

if [[ -n "$(git -C "$V" status --porcelain 2>/dev/null)" ]]; then
	echo "工作区有未提交变更，请先 commit 或 stash。文件:" >&2
	git -C "$V" status -s >&2
	exit 5
fi

if ! git -C "$V" remote get-url "$REMOTE" >/dev/null 2>&1; then
	echo "NO_REMOTE: 无远程 $REMOTE，参见 git-remote-wizard.md" >&2
	exit 3
fi

git -C "$V" fetch "$REMOTE"

if ! git -C "$V" rev-parse --verify "@{u}" >/dev/null 2>&1; then
	echo "NO_UPSTREAM: 当前分支未跟踪远程，例如: git push -u $REMOTE \"\$(git branch --show-current)\"" >&2
	exit 4
fi

read -r ahead behind _ < <(git -C "$V" rev-list --left-right --count HEAD..."@{u}" 2>/dev/null || echo "0 0")

if [[ "$ahead" -gt 0 && "$behind" -gt 0 ]]; then
	echo "DIVERGED: 本地领先 $ahead、落后 $behind，需人工合并或 rebase（见 vault-sync-sop 第 3 节）" >&2
	git -C "$V" log --oneline -n 5 HEAD >&2
	git -C "$V" log --oneline -n 5 "@{u}" >&2
	exit 2
fi

if [[ "$ahead" -eq 0 && "$behind" -eq 0 ]]; then
	echo "SYNC_OK: 与 @{u} 一致，无需 push/pull"
	exit 0
fi

if [[ "$ahead" -gt 0 && "$behind" -eq 0 ]]; then
	if git -C "$V" push; then
		echo "PUSH_OK"
		exit 0
	fi
	if [[ "$ALLOW_FORCE_LEASE" == "1" ]]; then
		echo "push 失败，尝试 --force-with-lease（需已接受 SOP）" >&2
		git -C "$V" push --force-with-lease
		echo "PUSH_FORCE_LEASE_OK"
		exit 0
	fi
	echo "push 失败；可设 OBSIDIAN_SOP_FORCE_LEASE=1 再试（force-with-lease）" >&2
	exit 9
fi

if [[ "$ahead" -eq 0 && "$behind" -gt 0 ]]; then
	if [[ "$REBASE_PULL" == "1" ]]; then
		git -C "$V" pull --rebase
	else
		git -C "$V" pull
	fi
	if [[ -n "$(git -C "$V" diff --name-only --diff-filter=U)" ]]; then
		echo "CONFLICT: 存在合并冲突" >&2
		git -C "$V" diff --name-only --diff-filter=U >&2
		exit 10
	fi
	echo "PULL_OK"
	exit 0
fi

exit 1
