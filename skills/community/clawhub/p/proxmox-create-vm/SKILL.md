---
name: proxmox-create-vm
version: 1.0.0
description: "Create Ubuntu 24.04 LXC containers or full VMs on Proxmox VE. Docker-ready with Compose v2. Handles nesting for Docker-in-LXC, auto-picks next available CTID, and includes post-boot Docker setup."
tags:
  - proxmox
  - lxc
  - vm
  - ubuntu
  - infrastructure
  - automation
  - docker
  - homelab
category: infrastructure
---

# Proxmox VM/Container Creator

Create Ubuntu 24.04 LXC containers or full VMs on Proxmox VE. Returns a Docker-ready host with SSH access.

## When to Use

- "create proxmox vm"
- "create proxmox container"
- "spin up lxc"
- "new container on proxmox-host"
- Any time you need a fresh Linux host on Proxmox

This is a **base skill**. It creates the infrastructure. Other skills deploy applications onto it.

## LXC vs VM Decision Guide

| Use LXC when | Use VM when |
|---|---|
| Running Docker containers (TheHive, MISP, etc.) | Security Onion, Zeek with AF_PACKET |
| Lightweight services | Need custom kernel modules |
| Want fast startup (~5 seconds) | Need full OS isolation |
| Most SOC tools | Network monitoring with raw sockets |

**Default: LXC.** Only use VM when the application explicitly needs kernel access.

## User Inputs

| Parameter | Default | Required |
|-----------|---------|----------|
| Name | - | Yes |
| Proxmox host | proxmox-host (YOUR_PROXMOX_IP) | No |
| Type | lxc | No (lxc or vm) |
| CPU cores | 2 | No |
| RAM (MB) | 4096 | No |
| Disk (GB) | 8 | No |
| Extra packages | - | No |

## Prerequisites Check

```bash
# SSH to Proxmox
ssh proxmox-host "pveversion" || echo "FAIL: Cannot SSH to Proxmox host"

# Check template (LXC)
ssh proxmox-host "pveam list local | grep ubuntu-24.04" || echo "Template not cached, will download"

# Find next CTID
ssh proxmox-host "pct list" | tail -n +2 | awk '{print $1}' | sort -n | tail -1
# Use max + 1
```

## Execution Flow: LXC Container

### Step 1: Ensure template is cached

```bash
ssh proxmox-host "pveam list local | grep ubuntu-24.04 || pveam download local ubuntu-24.04-standard_24.04-2_amd64.tar.zst"
```

### Step 2: Find next available CTID

```bash
NEXT_CTID=$(ssh proxmox-host "cat <(pct list | tail -n +2 | awk '{print \$1}') <(qm list | tail -n +2 | awk '{print \$1}') 2>/dev/null | sort -n | tail -1")
NEXT_CTID=$((NEXT_CTID + 1))
```

### Step 3: Create container

```bash
ssh proxmox-host "pct create $CTID local:vztmpl/ubuntu-24.04-standard_24.04-2_amd64.tar.zst \
  --hostname <name> \
  --memory <ram> \
  --cores <cores> \
  --rootfs local-lvm:<disk> \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --unprivileged 1 \
  --features nesting=1 \
  --start 1"
```

**Key flags:**
- `--unprivileged 1`: Security best practice
- `--features nesting=1`: Required for Docker inside LXC
- `--start 1`: Start immediately after creation

### Step 4: Wait for boot and get IP

```bash
sleep 10  # LXC boots in ~5 seconds

# Get IP from Proxmox
ssh proxmox-host "pct exec $CTID -- hostname -I"

# Or from DHCP
ssh proxmox-host "pct exec $CTID -- ip -4 addr show eth0 | grep inet | awk '{print \$2}' | cut -d/ -f1"
```

### Step 5: Post-boot Docker setup

```bash
bash scripts/post-boot-setup.sh proxmox-host $CTID
```

Or manually:
```bash
ssh proxmox-host "pct exec $CTID -- bash -c '
  apt-get update -qq
  apt-get install -y -qq docker.io curl git htop
  systemctl enable docker && systemctl start docker
  mkdir -p /usr/local/lib/docker/cli-plugins
  curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
  chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
'"
```

### Step 6: Verify

```bash
ssh proxmox-host "pct exec $CTID -- docker --version && pct exec $CTID -- docker compose version"
```

## Execution Flow: Full VM

Use `scripts/create-vm.sh` for full VMs when LXC won't work:

```bash
ssh proxmox-host "qm create $VMID --name <name> --memory <ram> --cores <cores> \
  --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-pci \
  --scsi0 local-lvm:<disk>,format=raw --ide2 local-lvm:cloudinit \
  --boot c --bootdisk scsi0 --serial0 socket --vga serial0 \
  --ciuser deploy --cipassword <password> --ipconfig0 ip=dhcp \
  --start 1"
```

### Return Values

Report to caller:
```
Container/VM Created: <name>
CTID/VMID: <id>
Type: lxc | vm
IP: <ip>
SSH: root@<ip> (LXC) or deploy@<ip> (VM)
Docker: installed
Docker Compose v2: installed
```

## Teardown

```bash
# LXC
ssh proxmox-host "pct stop $CTID && pct destroy $CTID --purge"

# VM
ssh proxmox-host "qm stop $VMID && qm destroy $VMID --purge"
```

## Critical Gotchas

See `references/gotchas.md` for full details:

1. **Docker in LXC needs nesting=1**: Without `--features nesting=1`, Docker fails to create networks
2. **LXC limitations**: No custom kernel modules, no raw sockets (AF_PACKET). Use VM for Security Onion, Zeek
3. **Template caching**: `pveam download` is slow first time. Check `pveam list local` first
4. **CTID conflicts**: Always check `pct list` before picking a CTID
5. **Disk is thin-provisioned**: 770GB free in pool but containers can fill up fast
6. **Wazuh (CTID 105)**: 99.3% full at 25GB. Don't colocate storage-heavy services
