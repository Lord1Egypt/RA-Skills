#!/bin/bash
# Create an LXC container on Proxmox with Docker support
# Usage: ./create-lxc.sh <proxmox-host> <name> [cores] [ram-mb] [disk-gb]

set -euo pipefail

HOST="${1:?Usage: $0 <proxmox-host> <name> [cores] [ram-mb] [disk-gb]}"
NAME="${2:?Usage: $0 <proxmox-host> <name> [cores] [ram-mb] [disk-gb]}"
CORES="${3:-2}"
RAM="${4:-4096}"
DISK="${5:-8}"
TEMPLATE="ubuntu-24.04-standard_24.04-2_amd64.tar.zst"

echo "=== Creating LXC: $NAME on $HOST ==="
echo "  Cores: $CORES | RAM: ${RAM}MB | Disk: ${DISK}GB"

# Ensure template is cached
echo "[1/5] Checking template..."
if ! ssh "$HOST" "pveam list local" 2>/dev/null | grep -q "$TEMPLATE"; then
  echo "  Downloading template (this may take a few minutes)..."
  ssh "$HOST" "pveam download local $TEMPLATE"
else
  echo "  Template cached."
fi

# Find next CTID
echo "[2/5] Finding next CTID..."
CTID=$(ssh "$HOST" "{ pct list 2>/dev/null | tail -n +2 | awk '{print \$1}'; qm list 2>/dev/null | tail -n +2 | awk '{print \$1}'; } | sort -n | tail -1")
CTID=$((CTID + 1))
echo "  Using CTID: $CTID"

# Create container
echo "[3/5] Creating container..."
ssh "$HOST" "pct create $CTID local:vztmpl/$TEMPLATE \
  --hostname $NAME \
  --memory $RAM \
  --cores $CORES \
  --rootfs local-lvm:$DISK \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --unprivileged 1 \
  --features nesting=1 \
  --start 1"

# Wait for boot
echo "[4/5] Waiting for boot..."
sleep 10

# Get IP
echo "[5/5] Getting IP..."
IP=$(ssh "$HOST" "pct exec $CTID -- hostname -I 2>/dev/null" | awk '{print $1}')

echo ""
echo "=== LXC Created ==="
echo "Name: $NAME"
echo "CTID: $CTID"
echo "IP: ${IP:-pending (check in a few seconds)}"
echo "Access: ssh $HOST \"pct exec $CTID -- bash\""
echo ""
echo "Next: Run post-boot-setup.sh to install Docker"
