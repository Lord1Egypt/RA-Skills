---
name: tailscale-manager
description: >
  Manage Tailscale tailnet from chat. Check status, list devices, ping hosts,
  run network diagnostics, check serve/funnel config. All public IPs are
  automatically masked in output (after JSON parsing, not before).
  Triggers on "tailscale status", "tailnet", "connected devices", "network check",
  "ping tailscale", "tailscale devices", "chi è connesso".
  NOT for: modifying serve/funnel config, administrative Tailscale operations.
dependencies:
  - tailscale CLI (https://tailscale.com/kb/1080/cli)
---

# Tailscale Manager

Secure Tailscale network management with automatic IP masking.

## Usage

```bash
python3 scripts/tailscale_ctrl.py status          # Network overview
python3 scripts/tailscale_ctrl.py devices         # Connected devices
python3 scripts/tailscale_ctrl.py ip              # This device's IPs
python3 scripts/tailscale_ctrl.py ping <host>     # Ping a device
python3 scripts/tailscale_ctrl.py netcheck        # Network diagnostics
python3 scripts/tailscale_ctrl.py serve-status    # Current serve config
python3 scripts/tailscale_ctrl.py whois <ip>      # Who is this IP
```

All commands support `--json` for structured output.

## Security

- **Command whitelist**: Only safe read-only commands (`status`, `ip`, `ping`, `netcheck`, `whois`, `serve-status`)
- **No write access**: Cannot modify serve/funnel config, change ACLs, or administer tailnet
- **IP masking**: Public IPs automatically replaced with `[IP-MASKED]`
- **No auth keys**: Never accesses or exposes Tailscale auth keys
- **No secrets**: Does not read config files or tokens

## What's Masked

| Kept | Masked |
|------|--------|
| Tailscale IPs (100.x.x.x) | Public IPs |
| DNS names | External IPs |
| Online/offline status | — |
