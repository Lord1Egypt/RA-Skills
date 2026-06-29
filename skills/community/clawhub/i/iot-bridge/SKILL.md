---
name: iot-bridge
version: 1.0.6
description: Bridge IoT devices to the cloud via aitun tunnel. Expose local MQTT brokers, device dashboards, or HTTP APIs so remote devices and services can connect, report data, and receive commands.
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: AITUN_SERVER
        required: false
        description: "AiTun server address (default: aitun.cc:6639)"
    install:
      - kind: pip
        package: aitun
        bins: [aitun]
      - kind: uv
        package: aitun
        bins: [aitun]
    emoji: "📡"
    homepage: https://aitun.cc
    clawhub: https://clawhub.ai/ctz168/iot-bridge
---

# IoT Bridge - Connect IoT Devices via Aitun Tunnel

## When to Use

Use this skill when:
- You have IoT devices on a local network that need to be accessible from the internet
- You want to expose a local MQTT broker or IoT gateway for remote device connections
- You need to access a local IoT dashboard (Home Assistant, Node-RED, Grafana) remotely
- You want to bridge local sensors or actuators to a cloud platform for data aggregation
- You need to test IoT integrations where the device or service is behind NAT/firewall

Do NOT use this skill when:
- The IoT platform is already cloud-hosted and publicly accessible
- You only need local device-to-device communication (no tunnel needed)
- You want to share a static file (use sendfile instead)

## Instructions

### Step 1: Install aitun

```bash
pip install aitun
```

Or install via one-line script (Linux/macOS):
```bash
curl -fsSL https://aitun.cc/install.sh | bash
```

Windows (PowerShell):
```powershell
irm https://aitun.cc/install.ps1 | iex
```

Or verify it is already installed:

```bash
which aitun
```

### Step 2: Start the local IoT service

Start the IoT service you want to expose. Examples:

```bash
# Home Assistant
hass --config /path/to/config &

# Node-RED
node-red --port 8080 &

# Mosquitto MQTT broker
mosquitto -p 1883 -v &

# Custom IoT HTTP API / dashboard
python3 -m http.server 8080 --directory /path/to/dashboard &

# Grafana dashboard
grafana-server --homepath /usr/share/grafana &
```

### Step 3: Create a tunnel

For HTTP-based services (dashboards, REST APIs):

```bash
aitun -p 8080 &
AITUN_PID=$!
sleep 3
```

For TCP-based services (MQTT broker on port 1883, use with auth token):

```bash
aitun -k YOUR_TOKEN --tcp-ports 1883 &
AITUN_PID=$!
sleep 3
```

The output will contain the public URL, e.g.:
- `https://aitun.cc/abc123` (HTTP)
- TCP forwarding address for MQTT

### Step 4: Share the IoT endpoint

```
Your IoT service is now accessible at: https://aitun.cc/abc123

- Dashboard: open in browser
- API endpoint: use for device data upload
- MQTT broker: connect via TCP forwarding

This tunnel expires in 24 hours.
For a permanent endpoint, register at https://aitun.cc
```

### Step 5: Connect remote devices or services

Configure remote IoT devices or cloud services to use the tunnel URL:

- **HTTP devices**: Set the reporting URL to `https://aitun.cc/abc123/api/data`
- **Cloud platforms**: Configure the webhook or data source URL to the tunnel address
- **MQTT devices**: Connect to the TCP-forwarded MQTT broker address
- **Dashboard users**: Open the URL in a browser to view live data

### Step 6: Clean up

When done, stop the tunnel and services:

```bash
kill $AITUN_PID 2>/dev/null
```

## CLI Reference

The `aitun` command (installed via `pip install aitun`, or alternatively `curl -fsSL https://aitun.cc/install.sh | bash` / `irm https://aitun.cc/install.ps1 | iex` on Windows) accepts these flags:

| Flag | Description |
|---|---|
| `-p PORT` | Local HTTP service port (optional; omit for TCP-only mode with `--tcp-ports`) |
| `-k TOKEN` | Auth token for registered subdomain (omit for free tunnel) |
| `--host HOST` | Local service address (default: localhost) |
| `--tcp-ports PORTS` | TCP forwarding ports, comma-separated (e.g., `22,3306`; requires `-k`). Use without `-p` for TCP-only mode |
| `--p2p` | Enable P2P direct connection (default: enabled) |
| `--no-p2p` | Disable P2P, force server relay mode |
| `--daemon` | Run as background daemon |
| `--stop` | Stop running daemon |

## Notes

- Free tunnels use proxy address mode (path-based URL like `aitun.cc/abc123`), NOT subdomains
- Free tunnels expire after 24 hours, auto-renewed on restart
- For a permanent IoT endpoint, register at https://aitun.cc to get a custom subdomain
- TCP forwarding (for MQTT, Modbus, etc.) requires a registered account and `-k` token
- Use `--tcp-ports` to forward multiple TCP ports: `--tcp-ports 1883,5683,502`
- For security, enable authentication on your IoT services before exposing them
- All traffic is encrypted end-to-end
- P2P mode reduces latency for real-time device communication
- Consider rate limiting for high-frequency sensor data
