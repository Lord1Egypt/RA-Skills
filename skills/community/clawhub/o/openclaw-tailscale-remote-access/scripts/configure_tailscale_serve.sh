#!/usr/bin/env bash
set -eu

PORT=18789
HTTPS_PORT=443
RESET_FIRST=0

while [ $# -gt 0 ]; do
  case "$1" in
    --port)
      PORT="$2"
      shift 2
      ;;
    --https-port)
      HTTPS_PORT="$2"
      shift 2
      ;;
    --reset-first)
      RESET_FIRST=1
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if ! command -v tailscale >/dev/null 2>&1; then
  echo "tailscale CLI not found" >&2
  exit 1
fi

if [ "$RESET_FIRST" -eq 1 ]; then
  echo "== Resetting existing serve configuration =="
  tailscale serve reset
fi

echo "== Configuring HTTPS Serve =="
tailscale serve --bg --https="$HTTPS_PORT" "http://127.0.0.1:$PORT"

echo "== Current serve status =="
tailscale serve status
