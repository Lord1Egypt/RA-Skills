#!/usr/bin/env bash
# memlog.sh — 自动时间戳的日志追加工具

set -euo pipefail

MEMORY_DIR="${MEMORY_DIR:-$HOME/.openclaw/workspace/memory}"
TODAY=$(TZ=Asia/Shanghai date +%Y-%m-%d)
NOW=$(TZ=Asia/Shanghai date +%H:%M)
FILE="$MEMORY_DIR/$TODAY.md"

TITLE="${1:?Usage: memlog.sh \"Title\" \"Body\"}"
BODY="${2:-}"

if [[ ! -f "$FILE" ]]; then
    printf "# %s\n\n" "$TODAY" > "$FILE"
fi

{
    printf "\n### %s — %s\n" "$NOW" "$TITLE"
    [[ -n "$BODY" ]] && printf "\n%s\n" "$BODY"
} >> "$FILE"

echo "✓ Logged to $TODAY.md at $NOW"
