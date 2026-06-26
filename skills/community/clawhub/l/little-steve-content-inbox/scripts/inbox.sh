#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DB="$BASE_DIR/data/items.json"
VIEW_STATE="$BASE_DIR/data/view-state.json"
MEDIA_DIR="$BASE_DIR/data/media"
DEFAULT_LIMIT=10

# ── init ──────────────────────────────────────────────

init_db(){
  if [[ ! -f "$DB" ]]; then
    mkdir -p "$(dirname "$DB")"
    cat > "$DB" <<JSON
{"items":[],"nextId":1}
JSON
    chmod 600 "$DB"
  fi
  if [[ ! -f "$VIEW_STATE" ]]; then
    cat > "$VIEW_STATE" <<JSON
{"lastStatus":"all","lastOffset":0,"lastLimit":10}
JSON
    chmod 600 "$VIEW_STATE"
  fi
  mkdir -p "$MEDIA_DIR"
}

require_jq(){
  command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 1; }
}

# ── validators ────────────────────────────────────────

validate_id(){
  [[ "$1" =~ ^[0-9]+$ ]] || { echo "error: invalid id (must be positive integer): $1" >&2; exit 1; }
}

validate_type(){
  case "$1" in
    link|note|image|video) ;;
    "") ;;
    *) echo "error: invalid type (allow: link|note|image|video): $1" >&2; exit 1 ;;
  esac
}

validate_status(){
  case "$1" in
    unread|read|starred) ;;
    "") ;;
    *) echo "error: invalid status (allow: unread|read|starred): $1" >&2; exit 1 ;;
  esac
}

validate_title(){
  if [[ ${#1} -gt 500 ]]; then
    echo "error: --title exceeds 500 char limit" >&2; exit 1
  fi
}

validate_content(){
  if [[ ${#1} -gt 5000 ]]; then
    echo "error: --content exceeds 5000 char limit" >&2; exit 1
  fi
}

validate_url(){
  [[ -z "$1" ]] && return 0
  if ! [[ "$1" =~ ^https?:// ]]; then
    echo "error: --url must start with http:// or https://" >&2; exit 1
  fi
  if [[ ${#1} -gt 2000 ]]; then
    echo "error: --url exceeds 2000 char limit" >&2; exit 1
  fi
}

validate_tags(){
  [[ -z "$1" ]] && return 0
  if ! [[ "$1" =~ ^[a-zA-Z0-9_,\ -]+$ ]]; then
    echo "error: --tags contains invalid characters (allow: alphanumeric, hyphen, underscore, comma)" >&2
    exit 1
  fi
  if [[ ${#1} -gt 200 ]]; then
    echo "error: --tags exceeds 200 char limit" >&2; exit 1
  fi
}

# ── helpers ───────────────────────────────────────────

save_view_state(){
  local status="$1" offset="$2" limit="$3"
  jq -n --arg s "$status" --argjson o "$offset" --argjson l "$limit" \
    '{lastStatus:$s, lastOffset:$o, lastLimit:$l}' > "$VIEW_STATE"
}

item_exists(){
  local id="$1"
  jq -e --argjson id "$id" '.items | any(.id == $id)' "$DB" >/dev/null 2>&1
}

# extract domain from URL for source field
extract_source(){
  local url="$1"
  [[ -z "$url" ]] && echo "" && return
  echo "$url" | sed -E 's|^https?://([^/]+).*|\1|' | sed 's/^www\.//'
}

# ── cmd: add ──────────────────────────────────────────

cmd_add(){
  local type="" title="" content="" url="" media_path="" tags=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --type) [[ $# -ge 2 ]] || { echo "error: missing value for --type" >&2; exit 1; }; type="$2"; shift 2 ;;
      --title) [[ $# -ge 2 ]] || { echo "error: missing value for --title" >&2; exit 1; }; title="$2"; shift 2 ;;
      --content) [[ $# -ge 2 ]] || { echo "error: missing value for --content" >&2; exit 1; }; content="$2"; shift 2 ;;
      --url) [[ $# -ge 2 ]] || { echo "error: missing value for --url" >&2; exit 1; }; url="$2"; shift 2 ;;
      --media-path) [[ $# -ge 2 ]] || { echo "error: missing value for --media-path" >&2; exit 1; }; media_path="$2"; shift 2 ;;
      --tags) [[ $# -ge 2 ]] || { echo "error: missing value for --tags" >&2; exit 1; }; tags="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  # auto-detect type if not provided
  if [[ -z "$type" ]]; then
    if [[ -n "$url" ]]; then
      type="link"
    elif [[ -n "$media_path" ]]; then
      type="image"
    else
      type="note"
    fi
  fi

  validate_type "$type"
  [[ -n "$title" ]] || { echo "error: missing --title" >&2; exit 1; }
  validate_title "$title"
  [[ -z "$content" ]] || validate_content "$content"
  validate_url "$url"
  validate_tags "$tags"

  if [[ "$type" == "link" && -z "$url" ]]; then
    echo "error: --url is required for type=link" >&2; exit 1
  fi
  if [[ "$type" == "image" && -z "$media_path" ]]; then
    echo "error: --media-path is required for type=image" >&2; exit 1
  fi

  local now id source
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  id=$(jq -r '.nextId' "$DB")
  source=$(extract_source "$url")

  jq --arg type "$type" \
     --arg title "$title" \
     --arg content "$content" \
     --arg url "$url" \
     --arg mediaPath "$media_path" \
     --arg source "$source" \
     --arg tags "$tags" \
     --arg now "$now" \
     --argjson id "$id" '
    .items += [{
      id: $id,
      type: $type,
      title: $title,
      content: (if $content == "" then null else $content end),
      url: (if $url == "" then null else $url end),
      mediaPath: (if $mediaPath == "" then null else $mediaPath end),
      source: (if $source == "" then null else $source end),
      status: "unread",
      tags: ($tags | split(",") | map(gsub("^[[:space:]]+|[[:space:]]+$";"") | select(length>0))),
      createdAt: $now,
      updatedAt: $now,
      readAt: null
    }] |
    .nextId += 1
  ' "$DB" > "$DB.tmp" && mv "$DB.tmp" "$DB"
  echo "added #$id [$type] $title"
}

# ── cmd: list ─────────────────────────────────────────

cmd_list(){
  local status="all" offset=0 limit=$DEFAULT_LIMIT
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --status) [[ $# -ge 2 ]] || { echo "error: missing value for --status" >&2; exit 1; }; status="$2"; shift 2 ;;
      --offset) [[ $# -ge 2 ]] || { echo "error: missing value for --offset" >&2; exit 1; }; offset="$2"; shift 2 ;;
      --limit) [[ $# -ge 2 ]] || { echo "error: missing value for --limit" >&2; exit 1; }; limit="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  if [[ "$status" != "all" ]]; then
    validate_status "$status"
  fi
  [[ "$offset" =~ ^[0-9]+$ ]] || { echo "error: --offset must be non-negative integer" >&2; exit 1; }
  [[ "$limit" =~ ^[0-9]+$ ]] || { echo "error: --limit must be positive integer" >&2; exit 1; }

  save_view_state "$status" "$offset" "$limit"

  local result
  result=$(jq -r --arg status "$status" --argjson offset "$offset" --argjson limit "$limit" '
    .items
    | (if $status == "all" then . else map(select(.status == $status)) end)
    | sort_by(.createdAt) | reverse
    | . as $all
    | .[$offset:$offset+$limit]
    | if length == 0 then "NO_ITEMS"
      else
        (map(
          "[\(.status)][\(.type)] #\(.id) \(.title)"
        ) | join("\n")) +
        (if ($offset + $limit) < ($all | length)
         then "\n-- more: \($all | length) total, showing \($offset+1)-\([$offset+$limit, ($all|length)] | min) --"
         else "\n-- end: \($all | length) total --"
         end)
      end
  ' "$DB")

  echo "$result"
}

# ── cmd: more ─────────────────────────────────────────

cmd_more(){
  local last_status last_offset last_limit next_offset
  last_status=$(jq -r '.lastStatus' "$VIEW_STATE")
  last_offset=$(jq -r '.lastOffset' "$VIEW_STATE")
  last_limit=$(jq -r '.lastLimit' "$VIEW_STATE")
  next_offset=$((last_offset + last_limit))
  cmd_list --status "$last_status" --offset "$next_offset" --limit "$last_limit"
}

# ── cmd: view ─────────────────────────────────────────

cmd_view(){
  local id=""
  if [[ "${1:-}" == "--id" ]]; then
    [[ $# -ge 2 ]] || { echo "error: missing value for --id" >&2; exit 1; }
    id="$2"
  else
    id="${1:-}"
  fi
  [[ -n "$id" ]] || { echo "usage: inbox.sh view --id <id>" >&2; exit 1; }
  validate_id "$id"

  if ! item_exists "$id"; then
    echo "error: item #$id not found" >&2; exit 1
  fi

  jq -r --argjson id "$id" '
    .items[] | select(.id == $id) |
    "Type: \(.type)\nTitle: \(.title)\nStatus: \(.status)" +
    (if .content then "\nContent: \(.content)" else "" end) +
    (if .url then "\nURL: \(.url)" else "" end) +
    (if .mediaPath then "\nMedia: \(.mediaPath)" else "" end) +
    (if .source then "\nSource: \(.source)" else "" end) +
    "\nCreated: \(.createdAt)\nUpdated: \(.updatedAt)" +
    (if .readAt then "\nRead at: \(.readAt)" else "" end) +
    (if (.tags | length) > 0 then "\nTags: \(.tags | join(", "))" else "" end)
  ' "$DB"
}

# ── cmd: status ───────────────────────────────────────

cmd_status(){
  local id="" status=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) [[ $# -ge 2 ]] || { echo "error: missing value for --id" >&2; exit 1; }; id="$2"; shift 2 ;;
      --status) [[ $# -ge 2 ]] || { echo "error: missing value for --status" >&2; exit 1; }; status="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$id" ]] || { echo "error: missing --id" >&2; exit 1; }
  [[ -n "$status" ]] || { echo "error: missing --status" >&2; exit 1; }
  validate_id "$id"
  validate_status "$status"

  if ! item_exists "$id"; then
    echo "error: item #$id not found" >&2; exit 1
  fi

  local now
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  jq --argjson id "$id" --arg status "$status" --arg now "$now" '
    .items |= map(if .id == $id then
      .status = $status |
      .updatedAt = $now |
      (if $status == "read" then .readAt = $now else . end)
    else . end)
  ' "$DB" > "$DB.tmp" && mv "$DB.tmp" "$DB"
  echo "updated #$id -> $status"
}

# ── cmd: delete ───────────────────────────────────────

cmd_delete(){
  local id=""
  if [[ "${1:-}" == "--id" ]]; then
    [[ $# -ge 2 ]] || { echo "error: missing value for --id" >&2; exit 1; }
    id="$2"
  else
    id="${1:-}"
  fi
  [[ -n "$id" ]] || { echo "usage: inbox.sh delete --id <id>" >&2; exit 1; }
  validate_id "$id"

  if ! item_exists "$id"; then
    echo "error: item #$id not found" >&2; exit 1
  fi

  jq --argjson id "$id" '.items |= map(select(.id != $id))' "$DB" > "$DB.tmp" && mv "$DB.tmp" "$DB"
  echo "deleted #$id"
}

# ── main ──────────────────────────────────────────────

main(){
  require_jq
  init_db
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    add)    cmd_add "$@" ;;
    list)   cmd_list "$@" ;;
    more)   cmd_more ;;
    view)   cmd_view "$@" ;;
    status) cmd_status "$@" ;;
    delete) cmd_delete "$@" ;;
    *) echo "usage: inbox.sh {add|list|more|view|status|delete}" >&2; exit 1 ;;
  esac
}

main "$@"
