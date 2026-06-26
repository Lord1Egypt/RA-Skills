---
name: paperclip-orchestration
description: Connect OpenClaw Gateway to Paperclip, diagnose onboarding and reachability failures, claim and store Paperclip API keys, install the Paperclip skill, and orchestrate Paperclip agents and tasks. Use when the user wants to join a Paperclip org, fix Paperclip connectivity, create or manage Paperclip agents, assign work through Paperclip, or monitor Paperclip agent status.
---

# Paperclip orchestration

Use this skill to connect an OpenClaw instance to Paperclip and operate it safely afterward.

## Keep the workflow strict

1. Verify which Paperclip base URL is reachable from the current runtime with `GET <base-url>/api/health`.
2. Fetch and read the invite-specific onboarding text before submitting anything.
3. Determine the OpenClaw gateway URL that Paperclip can reach.
4. Test Paperclip to gateway reachability with the invite's `test-resolution` endpoint.
5. Submit the join request with `adapterType: "openclaw_gateway"` and `agentDefaultsPayload.headers["x-openclaw-token"]`.
6. If join returns or later triggers `pairing required`, approve the pending device pairing in OpenClaw and retry.
7. After board approval, claim the Paperclip API key, save it locally with restrictive permissions, then install any Paperclip skill the onboarding requires.

Do not skip the reachability test. Do not assume a private Docker, LAN, or 172.x address is reachable from Paperclip.

## Connectivity checks

Prefer these checks first:

```bash
curl -fsS https://paperclip.example.com/api/health
openclaw status
openclaw qr --json
openclaw devices list
```

Interpretation:

- `openclaw qr --json` returns the best advertised gateway URL and the `urlSource` that produced it.
- A loopback gateway like `ws://127.0.0.1:18789` is not usable from a remote Paperclip deployment.
- A Tailscale Serve or public HTTPS/WSS URL is usually the right candidate for remote onboarding.
- Pending pairing requests mean network and auth probably worked far enough to require approval, so stop changing URLs until pairing is handled.

If none of the Paperclip hostnames are reachable, ask the user to add a reachable Paperclip hostname and restart Paperclip before retrying.

## Join request requirements

Send a JSON body shaped like this:

```json
{
  "requestType": "agent",
  "agentName": "OpenClaw",
  "adapterType": "openclaw_gateway",
  "capabilities": "OpenClaw gateway agent",
  "agentDefaultsPayload": {
    "url": "wss://your-openclaw-gateway.example",
    "paperclipApiUrl": "https://your-paperclip.example.com",
    "headers": { "x-openclaw-token": "<gateway-token>" },
    "waitTimeoutMs": 120000,
    "sessionKeyStrategy": "issue",
    "role": "operator",
    "scopes": ["operator.admin"]
  }
}
```

Rules:

- Read the token from `~/.openclaw/openclaw.json -> gateway.auth.token`.
- Use `x-openclaw-token` rather than legacy `x-openclaw-auth` unless compatibility forces otherwise.
- Keep device auth enabled unless the environment truly cannot pair.
- Use the working Paperclip base URL for `paperclipApiUrl`.
- Preserve trailing slash normalization exactly as the API returns it.

## Reachability test

Before the join request, call the invite test endpoint with a URL-encoded gateway URL.

```bash
python3 - <<'PY'
import urllib.parse
print(urllib.parse.quote('wss://your-openclaw-gateway.example', safe=''))
PY
```

Then:

```bash
curl -fsS "https://paperclip.example.com/api/invites/INVITE_ID/test-resolution?url=<encoded-url>"
```

Treat an `unreachable` result as a real warning. The join request may still be accepted for approval, but the deployment is not fully healthy until Paperclip can resolve the chosen gateway URL.

## Approval and claim flow

After the join request succeeds:

1. Save `request id`, `claimSecret`, and `claimApiKeyPath`.
2. Wait for board approval.
3. Claim the API key with the one-time claim secret.
4. Save the full claim response to `~/.openclaw/workspace/paperclip-claimed-api-key.json`.
5. `chmod 600 ~/.openclaw/workspace/paperclip-claimed-api-key.json`.
6. Load `PAPERCLIP_API_KEY` and `PAPERCLIP_API_URL` from that file for future runs.

If claim fails before approval, do not rotate secrets or regenerate payloads unnecessarily. Wait for approval and retry once.

## Creating and operating agents

First confirm identity and permissions:

```bash
curl -sS "$PAPERCLIP_API_URL/api/agents/me" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY"
```

Only proceed with agent creation if the response permits it.

When creating Paperclip agents:

- Use a valid Paperclip role enum only.
- Match the role to the work, for example `engineer`, `designer`, `qa`, `researcher`, `pm`, or `general`.
- Keep prompts and adapter config concise.
- Reuse the same validated gateway URL and auth header pattern.

## Troubleshooting

### Invite expired or inactive

Symptom:

```json
{"error":"Invite not found or inactive"}
```

Action: request a fresh invite.

### Join request not yet approved

Symptom:

```json
{"error":"Join request must be approved before key claim"}
```

Action: wait for Paperclip board approval, then retry the claim once.

### Pairing required

Action:

```bash
openclaw devices list
openclaw devices approve --latest
```

Then retry the gateway action that failed.

### Remote gateway unreachable from Paperclip

Common causes:

- loopback or localhost URL
- non-routable LAN or Docker address
- Tailscale or reverse proxy hostname not reachable from the Paperclip host
- wrong scheme, for example testing only `wss://...` when Paperclip reachability probe expects HTTPS on the same hostname

Action: choose a hostname Paperclip can actually resolve, verify `GET /api/health`, then rerun the invite `test-resolution` check.

### Invalid role enum

Use only valid Paperclip roles accepted by the target deployment. If the API rejects a custom role, switch to the nearest supported built-in role.

## Outcome summary template

When the onboarding or repair work is done, report these exact points:

- Paperclip base URL used
- OpenClaw gateway URL used
- Reachability test result
- Join request result and request id
- Claim result
- Whether the Paperclip skill was installed
- Remaining blockers, if any
