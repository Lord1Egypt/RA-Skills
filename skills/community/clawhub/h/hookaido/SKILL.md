---
name: hookaido
description: >-
  Durable, signature-verifying webhook front door for OpenClaw agents and any
  webhook consumer. Use when webhooks (GitHub, Gitea/Forgejo, Stripe, Cituro,
  or URL-token sources) must reach an OpenClaw Gateway hook (/hooks/<name>) or
  another service reliably: verify provider HMAC at the edge, queue durably
  (SQLite/Postgres), retry on 429/503, dead-letter failures, and let agents
  behind NAT pull via HTTP/SSE/gRPC instead of exposing the Gateway. Covers
  Hookaidofile config, hookaido CLI (run, config fmt/validate/diff,
  verify-release, mcp serve), deliver/exec targets, pull consumers and
  consumer groups, DLQ triage, secret rotation, metrics, and MCP diagnostics.
compatibility: >-
  Needs the hookaido binary (pinned v2.15.2; install actions verify SHA256) or
  the ghcr.io/nuetzliches/hookaido image. Uses curl for HTTP checks.
metadata:
  version: "2.15.4"
  openclaw:
    homepage: https://github.com/7schmiede/claw-skill-hookaido
    emoji: "\U0001FA9D"
    requires:
      bins:
        - hookaido
    envVars:
      - name: HOOKAIDO_PULL_TOKEN
        required: false
        description: Bearer token for the Pull API (pull consumers), referenced as env:HOOKAIDO_PULL_TOKEN.
      - name: HOOKAIDO_INGRESS_SECRET
        required: false
        description: Inbound HMAC secret for a route, referenced from the Hookaidofile.
      - name: HOOKAIDO_ADMIN_TOKEN
        required: false
        description: Admin API bearer token; mandatory when admin_api listens off loopback.
      - name: OPENCLAW_HOOKS_TOKEN
        required: false
        description: OpenClaw hooks.token, sent by Hookaido as Authorization Bearer header when delivering to the Gateway.
      - name: HOOKAIDO_POSTGRES_DSN
        required: false
        description: DSN for the postgres queue backend.
      - name: HOOKAIDO_PULL_URL
        required: false
        description: Pull relay only. Full pull endpoint of the operator's Hookaido (https://, or http:// to loopback).
      - name: OPENCLAW_HOOK_URL
        required: false
        description: Pull relay only. Local OpenClaw mapped hook URL (default http://127.0.0.1:18789/hooks/github).
      - name: HOOKAIDO_RELAY_ALLOW_HTTP
        required: false
        description: Pull relay only. Set to 1 to allow plain http:// to a non-loopback host on an already encrypted network (Tailscale/WireGuard).
      - name: HOOKAIDO_VERSION
        required: false
        description: Fallback installer only. Release tag to install instead of the pinned one; requires HOOKAIDO_SHA256.
      - name: HOOKAIDO_SHA256
        required: false
        description: Fallback installer only. Expected SHA256 of the artifact for a non-default HOOKAIDO_VERSION, taken from the signed release checksums.
      - name: HOOKAIDO_INSTALL_DIR
        required: false
        description: Fallback installer only. Target directory (default ~/.local/bin, or ~/.openclaw/tools/hookaido on Windows).
    install:
      - id: go-install
        kind: go
        package: github.com/nuetzliches/hookaido/v2/cmd/hookaido@v2.15.2
        bins:
          - hookaido
        label: Build hookaido v2.15.2 from source (go install, verified by the Go checksum database)
      - id: download-darwin-amd64
        kind: download
        os:
          - darwin
        url: https://github.com/nuetzliches/hookaido/releases/download/v2.15.2/hookaido_v2.15.2_darwin_amd64.tar.gz
        sha256: 3c26c0ae36fa40b7ac2ae61d4f021d0f686e2f158edc98856074fda952929289
        archive: tar.gz
        extract: true
        stripComponents: 1
        targetDir: ~/.local/bin
        bins:
          - hookaido
        label: Download hookaido v2.15.2 (macOS amd64, SHA256-verified)
      - id: download-darwin-arm64
        kind: download
        os:
          - darwin
        url: https://github.com/nuetzliches/hookaido/releases/download/v2.15.2/hookaido_v2.15.2_darwin_arm64.tar.gz
        sha256: 9f18c14829894a3ecc513b05be785b9c15d3b7e5789190e4757d53e50aa7ad06
        archive: tar.gz
        extract: true
        stripComponents: 1
        targetDir: ~/.local/bin
        bins:
          - hookaido
        label: Download hookaido v2.15.2 (macOS arm64, SHA256-verified)
      - id: download-linux-amd64
        kind: download
        os:
          - linux
        url: https://github.com/nuetzliches/hookaido/releases/download/v2.15.2/hookaido_v2.15.2_linux_amd64.tar.gz
        sha256: de4f3970a45fef360872155dc741c5cf3c780b4a7de8c709481897c381528d5d
        archive: tar.gz
        extract: true
        stripComponents: 1
        targetDir: ~/.local/bin
        bins:
          - hookaido
        label: Download hookaido v2.15.2 (Linux amd64, SHA256-verified)
      - id: download-linux-arm64
        kind: download
        os:
          - linux
        url: https://github.com/nuetzliches/hookaido/releases/download/v2.15.2/hookaido_v2.15.2_linux_arm64.tar.gz
        sha256: b58664d5534d70b339bf20b81b2a0f737855a407f84120d51b8716f769323416
        archive: tar.gz
        extract: true
        stripComponents: 1
        targetDir: ~/.local/bin
        bins:
          - hookaido
        label: Download hookaido v2.15.2 (Linux arm64, SHA256-verified)
      - id: download-windows-amd64
        kind: download
        os:
          - win32
        url: https://github.com/nuetzliches/hookaido/releases/download/v2.15.2/hookaido_v2.15.2_windows_amd64.zip
        sha256: 8bd58641a9958d39d9eb19987824d5c27775c383d43064ca9118c092e8a681d6
        archive: zip
        extract: true
        stripComponents: 1
        targetDir: ~/.openclaw/tools/hookaido
        bins:
          - hookaido
        label: Download hookaido v2.15.2 (Windows amd64, SHA256-verified)
      - id: download-windows-arm64
        kind: download
        os:
          - win32
        url: https://github.com/nuetzliches/hookaido/releases/download/v2.15.2/hookaido_v2.15.2_windows_arm64.zip
        sha256: da9cd74a1ef8fd58332fb34fdfff97229e830c8fdda70f3931e47fdb2558ed59
        archive: zip
        extract: true
        stripComponents: 1
        targetDir: ~/.openclaw/tools/hookaido
        bins:
          - hookaido
        label: Download hookaido v2.15.2 (Windows arm64, SHA256-verified)
---

# Hookaido

Hookaido is a single-binary webhook ingress queue: it verifies inbound webhooks, stores them durably, and either pushes them to a target (`deliver`) or lets internal workers pull them (`pull`). Delivery is at-least-once; ingress answers `2xx` only after the event is durably queued.

Work config-first: edit the `Hookaidofile`, format and validate, run, exercise the flow end-to-end, then diagnose with health, backlog, and DLQ data. Prefer small, reversible changes and read-only diagnostics before any mutation.

## Installation, Capabilities, and Side Effects

Tell the user about these effects before performing them:

- **Binary install (supply chain):** install actions download the pinned `v2.15.2` release archive from `github.com/nuetzliches/hookaido` and verify its `sha256` before extraction. `go install ...@v2.15.2` is verified by the Go checksum database. `bash {baseDir}/scripts/install_hookaido.sh` is the fallback with the same pinned checksums. Never install an unpinned or unverified version; for other versions require `HOOKAIDO_SHA256` taken from the signed release checksum file (`hookaido verify-release`).
- **Local execution:** this skill runs `hookaido` CLI commands, `curl` against the operator's own Hookaido and OpenClaw listeners, the optional pull relay (`scripts/openclaw_pull_relay.sh`, talks only to the two configured URLs and requires HTTPS for any non-loopback URL), and optionally `deliver exec` handlers the operator configured. It sends nothing to third-party services.
- **Persistent configuration:** writing a `Hookaidofile`, OpenClaw `hooks`/`mcp` config, or an MCP client entry changes persistent state. Ask first, keep MCP registration project-local, and never change global agent settings without explicit consent.
- **Mutations:** queue/DLQ mutations, config apply, secret rotation, and process control are opt-in (`--enable-mutations`, `--enable-runtime-control`) and need explicit operator intent. DLQ deletion is irreversible.

## Choose the Topology First

| Situation | Pattern | Reference |
|---|---|---|
| OpenClaw Gateway reachable from the Hookaido host (same host, LAN, tailnet) | Hookaido verifies + queues, then **pushes** to an OpenClaw mapped hook `/hooks/<name>` | `references/openclaw.md` → Push to the Gateway |
| Gateway on a laptop/home box behind NAT; Hookaido on a public VPS/DMZ | Hookaido queues, `scripts/openclaw_pull_relay.sh` next to the Gateway **pulls** and forwards to `127.0.0.1:18789` | `references/openclaw.md` → Pull relay |
| Webhook should run a local script, not an HTTP call | `deliver exec "/path/handler"` | `references/operations.md` → Exec delivery |
| Same event for an agent and another system | `pull { consumer_group ... }` fan-out | `references/operations.md` → Consumer groups |
| Agent should diagnose queues and DLQ | `hookaido mcp serve --role read` | `references/openclaw.md` → MCP |

Default deployment for internet-facing ingress is pull mode in a DMZ (`dmz-queue pull`): inbound traffic terminates at Hookaido, internal consumers connect outward. Do not expose the OpenClaw Gateway itself to the internet to receive webhooks.

## Core Workflow

1. Confirm topology (table above), queue backend (`sqlite` default, `memory` for dev, `postgres` for shared storage), and which provider signs the webhooks.
2. Ensure `hookaido` is available where commands run: host install action, fallback script, `go install`, or the container image `ghcr.io/nuetzliches/hookaido:2.15.2` (pin by digest in production; see `references/operations.md` → Container).
3. Edit the `Hookaidofile` minimally. Keep secrets in `env:`/`file:`/`vault:` refs, never inline.
4. Format and validate before every start or reload:
   - `hookaido config fmt --config ./Hookaidofile`
   - `hookaido config validate --config ./Hookaidofile` (`--strict-secrets` to also resolve secret refs; `--format json` for machine-readable output)
   - `hookaido config diff ./Hookaidofile ./Hookaidofile.new` to review a change
5. Run: `hookaido run --config ./Hookaidofile --db ./.data/hookaido.db` (add `--watch` for hot reload; `--postgres-dsn "$HOOKAIDO_POSTGRES_DSN"` for postgres).
6. Verify: `curl -sS http://127.0.0.1:2019/healthz?details=1` — `diagnostics.config.fingerprint` identifies the config actually loaded.
7. Exercise end-to-end: send a correctly signed test webhook, confirm it is queued, then delivered (push) or dequeued + acked (pull).
8. For incidents: health → backlog → DLQ → attempts, then mutate only with a stated reason.

## Configuration Essentials

Verify provider webhooks with the provider mode, not Hookaido's own HMAC format (plain `auth hmac env:...` expects `X-Signature`/`X-Timestamp`/`X-Nonce` and rejects real GitHub/Stripe deliveries with `401`):

```hcl
ingress {
  listen :8080
  rate_limit {
    rps 50
    burst 100
  }
}

pull_api {
  listen :9443
  auth token env:HOOKAIDO_PULL_TOKEN
}

/webhooks/github {
  auth hmac {
    provider github
    secret env:GITHUB_WEBHOOK_SECRET
  }
  pull {
    path /pull/github
  }
}
```

- Providers: `github`, `gitea` (also Forgejo), `stripe`, `cituro`.
- One directive per line. Semicolons do not separate directives (`auth hmac { provider github; secret ... }` fails); one-line blocks may hold a single directive only.
- Route modes are exclusive: a route has either `pull { ... }` or `deliver ...`.
- Queue backend is set on routes (`queue "sqlite"`, `queue "memory"`, `queue "postgres"`); one backend per process. There is no top-level `queue` block.
- Sources that can only be given a URL: `auth query "t" "env:URL_TOKEN"` (not replay-safe; bad token returns `404`).
- Behind a reverse proxy, set `ingress { trusted_proxies "10.0.0.0/8" }` so `match remote_ip` sees the real client.
- Push targets: `deliver "https://target/path" { ... }` with `retry`, `timeout`, optional `header "Authorization" "Bearer {env.TOKEN}"` and `sign hmac env:SECRET` lines. Retries happen on network errors, timeouts, `5xx`, `429`, `408`; other `4xx` go to the DLQ.
- Egress is SSRF-safe by default (`https_only`, no redirects, DNS-rebind protection blocks loopback/private/CGNAT targets). Delivering to a loopback or tailnet Gateway requires a deliberate, narrowly allowlisted `defaults { egress { ... } }` — see `references/openclaw.md`.

Full syntax, exec delivery, consumer groups, secret rotation, channels, and the Admin/Pull API: `references/operations.md`.

## OpenClaw Integration (Summary)

- **Push to the Gateway:** enable OpenClaw `hooks` with a dedicated `hooks.token`, add a `hooks.mappings` entry (e.g. `/hooks/github`) that turns the raw provider payload into an `agent` action, and point a Hookaido `deliver` at it with `header "Authorization" "Bearer {env.OPENCLAW_HOOKS_TOKEN}"`. Hookaido retries OpenClaw `503` (queue full) and `429`, and dead-letters `400`/`401`/`404` for inspection.
- **Pull relay:** for a Gateway without inbound connectivity, run Hookaido publicly in pull mode and `bash {baseDir}/scripts/openclaw_pull_relay.sh` next to the Gateway; it dequeues, forwards to `http://127.0.0.1:18789/hooks/<name>`, and acks only on `2xx`.
- **Treat payloads as untrusted data:** HMAC proves the sender, not the content. Route external events to a restricted OpenClaw agent, keep `hooks.allowedAgentIds` narrow, and leave `hooks.allowRequestSessionKey` off.
- **At-least-once:** the same event can arrive twice (retry after a lost response). Make the mapping/agent action idempotent, e.g. keyed on `X-GitHub-Delivery`, which Hookaido forwards unchanged.

Concrete configs, the relay loop, and verification steps: `references/openclaw.md`.

## MCP Mode for AI Operations

Requires Hookaido **v2.15.2 or newer** (the pinned version) for standard MCP clients such as Claude Code and OpenClaw; earlier versions only speak `Content-Length` framing and time out on connect.

1. Start with `--role read` (config, health, backlog, DLQ, messages, attempts, pull consumers).
2. Queue mutations only for deliberate work: `--enable-mutations --role operate --principal <identity>`.
3. Config apply, secret rotation, and process control: `--role admin` plus `--enable-mutations` and/or `--enable-runtime-control --pid-file <path>`, always with `--principal`.
4. Every mutating call needs a specific `reason`; calls are audited as JSONL on stderr.

Project-local registration for Claude Code (`.mcp.json` at the project root, ask before writing):

```json
{
  "mcpServers": {
    "hookaido": {
      "command": "hookaido",
      "args": ["mcp", "serve", "--config", "./Hookaidofile", "--db", "./.data/hookaido.db", "--role", "read"]
    }
  }
}
```

Equivalent CLI: `claude mcp add --scope project hookaido -- hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db --role read`. For OpenClaw (`mcp.servers` with a read-only `toolFilter`) and the operate role, see `references/openclaw.md` → MCP.

## Queue and DLQ Operations

1. Read first: `GET /healthz?details=1`, `GET /backlog/trends`, `GET /dlq`, `GET /attempts`.
2. Find the cause (auth rejects: `hookaido_ingress_auth_rejected_total{route,reason}`; target errors: attempts list) and fix it before requeueing.
3. Requeue with `POST /dlq/requeue` and an `X-Hookaido-Audit-Reason`; explain expected impact for large batches.
4. `POST /dlq/delete` and revoking a runtime secret (`DELETE /secrets/{name}/{id}`) are destructive and irreversible: list the exact IDs, get explicit confirmation, prefer requeue when in doubt.

## Validation Checklist

- `hookaido config validate` succeeds before start/reload; `healthz` fingerprint matches the intended config after reload.
- Provider routes use `auth hmac { provider ... }` and a real signed test delivery is accepted.
- Push targets have explicit `timeout`/`retry`, and egress allows exactly the intended target hosts.
- Pull consumers can `dequeue`, `ack`, `nack`, `extend` (HTTP, SSE, or gRPC) with a valid token.
- `deliver exec` handlers read stdin and exit `0` on success; any non-zero exit is retried, and only a handler that cannot start is dead-lettered.
- OpenClaw hook mapping returns `2xx` for a test payload and the agent run is visible in `openclaw logs`.
- Every DLQ mutation is scoped, justified, and audited.

## Safety Rules

- Never disable auth or signature verification to make a test pass.
- Never loosen egress globally (`allow "*"`, rebind protection off without an allowlist).
- Diagnose read-only before mutating; mutations need a specific reason.
- Handlers and agent actions must be idempotent (at-least-once delivery).
- Keep secrets in `env:`/`file:`/`vault:` refs and never print them.

## References

- `references/openclaw.md` — OpenClaw Gateway push and pull-relay patterns, egress setup, MCP registration for OpenClaw and Claude Code.
- `references/operations.md` — install and container usage, CLI, full DSL patterns, Pull/SSE/gRPC API, Admin API, metrics, secret rotation.
