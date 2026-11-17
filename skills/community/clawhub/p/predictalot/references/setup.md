# predictalot setup

Consumer-facing reference for running / pointing at a predictalot instance. This skill talks to an instance you already run and trust; the notes below cover standing one up if you haven't.

## Requirements

- Docker
- Optional: NVIDIA GPU + NVIDIA Container Toolkit for the CUDA image (CPU works for all five FMs; `chronos-2` is the fastest on CPU)
- Disk for model snapshots under `/models` (per-slug sizes ≈ chronos-2 ~120 MB, timesfm-2.5 ~200 MB, moirai-2 ~50 MB, toto-1 ~580 MB, sundial-base-128m ~490 MB) plus trained tabular models under `/models/tabular/<id>/`

## Security & safety

predictalot is a plain HTTP + MCP service — anyone who can reach the port can call it. Before any non-local / shared deployment:

- Set `PREDICTALOT_AUTH_TOKENS` to a strong generated secret, e.g. `$(openssl rand -hex 32)` — never leave it at a placeholder/default value.
- Bind to loopback by default (`-p 127.0.0.1:8080:8080`); only expose beyond loopback behind a reverse proxy / VPN (see "Public Access via Reverse Proxy" below).

## Quick Install

### CPU

```bash
docker run -d --name predictalot \
  -v $HOME/predictalot-models:/models \
  -e PREDICTALOT_AUTH_TOKENS=$(openssl rand -hex 32) \
  -p 127.0.0.1:8080:8080 \
  psyb0t/predictalot:latest
```

### CUDA

```bash
docker run -d --name predictalot --gpus all \
  -v /srv/predictalot-models:/models \
  -e PREDICTALOT_AUTH_TOKENS=$(openssl rand -hex 32) \
  -e PREDICTALOT_DEVICE=cuda \
  -e PREDICTALOT_PRELOAD=chronos-2,toto-1,sundial-base-128m \
  -p 127.0.0.1:8080:8080 \
  psyb0t/predictalot:latest-cuda
```

`PREDICTALOT_DEVICE=auto` (the default) picks CUDA when available, else CPU.

### docker-compose

```yaml
services:
  predictalot:
    image: psyb0t/predictalot:latest
    ports:
      - "127.0.0.1:8080:8080"
    environment:
      PREDICTALOT_AUTH_TOKENS: "${PREDICTALOT_AUTH_TOKENS:?set to a generated secret, e.g. openssl rand -hex 32}"
      PREDICTALOT_PRELOAD: chronos-2,toto-1
    volumes:
      - ./predictalot-models:/models
    restart: unless-stopped
```

Generate the token once and export it before `docker compose up` (e.g. `export PREDICTALOT_AUTH_TOKENS=$(openssl rand -hex 32)`) — never commit a real token or ship the example value as-is. The token MUST be changed before any non-local/shared deployment.

**Verify:** `curl http://localhost:8080/healthz` returns `{"ok": true}` once boot is done.

**Snapshots:** foundation-model weights download into `/models/<slug>/` on first use (or at boot when listed in `PREDICTALOT_PREFETCH`). Bind-mount `/models` so restarts are no-ops. Trained tabular models persist under `/models/tabular/<id>/`.

## Environment Variables

All runtime config is `PREDICTALOT_*` — set via `docker run -e`, compose `environment:`, or a k8s ConfigMap.

### Auth + bind

| Var | Default | What it does |
|---|---|---|
| `PREDICTALOT_AUTH_TOKENS` | (empty) | Comma-separated bearer tokens. Empty = **refused at startup** unless `PREDICTALOT_ALLOW_NO_AUTH=1`. When set, `Authorization: Bearer <token>` (or `?apiToken=<token>`) required on every `/v1/*` and `/mcp` request. |
| `PREDICTALOT_ALLOW_NO_AUTH` | `0` | Explicit opt-in to run with no tokens (open auth). Required to start with an empty token list. |
| `PREDICTALOT_HOST` | `0.0.0.0` | uvicorn bind host. |
| `PREDICTALOT_PORT` | `8080` | uvicorn bind port (inside the container). |

Control network exposure at `docker run` time:
- `-p 127.0.0.1:8080:8080` — loopback only on the host.
- `-p 8080:8080` — all host interfaces.

### Device + model registry

| Var | Default | What it does |
|---|---|---|
| `PREDICTALOT_DEVICE` | `auto` | `auto` / `cpu` / `cuda` / `cuda:N`. |
| `PREDICTALOT_MODEL_DIR` | `/models` | Where snapshot dirs land (and tabular models: `/models/tabular/<id>/`). **Bind-mount this** to persist. |
| `PREDICTALOT_PREFETCH` | (empty) | Comma-separated slugs or `all` — downloaded at container start before uvicorn boots. |
| `PREDICTALOT_PRELOAD` | (empty) | Comma-separated slugs loaded into memory at boot (skips first-call cold load). |

### Lifecycle (idle unloading)

| Var | Default | What it does |
|---|---|---|
| `PREDICTALOT_MODEL_IDLE_TIMEOUT` | `30m` | Idle time before a loaded FM is unloaded. Go-style durations (`30m`, `1h`, `1d2h3m`). `0` disables auto-unload. |
| `PREDICTALOT_MODEL_IDLE_TIMEOUT_<SLUG>` | inherits global | Per-model override. Slug normalized: uppercase + `-`/`.` → `_` (e.g. `PREDICTALOT_MODEL_IDLE_TIMEOUT_MOIRAI_2`). |

A background sweeper runs every 60 s and unloads models idle past their timeout.

### Limits + per-model caps

| Var | Default | What it does |
|---|---|---|
| `PREDICTALOT_MAX_BODY_SIZE` | `32mb` | Cap on request body — over → 413. Human-readable (`32mb`, `512k`, `1g`) or plain int bytes. |
| `PREDICTALOT_TIMESFM_MAX_CONTEXT` | `2048` | Compile-time max context for TimesFM. Multiple of 32. |
| `PREDICTALOT_TIMESFM_MAX_HORIZON` | `512` | Compile-time max horizon for TimesFM. Multiple of 128. |
| `PREDICTALOT_MOIRAI_MAX_CONTEXT` | `4000` | Wrapper context length for Moirai-2 (shorter inputs zero-padded). |
| `PREDICTALOT_MOIRAI_MAX_HORIZON` | `512` | Upper horizon for Moirai-2. Wrappers are cached per requested horizon. Multivariate requests have a 64-step native limit. |

### Sundial sidecar + logging

| Var | Default | What it does |
|---|---|---|
| `PREDICTALOT_SUNDIAL_SOCK` | `/tmp/predictalot/sundial.sock` | Unix socket the main service uses to reach the sundial sidecar venv. |
| `PREDICTALOT_SUNDIAL_NUM_SAMPLES` | `64` | Monte-Carlo samples per sundial forecast (more = smoother quantiles, linearly slower). |
| `PREDICTALOT_SUNDIAL_READY_TIMEOUT` | `60s` | How long to wait for the sundial sidecar on first request. |
| `PREDICTALOT_LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR`. |

## Ports

| Port | Service |
|---|---|
| 8080 | HTTP API + MCP (`/mcp`) on the same port |

Container binds `0.0.0.0:8080` by default. Use `-p` at `docker run` for whatever host mapping you want.

## Management

```bash
docker logs -f predictalot            # tail logs (sundial worker stderr tagged [sundial])
docker stop predictalot               # stop
docker rm predictalot                 # remove
docker pull psyb0t/predictalot:latest # update
```

Inspect model state without stopping anything:

```bash
curl -s http://localhost:8080/v1/timeseries/univariate/models \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" | jq
```

Free every resident foundation model early when the next task does not need it:

```bash
curl -s -X POST http://localhost:8080/v1/models/unload \
  -H "Authorization: Bearer $PREDICTALOT_AUTH_TOKEN" | jq
```

The endpoint returns `409` while a foundation forecast is active. A forecast body with `"unload": true` instead schedules that model for teardown after concurrent forecasts using the same model have finished.

## OpenClaw / ClawHub Config

```bash
export PREDICTALOT_URL=http://localhost:8080
export PREDICTALOT_AUTH_TOKEN=<token>   # only if the server requires it
```

Or via `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "predictalot": {
        "env": {
          "PREDICTALOT_URL": "http://localhost:8080",
          "PREDICTALOT_AUTH_TOKEN": "<token>"
        }
      }
    }
  }
}
```

## Public Access via Reverse Proxy (optional)

For public exposure, terminate TLS at a reverse proxy (Caddy / Traefik / nginx) and combine it with `PREDICTALOT_AUTH_TOKENS`.

```caddy
predictalot.example.com {
    reverse_proxy localhost:8080
}
```

Set the auth token on the container so even a misconfigured proxy still requires `Authorization: Bearer`. Don't rely on the proxy alone. The same logic applies to Cloudflare Tunnel / Tailscale — the tunnel provides transport security, the bearer token provides app-layer auth.
