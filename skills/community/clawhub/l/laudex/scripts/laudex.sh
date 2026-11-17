#!/usr/bin/env bash
# Laudex CLI helper — search the catalog, inspect a service, report an outcome.
#
#   laudex.sh search "<intent>" [--type mcp_server|api|tool|saas|other] [--limit N]
#   laudex.sh service <service_id>
#   laudex.sh report <service_id> success|failure "<notes>" [--rating 1-5] [--dry-run]
#   laudex.sh register [email]
#
# API key: $LAUDEX_API_KEY (the plugin's SessionStart hook sets it from the
# plugin's settings), else ~/.config/laudex/credentials. If neither exists, the
# first call registers a new agent and saves the key there.
# Base URL: $LAUDEX_URL (default https://laudex.dev).
# LAUDEX_REPORTING=off turns report into a no-op; --dry-run prints what it would send.
# --rating is optional: a whole number from 1 to 5, 3 to 5 with success, 1 and 2 with
# failure (the scale is in SKILL.md). A rating the server would refuse is refused here.

set -euo pipefail

BASE="${LAUDEX_URL:-https://laudex.dev}"
CRED_FILE="${LAUDEX_CREDENTIALS:-$HOME/.config/laudex/credentials}"

die() { echo "laudex: $*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

# Build a JSON object from key/value pairs without hand-escaping strings.
# Values prefixed with "json:" are emitted raw (for booleans).
json_obj() {
  if have jq; then
    local args=() filter="{" first=1 k v
    while [ $# -gt 0 ]; do
      k="$1"; v="$2"; shift 2
      [ $first -eq 1 ] || filter+=","
      first=0
      if [[ "$v" == json:* ]]; then args+=(--argjson "$k" "${v#json:}"); else args+=(--arg "$k" "$v"); fi
      filter+="\"$k\":\$$k"
    done
    jq -cn "${args[@]}" "$filter}"
  elif have python3; then
    python3 - "$@" <<'PY'
import json, sys
a = sys.argv[1:]
out = {}
for k, v in zip(a[::2], a[1::2]):
    out[k] = json.loads(v[5:]) if v.startswith("json:") else v
print(json.dumps(out))
PY
  else
    die "need jq or python3 to build request bodies"
  fi
}

register() {
  local email="${1:-}" body resp key
  if [ -n "$email" ]; then body=$(json_obj email "$email"); else body='{}'; fi
  resp=$(curl -sS -m 20 -X POST "$BASE/api/agents/register" -H 'Content-Type: application/json' -d "$body")
  key=$(printf '%s' "$resp" | grep -o '"api_key":"lx_[a-f0-9]*"' | cut -d'"' -f4 || true)
  [ -n "$key" ] || die "registration failed: $resp"
  mkdir -p "$(dirname "$CRED_FILE")"
  (umask 077; printf '%s\n' "$key" > "$CRED_FILE")
  echo "Registered with Laudex; key saved to $CRED_FILE" >&2
}

api_key() {
  if [ -n "${LAUDEX_API_KEY:-}" ]; then printf '%s' "$LAUDEX_API_KEY"; return; fi
  [ -s "$CRED_FILE" ] || register "${LAUDEX_EMAIL:-}"
  head -n1 "$CRED_FILE" | tr -d '[:space:]'
}

# GET/POST with auth. Prints the body; exits non-zero on HTTP >= 400.
call() {
  local method="$1" path="$2" data="${3:-}" out status
  out=$(mktemp)
  local args=(-sS -m 60 -o "$out" -w '%{http_code}' -X "$method" "$BASE$path" -H "Authorization: Bearer $(api_key)")
  [ -z "$data" ] || args+=(-H 'Content-Type: application/json' -d "$data")
  status=$(curl "${args[@]}") || { rm -f "$out"; die "request to $BASE$path failed"; }
  if [ "$status" -ge 400 ]; then
    echo "laudex: HTTP $status from $path: $(cat "$out")" >&2
    rm -f "$out"; exit 1
  fi
  cat "$out"; rm -f "$out"
}

# Notes leave this machine (Laudex keeps them; other agents see only totals).
# SKILL.md tells the agent what to leave out;
# this is the backstop for what slips through: secrets, emails, private-network
# addresses and the user's file paths are replaced, newlines are flattened, and
# the caller announces any change on stderr. Plain sed -E, so it behaves the
# same on macOS and Linux. Tests: tests/scrub_notes.sh.
#
# Three things are deliberately kept, because they are facts about a tool:
# git@host: SSH remotes, /tmp/<name> directories a tool writes into, and
# environment variable NAMES (only the value after `=` is replaced).
NOTES_MAX=600
flatten() { printf '%s' "$1" | tr '\n\r\t' '   '; }
# The end of a path or URL: no trailing quote, bracket or sentence punctuation.
TAIL='[^[:space:])>";,]*[^[:space:])>";,.]'
scrub_notes() {
  flatten "$1" | sed -E \
    -e 's!(sk|pk|rk)-[A-Za-z0-9_-]{16,}!<secret>!g' \
    -e 's!(sk|pk|rk)_(live|test)_[A-Za-z0-9]{8,}!<secret>!g' \
    -e 's!whsec_[A-Za-z0-9]{16,}!<secret>!g' \
    -e 's!gh[pousr]_[A-Za-z0-9]{20,}!<secret>!g' \
    -e 's!github_pat_[A-Za-z0-9_]{20,}!<secret>!g' \
    -e 's!glpat-[A-Za-z0-9_-]{16,}!<secret>!g' \
    -e 's!npm_[A-Za-z0-9]{30,}!<secret>!g' \
    -e 's!hf_[A-Za-z0-9]{30,}!<secret>!g' \
    -e 's!AIza[0-9A-Za-z_-]{30,}!<secret>!g' \
    -e 's!lx_[0-9a-f]{32}!<secret>!g' \
    -e 's!AKIA[0-9A-Z]{16}!<secret>!g' \
    -e 's!xox[abprs]-[A-Za-z0-9-]{10,}!<secret>!g' \
    -e 's!eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+!<secret>!g' \
    -e 's![Bb]earer [A-Za-z0-9._~+/=-]{16,}!Bearer <secret>!g' \
    -e 's!([A-Za-z0-9_]*([Kk][Ee][Yy]|[Tt][Oo][Kk][Ee][Nn]|[Ss][Ee][Cc][Rr][Ee][Tt]|[Pp][Aa][Ss][Ss][Ww]([Oo][Rr])?[Dd]|PWD)[A-Za-z0-9_]*)=[^[:space:]"'"'"',;)]+!\1=<secret>!g' \
    -e 's!([a-z][a-z0-9+.-]*://)[^/@:[:space:]]*:[^/@[:space:]]+@!\1<secret>@!g' \
    -e 's!([A-Za-z0-9]{32,})!<<lxt:\1:lxt>>!g' \
    -e 's!<<lxt:([A-Za-z]+):lxt>>!\1!g' \
    -e 's!<<lxt:([0-9]+):lxt>>!\1!g' \
    -e 's!<<lxt:[A-Za-z0-9]+:lxt>>!<secret>!g' \
    -e 's!https?://(localhost|127\.[0-9.]+|0\.0\.0\.0|10\.[0-9.]+|192\.168\.[0-9.]+|172\.(1[6-9]|2[0-9]|3[01])\.[0-9.]+|[A-Za-z0-9.-]+\.(internal|local|lan|corp|intranet))(:[0-9]+)?('"$TAIL"')?!<internal-url>!g' \
    -e 's!(^|[^A-Za-z0-9._%+-])git@([A-Za-z0-9.-]+\.[A-Za-z]{2,})([:/])!\1<<lxgit>>\2\3!g' \
    -e 's![A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}!<email>!g' \
    -e 's!<<lxgit>>[A-Za-z0-9.-]+\.(internal|local|lan|corp|intranet)[:/]('"$TAIL"')?!<internal-url>!g' \
    -e 's!<<lxgit>>!git@!g' \
    -e 's!(^|[^0-9A-Za-z.])((10|127)\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|192\.168\.[0-9]{1,3}\.[0-9]{1,3}|172\.(1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3}|0\.0\.0\.0)(:[0-9]+)?!\1<internal-host>!g' \
    -e 's!(^|[^A-Za-z0-9_./-])/tmp/([A-Za-z0-9_-]+)([^A-Za-z0-9_./-]|\.[[:space:]]|\.$|$)!\1<<lxtmp>>\2\3!g' \
    -e 's!(^|[^A-Za-z0-9_.:/~-])(/Users|/home|/root|/private|/tmp|/var/folders|/workspace|/opt|/Volumes|/mnt|/srv)/'"$TAIL"'!\1<path>!g' \
    -e 's!(^|[^A-Za-z0-9_./-])~/'"$TAIL"'!\1<path>!g' \
    -e 's!(^|[^A-Za-z0-9_./~-])\.\.?/'"$TAIL"'!\1<path>!g' \
    -e 's!(^|[^A-Za-z0-9_])[A-Za-z]:\\'"$TAIL"'!\1<path>!g' \
    -e 's!(^|[^A-Za-z0-9_./-])[A-Za-z0-9_][A-Za-z0-9._-]*\.(docx|doc|xlsx|xls|pptx|ppt|pdf|csv|tsv|key|pem|p12|pfx|sqlite|db)([^A-Za-z0-9]|$)!\1<path>\3!g' \
    -e 's!<<lxtmp>>!/tmp/!g'
}

urlencode() {
  if have jq; then printf '%s' "$1" | jq -sRr @uri
  else python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$1"; fi
}

cmd="${1:-}"; shift || true
case "$cmd" in
  search)
    intent="${1:-}"; shift || true
    [ -n "$intent" ] || die 'usage: laudex.sh search "<intent>" [--type T] [--limit N]'
    qs="intent=$(urlencode "$intent")"
    while [ $# -gt 0 ]; do
      case "$1" in
        --type) qs+="&type=$2"; shift 2 ;;
        --limit) qs+="&limit=$2"; shift 2 ;;
        *) die "unknown flag: $1" ;;
      esac
    done
    resp=$(call GET "/api/search?$qs")
    # The full response carries each row's quality_signals blob; trim to what an
    # agent needs to choose, so results don't flood the context window.
    if have jq; then
      # glama_url and credit survive the trim: Glama's licence asks for both
      # wherever one of its records is shown.
      # `note` survives too: when a search was not judged, it says why.
      printf '%s' "$resp" | jq '{mode, note, routing: (.routing // null | if . then {category, scope, confidence, candidates_considered} else null end),
        credit: ([.results[].attribution.credit // empty] | first),
        results: [.results[] | {id: .service.id, name: .service.name, type: .service.type, url: .service.url,
          description: ((.service.description // "") | .[0:240]),
          owner: .highlights.owner, repo: .highlights.repo, stars: .highlights.stars,
          weekly_downloads: .highlights.weekly_downloads, install: .highlights.install,
          fit: .score.fit, best_fit_share: .score.best_fit_share, similarity: .score.similarity, quality: .score.quality,
          success_rate: .score.success_rate, signal_count: .score.signal_count,
          rating_average: .score.rating_average, rating_count: .score.rating_count,
          glama_url: .attribution.glama_url}
          | with_entries(select(.value != null))]}
        | with_entries(select(.value != null))'
    else
      printf '%s\n' "$resp"
    fi
    ;;
  service)
    [ -n "${1:-}" ] || die "usage: laudex.sh service <service_id>"
    call GET "/api/services/$1"
    ;;
  report)
    [ $# -ge 2 ] || die 'usage: laudex.sh report <service_id> success|failure "<notes>" [--rating 1-5] [--dry-run]'
    id="$1"; outcome="$2"; shift 2
    raw=""; dry=0; rating=""; rating_given=0
    while [ $# -gt 0 ]; do
      case "$1" in
        --dry-run) dry=1; shift ;;
        --rating)
          [ $# -ge 2 ] || die "--rating needs a whole number from 1 to 5"
          rating="$2"; rating_given=1; shift 2 ;;
        *) raw="$1"; shift ;;
      esac
    done
    case "$outcome" in
      success|true) ok=true ;;
      failure|false) ok=false ;;
      *) die "outcome must be success or failure, got: $outcome" ;;
    esac
    # The server's rule, checked here first so a mistake is explained and the
    # report is not lost to a 400: a whole number 1 to 5, 3 to 5 with success,
    # 1 and 2 with failure. No --rating at all is always fine.
    if [ "$rating_given" = 1 ]; then
      case "$rating" in
        [1-5]) ;;
        *) die "rating must be a whole number from 1 to 5, got: '$rating'" ;;
      esac
      if [ "$ok" = true ] && [ "$rating" -lt 3 ]; then
        die "rating $rating cannot go with success. Ratings 3 to 5 go with success, 1 and 2 with failure"
      elif [ "$ok" = false ] && [ "$rating" -gt 2 ]; then
        die "rating $rating cannot go with failure. Ratings 3 to 5 go with success, 1 and 2 with failure"
      fi
    fi
    case "${LAUDEX_REPORTING:-on}" in
      off|false|0|no) echo "laudex: reporting is off (LAUDEX_REPORTING); nothing sent" >&2; exit 0 ;;
    esac
    notes=$(scrub_notes "$raw")
    [ "$notes" = "$(flatten "$raw")" ] ||
      echo "laudex: replaced paths, emails, internal URLs or secrets in the notes; rewrite them if the result no longer reads well" >&2
    if [ "${#notes}" -gt "$NOTES_MAX" ]; then
      notes="${notes:0:$NOTES_MAX}"
      echo "laudex: notes cut to $NOTES_MAX characters" >&2
    fi
    # No note means no notes field, rather than an empty string stored as one;
    # likewise no rating means no rating field (the server reads it as "not given").
    fields=(service_id "$id" success "json:$ok")
    [ "$rating_given" = 0 ] || fields+=(rating "json:$rating")
    [ -z "$notes" ] || fields+=(notes "$notes")
    body=$(json_obj "${fields[@]}")
    if [ "$dry" -eq 1 ]; then
      printf '%s\n' "$body"
      echo "laudex: dry run, nothing sent" >&2
      exit 0
    fi
    call POST /api/signal "$body"
    echo
    ;;
  register)
    register "${1:-}"
    ;;
  *)
    sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac
