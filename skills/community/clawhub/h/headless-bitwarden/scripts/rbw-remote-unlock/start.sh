#!/usr/bin/env bash
set -euo pipefail

# rbw remote unlock helper
#
# Quick start:
#   skills/headless-bitwarden/scripts/rbw-remote-unlock/start.sh
#
# Common options:
#   TTL_SECONDS=600            # auto-expire after N seconds (default: 600)
#   PORT=0                     # 0 = random localhost port (default)
#   TOKEN=<hex>                # override the one-time URL token (default: random)
#   SYNC_AFTER_UNLOCK=1        # run `rbw sync` after a successful unlock
#   START_TUNNEL=0             # disable Cloudflare tunnel even if cloudflared exists
#   START_TUNNEL=1             # force tunnel startup if cloudflared exists
#   UNLOCK_TIMEOUT_MS=90000    # kill a stuck `rbw unlock` attempt after N ms
#
# What it does:
#   - Starts a localhost-only HTTP helper with a random path token.
#   - Optionally opens a temporary Cloudflare TryCloudflare HTTPS tunnel.
#   - Accepts the password in memory only, uses a temporary pinentry override,
#     restores rbw config immediately, and exits after success or TTL expiry.
#
# What it does NOT do:
#   - It does not install cloudflared.
#   - It does not store the password on disk.
#   - It does not modify OpenClaw config.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SERVER_JS="$SCRIPT_DIR/server.mjs"
PINENTRY_SH="$SCRIPT_DIR/pinentry.sh"
TTL_SECONDS="${TTL_SECONDS:-600}"
PORT="${PORT:-0}"
TOKEN="${TOKEN:-}"
SYNC_AFTER_UNLOCK="${SYNC_AFTER_UNLOCK:-0}"
START_TUNNEL="${START_TUNNEL:-1}"
UNLOCK_TIMEOUT_MS="${UNLOCK_TIMEOUT_MS:-30000}"

if [[ ! -x "$PINENTRY_SH" ]]; then
  echo "pinentry helper is missing or not executable: $PINENTRY_SH" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "node is required but was not found in PATH" >&2
  exit 1
fi

if ! command -v rbw >/dev/null 2>&1; then
  echo "rbw is required but was not found in PATH" >&2
  exit 1
fi

SERVER_PID=""
CLOUDFLARED_PID=""
CLOUDFLARED_LOG=""
READY_JSON=""
PUBLIC_URL=""

cleanup() {
  if [[ -n "$CLOUDFLARED_PID" ]] && kill -0 "$CLOUDFLARED_PID" 2>/dev/null; then
    kill "$CLOUDFLARED_PID" 2>/dev/null || true
    wait "$CLOUDFLARED_PID" 2>/dev/null || true
  fi
  if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  if [[ -n "$CLOUDFLARED_LOG" ]] && [[ -f "$CLOUDFLARED_LOG" ]]; then
    rm -f "$CLOUDFLARED_LOG"
  fi
}
trap cleanup EXIT
trap 'exit 130' INT TERM

READY_PREFIX='RBW_REMOTE_UNLOCK_READY '

coproc SERVER_PROC {
  env \
    HOST=127.0.0.1 \
    PORT="$PORT" \
    TOKEN="$TOKEN" \
    TTL_SECONDS="$TTL_SECONDS" \
    SYNC_AFTER_UNLOCK="$SYNC_AFTER_UNLOCK" \
    UNLOCK_TIMEOUT_MS="$UNLOCK_TIMEOUT_MS" \
    PINENTRY_PATH="$PINENTRY_SH" \
    node "$SERVER_JS"
}
SERVER_PID=$SERVER_PROC_PID

while IFS= read -r line <&"${SERVER_PROC[0]}"; do
  if [[ "$line" == "$READY_PREFIX"* ]]; then
    READY_JSON=${line#"$READY_PREFIX"}
    break
  fi
  [[ -n "$line" ]] && printf '%s\n' "$line"
done

if [[ -z "$READY_JSON" ]]; then
  echo "Failed to read startup info from helper." >&2
  exit 1
fi

HOST_VALUE="$(node -p 'JSON.parse(process.argv[1]).host' "$READY_JSON")"
PORT_VALUE="$(node -p 'JSON.parse(process.argv[1]).port' "$READY_JSON")"
TOKEN_VALUE="$(node -p 'JSON.parse(process.argv[1]).token' "$READY_JSON")"
TTL_VALUE="$(node -p 'JSON.parse(process.argv[1]).ttlSeconds' "$READY_JSON")"
SYNC_VALUE="$(node -p 'JSON.parse(process.argv[1]).syncAfterUnlock' "$READY_JSON")"
LOCAL_URL="http://${HOST_VALUE}:${PORT_VALUE}/${TOKEN_VALUE}/"

cat <<MSG
rbw remote unlock helper is running.
- Local URL: $LOCAL_URL
- Token path: /$TOKEN_VALUE/
- TTL: ${TTL_VALUE}s
- Sync after unlock: $SYNC_VALUE
MSG

if [[ "$START_TUNNEL" != "0" ]]; then
  if command -v cloudflared >/dev/null 2>&1; then
    CLOUDFLARED_LOG="$(mktemp)"
    chmod 600 "$CLOUDFLARED_LOG"
    cloudflared tunnel --url "http://${HOST_VALUE}:${PORT_VALUE}" >"$CLOUDFLARED_LOG" 2>&1 &
    CLOUDFLARED_PID=$!

    for _ in $(seq 1 50); do
      if ! kill -0 "$CLOUDFLARED_PID" 2>/dev/null; then
        break
      fi
      PUBLIC_URL="$(grep -Eo 'https://[-a-zA-Z0-9]+\.trycloudflare\.com' "$CLOUDFLARED_LOG" | head -n1 || true)"
      if [[ -n "$PUBLIC_URL" ]]; then
        break
      fi
      sleep 0.2
    done

    if [[ -n "$PUBLIC_URL" ]]; then
      echo "- Public URL: ${PUBLIC_URL}/${TOKEN_VALUE}/"
    else
      echo "- Tunnel: cloudflared started, but the public URL was not detected yet." >&2
      echo "  Check: tail -f $CLOUDFLARED_LOG" >&2
    fi
  else
    cat <<MSG
- Tunnel: cloudflared not found.
  Install it if you want a temporary HTTPS URL, e.g.:
  https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
MSG
  fi
fi

echo "Press Ctrl+C to stop early."
wait "$SERVER_PID"
