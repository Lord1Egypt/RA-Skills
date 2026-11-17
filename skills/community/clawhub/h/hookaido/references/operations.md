# Hookaido Operations Reference (v2.15.2)

Concrete syntax for install, CLI, DSL, and APIs. Every config snippet below passes `hookaido config validate` and is in `hookaido config fmt` order. The DSL takes one directive per line: `{ a; b }` does not parse, and a one-line block may hold only a single directive (`pull { path /pull/x }`). Snippets with `pull` routes also need a `pull_api { auth token ... }` block.

Public repositories:

- Upstream project: `https://github.com/nuetzliches/hookaido`
- Skill repository: `https://github.com/7schmiede/claw-skill-hookaido`

## Install

### Host binary

- OpenClaw install actions (`metadata.openclaw.install`) download the pinned `v2.15.2` archive for the platform and verify its `sha256` before extraction.
  - macOS/Linux extract to `~/.local/bin`.
  - Windows extracts to `~/.openclaw/tools/hookaido`.
  - Archives contain one top-level folder; `stripComponents: 1` removes it.
- From source (verified by the Go checksum database; the module path has had a `/v2` suffix since v2.8.0):

  ```bash
  go install github.com/nuetzliches/hookaido/v2/cmd/hookaido@v2.15.2
  ```

- Fallback installer with pinned checksums:

  ```bash
  bash {baseDir}/scripts/install_hookaido.sh
  HOOKAIDO_INSTALL_DIR="$HOME/bin" bash {baseDir}/scripts/install_hookaido.sh
  # Any other version requires an explicit checksum from the signed release file:
  HOOKAIDO_VERSION=v2.15.0 HOOKAIDO_SHA256="<artifact-sha256>" bash {baseDir}/scripts/install_hookaido.sh
  ```

### Verify a release bundle

Download the release assets for one version into a directory, then:

```bash
hookaido verify-release \
  --checksums ./hookaido_v2.15.2_checksums.txt \
  --public-key ./hookaido_v2.15.2_checksums.txt.pub.pem \
  --signature ./hookaido_v2.15.2_checksums.txt.sig \
  --require-signature --require-provenance
```

This checks:

- the artifact checksums
- the ed25519 signature on the checksum file
- the SBOM
- the provenance attestations

`--json` gives machine-readable output.

### Container

Image: `ghcr.io/nuetzliches/hookaido`. Tags are `X.Y.Z` (no `v` prefix), `X.Y`, `X`, and `latest`. Images are published for linux/amd64 and linux/arm64. In production, pin by digest:

```bash
docker run -d --name hookaido \
  -p 8080:8080 -p 9443:9443 \
  -e HOOKAIDO_PULL_TOKEN -e GITHUB_WEBHOOK_SECRET \
  -v "$PWD/config:/app/config:ro" -v hookaido-data:/app/.data \
  ghcr.io/nuetzliches/hookaido:2.15.2@sha256:b62e6e23227007d209d63c4234cf150a5bb91074cdede9e6cc4a8638194a1aa0 \
  run --config /app/config/Hookaidofile --db /app/.data/hookaido.db --watch
```

- Default command: `run --config /app/Hookaidofile --db /app/.data/hookaido.db`. `/app/.data` is a volume. The process runs as UID 1000.
- Mount the config directory, not a single file, when using `--watch`. A single-file bind mount never fires the watcher; use `--watch-interval 30s` as a polling fallback.
- The admin API is loopback-only by default. To reach it from outside the container, give `admin_api` the directives `listen :2019` and `auth token env:HOOKAIDO_ADMIN_TOKEN` (one per line); a token is mandatory off loopback.
- OpenClaw Docker sandbox: build a sandbox image that copies the binary from the pinned image instead of downloading at runtime:

  ```dockerfile
  COPY --from=ghcr.io/nuetzliches/hookaido:2.15.2@sha256:b62e6e23227007d209d63c4234cf150a5bb91074cdede9e6cc4a8638194a1aa0 \
       /usr/local/bin/hookaido /usr/local/bin/hookaido
  ```

  `requires.bins` is checked on the host, so the host also needs `hookaido`, or the install action.

## CLI

```bash
hookaido config fmt --config ./Hookaidofile                  # canonical formatting (round-trip stable)
hookaido config validate --config ./Hookaidofile             # --strict-secrets resolves secret refs; --format json|text
hookaido config diff --context 3 ./Hookaidofile ./Hookaidofile.new

hookaido run --config ./Hookaidofile --db ./.data/hookaido.db
hookaido run --config ./Hookaidofile --db ./.data/hookaido.db --watch          # hot reload; SIGHUP also reloads
hookaido run --config ./Hookaidofile --postgres-dsn "$HOOKAIDO_POSTGRES_DSN"   # postgres backend
hookaido run --config ./Hookaidofile --dotenv ./hookaido.env --log-level info   # KEY=VALUE file for env: refs

hookaido version --long
hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db --role read
```

Hot reload applies routes, auth, matchers, deliver targets, headers and egress. Listener addresses, TLS, API prefixes, pull limits, the queue backend, retention and observability need a restart. After a reload, confirm `diagnostics.config.fingerprint` in `GET /healthz?details=1`.

## Defaults

| Setting | Default |
|---|---|
| Listeners | ingress `:8080`, pull API `:9443`, admin API `127.0.0.1:2019` (no prefixes) |
| `max_body` / `max_headers` | `2mb` / `64kb` |
| `queue_limits` | `max_depth 10000`, `drop_policy "reject"` |
| `deliver` | `retry exponential max 8 base 2s cap 2m jitter 0.2`, `timeout 10s`, `concurrency 20` |
| Egress | `https_only on`, `redirects off`, `dns_rebind_protection on` |
| Retention | queue `7d`, DLQ `30d`/`10000`, attempts `7d`/`200000` rows |
| Pull API | `max_batch 100`, `max_lease_batch 100`, `default_lease_ttl 30s` |

## Ingress Authentication

Provider-compatible HMAC (no timestamp/nonce replay check; providers do not send those headers):

```hcl
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

- `provider` is one of `github`, `gitea` (also Forgejo), `stripe`, `cituro`.
- `signature_header`, `timestamp_header`, `nonce_header` and `tolerance` are rejected in provider mode.

Other variants:

- `auth hmac env:SECRET`: Hookaido's own format (`X-Signature`/`X-Timestamp`/`X-Nonce`, with replay protection). Use it only for senders you control, never for GitHub or Stripe.
- `auth query "t" "env:URL_TOKEN"`: for sources that can only be given a URL. It is not replay-safe, a bad token returns `404`, and it cannot be combined with other auth. Repeat the line to rotate with overlap.
- `auth basic "user" "{env.PASS}"`: use the placeholder form; `env:` is rejected here.
- `auth forward "https://auth.internal/check" { timeout 2s }`: `2xx` allows, `401`/`403` deny, anything else fails closed with `503`.

Filtering and protection:

```hcl
ingress {
  listen :8080
  rate_limit {
    rps 50
    burst 100
  }
  trusted_proxies "10.0.0.0/8"
}

/webhooks/github {
  match {
    remote_ip "140.82.112.0/20"
  }
  auth hmac {
    provider github
    secret env:GITHUB_WEBHOOK_SECRET
  }
  pull {
    path /pull/github
  }
}
```

- `match` also supports `method`, `host`, `header "N" "V"`, `header_exists`, `query`, `query_exists`, and named matchers (`@name { ... }` plus `match @name`).
- Without `trusted_proxies`, `X-Forwarded-For` is ignored.
- Requests over the rate limit get `429`.

## Secret Rotation

Static versions: a `secrets { secret "S1" { ... } }` block with `value env:X`, `valid_from "..."` and `valid_until "..."` on separate lines, referenced as `auth hmac secret_ref "S1"`.

Runtime-mutable pools are for providers that roll secrets via API, such as Cituro:

```hcl
secrets {
  secret "cituro" {
    runtime true
    max_versions 16
  }
}

/webhooks/cituro {
  auth hmac {
    provider cituro
    secret_ref "cituro"
  }
  pull {
    path /pull/cituro
  }
}
```

- Requires `HOOKAIDO_SECRET_ENCRYPTION_KEY` (32 bytes, base64). Back the key up separately from the database.
- Add a version with `POST /secrets/cituro` and `{"value":"...","not_before":"...","not_after":"..."}`. The response is `201` with an id `sec_...`.
- List with `GET /secrets/cituro` (metadata only). Revoke with `DELETE /secrets/cituro/{id}`.
- Revoking is immediate and cannot be undone. List the pool first and never revoke the last version that is valid now: an empty pool rejects every webhook on the route with `401` until the provider's next secret is added. Name the exact id and get explicit operator confirmation before revoking.
- MCP: `rotate_secret` (admin role plus `--enable-mutations`).
- Never echo secret values in logs or chat.
- Watch `hookaido_runtime_secret_pool_versions` and `hookaido_runtime_secret_pool_exhaustion_seconds`. An empty pool rejects every webhook with `401`.

## Delivery

Push with custom headers and outbound signing:

```hcl
/webhooks/stripe {
  auth hmac {
    provider stripe
    secret env:STRIPE_SIGNING_SECRET
  }
  deliver "https://billing.internal.example.com/stripe" {
    timeout 10s
    sign hmac env:BILLING_SIGNING_SECRET
  }
}
```

- `header "Authorization" "Bearer {env.TOKEN}"` adds a static or placeholder header. Placeholders are `{env.X}`, `{file.PATH}` and `{vars.NAME}`, resolved at startup/reload. Headers are set before signing.
- `sign hmac` writes `X-Hookaido-Timestamp` and `X-Hookaido-Signature`. The signature is `hex(HMAC-SHA256(secret, METHOD\nPATH\nUNIX_TS\nsha256hex(body)))`.
- Retries happen on network errors, timeouts, `5xx`, `429` and `408`. Other `4xx` go to the DLQ.
- The target must pass the egress policy (`allow`/`deny` lines in `defaults { egress { ... } }`).

### Exec delivery

```hcl
/webhooks/forgejo {
  auth hmac {
    provider gitea
    secret env:FORGEJO_WEBHOOK_SECRET
  }
  deliver exec "/opt/hooks/deploy.sh" {
    retry exponential max 3 base 1s cap 30s jitter 0.2
    timeout 30s
    env DEPLOY_ENV production
  }
}
```

- The payload arrives on stdin.
- Environment: only `PATH`, `HOOKAIDO_ROUTE`, `HOOKAIDO_EVENT_ID`, `HOOKAIDO_CONTENT_TYPE`, `HOOKAIDO_ATTEMPT`, `HOOKAIDO_HEADER_*`, and the configured `env` entries. The host environment is not inherited.
- Exit `0` acks. Every non-zero exit, `126`/`127` included, is retried, as are a signal kill and a timeout.
- Only a handler that cannot start (missing, not executable) is dead-lettered immediately.
- `sign` is not allowed with exec.

### Channels

```hcl
outbound /jobs/notify {
  deliver "https://notify.internal.example.com/hook" {
    timeout 10s
  }
}

internal /jobs/report {
  pull {
    path /pull/reports
  }
}
```

- `outbound` routes receive no ingress traffic; feed them via `POST /messages/publish`.
- `internal` routes are pull-only work queues.

## Queue Backends

The backend is set per route and must be the same on every route in a process. There is no top-level `queue` block.

```hcl
/webhooks/stripe {
  auth hmac {
    provider stripe
    secret env:STRIPE_SIGNING_SECRET
  }
  queue "postgres"
  pull {
    path /pull/stripe
  }
}
```

- `queue "sqlite"` is the default: durable, with WAL.
- `queue "memory"` is for dev/tests only; data is lost on restart.
- `queue "postgres"` needs `--postgres-dsn` or `HOOKAIDO_POSTGRES_DSN`.

Example DSN setup:

```bash
export HOOKAIDO_POSTGRES_DSN='postgres://user:pass@db.internal/hookaido?sslmode=require'
```

## Pull API

The full endpoint is `pull_api.prefix` + `pull.path` + operation. The default prefix is empty: `http://localhost:9443/pull/github/dequeue`.

```bash
H=(-H "Authorization: Bearer $HOOKAIDO_PULL_TOKEN" -H "Content-Type: application/json")
B=http://localhost:9443/pull/github

curl -sS -X POST "$B/dequeue" "${H[@]}" -d '{"batch":10,"lease_ttl":"30s","max_wait":"10s"}'
# -> {"items":[{"id","lease_id","route","target","payload_b64","headers","received_at","attempt"}]}  (empty items = nothing queued)

curl -sS -X POST "$B/ack"    "${H[@]}" -d '{"lease_id":"lease_xyz"}'                 # or {"lease_ids":[...]}
curl -sS -X POST "$B/nack"   "${H[@]}" -d '{"lease_id":"lease_xyz","delay":"30s"}'   # retry later
curl -sS -X POST "$B/nack"   "${H[@]}" -d '{"lease_id":"lease_xyz","dead":true,"reason":"bad_payload"}'  # to DLQ
curl -sS -X POST "$B/extend" "${H[@]}" -d '{"lease_id":"lease_xyz","lease_ttl":"30s"}'
```

- An expired lease is requeued automatically.
- Repeated `ack`/`nack` of a completed lease is idempotent.
- `max_lease_batch` (default `100`) caps the lease IDs per call.
- Header names in `headers` are in canonical form (`X-Github-Event`), so look them up case-insensitively.

### SSE streaming

`GET $B/stream` with the same bearer token pushes events as `data: {...}` lines with the same item shape. Ack, nack and extend use the POST endpoints.

- Tune it in the global `pull_api` block: `sse_keepalive 15s` and `sse_max_connection <duration>` (default off).
- Keepalives exist for proxies. A consumer must reconnect when the stream drops, and should treat a long silence beyond the keepalive interval as a dead stream.
- Several SSE connections on one route are competing consumers.

### Consumer groups (fan-out)

```hcl
pull_api {
  listen :9443
  sse_keepalive 15s
  auth token env:HOOKAIDO_PULL_TOKEN
}

/webhooks/github {
  auth hmac {
    provider github
    secret env:GITHUB_WEBHOOK_SECRET
  }
  pull {
    path /pull/github
    consumer_group "openclaw"
    consumer_group "ci"
  }
}
```

- Each group gets its own copy of every event at `.../pull/github/<group>/{dequeue,ack,nack,extend,stream}`. The bare path returns `404`.
- Admin publish to a grouped route needs `target "pull:<group>"`.

### gRPC workers

- Enable with `pull_api { grpc_listen :9943 }`, on its own dedicated listener.
- It uses the same token, routing and lease semantics (`Dequeue`, `Ack`, `Nack`, `Extend`).
- Worker gRPC is lease transport only; it is not an admin surface and is outside MCP scope.

### Single-port deployment

Ingress, the pull API and the admin API can share one port with non-overlapping prefixes:

```hcl
ingress {
  listen :8080
}

pull_api {
  listen :8080
  prefix /pull
  auth token env:HOOKAIDO_PULL_TOKEN
}

admin_api {
  listen :8080
  prefix /admin
  auth token env:HOOKAIDO_ADMIN_TOKEN
}

/webhooks/github {
  auth hmac {
    provider github
    secret env:GITHUB_WEBHOOK_SECRET
  }
  pull {
    path /github
  }
}
```

- TLS must be identical on every shared listener.
- `grpc_listen` and the metrics listener stay separate.
- Pull endpoints then live under `/pull/github/...` and admin endpoints under `/admin/...`.

## Admin API

The default base is `http://127.0.0.1:2019`, with no prefix. If `admin_api auth token` is set, send `Authorization: Bearer $HOOKAIDO_ADMIN_TOKEN`; bare `GET /healthz` stays open for liveness probes.

Reads:

```bash
curl -sS "http://127.0.0.1:2019/healthz?details=1"            # includes diagnostics.config.{fingerprint,generation,loaded_at}
curl -sS "http://127.0.0.1:2019/backlog/trends?window=1h&step=5m"
curl -sS "http://127.0.0.1:2019/backlog/top_queued"
curl -sS "http://127.0.0.1:2019/dlq?limit=50"
curl -sS "http://127.0.0.1:2019/attempts?limit=50"
curl -sS "http://127.0.0.1:2019/messages?limit=50"
curl -sS "http://127.0.0.1:2019/pull/consumers?route=/webhooks/github"   # live SSE consumers
```

Mutations always carry an `X-Hookaido-Audit-Reason`:

```bash
# Requeue DLQ items after fixing the cause
curl -sS -X POST "http://127.0.0.1:2019/dlq/requeue" \
  -H "Content-Type: application/json" \
  -H "X-Hookaido-Audit-Reason: retry-after-token-fix" \
  -d '{"ids":["evt_1","evt_2"]}'

# Delete DLQ items -- DESTRUCTIVE and IRREVERSIBLE.
# Inspect them first (GET /dlq), list the exact IDs, and get explicit
# operator confirmation. Prefer requeue when in doubt.
curl -sS -X POST "http://127.0.0.1:2019/dlq/delete" \
  -H "Content-Type: application/json" \
  -H "X-Hookaido-Audit-Reason: remove-invalid-payloads" \
  -d '{"ids":["evt_3"]}'
```

Other mutation endpoints:

- `POST /messages/publish` with `{"items":[{"id","route","target"?,"payload_b64","headers"?}]}`.
- `POST /messages/{cancel,requeue,resume}`, plus `_by_filter` variants that preview with `preview_only`.

## Metrics

Prometheus metrics, when `observability { metrics { listen ... } }` is set:

- Backlog per route: `hookaido_queue_route_depth{route,consumer_group,state}`, `hookaido_queue_route_oldest_queued_age_seconds`, `hookaido_queue_route_ready_lag_seconds`.
- Why senders are rejected: `hookaido_ingress_auth_rejected_total{route,reason}`. Reasons are `no_valid_secret`, `signature_mismatch`, `timestamp_out_of_window`, `replay`, `malformed`, `credentials`, `forward_denied`.
- Rejects by status: `hookaido_ingress_rejected_by_reason_total{route,reason,status}` for `429`/`503`/`413` etc.
- SSE consumers per route: `hookaido_pull_sse_connection_active{route}`.

## MCP Roles

```bash
# Read-only diagnostics
hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db --role read

# Queue mutations
hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db \
  --enable-mutations --role operate --principal ops@example.test

# Full admin, including config apply, secret rotation, and process control
hookaido mcp serve --config ./Hookaidofile --db ./.data/hookaido.db \
  --enable-mutations --enable-runtime-control --role admin \
  --principal ops@example.test --pid-file ./hookaido.pid
```

Tools by role:

- **read:** `config_parse`, `config_validate`, `config_compile`, `config_fmt_preview`, `config_diff`, `admin_health`, `management_model`, `backlog_top_queued`, `backlog_oldest_queued`, `backlog_aging_summary`, `backlog_trends`, `messages_list`, `attempts_list`, `dlq_list`, `pull_consumers`.
- **operate** (with `--enable-mutations`): `dlq_requeue`, `dlq_delete`, `messages_publish`, `messages_cancel`, `messages_requeue`, `messages_resume`, `messages_*_by_filter`.
- **operate** (with `--enable-runtime-control`): `instance_status`, `instance_logs_tail`.
- **admin:** `config_apply`, `management_endpoint_upsert`, `management_endpoint_delete`, `rotate_secret`, `instance_start`, `instance_stop`, `instance_reload`.

Client registration for OpenClaw and Claude Code is in `openclaw.md` → MCP. It requires Hookaido v2.15.2+.
