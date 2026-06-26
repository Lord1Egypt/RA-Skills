#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG="$SKILL_DIR/assets/config/mcporter.json"

if ! command -v mcporter >/dev/null 2>&1; then
  echo "❌ 未找到 mcporter，请先安装或确保 PATH 正确。"
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ 未找到 python3。"
  exit 1
fi

LOAD_ALL=false
if [ "${1:-}" = "--comments" ]; then
  LOAD_ALL=true
  shift
fi

if [ $# -lt 1 ]; then
  echo "用法: $0 [--comments] <关键词>"
  exit 1
fi

KEYWORD="$*"
TMP_JSON="$(mktemp)"
TMP_ROWS="$(mktemp)"
TMP_ARGS="$(mktemp)"
trap 'rm -f "$TMP_JSON" "$TMP_ROWS" "$TMP_ARGS"' EXIT

mcporter --config "$CONFIG" call xiaohongshu.search_feeds keyword="$KEYWORD" > "$TMP_JSON"

python3 - "$TMP_JSON" "$TMP_ROWS" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
obj = json.load(open(src, 'r', encoding='utf-8'))
feeds = obj.get('feeds', [])
rows = []
for f in feeds:
    if f.get('modelType') != 'note':
        continue
    note = f.get('noteCard', {})
    user = note.get('user', {})
    interact = note.get('interactInfo', {})
    rows.append({
        'id': f.get('id', ''),
        'xsecToken': f.get('xsecToken', ''),
        'title': note.get('displayTitle', ''),
        'author': user.get('nickname') or user.get('nickName') or '',
        'likes': interact.get('likedCount', ''),
        'comments': interact.get('commentCount', ''),
        'collects': interact.get('collectedCount', ''),
    })
rows = rows[:10]
print(f"🔎 共找到 {len(rows)} 条可选笔记（仅显示前10条）")
for idx, r in enumerate(rows):
    print(f"[{idx}] {r['title']}")
    print(f"    作者: {r['author']} | 点赞: {r['likes']} | 评论: {r['comments']} | 收藏: {r['collects']}")
    print(f"    feed_id: {r['id']}")
open(dst, 'w', encoding='utf-8').write(json.dumps(rows, ensure_ascii=False))
PY

printf '\n请选择编号（默认 0）: '
read -r PICK || true
PICK="${PICK:-0}"

python3 - "$PICK" "$LOAD_ALL" "$TMP_ROWS" "$TMP_ARGS" <<'PY'
import json, sys
pick = int(sys.argv[1])
load_all = sys.argv[2].lower() == 'true'
rows = json.load(open(sys.argv[3], 'r', encoding='utf-8'))
out = sys.argv[4]
if pick < 0 or pick >= len(rows):
    raise SystemExit(f'❌ 编号越界: {pick}')
r = rows[pick]
args = {
    'feed_id': r['id'],
    'xsec_token': r['xsecToken'],
    'load_all_comments': load_all,
}
open(out, 'w', encoding='utf-8').write(json.dumps(args, ensure_ascii=False))
print(f"\n📖 正在读取: {r['title']}")
print(f"feed_id: {r['id']}")
PY

mcporter --config "$CONFIG" call xiaohongshu.get_feed_detail --args "$(cat "$TMP_ARGS")"
