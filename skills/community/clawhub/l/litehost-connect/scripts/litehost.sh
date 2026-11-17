#!/usr/bin/env bash
# Litehost Connect helper for agents.
#
# Each agent command usually runs in a fresh shell, so `export` does not
# survive between commands. This script keeps the API key in a file instead
# and reads it on every call, and it never prints the full key.
#
# Usage:
#   litehost.sh session                    Is there a saved key, and does it work?
#   litehost.sh request-code EMAIL [--resend]
#   litehost.sh verify EMAIL CODE          Signs in and saves the key (not printed)
#   litehost.sh save-key KEY [EMAIL]       Save a key the user pasted or made in the dashboard
#   litehost.sh forget                     Delete the saved key
#   litehost.sh temp FILE [FILE...]        Publish without signing in (15 min + claimUrl)
#   litehost.sh api METHOD PATH [curl args...]   Authenticated call, e.g.
#       litehost.sh api GET /v1/user
#       litehost.sh api POST /v1/projects -F "title=Site" -F "files=@index.html"
#
# Key lookup order: $LITEHOST_API_KEY, then $LITEHOST_CREDENTIALS
# (default ~/.config/litehost/credentials.json).

set -euo pipefail

BASE="${LITEHOST_API_URL:-https://connect.litehost.io}"
CRED="${LITEHOST_CREDENTIALS:-$HOME/.config/litehost/credentials.json}"

json_field() { # json_field NAME < json  (flat string fields only)
  sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" | head -n 1
}

saved_key() {
  if [ -n "${LITEHOST_API_KEY:-}" ]; then printf '%s' "$LITEHOST_API_KEY"; return; fi
  if [ -f "$CRED" ]; then json_field apiKey < "$CRED"; fi
}

save_key() { # save_key KEY EMAIL
  mkdir -p "$(dirname "$CRED")"
  umask 077
  printf '{"apiKey":"%s","email":"%s"}\n' "$1" "${2:-}" > "$CRED"
  chmod 600 "$CRED"
}

mask() { printf '%s…%s' "${1:0:12}" "${1: -4}"; }

# Every call goes through lh_curl: it tags requests as coming from this skill
# and turns "this environment cannot reach Litehost" (sandboxed chats with a
# domain allowlist, no network) into one clear code instead of a raw curl error.
lh_curl() {
  local out rc
  set +e
  out="$(curl -sS -H "X-Litehost-Client: skill" "$@" 2>&1)"
  rc=$?
  set -e
  case "$out" in
    \{*) printf '%s\n' "$out"; return 0 ;;
  esac
  local detail
  detail="$(printf '%s' "$out" | head -c 200 | tr '"\\\n\r' "'   ")"
  if [ "$rc" -ne 0 ]; then
    printf '{"status":"error","code":"NETWORK_BLOCKED","error":"This environment cannot reach %s (%s)","nextStep":"Stop and do not sign in. Tell the user this chat cannot reach Litehost and suggest the Litehost connector: Settings > Connectors > Add custom connector > https://connect.litehost.io/mcp. See Step 0 in SKILL.md."}\n' "$BASE" "$detail"
  else
    printf '{"status":"error","code":"UNEXPECTED_RESPONSE","error":"Litehost answered with something that is not JSON: %s","nextStep":"Wait a minute and try once more. If it happens again, tell the user Litehost may be down."}\n' "$detail"
  fi
  return 1
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  session)
    key="$(saved_key)"
    if [ -z "$key" ]; then
      # Check Litehost is reachable first, so a blocked sandbox is caught before any sign-in.
      reach="$(lh_curl "$BASE/v1")" || { printf '%s\n' "$reach"; exit 0; }
      echo '{"status":"error","code":"NO_SAVED_KEY","nextStep":"No key saved. To publish, use: litehost.sh temp FILE. Sign in only if the user wants you to manage their projects."}'
      exit 0
    fi
    lh_curl "$BASE/v1/auth/session" -H "Authorization: Bearer $key"
    ;;

  request-code)
    email="${1:?email required}"
    resend=false
    [ "${2:-}" = "--resend" ] && resend=true
    lh_curl -X POST "$BASE/v1/auth/otp/request" -H "Content-Type: application/json" \
      -d "{\"email\":\"$email\",\"resend\":$resend}"
    ;;

  verify)
    email="${1:?email required}"
    code="${2:?code required}"
    res="$(lh_curl -X POST "$BASE/v1/auth/otp/verify" -H "Content-Type: application/json" \
      -d "{\"email\":\"$email\",\"code\":\"$code\"}")" || { printf '%s\n' "$res"; exit 1; }
    key="$(printf '%s' "$res" | json_field apiKey)"
    if [ -n "$key" ]; then
      save_key "$key" "$email"
      expires="$(printf '%s' "$res" | json_field expiresAt)"
      echo "{\"status\":\"success\",\"email\":\"$email\",\"apiKey\":\"$(mask "$key")\",\"savedTo\":\"$CRED\",\"expiresAt\":\"$expires\",\"note\":\"Key saved; it renews while in use. Do not sign in again.\"}"
    else
      printf '%s\n' "$res"
    fi
    ;;

  save-key)
    key="${1:?key required}"
    save_key "$key" "${2:-}"
    echo "{\"status\":\"success\",\"apiKey\":\"$(mask "$key")\",\"savedTo\":\"$CRED\"}"
    ;;

  forget)
    rm -f "$CRED"
    echo '{"status":"success","note":"Saved key deleted."}'
    ;;

  temp)
    [ "$#" -ge 1 ] || { echo "usage: litehost.sh temp FILE [FILE...]" >&2; exit 2; }
    args=()
    for f in "$@"; do args+=(-F "files=@$f"); done
    lh_curl -X POST "$BASE/v1/projects/temp" "${args[@]}"
    ;;

  api)
    method="${1:?method required}"
    path="${2:?path required}"
    shift 2
    key="$(saved_key)"
    if [ -z "$key" ]; then
      echo '{"status":"error","code":"NO_SAVED_KEY","nextStep":"No key saved. Run: litehost.sh session. Sign in only if the user wants you to manage their projects."}'
      exit 1
    fi
    lh_curl -X "$method" "$BASE$path" -H "Authorization: Bearer $key" "$@"
    ;;

  *)
    sed -n '2,22p' "$0"
    ;;
esac
