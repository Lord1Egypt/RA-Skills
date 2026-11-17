#!/usr/bin/env bash
# Start the browser session: one headed Chromium with a private persistent
# profile, a durable X display, a loopback-only screen-sharing stack, and a
# loopback CDP endpoint.
#
# The session outlives this invocation and outlives any login handoff. It is
# stopped with stop_line_oa_chromium.sh, never by the handoff.
#
# This script never logs in to LINE and never handles credentials.
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/session.sh
source "$script_dir/lib/session.sh"
# shellcheck source=lib/ports.sh
source "$script_dir/lib/ports.sh"
# shellcheck source=lib/phase_timing.sh
source "$script_dir/lib/phase_timing.sh"
# shellcheck source=lib/caddy.sh
source "$script_dir/lib/caddy.sh"

profile_dir="${LINE_OA_SEND_CHAT_CHROMIUM_PROFILE:-/opt/data/chromium}"
profile_dir_source="LINE_OA_SEND_CHAT_CHROMIUM_PROFILE (or fallback /opt/data/chromium)"
chromium_bin="${LINE_OA_CHROMIUM:-}"
cdp_port="9222"
display="${DISPLAY:-}"
ready_timeout="${LINE_OA_SEND_CHAT_READY_TIMEOUT:-60}"

usage() {
  cat <<'EOF'
Usage: start_line_oa_chromium.sh [options]

Start the browser session: a headed Chromium with a persistent profile, a
durable X display, a loopback-only screen-sharing stack, and loopback CDP.
The profile comes from LINE_OA_SEND_CHAT_CHROMIUM_PROFILE, falling back to
/opt/data/chromium. The directory is created with mode 700 when absent.

Options:
  --profile-dir DIR       Override the environment-selected profile directory
  --chromium PATH         Chromium executable (or set LINE_OA_CHROMIUM)
  --cdp-port PORT         Loopback CDP port (default: 9222)
  --display DISPLAY       Use an existing X display instead of starting one
  -h, --help              Show this help

The session is left running in the background and recorded in a state file.
Stop it with stop_line_oa_chromium.sh.
EOF
}

die() { printf 'ERROR: %s\n' "$*" >&2; exit 2; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile-dir) profile_dir="${2:-}"; profile_dir_source="--profile-dir"; shift 2 ;;
    --chromium) chromium_bin="${2:-}"; shift 2 ;;
    --cdp-port) cdp_port="${2:-}"; shift 2 ;;
    --display) display="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

[[ "$cdp_port" =~ ^[0-9]{1,5}$ ]] && (( cdp_port > 0 && cdp_port < 65536 )) || die "--cdp-port must be 1-65535"

phase_init session
phase_mark script_entry

# The session guard runs first, ahead of display setup. It is the cheapest and
# most meaningful check, and putting it behind Xvfb meant a second start with no
# DISPLAY reported "could not start private Xvfb display" -- true, but not the
# reason. Attach mode makes this the first thing that should run.
if curl --max-time 2 -fsS "http://127.0.0.1:${cdp_port}/json/version" >/dev/null 2>&1; then
  die "a browser session is already reachable on 127.0.0.1:${cdp_port}; reuse it instead of starting another Chromium."
fi
if session_is_live; then
  die "a browser session is already recorded and live; reuse it instead of starting another Chromium."
fi
phase_mark session_guard

# Name every missing session dependency at once. Reporting them one failure at a
# time turns provisioning into a guessing game, and x11vnc/websockify/caddy
# would otherwise surface only as a confusing "did not listen" timeout.
missing=()
for command in x11vnc websockify caddy; do
  command -v "$command" >/dev/null 2>&1 || missing+=("$command")
done
[[ -n "$display" ]] || command -v Xvfb >/dev/null 2>&1 || missing+=("Xvfb")
if ((${#missing[@]})); then
  printf 'ERROR: missing browser-session dependencies: %s\n' "${missing[*]}" >&2
  printf 'Install commands (run by an identity with host package permission; no sudo is invoked by this skill):\n' >&2
  printf '  apt-get update && apt-get install -y xvfb x11vnc novnc websockify caddy\n' >&2
  exit 2
fi

[[ -n "$profile_dir" ]] || die "profile directory is empty; set LINE_OA_SEND_CHAT_CHROMIUM_PROFILE or pass --profile-dir."
if [[ ! -e "$profile_dir" ]]; then
  umask 077
  mkdir -p -- "$profile_dir"
  chmod 700 -- "$profile_dir"
  printf 'Created private Chromium profile directory from %s: %s\n' "$profile_dir_source" "$profile_dir"
fi
[[ -d "$profile_dir" && -r "$profile_dir" && -w "$profile_dir" ]] || die "profile path must be a readable/writable directory: $profile_dir"

# A SingletonLock left by a hard-killed Chromium records the hostname that held
# it. When the hostname no longer matches, Chromium refuses the profile as in
# use "on another computer" and the launch failure looks generic. Clear a lock
# only when it is demonstrably stale: same host, and the recorded PID is gone.
lock="$profile_dir/SingletonLock"
if [[ -L "$lock" ]]; then
  target="$(readlink "$lock" || true)"           # form: <hostname>-<pid>
  lock_host="${target%-*}"
  lock_pid="${target##*-}"
  if [[ "$lock_host" == "$(hostname)" && "$lock_pid" =~ ^[0-9]+$ ]] && ! kill -0 "$lock_pid" 2>/dev/null; then
    rm -f "$lock" "$profile_dir/SingletonCookie" "$profile_dir/SingletonSocket"
    printf 'Cleared a stale profile lock left by process %s on this host.\n' "$lock_pid"
  elif [[ "$lock_host" != "$(hostname)" ]]; then
    die "the profile is locked by host '${lock_host}' (this host is '$(hostname)'). A Chromium elsewhere may still hold it, or it was hard-killed under a different hostname. Verify no other Chromium uses ${profile_dir}, then remove ${lock}."
  fi
fi

if [[ -z "$chromium_bin" ]]; then
  for candidate in chromium chromium-browser google-chrome google-chrome-stable; do
    if command -v "$candidate" >/dev/null 2>&1; then
      chromium_bin="$(command -v "$candidate")"
      break
    fi
  done
fi
if [[ -z "$chromium_bin" && -n "${LINE_OA_SEND_CHAT_BROWSER_DIR:-}" && -d "$LINE_OA_SEND_CHAT_BROWSER_DIR" ]]; then
  chromium_bin="$(find "$LINE_OA_SEND_CHAT_BROWSER_DIR" -type f -path '*/chrome-linux*/chrome' -perm -u+x -print -quit 2>/dev/null || true)"
fi
[[ -n "$chromium_bin" && -x "$chromium_bin" ]] || die "Chromium was not found. Set LINE_OA_CHROMIUM, install a system Chromium, or run scripts/setup_line_oa_runtime.sh and export LINE_OA_SEND_CHAT_BROWSER_DIR."

runtime_dir="$(session_runtime_dir)"
mkdir -p "$runtime_dir/logs"
chmod 700 "$runtime_dir" "$runtime_dir/logs"

# The display is owned by the session, not by a single Chromium invocation, so
# it is never trapped to this script's exit.
xvfb_pid=""
owns_display=0
if [[ -z "$display" ]]; then
  command -v Xvfb >/dev/null 2>&1 || die "a headed display is required and Xvfb is unavailable. Install Xvfb or pass --display / set DISPLAY."
  display="${LINE_OA_SEND_CHAT_XVFB_DISPLAY:-:99}"
  x_display_in_use "$display" && die "display $display is already in use; choose another with LINE_OA_SEND_CHAT_XVFB_DISPLAY."
  setsid Xvfb "$display" -screen 0 1280x800x24 -nolisten tcp >"$runtime_dir/logs/xvfb.log" 2>&1 &
  xvfb_pid="$!"
  owns_display=1
  wait_for_x_display "$display" 10 \
    || die "display $display did not become connectable; see $runtime_dir/logs/xvfb.log"
  printf 'Started X display %s for this session.\n' "$display"
fi
phase_mark display_ready

# Chromium refuses to run as root with its sandbox enabled. Running unprivileged
# is the fix; disabling the sandbox is an escape hatch for deployments that
# cannot, and it is deliberately explicit because the cost is real: a login
# handoff grants interactive control, so someone holding the URL can navigate
# this browser anywhere, and an unsandboxed renderer contains far less when they
# do. That browser also holds the authenticated LINE session.
sandbox_args=()
if [[ "${LINE_OA_SEND_CHAT_ALLOW_NO_SANDBOX:-}" == "1" ]]; then
  sandbox_args=(--no-sandbox)
  printf 'WARNING: starting Chromium with --no-sandbox (LINE_OA_SEND_CHAT_ALLOW_NO_SANDBOX=1).\n' >&2
  printf 'WARNING: the renderer sandbox is disabled. Prefer running as an unprivileged user.\n' >&2
  printf 'WARNING: while a handoff is armed, whoever holds the URL can browse anywhere in this browser.\n' >&2
elif [[ "$(id -u)" == "0" ]]; then
  die "Chromium will not run as root with its sandbox enabled.
  Preferred: run as an unprivileged user that owns the profile directory, e.g.
    useradd --create-home --uid 1000 lineoa
    chown -R lineoa:lineoa $profile_dir
    su - lineoa -c 'cd $PWD && bash scripts/start_line_oa_chromium.sh'
  If this deployment cannot drop privileges, opt in explicitly:
    LINE_OA_SEND_CHAT_ALLOW_NO_SANDBOX=1 bash scripts/start_line_oa_chromium.sh
  That disables the renderer sandbox. See references/handoff-operations.md."
fi

setsid env DISPLAY="$display" "$chromium_bin" \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port="$cdp_port" \
  --remote-allow-origins='*' \
  --user-data-dir="$profile_dir" \
  --no-first-run \
  --no-default-browser-check \
  ${sandbox_args[@]+"${sandbox_args[@]}"} \
  https://chat.line.biz/ >"$runtime_dir/logs/chromium.log" 2>&1 &
chromium_pid="$!"
phase_mark chromium_spawned

cdp_url="http://127.0.0.1:${cdp_port}"
deadline_reached=1
for _ in $(seq 1 $(( ready_timeout * 5 )) ); do
  if curl --max-time 2 -fsS "${cdp_url}/json/version" >/dev/null 2>&1; then
    deadline_reached=0
    break
  fi
  kill -0 "$chromium_pid" 2>/dev/null || break
  sleep 0.2
done
if (( deadline_reached )); then
  kill "$chromium_pid" 2>/dev/null || true
  (( owns_display )) && kill "$xvfb_pid" 2>/dev/null
  die "Chromium did not expose CDP on ${cdp_url}; see $runtime_dir/logs/chromium.log"
fi
phase_mark cdp_reachable

# The LINE page is a separate phase from CDP: the browser can be answering
# debugger requests well before it has finished loading a page, and the gap
# between the two is exactly what a cold-start measurement needs to see.
for _ in $(seq 1 $(( ready_timeout * 5 )) ); do
  if curl --max-time 2 -fsS "${cdp_url}/json/list" 2>/dev/null | grep -q 'line\.biz'; then
    break
  fi
  sleep 0.2
done
phase_mark line_page_present

# The loopback screen-sharing stack starts with the session. Nothing here is
# externally reachable: an external route exists only while cloudflared runs,
# which is the handoff's job alone.
read -r vnc_port websockify_port caddy_port caddy_admin_port <<<"$(pick_loopback_ports 4 5900 6999)"

x11vnc -display "$display" -localhost -nopw -forever -shared \
  -noxrecord -noxfixes -noxdamage -rfbport "$vnc_port" \
  >"$runtime_dir/logs/x11vnc.log" 2>&1 &
vnc_pid="$!"
wait_for_tcp "$vnc_port" 10 || die "x11vnc did not listen on 127.0.0.1:${vnc_port}; see $runtime_dir/logs/x11vnc.log"
phase_mark x11vnc_listening

novnc_root=""
for candidate in /usr/share/novnc /usr/share/noVNC; do
  [[ -d "$candidate" ]] && { novnc_root="$candidate"; break; }
done
[[ -n "$novnc_root" ]] || die "noVNC web assets were not found."

websockify --web "$novnc_root" "127.0.0.1:$websockify_port" "127.0.0.1:$vnc_port" \
  >"$runtime_dir/logs/websockify.log" 2>&1 &
websockify_pid="$!"
wait_for_tcp "$websockify_port" 10 || die "websockify did not listen on 127.0.0.1:${websockify_port}; see $runtime_dir/logs/websockify.log"
phase_mark websockify_listening

# The front end starts closed: 404 to everything until a handoff arms a token
# route. Its port is selected like the others rather than hard-coded, and its
# output is kept so a bind failure is reported instead of surfacing later as a
# blank page behind a working tunnel URL.
caddy_config="$runtime_dir/Caddyfile"
caddy_write_closed "$caddy_config" "$caddy_port" "$caddy_admin_port"
caddy run --config "$caddy_config" --adapter caddyfile \
  >"$runtime_dir/logs/caddy.log" 2>&1 &
caddy_pid="$!"
wait_for_tcp "$caddy_port" 15 || die "Caddy did not listen on 127.0.0.1:${caddy_port}; see $runtime_dir/logs/caddy.log"
phase_mark caddy_listening

session_write \
  "display=$display" \
  "owns_display=$owns_display" \
  "xvfb_pid=$xvfb_pid" \
  "profile_dir=$profile_dir" \
  "cdp_url=$cdp_url" \
  "cdp_port=$cdp_port" \
  "chromium_pid=$chromium_pid" \
  "vnc_port=$vnc_port" \
  "vnc_pid=$vnc_pid" \
  "websockify_port=$websockify_port" \
  "websockify_pid=$websockify_pid" \
  "caddy_port=$caddy_port" \
  "caddy_admin_port=$caddy_admin_port" \
  "caddy_pid=$caddy_pid" \
  "caddy_config=$caddy_config" \
  "novnc_root=$novnc_root" \
  "runtime_dir=$runtime_dir" \
  "hostname=$(hostname)"
phase_mark session_recorded

printf 'Browser session ready.\n'
printf '  display: %s\n' "$display"
printf '  profile: %s\n' "$profile_dir"
printf '  CDP:     %s (loopback only)\n' "$cdp_url"
printf '  state:   %s\n' "$(session_state_path)"
printf 'Nothing is externally reachable. A login handoff is armed separately.\n'
phase_summary
