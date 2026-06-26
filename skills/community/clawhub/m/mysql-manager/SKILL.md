---
name: MySQL Manager
slug: mysql-manager
version: 1.1.0
description: "Manage a shared MySQL Docker container for local dev environments. Handles container lifecycle, database creation/removal, and cross-instance data dumps. Designed to work alongside proxy-manager and worktree-manager."
changelog: "v1.1.0: Fix dump to avoid sh -c/backtick shell injection (now uses two docker exec), validate all DB names against strict regex, unify password variable (MYSQL_ROOT_PASSWORD takes precedence over MYSQL_ROOT_PASS), warn on default password, bind host port to 127.0.0.1, pin image to mysql:8.0.36."
triggers:
  - "start mysql"
  - "stop mysql"
  - "mysql status"
  - "create database"
  - "criar banco"
  - "remover banco"
  - "drop database"
  - "dump database"
  - "copiar banco"
  - "mysql-manager"
metadata: {"clawdbot":{"emoji":"🗄","requires":{"bins":["docker"]},"os":["linux","darwin"]}}
---

# MySQL Manager

Manages the shared MySQL Docker container used by local dev instances.

## Architecture

```
mysql-manager/
├── docker-compose.yml   # MySQL 8.0 container
└── run.sh               # lifecycle + db admin CLI
```

The MySQL container runs on the shared Docker network (`nginx-proxy_net` by default), making it accessible to all app containers by hostname (`codai_db`). Data is persisted in a named volume (`mysql_data`).

## Commands

```bash
./run.sh start                    # start MySQL container
./run.sh stop                     # stop container (data persists in volume)
./run.sh status                   # container status + list databases
./run.sh wait                     # block until MySQL is ready (for scripts)
./run.sh create-db <name>         # CREATE DATABASE IF NOT EXISTS
./run.sh drop-db <name>           # DROP DATABASE (interactive confirm)
./run.sh dump <src> <dest>        # mysqldump src | mysql dest
./run.sh list-dbs                 # SHOW DATABASES (filtered)
```

## How to Execute Tasks

### Start MySQL for the first time
```bash
cd mysql-manager && ./run.sh start
```
On first run, Docker creates the volume and initializes `codai_main`.

### Create a database for a new instance
```bash
./run.sh create-db codai_alpha
```

### Snapshot main database into a new instance
```bash
./run.sh dump codai_main codai_alpha
```

### Remove a worktree database
```bash
./run.sh drop-db codai_alpha   # prompts for confirmation
```

### Check status
```bash
./run.sh status
```

## Startup Order

Start MySQL **before** starting any app instances:
1. `proxy-manager`: `./run.sh start`  (creates the shared Docker network)
2. `mysql-manager`: `./run.sh start`  (joins the shared network)
3. `worktree-manager`: `./run.sh start <instance>`

## Configuration

Set via environment variables or a `.env` file in `mysql-manager/`:

| Variable               | Default           | Purpose                          |
|------------------------|-------------------|----------------------------------|
| `MYSQL_CONTAINER`      | `codai_db`        | Container name                   |
| `MYSQL_ROOT_PASSWORD`  | `secret`          | MySQL root password (primary)    |
| `MYSQL_ROOT_PASS`      | *(fallback)*      | Legacy alias; `MYSQL_ROOT_PASSWORD` takes precedence |
| `MYSQL_MAIN_DB`        | `codai_main`      | Primary database name            |
| `MYSQL_PORT`           | `3307`            | Host port (maps to 3306)         |
| `CODAI_NETWORK`        | `nginx-proxy_net` | Shared Docker network name       |

## Rules

- Never drop `MYSQL_MAIN_DB` — it is the source of truth for snapshots.
- The `drop-db` command always prompts for confirmation.
- Database names are validated against `^[a-z][a-z0-9_]{0,62}$` before any SQL or shell operation.
- `stop` preserves data in the Docker volume. Use `docker compose down -v` only when you intentionally want to delete persisted data.
- The container uses `restart: unless-stopped` — it will resume after a Docker daemon restart. Run `./run.sh stop` when done.
- The host port (`MYSQL_PORT`) is bound to `127.0.0.1` only. Set a non-default `MYSQL_ROOT_PASSWORD` on shared machines.
- The container name (`codai_db`) is the hostname used by backend apps to connect.

## Related Plugins

- `proxy-manager` — manages the nginx-proxy that routes traffic to app instances (start this first)
- `worktree-manager` — manages app instances and git worktrees (depends on this plugin)
