---
name: otterkit-tunnel
description: Expose a local port to the internet via OtterKit tunnel, or create a webhook endpoint to capture incoming HTTP requests. Give your OpenClaw gateway a public HTTPS URL for incoming webhooks (/hooks/wake, /hooks/agent), capture and replay webhook deliveries, and protect tunnels with HTTP Basic auth. Use when the user asks to "tunnel", "expose", "share my localhost", needs a public URL for a local service or for OpenClaw webhooks, needs a webhook endpoint to capture requests, or wants to re-test a webhook handler against a previously received payload.
homepage: https://www.otterkit.com/docs
metadata:
  {
    'openclaw':
      {
        'requires': { 'bins': ['npx'] },
        'install': [{ 'id': 'node', 'kind': 'node', 'package': 'otterkit', 'bins': ['otterkit'] }],
      },
  }
---

# OtterKit Tunnel

Expose a local port to the internet instantly via a secure tunnel. Paid with prepaid **OtterKit credits** (1 credit = $0.01), metered by time: **1 credit per connected hour** (first hour charged at provision), **never more than 300 credits ($3) per endpoint per rolling 30 days** - webhooks and tunnels alike. Billing pauses while disconnected, and tunnels auto-stop after a TTL (default 24h) so a forgotten tunnel stops billing. The user logs in once with `otterkit login`; after that the CLI (and any agent on the same machine) provisions automatically, debiting the user's credit balance.

## Prerequisites

The user must be logged in. One-time:

```bash
npx otterkit login
```

This opens the browser, the user approves the device, and a token is saved to `~/.otterkit/credentials.json`. Buy credits at https://console.otterkit.com. New accounts get a small free-credit grant to start.

For headless/CI agents, set `OTTERKIT_TOKEN` (create a token at console.otterkit.com → API Tokens) instead of running `otterkit login`.

Check the logged-in account and balance:

```bash
npx otterkit whoami
npx otterkit balance
```

## OpenClaw: Wake Your Claw From Public Webhooks (zero gateway exposure)

The OpenClaw gateway binds to loopback (default port 18789), so external services can't reach `/hooks/wake` or `/hooks/agent` directly. The safest integration keeps it that way: a capture-only OtterKit endpoint takes the public traffic, and `--deliver-exec` relays each delivery to the gateway on loopback:

```bash
npx otterkit webhook --subdomain my-claw-hooks --daemon --ttl never \
  --deliver-exec 'curl -s -X POST http://127.0.0.1:18789/hooks/wake \
    -H "Authorization: Bearer $OPENCLAW_HOOKS_TOKEN" \
    -H "Content-Type: application/json" -d @-'
```

Point providers at `https://my-claw-hooks.otterkit.app`. Each capture's body arrives on the exec command's stdin (`-d @-` passes it through); metadata comes in `OTTERKIT_*` env vars. The gateway port is never public. Webhook endpoints are answered by OtterKit's servers from the moment they exist - providers always get their 200, even while the laptop is asleep, and up to 200 buffered captures replay into the local log (triggering the relay) on reconnect. Every delivery is in the capture log for `inspect`/`replay`. Use a dedicated `hooks.token`, not the gateway auth token.

Add `--verify <provider>:<secret>` (e.g. `stripe:whsec_…`) so every capture carries a server-checked signature verdict - the exec command sees it in the `OTTERKIT_*` metadata and can skip waking the Claw on unverified events.

An agent can also block on the next delivery instead of polling:

```bash
npx otterkit await my-claw-hooks --count 1 --timeout 120s --json
```

## OpenClaw: Direct Tunnel to the Gateway

If a caller needs a real endpoint on the gateway itself (e.g. `/hooks/agent` responses, or remote Control UI access), tunnel the port with a stable URL:

```bash
npx otterkit tunnel 18789 --subdomain my-claw --daemon --ttl 7d
```

Then hand providers the public hook URL (keep `hooks.token` required in `openclaw.json` - the tunnel does not remove auth):

```bash
curl -X POST https://my-claw.otterkit.app/hooks/wake \
  -H 'Authorization: Bearer HOOKS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"text":"CI build failed","mode":"now"}'
```

Notes for this setup:

- `--subdomain` gives the same URL across restarts, so provider configs don't go stale. Holding the name is free.
- Add `--log` to capture every delivery for `inspect`/`replay` debugging.
- The tunnel forwards the whole gateway port. Keep the gateway token and hooks token set; use a dedicated hooks token, not the gateway auth token. Stop the tunnel (`otterkit stop my-claw`) when public access isn't needed. Prefer the capture-and-relay setup above when providers only need to deliver events.

## When to Use

- User wants external events (CI, Stripe, GitHub, forms, sensors) to wake their OpenClaw agent
- User asks to expose a local port or server to the internet
- User needs a public URL for a local development server or their OpenClaw gateway webhooks
- User wants to share their localhost with others
- User needs a webhook endpoint to capture incoming HTTP requests (no local server needed)
- User needs to receive webhook callbacks from third-party services (Stripe, GitHub, Slack, etc.)
- User needs to debug webhook integrations (capture + forward + replay)
- User fixed a webhook handler and wants to re-test it against a real captured payload
- User wants the public tunnel URL protected so only callers with credentials reach their server

## Commands

### Tunnel (1 credit/hour)

```bash
npx otterkit tunnel <port>                     # foreground, Ctrl+C to stop
npx otterkit tunnel <port> --daemon --ttl 4h   # background, auto-stops after TTL (default 24h, or "never")
npx otterkit tunnel <port> --subdomain myapp   # stable URL: https://myapp.otterkit.app every run
npx otterkit tunnel <port> --auth user:pass    # require HTTP Basic auth (enforced locally, free)
npx otterkit tunnel <port> --log               # also capture every request for inspect/replay
```

Default URLs are random (`https://agent-<hex>.otterkit.app`); `--subdomain` claims a persistent name to the user's account (free to hold; if taken, the command fails with no charge). `--auth` returns 401 before anything reaches the local server; credentials never touch OtterKit's servers.

Pricing: 1 credit/hour while connected, first hour at provision, never more than 300 credits ($3) per endpoint per rolling 30 days, free while disconnected.

### Webhook Endpoint (capture-only, no local server)

```bash
npx otterkit webhook [--daemon] [--ttl 4h] [--subdomain name]
npx otterkit webhook --respond 204                              # custom auto-response status
npx otterkit webhook --respond 200 --respond-body '{"ok":true}' # custom body (challenge echoes)
npx otterkit webhook --email                                    # also give the endpoint an inbox: <subdomain>@otterkit.app
```

Every request is saved to `~/.otterkit/requests/<subdomain>.jsonl`. Same pricing as tunnels. Endpoints are **server-answered**: OtterKit's servers respond, capture, verify, and forward whether or not the CLI is connected - the terminal is a live viewer, and up to 200 captures that arrived while it was away replay into the local log on reconnect.

Local delivery and waiting:

```bash
npx otterkit webhook --deliver 3000                    # mirror every capture to a local server
npx otterkit webhook --deliver-exec './on-event.sh'    # run a command per capture (body on stdin, OTTERKIT_* env)
npx otterkit await <subdomain> --count 1 --timeout 120s --json   # block until a matching request lands (exit 2 on timeout)
```

### Signature Verification (`--verify`)

Server-side check of each request's provider signature at arrival; the verdict (verified/invalid/unsigned) is stored on the capture and reaches local delivery as an `X-OtterKit-Verified` header. Never blocks the request - it's a badge (and a gate for forward rules via `--verified-only`).

```bash
npx otterkit webhook --verify stripe:whsec_abc123
npx otterkit webhook --daemon --verify github:my-webhook-secret
```

Presets: stripe, github, shopify, slack, svix (Resend/Clerk/Polar), paddle, zoom, linear, lemonsqueezy, dropbox, gitlab, twilio, square, hubspot, discord, sendgrid.

### Server-Side Forwarding (`--forward`)

A forwarding rule delivers matching requests to another URL - HMAC-signed, retried with backoff, and it works **while the machine is off** (unlike `--deliver`, which is local-only). `--match` clauses combine: `method=`, `path=` (prefix), or any JSON-body dot-path equality. `--forward-transform` reshapes the delivery with `{{dot.path}}` templates - which turns forwarding into Slack/Discord/ntfy notifications with no relay server.

```bash
npx otterkit webhook --match event.type=payment.succeeded --forward https://ci.example.com/hooks/payments
npx otterkit webhook --daemon --match type=payment_intent.succeeded \
  --forward REDACTED-SECRET \
  --forward-transform '{"text": "Paid: {{data.object.amount}} {{data.object.currency}}"}'
npx otterkit webhook --verify stripe:whsec_… --verified-only --forward https://…   # only verified events forward
```

### Notifications

```bash
npx otterkit webhook --notify-email                          # email on arrivals (works with machine off, throttled)
npx otterkit webhook --notify-match event.type=payment.failed # conditional email rule
npx otterkit webhook --notify-push [k=v]                     # web push to enabled devices
```

### Cloud History (`requests`)

Cloud endpoints (created in the console) store up to 10,000 captures server-side, readable from any machine; CLI endpoints keep captures in the local JSONL log only (use `inspect`).

```bash
npx otterkit requests <subdomain> --json --method POST --limit 100
```

### Inspect & Replay Captured Requests

```bash
npx otterkit inspect <subdomain>                        # last 20 captures
npx otterkit inspect <subdomain> --json --last 50       # raw JSONL for piping
npx otterkit inspect <subdomain> --follow               # live-tail
npx otterkit inspect <subdomain> --method POST --status 5xx --path /hook
npx otterkit inspect <subdomain> --har > session.har    # HAR 1.2 export

npx otterkit replay <subdomain>                         # re-send latest capture to the local server
npx otterkit replay <subdomain> --index 3 --target 127.0.0.1:3000
npx otterkit replay <subdomain> --method PUT -H "X-Debug: 1" --body '{"event":"retry"}' --json
```

`replay` re-sends straight to the local server - no tunnel round-trip, **no credits spent**. Ideal loop: capture the real payload once, fix the handler, replay until it returns 200. Exit code 0 whenever the local server responded (even 4xx/5xx), 1 if unreachable.

### Project Config (`otterkit up` / `down`)

Define profiles in `otterkit.toml`, bring them all up as daemons with one idempotent command:

```toml
[tunnels.claw]
port = 18789
subdomain = "my-claw"
log = true
ttl = "7d"

[tunnels.hooks]
webhook = true
respond = 200
```

```bash
npx otterkit up --json
npx otterkit down
```

### Status, Stop, Account

```bash
npx otterkit status              # running daemons: URL, target, TTL, PID
npx otterkit stop <subdomain>    # stop a daemon
npx otterkit subdomains          # list/reserve/release stable names
npx otterkit whoami              # account + balance
```

### JSON Output (use when scripting)

Prefer `--json` on `tunnel --daemon`, `webhook --daemon`, `up`, `down`, `status`, `inspect`, `replay`, `subdomains list`, `whoami`, `balance`. Provision results include `{subdomain, publicUrl, target, pid, ttl, expiresAt, logPath}`. Errors are JSON too (e.g. `{"error":"insufficient_credits","topUpUrl":"..."}`) with exit code 1.

```bash
URL=$(npx otterkit tunnel 3000 --daemon --json | jq -r .publicUrl)
```

## Troubleshooting

- "Not logged in" → `npx otterkit login` (one-time), or set `OTTERKIT_TOKEN` for headless machines.
- "Out of credits" / `insufficient_credits` → top up at https://console.otterkit.com/billing.
- Pricing check: `curl https://otterkit.app/api/agent/pricing`
