#!/bin/bash
# run.sh — 定时执行 scrape.js，如果登录失效则通知
# 用法: ./run.sh [自定义prompt]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$ROOT_DIR/output/run.log"
NOTIFY_FILE="$ROOT_DIR/output/notify-login-expired"

mkdir -p "$ROOT_DIR/output"

echo "$(date '+%Y-%m-%d %H:%M:%S') — 开始执行 Grok 抓取" >> "$LOG_FILE"

# 切换到 scripts 目录执行，因为 package.json 在这里
cd "$SCRIPT_DIR" || exit 1

# 执行抓取（exit 3 = Grok service error，自动重试一次）
OUTPUT=$(npm run scrape --silent -- "$@" 2>&1)
EXIT_CODE=$?
echo "$OUTPUT" >> "$LOG_FILE"

if [ $EXIT_CODE -eq 3 ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') — ⚠️ Grok 服务错误，15s 后重试..." >> "$LOG_FILE"
  sleep 15
  OUTPUT=$(npm run scrape --silent -- "$@" 2>&1)
  EXIT_CODE=$?
  echo "$OUTPUT" >> "$LOG_FILE"
fi

if [ $EXIT_CODE -eq 2 ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') — ⚠️ 登录已失效" >> "$LOG_FILE"
  echo "$(date '+%Y-%m-%d %H:%M:%S')" > "$NOTIFY_FILE"
elif [ $EXIT_CODE -eq 0 ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') — ✅ 抓取成功" >> "$LOG_FILE"
  rm -f "$NOTIFY_FILE"
else
  echo "$(date '+%Y-%m-%d %H:%M:%S') — ❌ 抓取失败 (exit $EXIT_CODE)" >> "$LOG_FILE"
fi

exit $EXIT_CODE