# PPIO Sandbox: Browser Use Integration

Reference: https://ppio.com/docs/sandbox/integrate-browser-use

## Template

- **Template ID**: `browser-chromium`
- **Pre-installed**: Chromium browser with remote debugging
- **CDP Port**: 9223 (Chrome DevTools Protocol)

## Architecture

```
Local machine (OpenClaw)                 PPIO Cloud (Firecracker VM)
┌──────────────────────────┐            ┌──────────────────────────┐
│ OpenClaw browser tool    │───CDP────→ │ Chromium (port 9223)      │
│ (Playwright, native)     │   HTTPS    │ browser-chromium template │
└──────────────────────────┘            └──────────────────────────┘
```

OpenClaw's native browser tool connects to the sandbox Chromium via CDP.
The browser is isolated in the VM — no access to local filesystem or internal network.

## How It Works

1. Create sandbox with `browser-chromium` template
2. Get CDP URL via `sandbox.get_host(9223)` → `https://{host}`
3. Configure OpenClaw browser profile with that CDP URL
4. OpenClaw's browser tool connects and controls the browser natively

## Security Boundaries

The sandbox Chromium is isolated:
- **No local filesystem access** (VM boundary)
- **No internal network access** (nftables blocks 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- **No cloud metadata access** (169.254.0.0/16 blocked)
- **Internet access allowed** (for normal browsing)
- **Ephemeral** (destroyed on kill, paused on timeout)

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `PPIO_API_KEY` / `E2B_API_KEY` | Yes | PPIO API key |
| `E2B_DOMAIN` | No | Default: `sandbox.ppio.cn` |
