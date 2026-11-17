## VPN Integration & Bot Block Handling

Many booking platforms employ bot detection (Cloudflare, PerimeterX, Akamai, DataDome) that can block automated access. Spot integrates with `ocas-vpn` to route traffic through non-US exit nodes when bot blocks are detected.

### Bot Detection Triggers

Auto-detect bot blocks using `detect_bot_block()` from stealth config. Trigger VPN routing when:
- Page loads but booking widget never renders (blank page after 10+ seconds)
- CAPTCHA challenge appears (reCAPTCHA, hCaptcha, CF Turnstile)
- "Access denied" / "Please verify you are human" / "Bot detected" message
- HTTP 403/429 responses from the booking platform
- Availability data returns empty when manual browser check shows availability
- TLS fingerprint or headless browser detection triggers a block

### Automated VPN Workflow

```
1. Attempt booking page load (normal connection)
   ↓
2. Run detect_bot_block() after page load
   ├─ No block → Proceed normally
   └─ Block detected ↓
3. Check VPN status: ip addr show tun0
   ├─ VPN already connected → Kill and reconnect (fresh IP)
   └─ VPN not connected ↓
4. Connect VPN via ocas-vpn skill:
   a. Fetch best non-US server from VPN Gate API
   b. Save config to <fs-root>/vpn_gate.ovpn
   c. openvpn --config <fs-root>/vpn_gate.ovpn --daemon
   d. Wait for tun0, verify non-US exit IP
   ↓
5. Retry booking page load through VPN
   ↓
6. Still blocked?
   ├─ Yes → Try different VPN server (different country)
   │        Rotate through: Japan → Germany → UK → Netherlands → Canada
   └─ No → Proceed with availability check / booking
```

### VPN Server Rotation

Maintain a pool of VPN Gate servers for rotation. When one server fails:
1. Kill current VPN connection
2. Fetch next best server from VPN Gate API (different country preferred)
3. Reconnect and retry
4. Track failed servers in `{agent_root}/commons/data/ocas-spot/vpn-failures.jsonl`

### Platform-Specific Bot Detection & VPN Profiles

| Platform | Bot Detection | VPN Recommended | Preferred Exit | Notes |
|----------|--------------|-----------------|----------------|-------|
| Tock | Cloudflare Turnstile | ✅ Yes | Japan | URL-based iteration avoids most triggers; VPN for persistent blocks |
| OpenTable | Akamai CDN | ✅ Yes | Japan | Session-based workaround preferred; VPN if session expires |
| Mindbody | PerimeterX (HUMAN) | ✅ Yes | Japan/EU | Some deployments block headless; VPN + stealth scripts |
| Fresha | Cloudflare | ✅ Yes | Japan | "Checking your browser" page; VPN to non-US exit |
| Boulevard | Cloudflare | ⚠️ Maybe | Japan | Premium platform; may block aggressive automation |
| Yelp / Yelp Reservations | IP-range block | ✅ Yes | Residential proxy | Standard Yelp bot detection; VPN alone insufficient |
| Resy | None known | ❌ No | — | API-based; no VPN needed |
| Acuity Scheduling | None known | ❌ No | — | REST API; no VPN needed |
| Calendly | None known | ❌ No | — | API-based; no VPN needed |
| Square Appointments | None known | ❌ No | — | Browser automation works without VPN |
| SevenRooms | None known | ❌ No | — | Widget API (no auth) + browser automation; no VPN needed |
| Vagaro | API-level | ⚠️ Maybe | Japan | API errors may be IP-based; VPN can help |
| Meevo | None known | ❌ No | — | Browser automation works without VPN |
| StyleSeat | Basic | ⚠️ Maybe | Japan | Slow down interactions; VPN if blocked |
| Booksy | Cloudflare | ⚠️ Maybe | Japan | Consumer-facing; may have basic bot detection |
| GlossGenius | Minimal | ❌ No | — | Generally accessible |
| SimplyBook.me | Minimal | ❌ No | — | Generally accessible |
| Mangomint | Minimal | ❌ No | — | Generally accessible |
| DaySmart | Minimal | ❌ No | — | Generally accessible |
| ResDiary | Minimal | ❌ No | — | UK/Europe focus; VPN rarely needed |
| Eat App | Minimal | ❌ No | — | Middle East focus; VPN rarely needed |

### VPN Auto-Reconnection

VPN tunnels do not survive gateway/agent restarts. Spot automatically checks VPN health before watch sweeps and booking runs:

```bash
# VPN health check (runs automatically before each booking/vpn operation)
vpn_health_check() {
    # Check if tun0 exists and has an IP
    if ! ip addr show tun0 2>/dev/null | grep -q 'inet '; then
        echo "VPN down, reconnecting..."
        # Fetch fresh server list
        curl -s "https://www.vpngate.net/api/iphone/" | \
            python3 -c "
import csv, base64, sys, json
reader = csv.DictReader(sys.stdin)
servers = [r for r in reader if r.get('CountryShort') != 'US' and r.get('OpenVPN_ConfigData_Base64')]
best = sorted(servers, key=lambda s: int(s.get('Score', 0)), reverse=True)[0]
config = base64.b64decode(best['OpenVPN_ConfigData_Base64']).decode()
with open('<fs-root>/vpn_gate.ovpn', 'w') as f:
    f.write(config)
print(f\"Selected: {best['CountryLong']} (Score: {best['Score']})\")
"
        # Kill any existing openvpn
        pkill -f openvpn 2>/dev/null
        sleep 2
        # Connect
        openvpn --config <fs-root>/vpn_gate.ovpn --daemon --log <fs-root>/openvpn.log
        sleep 5
        # Verify
        ip addr show tun0
    fi
    # Verify exit IP is non-US
    curl -s --max-time 10 https://ipinfo.io/json
}
```

### Browser Routing Through VPN

When VPN is active (tun0 interface up), all system traffic including browser automation routes through the VPN automatically. No special Playwright configuration needed — system routing (`0.0.0.0/1` + `128.0.0.0/1` via tun0) handles it.

**VPN config cipher fix:** When downloading VPN Gate configs, many servers only support `AES-128-CBC`. OpenVPN 2.5+ defaults to GCM ciphers and will fail with `OPTIONS ERROR: failed to negotiate cipher`. Before connecting, patch the config:
```python
config = base64.b64decode(server['OpenVPN_ConfigData_Base64']).decode()
if 'data-ciphers' not in config:
    lines = config.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('cipher '):
            lines.insert(i+1, 'data-ciphers AES-128-CBC:AES-256-GCM:AES-128-GCM')
            break
    config = '\n'.join(lines)
```

For per-browser VPN routing (when multiple browsers need different exit nodes), use Playwright's `proxy` parameter:
```python
context = browser.new_context(
    proxy={'server': 'socks5://10.8.0.1:1080'}  # WireGuard/SOCKS proxy
)
```