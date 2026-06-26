#!/usr/bin/env bash
# Joplin API helper — simple, fast, no dependencies
# Usage: joplin.sh <command> [args...]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

# ── Load .env ──────────────────────────────────────────────

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: $ENV_FILE not found. Copy .env.example to .env and set api_token." >&2
  exit 1
fi

TOKEN=""
HOST=""
BASE=""

# Parse .env (skip comments and empty lines)
while IFS='=' read -r key value; do
  key=$(echo "$key" | xargs)
  value=$(echo "$value" | xargs | sed "s/^[\"']//;s/[\"']$//")
  case "$key" in
    api_token)   TOKEN="$value" ;;
    joplin_host) HOST="$value" ;;
    base_url)    BASE="$value" ;;
  esac
done < "$ENV_FILE"

if [[ -z "$TOKEN" ]]; then
  echo "Error: api_token is empty in $ENV_FILE" >&2
  exit 1
fi

# Determine mode
if [[ -n "$HOST" ]]; then
  REMOTE=true
else
  REMOTE=false
  BASE="${BASE:-http://localhost:41184}"
fi

# ── Helpers ────────────────────────────────────────────────

# Build a full URL with token appended correctly
# Usage: build_url PATH
build_url() {
  local base="$1"
  local path="$2"
  if [[ "$path" == *"?"* ]]; then
    echo "${base}${path}&token=${TOKEN}"
  else
    echo "${base}${path}?token=${TOKEN}"
  fi
}

# Make API request
# Usage: api_req METHOD PATH [DATA_JSON]
api_req() {
  local method="$1"
  local path="$2"
  local data="${3:-}"

  if [[ "$REMOTE" == true ]]; then
    local url
    url=$(build_url "http://127.0.0.1:41184" "$path")
    if [[ -n "$data" ]]; then
      # Base64 encode body to avoid shell quote swallowing on remote
      local b64
      b64=$(printf '%s' "$data" | base64 -w 0)
      # Use env vars + bash -c to avoid zsh globbing on remote macOS
      ssh "$HOST" "JOP_URL='${url}' JOP_BODY='${b64}' JOP_METHOD=${method} bash -c 'curl -s -X \$JOP_METHOD -H \"Content-Type: application/json\" -d \"\$(echo \"\$JOP_BODY\" | base64 -d)\" \"\$JOP_URL\"'"
    else
      # Use env var to avoid zsh globbing on remote macOS
      ssh "$HOST" "JOP_URL='${url}' JOP_METHOD=${method} bash -c 'curl -s -X \$JOP_METHOD \"\$JOP_URL\"'"
    fi
  else
    local url
    url=$(build_url "$BASE" "$path")
    if [[ -n "$data" ]]; then
      curl -s -X "$method" -H "Content-Type: application/json" -d "$data" "$url"
    else
      curl -s -X "$method" "$url"
    fi
  fi
}

# Pretty-print JSON if output looks like JSON, otherwise pass through
# Usage: pretty_json
pretty_json() {
  local input
  input=$(cat)
  # Check if it looks like JSON (starts with { or [)
  if [[ "$input" == "{"* ]] || [[ "$input" == "["* ]]; then
    echo "$input" | python3 -m json.tool 2>/dev/null || echo "$input"
  else
    echo "$input"
  fi
}

# URL-encode a string safely (via stdin, no shell injection)
# Usage: url_encode STRING
url_encode() {
  printf '%s' "$1" | python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read()), end='')"
}

# ── Commands ───────────────────────────────────────────────

cmd_ping() {
  local response
  if [[ "$REMOTE" == true ]]; then
    response=$(ssh "$HOST" "curl -s http://127.0.0.1:41184/ping" 2>/dev/null) || {
      echo "❌ Joplin Clipper Server 未运行（端口 41184，主机 $HOST）" >&2
      return 7
    }
  else
    response=$(curl -s -o /dev/null -w '%{http_code}' "${BASE}/ping" 2>/dev/null) || {
      echo "❌ Joplin Clipper Server 未运行（端口 41184）" >&2
      return 7
    }
    if [[ "$response" != "200" ]]; then
      response=$(curl -s "${BASE}/ping" 2>/dev/null) || true
    fi
  fi
  echo "✅ Joplin Clipper Server running (${response})"
}

cmd_get() {
  local note_id="$1"
  local fields="${2:-id,title,body}"
  api_req GET "/notes/${note_id}?fields=${fields}" | pretty_json
}

cmd_note() {
  # Friendly display: title + body preview
  local note_id="$1"
  local raw
  raw=$(api_req GET "/notes/${note_id}?fields=id,title,body,created_time,updated_time")

  local title body created updated
  title=$(echo "$raw" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title','(无标题)'))" 2>/dev/null) || title="(解析失败)"
  body=$(echo "$raw" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('body',''))" 2>/dev/null) || body=""
  created=$(echo "$raw" | python3 -c "import sys,json,datetime; d=json.load(sys.stdin); ts=d.get('created_time',0); print(datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M')) if ts else print('N/A')" 2>/dev/null) || created="N/A"
  updated=$(echo "$raw" | python3 -c "import sys,json,datetime; d=json.load(sys.stdin); ts=d.get('updated_time',0); print(datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M')) if ts else print('N/A')" 2>/dev/null) || updated="N/A"

  echo "📝 $title"
  echo "   创建: $created  更新: $updated"
  echo "---"
  # Show body preview (first 50 lines or full if shorter)
  if [[ -n "$body" ]]; then
    echo "$body" | head -50
    local total_lines
    total_lines=$(echo "$body" | wc -l)
    if [[ "$total_lines" -gt 50 ]]; then
      echo "... (共 $total_lines 行，显示前 50 行)"
    fi
  else
    echo "(空笔记)"
  fi
}

cmd_create() {
  local folder_id="$1"
  local title="$2"
  local body_file="$3"
  local body
  body=$(cat "$body_file")
  # Use python3 json.dumps for proper JSON encoding
  local data
  data=$(python3 -c "import json,sys; print(json.dumps({'title':sys.argv[1],'body':sys.argv[2],'parent_id':sys.argv[3]}), end='')" "$title" "$body" "$folder_id")
  api_req POST "/notes" "$data" | pretty_json
}

cmd_update() {
  local note_id="$1"
  local body_file="$2"
  local body
  body=$(cat "$body_file")
  # Unified: use python3 json.dumps for proper JSON encoding
  local data
  data=$(python3 -c "import json,sys; print(json.dumps({'body':sys.argv[1]}), end='')" "$body")
  api_req PUT "/notes/${note_id}" "$data" | pretty_json
}

cmd_delete() {
  local note_id="$1"
  local permanent="${2:-0}"
  local path="/notes/${note_id}"
  if [[ "$permanent" == "1" ]] || [[ "$permanent" == "--permanent" ]]; then
    path="${path}?permanent=1"
  fi
  api_req DELETE "$path" | pretty_json
}

cmd_search() {
  local query="$1"
  local fields="${2:-id,title}"
  local limit="${3:-50}"
  # Safe URL encoding via stdin (no shell injection)
  local encoded
  encoded=$(url_encode "$query")
  api_req GET "/search?query=${encoded}&fields=${fields}&limit=${limit}" | pretty_json
}

cmd_list() {
  local folder_id="$1"
  local fields="${2:-id,title,updated_time}"
  local limit="${3:-100}"
  api_req GET "/folders/${folder_id}/notes?fields=${fields}&limit=${limit}&order_by=updated_time&order_dir=DESC" | pretty_json
}

cmd_folders() {
  local query="${1:-}"
  if [[ -n "$query" ]]; then
    local encoded
    encoded=$(url_encode "$query")
    api_req GET "/search?query=${encoded}&type=folder" | pretty_json
  else
    api_req GET "/folders" | pretty_json
  fi
}

cmd_tags() {
  local query="${1:-}"
  if [[ -n "$query" ]]; then
    local encoded
    encoded=$(url_encode "$query")
    api_req GET "/search?query=${encoded}&type=tag" | pretty_json
  else
    api_req GET "/tags" | pretty_json
  fi
}

cmd_tree() {
  # Print folder hierarchy as a tree
  local raw
  raw=$(api_req GET "/folders")

  python3 -c "
import json, sys

raw = json.loads(sys.stdin.read())
# Handle both raw array and {items: [...]} wrapper
if isinstance(raw, list):
    folders = raw
elif isinstance(raw, dict) and 'items' in raw:
    folders = raw['items']
else:
    folders = []

# Build lookup
by_id = {f['id']: f for f in folders}
# Find roots (parent_id not in by_id or empty)
roots = []
for f in folders:
    pid = f.get('parent_id', '')
    if not pid or pid not in by_id:
        roots.append(f)

def print_tree(items, prefix=''):
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = '└── ' if is_last else '├── '
        print(f\"{prefix}{connector}{item['title']} ({item['id'][:8]}...)\")
        # Find children
        children = [f for f in folders if f.get('parent_id') == item['id']]
        children.sort(key=lambda x: x.get('title', ''))
        extension = '    ' if is_last else '│   '
        if children:
            print_tree(children, prefix + extension)

roots.sort(key=lambda x: x.get('title', ''))
print_tree(roots)
" <<< "$raw"
}

# ── Main ───────────────────────────────────────────────────

usage() {
  echo "Usage: joplin.sh <command> [args...]" >&2
  echo "Commands:" >&2
  echo "  ping                                  Test connection" >&2
  echo "  get <note_id> [fields]                Get a note (JSON)" >&2
  echo "  note <note_id>                        Friendly note display (title + body preview)" >&2
  echo "  create <folder_id> <title> <body_file> Create a note in folder" >&2
  echo "  update <note_id> <body_file>          Update note body from file" >&2
  echo "  delete <note_id> [--permanent]        Delete note (soft delete by default)" >&2
  echo "  search <query> [fields] [limit]       Search notes" >&2
  echo "  list <folder_id> [fields] [limit]     List notes in folder" >&2
  echo "  folders [query]                       List/search folders" >&2
  echo "  tags [query]                          List/search tags" >&2
  echo "  tree                                  Print folder tree" >&2
  exit 1
}

if [[ $# -lt 1 ]]; then
  usage
fi

cmd="$1"
shift

case "$cmd" in
  ping)     cmd_ping ;;
  get)      [[ $# -ge 1 ]] || usage; cmd_get "$@" ;;
  note)     [[ $# -ge 1 ]] || usage; cmd_note "$1" ;;
  create)   [[ $# -ge 3 ]] || usage; cmd_create "$@" ;;
  update)   [[ $# -ge 2 ]] || usage; cmd_update "$@" ;;
  delete)   [[ $# -ge 1 ]] || usage; cmd_delete "$@" ;;
  search)   [[ $# -ge 1 ]] || usage; cmd_search "$@" ;;
  list)     [[ $# -ge 1 ]] || usage; cmd_list "$@" ;;
  folders)  cmd_folders "${1:-}" ;;
  tags)     cmd_tags "${1:-}" ;;
  tree)     cmd_tree ;;
  *)        echo "Unknown command: $cmd" >&2; exit 1 ;;
esac
