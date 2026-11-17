#!/usr/bin/env bash
# Browser-session state: where it lives, how it is written, and how a caller
# decides whether it is real. Sourced, not executed.
#
# The state file is what lets the handoff attach to a running session instead of
# starting its own browser. It records no secret: paths, ports, PIDs, and a
# display number only.

[[ -n "${__LINE_OA_SESSION_LOADED:-}" ]] && return 0
__LINE_OA_SESSION_LOADED=1

session_runtime_dir() {
  printf '%s' "${LINE_OA_SEND_CHAT_RUNTIME_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/line-oa-chat-send}"
}

session_state_path() { printf '%s/session.env' "$(session_runtime_dir)"; }
session_handoff_path() { printf '%s/handoff.env' "$(session_runtime_dir)"; }

# session_write key=value ...
session_write() {
  local dir state
  dir="$(session_runtime_dir)"
  state="$(session_state_path)"
  mkdir -p "$dir"
  chmod 700 "$dir"
  : > "$state"
  chmod 600 "$state"
  local pair
  for pair in "$@"; do
    printf '%s\n' "$pair" >> "$state"
  done
}

# session_get <key> [file]  -- parsed, never sourced or eval'd.
session_get() {
  local key="$1" file="${2:-$(session_state_path)}"
  [[ -f "$file" ]] || return 1
  local line
  line="$(grep -m1 -E "^${key}=" "$file" 2>/dev/null)" || return 1
  printf '%s' "${line#*=}"
}

session_state_exists() { [[ -f "$(session_state_path)" ]]; }

# session_is_live
# A recorded session counts as present only when its display and its CDP
# endpoint both respond. A state file left behind by a crash is not a session,
# and attaching to one would put a handoff in front of a dead display.
session_is_live() {
  local state display cdp num
  state="$(session_state_path)"
  [[ -f "$state" ]] || return 1

  display="$(session_get display "$state")" || return 1
  num="${display#:}"; num="${num%%.*}"
  [[ -S "/tmp/.X11-unix/X${num}" ]] || return 1

  cdp="$(session_get cdp_url "$state")" || return 1
  curl --max-time 2 -fsS "${cdp}/json/version" >/dev/null 2>&1 || return 1

  return 0
}

# session_require_live -- emits the standard remediation when absent.
session_require_live() {
  if session_is_live; then
    return 0
  fi
  if session_state_exists; then
    printf 'ERROR: a session state file exists but the session is not live (stale display or CDP endpoint).\n' >&2
    printf 'Start a browser session first: bash scripts/start_line_oa_chromium.sh\n' >&2
  else
    printf 'ERROR: no browser session is running.\n' >&2
    printf 'Start one first: bash scripts/start_line_oa_chromium.sh\n' >&2
  fi
  return 1
}

session_clear() { rm -f "$(session_state_path)"; }

# session_looks_authenticated [samples]
# Whether the running session has a logged-in LINE OA page.
#
# Sampled over time rather than read once: a freshly started session opens
# chat.line.biz and only then redirects to the login screen, so a single
# instantaneous read can catch the pre-redirect moment and call an
# unauthenticated browser authenticated. Any login indicator in any sample
# settles it, so the answer errs toward "not authenticated" -- the safe
# direction for both callers. doctor.sh uses it to choose a verdict, and
# measure_handoff.sh uses it to refuse to expose a live account.
session_looks_authenticated() {
  local samples="${1:-5}" cdp pages saw_login=0 saw_chat=0 i
  cdp="$(session_get cdp_url 2>/dev/null || printf 'http://127.0.0.1:9222')"
  curl --max-time 3 -fsS "${cdp}/json/version" >/dev/null 2>&1 || return 1
  for (( i = 0; i < samples; i++ )); do
    pages="$(curl --max-time 5 -fsS "${cdp}/json/list" 2>/dev/null || true)"
    grep -qE 'account\.line\.biz|/login\?|LINE Business ID' <<<"$pages" && saw_login=1
    grep -q 'chat\.line\.biz' <<<"$pages" && saw_chat=1
    (( saw_login )) && return 1
    (( i + 1 < samples )) && sleep 1
  done
  (( saw_chat )) || return 1
  return 0
}

handoff_is_armed() {
  local file pid
  file="$(session_handoff_path)"
  [[ -f "$file" ]] || return 1
  pid="$(session_get tunnel_pid "$file")" || return 1
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}
