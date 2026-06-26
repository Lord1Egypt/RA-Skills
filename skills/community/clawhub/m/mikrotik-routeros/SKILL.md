# MikroTik RouterOS Skill

description: Connect and manage MikroTik RouterOS devices via API. Supports viewing device status, firewall rules, network configuration, and executing custom RouterOS commands.

Connect and manage MikroTik RouterOS devices via API.

## Features

- View device status (system info, CPU, memory, storage)
- View firewall rules (filter, NAT, mangle)
- View network configuration (interfaces, IP addresses, routes, DNS)
- Execute custom RouterOS commands
- Support for multi-device connection

## Configuration

### Option 1: TOOLS.md (Recommended)

Add device info in `~/.openclaw/workspace/TOOLS.md`:

### MikroTik Devices
- **office**: 192.168.88.1, admin, empty password

**Password format:**
- Empty password: write `empty password`, `no password`, `none`, or leave blank
- With password: write the password string directly

### Option 2: Environment Variables

```bash
export MIKROTIK_HOST=192.168.88.1
export MIKROTIK_USER=admin
export MIKROTIK_PASS=        # empty password
# or
export MIKROTIK_PASS=yourpassword  # with password
```

**Priority**: Environment Variables > TOOLS.md > Defaults

## Usage

### 📊 Device Status
- Show mikrotik device status
- Check office mikrotik status
- Check router health

### 🔥 Firewall
- Show firewall rules
- mikrotik firewall configuration
- Show NAT rules
- Check office firewall

### 🔌 Network Interfaces
- Show network interfaces
- mikrotik interface list
- Show IP address configuration

### 📋 DHCP
- Show DHCP configuration
- Show DHCP leases

### 📡 ARP Table
- Show ARP table
- Show ARP cache

### 🔐 WireGuard
- Show WireGuard configuration
- Show VPN peers

### 👤 Users
- Show user configuration
- Show PPP users

### 📝 Logs
- Show system logs
- Show recent logs

### 🔧 Services
- Show system services
- Show API/SSH ports

### 💾 Backup Configuration
- Backup configuration
- Backup router configuration

### 🧹 Clean Storage
- Clean storage
- Check for deletable files

### 🔐 API Configuration
- Configure API access
- Show API service configuration

### 📈 Traffic Statistics
- Show interface traffic
- Show traffic statistics

### 🔌 Interface Details
- Show interface details
- Show ether1 details

### 🏷️ VLAN
- Show VLAN configuration
- Show VLAN list

### 🌉 Bridge
- Show bridge configuration
- Show bridge ports

### 📊 Queues/Bandwidth
- Show queue configuration
- Show bandwidth limits
- Show rate limit rules

### 🌐 Routing
- Show routing configuration
- Show OSPF status
- Show BGP peers

### 🌡️ System Health
- Show system health
- Show temperature/voltage/fan

### 📅 Scheduled Tasks
- Show scheduled tasks
- Show cron jobs

### 📡 Neighbor Discovery
- Show neighbor devices
- Show network device discovery

### 🔗 Active Connections
- Show active connections
- Show connection statistics

### 🏓 Ping Test
- ping 8.8.8.8 on mikrotik

### 📡 Network Scan
- Scan local network
- Scan 192.168.1.0/24
- Find MikroTik devices

### 🎯 Custom Commands
- execute /system/resource/print on mikrotik
- run routeros command /ip/address/print
- execute /interface/print on office device

### 🖥️ Multi-device Support
If multiple devices are configured, you can specify the device name in the command:
- Show server-room mikrotik status
- Show home firewall rules

## Dependencies

- Device API enabled (default port 8728)
- Network reachable

## File Structure

├── SKILL.md           # Skill description (this file)
├── handler.py         # Command processor
└── mikrotik-api/      # API client library
    ├── __init__.py
    ├── client.py      # API client
    ├── commands.py    # Command wrappers
    ├── cli.py         # CLI tool
    └── scanner.py     # Network scanner

## Notes

### ⚠️ Security Warnings

1. **Network Scan Risks**
   - `mikrotik scan` actively scans the local subnet, generating network discovery traffic.
   - May trigger security alerts in production networks.
   - **Recommendation**: Run in isolated/test networks or obtain permission from the network administrator first.

2. **Credential Security**
   - ❌ **DO NOT** save router admin passwords in plaintext in public or unencrypted TOOLS.md.
   - ✅ **Recommended**: Use environment variables (`MIKROTIK_HOST`/`MIKROTIK_USER`/`MIKROTIK_PASS`).
   - ✅ **Recommended**: Use temporary credentials for short-term sessions and delete after use.

3. **Local Commands and Permissions**
   - scanner.py uses `subprocess` to call system commands (`ip`/`hostname`).
   - Requires opening UDP sockets for network scanning.
   - **Ensure**: The environment allows these operations.

## Changelog

### v1.8.6 (2026-03-30)
- Translated entire skill to English (Original by Xiage).
- Updated attribution and maintainer info.

### v1.8.5 (2026-03-09)
- 🔍 **Refactored network scanning** - Switched to API port scanning.
- 📊 **Optimized scan results**.
- 🔧 **Updated scanner.py**.

### v1.8.4 (2026-03-08)
- 💾 **New backup configuration feature**.
- 🧹 **New storage cleanup feature**.
- 🔐 **New API configuration view**.

### v1.8.2 (2026-03-06)
- 🔧 **Fixed firmware display bug**.
- 📋 Added device model and serial number.
- 📶 **New wireless client query (CAPsMAN)**.
- 🎯 **Onboarding optimization for new users**.
- 🔍 **Optimized network scanning**.
- 🆕 Added network scanning (Winbox-like).
