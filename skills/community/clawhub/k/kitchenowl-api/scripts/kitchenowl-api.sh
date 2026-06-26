#!/usr/bin/env bash
set -euo pipefail

SESSION_DIR="${HOME}/.config/kitchenowl-api"
SESSION_FILE="${SESSION_DIR}/session.json"

mkdir -p "$SESSION_DIR"

# Preferred vars requested by user: KITCHENOWL_URL + KITCHENOWL_TOKEN
# Backward compatibility: also accept KITCHENOWL_BASE_URL
BASE_URL="${KITCHENOWL_URL:-${KITCHENOWL_BASE_URL:-}}"
TOKEN="${KITCHENOWL_TOKEN:-}"
REFRESH_TOKEN="${KITCHENOWL_REFRESH_TOKEN:-}"

usage() {
  cat <<'EOF'
Usage:
  kitchenowl-api.sh probe [--base-url URL]
  kitchenowl-api.sh login --base-url URL --username USER --password PASS [--device NAME]
  kitchenowl-api.sh request METHOD PATH [--base-url URL] [--token TOKEN] [--json JSON]
  kitchenowl-api.sh graphql --query QUERY [--base-url URL] [--token TOKEN] [--variables JSON]
  kitchenowl-api.sh token show|load

Examples:
  kitchenowl-api.sh probe --base-url https://kitchenowl.example.com
  kitchenowl-api.sh login --base-url https://kitchenowl.example.com --username me --password 'secret'
  kitchenowl-api.sh request GET /api/user
  kitchenowl-api.sh graphql --query '{ __typename }'
EOF
}

json_pretty() { jq . 2>/dev/null || cat; }

save_session() {
  local base="$1" access="$2" refresh="$3"
  jq -n --arg base "$base" --arg access "$access" --arg refresh "$refresh" \
    '{base_url:$base,access_token:$access,refresh_token:$refresh,updated_at:(now|todate)}' > "$SESSION_FILE"
}

load_session() {
  [[ -f "$SESSION_FILE" ]] || return 1
  BASE_URL="${BASE_URL:-$(jq -r '.base_url // empty' "$SESSION_FILE") }"
  TOKEN="${TOKEN:-$(jq -r '.access_token // empty' "$SESSION_FILE") }"
  REFRESH_TOKEN="${REFRESH_TOKEN:-$(jq -r '.refresh_token // empty' "$SESSION_FILE") }"
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }
}

api_call() {
  local method="$1" path="$2" body="${3:-}"
  [[ -n "$BASE_URL" ]] || { echo "BASE_URL missing (set --base-url or KITCHENOWL_URL)." >&2; exit 1; }

  local url="${BASE_URL%/}${path}"
  local -a args=( -sS -X "$method" "$url" -H 'Accept: application/json' )

  if [[ -n "$TOKEN" ]]; then
    args+=( -H "Authorization: Bearer $TOKEN" )
  fi

  if [[ -n "$body" ]]; then
    args+=( -H 'Content-Type: application/json' --data "$body" )
  fi

  curl "${args[@]}"
}

cmd_probe() {
  local base=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --base-url) base="$2"; shift 2 ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done
  BASE_URL="${base:-$BASE_URL}"
  [[ -n "$BASE_URL" ]] || { echo "Missing --base-url" >&2; exit 1; }

  local candidates=(
    "/api"
    "/api/"
    "/api/auth"
    "/backend/api"
    "/backend/api/"
    "/graphql"
  )

  for p in "${candidates[@]}"; do
    code=$(curl -ks -o /tmp/kowl_probe.$$ -w '%{http_code}' "${BASE_URL%/}${p}")
    loc=$(curl -ksI "${BASE_URL%/}${p}" | awk -F': ' 'tolower($1)=="location"{print $2}' | tr -d '\r' || true)
    printf '%-18s  %s' "$p" "$code"
    [[ -n "${loc:-}" ]] && printf '  -> %s' "$loc"
    printf '\n'
  done
}

cmd_login() {
  local username="" password="" device="openclaw" base=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --base-url) base="$2"; shift 2 ;;
      --username) username="$2"; shift 2 ;;
      --password) password="$2"; shift 2 ;;
      --device) device="$2"; shift 2 ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  BASE_URL="${base:-$BASE_URL}"
  [[ -n "$BASE_URL" && -n "$username" && -n "$password" ]] || {
    echo "Missing --base-url / --username / --password" >&2
    exit 1
  }

  local payload
  payload=$(jq -n --arg u "$username" --arg p "$password" --arg d "$device" \
    '{username:$u,password:$p,device:$d}')

  local resp
  resp=$(api_call POST /api/auth "$payload")

  local access refresh
  access=$(echo "$resp" | jq -r '.access_token // empty')
  refresh=$(echo "$resp" | jq -r '.refresh_token // empty')

  if [[ -z "$access" ]]; then
    echo "Login failed:" >&2
    echo "$resp" | json_pretty >&2
    exit 1
  fi

  TOKEN="$access"
  REFRESH_TOKEN="$refresh"
  save_session "$BASE_URL" "$TOKEN" "$REFRESH_TOKEN"

  echo "Login OK. Session saved to $SESSION_FILE"
  echo "$resp" | jq '{user, has_refresh:(.refresh_token!=null)}'
}

cmd_request() {
  local method="${1:-}" path="${2:-}"; shift 2 || true
  local body="" base="" token_override=""
  [[ -n "$method" && -n "$path" ]] || { usage; exit 1; }

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --base-url) base="$2"; shift 2 ;;
      --token) token_override="$2"; shift 2 ;;
      --json) body="$2"; shift 2 ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  load_session || true
  BASE_URL="${base:-$BASE_URL}"
  TOKEN="${token_override:-$TOKEN}"

  api_call "$method" "$path" "$body" | json_pretty
}

cmd_graphql() {
  local query="" variables="{}" base="" token_override=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --query) query="$2"; shift 2 ;;
      --variables) variables="$2"; shift 2 ;;
      --base-url) base="$2"; shift 2 ;;
      --token) token_override="$2"; shift 2 ;;
      *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
  done

  [[ -n "$query" ]] || { echo "Missing --query" >&2; exit 1; }

  load_session || true
  BASE_URL="${base:-$BASE_URL}"
  TOKEN="${token_override:-$TOKEN}"

  local gql_path="/graphql"
  local payload
  payload=$(jq -n --arg q "$query" --argjson v "$variables" '{query:$q,variables:$v}')

  api_call POST "$gql_path" "$payload" | json_pretty
}

cmd_token() {
  local sub="${1:-show}"
  case "$sub" in
    show)
      load_session || true
      jq -n --arg base "$BASE_URL" --arg token "$TOKEN" --arg refresh "$REFRESH_TOKEN" \
        '{base_url:$base, token_present:($token|length>0), refresh_present:($refresh|length>0)}'
      ;;
    load)
      load_session
      echo "Loaded from $SESSION_FILE"
      ;;
    *)
      echo "Unknown token subcommand: $sub" >&2
      exit 1
      ;;
  esac
}

main() {
  need_cmd curl
  need_cmd jq

  local cmd="${1:-}"
  shift || true

  case "$cmd" in
    probe) cmd_probe "$@" ;;
    login) cmd_login "$@" ;;
    request) cmd_request "$@" ;;
    graphql) cmd_graphql "$@" ;;
    token) cmd_token "$@" ;;
    ""|-h|--help|help) usage ;;
    *)
      echo "Unknown command: $cmd" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
