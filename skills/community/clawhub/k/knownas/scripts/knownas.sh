#!/bin/sh
# knownas.sh: the knownas skill's only route to the knownAs.dev API.
#
# Every call the skill makes goes through here, so the rules hold in code,
# not only in prose:
#   - the API key is read from KNOWNAS_API_KEY and handed to curl on stdin,
#     never on a command line, and never printed;
#   - an origin secret goes straight from the API's answer into OpenClaw's
#     secret store, never to the terminal;
#   - nothing here creates an account, deletes an identity or archives one.
#
# Needs: sh, curl, jq. Exit codes: 0 ok, 2 usage, 3 the name is taken,
# 4 the name is not allowed, 5 the API refused (message printed), 6 the
# origin is not one the platform will accept.

set -eu
umask 077

API="${KNOWNAS_API_URL:-https://platform.knownas.dev}"
API="${API%/}"
SERVICES_DEFAULT="api webhooks"
STORE_CMD="${KNOWNAS_SECRET_STORE_CMD:-openclaw secrets store set}"

die() { printf 'knownas: %s\n' "$1" >&2; exit "${2:-1}"; }

case "$API" in
  https://*) ;;
  http://localhost:* | http://127.0.0.1:*) ;;
  *) die "KNOWNAS_API_URL must be https (http only for localhost)" 2 ;;
esac

command -v curl >/dev/null 2>&1 || die "curl is required" 2
command -v jq >/dev/null 2>&1 || die "jq is required" 2

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT INT TERM

need_key() {
  [ -n "${KNOWNAS_API_KEY:-}" ] || die "KNOWNAS_API_KEY is not set. A person mints it in the knownAs console; it is never pasted into chat." 2
}

# call METHOD PATH [BODY_FILE] -> HTTP status on stdout, body in $TMP/body
call() {
  method=$1; path=$2; body=${3:-}
  : > "$TMP/body"
  # Headers travel in curl's config on stdin: printf is a shell builtin, so
  # the key never appears in a process listing.
  {
    printf 'header = "Authorization: Bearer %s"\n' "$KNOWNAS_API_KEY"
    printf 'header = "Accept: application/json"\n'
    if [ -n "$body" ]; then
      printf 'header = "Content-Type: application/json"\n'
    fi
    if [ -n "${IDEMPOTENCY_KEY:-}" ]; then
      printf 'header = "Idempotency-Key: %s"\n' "$IDEMPOTENCY_KEY"
    fi
  } | if [ -n "$body" ]; then
    curl -sS --config - -X "$method" -o "$TMP/body" -w '%{http_code}' --data-binary "@$body" "$API$path"
  else
    curl -sS --config - -X "$method" -o "$TMP/body" -w '%{http_code}' "$API$path"
  fi
}

# The API's own error, without the request id noise.
api_error() {
  jq -r '.error | "\(.code): \(.message)" + ((.details // []) | map(" " + .message) | join(""))' "$TMP/body" 2>/dev/null ||
    printf 'HTTP %s\n' "$1"
}

ok_or_die() {
  case "$1" in
    2??) ;;
    *) die "$(api_error "$1")" 5 ;;
  esac
}

hash_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1"; else shasum -a 256 "$1"; fi | cut -c1-32
}

is_service() {
  case "$1" in api | mcp | webhooks) return 0 ;; *) return 1 ;; esac
}

# The platform refuses these; refusing first gives a clearer message.
origin_ok() {
  host=$(printf '%s' "$1" | tr 'A-Z' 'a-z')
  host=${host%.}
  case "$host" in
    "" | *://* | */* | *:* | *@* | *" "*) return 1 ;;
    localhost | *.localhost | *.local | *.internal | *.test | *.example | *.invalid | *.onion | *.arpa) return 1 ;;
    *.knownas.dev | knownas.dev) return 1 ;;
  esac
  # An IPv4 literal: all labels numeric.
  if printf '%s' "$host" | grep -Eq '^[0-9]+(\.[0-9]+){3}$'; then return 1; fi
  case "$host" in *.*) return 0 ;; *) return 1 ;; esac
}

cmd_whoami() {
  status=$(call GET /v1/me); ok_or_die "$status"
  jq '{principal_type, scopes, quota}' "$TMP/body"
}

# create SLUG NAME [MANIFEST_JSON_FILE] [SERVICES...]
cmd_create() {
  [ $# -ge 2 ] || die "usage: create SLUG NAME [MANIFEST_JSON_FILE] [SERVICE...]" 2
  slug=$1; name=$2; shift 2
  manifest=null
  if [ $# -ge 1 ] && [ -f "$1" ]; then manifest=$(jq -c . "$1"); shift; fi
  services=${*:-$SERVICES_DEFAULT}
  for s in $services; do is_service "$s" || die "unknown service: $s" 2; done
  jq -n --arg slug "$slug" --arg name "$name" --argjson manifest "$manifest" \
    --arg services "$services" \
    '{name: $name, slug: $slug, services: ($services | split(" ") | map(select(. != "")))}
     + (if $manifest == null then {} else {manifest: $manifest} end)' > "$TMP/request"
  IDEMPOTENCY_KEY=$(hash_of "$TMP/request")
  status=$(call POST /v1/identities "$TMP/request")
  code=$(jq -r '.error.code // empty' "$TMP/body" 2>/dev/null || true)
  case "$code" in
    IDENTITY_SLUG_UNAVAILABLE) die "$(api_error "$status")" 3 ;;
    IDENTITY_SLUG_INVALID | VALIDATION_ERROR) die "$(api_error "$status")" 4 ;;
  esac
  ok_or_die "$status"
  jq '{id, slug, fqdn, status, services, endpoints}' "$TMP/body"
}

# find SLUG -> the identity's id
cmd_find() {
  [ $# -eq 1 ] || die "usage: find SLUG" 2
  cursor=""
  while :; do
    status=$(call GET "/v1/identities?limit=100${cursor:+&cursor=$cursor}"); ok_or_die "$status"
    id=$(jq -r --arg s "$1" '.items[] | select(.slug == $s and (.status | IN("deleted", "deleting", "archived") | not)) | .id' "$TMP/body" | head -n 1)
    [ -n "$id" ] && { printf '%s\n' "$id"; return 0; }
    cursor=$(jq -r '.next_cursor // empty' "$TMP/body")
    [ -n "$cursor" ] || die "no identity named $1 on this account" 5
  done
}

# wait-active ID: up to about two minutes while DNS is provisioned
cmd_wait_active() {
  [ $# -eq 1 ] || die "usage: wait-active ID" 2
  i=0
  while [ $i -lt 24 ]; do
    status=$(call GET "/v1/identities/$1"); ok_or_die "$status"
    state=$(jq -r .status "$TMP/body")
    problem=$(jq -r '.provisioning_error // empty' "$TMP/body")
    [ -z "$problem" ] || die "provisioning failed: $problem" 5
    case "$state" in
      active) printf 'active\n'; return 0 ;;
      failed | suspended | archived | deleting | deleted) die "the identity is $state" 5 ;;
    esac
    i=$((i + 1)); sleep 5
  done
  die "the identity is still $state after two minutes; try again shortly" 5
}

# route ID SERVICE ORIGIN -> the route, with its proof token (not a secret)
cmd_route() {
  [ $# -eq 3 ] || die "usage: route ID SERVICE ORIGIN" 2
  is_service "$2" || die "unknown service: $2" 2
  origin_ok "$3" || die "$3 is not an origin the platform accepts: give a public host name only, no scheme, port, path or IP address" 6
  jq -n --arg origin "$3" '{origin: $origin}' > "$TMP/request"
  status=$(call PUT "/v1/identities/$1/routes/$2" "$TMP/request"); ok_or_die "$status"
  jq '{service, origin, status, token, proof_url}' "$TMP/body"
}

# check ID SERVICE -> passed/outcome; on a first pass the secret goes to the store
cmd_check() {
  [ $# -eq 2 ] || die "usage: check ID SERVICE" 2
  is_service "$2" || die "unknown service: $2" 2
  status=$(call POST "/v1/identities/$1/routes/$2/check")
  [ "$status" = 429 ] && die "checked less than a minute ago; wait a minute and check again" 5
  ok_or_die "$status"
  jq '{passed, outcome, http_status, status: .route.status}' "$TMP/body" > "$TMP/summary"
  stored=false
  if [ "$(jq -r '.origin_secret // empty | length > 0' "$TMP/body")" = true ]; then
    name="KNOWNAS_ORIGIN_SECRET_$(printf '%s' "$2" | tr 'a-z' 'A-Z')"
    jq -j '.origin_secret' "$TMP/body" | $STORE_CMD "$name" --kind secret >/dev/null
    stored=true
  fi
  # The secret leaves the disk as soon as it is in the store.
  : > "$TMP/body"
  jq --argjson stored "$stored" '. + {secret_stored: $stored}' "$TMP/summary"
}

# status ID -> identity, routes and traffic, as one JSON document
cmd_status() {
  [ $# -eq 1 ] || die "usage: status ID" 2
  status=$(call GET "/v1/identities/$1"); ok_or_die "$status"
  cp "$TMP/body" "$TMP/identity"
  status=$(call GET "/v1/identities/$1/routes"); ok_or_die "$status"
  cp "$TMP/body" "$TMP/routes"
  status=$(call GET "/v1/identities/$1/usage")
  case "$status" in 2??) cp "$TMP/body" "$TMP/usage" ;; *) printf 'null' > "$TMP/usage" ;; esac
  jq -n --slurpfile i "$TMP/identity" --slurpfile r "$TMP/routes" --slurpfile u "$TMP/usage" '
    ($i[0]) as $id | ($u[0]) as $use |
    {
      fqdn: $id.fqdn, status: $id.status, suspension_reason: $id.suspension_reason,
      record: $id.endpoints.manifest,
      routes: [$r[0].items[] | select(.status != "removed") |
               {service, origin, status, last_checked_at, last_success_at, consecutive_misses}],
      traffic: (if $use == null then null else
        {window_days: $use.window_days, bytes_total: $use.bytes_total, requests: $use.requests,
         busiest_hour_bytes_24h: $use.busiest_hour_bytes_24h, limits: $use.limits} end)
    }'
}

# remove-route ID SERVICE: idempotent
cmd_remove_route() {
  [ $# -eq 2 ] || die "usage: remove-route ID SERVICE" 2
  is_service "$2" || die "unknown service: $2" 2
  status=$(call DELETE "/v1/identities/$1/routes/$2"); ok_or_die "$status"
  jq '{service, status}' "$TMP/body"
}

cmd_origin_ok() {
  [ $# -eq 1 ] || die "usage: origin-ok HOST" 2
  origin_ok "$1" || die "$1 is not an origin the platform accepts: give a public host name only, no scheme, port, path or IP address" 6
  printf 'ok\n'
}

[ $# -ge 1 ] || die "usage: knownas.sh whoami|create|find|wait-active|route|check|status|remove-route|origin-ok ..." 2
sub=$1; shift
[ "$sub" = origin-ok ] || need_key
case "$sub" in
  whoami) cmd_whoami "$@" ;;
  create) cmd_create "$@" ;;
  find) cmd_find "$@" ;;
  wait-active) cmd_wait_active "$@" ;;
  route) cmd_route "$@" ;;
  check) cmd_check "$@" ;;
  status) cmd_status "$@" ;;
  remove-route) cmd_remove_route "$@" ;;
  origin-ok) cmd_origin_ok "$@" ;;
  *) die "unknown command: $sub" 2 ;;
esac
