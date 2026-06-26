# hyperv-create-vm

Create Ubuntu 24.04 VMs on Windows Hyper-V from cloud images with cloud-init. Handles all the gotchas (sparse VHDX, network config, permissions, Compose v2). Returns a Docker-ready VM with SSH access.

## What It Does

Reusable VM creation skill. Creates the infrastructure, doesn't deploy applications. Pair with:
- `soc-deploy-thehive` for TheHive + Cortex
- `soc-deploy-misp` for MISP
- Any Docker-based deployment

## Automation Includes

- Ubuntu cloud image download and VHDX conversion
- Sparse flag fix (the #1 Hyper-V gotcha)
- Cloud-init ISO with Docker, Compose v2, SSH access
- hv_netvsc network config (mandatory for Hyper-V)
- VM creation, permissions, and startup
- IP discovery via ARP scan
- SSH verification

## Requirements

- SSH access to a Windows Hyper-V host
- `qemu-img` on the Hyper-V host (`choco install qemu -y`)
- `genisoimage` on the agent's Linux host

## Tags

hyper-v, vm, ubuntu, cloud-init, infrastructure, automation, windows
