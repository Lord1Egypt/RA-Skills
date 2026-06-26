#!/bin/bash
# nas-dashboard/all-in-one.sh
# 数据采集 + 格式化 → 输出完整仪表盘文本
# agent 只需: bash all-in-one.sh | 发送到 Telegram

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── 1. 采集 ──
TMPFILE=$(mktemp /tmp/nas-collect.XXXXXX)
bash "$SCRIPT_DIR/scripts/collect.sh" 2>/dev/null > "$TMPFILE"

# ── 2. 格式化 ──
python3 "$SCRIPT_DIR/scripts/format.py" "$TMPFILE"
rm -f "$TMPFILE"
