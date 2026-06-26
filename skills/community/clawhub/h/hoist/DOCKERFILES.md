# Dockerfile & Docker Compose Reference for Hoist

Hoist deploys apps by building a Dockerfile on the server. If the project has no Dockerfile, generate one using the patterns below. If the project uses Docker Compose, see the Docker Compose section.

## Best Practices

1. **Multi-stage builds** — separate build deps from runtime to keep images small
2. **Non-root user** — always `USER` a non-root user in production
3. **`.dockerignore`** — always create one (see template below)
4. **Pin versions** — use specific tags (`node:22-slim`), never `latest`
5. **Layer caching** — copy lockfile first, install, then copy source
6. **Exec form for CMD** — use `CMD ["node", "server.js"]` not `CMD node server.js` (shell form breaks signal handling and delays shutdown ~10s)
7. **`npm ci` not `npm install`** — deterministic, respects lockfile, faster
8. **`--no-audit --no-fund`** — skip unnecessary network calls in CI
9. **Combine RUN commands** — `apt-get update && apt-get install` in one layer (separate causes stale cache)
10. **Never embed secrets** — use `--mount=type=secret` at build time, env vars at runtime
11. **Prefer `-slim` over `alpine` for Python** — alpine causes 50x slower pip installs due to source compilation
12. **Pointer compression** — for Node.js 25+, swap `node:25-slim` with `platformatic/node-caged:25-slim` for ~50% less memory, better P99 latency (V8 pointer compression). 4GB heap limit per isolate. Incompatible with legacy NAN native addons (check: `npm ls nan`). N-API modules (sharp, bcrypt, etc.) work fine.

## .dockerignore

Always create alongside the Dockerfile:

```
node_modules
.git
.gitignore
.env*
dist
.next
.turbo
coverage
*.md
.DS_Store
docker-compose*.yml
Dockerfile
```

---

**Tip:** For all Node.js Dockerfiles below, swap `node:22-slim` with `platformatic/node-caged:22-slim` to cut memory ~50%. See the node-caged section below for constraints.

---

## Next.js

Requires `output: "standalone"` in `next.config.js`. Uses built-in `node` user.

```dockerfile
FROM node:22-slim AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./
RUN if [ -f package-lock.json ]; then npm ci --no-audit --no-fund; \
    elif [ -f yarn.lock ]; then corepack enable yarn && yarn install --frozen-lockfile; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm install --frozen-lockfile; \
    else echo "No lockfile found." && exit 1; fi

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NODE_ENV=production
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0
COPY --from=builder --chown=node:node /app/public ./public
RUN mkdir .next && chown node:node .next
COPY --from=builder --chown=node:node /app/.next/standalone ./
COPY --from=builder --chown=node:node /app/.next/static ./.next/static
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

**Critical:** `HOSTNAME=0.0.0.0` is required or the app won't be reachable outside the container.

---

## Remix

Four-stage build: all deps -> production deps only -> build -> production.

```dockerfile
FROM node:22-slim AS base
ENV NODE_ENV=production

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --include=dev --no-audit --no-fund

FROM base AS prod-deps
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY package.json package-lock.json* ./
RUN npm prune --omit=dev

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/build ./build
COPY --from=builder --chown=node:node /app/public ./public
COPY --from=builder /app/package.json ./
USER node
EXPOSE 3000
CMD ["npm", "start"]
```

**Key pattern:** Install all deps (including dev) -> build -> prune to production only -> copy pruned node_modules to final image.

---

## Astro (SSR)

Requires `output: "server"` and a Node adapter in `astro.config.mjs`.

```dockerfile
FROM node:22-slim AS base

FROM base AS prod-deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev --no-audit --no-fund

FROM base AS build-deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund

FROM build-deps AS builder
WORKDIR /app
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=4321
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist
USER node
EXPOSE 4321
CMD ["node", "./dist/server/entry.mjs"]
```

---

## Express / Fastify / Hono (Node.js API)

```dockerfile
FROM node:22-slim AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --omit=dev --no-audit --no-fund

FROM base AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder /app/package.json ./
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

---

## Python (FastAPI / Flask / Django)

Use `-slim`, NOT `alpine` (alpine causes 50x slower pip installs). Use pip wheels for multi-stage.

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN adduser --system --uid 1001 app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels
COPY . .
USER app
EXPOSE 8000
# FastAPI:
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Flask:
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "--worker-tmp-dir", "/dev/shm", "app:app"]
# Django:
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "--worker-tmp-dir", "/dev/shm", "myproject.wsgi"]
```

**Critical Python ENV vars:**
- `PYTHONDONTWRITEBYTECODE=1` — no .pyc files (saves space, avoids stale bytecode)
- `PYTHONUNBUFFERED=1` — logs appear immediately in `docker logs`

**Gunicorn:** Always use `--worker-tmp-dir /dev/shm` to prevent freezes from disk-backed filesystems.

---

## Go

Use `CGO_ENABLED=0` for static binary, `distroless` or `scratch` for minimal runtime.

```dockerfile
FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o server .

FROM gcr.io/distroless/static-debian12 AS runner
COPY --from=builder /app/server /server
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/server"]
```

**Image size:** ~2MB with distroless (vs 1.1GB full Go image).

---

## Rust

Cache dependencies separately to avoid rebuilding on every source change.

```dockerfile
FROM rust:1.82-alpine AS builder
WORKDIR /app
RUN apk add --no-cache musl-dev
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo 'fn main() {}' > src/main.rs && cargo build --release && rm -rf src
COPY . .
RUN cargo build --release

FROM alpine:3.20 AS runner
RUN apk --no-cache add ca-certificates
RUN adduser --system --uid 1001 app
COPY --from=builder /app/target/release/app /app
USER app
EXPOSE 8080
CMD ["/app"]
```

---

## Static Site (Vite, CRA, Astro static)

Build locally, serve with Caddy:

```dockerfile
FROM node:22-slim AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund
COPY . .
RUN npm run build

FROM caddy:2-alpine AS runner
COPY --from=builder /app/dist /srv
EXPOSE 80
CMD ["caddy", "file-server", "--root", "/srv", "--listen", ":80"]
```

For SPA routing (fallback to index.html), create a Caddyfile:
```
:80 {
    root * /srv
    file_server
    try_files {path} /index.html
    encode gzip
}
```

---

## Docker Compose (Production)

For multi-service apps, generate a `docker-compose.yml` alongside the Dockerfile.

```yaml
services:
  app:
    build: .
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env.production
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"
    healthcheck:
      test: ["CMD", "wget", "-q", "-O-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      start_period: 10s
      retries: 3
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    deploy:
      resources:
        limits:
          memory: 256M
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redisdata:/data
    deploy:
      resources:
        limits:
          memory: 128M
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
  redisdata:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

**Docker Compose best practices:**
- `restart: unless-stopped` — survives reboots, stops with `docker compose down`
- `deploy.resources.limits` — prevent OOM kills and runaway containers
- `healthcheck` — enables `depends_on: condition: service_healthy`
- `secrets` — never put passwords in `environment`, use secrets mounted at `/run/secrets/`
- `env_file` — keep secrets out of `docker-compose.yml`
- Named volumes for persistence

---

## Security

- **Never expose Docker socket** (`-v /var/run/docker.sock`) to containers
- **Never use `--privileged`**
- **Drop all capabilities:** `docker run --cap-drop all --cap-add CHOWN`
- **Read-only filesystem:** `docker run --read-only --tmpfs /tmp`
- **No new privileges:** `docker run --security-opt=no-new-privileges`
- **Build-time secrets:** `RUN --mount=type=secret,id=key cat /run/secrets/key`
- **Scan images:** `docker scout cves <image>` or `trivy image <image>`
- **Lint Dockerfiles:** `hadolint Dockerfile`

---

## node-caged: Pointer Compression

Swap `node:25-slim` with `platformatic/node-caged:25-slim` for ~50% memory reduction.

**How it works:** V8 pointer compression stores 32-bit offsets instead of 64-bit pointers. Smaller heap = less GC pressure = better P99 latency.

**Constraints:**
- **4GB heap limit per isolate** — each thread (main + workers) gets its own 4GB cage via IsolateGroups. Total memory only limited by system RAM.
- **NAN addons will segfault** — check with `npm ls nan`. If nothing shows, you're safe.
- **N-API addons work fine** — sharp, bcrypt, canvas, sqlite3, etc.
- Available tags: `22`, `22-slim`, `22-alpine`, `25`, `25-slim`, `25-alpine`, `latest`

**Benchmark results (AWS EKS, Next.js SSR, 400 req/s):**
- Memory: ~50% reduction
- Average latency: +2-4%
- P99 latency: -7% (better, due to shorter GC pauses)

---

## Framework Detection

Read `package.json` to detect the framework:

| Dependency | Framework | Port | Notes |
|-----------|-----------|------|-------|
| `next` | Next.js | 3000 | Needs `output: "standalone"` in next.config.js |
| `@remix-run/node` | Remix | 3000 | Four-stage build for prod deps |
| `astro` | Astro | 4321 | Needs `output: "server"` + Node adapter for SSR |
| `express` | Express | 3000 | |
| `fastify` | Fastify | 3000 | |
| `hono` | Hono | 3000 | |

For Python: `requirements.txt`, `pyproject.toml`, or `Pipfile`
For Go: `go.mod`
For Rust: `Cargo.toml`

---

## After Generating a Dockerfile

1. Create `.dockerignore` alongside it
2. For Next.js: verify `output: "standalone"` in `next.config.js`
3. For Next.js: set `HOSTNAME=0.0.0.0` in ENV
4. Set the correct `port` in `hoist.json` to match EXPOSE
5. Add a health check endpoint (`/health` or `/api/health`)
6. Deploy: `hoist deploy`

## Anti-Patterns

- **Separate `apt-get update` and `install`** — stale cache
- **Shell form CMD** — breaks signal handling, 10s shutdown delay
- **`alpine` for Python** — 50x slower builds
- **Secrets in ENV/ARG** — persists in image layers
- **`npm install` instead of `npm ci`** — non-deterministic
- **Missing `.dockerignore`** — bloats context, may leak `.env`
- **Running as root** — security risk
- **`better-sqlite3` with node-caged** — segfaults (non-N-API)
