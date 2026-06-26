#!/usr/bin/env bash
set -euo pipefail

QUERY="${1:-}"
OUT_PATH="${2:-}"
PORT_FILE="$HOME/.openclaw/music/port"
CACHE_INDEX="$HOME/.openclaw/music/cache-index.json"
DEFAULT_DIR="$HOME/.openclaw/media"

if [ -z "$QUERY" ]; then
  echo "usage: $0 <query> [output-path]" >&2
  exit 1
fi

if [ -z "$OUT_PATH" ]; then
  SAFE_NAME="$(printf '%s' "$QUERY" | tr '/ ' '__' | tr -cd '[:alnum:]_-.一-龥')"
  [ -n "$SAFE_NAME" ] || SAFE_NAME="music"
  OUT_PATH="$DEFAULT_DIR/${SAFE_NAME}.mp3"
fi

mkdir -p "$(dirname "$OUT_PATH")" "$(dirname "$CACHE_INDEX")"
PORT="$(cat "$PORT_FILE" 2>/dev/null || echo 8080)"

python3 - <<'PY' "$QUERY" "$OUT_PATH" "$CACHE_INDEX"
import json, os, sys
query, out_path, cache_index = sys.argv[1:4]
if os.path.exists(out_path) and os.path.getsize(out_path) > 1024:
    print(json.dumps({'cache_hit': True, 'path': out_path, 'size': os.path.getsize(out_path), 'reason': 'output_exists'}, ensure_ascii=False))
    raise SystemExit(0)
if os.path.exists(cache_index):
    try:
        idx = json.load(open(cache_index, 'r', encoding='utf-8'))
    except Exception:
        idx = {}
    hit = idx.get(query)
    if isinstance(hit, dict):
        p = hit.get('path')
        if p and os.path.exists(p) and os.path.getsize(p) > 1024:
            if p != out_path:
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                import shutil
                shutil.copy2(p, out_path)
            print(json.dumps({'cache_hit': True, 'path': out_path, 'size': os.path.getsize(out_path), 'reason': 'query_index', 'chosen': hit.get('chosen')}, ensure_ascii=False))
            raise SystemExit(0)
print('{}')
PY

JSON="$(curl -fsS --get --data-urlencode "q=${QUERY}" "http://localhost:${PORT}/api/v1/music/search")"

python3 - <<'PY' "$JSON" "$PORT" "$QUERY" "$OUT_PATH" "$CACHE_INDEX"
import json, os, re, shutil, sys, urllib.parse, urllib.request
raw, port, query, out_path, cache_index = sys.argv[1:6]
data = json.loads(raw)
items = []
if isinstance(data, dict):
    if isinstance(data.get('data'), list):
        items = data['data']
    elif isinstance(data.get('data'), dict):
        inner = data['data']
        if isinstance(inner.get('data'), list):
            items = inner['data']
        elif isinstance(inner.get('list'), list):
            items = inner['list']
        elif isinstance(inner.get('songs'), list):
            items = inner['songs']
    elif isinstance(data.get('list'), list):
        items = data['list']
if not items:
    raise SystemExit('no items parsed from search response')

query_l = query.lower()
prefer_artist = None
for name in ('周杰伦', 'jay chou', 'jay', '林俊杰', '陈奕迅'):
    if name in query_l:
        prefer_artist = name
        break

def slug(text):
    text = re.sub(r'[^\w\-一-龥]+', '_', text, flags=re.UNICODE)
    text = re.sub(r'_+', '_', text).strip('_')
    return text or 'music'

def score(item):
    name = str(item.get('name', ''))
    artist = str(item.get('artist', ''))
    source = str(item.get('source', ''))
    s = 0
    for token in query.replace('/', ' ').split():
        if token and token in name:
            s += 80
        if token and token in artist:
            s += 50
    if prefer_artist and prefer_artist.replace(' ', '').lower() in artist.replace(' ', '').lower():
        s += 120
    if source in ('migu', 'qq', 'netease', 'kuwo', 'kugou'):
        s += 20
    bad_words = ('伴奏', '小提琴', '翻唱', 'cover', 'live', 'dj', 'remix', '纯音乐')
    if any(word.lower() in (name + ' ' + artist).lower() for word in bad_words):
        s -= 100
    return s

chosen = sorted(items, key=score, reverse=True)[0]
default_name = f"{slug(chosen.get('artist','unknown'))}-{slug(chosen.get('name','music'))}.mp3"
default_path = os.path.join(os.path.expanduser('~/.openclaw/media'), default_name)

if os.path.exists(default_path) and os.path.getsize(default_path) > 1024:
    if os.path.abspath(default_path) != os.path.abspath(out_path):
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        shutil.copy2(default_path, out_path)
    try:
        idx = json.load(open(cache_index, 'r', encoding='utf-8')) if os.path.exists(cache_index) else {}
    except Exception:
        idx = {}
    idx[query] = {'path': out_path, 'chosen': chosen}
    json.dump(idx, open(cache_index, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(json.dumps({'cache_hit': True, 'path': out_path, 'size': os.path.getsize(out_path), 'reason': 'song_file_exists', 'chosen': chosen}, ensure_ascii=False))
    raise SystemExit(0)

os.makedirs(os.path.dirname(out_path), exist_ok=True)
params = urllib.parse.urlencode({'id': chosen['id'], 'source': chosen['source']})
url = f'http://localhost:{port}/api/v1/music/stream?{params}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp, open(out_path, 'wb') as f:
    while True:
        chunk = resp.read(65536)
        if not chunk:
            break
        f.write(chunk)
if os.path.abspath(default_path) != os.path.abspath(out_path):
    shutil.copy2(out_path, default_path)
try:
    idx = json.load(open(cache_index, 'r', encoding='utf-8')) if os.path.exists(cache_index) else {}
except Exception:
    idx = {}
idx[query] = {'path': out_path, 'chosen': chosen}
json.dump(idx, open(cache_index, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(json.dumps({'cache_hit': False, 'chosen': chosen, 'path': out_path, 'canonical_path': default_path, 'size': os.path.getsize(out_path)}, ensure_ascii=False))
PY

RESULT_JSON="$(python3 - <<'PY' "$QUERY" "$OUT_PATH" "$CACHE_INDEX"
import json, os, sys
query, out_path, cache_index = sys.argv[1:4]
idx = {}
if os.path.exists(cache_index):
    try:
        idx = json.load(open(cache_index, 'r', encoding='utf-8'))
    except Exception:
        idx = {}
entry = idx.get(query, {})
print(json.dumps(entry, ensure_ascii=False))
PY
)"
SONG_JSON="$(python3 - <<'PY' "$RESULT_JSON"
import json, sys
entry = json.loads(sys.argv[1] or '{}')
print(json.dumps(entry.get('chosen') or {}, ensure_ascii=False))
PY
)"
COVER_URL="$(python3 - <<'PY' "$SONG_JSON"
import json, sys
song = json.loads(sys.argv[1] or '{}')
print(song.get('cover',''))
PY
)"
LYRIC_URL="$(python3 - <<'PY' "$SONG_JSON" "$PORT"
import json, sys, urllib.parse
song = json.loads(sys.argv[1] or '{}')
port = sys.argv[2]
id_ = song.get('id','')
source = song.get('source','')
if id_ and source:
    print(f"http://localhost:{port}/api/v1/music/lyric?" + urllib.parse.urlencode({'id': id_, 'source': source}))
else:
    print('')
PY
)"
python3 "$(dirname "$0")/embed_metadata.py" "$OUT_PATH" "$PORT" "$SONG_JSON" "$COVER_URL" "$LYRIC_URL" >/dev/null || true
