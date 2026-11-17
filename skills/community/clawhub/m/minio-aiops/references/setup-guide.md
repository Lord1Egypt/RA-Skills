# minio-aiops setup & security guide

> Verification status: mock-validated; no recorded end-to-end run against a
> live MinIO server yet. The cheapest live check is a single-node server
> running `minio-aiops doctor` — see `docs/VERIFICATION.md`.

## 1. Install

```bash
uv tool install minio-aiops        # or: pipx install minio-aiops
```

## 2. What the tool talks to

Four surfaces on the same MinIO origin:

- **S3 API** (`host:port`, default `9000`) — SigV4-signed via the official
  SDK; needs an access/secret key pair. Admin features (bucket quota,
  `server_info`) need **admin-capable** keys.
- **Health endpoints** — `/minio/health/live`, `/ready`, `/cluster`
  (unauthenticated by design).
- **Metrics endpoint** — `/minio/v2/metrics/cluster`. Two auth modes,
  matching the server's `MINIO_PROMETHEUS_AUTH_TYPE`:
  - `public` → set `metrics_public: true` for the target; no header sent.
  - default (`jwt`) → the tool derives a bearer token from the stored
    credentials at request time. **No extra secret to configure.**

## 3. Onboard a target

```bash
minio-aiops init
```

The wizard prompts for: target name, host, port, **TLS** (default yes),
**certificate verification** (default yes — answer No only for self-signed lab
certs), optional region, access key, secret key (hidden → encrypted store),
and whether the metrics endpoint is public.

Resulting `~/.minio-aiops/config.yaml` (non-secret only):

```yaml
targets:
  - name: lab1
    host: 192.0.2.10
    port: 9000
    access_key: minio-ops
    secure: true
    verify_ssl: true
    region: ""
    metrics_public: false
```

## 4. Secrets

- Secret keys live **encrypted** in `~/.minio-aiops/secrets.enc`
  (Fernet + scrypt master password; file chmod 600). Never in config.yaml.
- Non-interactive use (MCP server, CI): export
  `MINIO_AIOPS_MASTER_PASSWORD`. MCP clients start the server **without a TTY
  and without your shell profile** — put the variable in the client's `env`
  block.
- Legacy fallback: `MINIO_<TARGET_NAME_UPPER>_SECRET_KEY` (plaintext env) is
  honoured with a warning — migrate with `minio-aiops secret migrate`.

## 5. Verify

```bash
minio-aiops doctor
```

Checks config + secrets, then per target: live/ready endpoints, an
authenticated `ListBuckets` (proves the key pair), and metrics reachability
(the capacity/healing analyses depend on it — a failure prints the
`metrics_public` hint).

## 6. MCP client config

```json
{
  "mcpServers": {
    "minio-aiops": {
      "command": "uvx",
      "args": ["--from", "minio-aiops", "minio-aiops-mcp"],
      "env": { "MINIO_AIOPS_MASTER_PASSWORD": "your-master-password" }
    }
  }
}
```

## 7. Governance state

Everything lives under `~/.minio-aiops/` (relocatable via
`MINIO_AIOPS_HOME`): `audit.db` (every call) and `undo.db` (inverse descriptors
for reversible writes). The tool does not decide whether a write is permitted —
that is the agent's judgement or the permission of the access key you connect
with (a read-only IAM policy makes writes fail at the server); there is no
read-only switch, policy file, or approval gate. `MINIO_AUDIT_APPROVED_BY`
(+ `MINIO_AUDIT_RATIONALE`) are optional audit annotations, recorded when set
and never required.

## Self-test with a local server

Any single-node MinIO works — run the server binary (or a container image)
with a local data directory, create a key pair, then:

```bash
minio-aiops init      # point at 127.0.0.1:9000, secure: No for plain http
minio-aiops doctor
minio-aiops overview
```

Erasure-set / healing findings (`heal status`) only show substance on a
multi-drive deployment.
