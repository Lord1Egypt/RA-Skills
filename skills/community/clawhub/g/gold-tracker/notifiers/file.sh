#!/bin/sh
# 写文件通知器（默认示例，无真实通知渠道时使用，也用于测试）。
#
# 输入：stdin 传入消息正文。
# 输出：追加到 $OUTPUT_FILE（相对 $SKILL_ROOT，缺省 notifications/latest.txt）。
# 成功：stdout 输出 "SENT"（与 config.yaml 中 success_marker 一致）。
#
# 复制本文件改造为任意渠道：只需保证「成功时 stdout 输出 success_marker」，
# 退出码 0。其余消息组装/重试/去重/超时全部由 notify.py 统一处理。
set -eu

SKILL_ROOT="${SKILL_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
OUTPUT_FILE="${OUTPUT_FILE:-notifications/latest.txt}"

mkdir -p "$SKILL_ROOT/notifications"
{
  echo "--- $(date '+%Y-%m-%d %H:%M:%S') ---"
  cat
  echo
} >> "$SKILL_ROOT/$OUTPUT_FILE"

echo "SENT"
