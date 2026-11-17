#!/usr/bin/env bash
# Environment preflight: report whether this host can perform a message send.
#
# Every check asserts the capability, not the presence of a command: that the
# interpreter imports Playwright, that the browser binary is executable, that
# the profile directory is writable, that the endpoint answers. A command on
# PATH proves none of those.
#
# Exit 0 only when a send can actually run. A missing LINE login is reported as
# its own verdict, not as a broken environment -- it is a security checkpoint,
# and treating it as an install failure sends people to fix the wrong thing.
set -uo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/session.sh
source "$script_dir/lib/session.sh"

profile_dir="${LINE_OA_SEND_CHAT_CHROMIUM_PROFILE:-/opt/data/chromium}"
cdp_port="${LINE_OA_SEND_CHAT_CDP_PORT:-9222}"
cdp_url="http://127.0.0.1:${cdp_port}"

blockers=0
auth_required=0

ok()    { printf '  \033[32mok\033[0m       %s\n' "$1"; }
warn()  { printf '  \033[33mattn\033[0m     %s\n' "$1"; }
bad()   { printf '  \033[31mMISSING\033[0m  %s\n' "$1"; blockers=$((blockers + 1)); }
fix()   { printf '           → %s\n' "$1"; }

printf '\nLINE OA environment preflight\n\n'

# --- Python runtime -----------------------------------------------------------
printf 'Runtime\n'
# Checked in the order run_line_oa_chat.sh resolves them, so this reports what
# the launcher will actually do rather than what is merely installed.
python_bin=""
if [[ -n "${LINE_OA_PYTHON:-}" && -x "${LINE_OA_PYTHON}" ]] && "$LINE_OA_PYTHON" -c 'import playwright' >/dev/null 2>&1; then
  python_bin="$LINE_OA_PYTHON"
else
  for candidate in "${PYTHON:-}" python3 python; do
    [[ -n "$candidate" ]] || continue
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import playwright' >/dev/null 2>&1; then
      python_bin="$(command -v "$candidate")"
      break
    fi
  done
fi

# The location setup_line_oa_runtime.sh provisions. The launcher does not look
# here on its own, so finding it and reporting the export is the difference
# between "works, slowly, via uv" and "works directly".
provisioned="$(session_runtime_dir)/venv/bin/python"

if [[ -n "$python_bin" ]]; then
  ok "Python with Playwright: $python_bin"
elif [[ -x "$provisioned" ]] && "$provisioned" -c 'import playwright' >/dev/null 2>&1; then
  warn 'a provisioned runtime exists but LINE_OA_PYTHON is not exported'
  fix "export LINE_OA_PYTHON=$provisioned"
  fix 'without it the launcher falls back to uv, which works but re-resolves Playwright each run'
elif command -v uv >/dev/null 2>&1; then
  warn 'no Python has Playwright, but uv can supply one on demand'
  fix 'faster and more predictable: bash scripts/setup_line_oa_runtime.sh --runtime-dir <private-dir> --skip-browser-install'
  fix 'then: export LINE_OA_PYTHON=<private-dir>/venv/bin/python'
else
  bad 'no Python runtime with Playwright, and uv is unavailable'
  fix 'install uv, then: bash scripts/setup_line_oa_runtime.sh --runtime-dir <private-dir> --skip-browser-install'
  fix 'then: export LINE_OA_PYTHON=<private-dir>/venv/bin/python'
fi

# --- Browser ------------------------------------------------------------------
printf '\nBrowser\n'
chromium_bin="${LINE_OA_CHROMIUM:-}"
if [[ -z "$chromium_bin" ]]; then
  for candidate in chromium chromium-browser google-chrome google-chrome-stable; do
    command -v "$candidate" >/dev/null 2>&1 && { chromium_bin="$(command -v "$candidate")"; break; }
  done
fi
if [[ -n "$chromium_bin" && -x "$chromium_bin" ]]; then
  ok "Chromium executable: $chromium_bin"
else
  bad 'no executable Chromium found'
  fix 'set LINE_OA_CHROMIUM, or install a system Chromium (apt-get install -y chromium chromium-sandbox)'
fi

if [[ -d "$profile_dir" ]]; then
  if [[ -r "$profile_dir" && -w "$profile_dir" ]]; then
    ok "profile directory is readable and writable: $profile_dir"
  else
    bad "profile directory is not readable/writable: $profile_dir"
    fix 'fix its ownership so the automation identity owns it, mode 700'
  fi
else
  warn "profile directory does not exist yet: $profile_dir"
  fix 'it is created with mode 700 on the first session start'
fi

# --- Session dependencies -----------------------------------------------------
printf '\nSession dependencies\n'
session_missing=()
for command in Xvfb x11vnc websockify caddy; do
  command -v "$command" >/dev/null 2>&1 || session_missing+=("$command")
done
novnc_root=""
for candidate in /usr/share/novnc /usr/share/noVNC; do
  [[ -d "$candidate" ]] && { novnc_root="$candidate"; break; }
done
[[ -n "$novnc_root" ]] || session_missing+=("novnc-assets")
if ((${#session_missing[@]})); then
  bad "missing: ${session_missing[*]}"
  fix 'run by an identity with host package permission (this skill invokes no package manager and no sudo):'
  fix 'apt-get update && apt-get install -y xvfb x11vnc novnc websockify caddy'
else
  ok 'display, VNC, websockify, noVNC assets, and the HTTP front end are present'
fi

# --- Handoff dependency -------------------------------------------------------
printf '\nLogin handoff dependency\n'
if command -v cloudflared >/dev/null 2>&1; then
  ok 'cloudflared is present'
else
  warn 'cloudflared is absent; sending still works, only the login handoff is unavailable'
  fix 'run by an identity with host package permission:'
  fix 'curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg -o /usr/share/keyrings/cloudflare-main.gpg'
  fix 'printf "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main\n" > /etc/apt/sources.list.d/cloudflared.list'
  fix 'apt-get update && apt-get install -y cloudflared'
fi

# --- Live session -------------------------------------------------------------
printf '\nBrowser session\n'
cdp_live=0
if curl --max-time 3 -fsS "${cdp_url}/json/version" >/dev/null 2>&1; then
  cdp_live=1
  ok "CDP endpoint responds: $cdp_url (loopback only)"
else
  warn "no session is running (CDP endpoint $cdp_url does not respond)"
  fix 'start one: bash scripts/start_line_oa_chromium.sh'
fi

if session_state_exists; then
  if session_is_live; then
    ok "session state is live: $(session_state_path)"
  else
    warn 'a session state file exists but the session is not live (stale)'
    fix 'start a fresh session: bash scripts/start_line_oa_chromium.sh'
  fi
fi

# --- Authentication -----------------------------------------------------------
# Deliberately its own verdict. An environment that is entirely healthy but not
# logged in is not broken, and reporting it as broken sends people to reinstall
# things that are already fine.
printf '\nLINE authentication\n'
if (( cdp_live )); then
  # Shared with measure_handoff.sh, which refuses to run against a logged-in
  # profile. One detection, one place: writing it twice already produced two
  # copies of the same redirect race.
  if session_looks_authenticated; then
    ok 'an authenticated LINE OA Chat page is open'
  else
    auth_required=1
    warn 'the environment is usable, but LINE authentication is required'
    fix 'this is a security checkpoint, not an installation failure'
    fix 'the user completes login themselves through the handoff:'
    fix 'export LINE_OA_SEND_CHAT_HANDOFF_PURPOSE=line-login'
    fix 'bash scripts/start_line_oa_vnc_handoff.sh'
  fi
else
  auth_required=1
  warn 'cannot be determined without a running session'
fi

# --- Verdict ------------------------------------------------------------------
printf '\n'
if (( blockers > 0 )); then
  printf 'VERDICT: environment NOT usable (%d blocker(s) above).\n\n' "$blockers"
  exit 1
fi
if (( auth_required )); then
  printf 'VERDICT: environment usable; LINE authentication required.\n\n'
  exit 3
fi
printf 'VERDICT: environment usable; a message send can run.\n\n'
exit 0
