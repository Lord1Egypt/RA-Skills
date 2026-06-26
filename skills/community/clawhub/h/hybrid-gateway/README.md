# Hybrid Gateway — VPS + Local Node for OpenClaw

Run your OpenClaw gateway on a cloud VPS and connect a local machine (Mac Mini, desktop, Raspberry Pi) as a node — getting the best of both worlds.

## Why?

Most OpenClaw users start on a VPS. It's cheap, always online, and handles messaging (Telegram, Discord, etc.) well. But VPS machines can't do everything:

- **No GPU** — can't run local models (Ollama, Whisper) efficiently
- **Cloud IP** — gets blocked by services that detect datacenter IPs
- **No macOS** — can't use macOS-only tools (Xcode, native apps, etc.)
- **No browser automation** — headless Chrome on a VPS is limited

The hybrid gateway setup solves this: keep the gateway on your VPS for reliability, and add a local node for hardware capabilities.

## What you get

- **VPS handles**: messaging, agent orchestration, model API calls, always-on reliability
- **Local node handles**: GPU inference, browser automation, Whisper transcription, residential IP access, macOS tools
- **Tailscale connects them**: encrypted, zero-config VPN mesh

## Quick start

1. Install Tailscale on both machines
2. Set `gateway.bind: "lan"` on the VPS
3. Run `openclaw node run` on the local machine
4. Approve the device pairing
5. Set `tools.exec.node` to route commands

Full walkthrough in [SKILL.md](./SKILL.md).

## Common gotchas this skill covers

- `gateway.bind` wrong mode breaks local agents OR remote node (use `lan`)
- `ws://` security block on non-loopback (fix: `OPENCLAW_ALLOW_INSECURE_PRIVATE_WS=1` on Tailscale)
- Node `system.run` uses minimal PATH (fix: full binary paths or SSH fallback)
- Device pairing approval required after first connect
- Auto-start setup for macOS (LaunchAgent) and Linux (systemd)

## Install

```bash
clawhub install hybrid-gateway
```

## License

MIT
