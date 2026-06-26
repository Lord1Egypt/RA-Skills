# Gotchas: Proxmox VM/Container Creation

## Docker in LXC Requires Nesting
- Without `--features nesting=1`, Docker fails to create overlay networks
- **Fix:** Always include `--features nesting=1` when the container will run Docker
- Unprivileged + nesting is the safe default

## LXC Can't Run Everything
- No custom kernel modules (iptables works, but kernel-level packet capture doesn't)
- No AF_PACKET raw sockets (needed by Zeek, Security Onion, tcpdump with advanced features)
- No /dev access for specialized hardware
- **Fix:** Use `qm` (full VM) instead of `pct` (LXC) for these use cases

## Template Caching
- `pveam download local <template>` is slow on first download (~2-5 min depending on connection)
- Always check `pveam list local` first to see if the template is cached
- Template name for Ubuntu 24.04: `ubuntu-24.04-standard_24.04-2_amd64.tar.zst`

## CTID/VMID Conflicts
- Proxmox uses numeric IDs for both containers (CTID) and VMs (VMID) in the same namespace
- **Fix:** Always check both `pct list` and `qm list` before picking an ID
- Use max(all IDs) + 1 for safety

## Disk Thin Provisioning
- Proxmox reports ~770GB free in the LVM pool
- But individual containers can fill up fast, especially logging and DB-heavy services
- Wazuh container (CTID 105) is at 99.3% / 25GB. Don't colocate storage-heavy services
- **Fix:** Monitor with `pct exec <CTID> -- df -h` and resize with `pct resize <CTID> rootfs +10G`

## LXC Root Access
- LXC containers default to root user (no separate user created)
- Access via `pct exec <CTID> -- bash` or SSH as root
- VMs use cloud-init with a deploy user

## Container Startup
- LXC containers boot in ~5 seconds
- Full VMs with cloud-init take ~60-90 seconds
- Template download (if needed) adds 2-5 minutes

## Network
- All containers/VMs on `vmbr0` bridge with DHCP
- IP assigned by network DHCP server
- For static IPs, use `--net0 name=eth0,bridge=vmbr0,ip=192.168.x.x/24,gw=192.168.x.1`
