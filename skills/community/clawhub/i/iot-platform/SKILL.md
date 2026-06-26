---
name: openclaw-mcp-api
description: "[WIP] Guide to connect to Cloud Studio IoT's OpenClaw platform via MCP API. Use when configuring MCP server connections, sending commands to IoT devices, reading sensor data, or managing channels through the OpenClaw gateway."
---

# OpenClaw MCP API Connection Guide

> **🚧 WIP** -- This skill is under active development. Details may change as the OpenClaw API stabilizes.

## Overview

OpenClaw exposes an MCP (Model Context Protocol) server through its gateway, allowing Claude Code and other MCP clients to interact with IoT devices, read sensor data, and manage channels programmatically.

## Prerequisites

- OpenClaw installed and running (`openclaw --version`)
- Gateway daemon active (`systemctl --user status openclaw-gateway`)
- Gateway healthy (`curl -fsS http://127.0.0.1:18789/healthz`)
- Tailscale configured (for remote access)

## Quick Start

### 1. Verify the Gateway Is Running

```bash
curl -fsS http://127.0.0.1:18789/healthz
# Expected: OK
```

### 2. Configure MCP Client Connection

Add the OpenClaw MCP server to your Claude Code settings (`~/.claude/settings.json` or project `.claude/settings.json`):

```json
{
  "mcpServers": {
    "openclaw": {
      "type": "sse",
      "url": "http://127.0.0.1:18789/mcp"
    }
  }
}
```

For remote access via Tailscale:

```json
{
  "mcpServers": {
    "openclaw": {
      "type": "sse",
      "url": "http://openclaw-desktop:18789/mcp"
    }
  }
}
```

### 3. Verify Connection

Once configured, restart Claude Code and check that the OpenClaw tools appear in the available MCP tools list.

## Gateway Modes

### Loopback (default)

Gateway binds to `127.0.0.1` only. Accessible from the local machine.

```yaml
gateway:
  bind: loopback
  port: 18789
```

### Tailscale Serve (tailnet only)

Accessible from any device on your Tailscale network.

```yaml
gateway:
  bind: loopback
  port: 18789
  tailscale:
    mode: serve
```

### Tailscale Funnel (public with auth)

Publicly accessible with password authentication.

```yaml
gateway:
  bind: loopback
  port: 18789
  tailscale:
    mode: funnel
  auth:
    mode: password
    password: "your-secure-password"
```

## Available MCP Capabilities (WIP)

These are the expected MCP tools and resources exposed by the gateway:

### Tools

| Tool | Description |
|---|---|
| `openclaw_device_list` | List connected IoT devices |
| `openclaw_device_command` | Send a command to a specific device |
| `openclaw_sensor_read` | Read current sensor data |
| `openclaw_channel_list` | List configured channels (Telegram, etc.) |
| `openclaw_channel_send` | Send a message through a channel |
| `openclaw_agent_run` | Run an agent task on the gateway |

### Resources

| URI Pattern | Description |
|---|---|
| `openclaw://devices` | List of all registered devices |
| `openclaw://devices/{id}/sensors` | Sensor readings for a device |
| `openclaw://channels` | Configured communication channels |
| `openclaw://config` | Current gateway configuration |

## Troubleshooting

### Gateway not responding

```bash
systemctl --user restart openclaw-gateway
journalctl --user -u openclaw-gateway -f
```

### MCP connection refused

1. Verify the gateway is healthy: `curl http://127.0.0.1:18789/healthz`
2. Check the port is not blocked: `ss -tlnp | grep 18789`
3. For remote access, confirm Tailscale is connected: `tailscale status`

### Authentication errors (funnel mode)

Ensure the password in your MCP config matches the one in `~/.openclaw/gateway.yaml`.

## Useful Commands

```bash
# Gateway management
openclaw doctor              # Run diagnostics
openclaw config list         # Show current config
openclaw channels list       # List channels

# Device interaction (CLI)
openclaw devices list        # List devices
openclaw devices status      # Device health overview

# Logs
journalctl --user -u openclaw-gateway -f
```

## References

- Gateway config example: `config/gateway.yaml.example`
- Setup scripts: `scripts/`
- OpenClaw docs: https://docs.openclaw.ai/gateway

---

**OpenClaw** — IoT Platform & AI Gateway
https://cloudstudioiot.com/
