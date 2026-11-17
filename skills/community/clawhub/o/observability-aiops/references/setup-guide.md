# observability-aiops setup & security guide

> The Prometheus/Alertmanager/Grafana surfaces have been exercised against a live Prometheus 3.x + Alertmanager + Grafana 13 stack; the Loki surface has not
> (see docs/VERIFICATION.md). **Prometheus,
> Grafana, and Loki are all free/open-source and trivial to stand up in a lab
> (`docker run prom/prometheus`, `grafana/grafana`, `grafana/loki`), so a live
> `doctor` check is easy.**

## 1. Install

```bash
uv tool install observability-aiops
```

## 2. Get a credential

- **Prometheus** — a bearer token is **optional**; many self-hosted deployments
  are unauthenticated. observability-aiops talks to the HTTP API on port **9090**
  and a companion Alertmanager on **9093** (`/api/v2`).
- **Grafana** — a **service-account token** (Administration → Service accounts →
  Add token) or legacy API key is **required**. Grafana's HTTP API is on port
  **3000**.
- **Loki** — auth is **optional** (bearer token, or per-target `basic` auth where
  the stored secret is `user:password`). The HTTP API is on port **3100**. For a
  multi-tenant deployment set `org_id` to send the `X-Scope-OrgID` header. Loki is
  **read-only** here.

## 3. Onboard

```bash
observability-aiops init
```

The wizard asks, per target, for the **platform** (`prometheus` / `grafana` /
`loki`), the **host**, the **scheme** (`http` / `https`), the **port** (defaults
9090 for Prometheus, 3000 for Grafana, 3100 for Loki), an optional **Alertmanager
URL** (Prometheus only), the **auth type** and **org id** (Loki only), and the
**token** — required for Grafana, optional for Prometheus/Loki. Non-secret
connection details go to `~/.observability-aiops/config.yaml`; the token is stored
**encrypted** into `~/.observability-aiops/secrets.enc`. Example config (one config
can span the whole stack):

```yaml
targets:
  - name: prod-prom
    platform: prometheus
    host: 10.0.0.20
    scheme: http
    port: 9090
    alertmanager_url: http://10.0.0.20:9093   # optional; blank assumes host:9093
  - name: prod-grafana
    platform: grafana
    host: 10.0.0.30
    scheme: https
    port: 3000
    verify_ssl: true
  - name: prod-loki
    platform: loki
    host: 10.0.0.40
    scheme: http
    port: 3100
    auth_type: bearer        # or 'basic' (secret is user:password)
    org_id: team-a           # optional; sent as X-Scope-OrgID (multi-tenant)
```

## 4. Non-interactive use (MCP server / CI / cron)

Export the master password so the encrypted store can be unlocked without a
prompt:

```bash
export OBSERVABILITY_AIOPS_MASTER_PASSWORD='your-master-password'
```

## Credential security

- The token is **never** written to disk in plaintext. It lives only in
  `~/.observability-aiops/secrets.enc`, encrypted with Fernet (AES-128-CBC +
  HMAC), the key derived from your master password via scrypt. Only a per-store
  random salt and the ciphertext are on disk (chmod 600); the master password
  itself is never stored.
- A legacy plaintext env var `OBSERVABILITY_<TARGET_NAME_UPPER>_TOKEN` is still
  honoured as a fallback with a deprecation warning — migrate with
  `observability-aiops secret migrate` (it imports then renames the old `.env`).
- The token is sent as an `Authorization: Bearer` header at request time and held
  only in memory; it is never logged or echoed. Exception text and tracebacks are
  scrubbed of secret-shaped strings before being written to the audit log.

## Governance harness state

State lives under `~/.observability-aiops/` (relocate with `OBSERVABILITY_AIOPS_HOME`):

- `audit.db` — every tool call (SQLite), with risk tier and any operator-supplied
  approver/rationale (optional annotations, never required)
- `undo.db` — inverse descriptors for reversible writes (create_silence→expire,
  update/delete dashboard→restore/recreate)
- budget / runaway guard — caps cumulative tool calls and wall-time; trips on
  tight poll/retry loops

## Governed writes

- **High-risk** op (`delete_dashboard`) supports `dry_run` and captures the full
  prior dashboard model **before** deleting so the recorded undo can recreate
  it. Optionally set `OBSERVABILITY_AUDIT_APPROVED_BY` and
  `OBSERVABILITY_AUDIT_RATIONALE` to annotate the audit row — neither is
  required, and the write runs either way.
- **Reversible** writes capture the real fetched before-state:
  `update_dashboard` (restore prior model), `create_silence` (expire the created
  silence). `reload_prometheus_config` records the pre-reload config hash.
- **Time-boxed** ops require a positive duration: `create_silence` (in minutes).
  This prevents forgotten, indefinite silences.

## Verify

```bash
observability-aiops doctor
```

`doctor` is platform-aware: it checks the config file, the encrypted store and its
permissions, that a token is present where required, and (unless `--skip-auth`)
connectivity — `/api/v1/status/buildinfo` for Prometheus targets, `/api/health`
for Grafana targets, and `/ready` + `/loki/api/v1/status/buildinfo` for Loki
targets.

## Loki query bounding (safety)

Loki reads are deliberately bounded so an agent can't ask for "all logs, forever":

- Every `loki_query` must carry a `{…}` **stream selector** — an unbounded query
  with no selector (or an empty query) is rejected with a teaching error.
- Lookback is capped at **24h** (`MAX_LOOKBACK_HOURS`); a longer window is refused.
- Returned lines are clamped to **1000** (`MAX_LINE_LIMIT`, default 100).
- `loki_tail_errors` wraps a selector with a canned case-insensitive error filter.
- Label values interpolated into a selector are backslash-escaped and label names
  in a path segment are percent-encoded, so a hostile label value can't break out
  of the LogQL string or rewrite the request path.
