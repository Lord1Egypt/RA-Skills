# Troubleshooting

Use this order. Do not keep changing OpenClaw, Tailscale, and client DNS at the same time.

## Contents

- Gateway health
- Tailscale health
- HTTPS and certificate failures
- `origin not allowed`
- `pairing required`
- `NXDOMAIN` for `*.ts.net`

## 1. Gateway Health

Check the service first:

```bash
systemctl --user status openclaw-gateway --no-pager
journalctl --user -u openclaw-gateway -n 100 --no-pager
```

If the service is not `active (running)`, stop here and fix OpenClaw before changing Tailscale.

## 2. Tailscale Health

Check both the network state and Serve state:

```bash
tailscale status --json
tailscale netcheck
tailscale serve status --json
tailscale ip -4
```

Look for:

- `BackendState: "Running"`
- recent peer handshakes
- an HTTPS handler on TCP 443
- a valid local Tailscale IPv4 address

If `tailscale ping --verbose <peer>` starts on DERP and later switches to a direct endpoint, that is normal.

## 3. HTTPS And Certificate Failures

Common symptoms:

- `ERR_SSL_PROTOCOL_ERROR`
- `invalid response`
- Serve exists but the browser cannot finish TLS

Check:

```bash
tailscale serve status --json
journalctl -u tailscaled -n 100 --no-pager
resolvectl query acme-v02.api.letsencrypt.org
curl -vkI --resolve "$TS_HOSTNAME:443:$(tailscale ip -4 | head -n1)" "https://$TS_HOSTNAME/"
```

Common Linux root cause:

- `tailscaled` cannot resolve ACME endpoints because `systemd-resolved` on `127.0.0.53` is timing out

If host DNS is unstable, add explicit upstream resolvers:

File:

- `/etc/systemd/resolved.conf.d/99-openclaw-dns.conf`

Example:

```ini
[Resolve]
DNS=1.1.1.1 8.8.8.8
FallbackDNS=1.0.0.1 8.8.4.4
DNSStubListener=yes
```

Then:

```bash
sudo systemctl restart systemd-resolved
journalctl -u tailscaled -n 50 --no-pager
```

## 4. `origin not allowed`

Cause:

- `gateway.controlUi.allowedOrigins` does not include the exact browser origin

Fix it by re-running the config script with the correct hostname:

```bash
python3 "$SKILL_DIR/scripts/apply_gateway_config.py" \
  --config "$OPENCLAW_CONFIG" \
  --ts-hostname "$TS_HOSTNAME" \
  --token "$GATEWAY_TOKEN" \
  --port "${GATEWAY_PORT:-18789}"

systemctl --user restart openclaw-gateway
```

The required origin must be exactly:

```text
https://<machine>.<tailnet>.ts.net
```

## 5. `pairing required`

Check for pending requests:

```bash
cat ~/.openclaw/devices/pending.json
openclaw devices list
```

Approve the specific request:

```bash
openclaw devices approve <requestId>
```

If the CLI path is broken:

```bash
command -v openclaw
python3 - <<'PY'
import shutil
print(shutil.which("openclaw"))
PY
```

Then inspect the installed CLI or package on the host and use its built-in approval path. Do not hand-edit `pending.json` or `paired.json` unless the user explicitly wants a last-resort recovery.

## 6. `NXDOMAIN` For `*.ts.net` On The Client

This is a client-side MagicDNS problem, not a server bind problem.

On the client:

```bash
tailscale set --accept-dns=true
tailscale set --accept-routes=false
scutil --dns | grep -E 'ts.net|tailscale'
nslookup "$TS_HOSTNAME"
```

If `nslookup` shows `100.100.100.100` and resolves to the host's Tailscale IP, MagicDNS is working.

If the client still does not resolve `*.ts.net`, keep debugging the client DNS path. Do not change the server to `bind: "tailnet"` just to work around name resolution.
