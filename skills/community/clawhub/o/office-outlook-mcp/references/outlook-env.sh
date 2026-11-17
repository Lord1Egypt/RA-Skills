#!/usr/bin/env bash
# Outlook access helpers — source this file, then use outlook_get / outlook_post.
#
#   source references/outlook-env.sh
#   outlook_token_refresh          # once per ~25h (browser needed only here)
#   outlook_get '/me/messages?$top=5&$select=Subject,From' | jq .
#
# Works under bash and zsh. Data on stdout, diagnostics on stderr.
# The bearer token never appears in argv (curl reads it from a 0600 config file).

OUTLOOK_FPX_DIR="${OUTLOOK_FPX_DIR:-$HOME/.outlook-fpx}"
OUTLOOK_FPX_PROFILE="${OUTLOOK_FPX_PROFILE:-outlook}"
OUTLOOK_API="${OUTLOOK_API:-https://outlook.office.com/api/v2.0}"
# Host whose outgoing Authorization header we snapshot. New Outlook Web is on
# outlook.cloud.microsoft; older tenants still serve outlook.office.com.
OUTLOOK_CAPTURE_HOST="${OUTLOOK_CAPTURE_HOST:-outlook.cloud.microsoft}"

_outlook_curlrc() { printf '%s/curlrc' "$OUTLOOK_FPX_DIR"; }

# Reload an open Outlook tab so the page re-issues API calls while we capture.
# macOS/Chrome only; a no-op elsewhere (the capture still works if the tab is
# active on its own, it is just less reliable).
_outlook_poke_tab() {
  command -v osascript >/dev/null 2>&1 || return 0
  osascript - "$OUTLOOK_CAPTURE_HOST" <<'APPLESCRIPT' >/dev/null 2>&1 || true
on run argv
	set theHost to item 1 of argv
	tell application "Google Chrome"
		repeat with w in windows
			repeat with t in tabs of w
				if (URL of t) contains theHost then
					tell t to reload
					return "ok"
				end if
			end repeat
		end repeat
	end tell
	return "none"
end run
APPLESCRIPT
}

# Capture a fresh bearer token from the signed-in browser tab.
outlook_token_refresh() {
  local timeout="${1:-55}" tmp rc token dir
  dir="$OUTLOOK_FPX_DIR"
  mkdir -p "$dir" || return 1
  chmod 700 "$dir" 2>/dev/null

  command -v fpx >/dev/null 2>&1 || {
    echo "fpx not found — npm i -g @fetchproxy/cli" >&2; return 1; }

  tmp="$(mktemp "${TMPDIR:-/tmp}/outlook-cap.XXXXXX")" || return 1

  echo "capturing token from ${OUTLOOK_CAPTURE_HOST} (reloading your Outlook tab)…" >&2
  fpx capture "authorization@${OUTLOOK_CAPTURE_HOST}" \
      --capture-timeout "$timeout" -p "$OUTLOOK_FPX_PROFILE" >"$tmp" 2>"$tmp.err" &
  local cappid=$!
  sleep 3
  _outlook_poke_tab
  wait "$cappid"; rc=$?

  if [ "$rc" -ne 0 ] || [ ! -s "$tmp" ]; then
    echo "capture failed (exit $rc). Is an Outlook tab open and signed in?" >&2
    sed -n '1,3p' "$tmp.err" >&2 2>/dev/null
    rm -f "$tmp" "$tmp.err"; return 1
  fi

  token="$(OUTLOOK_CAP_FILE="$tmp" OUTLOOK_CAP_HOST="$OUTLOOK_CAPTURE_HOST" python3 -c '
import json, os, sys
d = json.load(open(os.environ["OUTLOOK_CAP_FILE"]))
v = d.get("authorization@" + os.environ["OUTLOOK_CAP_HOST"])
if not v:
    vals = [x for x in d.values() if isinstance(x, str) and x.strip()]
    v = vals[0] if vals else ""
sys.stdout.write(v.strip())
')"
  rm -f "$tmp" "$tmp.err"

  case "$token" in
    Bearer\ *) : ;;
    "") echo "no authorization header captured — reload Outlook and retry" >&2; return 1 ;;
    *) token="Bearer $token" ;;
  esac

  local rc_file; rc_file="$(_outlook_curlrc)"
  # Subshell: this file is sourced, and a bare `umask` would outlive the call.
  ( umask 077; printf 'header = "Authorization: %s"\n' "$token" > "$rc_file" ) || return 1
  chmod 600 "$rc_file" 2>/dev/null
  echo "token stored in $rc_file ($(outlook_token_expiry))" >&2
}

# Print the token's expiry (non-secret claim) without revealing the token.
outlook_token_expiry() {
  local rc_file; rc_file="$(_outlook_curlrc)"
  [ -f "$rc_file" ] || { echo "no token"; return 1; }
  OUTLOOK_RC="$rc_file" python3 -c '
import base64, json, os, re, sys, datetime
txt = open(os.environ["OUTLOOK_RC"]).read()
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
# PATH array (assigning it wipes PATH for the rest of the function, so even
# `mktemp` stops resolving) and `status` is read-only. Both are harmless under
# bash, so this only shows up when the file is sourced from a zsh shell.
_outlook_request() {
  local method="$1" req_path="$2"; shift 2
  local rc_file; rc_file="$(_outlook_curlrc)"
  [ -f "$rc_file" ] || { echo "no token — run: outlook_token_refresh" >&2; return 1; }

  local http_status tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/outlook-resp.XXXXXX")" || return 1
  # Args in an array so nothing is re-split; token stays in the -K file.
  local -a args
  args=(-s -K "$rc_file" -X "$method" -H 'Accept: application/json'
        -o "$tmp" -w '%{http_code}' --max-time 60)
  http_status="$(curl "${args[@]}" "$@" "${OUTLOOK_API}${req_path}")" || {
    echo "curl failed" >&2; rm -f "$tmp"; return 1; }

  case "$http_status" in
    2*) cat "$tmp"; rm -f "$tmp"; return 0 ;;
    401) echo "401 — token expired or revoked. Run: outlook_token_refresh" >&2
         rm -f "$tmp"; return 4 ;;
    *)  echo "HTTP $http_status" >&2; sed -n '1,5p' "$tmp" >&2; rm -f "$tmp"; return 4 ;;
  esac
}

# outlook_get '<path>' [extra curl args...]
outlook_get() { local p="$1"; shift; _outlook_request GET "$p" "$@"; }

# outlook_post '<path>' '<json>' [extra curl args...]
outlook_post() {
  local p="$1" body="$2"; shift 2
  _outlook_request POST "$p" -H 'Content-Type: application/json' -d "$body" "$@"
}

# outlook_patch '<path>' '<json>' [extra curl args...]
outlook_patch() {
  local p="$1" body="$2"; shift 2
  _outlook_request PATCH "$p" -H 'Content-Type: application/json' -d "$body" "$@"
}

# Plain-text bodies instead of HTML — ~3-9x smaller. Use for anything you read.
outlook_get_text() { local p="$1"; shift; outlook_get "$p" -H 'Prefer: outlook.body-content-type="text"' "$@"; }
