# Install and Self-Hosting

Source: upstream compose files and `docs/deployment/` at v0.0.20.

## Stack shape
- One app container (Bun server: admin SPA, CMS API, renderer, migrations, publish scheduler).
- Optional bundled Postgres service; SQLite mode needs no second container.
- Optional Caddy TLS proxy (`compose.tls.yml`) terminating 80/443.
- Persistent storage: data volume (SQLite db) plus uploads volume (media, fonts, plugin packs, published artifacts).

## Compose modes
| Mode | Files | Containers |
|------|-------|-----------|
| SQLite | compose.prod.yml + compose.sqlite.yml | app |
| Postgres | compose.prod.yml | app, postgres |
| add TLS | plus compose.tls.yml | adds caddy |
| source build | plus compose.build.yml with --build | local image tag |

`compose.sqlite.yml` disables the postgres service, sets `DATABASE_URL=sqlite:/app/data/cms.db`, mounts the data volume, and resets depends_on. Image-pull installs set `INSTATIC_IMAGE` and skip `compose.build.yml`.

## Ports and env
- App listens on `PORT` (default 3001). `HOST_PORT` publishes it directly without TLS. With the TLS layer, Caddy owns 80/443 and HOST_PORT is unused.
- Postgres installs must set `POSTGRES_PASSWORD`.
- Set `INSTATIC_SECRET_KEY` (generate per upstream script) before storing AI provider credentials, plugin secrets, or enabling TOTP. It must never change afterward.
- `PUBLIC_ORIGIN` lists canonical origins for CSRF and preview links; unset falls back to the request Host.
- Full env table in `api.md`.

## Image platform (v0.0.20)
- Published image ships linux/amd64 only; upstream says ARM64 hosts should build from source. On Apple Silicon it runs under emulation.
- Pull with `--platform=linux/amd64` and a pinned tag. On macOS Docker Desktop the credential helper can hang anonymous GHCR pulls (symptom: "error getting credentials - signal: terminated"); workaround is `DOCKER_CONFIG` pointed at a directory whose config.json is `{"auths":{}}`.

## Upgrade procedure
1. Read release notes for the target tag (check arm64 image availability).
2. Pull the pinned tag. Recreate the container; named volumes survive. Migrations apply idempotently at boot and a failed migration exits the process.
3. Verify health endpoint, a login, and `/admin/api/cms/setup/status`. Keep the old tag until the operator confirms.
Never track `:latest` on a live instance.

## Managed-platform notes
Railway and Render one-click templates exist upstream and push referral links; irrelevant to self-host except that `RENDER_EXTERNAL_URL` / `RAILWAY_PUBLIC_DOMAIN` participate in origin derivation. Upstream also documents a Caddy TLS layer; see `publishing.md`.
