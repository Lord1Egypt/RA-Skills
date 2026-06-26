#!/usr/bin/env bash
# extract-messages.sh — 从会话文件中提取用户消息（调用 Python 脚本实现）
# 输入：_mbti_work/session_list.txt
# 输出：_mbti_work/user_messages.txt（每条消息之间用 --- 分隔）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/extract_messages.py"
