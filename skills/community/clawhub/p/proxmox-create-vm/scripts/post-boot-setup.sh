#!/bin/bash
# Install Docker + Compose v2 inside a Proxmox LXC container
# Usage: ./post-boot-setup.sh <proxmox-host> <ctid> [extra-packages]

set -euo pipefail

HOST="${1:?Usage: $0 <proxmox-host> <ctid> [extra-packages]}"
CTID="${2:?Usage: $0 <proxmox-host> <ctid> [extra-packages]}"
EXTRA="${3:-}"

echo "=== Post-boot setup for CTID $CTID ==="

echo "[1/3] Installing base packages..."
ssh "$HOST" "pct exec $CTID -- bash -c '
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y -qq docker.io curl git htop $EXTRA
'"

echo "[2/3] Installing Docker Compose v2..."
ssh "$HOST" "pct exec $CTID -- bash -c '
  systemctl enable docker
  systemctl start docker
  mkdir -p /usr/local/lib/docker/cli-plugins
  curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
  chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
'"

echo "[3/3] Verifying..."
ssh "$HOST" "pct exec $CTID -- docker --version"
ssh "$HOST" "pct exec $CTID -- docker compose version"

echo ""
echo "=== Setup complete for CTID $CTID ==="
