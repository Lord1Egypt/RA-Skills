# Hookaido Operations Reference

Use this file for concrete command syntax and request payloads.

## Install Hookaido

OpenClaw supports two runtime variants.

Public repositories:

- Upstream project: `https://github.com/nuetzliches/hookaido`
- Public skill repo: `https://github.com/7schmiede/claw-skill-hookaido`

### Variant A: Host Binary (Gateway/Host)

- Use one of the skill installer actions from `metadata.openclaw.install` (platform + architecture specific download).
- Choose the artifact that matches your host architecture (`amd64` or `arm64`).
- The OpenClaw download URLs are pinned to Hookaido `v2.6.0`.
- macOS/Linux installers extract to `~/.local/bin` (with `stripComponents: 1`).
- Windows installers extract to `~/.openclaw/tools/hookaido`.

Direct CLI fallback:

```bash
go install github.com/nuetzliches/hookaido/cmd/hookaido@v2.6.0
```

Release-binary fallback from this skill folder:

```bash
bash {baseDir}/scripts/install_hookaido.sh
```

The fallback installer is hardened:

- Defaults to pinned `v2.6.0` (no dynamic `latest` lookup).
- Verifies SHA256 of the downloaded release artifact before extraction/install.

Optional pins/overrides for the installer script:

```bash
# Default pinned install, custom location
HOOKAIDO_INSTALL_DIR="$HOME/bin" bash {baseDir}/scripts/install_hookaido.sh

# Non-default release requires explicit checksum
HOOKAIDO_VERSION=v2.0.1 \
HOOKAIDO_SHA256="<artifact-sha256>" \
bash {baseDir}/scripts/install_hookaido.sh
```

### Variant B: Docker Sandbox

- OpenClaw supports Docker sandbox mode via `sandboxing.enabled: true` and `sandboxing.type: docker`.
- Preferred: provide a custom sandbox image with `hookaido` preinstalled, and pin the image by immutable digest.
- Optional: use `agents.defaults.sandbox.docker.setupCommand` to install `hookaido` inside the container at startup.
- Keep `metadata.openclaw.install` as fallback and for `metadata.openclaw.requires.bins` checks on the host.

## Core CLI Commands

```bash
# Validate and format config
hookaido config fmt --config ./Hookaidofile
hookaido config validate --config ./Hookaidofile
hookaido config validate --config ./Hookaidofile --strict-secrets

# Start runtime
hookaido run --config ./Hookaidofile --db ./.data/hookaido.db

# Start runtime with Postgres queue backend
hookaido run --config ./Hookaidofile --postgres-dsn "$HOOKAIDO_POSTGRES_DSN"

# Start runtime with live config watch
hookaido run --config ./Hookaidofile --db ./.data/hookaido.db --watch

# Start MCP server (read-only)
hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db --role read

# Verify a public release bundle before rollout
hookaido verify-release \
  --checksums ./hookaido_v2.6.0_checksums.txt \
  --public-key ./hookaido_v2.6.0_checksums.txt.pub.pem \
  --require-provenance
```

## Minimal Pull-Mode Config

```hcl
ingress {
  listen :8080
}

pull_api {
  listen :9443
  auth token env:HOOKAIDO_PULL_TOKEN
}

/webhooks/github {
  auth hmac env:HOOKAIDO_INGRESS_SECRET
  pull { path /pull/github }
}
```

## Exec Delivery Config (v2.2.0+)

```hcl
/webhooks/github {
  auth hmac {
    provider github
    secret env:GITHUB_WEBHOOK_SECRET
  }
  deliver exec "/opt/hooks/deploy.sh" {
    timeout 30s
    retry exponential max 3 base 1s cap 30s jitter 0.2
    env DEPLOY_ENV production
  }
}
```

Exit codes: `0` = ack, `75`/`1-125` = retry, `126`/`127` = immediate DLQ.
Metadata env vars: `HOOKAIDO_ROUTE`, `HOOKAIDO_EVENT_ID`, `HOOKAIDO_CONTENT_TYPE`, `HOOKAIDO_ATTEMPT`, `HOOKAIDO_HEADER_*`.

## Provider-Compatible HMAC Config (v2.2.0+)

```hcl
# GitHub
/webhooks/github {
  auth hmac {
    provider github
    secret env:GITHUB_WEBHOOK_SECRET
  }
  pull { path /pull/github }
}

# Gitea / Forgejo
/webhooks/gitea {
  auth hmac {
    provider gitea
    secret env:GITEA_WEBHOOK_SECRET
  }
  pull { path /pull/gitea }
}

# Stripe (v2.6.0+)
/webhooks/stripe {
  auth hmac {
    provider stripe
    secret env:STRIPE_SIGNING_SECRET
  }
  pull { path /pull/stripe }
}

# Cituro (v2.6.0+)
/webhooks/cituro {
  auth hmac {
    provider cituro
    secret env:CITURO_WEBHOOK_SECRET
  }
  pull { path /pull/cituro }
}
```

## Pull API Calls

Assume base URL `http://localhost:9443/pull/github` and token in `HOOKAIDO_PULL_TOKEN`.

```bash
# Dequeue
curl -sS -X POST "http://localhost:9443/pull/github/dequeue" \
  -H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"batch":10,"lease_ttl":"30s","max_wait":"5s"}'

# Ack
curl -sS -X POST "http://localhost:9443/pull/github/ack" \
  -H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lease_id":"lease_xyz"}'

# Batch ack (v2.2.0+)
curl -sS -X POST "http://localhost:9443/pull/github/ack" \
  -H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lease_ids":["lease_a","lease_b"]}'

# Nack (requeue with delay)
curl -sS -X POST "http://localhost:9443/pull/github/nack" \
  -H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lease_id":"lease_xyz","delay":"5s","dead":false}'

# Extend lease
curl -sS -X POST "http://localhost:9443/pull/github/extend" \
  -H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lease_id":"lease_xyz","lease_ttl":"30s"}'

# Batch nack (v2.2.0+)
curl -sS -X POST "http://localhost:9443/pull/github/nack" \
  -H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lease_ids":["lease_a","lease_b"],"delay":"5s","dead":false}'
```

## Optional gRPC Pull-Worker Mode (`v1.4.0+`)

Enable gRPC pull-worker transport alongside HTTP pull:

```hcl
pull_api {
  listen :9443
  grpc_listen :9943
  auth token env:HOOKAIDO_PULL_TOKEN
}

/webhooks/github {
  pull { path /pull/github }
}
```

Use gRPC workers with the same lease semantics and operation parity as Pull HTTP:

- `Dequeue` -> `POST {endpoint}/dequeue`
- `Ack` -> `POST {endpoint}/ack`
- `Nack` -> `POST {endpoint}/nack`
- `Extend` -> `POST {endpoint}/extend`

Notes:

- Worker gRPC reuses pull token auth and pull endpoint routing.
- Keep `grpc_listen` on a dedicated internal listener; do not share ingress/pull/admin/metrics ports.
- Worker lease operations are intentionally outside MCP scope.

## Queue Backend Modes

```hcl
# Default durable mode
queue sqlite

# Ephemeral development/testing mode
queue memory

# Shared database mode (v2.2.0+)
queue postgres
```

Postgres runtime wiring:

```bash
export HOOKAIDO_POSTGRES_DSN='postgres://user:pass@db.internal/hookaido?sslmode=require'
hookaido run --config ./Hookaidofile --postgres-dsn "$HOOKAIDO_POSTGRES_DSN"
```

## Admin API Reads

```bash
# Health summary
curl -sS "http://127.0.0.1:2019/healthz"

# Detailed diagnostics
curl -sS "http://127.0.0.1:2019/healthz?details=1"

# Backlog trends
curl -sS "http://127.0.0.1:2019/backlog/trends?window=1h&step=5m"

# Dead-letter queue
curl -sS "http://127.0.0.1:2019/dlq?limit=50"
```

## Admin API Mutations

Use `X-Hookaido-Audit-Reason` and keep reasons actionable.

```bash
# Requeue DLQ items
curl -sS -X POST "http://127.0.0.1:2019/dlq/requeue" \
  -H "Content-Type: application/json" \
  -H "X-Hookaido-Audit-Reason: retry-after-fix" \
  -d '{"ids":["evt_1","evt_2"]}'

# Delete DLQ items
curl -sS -X POST "http://127.0.0.1:2019/dlq/delete" \
  -H "Content-Type: application/json" \
  -H "X-Hookaido-Audit-Reason: remove-invalid-payloads" \
  -d '{"ids":["evt_3"]}'
```

## SSE Streaming (v2.5.3+)

Connect a persistent SSE stream instead of polling dequeue:

```bash
# Stream events in real time (persistent connection, server pushes)
curl -sS -N "http://localhost:9443/pull/github/stream" \
  -H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN"

# ACK a streamed event (same endpoint as pull)
curl -sS -X POST "http://localhost:9443/pull/github/ack" \
  -H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lease_id":"lease_xyz"}'
```

Notes:
- Multiple concurrent SSE connections act as competing consumers.
- ACK/NACK/extend operations use the same POST endpoints as pull mode.
- Prometheus metrics are emitted per route.

## MCP Role Patterns

```bash
# Read-only diagnostics
hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db --role read

# Queue mutation workflows
hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db \
  --enable-mutations --role operate --principal ops@example.test

# Full admin control (includes runtime operations)
hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db \
  --enable-mutations --enable-runtime-control --role admin \
  --principal ops@example.test --pid-file ./hookaido.pid
```

## Claude Code MCP Plugin Config

Register Hookaido as a Claude Code MCP plugin in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "hookaido": {
      "command": "hookaido",
      "args": [
        "mcp", "serve",
        "--config", "./Hookaidofile",
        "--db", "./.data/hookaido.db",
        "--role", "read"
      ]
    }
  }
}
```

For operate role (queue mutations enabled):

```json
{
  "mcpServers": {
    "hookaido": {
      "command": "hookaido",
      "args": [
        "mcp", "serve",
        "--config", "./Hookaidofile",
        "--db", "./.data/hookaido.db",
        "--enable-mutations",
        "--role", "operate",
        "--principal", "claude"
      ]
    }
  }
}
```

Use `~/.claude/settings.json` for global registration across all projects.
