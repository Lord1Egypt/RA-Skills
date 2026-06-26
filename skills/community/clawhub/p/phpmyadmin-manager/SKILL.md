---
name: phpmyadmin-manager
slug: phpmyadmin-manager
version: 1.0.0
description: "Manage the phpMyAdmin Docker container for local dev environments. Provides a web UI for MySQL at http://localhost:8081. Requires mysql-manager and proxy-manager to be running first."
changelog: Initial release.
triggers:
  - "abrir phpmyadmin"
  - "start phpmyadmin"
  - "stop phpmyadmin"
  - "phpmyadmin status"
  - "interface mysql"
  - "admin mysql"
  - "phpmyadmin-manager"
metadata: {"clawdbot":{"emoji":"🔷","requires":{"bins":["docker"]},"os":["linux","darwin"]}}
---

# phpMyAdmin Manager

Manages the phpMyAdmin Docker container, providing a web UI for MySQL database management.

## Architecture

```
phpmyadmin-manager/
├── docker-compose.yml   # phpMyAdmin 5.2 container
└── run.sh               # lifecycle CLI
```

Connects to the shared `nginx-proxy_net` network and reaches MySQL at `codai_db:3306`. No data is persisted — phpMyAdmin is stateless.

## Commands

```bash
./run.sh start    # start phpMyAdmin container
./run.sh stop     # stop container
./run.sh status   # show status and URL
./run.sh open     # print access URL
```

## How to Execute Tasks

### Start phpMyAdmin

Check your session context for the absolute script path, then run:
```bash
<plugin-root>/phpmyadmin-manager/run.sh start
```
Open `http://localhost:8081` in a browser. Login: `root` / MySQL root password.

### Check status
```bash
<plugin-root>/phpmyadmin-manager/run.sh status
```

## Prerequisites

Start in this order:
1. `proxy-manager start` — creates the shared Docker network
2. `mysql-manager start` — MySQL must be running before phpMyAdmin connects

## Configuration

| Variable               | Default             | Purpose                        |
|------------------------|---------------------|--------------------------------|
| `PMA_CONTAINER`        | `codai_phpmyadmin`  | Container name                 |
| `PMA_PORT`             | `8081`              | Host port                      |
| `MYSQL_CONTAINER`      | `codai_db`          | MySQL hostname on shared net   |
| `MYSQL_ROOT_PASSWORD`  | `secret`            | MySQL root password            |
| `PMA_UPLOAD_LIMIT`     | `64M`               | Max SQL file upload size       |
| `CODAI_NETWORK`        | `nginx-proxy_net`   | Shared Docker network name     |

## Rules

- Start `mysql-manager` before this plugin — phpMyAdmin cannot connect without MySQL.
- Port `8081` is bound to `127.0.0.1` — accessible from the host only.
- Use `stop` when done; the container uses `restart: unless-stopped` and survives reboots.

## Related Plugins

- `proxy-manager` — creates the shared Docker network (start first)
- `mysql-manager` — MySQL container that phpMyAdmin connects to
