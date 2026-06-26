#!/bin/bash
# model-switch — 模型切换与管理工具（Shell 入口）
# 用法: bash model-switcher.sh <command> [args...]
# 示例: bash model-switcher.sh switch main openai/gpt-4o
#       bash model-switcher.sh add openai gpt-5
#       bash model-switcher.sh list
#       bash model-switcher.sh compare

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/model_switcher.py" "$@"
