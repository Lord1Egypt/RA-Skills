#!/usr/bin/env bash
# Revoke a login handoff.
#
# This removes external reachability only. Chromium, its display, and its
# authenticated profile keep running, so a send can follow immediately and a
# later re-authentication needs no browser restart.
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/session.sh
source "$script_dir/lib/session.sh"
# shellcheck source=lib/caddy.sh
source "$script_dir/lib/caddy.sh"

handoff_file="$(session_handoff_path)"
quiet=0
[[ "${1:-}" == "--quiet" ]] && quiet=1
say() { (( quiet )) || printf '%s\n' "$*"; }

if [[ ! -f "$handoff_file" ]]; then
  say 'No handoff is armed; nothing to revoke.'
  exit 0
fi

tunnel_pid="$(session_get tunnel_pid "$handoff_file" || true)"
ttl_pid="$(session_get ttl_pid "$handoff_file" || true)"

# Stop the tunnel first: that is what makes the browser externally reachable.
# Closing the route afterwards is belt and braces.
if [[ -n "$tunnel_pid" ]] && kill -0 "$tunnel_pid" 2>/dev/null; then
  kill -TERM "$tunnel_pid" 2>/dev/null || true
  for _ in $(seq 1 25); do
    kill -0 "$tunnel_pid" 2>/dev/null || break
    sleep 0.2
  done
  kill -0 "$tunnel_pid" 2>/dev/null && kill -KILL "$tunnel_pid" 2>/dev/null || true
  say 'Tunnel stopped; the browser is no longer externally reachable.'
fi

if [[ -n "$ttl_pid" ]] && kill -0 "$ttl_pid" 2>/dev/null; then
  kill -TERM "$ttl_pid" 2>/dev/null || true
fi

# Close the front end back to 404. Only possible when a session is still
# running; if the session is gone the route died with it.
caddy_config="$(session_get caddy_config || true)"
caddy_port="$(session_get caddy_port || true)"
caddy_admin_port="$(session_get caddy_admin_port || true)"
runtime_dir="$(session_runtime_dir)"
if [[ -n "$caddy_config" && -n "$caddy_port" && -n "$caddy_admin_port" ]]; then
  caddy_write_closed "$caddy_config" "$caddy_port" "$caddy_admin_port"
  if caddy_reload "$caddy_config" "$caddy_admin_port" "$runtime_dir/logs/caddy.log"; then
    say 'Private route removed; the front end is closed again.'
  else
    say 'Warning: the front end could not be reloaded (the session may already be stopped).'
  fi
fi

rm -f "$handoff_file"
say 'Handoff revoked. The browser session is untouched.'
