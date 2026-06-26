---
name: pgadmin-manager
slug: pgadmin-manager
version: 1.0.0
description: "Manage the pgAdmin Docker container for local dev environments. Provides a web UI for PostgreSQL at http://localhost:8082. Requires postgres-manager and proxy-manager to be running first."
changelog: Initial release.
triggers:
  - "abrir pgadmin"
  - "start pgadmin"
  - "stop pgadmin"
  - "pgadmin status"
  - "interface postgres"
  - "admin postgres"
  - "pgadmin-manager"
metadata: {"clawdbot":{"emoji":"🐘","requires":{"bins":["docker"]},"os":["linux","darwin"]}}
---

# pgAdmin Manager

Manages the pgAdmin Docker container, providing a web UI for PostgreSQL database management.

## Architecture

```
pgadmin-manager/
├── docker-compose.yml   # pgAdmin 4 container (pinned to 8.6)
└── run.sh               # lifecycle CLI
```

Connects to the shared `nginx-proxy_net` network and reaches PostgreSQL at `codai_postgres:5432`. Server configurations are persisted in a named volume (`pgadmin_data`).

## Commands

```bash
./run.sh start    # start pgAdmin container
./run.sh stop     # stop container (config persists in volume)
./run.sh status   # show status and URL
./run.sh open     # print access URL
```

## How to Execute Tasks

### Start pgAdmin

Check your session context for the absolute script path, then run:
```bash
<plugin-root>/pgadmin-manager/run.sh start
```
Open `http://localhost:8082` in a browser. Login: `admin@codai.local` / `pgadmin`.

To connect to PostgreSQL inside pgAdmin, add a server with:
- **Host**: `codai_postgres`
- **Port**: `5432`
- **User**: `codai` / **Password**: `pgpass`

### Check status
```bash
<plugin-root>/pgadmin-manager/run.sh status
```

## Prerequisites

Start in this order:
1. `proxy-manager start` — creates the shared Docker network
2. `postgres-manager start` — PostgreSQL must be running before pgAdmin connects

## Configuration

| Variable             | Default              | Purpose                        |
|----------------------|----------------------|--------------------------------|
| `PGADMIN_CONTAINER`  | `codai_pgadmin`      | Container name                 |
| `PGADMIN_PORT`       | `8082`               | Host port                      |
| `PGADMIN_EMAIL`      | `admin@codai.local`  | Login e-mail                   |
| `PGADMIN_PASSWORD`   | `pgadmin`            | Login password                 |
| `CODAI_NETWORK`      | `nginx-proxy_net`    | Shared Docker network name     |

## Rules

- Start `postgres-manager` before this plugin — pgAdmin cannot connect without PostgreSQL.
- Port `8082` is bound to `127.0.0.1` — accessible from the host only.
- Server configurations survive container restarts (stored in `pgadmin_data` volume).
- Use `stop` when done; the container uses `restart: unless-stopped` and survives reboots.
- Use `docker compose down -v` only when you intentionally want to delete saved server configs.

## Related Plugins

- `proxy-manager` — creates the shared Docker network (start first)
- `postgres-manager` — PostgreSQL container that pgAdmin connects to
