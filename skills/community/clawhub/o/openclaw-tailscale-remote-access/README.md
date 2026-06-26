# OpenClaw Tailscale Remote Access

[中文说明](./README.zh-CN.md)

Codex/OpenClaw skill for configuring or repairing OpenClaw remote access over Tailscale with a directly executable workflow.

## Links

- ClawHub: https://clawhub.ai/skills/openclaw-tailscale-remote-access
- GitHub: https://github.com/JiangAgentLabs/openclaw-tailscale-remote-access

## What This Skill Does

- Inspects OpenClaw, Tailscale, and Tailscale Serve state before changing anything.
- Applies a known-good OpenClaw gateway config for `Tailscale Serve + HTTPS`.
- Configures the Tailscale Serve mapping to `http://127.0.0.1:18789/`.
- Guides end-to-end validation and common repair paths for origin, DNS, TLS, and pairing issues.

## Quick Start

Install from ClawHub into an OpenClaw workspace:

```bash
clawhub install openclaw-tailscale-remote-access
```

Or copy/clone the skill into your local Codex skill directory:

```bash
git clone git@github.com:JiangAgentLabs/openclaw-tailscale-remote-access.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/openclaw-tailscale-remote-access"
```

Typical locations:

- OpenClaw workspace: `~/.openclaw/workspace/skills/openclaw-tailscale-remote-access`
- Codex user skills: `~/.codex/skills/openclaw-tailscale-remote-access`

Set the required values:

```bash
export SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/openclaw-tailscale-remote-access"
export OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
export GATEWAY_PORT="${GATEWAY_PORT:-18789}"
export TS_HOSTNAME="<machine>.<tailnet>.ts.net"
export GATEWAY_TOKEN="<gateway-token>"
```

Run the standard flow:

```bash
bash "$SKILL_DIR/scripts/inspect_remote_access.sh" "$OPENCLAW_CONFIG"
python3 "$SKILL_DIR/scripts/apply_gateway_config.py" \
  --config "$OPENCLAW_CONFIG" \
  --ts-hostname "$TS_HOSTNAME" \
  --token "$GATEWAY_TOKEN" \
  --port "$GATEWAY_PORT"
systemctl --user restart openclaw-gateway
tailscale up --accept-dns=false --accept-routes=false --ssh=false
bash "$SKILL_DIR/scripts/configure_tailscale_serve.sh" --port "$GATEWAY_PORT"
```

## Repository Layout

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── remote-setup.md
│   └── troubleshooting.md
└── scripts/
    ├── apply_gateway_config.py
    ├── configure_tailscale_serve.sh
    └── inspect_remote_access.sh
```

## Included Scripts

- `scripts/inspect_remote_access.sh`: checks host identity, Tailscale state, Serve state, OpenClaw service status, config file, and pending pairing requests.
- `scripts/apply_gateway_config.py`: backs up and updates `openclaw.json` with the recommended gateway configuration.
- `scripts/configure_tailscale_serve.sh`: creates or resets the HTTPS Serve mapping to the local OpenClaw gateway.

## Primary Workflow

1. Confirm you are not changing Tailscale state from a Tailscale SSH session.
2. Inspect current state with `inspect_remote_access.sh`.
3. Apply the gateway config with `apply_gateway_config.py`.
4. Restart `openclaw-gateway`.
5. Run `tailscale up --accept-dns=false --accept-routes=false --ssh=false` from a safe session.
6. Configure Serve with `configure_tailscale_serve.sh`.
7. Validate HTTPS access to `https://<machine>.<tailnet>.ts.net/`.

## Compatibility

- Host: Linux system with `systemd`, `tailscale`, `python3`, `bash`, and `curl`
- Client notes included for macOS MagicDNS repair
- Primary config path: `~/.openclaw/openclaw.json`

## Documentation

- Main skill: [SKILL.md](./SKILL.md)
- Host-side setup: [references/remote-setup.md](./references/remote-setup.md)
- Troubleshooting: [references/troubleshooting.md](./references/troubleshooting.md)

## Release Notes

See [CHANGELOG.md](./CHANGELOG.md).

## Inspiration

This repository layout follows the common pattern used by public skill projects and ClawHub examples:

- a concise top-level pitch
- a copy-paste quick start
- a visible repository structure
- explicit script inventory
- a separate changelog and UI metadata file
