#!/usr/bin/env bash
# Teams chat-service helpers — source this file, then use teams_get.
#
#   source references/teams-env.sh
#   teams_token_refresh            # once per ~23h (browser needed only here)
#   teams_get '/users/ME/conversations?view=msnp24Equivalent&pageSize=200' | jq .
#
# Works under bash and zsh. Data on stdout, diagnostics on stderr.
# The bearer token never appears in argv (curl reads it from a 0600 config file).
# Read-only: there is deliberately no PUT/POST helper — a PUT of
# consumptionhorizon would mark the user's chats read.

TEAMS_FPX_DIR="${TEAMS_FPX_DIR:-$HOME/.teams-fpx}"
TEAMS_FPX_PROFILE="${TEAMS_FPX_PROFILE:-teams}"
TEAMS_CHATSVC_REGION="${TEAMS_CHATSVC_REGION:-amer}"
TEAMS_CHATSVC_BASE="${TEAMS_CHATSVC_BASE:-https://teams.cloud.microsoft/api/chatsvc/${TEAMS_CHATSVC_REGION}/v1}"
# The capture declaration: the Authorization header of any request the Teams
# worker makes to its chat service.
TEAMS_CAPTURE="authorization@teams.cloud.microsoft/api/chatsvc/*"

_teams_curlrc() { printf '%s/curlrc' "$TEAMS_FPX_DIR"; }

# Capture a fresh bearer token from the signed-in browser tab.
teams_token_refresh() {
  local timeout="${1:-55}" tmp rc token dir
  dir="$TEAMS_FPX_DIR"
  mkdir -p "$dir" || return 1
  chmod 700 "$dir" 2>/dev/null

  command -v fpx >/dev/null 2>&1 || {
    echo "fpx not found — npm i -g @fetchproxy/cli" >&2; return 1; }

  tmp="$(mktemp "${TMPDIR:-/tmp}/teams-cap.XXXXXX")" || return 1

  # An idle tab never calls the chat service, so nothing would match.
  echo "capturing token — click into any chat in your Teams tab now…" >&2
  fpx capture "$TEAMS_CAPTURE" --capture-timeout "$timeout" -p "$TEAMS_FPX_PROFILE" \
      >"$tmp" 2>"$tmp.err"; rc=$?

  if [ "$rc" -ne 0 ] || [ ! -s "$tmp" ]; then
    echo "capture failed (exit $rc). Is a signed-in Teams tab open, and did you click a chat?" >&2
    sed -n '1,3p' "$tmp.err" >&2 2>/dev/null
    rm -f "$tmp" "$tmp.err"; return 1
  fi

  token="$(TEAMS_CAP_FILE="$tmp" python3 -c '
import json, os, sys
d = json.load(open(os.environ["TEAMS_CAP_FILE"]))
vals = [x for x in d.values() if isinstance(x, str) and x.strip()] if isinstance(d, dict) else []
sys.stdout.write(vals[0].strip() if vals else "")
')"
  rm -f "$tmp" "$tmp.err"

  case "$token" in
    Bearer\ *) : ;;
    "") echo "no authorization header captured — click into a chat and retry" >&2; return 1 ;;
    *) token="Bearer $token" ;;
  esac

  local rc_file; rc_file="$(_teams_curlrc)"
  # The umask is set in a subshell: this file is sourced, so a bare umask
  # would leak into the caller's shell for good.
  ( umask 077; printf 'header = "Authorization: %s"\n' "$token" > "$rc_file" ) || return 1
  chmod 600 "$rc_file" 2>/dev/null
  echo "token stored in $rc_file ($(teams_token_expiry))" >&2
}

# Print the token's expiry (non-secret claim) without revealing the token.
teams_token_expiry() {
  local rc_file; rc_file="$(_teams_curlrc)"
  [ -f "$rc_file" ] || { echo "no token"; return 1; }
  TEAMS_RC="$rc_file" python3 -c '
import base64, json, os, re, sys, datetime
txt = open(os.environ["TEAMS_RC"]).read()
m = re.search(r"Authorization: Bearer ([A-Za-z0-9._-]+)", txt)
if not m: print("unparseable"); sys.exit(1)
p = m.group(1).split(".")
if len(p) < 2: print("not a jwt"); sys.exit(1)
s = p[1] + "=" * (-len(p[1]) % 4)
try:
    exp = json.loads(base64.urlsafe_b64decode(s)).get("exp")
except Exception:
    print("undecodable"); sys.exit(1)
if not exp: print("no exp"); sys.exit(1)
now = datetime.datetime.now(datetime.timezone.utc).timestamp()
left = int(exp - now)
when = datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
print(f"expires {when}" + (f", {left//3600}h{(left%3600)//60}m left" if left > 0 else ", EXPIRED"))
'
}

# NOTE: never name a local `path` or `status` here. In zsh `path` is tied to the
# PATH array (assigning it wipes PATH for the rest of the function) and
# `status` is read-only. Both are harmless under bash.
_teams_request() {
  local url="$1"; shift
  local rc_file; rc_file="$(_teams_curlrc)"
  [ -f "$rc_file" ] || { echo "no token — run: teams_token_refresh" >&2; return 1; }

  local http_status tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/teams-resp.XXXXXX")" || return 1
  # Args in an array so nothing is re-split; token stays in the -K file.
  local -a args
  args=(-s -K "$rc_file" -H 'behavioroverride: redirectAs404'
        -o "$tmp" -w '%{http_code}' --max-time 60)
  http_status="$(curl "${args[@]}" "$@" "$url")" || {
    echo "curl failed" >&2; rm -f "$tmp"; return 1; }

  case "$http_status" in
    2*) cat "$tmp"; rm -f "$tmp"; return 0 ;;
    401) echo "401 — token expired or revoked. Run: teams_token_refresh" >&2
         rm -f "$tmp"; return 4 ;;
    *)  echo "HTTP $http_status" >&2; sed -n '1,5p' "$tmp" >&2; rm -f "$tmp"; return 4 ;;
  esac
}

# teams_get '<path under the chat-service base>' [extra curl args...]
teams_get() { local p="$1"; shift; _teams_request "${TEAMS_CHATSVC_BASE}${p}" -H 'Accept: application/json' "$@"; }

# teams_get_url '<absolute chat-service URL, e.g. a backwardLink>' [extra curl args...]
teams_get_url() {
  local u="$1"; shift
  case "$u" in
    https://teams.cloud.microsoft/api/chatsvc/*) _teams_request "$u" -H 'Accept: application/json' "$@" ;;
    *) echo "refusing to send the Teams token to $u" >&2; return 1 ;;
  esac
}

# teams_get_image '<https://*.asm.skype.com/... img src>' <out-file>
# The URL comes from message content, so the host is checked before the token
# is sent anywhere.
teams_get_image() {
  local u="$1" out="$2"
  [ -n "$out" ] || { echo "usage: teams_get_image <url> <out-file>" >&2; return 1; }
  local host="${u#https://}"; host="${host%%/*}"
  case "$u" in
    https://*) : ;;
    *) echo "refusing a non-https image URL" >&2; return 1 ;;
  esac
  case "$host" in
    *[!A-Za-z0-9.-]*) echo "refusing an image URL with an unusual host" >&2; return 1 ;;
    *.asm.skype.com) : ;;
    *) echo "refusing to send the Teams token to $host" >&2; return 1 ;;
  esac
  _teams_request "$u" -H 'Accept: image/*' > "$out"
}
