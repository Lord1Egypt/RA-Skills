#!/usr/bin/env bash
# ssh-exec.sh — Run a RouterOS command via SSH
# Prefers SSH key auth. Falls back to sshpass if key not available.
# Usage: ./ssh-exec.sh "<HOST>" "<USER>" "<CMD>" [key_path]

set -euo pipefail

HOST="${MIKROTIK_HOST:-$1}"
USER="${MIKROTIK_USER:-$2}"
CMD="${3:-/system resource print}"
KEY="${4:-${MIKROTIK_KEY:-$HOME/.ssh/mikrotik_key}}"

SSH_OPTS="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 -o BatchMode=yes"

if [ -f "$KEY" ]; then
  # Preferred: key-based auth (no password in process list)
  ssh $SSH_OPTS -i "$KEY" "$USER@$HOST" "$CMD"
else
  # Fallback: password via env var only
  if [ -z "${MIKROTIK_PASS:-}" ]; then
    echo "ERROR: No SSH key at $KEY and MIKROTIK_PASS not set." >&2
    exit 1
  fi
  if ! command -v sshpass &>/dev/null; then
    echo "ERROR: sshpass not found. Install: apt install sshpass" >&2
    exit 1
  fi
  sshpass -p "$MIKROTIK_PASS" ssh $SSH_OPTS "$USER@$HOST" "$CMD"
fi
