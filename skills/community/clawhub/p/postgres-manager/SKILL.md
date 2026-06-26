---
name: PostgreSQL Manager
slug: postgres-manager
version: 1.1.0
description: "Manage a shared PostgreSQL Docker container for local dev environments. Handles container lifecycle, database creation/removal, and cross-instance dumps via pg_dump. Joins the shared Docker network created by proxy-manager."
changelog: "v1.1.0: Fix dump to avoid sh -c shell injection (now uses two docker exec with -d flag), validate all DB names against strict regex, warn on default password, bind host port to 127.0.0.1, pin image to postgres:16.4-alpine."
triggers:
  - "start postgres"
  - "stop postgres"
  - "postgres status"
  - "create postgres database"
  - "criar banco postgres"
  - "dump postgres"
  - "postgres-manager"
metadata: {"clawdbot":{"emoji":"🐘","requires":{"bins":["docker"]},"os":["linux","darwin"]}}
---

# PostgreSQL Manager

Manages the shared PostgreSQL Docker container for local dev environments.

## Architecture

```
postgres-manager/
├── docker-compose.yml   # PostgreSQL 16 Alpine container
└── run.sh               # lifecycle + db admin CLI
```

Joins the shared `nginx-proxy_net` network (created by proxy-manager) so app containers connect via hostname `codai_postgres`. Data is persisted in a named volume.

## Commands

```bash
./run.sh start                    # start PostgreSQL container
./run.sh stop                     # stop container (data persists in volume)
./run.sh status                   # status + list databases
./run.sh wait                     # block until PostgreSQL is ready
./run.sh create-db <name>         # CREATE DATABASE (idempotent)
./run.sh drop-db <name>           # DROP DATABASE (interactive confirm)
./run.sh dump <src> <dest>        # pg_dump src | psql dest
./run.sh list-dbs                 # list all non-template databases
./run.sh psql [<db>]              # open psql interactive session
```

## How to Execute Tasks

### Start PostgreSQL for the first time
```bash
cd postgres-manager && ./run.sh start
```
On first run, Docker creates the volume and initializes `codai_main`.

### Create a database for a new instance
```bash
./run.sh create-db codai_feature
```

### Snapshot main database into a new instance
```bash
./run.sh dump codai_main codai_feature
```

### Remove a worktree database
```bash
./run.sh drop-db codai_feature   # prompts for confirmation
```

### Open interactive psql
```bash
./run.sh psql                    # connects to codai_main
./run.sh psql codai_feature      # connects to specific db
```

## Startup Order

1. `proxy-manager start` — creates the shared Docker network
2. `postgres-manager start` — joins the shared network
3. `worktree-manager start <instance>`

## Configuration

| Variable              | Default          | Purpose                        |
|-----------------------|------------------|--------------------------------|
| `POSTGRES_CONTAINER`  | `codai_postgres` | Container name                 |
| `POSTGRES_USER`       | `codai`          | Database user                  |
| `POSTGRES_PASSWORD`   | `pgpass`         | Database password              |
| `POSTGRES_MAIN_DB`    | `codai_main`     | Primary database name          |
| `POSTGRES_PORT`       | `5433`           | Host port (maps to 5432)       |
| `CODAI_NETWORK`       | `nginx-proxy_net`| Shared Docker network name     |

## App Connection

Backend containers connect to PostgreSQL at:
- **Host**: `codai_postgres` (container name on shared network)
- **Port**: `5432`
- **User**: `codai` / **Password**: `pgpass`
- **DB**: `codai_main` (or instance-specific db)

## Rules

- Never drop `POSTGRES_MAIN_DB` — it is the source of truth for snapshots.
- `drop-db` always prompts for confirmation.
- Database names are validated against `^[a-z][a-z0-9_]{0,62}$` before any SQL or shell operation.
- `stop` preserves data in the Docker volume. Use `docker compose down -v` only when you intentionally want to delete persisted data.
- The container uses `restart: unless-stopped` — it will resume after a Docker daemon restart. Run `./run.sh stop` when done.
- The host port (`POSTGRES_PORT`) is bound to `127.0.0.1` only. Set a non-default `POSTGRES_PASSWORD` on shared machines.
- Network is `external: true` — proxy-manager must start first.

## Related Plugins

- `proxy-manager` — creates the shared Docker network (start first)
- `mysql-manager` — MySQL alternative
- `redis-manager` — in-memory cache companion
- `worktree-manager` — app instances that consume PostgreSQL
