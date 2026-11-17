# MyAtriumHealth (Epic MyChart) helpers — source this file.
#   source references/mah.sh
# Data goes to stdout; pair codes and status to stderr. Works under bash and zsh.

MAH_PROFILE="${MAH_PROFILE:-myatriumhealth}"
MAH_BASE="https://my.atriumhealth.org/myatriumhealth"

# Fetch a page through the signed-in tab. $1 = path under /myatriumhealth.
mah_page() { fpx get "$MAH_BASE/${1#/}" -p "$MAH_PROFILE"; }

# True (0) when the session is alive. Two ways this lies if written naively:
#   1. MyChart answers an EXPIRED session with HTTP 200 whose body is the login
#      page, so the status code cannot be trusted.
#   2. An EMPTY body (no signed-in tab open for the bridge to relay through)
#      contains no login marker either — so a bare `grep -q login || return 0`
#      reports SIGNED IN for a response that never happened.
# Check for emptiness first, then for the login page.
mah_signed_in() {
  local page
  page="$(mah_page "Home" 2>/dev/null)"
  if [ -z "$page" ]; then
    echo "bridge returned nothing — open https://my.atriumhealth.org/ in Chrome (fpx relays through that tab)" >&2
    return 2
  fi
  # Also catch a two-factor / verification step-up, not just the login page.
  # This deployment has 2FA enabled, and an interstitial that is not the login
  # page would otherwise read as "signed in" and produce confusing failures
  # downstream. The exact step-up markup is unobserved, so the match is broad.
  # Match on the TITLE, never the body: every signed-in page links to two-factor
  # setup under Settings, so a body-wide *twoFactor* match reports "signed out"
  # for a perfectly good session (verified against the real Home page).
  local title
  title="$(printf %s "$page" | sed -n 's/.*<title>\([^<]*\)<\/title>.*/\1/p' | head -1)"
  # Keep these in step with isAuthWall() in src/client.ts. Matching two-factor
  # in the TITLE is safe; matching it in the BODY is not (see above).
  case "$title" in
    *"Login Page"*|*Verify*|*Verification*|*[Tt]wo-[Ff]actor*|*[Tt]wo\ [Ff]actor*|*twoFactor*) return 1 ;;
  esac
  case "$page" in
    *'name="verificationCode"'*) return 1 ;;
  esac
  return 0
}

# The 172-char ASP.NET antiforgery token from any signed-in page. Cache it:
#   export MAH_TOKEN="$(mah_token)"
mah_token() {
  { [ -n "$MAH_TOKEN" ] && printf %s "$MAH_TOKEN" && return 0; } 2>/dev/null
  local page
  page="$(mah_page "Home" 2>/dev/null)"
  [ -n "$page" ] || { echo "bridge returned nothing — is a signed-in my.atriumhealth.org tab open?" >&2; return 2; }
  printf %s "$page" \
    | perl -ne 'if (/name="__RequestVerificationToken"[^>]*value="([^"]+)"/) { print $1; exit }'
}

# The page CSP nonce ($$WPUtil.GetPageNonce), needed by the conversations
# endpoints. Only /app/* SPA pages carry one, and it is SINGLE-quoted.
# $1 = an /app/... path, e.g. app/communication-center
mah_nonce() {
  mah_page "${1:-app/communication-center}" 2>/dev/null \
    | perl -ne "if (/id='cspScripts'[^>]*nonce='([0-9a-f]{32})'/ || /id=\"cspScripts\"[^>]*nonce=\"([0-9a-f]{32})\"/) { print \$1 || \$2; exit }"
}

# mah_api <area/Action> [json-body]   — modern JSON endpoints. Default body {}.
mah_api() {
  local ep="$1" body="${2:-{\}}" tok
  tok="$(mah_token)"
  if [ -z "$tok" ]; then
    echo "no antiforgery token — sign in to MyAtriumHealth in Chrome, then retry" >&2
    return 2
  fi
  fpx request "$MAH_BASE/api/$ep" -p "$MAH_PROFILE" -X POST \
    -H "__RequestVerificationToken: $tok" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "$body"
}

# mah_legacy <Area/Controller/Action> [querystring] — older form-encoded endpoints.
mah_legacy() {
  local ep="$1" qs="$2" tok
  tok="$(mah_token)"
  [ -n "$tok" ] || { echo "no antiforgery token — sign in first" >&2; return 2; }
  fpx request "$MAH_BASE/$ep?${qs}${qs:+&}noCache=0.$RANDOM" -p "$MAH_PROFILE" -X POST \
    -H "__RequestVerificationToken: $tok" \
    -H "X-Requested-With: XMLHttpRequest" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d ''
}

# mah_messages [folderTag]  — Message Center conversations. Default folder 1 (inbox).
# Needs FIVE body keys; the fussy parts are the page CSP nonce and the fact that
# externalLoadParams must list the NON-local organizations only (including the
# local one, or handles taken from the visits response, returns HTTP 500).
mah_messages() {
  local tag="${1:-1}" nonce orgs
  # Same emptiness guard as mah_api/mah_legacy: a helper can exit 0 and print
  # nothing, and an empty nonce or org list silently produces a body the API
  # rejects with an opaque error.
  nonce="$(mah_nonce app/communication-center)"
  [ -n "$nonce" ] || { echo "no page nonce — is a signed-in my.atriumhealth.org tab open?" >&2; return 2; }
  orgs="$(mah_api conversations/GetOrganizations)"
  [ -n "$orgs" ] || { echo "could not read organizations — sign in and retry" >&2; return 2; }
  printf %s "$orgs" | python3 -c '
import json,sys
tag,nonce = sys.argv[1], sys.argv[2]
orgs = json.load(sys.stdin).get("organizations") or {}
load = {"loadStartInstantISO":"","loadEndInstantISO":"","pagingInfo":1}
ext  = {h:{"communicationCenter":dict(load)} for h,o in orgs.items() if not o.get("isLocal")}
print(json.dumps({"tag":int(tag),"localLoadParams":load,"externalLoadParams":ext,
                  "searchQuery":"","PageNonce":nonce}))' "$tag" "$nonce" \
    | { read -r body; mah_api conversations/GetConversationList "$body"; }
}

# mah_legacy_form <Area/Controller/Action> <urlencoded-form-body>
# Some legacy endpoints require a form BODY rather than query params — e.g.
# Insurance/Coverages/GetCoverages needs isStandAlone=true, and returns the
# "Oops!" error page without it.
mah_legacy_form() {
  local ep="$1" form="$2" tok
  # Guard on EMPTINESS, not just exit status: mah_token exits 0 while printing
  # nothing when the page loads but the token regex does not match.
  tok="$(mah_token)"
  [ -n "$tok" ] || { echo "no antiforgery token — sign in to MyAtriumHealth in Chrome, then retry" >&2; return 2; }
  fpx request "$MAH_BASE/$ep?noCache=0.$RANDOM" -p "$MAH_PROFILE" -X POST \
    -H "__RequestVerificationToken: $tok" \
    -H "X-Requested-With: XMLHttpRequest" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "$form"
}
