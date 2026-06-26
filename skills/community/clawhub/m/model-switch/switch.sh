#!/bin/bash
# switch.sh — Thin wrapper: 调用 Python 版 model_switcher
# 用法: bash switch.sh <agent_id> <model>
# 示例: bash switch.sh main openai/gpt-4o
#       bash switch.sh ALL deepseek/deepseek-v4-flash

set -e

AGENT_ID="${1:?Usage: switch.sh <agent_id|ALL> <model>}"
TARGET_MODEL="${2:?Usage: switch.sh <agent_id|ALL> <model>}";

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec python3 "$SCRIPT_DIR/model_switcher.py" switch "$AGENT_ID" "$TARGET_MODEL"
