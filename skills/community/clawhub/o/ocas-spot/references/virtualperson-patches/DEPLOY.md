# VirtualPerson + VPN Gate — Deployment Guide

Patched version of [VirtualPerson](https://github.com/0xyg3n/VirtualPerson) that uses our existing VPN Gate (OpenVPN) tunnel instead of Mullvad.

## Architecture

```
Host Server
├── VPN Gate (OpenVPN) → tun0 (Japan exit)
├── SOCKS5 bridge (microsocks) → 127.0.0.1:1080 via tun0
└── Docker Container (VirtualPerson)
    ├── Xvfb :99 (virtual display)
    ├── Chrome → CDP :9222 → proxy → host SOCKS5 → tun0 → VPN exit
    ├── x11vnc :5900 (VNC)
    ├── websockify :6080 (noVNC)
    └── Hermes Agent gateway
```

## Prerequisites

- Ubuntu 22.04+ with Docker & Docker Compose
- VPN Gate config at `<fs-root>/vpn_gate.ovpn`
- `microsocks` installed (or auto-installed by bridge script)

## Quick Start

### 1. Start VPN Gate

```bash
# Connect to VPN Gate (Japan server)
openvpn --config <fs-root>/vpn_gate.ovpn --daemon --log <fs-root>/openvpn.log

# Wait for connection
sleep 5
ip addr show tun0
curl -s https://ipinfo.io/json  # Should show JP IP
```

### 2. Start SOCKS5 Bridge

```bash
# Start the SOCKS5 proxy that routes through tun0
./vpn-socks5-bridge.sh start

# Verify
./vpn-socks5-bridge.sh status
curl --socks5 127.0.0.1:1080 https://ipinfo.io/json  # Should show JP IP
```

### 3. Deploy VirtualPerson

```bash
# Copy patched files over the original VirtualPerson repo
cp virtualperson-patches/docker-compose.yml VirtualPerson/docker-compose.yml
cp virtualperson-patches/launch-chrome.sh VirtualPerson/launch-chrome.sh
cp virtualperson-patches/entrypoint.sh VirtualPerson/entrypoint.sh

cd VirtualPerson
docker compose up -d

# Verify
docker logs hermes 2>&1 | grep -E '\[entrypoint\]|\[launch-chrome\]'
docker exec hermes curl -sf http://127.0.0.1:9222/json/version
```

### 4. Verify VPN Routing from Container

```bash
# Check Chrome's exit IP from inside the container
docker exec hermes curl -sf --socks5 host.docker.internal:1080 https://ipinfo.io/json

# Should show Japan IP (same as host's VPN exit)
```

### 5. Access VNC

```bash
# SSH tunnel
ssh -N -L 6080:localhost:6080 user@your-server

# Open in browser
# http://localhost:6080/vnc.html
```

## VPN Rotation

When you need to rotate to a different VPN server:

```bash
# On the host:
pkill -f openvpn
sleep 2

# Get new server (different country preferred)
curl -s "https://www.vpngate.net/api/iphone/" -o /tmp/vpn_list.csv
python3 << 'EOF'
import csv, base64
with open('/tmp/vpn_list.csv', newline='') as f:
    content = f.read()
lines = content.split('\n')
data_lines = [l for l in lines if not l.startswith('*') and l.strip()]
reader = csv.DictReader(data_lines)
rows = list(reader)
non_us = [r for r in rows if r.get('CountryShort','').strip() != 'US' and r.get('OpenVPN_ConfigData_Base64','').strip()]
# Pick best from a different country (e.g., Korea instead of Japan)
kr = [r for r in non_us if r['CountryShort'] == 'KR']
jp = [r for r in non_us if r['CountryShort'] == 'JP']
target = (kr or jp or non_us)[0]
config = base64.b64decode(target['OpenVPN_ConfigData_Base64']).decode()
if 'data-ciphers' not in config:
    lines2 = config.split('\n')
    for i, line in enumerate(lines2):
        if line.startswith('cipher '):
            lines2.insert(i+1, 'data-ciphers AES-128-CBC:AES-256-GCM:AES-128-GCM')
            break
    config = '\n'.join(lines2)
with open('<fs-root>/vpn_gate.ovpn', 'w') as f:
    f.write(config)
print(f"Selected: {target['CountryLong']} {target['IP']}")
EOF

# Reconnect
openvpn --config <fs-root>/vpn_gate.ovpn --daemon
sleep 5

# Restart SOCKS5 bridge (it auto-detects the new tun0)
./vpn-socks5-bridge.sh restart

# Verify new exit IP
curl --socks5 127.0.0.1:1080 https://ipinfo.io/json
```

## Integration with ocas-spot

Once VirtualPerson is running, ocas-spot can use it as a VPN-routed browser:

```python
# In ocas-spot browser automation scripts:
# Instead of launching a local Playwright browser, connect to VirtualPerson's CDP

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Connect to VirtualPerson's Chrome via CDP
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    page = browser.new_page()
    
    # All traffic automatically routes through VPN Gate
    page.goto("https://www.opentable.com/r/restaurant-name")
    
    # ... booking automation ...
```

## Troubleshooting

### Chrome can't reach the SOCKS5 proxy
- Verify the bridge is running: `./vpn-socks5-bridge.sh status`
- Check tun0 is up: `ip addr show tun0`
- Test from container: `docker exec hermes curl -sf --socks5 host.docker.internal:1080 https://ipinfo.io/json`

### VPN connection drops
- The watchdog in entrypoint.sh will restart Chrome when CDP goes down
- Restart the bridge: `./vpn-socks5-bridge.sh restart`
- If tun0 is down, reconnect VPN: `openvpn --config <fs-root>/vpn_gate.ovpn --daemon`

### Cipher negotiation fails
- VPN Gate servers often use AES-128-CBC
- The patched config includes `data-ciphers AES-128-CBC:AES-256-GCM:AES-128-GCM`
- If a server still fails, try a different one from the VPN Gate list

### Docker can't reach host.docker.internal
- On Linux, add `extra_hosts: ["host.docker.internal:host-gateway"]` to docker-compose.yml (already in patched version)
- Alternative: use `--network host` mode (less isolated)