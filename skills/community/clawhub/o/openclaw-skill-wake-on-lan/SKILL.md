---
name: wake-on-lan
description: Wake-on-LAN functionality for macOS - wake devices remotely by MAC address or name
triggers:
  - "wake"
  - "wol"
  - "wake on lan"
  - "wake device"
commands:
  wake_by_mac:
    description: Wake a device by its MAC address
    usage: "wake <MAC address> [broadcast IP]"
    examples:
      - "wake 00:11:22:33:44:55"
      - "wake 00:11:22:33:44:55 192.168.1.255"
  wake_by_name:
    description: Wake a saved device by name
    usage: "wake-name <device name>"
    examples:
      - "wake-name desktop"
      - "wake-name server"
  list_devices:
    description: List all saved Wake-on-LAN devices
    usage: "list"
    examples:
      - "list"
  add_device:
    description: Add a new device to the config
    usage: "add <name> <MAC address> [broadcast IP] [ping IP]"
    examples:
      - "add desktop 00:11:22:33:44:55"
      - "add server 00:11:22:33:44:55 192.168.1.255"
      - "add server 00:11:22:33:44:55 192.168.1.255 192.168.1.100"
  remove_device:
    description: Remove a device from config
    usage: "remove <device name>"
    examples:
      - "remove desktop"
  query_status:
    description: Check if a device is online by pinging it
    usage: "status <device name>"
    examples:
      - "status desktop"
  broadcast:
    description: Wake all saved devices at once
    usage: "broadcast"
    examples:
      - "broadcast"
---

# Wake-on-LAN Skill

Wake devices on your local network using Wake-on-LAN (WOL) magic packets.

## Installation

```bash
# Install wakeonlan tool
brew install wakeonlan

# The skill will automatically create config at:
# ~/.config/openclaw/wol-devices.json
```

## Commands

### Wake by MAC Address
Wake any device on your network using its MAC address:
```
wake <MAC address> [broadcast IP]
```
Example: `wake 00:11:22:33:44:55`

### Wake by Name
Wake a device you've saved in the config:
```
wake-name <device name>
```
Example: `wake-name desktop`

### List Devices
Show all saved devices:
```
list
```

### Add Device
Save a new device for easy access:
```
add <name> <MAC address> [broadcast IP]
```
Example: `add desktop 00:11:22:33:44:55 192.168.1.255`

### Remove Device
Remove a device from the config:
```
remove <device name>
```
Example: `remove desktop`

### Query Status
Check if a device is online (requires IP in config):
```
status <device name>
```
Example: `status desktop`

### Broadcast
Wake all saved devices at once:
```
broadcast
```

## Configuration

Devices are stored in `~/.config/openclaw/wol-devices.json`:
```json
[
  {
    "name": "desktop",
    "mac": "00:11:22:33:44:55",
    "broadcast": "192.168.1.255"
  },
  {
    "name": "server",
    "mac": "AA:BB:CC:DD:EE:FF",
    "broadcast": "192.168.1.255"
  }
]
```

## Requirements

- `wakeonlan` command (install via Homebrew)
- Network access to the broadcast address
- Target devices must support Wake-on-LAN (enabled in BIOS/UEFI and OS)
