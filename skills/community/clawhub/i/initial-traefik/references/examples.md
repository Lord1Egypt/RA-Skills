# Traefik Configuration Examples

## Example 1: Path Prefix Routing

All services accessible via single IP with different paths.

```yaml
# traefik-dynamic.yml
http:
  routers:
    grafana:
      rule: "PathPrefix(`/grafana`)"
      service: grafana
      entryPoints:
        - web
      middlewares:
        - grafana-stripprefix
    
    n8n:
      rule: "PathPrefix(`/n8n`)"
      service: n8n
      entryPoints:
        - web
      middlewares:
        - n8n-stripprefix
  
  middlewares:
    grafana-stripprefix:
      stripPrefix:
        prefixes:
          - /grafana
    
    n8n-stripprefix:
      stripPrefix:
        prefixes:
          - /n8n
  
  services:
    grafana:
      loadBalancer:
        servers:
          - url: "http://grafana:3000"
        passHostHeader: true
    
    n8n:
      loadBalancer:
        servers:
          - url: "http://n8n:5678"
        passHostHeader: true
```

Access:
- Grafana: `http://192.168.9.192/grafana`
- n8n: `http://192.168.9.192/n8n`

## Example 2: Host-Based Routing with .nip.io

Each service has its own subdomain.

```yaml
http:
  routers:
    grafana:
      rule: "Host(`grafana.192.168.9.192.nip.io`)"
      service: grafana
      entryPoints:
        - web
    
    n8n:
      rule: "Host(`n8n.192.168.9.192.nip.io`)"
      service: n8n
      entryPoints:
        - web
  
  services:
    grafana:
      loadBalancer:
        servers:
          - url: "http://grafana:3000"
    
    n8n:
      loadBalancer:
        servers:
          - url: "http://n8n:5678"
```

Access:
- Grafana: `http://grafana.192.168.9.192.nip.io`
- n8n: `http://n8n.192.168.9.192.nip.io`

## Example 3: Docker Labels Only

No dynamic config file, all routing via labels.

```yaml
# docker-compose.yml
services:
  traefik:
    image: traefik:v3.0
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command:
      - --api=true
      - --providers.docker=true
      - --providers.docker.exposedbydefault=false
    labels:
      # Dashboard
      - "traefik.enable=true"
      - "traefik.http.routers.dashboard.rule=Host(`traefik.192.168.9.192.nip.io`)"
      - "traefik.http.routers.dashboard.service=api@internal"
      - "traefik.http.routers.dashboard.entrypoints=web"
```

Access: `http://traefik.192.168.9.192.nip.io`

## Example 4: Dashboard with Authentication

Secure Traefik dashboard with basic auth.

```yaml
http:
  routers:
    traefik:
      rule: "Host(`traefik.192.168.9.192.nip.io`)"
      service: api@internal
      entryPoints:
        - web
      middlewares:
        - traefik-auth
  
  middlewares:
    traefik-auth:
      basicAuth:
        users:
          - admin:$2y$05$YQ6ZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZ
```

Generate password:
```bash
docker run --rm -it python:3.11-alpine sh -c "pip install passlib && python -c 'from passlib.hash import bcrypt; print(\"admin:\" + bcrypt.hash(\"yourpassword\"))'"
```

## Example 5: HTTPS with Let's Encrypt

Auto-provision TLS certificates.

```yaml
# docker-compose.yml
services:
  traefik:
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - traefik-data:/traefik
    command:
      - --entrypoints.web.address=:80
      - --entrypoints.websecure.address=:443
      - --certificatesresolvers.le.acme.email=admin@example.com
      - --certificatesresolvers.le.acme.storage=/traefik/acme.json
      - --certificatesresolvers.le.acme.tlschallenge=true
      - --entrypoints.websecure.http.tls.certresolver=le
      - --entrypoints.web.http.redirections.entrypoint.to=websecure
      - --entrypoints.web.http.redirections.entrypoint.permanent=true

volumes:
  traefik-data:
```

```yaml
# traefik-dynamic.yml
http:
  routers:
    myservice:
      rule: "Host(`myservice.example.com`)"
      service: myservice
      entryPoints:
        - websecure
      tls: {}
```

## Example 6: Rate Limiting

Protect services from abuse.

```yaml
http:
  routers:
    api:
      rule: "PathPrefix(`/api`)"
      service: api
      entryPoints:
        - web
      middlewares:
        - api-ratelimit
        - api-stripprefix
  
  middlewares:
    api-ratelimit:
      rateLimit:
        average: 100
        burst: 50
        period: 1m
    
    api-stripprefix:
      stripPrefix:
        prefixes:
          - /api
  
  services:
    api:
      loadBalancer:
        servers:
          - url: "http://api:8080"
```

## Example 7: Multiple Backend Servers

Load balance across multiple instances.

```yaml
http:
  services:
    web:
      loadBalancer:
        servers:
          - url: "http://web1:80"
          - url: "http://web2:80"
          - url: "http://web3:80"
        passHostHeader: true
```

## Example 8: Security Headers

Add security headers to all responses.

```yaml
http:
  middlewares:
    security:
      headers:
        frameDeny: true
        stsSeconds: 31536000
        stsIncludeSubdomains: true
        stsPreload: true
        customFrameOptionsValue: SAMEORIGIN
        customResponseHeaders:
          X-Content-Type-Options: nosniff
          X-Frame-Options: DENY
          X-XSS-Protection: 1; mode=block
```

Apply to router:
```yaml
routers:
  myservice:
    middlewares:
      - security
```
