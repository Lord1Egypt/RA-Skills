# Defaults: Proxmox VM/Container Creation

## Host Info

| Parameter | Value |
|-----------|-------|
| Hostname | proxmox-host |
| IP | YOUR_PROXMOX_IP |
| SSH user | root |
| PVE version | 9.1.6 |
| CPU | Intel Ultra 9 285 |
| RAM | 32GB |
| Bridge | vmbr0 (DHCP) |

## Resource Budget

| Resource | Total | Used | Free |
|----------|-------|------|------|
| CPU cores | 24 | ~14 | ~10 |
| RAM | 32GB | ~22GB | ~10GB |
| Disk (LVM) | ~800GB | ~30GB | ~770GB |

## Existing Containers (as of March 2026)

| CTID | Name | Purpose | Notes |
|------|------|---------|-------|
| 100 | adguard | DNS ad blocking | |
| 101 | twingate-connector | Zero-trust VPN | |
| 102 | crafty-controller | Minecraft server | |
| 103 | homarr | Dashboard | |
| 105 | wazuh | SIEM | 99.3% disk full! |
| 109 | social-automation | n8n + Postiz | |

**Next CTID: 110+** (always verify with `pct list`)

## LXC Defaults

| Parameter | Default |
|-----------|---------|
| OS template | ubuntu-24.04-standard_24.04-2_amd64.tar.zst |
| Cores | 2 |
| RAM | 4096 MB |
| Disk | 8 GB |
| Network | eth0, vmbr0, DHCP |
| Unprivileged | Yes |
| Nesting | Yes (for Docker) |

## VM Defaults

| Parameter | Default |
|-----------|---------|
| OS | Ubuntu 24.04 cloud-init |
| Cores | 2 |
| RAM | 4096 MB |
| Disk | 20 GB |
| SCSI | virtio-scsi-pci |
| Network | virtio, vmbr0, DHCP |
| User | deploy |
