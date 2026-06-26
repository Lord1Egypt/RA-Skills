#!/usr/bin/env bash
set -euo pipefail
TZ="${OBSIDIAN_CRON_TZ:-Asia/Shanghai}"
NAME="${OBSIDIAN_CRON_NAME:-obsidian-vault-sync}"
EXPR="${OBSIDIAN_CRON_EXPR:-0 */2 * * *}"
MSG="${OBSIDIAN_CRON_MESSAGE:-按 obsidian-git-vault skill：对默认/当前 vault 执行 scripts/vault-sync.sh（先 resolve）；失败则报告并停止；强推仅当已接受 SOP 且 OBSIDIAN_SOP_FORCE_LEASE=1。}"

if ! command -v openclaw >/dev/null 2>&1; then
	echo "未找到 openclaw 命令，跳过 cron 注册。" >&2
	exit 1
fi

openclaw cron add \
	--name "$NAME" \
	--cron "$EXPR" \
	--tz "$TZ" \
	--session isolated \
	--message "$MSG"
