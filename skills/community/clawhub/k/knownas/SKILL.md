---
name: knownas
description: "Give this OpenClaw a stable public name on knownas.dev: HTTPS, a public record of who runs it, and webhook and API addresses that survive tunnel restarts."
homepage: https://knownas.dev
metadata:
  {
    "openclaw":
      {
        "emoji": "🪪",
        "requires": { "bins": ["curl", "jq"], "env": ["KNOWNAS_API_KEY"] },
        "primaryEnv": "KNOWNAS_API_KEY",
      },
  }
user-invocable: true
---

# knownAs: a name for this OpenClaw

knownAs.dev gives an AI agent its own name on the internet, with HTTPS and a
public record of who answers for it. This skill gives *this* gateway a name
such as `myclaw.knownas.dev`, and addresses such as
`myclaw.hooks.knownas.dev` for channel webhooks and `myclaw.api.knownas.dev`
for the gateway's API, that keep working when the tunnel behind them changes.

## Rules

- A person signs up and mints the key. Never create an account, never ask
  for a password, never paste the key into chat or a message.
- Ask before anything that changes public state: creating an identity,
  setting or re-pointing a route, editing a channel's webhook URL.
- Never print `KNOWNAS_API_KEY` or the origin secret. The secret is shown by
  the API once; the helper stores it in OpenClaw's secret store as
  `KNOWNAS_ORIGIN_SECRET_<SERVICE>` without printing it.
- One identity per gateway. The free tier is one identity; say so.
- Publish in the record only what the owner chooses (name, description,
  contact, homepage). Nothing about the machine, the network or the chat.
- If the origin is a loopback, private or IP address, stop and explain: the
  platform refuses those, and so should you.

## How to call the API

Only through the helper, never with your own `curl`:

```bash
sh {baseDir}/scripts/knownas.sh <command> [args]
```

It reads `KNOWNAS_API_KEY` and `KNOWNAS_API_URL` (default
`https://platform.knownas.dev`) from the environment, keeps the key off
every command line, and prints JSON. Exit codes: `0` ok, `2` usage or
missing key, `3` the name is taken, `4` the name is not allowed, `5` the API
refused (its message is printed), `6` the origin is not acceptable.

| Command | What it does |
|---|---|
| `whoami` | The key's scopes and the account's quota |
| `create SLUG NAME [MANIFEST.json] [SERVICE...]` | Creates the identity; services default to `api webhooks` |
| `find SLUG` | The identity's id |
| `wait-active ID` | Waits (up to two minutes) until its DNS is ready |
| `route ID SERVICE ORIGIN` | Points a service at the origin; prints the proof `token` (not a secret) |
| `check ID SERVICE` | Asks the platform to fetch the proof now; stores the origin secret on the first pass |
| `status ID` | Identity, routes and traffic as one JSON document |
| `remove-route ID SERVICE` | Removes a route (idempotent) |
| `origin-ok HOST` | Whether the platform would accept this origin |

Services are `api` (the gateway: A2A and its OpenAI-compatible endpoints),
`webhooks` (channel webhooks, at `<slug>.hooks.knownas.dev`) and `mcp`
(only if the owner runs an MCP server behind the same origin; off by
default).

## Context to find first

- The key works and has `identity:create`, `identity:read`,
  `manifest:write` and `route:write`: `whoami`. If a scope is missing, say
  which, and that a person mints a new key in the console.
- The gateway's public origin, as a host name: `openclaw config get
  channels.a2a.advertisedUrl` (strip `https://` and any path), else the
  Tailscale Funnel name, else ask. Run `origin-ok` on it, then confirm it
  answers: `curl -sS -o /dev/null -w '%{http_code}' https://<origin>/`.
- Whether the `knownas` plugin is installed (`openclaw plugins list`). It
  serves the proof token; without it the owner must serve a file.
- Which channels use webhooks today, and their current URLs.

## Commands

### /knownas setup <name>

1. Tell the owner what will happen and ask for a yes: the identity
   `<name>.knownas.dev` with `api` and `webhooks`, pointed at `<origin>`,
   and what its public record will say. Ask what to publish: display name,
   one-line description, contact email, homepage. Leave out anything they
   do not give.
2. Write the record to a file and create:
   `create <name> "<display name>" record.json`. There is deliberately no
   way to ask whether a name is free (it would let anyone list who uses
   knownAs). On exit `3`, suggest two alternatives, such as
   `<name>-claw` and `<name>-<their initials>`, and ask. On exit `4`, read
   the message (reserved words and brand look-alikes are refused).
3. `wait-active <id>`.
4. For each service: `route <id> <service> <origin>`. Collect the tokens.
5. Serve the tokens. With the plugin:
   `openclaw config set plugins.entries.knownas.config.originTokens '["<api token>","<webhooks token>"]' --strict-json`.
   The gateway applies it without a restart, within seconds. Then check it
   yourself: `curl -sS https://<origin>/.well-known/knownas-origin` must
   show each token on its own line. Without the plugin, tell the owner the exact path
   and that it must return those lines as plain text, with no redirect.
6. For each service: `check <id> <service>`. On `passed: true` the secret is
   stored (`secret_stored: true`). Otherwise explain the one cause and stop:
   `token_absent` (the file is not served, or not every token is in it),
   `timeout` (the origin did not answer in 5 seconds), `redirect` (the
   path redirects; it must answer directly), `forbidden_address` (the name
   resolves to a private address). Exit `5` with "less than a minute":
   wait a minute.
7. Show the three public addresses and what each is for: the record at
   `https://<name>.knownas.dev/.well-known/agent-identity.json`, the gateway
   at `https://<name>.api.knownas.dev`, webhooks at
   `https://<name>.hooks.knownas.dev/<path>`. Offer `/knownas channels`.

### /knownas repoint <origin>

After a tunnel restart. `find <name>`, then for every route that is not
removed: `route <id> <service> <new origin>` (a new token each), serve the
new tokens as in setup step 5, `check` each. Say that the public addresses
did not change, so no channel needs editing.

### /knownas channels

List the channels that receive webhooks and their current URLs. Offer to
point each at `https://<name>.hooks.knownas.dev/<the same path>`; the path
is forwarded unchanged. Edit only the ones the owner names, and ask before
each. Set `channels.a2a.advertisedUrl` to `https://<name>.api.knownas.dev`
the same way.

### /knownas status

`find <name>`, then `status <id>`. Report the identity's state, each route
(`pending`, `verified`, `paused`) with its last check, the traffic in the
window against the limits (`limits.warn_bytes_30d`,
`suspend_bytes_30d`, `suspend_bytes_1h`) in GB, and the record's URL.

### /knownas remove

Ask first. `remove-route` for each service. Then tell the owner that
archiving or deleting the identity is done in the console, by a person,
with the name typed out; this skill never does it.

## When something is wrong

When the owner asks why something is not working, read
`{baseDir}/references/faq.md` first and answer from it; if it does not cover
the question, say so and give ops@knownas.dev.

- A route is `paused`: the daily check missed three times. Fix the origin,
  then `check` again; a pass resumes it.
- The identity is `suspended` with reason `bandwidth_quota`: the owner can
  resume it once per 30 days from the console; the mail they received says
  what happens after that.
- `403` of any kind from the knownAs API, including
  `QUOTA_RESUME_OPERATOR_ONLY`: stop; it is a person's call.
- A request through `<name>.api.knownas.dev` gets `403` with
  `"type":"proxy_attribution_required"` from the **gateway**: OpenClaw
  refuses forwarded traffic on its own token-protected routes until
  `gateway.trustedProxies` names the proxy in front of it (the tunnel). The
  same request straight to the tunnel gets the same answer, so it is not
  knownAs. Channel webhooks and the proof route are not affected. Point the
  owner to OpenClaw's "Reverse proxy configuration" guide; do not change
  `gateway.trustedProxies` yourself.
- The secret: the platform's edge sends it to the gateway as
  `x-knownas-origin-secret`. OpenClaw cannot check it for other plugins'
  routes; an operator who fronts the gateway with a reverse proxy can (see
  the README).
