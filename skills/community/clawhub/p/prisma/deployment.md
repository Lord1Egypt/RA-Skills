# Deployment — Generate, Engines, Containers, and Serverless

Almost every Prisma deployment failure is one of two things: the client was never generated in that environment, or it was generated for a different platform than the one running it. Both surface as an initialization error at the first query, long after the build looked green.

## Contents

- The generate contract
- Engines and `binaryTargets`
- Docker
- Serverless (Lambda, Cloud Functions, Vercel Functions)
- Edge runtimes
- Platform notes
- Environment variables
- Pre-deploy checklist

## The Generate Contract

`@prisma/client` is a shell; the real client is written by `prisma generate` into the generator's `output` directory. It must run wherever `node_modules` is created or restored.

- Keep `"postinstall": "prisma generate"` in `package.json` **and** an explicit generate step in the build. The postinstall covers local installs; the explicit step covers every CI that restores a cache instead of installing.
- Generation needs the schema, not the database. It runs offline — except with TypedSQL, which analyzes real SQL against a live database (→ `raw-sql.md`).
- Pin `prisma` and `@prisma/client` to the same exact version. A mismatched pair produces errors that read like schema problems.
- Set the generator `output` explicitly. Writing into `node_modules` leaves the client at the mercy of hoisting, pruning and layer caching:

```prisma
generator client {
  provider      = "prisma-client-js"
  output        = "../src/generated/prisma"
  binaryTargets = ["native", "debian-openssl-3.0.x"]
}
```

With an explicit output, the client is application code: it is bundled, copied and traced like anything else in `src`.

## Engines and `binaryTargets`

The query engine is a native binary matched to libc and OpenSSL. `native` covers the machine that ran `generate`; every other machine that will run the client needs its target listed.

| Runtime | Target |
|---|---|
| Debian/Ubuntu (bookworm, 22.04+) | `debian-openssl-3.0.x` |
| Debian/Ubuntu (bullseye, 20.04) | `debian-openssl-1.1.x` |
| Alpine (musl), OpenSSL 3 | `linux-musl-openssl-3.0.x` |
| Alpine (musl), older | `linux-musl` |
| AWS Lambda on Amazon Linux 2 | `rhel-openssl-1.0.x` |
| AWS Lambda on Amazon Linux 2023 | `rhel-openssl-3.0.x` |
| ARM64 Linux containers | `linux-arm64-openssl-3.0.x` |

- "Query engine could not be located" or "not compatible with the detected platform" is this table, always.
- Building on an arm64 laptop for an amd64 host produces a client whose only engine is the wrong architecture — build with the target platform or list both targets.
- Alpine also needs OpenSSL present in the image (`apk add --no-cache openssl`); musl images ship without it more often than not.

## Docker

```dockerfile
FROM node:22-bookworm-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends openssl && rm -rf /var/lib/apt/lists/*
COPY package*.json ./
RUN npm ci
COPY prisma ./prisma
RUN npx prisma generate            # after deps, before source: the cache layer that matters
COPY . .
RUN npm run build

FROM node:22-bookworm-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends openssl && rm -rf /var/lib/apt/lists/*
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY --from=build /app/prisma ./prisma      # migrations, for the release step
CMD ["node", "dist/main.js"]
```

- Copy `prisma/` into the runtime image only if that image runs `migrate deploy`. Prefer a separate release step or job that does (→ `migrations.md`).
- `npm prune --production` after generating can delete the `prisma` CLI while keeping the generated client — fine for the app, fatal for an image expected to run migrations.
- The generate step belongs after `npm ci` and before `COPY . .`, so a source edit does not invalidate it.

## Serverless (Lambda, Cloud Functions, Vercel Functions)

- Instantiate the client **outside** the handler so warm invocations reuse it; a client created inside the handler opens a pool per invocation.
- `connection_limit=1-2` plus an external pooler. Sandbox count is set by traffic, and every sandbox has its own pool (→ `connections.md`).
- Never `$disconnect()` at the end of a handler: the next warm invocation then pays a reconnect.
- Bundlers do not follow the engine binary. With `output` inside `src`, most bundlers copy it; otherwise add an explicit copy step or a bundler plugin, and verify by listing the deployment artifact rather than by deploying and hoping.
- Package size: one engine binary is tens of megabytes. Restrict `binaryTargets` to the one target the platform actually uses.
- Cold start includes engine startup. Provisioned concurrency, or an HTTP-based path (Accelerate, a driver adapter over HTTP), are the two ways out.

## Edge Runtimes

Edge (Vercel Edge, Cloudflare Workers, Deno Deploy) has no TCP sockets and no native binaries, so the standard engine cannot run there. Two supported shapes:

- **Driver adapters** — a JavaScript driver for a database that speaks HTTP or WebSockets (Neon, PlanetScale, Turso/libSQL, Cloudflare D1). Connection behavior becomes the driver's, and the available feature set is narrower than the native engine's.
- **Prisma Accelerate** — the client talks HTTP to a managed pooler that holds the real connections.

Both were preview features before becoming standard paths; check what the installed version requires in its generator block rather than assuming.

## Platform Notes

- **Vercel**: the build cache can restore `node_modules` without running `postinstall`, shipping yesterday's client. Put `prisma generate` in the build command explicitly. Migrations belong in a release step, not in the build.
- **Next.js**: the client is server-only — importing it from a client component pulls the engine into the browser bundle and fails at build. In dev, use the `globalThis` singleton or hot reload exhausts the pool (→ `connections.md`).
- **Monorepos**: generate into a shared package with an explicit `output`, and let every app import that package. Two apps generating into their own `node_modules` from the same schema is two clients whose types diverge the moment one of them skips a generate.
- **Standalone builds and file tracing**: bundlers that trace dependencies need the generated directory and the engine file included explicitly when they live outside `node_modules`.

## Environment Variables

- `DATABASE_URL` is needed at **runtime** for queries and at **build time** only for TypedSQL and introspection. A build failing on a missing URL usually means something invoked `db pull` or `migrate` where it should have invoked `generate`.
- The Prisma CLI reads `.env`; your application at runtime does not, unless it loads it. Deployment platforms inject env vars into the process, which is why the same code reads the URL in production and not in a local script.
- Use a pooled URL for the app and `directUrl` for migrations when a transaction-mode pooler is in play (→ `connections.md`).
- Never bake credentials into the image. The URL is runtime configuration, and it appears in `docker history` if it was ever an ARG.

## Pre-Deploy Checklist

- Does the deploy path run `prisma generate`, provably (check the build log, not the config)?
- Does `binaryTargets` list the runtime platform, and does the image have OpenSSL?
- Do `prisma` and `@prisma/client` versions match exactly?
- Is `migrate deploy` a separate release step, running once, with a DDL-capable role?
- Is the client a process-level singleton, with `connection_limit` set for this topology?
- Does a smoke test run one real query against the deployed artifact before traffic reaches it?
