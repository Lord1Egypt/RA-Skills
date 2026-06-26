#!/usr/bin/env bash
set -euo pipefail

HTML_FILE="${1:?Usage: render.sh <html-file> [output-dir] [viewport]}"
OUTPUT_DIR="${2:-./screenshots}"
VIEWPORT="${3:-mobile}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

BASENAME="$(basename "$HTML_FILE" .html)"

if [[ "$OUTPUT_DIR" != /* ]]; then
  OUTPUT_DIR="$PROJECT_ROOT/$OUTPUT_DIR"
fi
mkdir -p "$OUTPUT_DIR"

# 转绝对路径
if [[ "$HTML_FILE" != /* ]]; then
  HTML_FILE="$PROJECT_ROOT/$HTML_FILE"
fi

# 截图
node "$PROJECT_ROOT/screenshot.mjs" "$HTML_FILE" \
  --viewport "$VIEWPORT" \
  --selector '#app' \
  --out "$OUTPUT_DIR" \
  --name "$BASENAME" 2>&1

# 输出截图绝对路径（文件名格式：{name}-default-{viewport}.png）
SCREENSHOT_PATH="$OUTPUT_DIR/${BASENAME}-default-${VIEWPORT}.png"
echo "$SCREENSHOT_PATH"
