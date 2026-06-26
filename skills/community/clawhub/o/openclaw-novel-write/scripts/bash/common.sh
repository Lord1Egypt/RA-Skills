#!/bin/bash
# common.sh - 公共函数库

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# 检查文件是否存在
check_file() {
  if [ ! -f "$1" ]; then
    log_error "文件不存在: $1"
    return 1
  fi
  return 0
}

# 统计中文字数
count_chinese_words() {
  local file="$1"
  if [ ! -f "$file" ]; then
    echo "0"
    return
  fi
  cat "$file" | grep -oP '[\x{4e00}-\x{9fff}]' | wc -l
}

# 检查字数是否在范围内
validate_word_count() {
  local actual="$1"
  local min="$2"
  local max="$3"
  
  if [ "$actual" -lt "$min" ]; then
    echo "⚠️ 字数不足 (${actual}字 < ${min}字)"
    return 1
  elif [ "$actual" -gt "$max" ]; then
    echo "⚠️ 字数超出 (${actual}字 > ${max}字)"
    return 1
  else
    echo "✅ 字数符合要求 (${actual}字)"
    return 0
  fi
}
