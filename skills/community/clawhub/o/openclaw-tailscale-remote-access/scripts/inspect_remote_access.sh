#!/usr/bin/env bash
set -u

CONFIG_PATH="${1:-$HOME/.openclaw/openclaw.json}"

echo "== Identity =="
echo "user: $(id -un)"
echo "host: $(hostname)"
echo "ssh_connection: ${SSH_CONNECTION:-<none>}"
echo

if command -v tailscale >/dev/null 2>&1; then
  echo "== Tailscale IPs =="
  tailscale ip -4 2>/dev/null || true
  echo

  echo "== Tailscale Status =="
  tailscale status --json 2>/dev/null || tailscale status || true
  echo

  echo "== Tailscale Serve Status =="
  tailscale serve status --json 2>/dev/null || tailscale serve status || true
  echo
else
  echo "tailscale CLI not found"
  echo
fi

if command -v systemctl >/dev/null 2>&1; then
  echo "== openclaw-gateway status =="
  systemctl --user status openclaw-gateway --no-pager || true
  echo
fi

if [ -f "$CONFIG_PATH" ]; then
  echo "== OpenClaw config: $CONFIG_PATH =="
  sed -n '1,220p' "$CONFIG_PATH"
  echo
else
  echo "Config file not found: $CONFIG_PATH"
  echo
fi

if [ -f "$HOME/.openclaw/devices/pending.json" ]; then
  echo "== Pending pairing requests =="
  cat "$HOME/.openclaw/devices/pending.json"
  echo
fi
