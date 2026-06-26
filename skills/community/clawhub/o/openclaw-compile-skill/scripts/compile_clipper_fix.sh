#!/bin/bash
set -u

FILE=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --file)
      FILE="$2"; shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$FILE" ]; then
  echo "用法: compile_clipper_fix.sh --file <收件箱原文路径>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "❌ 文件不存在: $FILE"
  exit 1
fi

TMP_BASE="${TMPDIR:-$(python3 - <<'PY'
import tempfile
print(tempfile.gettempdir())
PY
)}"
BACKUP_DIR="$TMP_BASE/clipper_fix_backup/$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$BACKUP_DIR"
cp "$FILE" "$BACKUP_DIR/$(basename "$FILE")"

python3 - "$FILE" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8')
original = text
logs = []

if text.startswith('---\n'):
    second = text.find('\n---\n', 4)
    if second == -1:
        split = text.find('\n# ')
        if split == -1:
            split = text.find('\n## ')
        if split != -1:
            fm = text[:split]
            body = text[split+1:]
            text = fm.rstrip() + '\n---\n' + body
            logs.append('补全 frontmatter 结束分隔符')

text2 = text.replace('\nValue:', '\nauthor:')
if text2 != text:
    text = text2
    logs.append('Value -> author')

text2 = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
if text2 != text:
    text = text2
    logs.append('弯引号 -> 直引号')

if text.startswith('---\n'):
    parts = text.split('\n---\n', 1)
    if len(parts) == 2:
        fm, body = parts
        fm_lines = fm.splitlines()
        images = []
        kept = []
        for line in fm_lines:
            stripped = line.strip()
            if stripped.startswith('![['):
                images.append(stripped)
            else:
                kept.append(line)
        if images:
            body = '\n'.join(images) + '\n\n' + body.lstrip('\n')
            text = '\n'.join(kept) + '\n---\n' + body
            logs.append('YAML 内图片移到正文开头')

        def quote_yaml_value(match):
            key = match.group(1)
            value = match.group(2).strip()
            if not value or value.startswith(('"', "'", '[', '{')):
                return match.group(0)
            if any(ch in value for ch in [':', '@', '|']):
                return f'{key}: "{value}"'
            return match.group(0)

        new_fm = []
        for line in kept:
            new_fm.append(re.sub(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.+)$', quote_yaml_value, line))
        rebuilt = '\n'.join(new_fm) + '\n---\n' + body
        if rebuilt != text:
            text = rebuilt
            logs.append('补加 YAML 特殊值双引号')

path.write_text(text, encoding='utf-8')
for item in logs:
    print(f'FIX: {item}')
print('RESULT: CLEAN' if text == original else 'RESULT: FIXED')
PY

rc=$?
if [ "$rc" -ne 0 ]; then
  echo "❌ clipper 修复失败"
  exit 1
fi

echo "BACKUP: $BACKUP_DIR/$(basename "$FILE")"
exit 0
