---
name: nginxwebui-manager
description: "Manage NginxWebUI reverse proxy rules via its REST API. List/create/delete servers and locations, reload nginx, manage upstreams. All calls through docker exec into the nginxwebui container."
---

# NginxWebUI Manager

Manage NginxWebUI via its built-in REST API. All API calls are made via `docker exec` into the running `nginxwebui` container (requires Docker socket access).

## How it works

- Authenticates via `POST /token/getToken` with username/password
- Stores token in `NGINXWEBUI_TOKEN` env var (auto-refreshed via `--mode login`)
- All subsequent calls use the token in the `token` header

## Usage

### Authentication

```bash
# First time — get token and save to .env
python3 {{SKILL_DIR}}/scripts/manage.py --mode login
```

### Nginx operations

```bash
# Check nginx status
python3 {{SKILL_DIR}}/scripts/manage.py --mode status

# Validate config
python3 {{SKILL_DIR}}/scripts/manage.py --mode check

# Reload nginx
python3 {{SKILL_DIR}}/scripts/manage.py --mode reload
```

### Server (reverse proxy) management

```bash
# List all servers
python3 {{SKILL_DIR}}/scripts/manage.py --mode list-servers

# Add a new reverse proxy
python3 {{SKILL_DIR}}/scripts/manage.py --mode add-server \
  --name "app.example.com" --listen 443 --ssl \
  --pem /path/to/cert.pem --key /path/to/key.pem \
  --descr "My app"

# Delete a server by ID prefix
python3 {{SKILL_DIR}}/scripts/manage.py --mode delete-server --id 12345abc
```

### Location (reverse proxy rule) management

```bash
# List locations for a server
python3 {{SKILL_DIR}}/scripts/manage.py --mode list-locations --server-id 12345abc

# Add a location (path → target)
python3 {{SKILL_DIR}}/scripts/manage.py --mode add-location \
  --server-id 12345abc \
  --path /api/ \
  --target http://10.0.0.5:3000 \
  --descr "API backend"

# Add with websocket support
python3 {{SKILL_DIR}}/scripts/manage.py --mode add-location \
  --server-id 12345abc \
  --path /ws \
  --target http://10.0.0.5:3000 \
  --websocket

# Delete a location
python3 {{SKILL_DIR}}/scripts/manage.py --mode delete-location --id 67890def
```

### Upstream (load balancer) management

```bash
# List upstreams
python3 {{SKILL_DIR}}/scripts/manage.py --mode list-upstreams
```

## Environment variables

- `NGINXWEBUI_USER` — required
- `NGINXWEBUI_PASS` — required
- `NGINXWEBUI_TOKEN` — auto-managed, stored in `.env`

## Requirements

- Docker socket accessible from the calling environment
- Running nginxwebui container (name: `nginxwebui`)
- Valid NginxWebUI admin credentials with API access enabled
