#!/usr/bin/env bash
# Stop the browser session.
#
# Resolves what to stop from the recorded session state, never from a process
# name pattern or a fixed path. The persistent profile is left untouched: it
# holds the retained LINE session and a later start reuses it.
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/session.sh
source "$script_dir/lib/session.sh"

graceful_timeout="${LINE_OA_SEND_CHAT_SHUTDOWN_TIMEOUT:-20}"

if ! session_state_exists; then
  printf 'No session state found; nothing to stop.\n'
  exit 0
fi

state="$(session_state_path)"
chromium_pid="$(session_get chromium_pid "$state" || true)"
profile_dir="$(session_get profile_dir "$state" || true)"
cdp_url="$(session_get cdp_url "$state" || true)"
display="$(session_get display "$state" || true)"
owns_display="$(session_get owns_display "$state" || echo 0)"

# A tunnel outliving the browser it points at would be the worst possible
# leftover, so the handoff goes first.
if handoff_is_armed; then
  printf 'Revoking the armed handoff before stopping the session...\n'
  bash "$script_dir/stop_line_oa_vnc_handoff.sh" || true
fi

# Graceful termination of the recorded root process, then wait. No forced kill:
# on timeout this reports the blocker and stops, because escalating is a
# decision for whoever is watching, not for this script.
if [[ -n "$chromium_pid" ]] && kill -0 "$chromium_pid" 2>/dev/null; then
  printf 'Stopping Chromium (pid %s)...\n' "$chromium_pid"
  kill -TERM "$chromium_pid" 2>/dev/null || true
  waited=0
  while kill -0 "$chromium_pid" 2>/dev/null; do
    waited="$(awk -v w="$waited" 'BEGIN{printf "%.1f", w+0.2}')"
    if awk -v w="$waited" -v d="$graceful_timeout" 'BEGIN{exit !(w>=d)}'; then
      printf 'ERROR: Chromium (pid %s) did not exit within %ss.\n' "$chromium_pid" "$graceful_timeout" >&2
      printf 'Reporting rather than forcing a kill. Inspect the process, then decide.\n' >&2
      printf 'The session state file was left in place: %s\n' "$state" >&2
      exit 2
    fi
    sleep 0.2
  done
  printf 'Chromium exited.\n'
fi

for component in caddy_pid websockify_pid vnc_pid; do
  pid="$(session_get "$component" "$state" || true)"
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    kill -TERM "$pid" 2>/dev/null || true
  fi
done

if [[ "$owns_display" == "1" ]]; then
  xvfb_pid="$(session_get xvfb_pid "$state" || true)"
  if [[ -n "$xvfb_pid" ]] && kill -0 "$xvfb_pid" 2>/dev/null; then
    kill -TERM "$xvfb_pid" 2>/dev/null || true
  fi
  printf 'Stopped the display this session started (%s).\n' "$display"
fi

if [[ -n "$cdp_url" ]]; then
  if curl --max-time 3 -fsS "${cdp_url}/json/version" >/dev/null 2>&1; then
    printf 'ERROR: the CDP endpoint %s is still reachable after shutdown.\n' "$cdp_url" >&2
    exit 2
  fi
  printf 'CDP endpoint is unreachable, as expected.\n'
fi

# Chromium normally removes its own lock on a graceful exit. Clearing a lock it
# left behind here means the next start is not refused as "in use on another
# computer" -- and it is safe precisely because the process is confirmed gone.
if [[ -n "$profile_dir" && -L "$profile_dir/SingletonLock" ]]; then
  rm -f "$profile_dir/SingletonLock" "$profile_dir/SingletonCookie" "$profile_dir/SingletonSocket"
  printf 'Cleared the profile lock left by the stopped session.\n'
fi

session_clear
printf 'Session stopped. The persistent profile is unchanged: %s\n' "$profile_dir"
