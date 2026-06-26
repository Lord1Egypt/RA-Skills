#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"
if V="$(resolve_vault "${1:-}")"; then
	printf '%s\n' "$V"
else
	echo "无法解析 vault：请设置 OBSIDIAN_VAULT、传入绝对路径、在含 .obsidian 的目录执行，或先 init-default-vault.sh。" >&2
	exit 1
fi
