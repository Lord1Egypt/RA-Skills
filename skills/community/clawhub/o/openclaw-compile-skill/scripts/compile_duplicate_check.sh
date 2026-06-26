#!/bin/bash
set -eu

FILE=""
TITLE=""
VAULT="${OPENCLAW_VAULT:-$(pwd)}"
RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"

usage() {
  echo "用法: compile_duplicate_check.sh (--file <path> | --title <title>) [--vault <path>]"
}

trim_quotes() {
  printf '%s' "$1" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' | sed 's/^"//; s/"$//'
}

extract_source() {
  local file="$1"
  local line
  line="$(sed -n 's/^source:[[:space:]]*//p' "$file" | head -n 1 || true)"
  trim_quotes "$line"
}

normalize_source() {
  python3 - "$1" <<'PY'
import sys
from urllib.parse import urlsplit, urlunsplit

raw = sys.argv[1].strip()
if not raw:
    print("")
    raise SystemExit(0)

parts = urlsplit(raw)
normalized = urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), "", ""))
print(normalized)
PY
}

# 判断是否为有意义的 URL（真实域名含 dot），非 URL 值（如 "eb-clipper"）不参与 source 比对
is_meaningful_source() {
  python3 - "$1" <<'PY'
import sys
from urllib.parse import urlsplit

raw = sys.argv[1].strip()
if not raw:
    print("false")
    raise SystemExit(0)

parts = urlsplit(raw)
# 有意义 URL：netloc 含 dot（如 x.com、example.com），非采集器标识
if parts.netloc and "." in parts.netloc:
    print("true")
else:
    print("false")
PY
}

normalize_title() {
  python3 - "$1" <<'PY'
import re
import sys
import unicodedata

raw = unicodedata.normalize("NFKC", sys.argv[1]).lower().strip()
chars = []
for ch in raw:
    cat = unicodedata.category(ch)
    if cat[0] in {"L", "N"}:
        chars.append(ch)
    else:
        chars.append(" ")

normalized = re.sub(r"\s+", " ", "".join(chars)).strip()
print(normalized)
PY
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --file)
      FILE="$2"; shift 2 ;;
    --title)
      TITLE="$2"; shift 2 ;;
    --vault)
      VAULT="$2"
      RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      usage
      exit 2 ;;
  esac
done

if [ -n "$FILE" ] && [ -n "$TITLE" ]; then
  echo "❌ --file 和 --title 只能二选一"
  usage
  exit 2
fi

if [ -z "$FILE" ] && [ -z "$TITLE" ]; then
  echo "❌ 必须提供 --file 或 --title"
  usage
  exit 2
fi

if [ -n "$FILE" ] && [ ! -f "$FILE" ]; then
  echo "❌ 文件不存在: $FILE"
  exit 2
fi

if [ -n "$FILE" ]; then
  TITLE="$(basename "$FILE" .md)"
fi

NORMALIZED_TITLE="$(normalize_title "$TITLE")"
SOURCE_URL=""
NORMALIZED_SOURCE=""

if [ -n "$FILE" ]; then
  SOURCE_URL="$(extract_source "$FILE")"
  NORMALIZED_SOURCE="$(normalize_source "$SOURCE_URL")"
fi

echo "标题=$TITLE"
echo "归一化标题=$NORMALIZED_TITLE"
if [ -n "$SOURCE_URL" ]; then
  echo "来源URL=$SOURCE_URL"
  echo "归一化来源=$NORMALIZED_SOURCE"
fi

find_duplicate_by_title() {
  local dir="$1"
  local scope="$2"
  local candidate
  for candidate in "$dir"/*.md; do
    [ -f "$candidate" ] || continue
    if [ -n "$FILE" ] && [ "$candidate" = "$FILE" ]; then
      continue
    fi
    local candidate_title candidate_normalized
    candidate_title="$(basename "$candidate" .md)"
    candidate_normalized="$(normalize_title "$candidate_title")"
    if [ "$candidate_normalized" = "$NORMALIZED_TITLE" ]; then
      echo "RESULT=DUPLICATE"
      echo "MATCH_SCOPE=$scope"
      echo "MATCH_REASON=normalized-title"
      echo "MATCH_FILE=$candidate"
      return 0
    fi
  done
  return 1
}

find_duplicate_by_source() {
  local dir="$1"
  local scope="$2"
  local candidate
  [ -n "$NORMALIZED_SOURCE" ] || return 1
  for candidate in "$dir"/*.md; do
    [ -f "$candidate" ] || continue
    if [ -n "$FILE" ] && [ "$candidate" = "$FILE" ]; then
      continue
    fi
    local candidate_source candidate_normalized_source
    candidate_source="$(extract_source "$candidate")"
    [ -n "$candidate_source" ] || continue
    candidate_normalized_source="$(normalize_source "$candidate_source")"
    if [ "$candidate_normalized_source" = "$NORMALIZED_SOURCE" ]; then
      echo "RESULT=DUPLICATE"
      echo "MATCH_SCOPE=$scope"
      echo "MATCH_REASON=source-url"
      echo "MATCH_FILE=$candidate"
      return 0
    fi
  done
  return 1
}

if [ ! -d "$RAW_DIR" ]; then
  echo "❌ 原材料仓库不存在: $RAW_DIR"
  exit 2
fi

find_duplicate_by_title "$RAW_DIR" "raw-material" && exit 1

# 编译流程中的唯一源文章库存放在原材料仓库；中转站与已入库不参与 Step 0 查重
if [ -n "$NORMALIZED_SOURCE" ] && is_meaningful_source "$NORMALIZED_SOURCE" | grep -q "true"; then
  find_duplicate_by_source "$RAW_DIR" "raw-material" && exit 1
fi

echo "RESULT=OK"
exit 0
