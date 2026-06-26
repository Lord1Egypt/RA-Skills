# Docker and container edge cases

## Short answer

Yes, the skill can still be used when OpenClaw runs in Docker, but the recommended deployment shape changes.

Do not assume the Shopify connector, Tailscale, and systemd all belong inside the same container.

## Recommended deployment shapes

### 1. Best default: OpenClaw in Docker, Shopify connector on the host

Use this when:

- OpenClaw already runs in Docker
- the host has systemd
- the host can run Tailscale directly

Why this is the best default:

- systemd works normally on the host
- Tailscale Serve/Funnel works normally on the host
- the Shopify connector can bind to `127.0.0.1` on the host
- fewer container-networking surprises

In this model:

- OpenClaw stays in Docker
- Shopify connector runs as a host process/service
- Tailscale runs on the host
- Shopify public callback/webhook traffic reaches the host service

### 2. Good fallback: OpenClaw in Docker, Shopify connector in a separate sidecar container

A productized starter compose file is available under `examples/docker-compose.sidecar.yml` in the source repo, with usage notes in `examples/docker-compose.sidecar.md`.

Use this when:

- the user wants everything containerized
- they are comfortable with Docker Compose networking
- they do not need host systemd for the connector lifecycle

In this model:

- OpenClaw runs in one container
- Shopify connector runs in a second container
- a reverse proxy or Tailscale sidecar/host handles public HTTPS

Caveat:

- systemd helper scripts are not the right control plane here
- use `docker compose up -d`, `docker compose stop`, `docker compose logs` instead

### 3. Possible but not ideal: OpenClaw + Shopify connector inside one container

Use only for simple experiments.

Why it is not ideal:

- mixes concerns
- harder restarts and logging separation
- systemd often unavailable in normal containers
- Tailscale inside the same app container adds more moving parts

## What changes in Docker

### systemd

The bundled service template is for host or VM deployments with systemd.

If the connector runs in a normal container:

- do not try to use host-style systemd management inside the container
- use your container orchestrator instead

### Tailscale

Best practice for Docker-based OpenClaw installs:

- run Tailscale on the host if possible
- expose the connector through the host
- avoid forcing Tailscale into the same application container unless there is a clear reason

### Local bind / networking

If the connector runs on the host:

- bind to `127.0.0.1`
- let Tailscale or the reverse proxy publish it

If the connector runs in a container:

- bind to the container port
- publish only through an explicit proxy or ingress path
- ensure the configured public callback URL matches the published path exactly

## Persistence

Container filesystems are often ephemeral.

If the connector runs in Docker, persist at least:

- `config.json`
- `.env`
- `state/`
- `logs/`

Mount them from a host volume.

## Production recommendation

For most users running OpenClaw in Docker, recommend:

- OpenClaw containerized
- Shopify connector on the host or a dedicated sidecar
- Tailscale on the host
- persistent runtime files on host storage

That is the least fragile setup.
