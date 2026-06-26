# Wake-on-LAN Skill for OpenClaw

Remotely wake devices on your local network using Wake-on-LAN magic packets.

## Features

- 🎯 Wake devices by MAC address
- 📋 Save devices by name for quick access
- 📱 List all saved devices
- ➕ Add/remove devices from config
- 🔍 Query device status (ping)
- 📢 Broadcast wake signal to all devices

## Installation

```bash
# Install the wakeonlan tool (required)
brew install wakeonlan
```

The skill will automatically manage your device configuration at:
`~/.config/openclaw/wol-devices.json`

## Usage

### Wake a device by MAC address
```
wake 00:11:22:33:44:55
wake 00:11:22:33:44:55 192.168.1.255
```

### Wake a device by name
```
wake-name desktop
wake-name server
```

### List saved devices
```
list
```

### Add a new device
```
add desktop 00:11:22:33:44:55
add server AA:BB:CC:DD:EE:FF 192.168.1.255
add desktop 00:11:22:33:44:55 192.168.1.255 192.168.1.100
```
The fourth parameter is the IP address used for the status/ping check.

### Remove a device
```
remove desktop
```

### Check device status
```
status desktop
```

### Wake all devices
```
broadcast
```

## Configuration

Devices are stored in JSON format:

```json
[
  {
    "name": "desktop",
    "mac": "00:11:22:33:44:55",
    "broadcast": "192.168.1.255",
    "ip": "192.168.1.100"
  },
  {
    "name": "server",
    "mac": "AA:BB:CC:DD:EE:FF",
    "broadcast": "192.168.1.255",
    "ip": "192.168.1.200"
  }
]
```

## Requirements

- **wakeonlan**: Install via `brew install wakeonlan`
- **Network**: Devices must be on the same local network
- **WOL Support**: Target devices must have Wake-on-LAN enabled in:
  - BIOS/UEFI settings
  - Operating system network driver

## Troubleshooting

1. **Device won't wake**:
   - Verify WOL is enabled in BIOS/UEFI
   - Check if device is connected via Ethernet (WOL typically doesn't work over WiFi)
   - Ensure correct MAC address
   - Try a different broadcast address

2. **Status check fails**:
   - Make sure the device has an IP configured in the config
   - Check firewall settings on the target device

3. **Command not found**:
   - Run `brew install wakeonlan` to install the required tool

## License

MIT License - see LICENSE file for details.
