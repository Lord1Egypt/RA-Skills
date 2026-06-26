#!/bin/bash
# Get IP address of a Proxmox container or VM
# Usage: ./find-ip.sh <proxmox-host> <id> [type: lxc|vm]

set -euo pipefail

HOST="${1:?Usage: $0 <proxmox-host> <id> [lxc|vm]}"
ID="${2:?Usage: $0 <proxmox-host> <id> [lxc|vm]}"
TYPE="${3:-lxc}"

if [ "$TYPE" = "lxc" ]; then
  IP=$(ssh "$HOST" "pct exec $ID -- hostname -I 2>/dev/null" | awk '{print $1}')
elif [ "$TYPE" = "vm" ]; then
  IP=$(ssh "$HOST" "qm guest cmd $ID network-get-interfaces 2>/dev/null" | grep -oP '"ip-address"\s*:\s*"\K[0-9.]+' | head -1)
  if [ -z "$IP" ]; then
    echo "VM guest agent not responding. Try ARP scan:"
    echo "  arp -a | grep the VM's MAC address"
    exit 1
  fi
fi

if [ -n "$IP" ]; then
  echo "$IP"
else
  echo "Could not determine IP. The container/VM may still be booting."
  exit 1
fi
