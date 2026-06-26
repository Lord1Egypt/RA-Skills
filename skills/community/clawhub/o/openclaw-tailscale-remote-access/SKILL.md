---
name: openclaw-tailscale-remote-access
description: "Configure or repair OpenClaw remote access over Tailscale with a directly executable workflow: inspect state, apply the gateway config, enable Tailscale Serve over HTTPS, validate browser access, and handle origin, DNS, or pairing failures."
metadata:
  openclaw:
    version: "1.0.1"
    homepage: "https://github.com/JiangAgentLabs/openclaw-tailscale-remote-access"
    requires:
      bins:
        - "bash"
        - "python3"
        - "tailscale"
        - "systemctl"
        - "curl"
      configs:
        - "~/.openclaw/openclaw.json"
---

# OpenClaw Tailscale Remote Access

Use this skill when Codex needs to make an OpenClaw gateway reachable over Tailscale and the result must be directly configurable, not just described.

Prefer `Tailscale Serve + HTTPS` for browser access. The recommended shape is:

- OpenClaw binds to `127.0.0.1`
- Browser access goes through `https://<machine>.<tailnet>.ts.net`
- `auth.mode` is `token`
- `auth.allowTailscale` is `true`

## Required Inputs

Collect these values before making changes:

- a non-Tailscale access path to the Linux host
  cloud console or public SSH is preferred
- the OpenClaw config file path
  default: `~/.openclaw/openclaw.json`
- the final MagicDNS hostname
  example: `<machine>.<tailnet>.ts.net`
- the gateway token to place in the config

## Skill Resources

Resolve the skill directory first so Codex can call the bundled scripts even if the skill is still in `~/Downloads`:

```bash
export SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/openclaw-tailscale-remote-access"
if [ ! -d "$SKILL_DIR" ] && [ -d "$HOME/Downloads/openclaw-tailscale-remote-access" ]; then
  export SKILL_DIR="$HOME/Downloads/openclaw-tailscale-remote-access"
fi

export OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
export GATEWAY_PORT="${GATEWAY_PORT:-18789}"
export TS_HOSTNAME="<machine>.<tailnet>.ts.net"
export GATEWAY_TOKEN="<gateway-token>"
```

## Safety Rules

1. Do not run `tailscale up` from a Tailscale SSH session.
2. If you need to change Tailscale state, prefer a cloud console or public SSH session.
3. Do not switch OpenClaw to `bind: "tailnet"` unless the user explicitly accepts HTTP-only access and weaker browser behavior.
4. On a Mac client, keep Tailscale DNS enabled if the browser must resolve `*.ts.net`.

## Direct Workflow

### 1. Inspect Current State

Run the bundled inspector first:

```bash
bash "$SKILL_DIR/scripts/inspect_remote_access.sh" "$OPENCLAW_CONFIG"
```

Use the output to answer these questions before changing anything:

- is `openclaw-gateway` running
- is Tailscale running
- is an HTTPS Serve handler already present
- are there pending pairing requests

### 2. Confirm the Session Is Safe For `tailscale up`

Use these checks:

```bash
printf 'SSH_CONNECTION=%s\n' "${SSH_CONNECTION:-<none>}"
hostname
tailscale ip -4 2>/dev/null || true
```

If the current shell is reached through Tailscale SSH or through a Tailscale IP, stop and switch to cloud console or public SSH before changing Tailscale state.

### 3. Apply the OpenClaw Gateway Config

The bundled script creates a timestamped backup and updates only the gateway fields needed for remote access:

```bash
python3 "$SKILL_DIR/scripts/apply_gateway_config.py" \
  --config "$OPENCLAW_CONFIG" \
  --ts-hostname "$TS_HOSTNAME" \
  --token "$GATEWAY_TOKEN" \
  --port "$GATEWAY_PORT"
```

The script enforces this shape:

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "controlUi": {
      "allowedOrigins": [
        "http://localhost:18789",
        "http://127.0.0.1:18789",
        "https://<machine>.<tailnet>.ts.net"
      ]
    },
    "auth": {
      "mode": "token",
      "token": "<gateway-token>",
      "allowTailscale": true
    },
    "tailscale": {
      "mode": "serve",
      "resetOnExit": false
    }
  }
}
```

### 4. Restart The Gateway

```bash
systemctl --user restart openclaw-gateway
systemctl --user status openclaw-gateway --no-pager
```

If the service does not return to `active (running)`, fix that before touching Tailscale Serve.

### 5. Start Or Repair Tailscale In Low-Impact Mode

Use this only from a safe session:

```bash
tailscale up --accept-dns=false --accept-routes=false --ssh=false
```

If Tailscale says all non-default flags must be restated, rerun `tailscale up` with the existing non-default flags plus the flags above. Do not use `--reset` blindly.

### 6. Configure HTTPS Serve

Use the bundled helper:

```bash
bash "$SKILL_DIR/scripts/configure_tailscale_serve.sh" --port "$GATEWAY_PORT"
```

If the node already has Serve config that must be replaced, rerun with:

```bash
bash "$SKILL_DIR/scripts/configure_tailscale_serve.sh" --reset-first --port "$GATEWAY_PORT"
```

Expected mapping:

```text
https://<machine>.<tailnet>.ts.net/ -> http://127.0.0.1:18789/
```

### 7. Validate End To End

Run these checks in order:

```bash
tailscale status --json
tailscale serve status --json
systemctl --user status openclaw-gateway --no-pager
tailscale ip -4
curl -vkI --resolve "$TS_HOSTNAME:443:$(tailscale ip -4 | head -n1)" "https://$TS_HOSTNAME/"
```

Expected results:

- Tailscale backend is `Running`
- Serve reports an HTTPS handler on TCP 443
- `openclaw-gateway` is `active (running)`
- the HTTPS request reaches the service and does not fail at DNS or TLS handshake

## Client Repair

If the browser client is a Mac and `*.ts.net` stopped resolving after Tailscale changes, do not change the server bind mode. Repair the client first:

```bash
tailscale set --accept-routes=false
tailscale set --accept-dns=true
scutil --dns | grep -E 'ts.net|tailscale'
nslookup "$TS_HOSTNAME"
```

## Pairing Required

If the dashboard loads but reports `pairing required`:

```bash
cat ~/.openclaw/devices/pending.json
openclaw devices list
openclaw devices approve <requestId>
```

If the CLI path is broken, inspect the installed OpenClaw CLI or Python package on the host and call its built-in approval path. Do not manually edit `pending.json` or `paired.json` unless the user explicitly asks for a last-resort recovery.

## Troubleshooting Priorities

- `origin not allowed`
  `controlUi.allowedOrigins` is wrong; re-run the config script with the correct `TS_HOSTNAME`.
- `ERR_SSL_PROTOCOL_ERROR`, `invalid response`, or TLS handshake failure
  Check `tailscale serve status`, then inspect host DNS and certificate issuance.
- `NXDOMAIN` for `*.ts.net` on the client
  Fix client MagicDNS; do not switch the server to `bind: "tailnet"` just to bypass DNS.
- `pairing required`
  Approve the pending device on the gateway host.

## References

- Read [remote-setup.md](./references/remote-setup.md) when you need the exact host-side setup sequence.
- Read [troubleshooting.md](./references/troubleshooting.md) when configuration is already in place but access still fails.
