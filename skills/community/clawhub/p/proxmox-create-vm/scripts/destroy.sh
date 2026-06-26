#!/bin/bash
# Destroy a Proxmox container or VM
# Usage: ./destroy.sh <proxmox-host> <ctid-or-vmid> [type: lxc|vm]

set -euo pipefail

HOST="${1:?Usage: $0 <proxmox-host> <id> [lxc|vm]}"
ID="${2:?Usage: $0 <proxmox-host> <id> [lxc|vm]}"
TYPE="${3:-lxc}"

echo "=== Destroying $TYPE $ID on $HOST ==="

if [ "$TYPE" = "lxc" ]; then
  ssh "$HOST" "pct stop $ID 2>/dev/null; pct destroy $ID --purge"
elif [ "$TYPE" = "vm" ]; then
  ssh "$HOST" "qm stop $ID 2>/dev/null; qm destroy $ID --purge"
else
  echo "ERROR: Type must be 'lxc' or 'vm'"
  exit 1
fi

echo "=== $TYPE $ID destroyed ==="
