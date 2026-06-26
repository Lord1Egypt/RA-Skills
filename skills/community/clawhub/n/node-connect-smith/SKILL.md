---
name: node-connect
description: Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. Use when manual connect fails, local Wi-Fi works but VPS/tailnet does not, or errors mention pairing required, unauthorized, bootstrap token invalid or expired, gateway.bind, gateway.remote.url, Tailscale, or plugins.entries.device-pair.config.publicUrl.
---

# Node Connect

Goal: find the one intended route from node -> gateway, verify OpenClaw config matches that route, then fix pairing/auth.

## Instructions

## Step 0: topology gate

Classify the intended route before executing any command. If the route is unclear, ask at most two short questions:

1. Same device, emulator, or USB tunnel? → `same machine`
2. Same local Wi-Fi / LAN? → `same LAN`
3. Same Tailscale tailnet? → `same Tailscale tailnet`
4. Public URL or reverse proxy? → `public URL / reverse proxy`

If the route is still ambiguous after two questions, stop and ask for:

- the intended topology
- whether they used manual host/port or a manually entered WebSocket URL
- the exact app text/status/error, quoted exactly if possible
- whether `openclaw devices list` shows a pending pairing request

Do not guess from `can't connect`.
Do not mix topologies.

- Same-machine / emulator / USB-tunnel problem: keep the diagnosis on loopback / explicit local forwarding first. Do not switch to LAN, Tailscale, or public URL unless the user is truly leaving the local machine.
- Local Wi-Fi problem: do not switch to Tailscale unless remote access is actually needed.
- VPS / remote gateway problem: do not keep debugging `localhost` or LAN IPs.

If topology is `same machine`, short-circuit the network ladder:

- prefer loopback or the explicit forwarded local address the user is actually using
- verify the setup/manual URL is local (`127.0.0.1`, `localhost`, or the tunnel endpoint)
- do not recommend `gateway.bind=lan`, Tailscale, or `publicUrl` unless the route is no longer local

## Canonical checks

Prefer config-driven route checks. Read only the minimum config needed to identify the intended route.

## Execution order

⚠️ Sequential execution only. Do not run approval checks, `nodes` checks, extra route/auth checks, or fallback commands until the numbered steps explicitly branch to them. Never run commands speculatively.

### Phase 1 — route discovery (always first)

1. Confirm the intended topology first.
2. If topology is `same machine`, use a local-only route check first and skip remote-route advice unless the user is actually leaving the local machine.
3. Read only the core route selectors first:

```bash
openclaw config get gateway.mode
openclaw config get gateway.bind
openclaw config get gateway.tailscale.mode
openclaw config get gateway.remote.url
openclaw config get plugins.entries.device-pair.config.publicUrl
```

4. Match the effective route against the route map below.
5. Stop here if the route already matches the intended topology.

### Phase 2 — manual entry gate

Before treating config as the full truth, check whether the user is troubleshooting a manually entered route.

Ask this only when relevant:

- Is the app using a manual host/port or manual WebSocket URL?
- If yes, what exact address did they enter?

Rules:

- For default config-driven flows, treat the active route config as canonical route evidence.
- For manual host/port or manual WebSocket entry, treat the manually entered address as intended-route evidence and compare config against that address.
- If the user cannot say whether a manual address was used, fall back to the default config route map.

### Phase 3 — route mismatch / route unknown only

Run only the smallest config subset that matches the mismatch you already identified. Do not dump every route/auth key unless the mismatch type is still unclear.

If the mismatch is LAN vs loopback / local bind confusion:

```bash
openclaw config get gateway.bind
```

If the mismatch is Tailscale route confusion (direct tailnet bind vs Serve/Funnel vs no tailnet IP):

```bash
openclaw config get gateway.bind
openclaw config get gateway.tailscale.mode
tailscale status --json
```

If the mismatch is public URL / reverse proxy / Funnel / remote-gateway confusion:

```bash
openclaw config get plugins.entries.device-pair.config.publicUrl
openclaw config get gateway.remote.url
openclaw config get gateway.tailscale.mode
```

If the mismatch is auth-mode expectation on an otherwise correct route:

```bash
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.allowTailscale
```

If the mismatch type is still unclear after reading the route selectors, then fall back once to the broader set:

```bash
openclaw config get gateway.mode
openclaw config get gateway.bind
openclaw config get gateway.tailscale.mode
openclaw config get gateway.remote.url
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.allowTailscale
openclaw config get plugins.entries.device-pair.config.publicUrl
```

### Phase 4 — auth / pairing checks only after the route matches

Run approval-state checks only after the route matches the intended topology, or when the app error explicitly shows an auth / pairing problem.

Device-pair approval path:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

Use `openclaw devices approve <requestId>` after listing current pending requests. Prefer the explicit current request id over `--latest`, because a retried pairing request can supersede an older pending entry.

Auth detail-code branch after the route matches:

- `AUTH_TOKEN_MISSING` → paste/set the required token first; do not rotate devices or rewrite route settings yet.
- `PAIRING_REQUIRED` → approve the pending device request.
- `AUTH_TOKEN_MISMATCH` with `canRetryWithDeviceToken=true` → allow one trusted retry first; if it still fails, use the token-drift recovery path.
- `AUTH_DEVICE_TOKEN_MISMATCH` → rotate or re-approve the affected device token instead of treating it like a fresh route problem.
- `bootstrap token invalid or expired` → old bootstrap payload; generate a fresh bootstrap flow only after the route is correct.
- generic `unauthorized` without detail code → verify the intended auth mode, token/password, and Tailscale expectation.

Token / device-token drift recovery path:

```bash
openclaw config get gateway.auth.token
openclaw devices list
openclaw devices rotate --device <deviceId> --role operator
```

If rotation is not enough, remove the stale pairing, approve the current pending request again, then reconnect.

### Phase 5 — post-route capability verification (optional, narrow scope)

Use these only after route + device pairing are no longer the active problem, and only when you are diagnosing a node that should expose declared commands/capabilities beyond the default companion-app pairing flow.

Do not use this phase for default Android/iOS/macOS companion-app pairing diagnosis.
Use it only when the node explicitly needs node-pair trust / declared command visibility after device pairing already succeeded.

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes status
```

## Read the result, not guesses

The goal is to identify which route OpenClaw is configured to expose and compare that with the route the user actually needs.

## Route map

Match the active config path against the rows below.

| Config signal | Expected topology | If that does not match the intended route |
| --- | --- | --- |
| `gateway.bind=lan` | same Wi-Fi / LAN | keep the diagnosis on LAN; do not switch to Tailscale or public URL unless remote access is actually required |
| `gateway.bind=tailnet` | same Tailscale tailnet (direct tailnet bind, not Serve/Funnel) | verify the user intentionally wants a direct tailnet bind; if they expected Serve/Funnel or a different remote route, treat it as a route mismatch instead of silently accepting it |
| `gateway.tailscale.mode=serve` | same Tailscale tailnet (Serve) | verify Tailscale Serve is the intended route; loopback bind can still be correct here because Serve exposes a reachable tailnet URL while the gateway stays on `127.0.0.1`; do not debug LAN IPs first |
| `gateway.tailscale.mode=funnel` | public URL via Tailscale Funnel (not generic reverse proxy) | verify Tailscale Funnel is really the intended public route; check Funnel-specific auth expectations before debugging generic proxy paths; do not debug LAN IPs first |
| `plugins.entries.device-pair.config.publicUrl` | public URL / reverse proxy | inspect the public URL / proxy path, not LAN-only config |
| `gateway.remote.url` | remote gateway route | inspect the remote gateway route, not local bind settings |
| loopback-only config such as `gateway.bind=loopback` or local-only manual entry | valid only for same-machine flows unless a separate explicit proxy/Serve layer is intentionally advertising the reachable remote URL | fix the route first before changing auth/pairing assumptions |

If the route is still unclear after the route selectors, fall back to:

```bash
openclaw config get gateway.bind
openclaw config get gateway.tailscale.mode
openclaw config get plugins.entries.device-pair.config.publicUrl
openclaw config get gateway.remote.url
```

Then identify the effective route manually and return to the route map.

## Root-cause map

If the effective config is still loopback-only:

- this is fine for same-machine flows
- this is also fine when a separate explicit Serve/proxy layer is intentionally exposing the reachable remote route
- otherwise a remote node cannot connect yet
- `gateway.bind=auto` is not enough if the effective route is still loopback for a route that should be LAN, direct tailnet bind, or public URL
- same LAN: use `gateway.bind=lan`
- same Tailscale tailnet: prefer `gateway.tailscale.mode=serve` or use `gateway.bind=tailnet` if direct tailnet bind is intentional
- public internet: set a real `plugins.entries.device-pair.config.publicUrl`, `gateway.remote.url`, or intentional Tailscale Funnel route

If `gateway.bind=tailnet` is set but no tailnet IP was found:

- gateway host is not actually on Tailscale

If remote mode is intended but `gateway.remote.url` is empty:

- remote-mode config is incomplete

If the app says `pairing required` or the auth detail code is `PAIRING_REQUIRED`:

- network route and auth worked well enough to reach the gateway
- approve the pending device pairing request for the current request id

```bash
openclaw devices list
openclaw devices approve <requestId>
```

If the auth detail code is `AUTH_TOKEN_MISMATCH`:

- shared token does not match the gateway token
- if `canRetryWithDeviceToken=true`, allow one trusted retry first
- if that still fails, follow token drift recovery instead of changing route settings

If the auth detail code is `AUTH_DEVICE_TOKEN_MISMATCH`:

- cached per-device token is stale or revoked
- rotate / re-approve the device token instead of regenerating route guesses

If device pairing succeeds but a node still does not expose the declared commands / capabilities you expected:

- on current OpenClaw builds, node commands are disabled until node pairing is approved
- inspect node-pair state only after the route is correct and device pairing is no longer the blocker
- this is a narrow node-capability follow-up, not the default path for companion-app pairing failures

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes status
```

If the app says `bootstrap token invalid or expired`:

- old bootstrap payload
- refresh the bootstrap flow after any real route/auth fix that changes what the client must use

If the app says `unauthorized` without a more specific auth detail code:

- wrong token/password, wrong auth mode, or wrong Tailscale expectation
- for Tailscale Serve, `gateway.auth.allowTailscale` must match the intended flow
- otherwise use explicit token/password
- do not rewrite route settings until the active route is confirmed wrong

## Fix style

Reply with one concrete diagnosis and one route.

If there is not enough signal yet, ask for setup + exact app text instead of guessing.

Good:

- `The gateway is still local-only, so a node on another network can never reach it. Enable the route that matches your topology, verify the app is using that route, then approve the pending device pairing.`

Bad:

- `Maybe LAN, maybe Tailscale, maybe port forwarding, maybe public URL.`

## Hard stop & loop limit

- One fix, one verify only. Apply at most one targeted route or config fix. Re-check the relevant route selectors exactly once to verify.
- If the active route now matches the intended topology, stop network diagnosis. Tell the user to reconnect and approve if pairing is pending.
- If the route still does not match after one fix, stop and request the relevant config output (`gateway.bind`, `gateway.tailscale.mode`, `gateway.remote.url`, `plugins.entries.device-pair.config.publicUrl`) instead of attempting a second speculative fix.
- Do not attempt a second fix or iterate further.
- If the route matches and topology is confirmed, exit immediately. Do not run extra config checks.
