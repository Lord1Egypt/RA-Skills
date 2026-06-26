# Traefik Features

## Core Features

### API & Dashboard

```yaml
command:
  - --api=true
  - --api.dashboard=true
  - --api.insecure=true  # Enable insecure access (for dev only)
```

Access: `http://<IP>/traefik` or configured host

### Docker Provider

```yaml
command:
  - --providers.docker=true
  - --providers.docker.exposedbydefault=false  # Only expose labeled containers
  - --providers.docker.network=compose_default  # Use specific network
```

### File Provider

```yaml
command:
  - --providers.file.directory=/etc/traefik
  - --providers.file.watch=true  # Auto-reload on file changes
```

### EntryPoints

```yaml
command:
  - --entrypoints.web.address=:80
  - --entrypoints.websecure.address=:443
```

## Logging & Monitoring

### Access Log

```yaml
command:
  - --accesslog=true
  - --accesslog.format=json
  - --accesslog.filters.statuscodes=200-299,400-499  # Filter status codes
```

View: `docker logs traefik`

### Traefik Log

```yaml
command:
  - --log.level=DEBUG  # DEBUG, INFO, WARN, ERROR
  - --log.format=json  # json or common
```

### Prometheus Metrics

```yaml
command:
  - --metrics.prometheus=true
  - --metrics.prometheus.buckets=0.1,0.3,1.2,5.0
```

Access: `http://<IP>/traefik/metrics`

## Tracing

### Jaeger Tracing

```yaml
command:
  - --tracing.jaeger=true
  - --tracing.jaeger.address=127.0.0.1:6831
  - --tracing.jaeger.serviceName=traefik
  - --tracing.jaeger.samplingServerURL=http://127.0.0.1:5778/sampling
  - --tracing.jaeger.samplingType=const
  - --tracing.jaeger.samplingParam=1.0
```

### Zipkin Tracing

```yaml
command:
  - --tracing.zipkin=true
  - --tracing.zipkin.address=http://127.0.0.1:9411/api/v2/spans
```

### OTLP Tracing

```yaml
command:
  - --tracing.otlp=true
  - --tracing.otlp.address=127.0.0.1:4317
  - --tracing.otlp.insecure=true
```

## Global Settings

```yaml
command:
  - --global.checknewversion=false  # Disable version check
  - --global.sendanonymoususage=false  # Disable analytics
```

## TLS/HTTPS

### Let's Encrypt Auto-Certificates

```yaml
command:
  - --certificatesresolvers.le.acme.email=admin@example.com
  - --certificatesresolvers.le.acme.storage=/traefik/acme.json
  - --certificatesresolvers.le.acme.tlschallenge=true
  - --entrypoints.websecure.http.tls.certresolver=le
```

### Redirect HTTP to HTTPS

```yaml
http:
  routers:
    redirect:
      rule: "HostRegexp(`{host:.+}`)"
      entryPoints:
        - web
      middlewares:
        - redirect-to-https
  
  middlewares:
    redirect-to-https:
      redirectScheme:
        scheme: https
        permanent: true
```

## Middlewares

### Rate Limiting

```yaml
http:
  middlewares:
    ratelimit:
      rateLimit:
        average: 100
        burst: 50
```

### Basic Auth

```yaml
http:
  middlewares:
    auth:
      basicAuth:
        users:
          - admin:$2y$05$YQ6ZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZkZ
```

Generate password: `htpasswd -nb admin password`

### Headers

```yaml
http:
  middlewares:
    security-headers:
      headers:
        frameDeny: true
        stsSeconds: 31536000
        stsIncludeSubdomains: true
        stsPreload: true
        customFrameOptionsValue: SAMEORIGIN
```

### Compression

```yaml
http:
  middlewares:
    compress:
      compress: {}
```

## Load Balancing

### Round Robin (Default)

```yaml
http:
  services:
    myservice:
      loadBalancer:
        servers:
          - url: "http://server1:8080"
          - url: "http://server2:8080"
        passHostHeader: true
```

### Sticky Sessions

```yaml
http:
  services:
    myservice:
      loadBalancer:
        servers:
          - url: "http://server1:8080"
          - url: "http://server2:8080"
        sticky:
          cookie:
            name: TRAEFIK_SB
            httpOnly: true
            secure: true
```
