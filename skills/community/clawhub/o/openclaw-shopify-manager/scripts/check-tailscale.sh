#!/usr/bin/env bash
set -euo pipefail

installed=false
reachable=false
logged_in=false
serve_supported=false
funnel_supported=false
version=""
status_output=""

if command -v tailscale >/dev/null 2>&1; then
  installed=true
  version="$(tailscale version 2>/dev/null | head -n1 || true)"
  status_output="$(tailscale status 2>/dev/null || true)"
  reachable=true
  if [ -n "$status_output" ]; then
    logged_in=true
  fi
  if tailscale serve --help >/dev/null 2>&1; then
    serve_supported=true
  fi
  if tailscale funnel --help >/dev/null 2>&1; then
    funnel_supported=true
  fi
fi

cat <<EOF
installed=$installed
reachable=$reachable
logged_in=$logged_in
serve_supported=$serve_supported
funnel_supported=$funnel_supported
version=${version}
EOF
