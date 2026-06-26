---
name: hyperv-create-vm
version: 1.0.0
description: "Create Ubuntu 24.04 VMs on Windows Hyper-V from cloud images with cloud-init. Handles all the gotchas: sparse VHDX fix, hv_netvsc network config, permissions, Secure Boot, and Docker Compose v2. Returns a Docker-ready VM with SSH access."
tags:
  - hyper-v
  - vm
  - ubuntu
  - cloud-init
  - infrastructure
  - automation
  - windows
category: infrastructure
requires:
  env:
    - name: VM_PASSWORD
      description: "Password for the VM's deploy user. Read via env var or stdin (never CLI args)."
      required: false
  credentials:
    - name: SSH access to Hyper-V host
      description: "SSH key or password auth to the Windows Hyper-V host for remote PowerShell execution."
      required: true
    - name: Hyper-V admin privileges
      description: "The SSH user must be able to run elevated PowerShell (Hyper-V cmdlets, fsutil, icacls)."
      required: true
  tools:
    - name: genisoimage
      description: "Required on the Linux build host to create cloud-init ISOs."
      install: "apt install genisoimage"
    - name: qemu-img
      description: "Required on the Windows Hyper-V host for qcow2-to-VHDX conversion."
      install: "choco install qemu -y"
files:
  - SKILL.md
  - README.md
  - scripts/build-cidata-iso.sh
  - scripts/create-vm.ps1
  - scripts/destroy-vm.ps1
  - scripts/find-vm-ip.ps1
  - scripts/cloud-init-user-data.yaml
  - scripts/cloud-init-meta-data.yaml
  - scripts/cloud-init-network-config.yaml
  - references/defaults.md
  - references/gotchas.md
---

# Hyper-V VM Creator

Create Ubuntu 24.04 VMs on Windows Hyper-V from cloud images with cloud-init. Returns a Docker-ready VM with SSH access.

## When to Use

- "create hyper-v vm"
- "spin up vm on hyper-v"
- "new hyper-v ubuntu vm"
- Any time you need a fresh Linux VM on a Windows Hyper-V host

This is a **base skill**. It creates the VM. Other skills (soc-deploy-thehive, soc-deploy-misp) deploy applications onto it.

## User Inputs

| Parameter | Default | Required |
|-----------|---------|----------|
| VM name | - | Yes |
| Hyper-V host | hyperv-host (YOUR_HYPERV_IP) | No |
| CPU cores | 2 | No |
| RAM | 4GB | No |
| Disk | 40GB | No |
| VM user password | (generated) | No |
| Extra cloud-init packages | - | No |
| Network switch | DNS-NIC-Switch | No |

## Prerequisites Check

```bash
# SSH to Hyper-V host
ssh hyperv-host "echo OK" 2>/dev/null || echo "FAIL: Cannot SSH to Hyper-V host"

# qemu-img on Windows
ssh hyperv-host 'where "C:\Program Files\qemu\qemu-img.exe"' 2>/dev/null || echo "FAIL: qemu-img not installed (choco install qemu -y)"

# genisoimage on Linux (for building cloud-init ISO)
which genisoimage || echo "FAIL: genisoimage not installed (apt install genisoimage)"
```

## Execution Flow

### Step 1: Build cloud-init ISO (on Linux)

```bash
# Password via env var (recommended, avoids shell history/process list exposure)
VM_PASSWORD="<password>" bash scripts/build-cidata-iso.sh <vm-name> [ssh-public-key]

# Or via stdin
echo "<password>" | bash scripts/build-cidata-iso.sh <vm-name> [ssh-public-key]

# Creates /tmp/<vm-name>-cidata.iso
```

The ISO contains three files:
- `user-data`: deploy user, Docker, Compose v2, SSH password auth
- `meta-data`: instance-id and hostname
- `network-config`: hv_netvsc DHCP match (CRITICAL for Hyper-V networking)

### Step 2: Transfer files to Hyper-V host

```bash
# Cloud image (if not already cached)
wget -q https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img -O /tmp/ubuntu-24.04-cloud.img
scp /tmp/ubuntu-24.04-cloud.img hyperv-host:C:/Users/youruser/Downloads/

# Cloud-init ISO
scp /tmp/<vm-name>-cidata.iso hyperv-host:C:/Users/youruser/Downloads/
```

### Step 3: Create VM (elevated PowerShell on Hyper-V host)

```bash
# Copy script to host
scp scripts/create-vm.ps1 hyperv-host:C:/Users/youruser/Downloads/

# Execute (needs elevation)
ssh hyperv-host "powershell -ExecutionPolicy Bypass -File C:\\Users\\youruser\\Downloads\\create-vm.ps1 \
  -VMName <vm-name> \
  -CloudInitISO C:\\Users\\youruser\\Downloads\\<vm-name>-cidata.iso \
  -DiskSizeGB <disk> -MemoryGB <ram> -CPUCount <cores>"
```

### Step 4: Wait for boot and find IP

```bash
sleep 90  # Cloud-init needs ~90 seconds

# Hyper-V VMs have MACs starting with 00-15-5d
arp -a | grep "00-15-5d"

# Get VM MAC to match
ssh hyperv-host "powershell (Get-VMNetworkAdapter -VMName '<vm-name>').MacAddress"
# PowerShell shows: 00155D38010A
# ARP shows:        00-15-5d-38-01-0a
```

### Step 5: Verify SSH and Docker

```bash
ssh deploy@<ip> "docker --version && docker compose version && echo 'VM READY'"
```

### Return Values

Report to caller:
```
VM Created: <vm-name>
IP: <ip>
SSH: deploy@<ip> (password: <password>)
Docker: installed
Docker Compose v2: installed
```

## Teardown

To destroy a VM completely:
```bash
ssh hyperv-host "powershell -Command \"Stop-VM -Name '<vm-name>' -Force -TurnOff; Remove-VM -Name '<vm-name>' -Force; Remove-Item 'C:\\ProgramData\\Microsoft\\Windows\\Virtual Hard Disks\\<vm-name>.vhdx' -Force\""
```

Or use `scripts/destroy-vm.ps1`:
```bash
scp scripts/destroy-vm.ps1 hyperv-host:C:/Users/youruser/Downloads/
ssh hyperv-host "powershell -ExecutionPolicy Bypass -File C:\\Users\\youruser\\Downloads\\destroy-vm.ps1 -VMName <vm-name>"
```

## Critical Gotchas

See `references/gotchas.md` for full details. Top blockers:

1. **Sparse VHDX**: `fsutil sparse setflag <path> 0` BEFORE `Resize-VHD` or error 0xC03A001A
2. **Network config**: Must include `match: driver: hv_netvsc` or VM gets no IP
3. **Permissions**: `icacls /grant "NT VIRTUAL MACHINE\Virtual Machines:(F)"` or Start-VM fails
4. **Secure Boot Off**: Ubuntu cloud images aren't signed for Hyper-V
5. **Cloud-init runs once**: No redo. Delete VM + VHDX and start over
6. **Don't batch PowerShell**: Run Hyper-V commands one at a time
7. **All commands need elevated PowerShell**
8. **Docker Compose v2**: Install via curl in runcmd, NOT apt
9. **IP discovery**: Use ARP scan, not Get-VMNetworkAdapter (needs linux-tools-virtual)
