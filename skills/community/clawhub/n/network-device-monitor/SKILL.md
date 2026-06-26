---
name: network-device-monitor
description: Monitor network devices, detect unknown clients, and alert on new connections. Works with any router that serves a web UI. Tracks device state changes over time.
metadata: {"openclaw":{"emoji":"📡","requires":{"bins":["python3"]}}}
---

# Network Device Monitor

Monitor your network for unknown devices. Works with any router that exposes an HTTP admin panel. Tracks device state changes and alerts on new connections.

## Quick Start

```bash
# Scan your network (requires nmap)
python3 {baseDir}/scripts/scan-network.py --subnet 192.168.1.0/24

# Quick ARP-based scan (faster)
python3 {baseDir}/scripts/scan-network.py --subnet 192.168.1.0/24 --arp
```

## Options

- `--subnet CIDR` — Network range to scan (required)
- `--arp` — Use ARP scan (faster, requires root)
- `--known FILE` — JSON file with known devices (MAC → name mapping)
- `--state FILE` — State file for tracking changes (default: `~/.network-state.json`)
- `--alerts` — Only output when unknown devices are found
- `--json` — Output as JSON
- `--table` — Pretty-print as table

## State Tracking

The monitor saves device state between runs:

```json
{
  "last_scan": "2026-03-29T12:00:00",
  "devices": {
    "AA:BB:CC:DD:EE:FF": {
      "ip": "192.168.1.100",
      "hostname": "my-laptop",
      "first_seen": "2026-03-29T10:00:00",
      "last_seen": "2026-03-29T12:00:00",
      "status": "online"
    }
  },
  "unknown_devices": ["11:22:33:44:55:66"]
}
```

## Alert Mode

Run with `--alerts` for cron/heartbeat integration:
```bash
# Only prints output if unknown devices are detected
python3 scan-network.py --subnet 192.168.1.0/24 --alerts
```

## Known Devices Format

Create a `known-devices.json`:
```json
{
  "AA:BB:CC:DD:EE:FF": "My Laptop",
  "11:22:33:44:55:66": "Smart TV",
  "DE:AD:BE:EF:00:00": "Game Console"
}
```

## Notes

- ARP scan requires root: `sudo python3 scan-network.py --arp`
- nmap scan works without root but is slower
- Works on Linux and macOS
- No external API dependencies
