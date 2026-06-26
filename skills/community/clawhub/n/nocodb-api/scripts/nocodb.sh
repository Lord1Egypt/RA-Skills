#!/usr/bin/env bash
###############################################################################
# nc - NocoDB v3 CLI for OpenClaw
###############################################################################
set -euo pipefail

NC_URL="${NOCODB_URL:-https://app.nocodb.com}"
NC_TOKEN="${NOCODB_TOKEN:-}"
NC_VERBOSE="${NOCODB_VERBOSE:-0}"

[[ -z "$NC_TOKEN" ]] && { echo "NOCODB_TOKEN required" >&2; exit 1; }

_v() { [[ "$NC_VERBOSE" == "1" ]] && echo "→ $*" >&2 || true; }

_get()    { curl -sS -H "xc-token: $NC_TOKEN" "$NC_URL/api/v3/$1"; }
_post()   { curl -sS -X POST -H "xc-token: $NC_TOKEN" -H "Content-Type: application/json" "$NC_URL/api/v3/$1" -d "${2:-}"; }
_patch()  { curl -sS -X PATCH -H "xc-token: $NC_TOKEN" -H "Content-Type: application/json" "$NC_URL/api/v3/$1" -d "${2:-}"; }
_put()    { curl -sS -X PUT -H "xc-token: $NC_TOKEN" -H "Content-Type: application/json" "$NC_URL/api/v3/$1" -d "${2:-}"; }
_delete() { curl -sS -X DELETE -H "xc-token: $NC_TOKEN" -H "Content-Type: application/json" "$NC_URL/api/v3/$1" ${2:+-d "$2"}; }
_upload() { curl -sS -X POST -H "xc-token: $NC_TOKEN" -F "file=@$2" "$NC_URL/api/v3/$1"; }

_enc() {
    local s="$1" o="" c
    for ((i=0; i<${#s}; i++)); do c="${s:i:1}"; [[ "$c" =~ [a-zA-Z0-9._~-] ]] && o+="$c" || o+=$(printf '%%%02X' "'$c"); done
    echo "$o"
}

_jqf() { jq -r --arg n "$2" '.[]|select(.title|ascii_downcase==($n|ascii_downcase))|.id' <<< "$1" | head -1; }

_err() { echo "error: $1" >&2; exit 1; }

_is_ws_id()   { [[ "$1" =~ ^w[a-z0-9]+$ ]]; }
_is_base_id() { [[ "$1" =~ ^p[a-z0-9]+$ ]]; }
_is_tbl_id()  { [[ "$1" =~ ^m[a-z0-9]+$ ]]; }
_is_view_id() { [[ "$1" =~ ^vw[a-z0-9]+$ ]]; }
_is_fld_id()  { [[ "$1" =~ ^c[a-z0-9]+$ ]]; }

_ws() {
    if _is_ws_id "$1"; then
        _v "workspace: $1"; echo "$1"; return
    fi
    local r; r=$(_jqf "$(_get meta/workspaces | jq -c .list)" "$1")
    [[ -n "$r" ]] && { _v "workspace: $1 → $r"; echo "$r"; } || { echo "workspace not found: $1" >&2; exit 1; }
}

_base() {
    if _is_base_id "$1"; then
        _v "base: $1"; echo "$1"; return
    fi
    local wl bl r; wl=$(_get meta/workspaces | jq -c .list)
    for w in $(jq -r '.[].id' <<< "$wl"); do
        bl=$(_get "meta/workspaces/$w/bases" | jq -c .list)
        r=$(_jqf "$bl" "$1"); [[ -n "$r" ]] && { _v "base: $1 → $r"; echo "$r"; return; }
    done
    echo "base not found: $1" >&2; exit 1
}

_tbl() {
    if _is_tbl_id "$2"; then
        _v "table: $2"; echo "$2"; return
    fi
    local r; r=$(_jqf "$(_get "meta/bases/$1/tables" | jq -c .list)" "$2")
    [[ -n "$r" ]] && { _v "table: $2 → $r"; echo "$r"; } || { echo "table not found: $2" >&2; exit 1; }
}

_view() {
    if _is_view_id "$3"; then
        _v "view: $3"; echo "$3"; return
    fi
    local r; r=$(_jqf "$(_get "meta/bases/$1/tables/$2/views" | jq -c .list)" "$3")
    [[ -n "$r" ]] && { _v "view: $3 → $r"; echo "$r"; } || { echo "view not found: $3" >&2; exit 1; }
}

_fld() {
    if _is_fld_id "$3"; then
        _v "field: $3"; echo "$3"; return
    fi
    local r; r=$(_get "meta/bases/$1/tables/$2" | jq -r --arg n "$3" '.fields[]|select(.title|ascii_downcase==($n|ascii_downcase))|.id' | head -1)
    [[ -n "$r" ]] && { _v "field: $3 → $r"; echo "$r"; } || { echo "field not found: $3" >&2; exit 1; }
}

cmd=$1; shift || true

case "$cmd" in
workspace:list) _get meta/workspaces | jq -r '.list[]|[.title,.id]|@tsv' ;;
workspace:get) _get "meta/workspaces/$(_ws "$1")" | jq . ;;
workspace:create) _post meta/workspaces "$1" | jq . ;;
workspace:update) _patch "meta/workspaces/$(_ws "$1")" "$2" | jq . ;;
workspace:delete) _delete "meta/workspaces/$(_ws "$1")" | jq . ;;
workspace:members) _get "meta/workspaces/$(_ws "$1")?include[]=members" | jq .members ;;
workspace:members:add) _post "meta/workspaces/$(_ws "$1")/members" "$2" | jq . ;;
workspace:members:update) _patch "meta/workspaces/$(_ws "$1")/members" "$2" | jq . ;;
workspace:members:remove) _delete "meta/workspaces/$(_ws "$1")/members" "$2" | jq . ;;

base:list) _get "meta/workspaces/$(_ws "$1")/bases" | jq -r '.list[]|[.title,.id]|@tsv' ;;
base:get) _get "meta/bases/$(_base "$1")" | jq . ;;
base:create) _post "meta/workspaces/$(_ws "$1")/bases" "$2" | jq . ;;
base:update) _patch "meta/bases/$(_base "$1")" "$2" | jq . ;;
base:delete) _delete "meta/bases/$(_base "$1")" | jq . ;;
base:members) _get "meta/bases/$(_base "$1")?include[]=members" | jq .members ;;
base:members:add) _post "meta/bases/$(_base "$1")/members" "$2" | jq . ;;
base:members:update) _patch "meta/bases/$(_base "$1")/members" "$2" | jq . ;;
base:members:remove) _delete "meta/bases/$(_base "$1")/members" "$2" | jq . ;;

table:list) b=$(_base "$1"); _get "meta/bases/$b/tables" | jq -r '.list[]|[.title,.id]|@tsv' ;;
table:get) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _get "meta/bases/$b/tables/$t" | jq . ;;
table:create) _post "meta/bases/$(_base "$1")/tables" "$2" | jq . ;;
table:update) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _patch "meta/bases/$b/tables/$t" "$3" | jq . ;;
table:delete) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _delete "meta/bases/$b/tables/$t" | jq . ;;

field:list) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _get "meta/bases/$b/tables/$t" | jq -r '.fields[]|[.title,.type,.id]|@tsv' ;;
field:get) b=$(_base "$1"); t=$(_tbl "$b" "$2"); f=$(_fld "$b" "$t" "$3"); _get "meta/bases/$b/fields/$f" | jq . ;;
field:create) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _post "meta/bases/$b/tables/$t/fields" "$3" | jq . ;;
field:update) b=$(_base "$1"); t=$(_tbl "$b" "$2"); f=$(_fld "$b" "$t" "$3"); _patch "meta/bases/$b/fields/$f" "$4" | jq . ;;
field:delete) b=$(_base "$1"); t=$(_tbl "$b" "$2"); f=$(_fld "$b" "$t" "$3"); _delete "meta/bases/$b/fields/$f" | jq . ;;

view:list) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _get "meta/bases/$b/tables/$t/views" | jq -r '.list[]|[.title,.type,.id]|@tsv' ;;
view:get) b=$(_base "$1"); t=$(_tbl "$b" "$2"); v=$(_view "$b" "$t" "$3"); _get "meta/bases/$b/views/$v" | jq . ;;
view:create) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _post "meta/bases/$b/tables/$t/views" "$3" | jq . ;;
view:update) b=$(_base "$1"); t=$(_tbl "$b" "$2"); v=$(_view "$b" "$t" "$3"); _patch "meta/bases/$b/views/$v" "$4" | jq . ;;
view:delete) b=$(_base "$1"); t=$(_tbl "$b" "$2"); v=$(_view "$b" "$t" "$3"); _delete "meta/bases/$b/views/$v" | jq . ;;

filter:list) b=$(_base "$1"); t=$(_tbl "$b" "$2"); v=$(_view "$b" "$t" "$3"); _get "meta/bases/$b/views/$v/filters" | jq . ;;
filter:create) b=$(_base "$1"); t=$(_tbl "$b" "$2"); v=$(_view "$b" "$t" "$3"); _post "meta/bases/$b/views/$v/filters" "$4" | jq . ;;
filter:replace) b=$(_base "$1"); t=$(_tbl "$b" "$2"); v=$(_view "$b" "$t" "$3"); _put "meta/bases/$b/views/$v/filters" "$4" | jq . ;;
filter:update) _patch "meta/bases/$(_base "$1")/filters/$2" "$3" | jq . ;;
filter:delete) _delete "meta/bases/$(_base "$1")/filters/$2" | jq . ;;

sort:list) b=$(_base "$1"); t=$(_tbl "$b" "$2"); v=$(_view "$b" "$t" "$3"); _get "meta/bases/$b/views/$v/sorts" | jq . ;;
sort:create) b=$(_base "$1"); t=$(_tbl "$b" "$2"); v=$(_view "$b" "$t" "$3"); _post "meta/bases/$b/views/$v/sorts" "$4" | jq . ;;
sort:update) _patch "meta/bases/$(_base "$1")/sorts/$2" "$3" | jq . ;;
sort:delete) _delete "meta/bases/$(_base "$1")/sorts/$2" | jq . ;;

record:list)
    b=$(_base "$1"); t=$(_tbl "$b" "$2")
    pg="${3:-1}"; sz="${4:-25}"; wh="${5:-}"; so="${6:-}"; fl="${7:-}"; vi="${8:-}"
    q="page=$pg&pageSize=$sz"
    [[ -n "$wh" ]] && q+="&where=$(_enc "$wh")"
    [[ -n "$so" ]] && q+="&sort=$(_enc "$so")"
    [[ -n "$fl" ]] && q+="&fields=$(_enc "$fl")"
    [[ -n "$vi" ]] && q+="&viewId=$vi"
    _get "data/$b/$t/records?$q" | jq .records
    ;;
record:get)
    b=$(_base "$1"); t=$(_tbl "$b" "$2")
    q=""; [[ -n "${4:-}" ]] && q="?fields=$(_enc "$4")"
    _get "data/$b/$t/records/$3$q" | jq .
    ;;
record:create) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _post "data/$b/$t/records" "$3" | jq . ;;
record:update) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _patch "data/$b/$t/records" "[{\"id\":$3,\"fields\":$4}]" | jq '.records[0]' ;;
record:update-many) b=$(_base "$1"); t=$(_tbl "$b" "$2"); _patch "data/$b/$t/records" "$3" | jq . ;;
record:delete)
    b=$(_base "$1"); t=$(_tbl "$b" "$2")
    if [[ "$3" =~ ^\[ ]]; then
        if echo "$3" | jq -e '.[0].id' >/dev/null 2>&1; then ids="$3"
        elif echo "$3" | jq -e '.[0]|type == "string"' >/dev/null 2>&1; then
            ids=$(echo "$3" | jq '[.[]|{id:.}]')
        else _err "array must contain strings or objects with 'id' field"; fi
    else ids="[{\"id\":\"$3\"}]"; fi
    _delete "data/$b/$t/records" "$ids" | jq .
    ;;
record:count)
    b=$(_base "$1"); t=$(_tbl "$b" "$2")
    q=""; [[ -n "${3:-}" ]] && q="where=$(_enc "$3")"; [[ -n "${4:-}" ]] && q+="${q:+&}viewId=$4"
    _get "data/$b/$t/count${q:+?$q}" | jq -r .count
    ;;

link:list)
    b=$(_base "$1"); t=$(_tbl "$b" "$2"); f=$(_fld "$b" "$t" "$3")
    pg="${5:-1}"; sz="${6:-25}"; wh="${7:-}"; so="${8:-}"; fl="${9:-}"
    q="page=$pg&pageSize=$sz"
    [[ -n "$wh" ]] && q+="&where=$(_enc "$wh")"
    [[ -n "$so" ]] && q+="&sort=$(_enc "$so")"
    [[ -n "$fl" ]] && q+="&fields=$(_enc "$fl")"
    _get "data/$b/$t/links/$f/$4?$q" | jq .
    ;;
link:add) b=$(_base "$1"); t=$(_tbl "$b" "$2"); f=$(_fld "$b" "$t" "$3"); _post "data/$b/$t/links/$f/$4" "$5" | jq . ;;
link:remove) b=$(_base "$1"); t=$(_tbl "$b" "$2"); f=$(_fld "$b" "$t" "$3"); _delete "data/$b/$t/links/$f/$4" "$5" | jq . ;;

attachment:upload) b=$(_base "$1"); t=$(_tbl "$b" "$2"); f=$(_fld "$b" "$t" "$4"); _upload "data/$b/$t/records/$3/fields/$f/upload" "$5" | jq . ;;

action:trigger) b=$(_base "$1"); t=$(_tbl "$b" "$2"); f=$(_fld "$b" "$t" "$3"); _post "data/$b/$t/actions/$f" "{\"recordId\":\"$4\"}" | jq . ;;

script:list) _get "meta/bases/$(_base "$1")/scripts" | jq -r '.list[]|[.title,.id]|@tsv' ;;
script:get) _get "meta/bases/$(_base "$1")/scripts/$2" | jq . ;;
script:create) _post "meta/bases/$(_base "$1")/scripts" "$2" | jq . ;;
script:update) _patch "meta/bases/$(_base "$1")/scripts/$2" "$3" | jq . ;;
script:delete) _delete "meta/bases/$(_base "$1")/scripts/$2" | jq . ;;

team:list) _get "meta/workspaces/$(_ws "$1")/teams" | jq -r '.list[]|[.title,.id]|@tsv' ;;
team:get) _get "meta/workspaces/$(_ws "$1")/teams/$2" | jq . ;;
team:create) _post "meta/workspaces/$(_ws "$1")/teams" "$2" | jq . ;;
team:update) _patch "meta/workspaces/$(_ws "$1")/teams/$2" "$3" | jq . ;;
team:delete) _delete "meta/workspaces/$(_ws "$1")/teams/$2" | jq . ;;
team:members:add) _post "meta/workspaces/$(_ws "$1")/teams/$2/members" "$3" | jq . ;;
team:members:update) _patch "meta/workspaces/$(_ws "$1")/teams/$2/members" "$3" | jq . ;;
team:members:remove) _delete "meta/workspaces/$(_ws "$1")/teams/$2/members" "$3" | jq . ;;

token:list) _get meta/tokens | jq -r '.list[]|[.title,.id]|@tsv' ;;
token:create) _post meta/tokens "$1" | jq . ;;
token:delete) _delete "meta/tokens/$1" | jq . ;;

where:help|filter:help)
    cat <<'EOF'
WHERE FILTER SYNTAX
===================
(field,operator,value)           Basic filter
(field,operator)                 No-value operators
(field,op,sub_op)                Date with sub-operator
(field,op,sub_op,value)          Date with sub-operator and value

OPERATORS:
  eq, neq, like, nlike, in, gt, lt, gte, lte
  blank, notblank, null, notnull, checked, notchecked

LOGICAL: ~and, ~or, ~not (with tilde prefix)

EXAMPLES:
  (status,eq,active)
  (name,like,%john%)
  (status,eq,active)~and(created_at,isWithin,pastWeek)
  (due_date,lt,today)~and(priority,eq,high)
EOF
    ;;

*) cat <<'EOF'
NocoDB CLI - Usage: nc <command> [args]

Workspaces:   workspace:list|get|create|update|delete|members
Bases:        base:list|get|create|update|delete|members
Tables:       table:list|get|create|update|delete
Fields:       field:list|get|create|update|delete
Views:        view:list|get|create|update|delete
Records:      record:list|get|create|update|update-many|delete|count
Links:        link:list|add|remove
Filters:      filter:list|create|replace|update|delete
Sorts:        sort:list|create|update|delete
Attachments:  attachment:upload
Scripts:      script:list|get|create|update|delete
Teams:        team:list|get|create|update|delete
Tokens:       token:list|create|delete
Help:         where:help

Env: NOCODB_TOKEN (required), NOCODB_URL (default: https://app.nocodb.com)
EOF
    ;;
esac
