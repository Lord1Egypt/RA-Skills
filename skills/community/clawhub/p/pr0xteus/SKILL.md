---
name: pr0xteus
description: Give a trusted self-hosted workload configured WireGuard-backed SOCKS5 and HTTP exits through pr0xteus's bearer-protected private API. Request an operator-approved ISO country or logical pool, inspect leased-cell state, replace a failed assignment with excludeProxy, or integrate the Go client with VPN-only or public-first retry behavior. It uses operator-owned WireGuard bundles, Docker-spawned cells, country routing, fallback pools, and controller-fronted proxies. Use when a service needs controlled country-specific egress without exposing an open proxy or accepting caller-supplied Docker and provider configuration.
homepage: https://github.com/psyb0t/pr0xteus
user-invocable: true
metadata:
  openclaw:
    emoji: "🧬"
    primaryEnv: PR0XTEUS_URL
    requires:
      bins: [bash, curl, docker, jq]
permissions:
  network: "Runtime control-API calls go only to the user-configured PR0XTEUS_URL. Traffic sent through allocated SOCKS5 or HTTP URLs exits through operator-configured WireGuard infrastructure; use only trusted private control endpoints and operator-approved destination URLs. pkg/client's preflight check additionally makes direct, unproxied calls to api.ipify.org and ifconfig.me to confirm the exit IP actually changed. Setup time (references/setup.md) also reaches raw.githubusercontent.com for the installer and Docker Hub for the pinned image."
  shell: "bash, curl, jq, and explicit Docker commands from references/setup.md for user-requested setup or verification."
  filesystem: "Normal use reads PR0XTEUS_URL and PR0XTEUS_API_TOKEN from the environment. Operator setup writes only gitignored local WireGuard, pool, routing, token, and .env files."
---

# pr0xteus

pr0xteus is the not-an-open-proxy bit between a trusted service and
WireGuard-backed SOCKS5 and HTTP exits. The operator owns the local pool policy. Callers
can ask for an approved country or pool; they cannot smuggle Docker flags,
host paths, images, or arbitrary provider configs into the daemon.

For the actual setup, local config, a complete pool example, and proof that a
controller-fronted proxy exit works, read
[references/setup.md](references/setup.md) before touching the stack.

## Security and safety

- This skill is for an instance the user already runs and trusts. Do not hunt
  through the workspace for tokens, provider bundles, or Docker config. Take
  `PR0XTEUS_URL` and `PR0XTEUS_API_TOKEN` from the environment or ask.
- Allocating a proxy starts or reuses a configured WireGuard cell. It can spend
  provider capacity and sends later traffic through the operator's exit, so
  only request the country, pool, and task the user actually named.
- Returned `socks5://` and `http://` URLs are short-lived bearer capabilities
  for the controller's proxy gateways. Keep them out of logs, issue trackers,
  and public services. Trusted host and container clients can use either; only
  the controller talks to the selected cell's private address.
- pr0xteus has no MCP endpoint. This is a documentation skill, not a fake
  bridge plugin with invented tools.

## Use it for

- Giving a trusted workload configured country-specific SOCKS5 or HTTP egress.
- Checking whether the controller is alive or inspecting configured pools and
  their hot-tunnel state.
- Replacing a broken assignment while avoiding the same old cell.
- Inspecting live cells and their traffic (`/v1/cells`), or destroying one on
  demand. See [references/setup.md](references/setup.md#cells).
- Wiring a Go service through `pkg/client`, with VPN-only traffic by default or
  explicit public-first fallback where that makes sense.

## Do not use it for

- A public or anonymous proxy service.
- Provider-account provisioning, config scraping, or random WireGuard surgery
  outside the operator-owned pool policy.
- An untrusted caller, public proxy use case, or a destination the operator
  has not approved.

## Talk to a running controller

Set the private control URL and bearer token supplied by the operator:

```bash
export PR0XTEUS_URL=http://127.0.0.1:8000
export PR0XTEUS_API_TOKEN=replace-with-the-token-from-your-secret-store

auth_header=(--header @<(printf 'Authorization: Bearer %s' "$PR0XTEUS_API_TOKEN"))
```

Health lives on the separate metrics listener and deliberately has no token:

```bash
curl --fail --silent http://127.0.0.1:9091/healthz
```

Ask for the configured US route:

```bash
curl --fail-with-body --request POST \
  "${auth_header[@]}" \
  --header 'Content-Type: application/json' \
  --data '{"country":"US"}' \
  "$PR0XTEUS_URL/v1/proxies"
```

The response contains `proxies.socks5`, `proxies.http`, `pool`, `exitCountry`,
and `expiresAt`. Both URLs share one lease and work from the host or another
reachable trusted client. They authenticate to the controller, which forwards
to the chosen cell without resolving the destination itself. The setup
reference shows a direct `curl --proxy` proof.

Inspect active exits without creating another lease:

```bash
curl --fail-with-body "${auth_header[@]}" \
  "$PR0XTEUS_URL/v1/proxies?limit=100" | jq .
```

Every collection route (`/v1/proxies`, `/v1/pools`, and `/v1/cells`) accepts
`limit` and `offset` and returns its items plus `limit`, `offset`, and `total`.

Inspect the operator view:

```bash
curl --fail-with-body "${auth_header[@]}" "$PR0XTEUS_URL/v1/pools" | jq .
```

## Replace a bad assignment

There is no lease-release endpoint. pr0xteus records the assignment, finishes
the API request, then keeps a healthy cell warm until its idle policy reaps it.
If the workload cannot use an allocated proxy, request another one and exclude
the old URL:

```bash
curl --fail-with-body --request POST \
  "${auth_header[@]}" \
  --header 'Content-Type: application/json' \
  --data '{"country":"US","excludeProxy":"socks5://previous-lease-id:previous-secret@127.0.0.1:1080"}' \
  "$PR0XTEUS_URL/v1/proxies"
```

## Go client

The public [`pkg/client`](../../../pkg/client) package requests a proxy,
builds an HTTP client around it, and can preflight that the exit IP changes.
Keep the control token in the service's secret store and pass it with
`client.WithBearerToken`; the package doc comment contains the full shape.

Read [references/setup.md](references/setup.md) before changing local pool
policy or operating the persistent stack.
