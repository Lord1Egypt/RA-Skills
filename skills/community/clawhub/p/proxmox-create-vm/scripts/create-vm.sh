#!/bin/bash
# Create a full VM on Proxmox with cloud-init
# Usage: ./create-vm.sh <proxmox-host> <name> <password> [cores] [ram-mb] [disk-gb]

set -euo pipefail

HOST="${1:?Usage: $0 <proxmox-host> <name> <password> [cores] [ram-mb] [disk-gb]}"
NAME="${2:?Usage: $0 <proxmox-host> <name> <password> [cores] [ram-mb] [disk-gb]}"
PASSWORD="${3:?Usage: $0 <proxmox-host> <name> <password> [cores] [ram-mb] [disk-gb]}"
CORES="${4:-2}"
RAM="${5:-4096}"
DISK="${6:-20}"

echo "=== Creating VM: $NAME on $HOST ==="
echo "  Cores: $CORES | RAM: ${RAM}MB | Disk: ${DISK}GB"

# Find next VMID
echo "[1/4] Finding next VMID..."
VMID=$(ssh "$HOST" "{ pct list 2>/dev/null | tail -n +2 | awk '{print \$1}'; qm list 2>/dev/null | tail -n +2 | awk '{print \$1}'; } | sort -n | tail -1")
VMID=$((VMID + 1))
echo "  Using VMID: $VMID"

# Download cloud image if needed
echo "[2/4] Checking cloud image..."
ssh "$HOST" "ls /var/lib/vz/template/iso/ubuntu-24.04-cloud.img 2>/dev/null" || {
  echo "  Downloading cloud image..."
  ssh "$HOST" "wget -q https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img -O /var/lib/vz/template/iso/ubuntu-24.04-cloud.img"
}

# Create VM
echo "[3/4] Creating VM..."
ssh "$HOST" "qm create $VMID --name $NAME --memory $RAM --cores $CORES \
  --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-pci \
  --scsi0 local-lvm:$DISK,format=raw --ide2 local-lvm:cloudinit \
  --boot c --bootdisk scsi0 --serial0 socket --vga serial0 \
  --ciuser deploy --cipassword '$PASSWORD' --ipconfig0 ip=dhcp"

# Import cloud image disk
ssh "$HOST" "qm importdisk $VMID /var/lib/vz/template/iso/ubuntu-24.04-cloud.img local-lvm"

# Start
echo "[4/4] Starting VM..."
ssh "$HOST" "qm start $VMID"

echo ""
echo "=== VM Created ==="
echo "Name: $NAME"
echo "VMID: $VMID"
echo "User: deploy / $PASSWORD"
echo "Wait ~90 seconds for cloud-init, then check IP"
