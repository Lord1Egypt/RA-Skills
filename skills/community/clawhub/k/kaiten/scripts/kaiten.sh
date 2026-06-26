#!/usr/bin/env bash
# Kaiten API CLI wrapper
# Requires: KAITEN_TOKEN and KAITEN_DOMAIN env vars
set -euo pipefail

BASE="https://${KAITEN_DOMAIN}/api/latest"
AUTH="Authorization: Bearer ${KAITEN_TOKEN}"

_get()  { curl -sf -H "$AUTH" "$BASE$1"; }
_post() { curl -sf -H "$AUTH" -H "Content-Type: application/json" -X POST -d "$2" "$BASE$1"; }
_patch(){ curl -sf -H "$AUTH" -H "Content-Type: application/json" -X PATCH -d "$2" "$BASE$1"; }
_del()  { curl -sf -H "$AUTH" -X DELETE "$BASE$1"; }

_fmt() { python3 -m json.tool 2>/dev/null || cat; }

# State management
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_FILE="$SCRIPT_DIR/kaiten-state.json"

_read_state() { python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('$1') or '')" 2>/dev/null || echo ""; }

_update_state() {
  python3 -c "
import json, sys
f='$STATE_FILE'
try:
    d=json.load(open(f))
except:
    d={}
d[sys.argv[1]]=int(sys.argv[2]) if sys.argv[2].isdigit() else sys.argv[2]
json.dump(d, open(f,'w'), indent=2)
" "$1" "$2"
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  state)
    cat "$STATE_FILE" | _fmt
    ;;
  set-default-space)
    [[ -z "${1:-}" ]] && { echo "Usage: set-default-space <space_id>"; exit 1; }
    _update_state "default_space_id" "$1"
    echo "Default space set to $1"
    ;;
  set-default-board)
    [[ -z "${1:-}" ]] && { echo "Usage: set-default-board <board_id>"; exit 1; }
    _update_state "default_board_id" "$1"
    echo "Default board set to $1"
    ;;
  spaces)
    _get "/spaces" | _fmt
    ;;
  boards)
    [[ -z "${1:-}" ]] && { echo "Usage: boards <space_id>"; exit 1; }
    _update_state "last_space_id" "$1"
    _get "/spaces/$1/boards" | _fmt
    ;;
  board)
    [[ -z "${1:-}" ]] && { echo "Usage: board <board_id>"; exit 1; }
    _update_state "last_board_id" "$1"
    _get "/boards/$1" | _fmt
    ;;
  columns)
    [[ -z "${1:-}" ]] && { echo "Usage: columns <board_id>"; exit 1; }
    _update_state "last_board_id" "$1"
    _get "/boards/$1/columns" | _fmt
    ;;
  lanes)
    [[ -z "${1:-}" ]] && { echo "Usage: lanes <board_id>"; exit 1; }
    _update_state "last_board_id" "$1"
    _get "/boards/$1/lanes" | _fmt
    ;;
  cards)
    limit="${1:-20}"
    offset="${2:-0}"
    _get "/cards?limit=$limit&offset=$offset" | _fmt
    ;;
  card)
    [[ -z "${1:-}" ]] && { echo "Usage: card <card_id>"; exit 1; }
    _get "/cards/$1" | _fmt
    ;;
  search)
    [[ -z "${1:-}" ]] && { echo "Usage: search <query>"; exit 1; }
    query=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1")
    _get "/search?query=$query" | _fmt
    ;;
  create-card)
    [[ -z "${4:-}" ]] && { echo "Usage: create-card <board_id> <column_id> <lane_id> <title> [description]"; exit 1; }
    board_id="$1"; col_id="$2"; lane_id="$3"; title="$4"; desc="${5:-}"
    _update_state "last_board_id" "$board_id"
    _update_state "last_column_id" "$col_id"
    _update_state "last_lane_id" "$lane_id"
    body=$(python3 -c "
import json, sys
d = {'title': sys.argv[1], 'board_id': int(sys.argv[2]), 'column_id': int(sys.argv[3]), 'lane_id': int(sys.argv[4])}
if len(sys.argv) > 5 and sys.argv[5]: d['description'] = sys.argv[5]
print(json.dumps(d))
" "$title" "$board_id" "$col_id" "$lane_id" "$desc")
    _post "/cards" "$body" | _fmt
    ;;
  update-card)
    [[ -z "${2:-}" ]] && { echo "Usage: update-card <card_id> '{\"field\":\"value\"}'"; exit 1; }
    _patch "/cards/$1" "$2" | _fmt
    ;;
  move-card)
    [[ -z "${4:-}" ]] && { echo "Usage: move-card <card_id> <board_id> <column_id> <lane_id>"; exit 1; }
    body="{\"board_id\":$2,\"column_id\":$3,\"lane_id\":$4}"
    _patch "/cards/$1/location" "$body" | _fmt
    ;;
  delete-card)
    [[ -z "${1:-}" ]] && { echo "Usage: delete-card <card_id>"; exit 1; }
    _del "/cards/$1"
    echo "Deleted card $1"
    ;;
  comment)
    [[ -z "${2:-}" ]] && { echo "Usage: comment <card_id> <text>"; exit 1; }
    body=$(python3 -c "import json,sys; print(json.dumps({'text': sys.argv[1]}))" "$2")
    _post "/cards/$1/comments" "$body" | _fmt
    ;;
  tags)
    _get "/tags" | _fmt
    ;;
  add-tag)
    [[ -z "${2:-}" ]] && { echo "Usage: add-tag <card_id> <tag_id>"; exit 1; }
    _post "/cards/$1/tags" "{\"tag_id\":$2}" | _fmt
    ;;
  remove-tag)
    [[ -z "${2:-}" ]] && { echo "Usage: remove-tag <card_id> <tag_id>"; exit 1; }
    _del "/cards/$1/tags/$2"
    echo "Removed tag $2 from card $1"
    ;;
  users)
    _get "/users" | _fmt
    ;;
  me)
    _get "/users/current" | _fmt
    ;;
  members)
    [[ -z "${1:-}" ]] && { echo "Usage: members <card_id>"; exit 1; }
    _get "/cards/$1/members" | _fmt
    ;;
  add-member)
    [[ -z "${2:-}" ]] && { echo "Usage: add-member <card_id> <user_id>"; exit 1; }
    _post "/cards/$1/members" "{\"user_id\":$2}" | _fmt
    ;;
  remove-member)
    [[ -z "${2:-}" ]] && { echo "Usage: remove-member <card_id> <member_id>"; exit 1; }
    _del "/cards/$1/members/$2"
    echo "Removed member $2 from card $1"
    ;;
  checklists)
    [[ -z "${1:-}" ]] && { echo "Usage: checklists <card_id>"; exit 1; }
    _get "/cards/$1/checklists" | _fmt
    ;;
  create-checklist)
    [[ -z "${2:-}" ]] && { echo "Usage: create-checklist <card_id> <name>"; exit 1; }
    body=$(python3 -c "import json,sys; print(json.dumps({'name': sys.argv[1]}))" "$2")
    _post "/cards/$1/checklists" "$body" | _fmt
    ;;
  add-checklist-item)
    [[ -z "${3:-}" ]] && { echo "Usage: add-checklist-item <card_id> <checklist_id> <text>"; exit 1; }
    body=$(python3 -c "import json,sys; print(json.dumps({'text': sys.argv[1]}))" "$3")
    _post "/cards/$1/checklists/$2/items" "$body" | _fmt
    ;;
  toggle-checklist-item)
    [[ -z "${3:-}" ]] && { echo "Usage: toggle-checklist-item <card_id> <checklist_id> <item_id>"; exit 1; }
    # Toggle checked state
    _patch "/cards/$1/checklists/$2/items/$3" '{"checked":true}' | _fmt
    ;;
  log-time)
    [[ -z "${2:-}" ]] && { echo "Usage: log-time <card_id> <minutes> [comment]"; exit 1; }
    body=$(python3 -c "
import json, sys
d = {'time_spent': int(sys.argv[1])}
if len(sys.argv) > 2 and sys.argv[2]: d['comment'] = sys.argv[2]
print(json.dumps(d))
" "$2" "${3:-}")
    _post "/cards/$1/time" "$body" | _fmt
    ;;
  time-logs)
    [[ -z "${1:-}" ]] && { echo "Usage: time-logs <card_id>"; exit 1; }
    _get "/cards/$1/time" | _fmt
    ;;
  files)
    [[ -z "${1:-}" ]] && { echo "Usage: files <card_id>"; exit 1; }
    _get "/cards/$1/files" | _fmt
    ;;
  children)
    [[ -z "${1:-}" ]] && { echo "Usage: children <card_id>"; exit 1; }
    _get "/cards/$1/children" | _fmt
    ;;
  help|*)
    cat << 'HELP'
Kaiten CLI — Usage: kaiten.sh <command> [args]

STATE:
  state                          Show current state (defaults + last used)
  set-default-space <space_id>   Set default space
  set-default-board <board_id>   Set default board

READ:
  spaces                         List all spaces
  boards <space_id>              List boards in a space
  board <board_id>               Get board details
  columns <board_id>             List columns on a board
  lanes <board_id>               List lanes on a board
  cards [limit] [offset]         List cards (default: 20, 0)
  card <card_id>                 Get card details
  search <query>                 Search cards
  tags                           List all tags
  users                          List all users
  me                             Current user info
  members <card_id>              List card members
  checklists <card_id>           List card checklists
  time-logs <card_id>            List time logs
  files <card_id>                List card files
  children <card_id>             List child cards

WRITE:
  create-card <board> <col> <lane> <title> [desc]
  update-card <card_id> '{"field":"value"}'
  move-card <card_id> <board> <col> <lane>
  delete-card <card_id>
  comment <card_id> <text>
  add-tag <card_id> <tag_id>
  remove-tag <card_id> <tag_id>
  add-member <card_id> <user_id>
  remove-member <card_id> <member_id>
  create-checklist <card_id> <name>
  add-checklist-item <card_id> <cl_id> <text>
  toggle-checklist-item <card_id> <cl_id> <item_id>
  log-time <card_id> <minutes> [comment]
HELP
    ;;
esac
