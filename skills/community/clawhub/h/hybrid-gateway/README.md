# Hybrid Gateway: VPS + Local Node for OpenClaw

Run the OpenClaw Gateway on a VPS and pair a local machine (Mac Mini, desktop, Raspberry Pi) as a node for the hardware a VPS lacks: GPU and local models, a real browser on a residential IP, macOS tools, local files.

## Security-first (1.1.0)

- Gateway stays on loopback; Tailscale Serve publishes it as `wss://` on the tailnet only. No public port, no Funnel.
- Pairing uses a single-use Node-host join link (Control UI or `openclaw devices join-code`). Tokens and setup codes never go through chat.
- Approve the exact pending request id; capability expansions (including post-upgrade reapproval) are separate approvals.
- Node exec is allowlist + approval gates with absolute-path binaries. No shell in any allowlist.
- SSH is an optional, separately secured fallback, set up in the companion skill.

Every step ends with a verifiable **Done when** check. Full walkthrough in [SKILL.md](./SKILL.md); upgrade procedure in [references/upgrade-notes.md](./references/upgrade-notes.md).

## Companion

[`remote-node-ssh`](https://github.com/jkfaris94/remote-node-ssh) for SSH setup, day-to-day exec, and file transfer once the topology is secure.

## Install

```bash
clawhub install hybrid-gateway
```

## Tested with

OpenClaw 2026.9.3, Node 24, Tailscale 1.x, macOS 26 node, Ubuntu 24.04 VPS.

## License

MIT
