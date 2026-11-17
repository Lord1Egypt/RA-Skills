# hybrids3 setup

Consumer-side reference for standing up an instance to talk to. If an operator already runs one, you only need its URL and a bucket key. Skip to [OpenClaw / ClawHub Config](#openclaw--clawhub-config).

## Requirements

- Docker
- A `config.yaml` (buckets, keys, master key; see [Configuration](#configuration))
- A persistent volume/dir for `/data` (object bytes + SQLite metadata)
- ~1 core / modest RAM. It's a thin FastAPI service, not a cluster

The container runs as **UID 1000** and expects:

- Config file mounted at `/config/config.yaml`
- Data at `/data`
- Listens on port `8080`

## Quick Install

Grab the example config, edit keys + buckets, run:

```bash
# fetch the example config
wget -O config.yaml \
  https://raw.githubusercontent.com/psyb0t/docker-hybrids3/master/config.example.yaml

# edit it: set master_key and each bucket's key
vi config.yaml

# run
docker run -d --name hybrids3 \
    -p 127.0.0.1:8080:8080 \
    -v ./config.yaml:/config/config.yaml:ro \
    -v hybrids3-data:/data \
    psyb0t/hybrids3

# verify
curl http://localhost:8080/health      # → {"status":"ok"}
```

**`-p 8080:8080` binds all interfaces**: the service becomes reachable from the network, not just localhost. Use `-p 127.0.0.1:8080:8080` (loopback-only) unless remote access is intentionally required, matching the fleet convention.

### docker-compose

```yaml
services:
  hybrids3:
    image: psyb0t/hybrids3
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - ./config.yaml:/config/config.yaml:ro
      - hybrids3-data:/data
    restart: unless-stopped

volumes:
  hybrids3-data:
```

**`"127.0.0.1:8080:8080"` binds loopback-only.** Use `"8080:8080"` only if remote access is intentionally required, matching the fleet convention above. For a real deployment where other hosts or services need to reach it, put hybrids3 on an internal Docker network and front it with a reverse proxy (see [Behind a Reverse Proxy](#behind-a-reverse-proxy)) rather than publishing the port on all interfaces.

**Uploads to a `public: true` bucket are world-readable.** Any bucket with `public: true` serves GET/HEAD/LIST with no authentication at all. Anyone who can reach the port can read anything stored there. Don't put sensitive data in a public bucket, and keep the port bound to loopback (or behind an authenticating proxy) unless that's the intended exposure.

## Configuration

**All configuration is the YAML file. There are no application env vars.** Buckets are defined here and only here; there is no create/delete API. Change config and restart to add or remove a bucket.

Top-level keys:

| Field | Default | What it does |
|---|---|---|
| `master_key` | `""` | Cross-bucket god key. Works on every bucket, only credential that lists all buckets. Keep secret. |
| `master_public_key` | `"master"` | Non-secret `aws_access_key_id` paired with `master_key` in S3 auth. Safe to share. |
| `cleanup_interval` | `60` (`1m`) | How often the background loop deletes expired objects + orphan files. Duration string (`30s`, `5m`, `1h`) or raw seconds. |
| `lock_acquire_timeout` | `30` | Seconds a request waits for a per-key lock before `503`. Float. |
| `lock_hold_timeout` | `300` | Seconds a request may hold a lock before it's force-released with `503`. Guards stalled uploads. |
| `lock_max_waiters` | `100` | Max requests queued for one key before new ones get `503` immediately. |
| `path_prefix` | `""` | Serve all routes under a subpath (e.g. `/storage`) for reverse-proxy deployments. `"/storage"` and `"/storage/"` both normalize. Empty = root. |

Per-bucket fields (under `buckets:`, keyed by bucket name; the name must not contain `/` or `..`):

| Field | Default | What it does |
|---|---|---|
| `key` | **required** | Private key: Bearer token (HTTP/MCP) + `aws_secret_access_key` (S3). Never transmitted. Keep secret. |
| `public` | `false` | `true` = anyone reads (GET/HEAD/LIST) without auth; writes still need a key. `false` = auth for everything. |
| `public_key` | bucket name | Public `aws_access_key_id`; appears in presigned `Credential=`. Safe to share. |
| `ttl` | `0` | Objects expire this long after last write (overwrite resets). `0` = never. Formats: `30s 5m 1h 1h30m12s 1d 2d12h`. |
| `max_file_size` | `0` | Reject uploads over this with `413`. Formats: `500B 50KB 10MB 1GB`, `0` = no limit. |

Minimal example (`config.example.yaml`):

```yaml
master_key: "change-me-to-something-secret"
master_public_key: "master"
cleanup_interval: 1m
lock_acquire_timeout: 30
lock_hold_timeout: 300
lock_max_waiters: 100
# path_prefix: /storage

buckets:
  uploads:
    public: true
    key: "uploads-secret"
    public_key: "uploads-id"
    ttl: 24h
    max_file_size: 50MB

  permanent:
    public: false
    key: "perm-secret"
    public_key: "permanent-id"
    ttl: 0
    max_file_size: 100MB
```

## Environment Variables

The **application** takes no env vars; everything is in `config.yaml`. The only tunables at run time are Docker-level:

| Concern | How | Example |
|---|---|---|
| Config path | mount to `/config/config.yaml` | `-v ./config.yaml:/config/config.yaml:ro` |
| Data location | mount to `/data` | `-v hybrids3-data:/data` |
| Host port / interface | `docker run -p` | `-p 127.0.0.1:8080:8080` (loopback), `-p 8080:8080` (all interfaces) |

For S3 clients (`boto3`, `aws-cli`), the credentials aren't hybrids3 env vars. They're the standard AWS SDK ones, sourced from a bucket's config:

| SDK var / arg | Value from config |
|---|---|
| `AWS_ACCESS_KEY_ID` / `aws_access_key_id` | the bucket's `public_key` (or `master_public_key`) |
| `AWS_SECRET_ACCESS_KEY` / `aws_secret_access_key` | the bucket's `key` (or `master_key`) |
| `AWS_DEFAULT_REGION` / `region_name` | any value. The server doesn't check it; `us-east-1` below is just an example |
| `endpoint_url` | `HYBRIDS3_URL` (e.g. `http://localhost:8080`) |

The skill's own convenience vars for HTTP/MCP work: `HYBRIDS3_URL`, `HYBRIDS3_KEY`, `HYBRIDS3_PUBLIC_KEY`, `HYBRIDS3_MASTER_KEY`, `HYBRIDS3_MASTER_PUBLIC_KEY`.

## Ports

| Port | Service |
|---|---|
| 8080 | HTTP API + S3 API + MCP (`/mcp/`), all on the same port |

The container listens on `8080` internally. Map it however you like with `-p`.

## Behind a Reverse Proxy

Set `path_prefix` in config to match the proxy location; hybrids3 serves every route under it natively (including `/{prefix}/health`), so nginx forwards the path **as-is**, no stripping. SigV4 works because the signed path matches what the server sees.

```yaml
# config.yaml
path_prefix: /storage
```

```nginx
location /storage {
    proxy_pass http://hybrids3:8080;          # NO trailing slash: forwards full path
    proxy_set_header Host $http_host;         # $http_host, NOT $host: keeps the port for SigV4
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Then clients use the prefixed URL: `HYBRIDS3_URL=http://yourdomain/storage`, boto3 `endpoint_url="http://yourdomain/storage"`, MCP `http://yourdomain/storage/mcp/`.

A trailing slash in `proxy_pass` (`http://hybrids3:8080/`) strips the prefix and breaks SigV4, so don't. `$host` drops the port and also breaks SigV4, so use `$http_host`.

## Management

```bash
docker logs -f hybrids3                 # tail structured JSON logs (one line per entry)
docker stop hybrids3                     # stop
docker rm hybrids3                       # remove
docker pull psyb0t/hybrids3              # update image
curl http://localhost:8080/health        # liveness → {"status":"ok"}
```

Logs are structured JSON to stdout with a per-request `rid` that matches the `X-Request-Id` response header, so you can trace one request end-to-end. The private `key` is never logged.

## OpenClaw / ClawHub Config

```bash
export HYBRIDS3_URL=http://localhost:8080
export HYBRIDS3_KEY=<bucket-private-key>        # only if you'll write / read private buckets
export HYBRIDS3_MASTER_KEY=<master-key>         # only for cross-bucket / list-all
```

Or via `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "hybrids3": {
        "env": {
          "HYBRIDS3_URL": "http://localhost:8080",
          "HYBRIDS3_KEY": "<bucket-private-key>"
        }
      }
    }
  }
}
```
