The current version of this file is at https://knownas.dev/faq.md

# knownAs.dev FAQ: forwarding, OpenClaw, traffic limits, API keys

The sections of the knownAs.dev FAQ an agent needs when its owner asks why a name is not working. The full FAQ is at the address above.

## Forwarding (routes)

### How does forwarding work?

You tell the platform where your agent is reachable over HTTPS (its
*origin*, a public host name such as `abc.trycloudflare.com` or
`myclaw.example.org`), per service. The platform gives you a **token** and
asks you to serve it at `https://<origin>/.well-known/knownas-origin`. When
the check finds the token there, the route is verified, and requests to
`yourname.api.knownas.dev` (or `.hooks.`, `.mcp.`) are forwarded to your
origin with the path and method unchanged. The tunnel or proxy in front of
your agent stays; only the public name changes, and it never changes again.

### Which origins are refused?

Loopback (`localhost`), private and link-local addresses, bare IP
addresses, names with a scheme, port or path, and anything under
`knownas.dev`. Give a public host name only; it must answer HTTPS on port
443 with a valid certificate.

### The check failed. What does the outcome mean?

| Outcome | Meaning | What to do |
|---|---|---|
| `token_absent` | The path answered, but not with your token on a line of its own | Serve the exact token; one per line if you have several |
| `redirect` | The path redirected | It must answer directly, with a 200 |
| `timeout` | No answer within 5 seconds | Is the tunnel up? Is the origin reachable from the internet? |
| `tls_failed` | The certificate did not verify | A real certificate for that name; a quick tunnel provides one |
| `forbidden_address` | The name resolves to a private or forbidden address | Use a public origin |
| `dns_failed` / `no_such_name` | The name does not resolve | Check the spelling; wait for DNS |
| `connect_failed` | Nothing accepted the connection on 443 | The service behind the name is down |
| `http_error` | The path answered with an error status | Make it answer 200 |
| `too_large` / `malformed` | The answer was not a small text file | Serve plain text, a few lines at most |

### "Checked less than a minute ago"

The check runs at most once a minute per route. Fix the cause, wait a
minute, check again.

### Do I have to keep serving the token?

**Yes.** Every verified route is re-checked daily. One miss moves the next
check a day on; three misses in a row **pause** the route (traffic stops;
the name still resolves). Fix the origin and run a check: a pass resumes it.
Pressing "check" repeatedly does not count against you.

### What is the origin secret, and why was it shown only once?

On the check that first verifies a route, the platform issues a secret and
sends it to your origin on every forwarded request as the
`x-knownas-origin-secret` header. If your server checks it, traffic that
did not come through knownAs.dev can be refused. It is shown once; store it
where your server can read it. Setting the route again issues a new one.
Tokens are not secrets; the secret is.

### My name answers 404

No verified route for that service. Either no route was set, the check has
not passed yet, or the route is paused. The console's identity page shows
each route's state.

### My name answered 530 (or 502) after my tunnel restarted

Your tunnel got a new host name and the route still points at the old one.
Set the route again with the new origin (in OpenClaw, `/knownas repoint`),
serve the new token, and check; the public name is unchanged, so nothing
that points at it needs editing. On the dev test this took about 35 seconds
end to end.

### I removed a route, but the name still answers for a while

Removal reaches the edge in about 35 seconds. After that the name answers
404 and drops out of the record's endpoints.

### Does the forwarder change my request?

No. The method, path, query and body reach your origin as sent, over HTTPS
to port 443. The `x-knownas-origin-secret` header is added. Responses are
passed back as they are; the read timeout is 60 seconds.

### Can I forward WebSockets or long-running streams?

Request and response forwarding, with a 60-second read timeout. Long
streams and WebSockets are not promised during the beta; tell
`ops@knownas.dev` what you need.

---

## OpenClaw

### How do I give my OpenClaw a name?

Install the `knownas` skill (and its small plugin) from ClawHub, put your
API key in OpenClaw's secret store, then say `/knownas setup <name>`. The
skill asks before it creates anything public. It creates the name, points
the `api` and `webhooks` services at your gateway's public origin, serves
the proof tokens through the plugin, runs the checks, and shows you the
three public addresses. The README in `authecity/openclaw-knownas` has the
exact commands.

### Where does the API key come from?

A person mints it in the console, under API keys, with the scopes
`identity:create`, `identity:read`, `manifest:write` and `route:write`, and
an expiry. Store it in OpenClaw's secret store; the skill reads it from
there and never prints it. Never paste it into a chat.

### My gateway answers 403 "proxy_attribution_required" through the name

That is OpenClaw's rule for its authenticated routes behind **any** proxy
or tunnel, not something we add: until `gateway.trustedProxies` names your
proxy, those routes refuse. Channel webhooks, the A2A routes and the proof
route are unaffected. The skill's README gives the setting line.

### I already have a stable hostname from a named Cloudflare tunnel. What do I gain?

A stable name is only part of it. The rest is the public record: a page at
a well-known path saying who answers for the agent and whether it is in
good standing, in an open format other tools can read; and names for the
agent's services that do not depend on which tunnel you use this month.
If you only want a hostname and own a domain, you may not need us.

### Does the plugin protect my gateway?

No, and it says so. The plugin serves the proof tokens and nothing else.
OpenClaw's plugin system cannot let one plugin guard another's routes, so
a "secret check" there would be protection that is not there. Your channels
keep their own verification; if you front the gateway with a reverse proxy,
the proxy can enforce the origin secret for everything (the README shows a
Caddy example).

### The skill says the name is taken. Can it check another?

It cannot ask whether a name is free (by design; see "Why was my name
refused?"), so it suggests two alternatives and tries the one you choose.

---

## Traffic limits

### How much traffic can a name carry?

Per name, counted at the edge in both directions, headers included:

| Line | Amount | What happens |
|---|---|---|
| Warning | 12.5 GB in 30 days | One email |
| Suspension | 25 GB in 30 days | The name is suspended |
| Burst | 5 GB in one hour | The name is suspended at once |

The edge's own 404s are not counted. A busy personal agent moving webhook
payloads uses a small fraction of this; the lines exist to stop a name
being used as a free file server. Nothing is billed for traffic.

### What does "suspended" mean?

Forwarding stops, the service names answer 404 within about a minute, and
the public record says `suspended`. The record and the name are not
deleted; your settings and routes are kept.

### How do I resume?

From the console, once per 30-day window. The email you received says the
rest: after a self-resume you have about a day; if traffic stays above the
line the name is suspended again, and that one only an operator can lift.
Write to `ops@knownas.dev` and say what the traffic is.

### Where do I see my usage?

The identity page's Traffic card in the console, or
`GET /v1/identities/{id}/usage` with a key that has `identity:read`. Usage
is counted hourly from the edge's logs, so the latest hour or two fills in
late.

### Will the limits change?

We will review the lines at the end of October 2026, after the first month
of real traffic: whether there should be a free line and a higher paid
line, and whether going over a line should pause forwarding rather than
suspend the public record. Lines do not go down for existing names without
notice.

---

## API keys and the API

### Where is the API?

`https://platform.knownas.dev` (production). Its OpenAPI document is
published at the public launch; until then, ask `ops@knownas.dev` for it.
The old `execute-api` URL still answers but should not be given to anyone
new.

### How do I get a key, and what can it do?

Mint it in the console under API keys, choosing scopes and an expiry. The
token is shown **once**. Scopes: `identity:create`, `identity:read`,
`identity:update`, `identity:suspend`, `identity:delete`, `manifest:write`,
`route:write`, `audit:read`, `apikey:read`, `apikey:write`, `dns:read`.
Give an agent the narrowest set that does its job; a key cannot grant
scopes it does not have, and no key can change the account, sign in, or
verify a domain.

### 401 or 403: which is which?

**401** means the key was missing, malformed, expired or revoked: mint or
check the key. **403** means the key is fine but lacks the scope, or the
action is a person's or an operator's (for example resuming a name a second
time). `GET /v1/me` tells you what a key is and what it may do.

### I lost the key

It cannot be shown again; only its hash is stored. Revoke it in the console
and mint another.

### Why did I get 429?

The API has rate limits per account, and the route check allows one call a
minute per route. Back off and retry after the time in the response.

### Can I use it from a tool rather than code?

The MCP server in `clients/mcp` exposes the API as tools for Claude Code,
Claude Desktop, Cursor and similar: list and create identities, read the
record, update it, read audit events. It needs only the key; the URL
defaults to the platform's.
