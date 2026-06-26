---
name: hilink-lte
description: Control Huawei HiLink USB LTE modems (E3372, E8372, etc.) via REST API. Send/receive SMS, check signal strength, manage SIM PIN, query prepaid balance, and monitor connection status. Use when sending or reading SMS messages, checking LTE signal/status, entering SIM PIN, querying mobile balance (USSD), or managing a HiLink USB modem.
---

# HiLink LTE Modem

Control Huawei HiLink USB LTE modems via their local REST API.

## Setup

The modem must be in **HiLink mode** (not stick/serial mode) and accessible via HTTP.

### Config

Set gateway IP in `~/.config/hilink/config`:
```bash
HILINK_GATEWAY=192.168.200.1
```

Or pass via environment: `export HILINK_GATEWAY=192.168.200.1`

Default: `192.168.200.1`

### Network Requirements

The LTE USB interface needs an IP on the modem's subnet (e.g., 192.168.200.x). Configure as **static IP with no gateway and no DNS** to avoid routing conflicts:

```
# /etc/network/interfaces.d/lte
allow-hotplug lte0
iface lte0 inet static
    address 192.168.200.100/24
```

**Critical:** Never let the LTE interface set a default route or DNS — it will override your LAN connection. Use `nogateway` and `nohook resolv.conf` in dhcpcd, or a static config with no gateway line.

### Persistent Interface Name

USB network interfaces get random names on each boot. Create a udev rule for a stable name:

```bash
# Find MAC address
cat /sys/class/net/enx*/address

# Create udev rule
echo 'SUBSYSTEM=="net", ACTION=="add", ATTR{address}=="xx:xx:xx:xx:xx:xx", NAME="lte0"' \
  | sudo tee /etc/udev/rules.d/70-lte-modem.rules
```

## CLI Usage

```bash
# SMS
scripts/hilink.sh sms send "+41791234567" "Hello!"
scripts/hilink.sh sms list
scripts/hilink.sh sms read 40001
scripts/hilink.sh sms delete 40001

# Status & Signal
scripts/hilink.sh status
scripts/hilink.sh signal

# SIM PIN
scripts/hilink.sh pin enter 1234
scripts/hilink.sh pin disable 1234
scripts/hilink.sh pin status

# Prepaid Balance (USSD)
scripts/hilink.sh balance

# Connection info
scripts/hilink.sh info
```

## API Overview

All HiLink API calls require a session token + CSRF token pair:

```bash
# Get tokens
curl -s http://GATEWAY/api/webserver/SesTokInfo
# Returns: <SesInfo>cookie</SesInfo><TokInfo>csrf_token</TokInfo>

# Use in requests
curl -X POST http://GATEWAY/api/endpoint \
  -H "Cookie: <SesInfo value>" \
  -H "__RequestVerificationToken: <TokInfo value>" \
  -H "Content-Type: application/xml" \
  -d '<xml request body>'
```

For detailed API endpoints, see [references/api.md](references/api.md).

## Troubleshooting

- **Error 113018 on SMS send**: SIM not registered to network. Check PIN status and signal.
- **SimState 260**: PIN required. Enter PIN first via `scripts/hilink.sh pin enter <PIN>`.
- **SignalStrength 0**: No network registration. Wait after PIN entry or check antenna.
- **DNS/routing broken**: LTE interface set a default route. Remove it: `sudo ip route del default via 192.168.200.1`
- **Interface name changed**: USB MAC randomized. Create udev rule (see Setup).
