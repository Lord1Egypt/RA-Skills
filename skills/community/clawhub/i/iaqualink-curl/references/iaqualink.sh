# shellcheck shell=bash
# iAqualink from a shell — source me (bash or zsh):   . references/iaqualink.sh
#
# DERIVED FROM iaqualink-py 0.7.0, PARTLY VERIFIED LIVE. Every endpoint, header
# and body below is transcribed from the open-source client Home Assistant uses
# (see the repo's docs/IAQUALINK-API.md). Sign-in, devices.json and the iAqua
# get_home / get_devices reads have been seen working on a real panel; the eXO
# shadow read has not.
#
# Credentials come from the macOS Keychain item with service "iaqualink":
#   security add-generic-password -s iaqualink -a 'you@example.com' -w
# (the account attribute is the email, the password is the secret). For a dry
# run or a test, IAQ_EMAIL / IAQ_PASSWORD override the Keychain.
#
# IAQ_DRY_RUN=1 prints each request (password redacted) instead of sending it.
#
# State: this helper's OWN session file, $IAQ_SESSION (default
# ~/.iaqualink-curl/session.json, mode 600). It is NOT shared with the
# iaqualink-mcp server, which keeps its session in memory only.

IAQ_API_KEY='EOOEMOW4YR6QNB07'
IAQ_UA='okhttp/3.14.7'
IAQ_SESSION="${IAQ_SESSION:-$HOME/.iaqualink-curl/session.json}"

iaq_email() {
  if [ -n "${IAQ_EMAIL:-}" ]; then printf '%s' "$IAQ_EMAIL"; return 0; fi
  security find-generic-password -s iaqualink 2>/dev/null | awk -F'"' '/"acct"<blob>=/{print $4}'
}

iaq_password() {
  if [ -n "${IAQ_PASSWORD:-}" ]; then printf '%s' "$IAQ_PASSWORD"; return 0; fi
  security find-generic-password -s iaqualink -w 2>/dev/null
}

# _iaq_curl <args...>: run curl, or print it when IAQ_DRY_RUN=1. Bodies always
# arrive on stdin (--data @-) so the password never appears in `ps`.
_iaq_curl() {
  if [ "${IAQ_DRY_RUN:-}" = "1" ]; then
    printf 'curl'; printf ' %q' "$@"; printf '\n'
    case " $* " in
      *" @- "*) printf '  body: '; jq -c 'if has("password") then .password = "[redacted]" else . end' ;;
    esac
    return 0
  fi
  curl -sS --fail-with-body -H "user-agent: $IAQ_UA" -H 'content-type: application/json' "$@"
}

_iaq_get() { jq -r --arg k "$1" '.[$k] // empty' "$IAQ_SESSION"; }

# Sign in ONCE. A 401 means the email/password is wrong — fix it, do NOT loop:
# repeated failed sign-ins are how accounts get locked.
iaq_login() {
  local email pw out
  email=$(iaq_email); pw=$(iaq_password)
  if [ -z "$email" ] || [ -z "$pw" ]; then
    echo 'iaq_login: no credential — add the Keychain item (see the header) or set IAQ_EMAIL/IAQ_PASSWORD' >&2
    return 2
  fi
  if [ "${IAQ_DRY_RUN:-}" = "1" ]; then
    jq -n --arg k "$IAQ_API_KEY" --arg e "$email" --arg p "$pw" '{api_key:$k,email:$e,password:$p}' |
      _iaq_curl -X POST https://prod.zodiac-io.com/users/v1/login --data @-
    return 0
  fi
  out=$(jq -n --arg k "$IAQ_API_KEY" --arg e "$email" --arg p "$pw" '{api_key:$k,email:$e,password:$p}' |
    _iaq_curl -X POST https://prod.zodiac-io.com/users/v1/login --data @-) || {
    echo 'iaq_login: refused — check the email/password; not retrying' >&2
    return 1
  }
  mkdir -p "$(dirname "$IAQ_SESSION")"
  (umask 077 && printf '%s' "$out" | jq --arg e "$email" '{
      email: $e, user_id: (.id|tostring), authentication_token, session_id,
      id_token: .userPoolOAuth.IdToken, refresh_token: .userPoolOAuth.RefreshToken }' > "$IAQ_SESSION")
  echo "signed in; session saved to $IAQ_SESSION" >&2
}

# Refresh the tokens (no api_key on this endpoint). On a 401, run iaq_login.
iaq_refresh() {
  local out
  out=$(jq -n --arg e "$(_iaq_get email)" --arg r "$(_iaq_get refresh_token)" '{email:$e,refresh_token:$r}' |
    _iaq_curl -X POST https://prod.zodiac-io.com/users/v1/refresh --data @-) || return 1
  [ "${IAQ_DRY_RUN:-}" = "1" ] && { printf '%s\n' "$out"; return 0; }
  local tmp="$IAQ_SESSION.tmp"
  (umask 077 && jq --argjson n "$out" '. + {authentication_token: $n.authentication_token,
      session_id: $n.session_id, id_token: $n.userPoolOAuth.IdToken,
      refresh_token: ($n.userPoolOAuth.RefreshToken // .refresh_token)}' "$IAQ_SESSION" > "$tmp") &&
    mv "$tmp" "$IAQ_SESSION"
}

# The systems on the account: serial_number, name, device_type (iaqua | exo | …).
iaq_devices() {
  _iaq_curl "https://r-api.iaqualink.net/devices.json?api_key=$IAQ_API_KEY&authentication_token=$(_iaq_get authentication_token)&user_id=$(_iaq_get user_id)"
}

# iaq_command <serial> <command> [extra query, e.g. 'temp1=100&temp2=84']
# Reads: get_home, get_devices. Writes are TOGGLES (set_pool_pump, set_aux_3, …):
# read get_home first and only send when the state differs.
iaq_command() {
  local serial="$1" cmd="$2" extra="${3:+$3&}"
  _iaq_curl -H "Authorization: Bearer $(_iaq_get id_token)" -H "api_key: $IAQ_API_KEY" \
    "https://r-api.iaqualink.net/v2/mobile/session.json?${extra}actionID=command&command=$cmd&serial=$serial&sessionID=$(_iaq_get session_id)"
}

iaq_home()    { iaq_command "$1" get_home; }
iaq_auxes()   { iaq_command "$1" get_devices; }

# eXO chlorinators: the device shadow. Authorization is the raw IdToken (no "Bearer").
iaq_shadow() {
  _iaq_curl -H "Authorization: $(_iaq_get id_token)" "https://prod.zodiac-io.com/devices/v1/$1/shadow"
}
