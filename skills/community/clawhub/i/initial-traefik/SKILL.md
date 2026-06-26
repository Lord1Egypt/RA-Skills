---
name: initial-traefik
description: Initialize and configure Traefik reverse proxy with Docker. Install Traefik, configure Docker Compose, set up service routing via path prefix or host-based routing, enable features like dashboard metrics logging tracing, configure Dashboard access via nip.io or path prefix
---

# Initial Traefik

Initialize and configure Traefik v3 reverse proxy with Docker Compose for service routing and load balancing.

## Quick Start

### 1. Create Configuration

```bash
mkdir -p ~/.docker/compose
cd ~/.docker/compose
```

### 2. Create docker-compose.yml

Use `assets/docker-compose.yml` as template. Key configuration:

```yaml
services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik-dynamic.yml:/etc/traefik/dynamic.yml:ro
    command:
      - --api=true
      - --api.dashboard=true
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
      - --providers.file.directory=/etc/traefik
      - --providers.file.watch=true
      - --entrypoints.web.address=:80
      - --accesslog=true
      - --metrics.prometheus=true
```

### 3. Create Dynamic Configuration

Use `assets/traefik-dynamic.yml` as template for service routing.

### 4. Start Traefik

```bash
docker compose up -d
```

### 5. Connect Services to Network

```bash
for container in <service-names>; do
  docker network connect compose_default $container
done
```

## Routing Options

### Option A: Path Prefix Routing (IP + Path)

Access services via `http://<IP>/<service>`:

```yaml
http:
  routers:
    n8n:
      rule: "PathPrefix(`/n8n`)"
      service: n8n
      entryPoints:
        - web
      middlewares:
        - n8n-stripprefix
  
  middlewares:
    n8n-stripprefix:
      stripPrefix:
        prefixes:
          - /n8n
  
  services:
    n8n:
      loadBalancer:
        servers:
          - url: "http://n8n:5678"
```

Access: `http://192.168.9.192/n8n`

### Option B: Host-Based Routing (.nip.io)

Access services via `http://<service>.<IP>.nip.io`:

```yaml
http:
  routers:
    n8n:
      rule: "Host(`n8n.192.168.9.192.nip.io`)"
      service: n8n
      entryPoints:
        - web
  
  services:
    n8n:
      loadBalancer:
        servers:
          - url: "http://n8n:5678"
```

Access: `http://n8n.192.168.9.192.nip.io`

### Option C: Docker Labels

Configure routing directly in docker-compose.yml labels:

```yaml
services:
  traefik:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`traefik.192.168.9.192.nip.io`)"
      - "traefik.http.routers.dashboard.service=api@internal"
      - "traefik.http.routers.dashboard.entrypoints=web"
```

## Enable Features

See `references/features.md` for complete feature list and configuration.

## Common Tasks

### Add New Service

1. Connect container to network:
   ```bash
   docker network connect compose_default <container-name>
   ```

2. Add router to `traefik-dynamic.yml`:
   ```yaml
   routers:
     myservice:
       rule: "PathPrefix(`/myservice`)"
       service: myservice
       entryPoints:
         - web
       middlewares:
         - myservice-stripprefix
   
   services:
     myservice:
       loadBalancer:
         servers:
           - url: "http://<container-name>:<port>"
   ```

Traefik auto-reloads configuration.

### Check Status

```bash
docker logs traefik | grep -E "router|error"
docker exec traefik wget -q -O - http://localhost:8080/api/http/routers
```

### Restart Traefik

```bash
docker restart traefik
```

## References

- **Features**: See `references/features.md` for all available features
- **Examples**: See `references/examples.md` for common configurations
- **Templates**: See `assets/` for configuration templates

## Troubleshooting

- **404 errors**: Check container is connected to `compose_default` network
- **Configuration not loading**: Check `traefik-dynamic.yml` YAML syntax
- **Service not accessible**: Verify container name and port in service configuration
- **Dashboard not working**: Ensure `--api.dashboard=true` is in command
