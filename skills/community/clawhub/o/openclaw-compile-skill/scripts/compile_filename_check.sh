#!/bin/bash
set -eu

FILE=""
LLM_SUMMARY=""
LLM_KEYWORDS=""
APPLY=0
VAULT="${OPENCLAW_VAULT:-$(pwd)}"
LOG_FILE="${COMPILE_FILENAME_LOG_FILE:-}"

sanitize_filename() {
  printf '%s' "$1" | tr '/:|"' '----' | tr -d '?' | sed 's/[[:space:]]\+$//' | cut -c1-80
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --file)
      FILE="$2"; shift 2 ;;
    --llm-summary)
      LLM_SUMMARY="$2"; shift 2 ;;
    --llm-keywords)
      LLM_KEYWORDS="$2"; shift 2 ;;
    --apply)
      APPLY=1; shift ;;
    --vault)
      VAULT="$2"
      LOG_FILE="${COMPILE_FILENAME_LOG_FILE:-}"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$FILE" ] || [ -z "$LLM_SUMMARY" ] || [ -z "$LLM_KEYWORDS" ]; then
  echo "用法: compile_filename_check.sh --file <path> --llm-summary <text> --llm-keywords <csv> [--apply]"
  exit 2
fi

if [ -z "$LOG_FILE" ]; then
  echo "❌ COMPILE_FILENAME_LOG_FILE 未配置；拒绝写入通用日志目录。"
  exit 2
fi

if [ ! -f "$FILE" ]; then
  echo "❌ 文件不存在: $FILE"
  exit 2
fi

BASENAME="$(basename "$FILE" .md)"
SUGGESTED="$(sanitize_filename "$LLM_SUMMARY")"

printf '文件名=%s\n' "$BASENAME"
printf '主题=%s\n' "$LLM_SUMMARY"
printf '关键词=%s\n' "$LLM_KEYWORDS"

if printf '%s' "$BASENAME" | grep -Fqi -- "$SUGGESTED" || printf '%s' "$SUGGESTED" | grep -Fqi -- "$BASENAME"; then
  echo "判定=一致"
  exit 0
fi

DIRNAME="$(dirname "$FILE")"
NEW_FILE="$DIRNAME/$SUGGESTED.md"
if [ -e "$NEW_FILE" ]; then
  echo "❌ 建议改名目标已存在: $NEW_FILE"
  exit 2
fi

if [ "$APPLY" -ne 1 ]; then
  echo "判定=不一致"
  echo "建议改名=$NEW_FILE"
  echo "提示=如需执行改名，请追加 --apply"
  exit 1
fi

mv "$FILE" "$NEW_FILE"
mkdir -p "$(dirname "$LOG_FILE")"
if [ ! -f "$LOG_FILE" ]; then
  cat > "$LOG_FILE" <<'EOF'
# 荔枝编译决策日志

| 日期 | 原文件名 | 改后文件名 | 理由 |
|---|---|---|---|
EOF
fi
printf '| %s | %s | %s | %s |\n' "$(date +%Y-%m-%d)" "$BASENAME" "$SUGGESTED" "$LLM_SUMMARY" >> "$LOG_FILE"

echo "判定=不一致"
echo "已改名=$NEW_FILE"
exit 1
