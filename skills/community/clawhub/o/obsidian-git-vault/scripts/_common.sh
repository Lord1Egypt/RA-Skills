#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

resolve_vault() {
	local override="${1:-}"
	local p=""
	if [[ -n "$override" && -d "$override" ]]; then
		(cd "$override" && pwd) && return 0
	fi
	if [[ -n "${OBSIDIAN_VAULT:-}" && -d "$OBSIDIAN_VAULT" ]]; then
		(cd "$OBSIDIAN_VAULT" && pwd) && return 0
	fi
	if [[ -n "${CURSOR_WORKSPACE:-}" && -d "${CURSOR_WORKSPACE}/.obsidian" ]]; then
		(cd "$CURSOR_WORKSPACE" && pwd) && return 0
	fi
	if [[ -d "${PWD}/.obsidian" ]]; then
		(cd "$PWD" && pwd) && return 0
	fi
	p="${HOME}/.openclaw/workspace/obsidian-git-vault"
	if [[ -d "$p" ]]; then
		(cd "$p" && pwd) && return 0
	fi
	return 1
}

require_git_repo() {
	local v="$1"
	git -C "$v" rev-parse --is-inside-work-tree >/dev/null 2>&1
}
