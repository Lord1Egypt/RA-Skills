#!/bin/bash
set -u

SOURCE=""
COMPILED=""
TITLE=""
VAULT="${OPENCLAW_VAULT:-$(pwd)}"
RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
TRANSIT_DIR="${COMPILE_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source)
      SOURCE="$2"; shift 2 ;;
    --compiled)
      COMPILED="$2"; shift 2 ;;
    --title)
      TITLE="$2"; shift 2 ;;
    --vault)
      VAULT="$2"
      RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
      TRANSIT_DIR="${COMPILE_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$SOURCE" ] || [ -z "$COMPILED" ] || [ -z "$TITLE" ]; then
  echo "用法: compile_archive.sh --source <path> --compiled <path> --title <title>"
  exit 1
fi

if [ ! -f "$SOURCE" ] || [ ! -f "$COMPILED" ]; then
  echo "❌ source 或 compiled 文件不存在"
  exit 1
fi

COMPILED_BASENAME="$(basename "$COMPILED" .md)"
if [ "$COMPILED_BASENAME" != "$TITLE" ]; then
  echo "❌ 中转站文件名与标题不一致: compiled=$COMPILED_BASENAME | title=$TITLE"
  exit 1
fi

RAW_TARGET="$RAW_DIR/$(basename "$SOURCE")"
if [ -e "$RAW_TARGET" ]; then
  echo "❌ 原材料目标已存在: $RAW_TARGET"
  exit 1
fi

SRC_ASSET_DIR="$(dirname "$SOURCE")/assets/$(basename "$SOURCE" .md)"
RAW_ASSET_DIR="$RAW_DIR/assets/$TITLE"
if [ -d "$SRC_ASSET_DIR" ] && [ -e "$RAW_ASSET_DIR" ]; then
  echo "❌ 原材料图片目标已存在: $RAW_ASSET_DIR"
  exit 1
fi

mv "$SOURCE" "$RAW_TARGET"
echo "MOVED_SOURCE: $RAW_TARGET"

if [ -d "$SRC_ASSET_DIR" ]; then
  mkdir -p "$(dirname "$RAW_ASSET_DIR")"
  mv "$SRC_ASSET_DIR" "$RAW_ASSET_DIR"
  echo "MOVED_ASSETS: $RAW_ASSET_DIR"
fi

rel_without_ext() {
  local path="$1"
  case "$path" in
    "$VAULT"/*)
      path="${path#$VAULT/}" ;;
  esac
  path="${path%.md}"
  printf '%s' "$path"
}

RAW_REL="$(rel_without_ext "$RAW_TARGET")"
COMPILED_REL="$(rel_without_ext "$COMPILED")"

python3 - "$RAW_TARGET" "$COMPILED" "$RAW_REL" "$COMPILED_REL" <<'PY'
from pathlib import Path
import re
import sys

raw_path = Path(sys.argv[1])
compiled_path = Path(sys.argv[2])
raw_rel = sys.argv[3]
compiled_rel = sys.argv[4]


def upsert(text, key, value):
    pattern = re.compile(rf'^{re.escape(key)}:.*$', re.M)
    line = f'{key}: {value}'
    if pattern.search(text):
        return pattern.sub(line, text, count=1)
    parts = text.split('\n---\n', 1)
    if len(parts) != 2:
        raise SystemExit('frontmatter 结构异常')
    return parts[0] + '\n' + line + '\n---\n' + parts[1]

raw_text = raw_path.read_text(encoding='utf-8')
compiled_text = compiled_path.read_text(encoding='utf-8')

raw_text = upsert(raw_text, 'type', '"raw-material"')
raw_text = upsert(raw_text, 'status', '"archived"')
raw_text = upsert(raw_text, 'compiled_version', f'"[[{compiled_rel}]]"')
compiled_text = upsert(compiled_text, 'original', f'"[[{raw_rel}]]"')
compiled_text = re.sub(r'(^-\s*原材料：)\s*.*$', rf'\1[[{raw_rel}]]', compiled_text, count=1, flags=re.M)

raw_path.write_text(raw_text, encoding='utf-8')
compiled_path.write_text(compiled_text, encoding='utf-8')
print(f'RAW_LINK=[[{compiled_rel}]]')
print(f'COMPILED_LINK=[[{raw_rel}]]')
PY

rc=$?
if [ "$rc" -ne 0 ]; then
  echo "❌ frontmatter 回写失败"
  exit 1
fi

grep -q "\[\[$COMPILED_REL\]\]" "$RAW_TARGET" || { echo "❌ 原材料 compiled_version 回读失败"; exit 1; }
grep -q "\[\[$RAW_REL\]\]" "$COMPILED" || { echo "❌ 中转站 original 回读失败"; exit 1; }
grep -q -- "- 原材料：\[\[$RAW_REL\]\]" "$COMPILED" || { echo "❌ 中转站来源区原材料回读失败"; exit 1; }

echo "RESULT: OK"
exit 0
