---
name: "netstatus"
description: "Combined network + gateway status with VPN info, IP location, and system health"
---

# netstatus — Network + Gateway Status

Show combined network and gateway status including VPN state, public IP location, local network details, Tailscale, and system health.

## When to Use

Use `/netstatus` or `/net` when you want a quick overview of:
- Current VPN connection (country, IP, provider)
- Local network interfaces and private IPs
- Tailscale / mesh network status
- Gateway health and uptime
- System status
- Whether traffic is routed through VPN or direct

## Commands

| Command | Description |
|---------|-------------|
| `/netstatus` | Full network + gateway status |
| `/net` | Alias for `/netstatus` |

## Output Format

```
🌐 Network Status
━━━━━━━━━━━━━━━━━━━━━
🛡️ VPN: ProtonVPN 🇸🇪 (Stockholm)
    Public IP: 159.26.108.93
    Provider: AS208172 Proton AG
    Interface: utun2 (mtu 1380)

🏠 Local Network
    WiFi (en0): 192.168.1.42
    Gateway: 192.168.1.1

🔗 Tailscale
    Interface: utun3
    IPs: 100.92.54.38, fd7a:115c:a1e0::1
    Status: running

🌍 Public IP: 159.26.108.93 (same as VPN — no leak)

🖥️ Gateway: Running (14h 29m)
    Model: kimi/k2.7
    Context: 27k/131k (20%)

⏱️ System: 19h 44m uptime
    Load: 2.32 1.82 1.62
```

Or compact mode:
```
🌐 SE 159.26.108.93 | 🏠 192.168.1.42 | 🖥️ k2.7 20% | ⏱️ 19h 44m
```

## Implementation

The skill runs these checks in sequence:

### 1. All Network Interfaces
```bash
# macOS: list all interfaces with their IPv4/IPv6 addresses
ifconfig | awk '/^[a-zA-Z0-9]+:/ { iface=$1 } /inet / { print iface, $2 }'

# Alternative: get specific interface IPs
ipconfig getifaddr en0  # WiFi
ipconfig getifaddr en1  # Ethernet / Thunderbolt
```

Interface categories to detect:
| Pattern | Type | Example |
|---------|------|---------|
| `en0`, `en1` | Physical (WiFi/Ethernet) | `192.168.x.x` |
| `utun[0-9]+`, `tun[0-9]+` | VPN / tunnel | `10.x.x.x`, public IP |
| `utun[0-9]+` with `100.x` | Tailscale | `100.x.y.z` |
| `lo0` | Loopback | `127.0.0.1` |
| `awdl0` | Apple Wireless Direct Link | link-local |
| `bridge0` | Bridge | usually no IP |

### 2. VPN Detection
```bash
# Check for tunnel interfaces
ifconfig | grep -E "^(utun|tun|ppp)"

# Get public IP via VPN
curl -s --connect-timeout 5 https://ipinfo.io/json
```

### 3. Tailscale Detection
```bash
# Check if tailscaled is running
pgrep -x tailscaled >/dev/null && echo "running" || echo "stopped"

# Tailscale IPs (if interface exists)
ifconfig utun3 2>/dev/null | grep inet

# Or use tailscale CLI
tailscale status --json 2>/dev/null | jq -r '.Self.TailscaleIPs[]'
```

### 4. Default Gateway
```bash
# macOS
netstat -rn | grep default | head -3

# Linux
ip route | grep default
```

### 5. IP Location
```bash
curl -s --connect-timeout 5 https://ipinfo.io/json
```

### 6. Gateway Status
Read from runtime or `openclaw gateway status`.

### 7. System Uptime
```bash
# macOS
uptime

# Linux
uptime -p
```

## Interface Categorization Rules

1. **Physical**: `en*`, `eth*`, `wlan*` → "Local Network"
2. **VPN tunnel**: `utun*`, `tun*`, `ppp*` with public IP or non-local range → "VPN"
3. **Tailscale**: `utun*` with `100.64.0.0/10` range → "Tailscale"
4. **Loopback**: `lo*` → skip or show as "Loopback"
5. **Other**: `awdl*`, `bridge*` → "Other" or skip

## IP Leak Detection

Compare VPN state against public IP reachability:
- If VPN interfaces exist AND public IP is reachable → traffic routed through VPN ✅
- If no VPN interfaces but public IP exists → direct connection (no VPN)

Note: The public IP will NOT match the VPN tunnel interface IP (e.g., ProtonVPN uses `10.x.x.x` on the tunnel while the exit IP is public). Checking for IP equality is incorrect — instead, check if VPN is up and internet is reachable.

## macOS vs Linux

| Check | Linux | macOS |
|-------|-------|-------|
| List interfaces | `ip -4 addr show` | `ifconfig` |
| Get interface IP | `ip addr show dev eth0` | `ipconfig getifaddr en0` |
| VPN interface | `ip addr show tun0` | `ifconfig \| grep utun` |
| Default gateway | `ip route \| grep default` | `netstat -rn \| grep default` |
| Uptime parsing | `uptime -p` | `uptime` (raw output) |
| Tailscale check | `tailscale status` | `tailscale status` |

## Error States

| State | Display |
|-------|---------|
| VPN down | `🛡️ VPN: DISCONNECTED` |
| IP mismatch | `⚠️ IP leak detected: VPN=SE but public=IN` |
| Can't reach ipinfo | `🌍 Public IP: unreachable` |
| Tailscale down | `🔗 Tailscale: not running` |
| No local network | `🏠 Local Network: no active interface` |

## Notes

- Uses `ipinfo.io` for geolocation (free tier, no auth needed)
- Caches result for 30 seconds to avoid rate limits
- Requires `curl`, `jq`, `ifconfig` (macOS) or `ip` (Linux)
- VPN detection uses `utun` on macOS, `tun` on Linux
- Tailscale uses `100.64.0.0/10` (CGNAT range) for mesh IPs
