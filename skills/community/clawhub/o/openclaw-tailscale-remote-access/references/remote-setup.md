# Remote Setup

Use this reference when Codex needs the exact host-side sequence for a Linux OpenClaw gateway.

## Inputs

Set these variables first:

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

## Recommended Topology

The known-good pattern is:

```text
browser
  -> https://<machine>.<tailnet>.ts.net/
  -> Tailscale Serve on TCP 443
  -> http://127.0.0.1:18789/
  -> OpenClaw gateway bound to loopback
```

Do not expose the raw OpenClaw port publicly.

## Exact Host Workflow

### 1. Inspect Before Changing Anything

```bash
bash "$SKILL_DIR/scripts/inspect_remote_access.sh" "$OPENCLAW_CONFIG"
```

### 2. Make Sure The Shell Is Safe

```bash
printf 'SSH_CONNECTION=%s\n' "${SSH_CONNECTION:-<none>}"
hostname
tailscale ip -4 2>/dev/null || true
```

If this shell is reached through Tailscale SSH, stop and move to cloud console or public SSH before running `tailscale up`.

### 3. Apply The Gateway Config

```bash
python3 "$SKILL_DIR/scripts/apply_gateway_config.py" \
  --config "$OPENCLAW_CONFIG" \
  --ts-hostname "$TS_HOSTNAME" \
  --token "$GATEWAY_TOKEN" \
  --port "$GATEWAY_PORT"
```

The resulting gateway block will include:

- `mode: "local"`
- `bind: "loopback"`
- `auth.mode: "token"`
- `auth.allowTailscale: true`
- `tailscale.mode: "serve"`
- `controlUi.allowedOrigins` for localhost and `https://$TS_HOSTNAME`

### 4. Restart OpenClaw

```bash
systemctl --user restart openclaw-gateway
systemctl --user status openclaw-gateway --no-pager
```

If restart fails, fix OpenClaw first. Do not keep changing Tailscale while the service is down.

### 5. Start Tailscale In Low-Impact Mode

```bash
tailscale up --accept-dns=false --accept-routes=false --ssh=false
```

Intent:

- keep host DNS under the host's existing control
- avoid accepting subnet routes
- avoid turning on Tailscale SSH

### 6. Configure Serve

```bash
bash "$SKILL_DIR/scripts/configure_tailscale_serve.sh" --port "$GATEWAY_PORT"
```

If a stale Serve config must be replaced:

```bash
bash "$SKILL_DIR/scripts/configure_tailscale_serve.sh" --reset-first --port "$GATEWAY_PORT"
```

### 7. Validate

```bash
tailscale status --json
tailscale serve status --json
systemctl --user status openclaw-gateway --no-pager
curl -vkI --resolve "$TS_HOSTNAME:443:$(tailscale ip -4 | head -n1)" "https://$TS_HOSTNAME/"
```

## Resulting Config Shape

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

## Client Notes

On a Mac client, keep MagicDNS enabled if the browser must resolve `*.ts.net`:

```bash
tailscale set --accept-routes=false
tailscale set --accept-dns=true
```
