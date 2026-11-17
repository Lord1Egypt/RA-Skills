#!/usr/bin/env bash
# Caddy front-end configuration. Sourced, not executed.
#
# Two shapes only: closed (404 to everything) and armed (one high-entropy token
# route to websockify). Arming and revoking a handoff is a switch between them.

[[ -n "${__LINE_OA_CADDY_LOADED:-}" ]] && return 0
__LINE_OA_CADDY_LOADED=1

# caddy_write_closed <config-path> <listen-port> <admin-port>
caddy_write_closed() {
  local config="$1" port="$2" admin="$3"
  # A host-agnostic site address with an explicit loopback bind. Binding to
  # http://127.0.0.1:<port> instead would reject the public tunnel Host header
  # and serve an empty page through a working tunnel URL.
  printf '{\n  auto_https off\n  admin 127.0.0.1:%s\n}\n:%s {\n  bind 127.0.0.1\n  respond 404\n}\n' \
    "$admin" "$port" > "$config"
  chmod 600 "$config"
}

# caddy_write_armed <config-path> <listen-port> <admin-port> <token> <websockify-port>
# Multi-line handle blocks are deliberate: compact inline blocks can fail Caddy
# parsing.
caddy_write_armed() {
  local config="$1" port="$2" admin="$3" token="$4" ws_port="$5"
  printf '{\n  auto_https off\n  admin 127.0.0.1:%s\n}\n:%s {\n  bind 127.0.0.1\n  @private path /%s/*\n  handle @private {\n    uri strip_prefix /%s\n    reverse_proxy 127.0.0.1:%s\n  }\n  respond 404\n}\n' \
    "$admin" "$port" "$token" "$token" "$ws_port" > "$config"
  chmod 600 "$config"
}

# caddy_reload <config-path> <admin-port> [log-path]
caddy_reload() {
  local config="$1" admin="$2" log="${3:-/dev/null}"
  caddy reload --config "$config" --adapter caddyfile --address "127.0.0.1:${admin}" >>"$log" 2>&1
}
