# Troubleshooting

## REST works on VPS but fails on the laptop

Symptom:

```bash
curl http://localhost:3210/v1/models
```

returns connection refused on the user's Mac or local machine.

Cause:
- Proxima REST is listening on the VPS loopback, not on the user's local machine.

Fix:

```bash
ssh -L 3210:127.0.0.1:3210 root@<VPS_IP>
```

Then retry the local curl.

## Electron refuses to start

Symptom:

```text
Running as root without --no-sandbox is not supported. See https://crbug.com/638180.
```

Cause:
- Electron or Chromium was started as root.

Fix:
- run the app as the `proxima` user through systemd
- keep sandboxing intact

## IDE MCP config looks correct but never connects

Common causes:
- SSH still asks for a password
- SSH alias is wrong
- `proxima-mcp` is missing or not executable
- `proxima-app.service` is not active
- no provider session is logged in yet

Fix sequence:
1. `ssh proxima-vps 'echo OK'`
2. `ssh -T proxima-vps proxima-mcp`
3. `systemctl status proxima-app.service --no-pager`
4. `curl http://127.0.0.1:3210/v1/models` on the VPS

## Browser shows `ERR_INVALID_HTTP_RESPONSE` on port 5902

Cause:
- user opened a VNC port with a browser.

Fix:
- use a VNC client for `localhost:5902`
- use noVNC on `localhost:6081` for browser access

## noVNC works but clipboard is frustrating

This is common. Browser clipboard forwarding is weaker than native VNC.

Fix:
- prefer a native VNC client for smoother paste and keyboard shortcuts
- if staying in noVNC, use its clipboard panel rather than relying on `Cmd+V`

## `/v1/models` shows old-looking names

Cause:
- Proxima exposes provider aliases there, not a trustworthy real-time exact-model entitlement list.

Explain:
- this does not prove MCP is using an old model
- it also does not guarantee exact premium-model pinning
- Proxima is routing by provider more than by exact model slug

## Everything is green but answers still fail

Possible causes:
- provider session expired
- login incomplete due to CAPTCHA or 2FA
- browser automation broke due to provider UI changes

Fix:
- open the remote GUI
- confirm the provider is visibly logged in
- try a simple test prompt in the UI or via MCP
- if needed, restart `proxima-app.service` and re-check logs
