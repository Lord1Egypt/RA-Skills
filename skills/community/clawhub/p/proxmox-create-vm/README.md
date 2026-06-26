# proxmox-create-vm

Create Ubuntu 24.04 LXC containers or full VMs on Proxmox VE. Docker-ready with Compose v2. Handles nesting for Docker-in-LXC and auto-picks CTIDs.

## What It Does

Reusable infrastructure skill. Creates the host, doesn't deploy applications. Pair with:
- `soc-deploy-thehive` for TheHive + Cortex
- `soc-deploy-misp` for MISP
- Any Docker-based deployment

Supports both LXC containers (default, fast, lightweight) and full VMs (for tools needing kernel access).

## Automation Includes

- Template download and caching
- Auto CTID/VMID selection
- LXC creation with Docker nesting support
- Full VM creation with cloud-init
- Post-boot Docker + Compose v2 setup
- IP discovery and SSH verification
- Clean teardown

## Requirements

- SSH access to a Proxmox VE host (root)

## Tags

proxmox, lxc, vm, ubuntu, infrastructure, automation, docker, homelab
