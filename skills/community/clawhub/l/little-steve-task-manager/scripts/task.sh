#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DB="$BASE_DIR/data/tasks.json"

init_db(){
  if [[ ! -f "$DB" ]]; then
    mkdir -p "$(dirname "$DB")"
    cat > "$DB" <<JSON
{"tasks":[],"nextId":1}
JSON
    chmod 600 "$DB"
  fi
}

require_jq(){
  command -v jq >/dev/null 2>&1 || { echo "jq is required"; exit 1; }
}

priority_weight(){
  case "$1" in
    P0) echo 0 ;;
    P1) echo 1 ;;
    P2) echo 2 ;;
    P3) echo 3 ;;
    *) echo "error: invalid priority (allow: P0|P1|P2|P3): $1" >&2; exit 1 ;;
  esac
}

validate_status(){
  case "$1" in
    open|doing|blocked|done|cancelled) ;;
    "") ;;
    *) echo "error: invalid status (allow: open|doing|blocked|done|cancelled): $1" >&2; exit 1 ;;
  esac
}

validate_date(){
  local v="$1"
  [[ -z "$v" ]] && return 0
  [[ "$v" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || { echo "error: invalid due date (YYYY-MM-DD): $v" >&2; exit 1; }
}

validate_id(){
  [[ "$1" =~ ^[0-9]+$ ]] || { echo "error: invalid id (must be positive integer): $1" >&2; exit 1; }
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

validate_title(){
  if [[ ${#1} -gt 500 ]]; then
    echo "error: --title exceeds 500 char limit" >&2; exit 1
  fi
}

cmd_add(){
  local title="" priority="P2" due="" tags=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --title) [[ $# -ge 2 ]] || { echo "error: missing value for --title" >&2; exit 1; }; title="$2"; shift 2 ;;
      --priority) [[ $# -ge 2 ]] || { echo "error: missing value for --priority" >&2; exit 1; }; priority="$2"; shift 2 ;;
      --due) [[ $# -ge 2 ]] || { echo "error: missing value for --due" >&2; exit 1; }; due="$2"; shift 2 ;;
      --tags) [[ $# -ge 2 ]] || { echo "error: missing value for --tags" >&2; exit 1; }; tags="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$title" ]] || { echo "error: missing --title" >&2; exit 1; }
  validate_title "$title"
  priority_weight "$priority" >/dev/null
  validate_date "$due"
  validate_tags "$tags"

  local now id w
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  id=$(jq -r '.nextId' "$DB")
  w=$(priority_weight "$priority")

  jq --arg title "$title" --arg priority "$priority" --arg due "$due" --arg tags "$tags" --arg now "$now" --argjson id "$id" --argjson w "$w" '
    .tasks += [{
      id:$id,
      title:$title,
      status:"open",
      priority:$priority,
      priorityWeight:$w,
      due:$due,
      tags:($tags|split(",")|map(gsub("^[[:space:]]+|[[:space:]]+$";"")|select(length>0))),
      createdAt:$now,
      updatedAt:$now
    }] |
    .nextId += 1
  ' "$DB" > "$DB.tmp" && mv "$DB.tmp" "$DB"
  echo "added #$id"
}

cmd_update(){
  local id="" status="" priority="" due="" title=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) [[ $# -ge 2 ]] || { echo "error: missing value for --id" >&2; exit 1; }; id="$2"; shift 2 ;;
      --status) [[ $# -ge 2 ]] || { echo "error: missing value for --status" >&2; exit 1; }; status="$2"; shift 2 ;;
      --priority) [[ $# -ge 2 ]] || { echo "error: missing value for --priority" >&2; exit 1; }; priority="$2"; shift 2 ;;
      --due) [[ $# -ge 2 ]] || { echo "error: missing value for --due" >&2; exit 1; }; due="$2"; shift 2 ;;
      --title) [[ $# -ge 2 ]] || { echo "error: missing value for --title" >&2; exit 1; }; title="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$id" ]] || { echo "error: missing --id" >&2; exit 1; }
  validate_id "$id"
  validate_status "$status"
  [[ -z "$priority" ]] || priority_weight "$priority" >/dev/null
  validate_date "$due"
  [[ -z "$title" ]] || validate_title "$title"

  local now w
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  w=$( [[ -n "$priority" ]] && priority_weight "$priority" || echo 0 )

  jq --argjson id "$id" --arg status "$status" --arg priority "$priority" --arg due "$due" --arg title "$title" --arg now "$now" --argjson w "$w" '
    .tasks |= map(if .id==$id then
      .status = (if $status=="" then .status else $status end) |
      .priority = (if $priority=="" then .priority else $priority end) |
      .priorityWeight = (if $priority=="" then .priorityWeight else $w end) |
      .due = (if $due=="" then .due else $due end) |
      .title = (if $title=="" then .title else $title end) |
      .updatedAt = $now
    else . end)
  ' "$DB" > "$DB.tmp" && mv "$DB.tmp" "$DB"
  echo "updated #$id"
}

cmd_done(){
  local id=""
  if [[ "${1:-}" == "--id" ]]; then
    [[ $# -ge 2 ]] || { echo "error: missing value for --id" >&2; exit 1; }
    id="$2"
  else
    id="${1:-}"
  fi
  [[ -n "$id" ]] || { echo "usage: task.sh done --id <id>" >&2; exit 1; }
  validate_id "$id"
  cmd_update --id "$id" --status done
}

cmd_list(){
  local status=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --status) [[ $# -ge 2 ]] || { echo "error: missing value for --status" >&2; exit 1; }; status="$2"; shift 2 ;;
      *) echo "error: unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  validate_status "$status"

  jq -r --arg status "$status" '
    .tasks
    | (if $status=="" then . else map(select(.status==$status)) end)
    | sort_by(.priorityWeight, (if .due=="" then "9999-12-31" else .due end), .createdAt)
    | .[]
    | "[\(.status)][\(.priority)] #\(.id) \(.title)" +
      (if .due=="" then "" else " (due: \(.due))" end) +
      (if (.tags|length)>0 then " tags:" + (.tags|join(",")) else "" end)
  ' "$DB"
}

main(){
  require_jq
  init_db
  local cmd="${1:-}"
  shift || true
  case "$cmd" in
    add) cmd_add "$@" ;;
    update) cmd_update "$@" ;;
    done) cmd_done "$@" ;;
    list) cmd_list "$@" ;;
    *) echo "usage: task.sh {add|update|done|list}"; exit 1 ;;
  esac
}

main "$@"
