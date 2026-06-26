---
name: netmap
description: |
  Scan and map all devices on the local network. Discovers IPs, hostnames, vendors, and device types. Tracks when devices first appeared and were last seen. Supports labeling devices with friendly names and searching by IP, hostname, MAC, or type.

  USE WHEN: User asks what's on their network, wants to find a device's IP (printer, NAS, TV, etc.), wants to see new/unknown devices, or needs to diagnose connectivity issues. Also use when an IP is needed for a specific device (e.g. "what IP is my printer?").

  DON'T USE WHEN: User asks about internet speed, WiFi signal strength, or remote networks they're not connected to.
---

# netmap

Scans the local network and maintains a persistent device database at `~/.config/netmap/devices.json`.

## Requirements

- `nmap` must be installed: `brew install nmap`
- Script: `scripts/netmap.py`

## Commands

```bash
# Discover all devices on the network (fast, ~30-60s)
python3 scripts/netmap.py scan

# Deep scan — also port-scans each device to identify type (slower, ~2-3min)
python3 scripts/netmap.py scan --deep

# Override subnet (auto-detected by default)
python3 scripts/netmap.py scan --subnet 10.0.0.0/24

# List all known devices
python3 scripts/netmap.py list
python3 scripts/netmap.py list --times   # include first/last seen

# Find a device by IP, hostname, MAC, vendor, or device type
python3 scripts/netmap.py find printer
python3 scripts/netmap.py find 192.168.1.12
python3 scripts/netmap.py find Canon

# Label a device with a friendly name
python3 scripts/netmap.py label 192.168.1.12 "Canon Printer"
python3 scripts/netmap.py label AA:BB:CC:DD:EE:FF "Kevin's iPhone"

# Show devices first seen in the last N minutes
python3 scripts/netmap.py new --minutes 30

# Export device database as JSON
python3 scripts/netmap.py export

# Continuous watch mode (scans every 2min by default)
python3 scripts/netmap.py watch
python3 scripts/netmap.py watch --interval 60
```

## Notes

- MAC addresses and vendor info require running with `sudo` (or they appear blank without it)
- Deep scan adds port-based device fingerprinting: identifies printers, NAS, SSH servers, Apple devices, etc.
- Device database persists across scans — labels survive rescans
- Subnet is auto-detected from the machine's default interface
- Run `scan --deep` first time to populate device types, then `scan` for fast refreshes
