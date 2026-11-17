#!/usr/bin/env bash
# Startup script for the OpenClaw Docker container.
#
# Shipped with the openclaw-docker-linux skill. Without it the compose file's
# `command:` override pointed at a file that did not exist, so the container
# failed to start.
#
# Responsibilities:
#   - Confirm the required gateway token is present before starting.
#   - Keep the gateway bound to loopback inside the container.
#   - Hand off to the OpenClaw entrypoint.

set -euo pipefail

log() { printf '[openclaw-start] %s\n' "$*"; }
fail() { printf '[openclaw-start] ERROR: %s\n' "$*" >&2; exit 1; }

# --- required configuration ------------------------------------------------
if [ -z "${OPENCLAW_GATEWAY_TOKEN:-}" ]; then
  fail "OPENCLAW_GATEWAY_TOKEN is not set. Generate one with: openssl rand -hex 32"
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ] && [ -z "${OPENAI_API_KEY:-}" ]    && [ -z "${OPENCLAW_USE_OLLAMA:-}" ]; then
  fail "No model provider key found. Set ANTHROPIC_API_KEY (or another provider key)."
fi

# --- ownership -------------------------------------------------------------
# The container user must own the mounted state directory, otherwise the
# gateway cannot write its database and locks up on start.
STATE_DIR="${HOME}/.openclaw"
mkdir -p "$STATE_DIR" 2>/dev/null || true

if [ ! -w "$STATE_DIR" ]; then
  log "State directory is not writable by uid $(id -u); attempting to fix ownership"
  chown -R "$(id -u):$(id -g)" "$STATE_DIR" 2>/dev/null || \
    log "WARN: could not fix ownership automatically. Check host directory permissions."
fi

# --- bind mode -------------------------------------------------------------
# Default to "lan" inside the container. Docker's port publishing only works
# if the gateway inside the container listens on a non-loopback address; with
# "loopback" the published port forwards to an address nothing is listening
# on and the gateway is unreachable from the host.
#
# This is the IN-CONTAINER half and is not what exposes you. The host-side
# publish in docker-compose.yml binds 127.0.0.1, so only processes on the
# host can connect. Do not "fix" reachability by changing that host mapping
# to 0.0.0.0 -- use Tailscale Serve for remote access.
#
# This matches references/gotchas.md, which documents "lan" as the required
# in-container value for Docker port publishing to work.
#
# Override with OPENCLAW_BIND=loopback only when the container is reached
# through an in-container proxy (not the published port).
BIND_MODE="${OPENCLAW_BIND:-lan}"
case "$BIND_MODE" in
  loopback|lan) ;;
  *) log "WARN: unknown OPENCLAW_BIND='$BIND_MODE', falling back to 'lan'"; BIND_MODE=lan ;;
esac

export OPENCLAW_BIND="$BIND_MODE"
log "Starting OpenClaw (bind=$BIND_MODE)"

# --- exec ------------------------------------------------------------------
# The image's default entrypoint starts the gateway. If the image provides one,
# use it. Otherwise fall back to the documented CLI entrypoint.
if [ -x /app/entrypoint.sh ]; then
  log "Using image entrypoint /app/entrypoint.sh"
  exec /app/entrypoint.sh
elif [ -f /app/dist/index.js ]; then
  log "Starting gateway via node dist/index.js"
  exec node /app/dist/index.js
else
  exec openclaw gateway run
fi
