# Defaults: Hyper-V VM Creation

## VM Specs

| Parameter | Default | Notes |
|-----------|---------|-------|
| OS | Ubuntu 24.04 LTS | Cloud image (qcow2) |
| Generation | 2 | Required for UEFI boot |
| CPU | 2 cores | |
| RAM | 4 GB | |
| Disk | 40 GB | |
| Network switch | DNS-NIC-Switch | |
| VM user | deploy | |
| Secure Boot | Off | Cloud images unsigned |
| Auto checkpoints | Off | Prevents disk bloat |

## File Paths (Hyper-V Host)

| Item | Path |
|------|------|
| Cloud image cache | `C:\Users\youruser\Downloads\ubuntu-24.04-cloud.img` |
| VHDX storage | `C:\ProgramData\Microsoft\Windows\Virtual Hard Disks\` |
| Cloud-init ISOs | `C:\Users\youruser\Downloads\` |
| qemu-img | `C:\Program Files\qemu\qemu-img.exe` |

## Cloud Image URL

```
https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img
```

## Installed via Cloud-Init

- docker.io
- curl
- git
- htop
- Docker Compose v2 plugin (via curl, not apt)
- SSH password auth disabled (key-only by default)
