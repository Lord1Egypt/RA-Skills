# Docker HTTP Static Server

## Nginx (recommended)

```bash
docker run --rm -v "$PWD":/usr/share/nginx/html:ro -p 8000:80 nginx
```

With custom config:

```bash
docker run --rm -v "$PWD":/usr/share/nginx/html:ro -v "$PWD/nginx.conf":/etc/nginx/conf.d/default.conf:ro -p 8000:80 nginx
```

Features:
- Directory listing: Configurable via nginx.conf (`autoindex on;`)
- Production-grade
- No local runtime needed (only Docker)
- Custom configuration support

## PHP

```bash
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp -p 8000:8000 php:8.2-cli php -S 0.0.0.0:8000
```

## Python

```bash
docker run --rm -v "$PWD":/srv -w /srv -p 8000:8000 python:3-slim python -m http.server 8000
```

## Alpine with BusyBox

Ultra-lightweight:

```bash
docker run --rm -v "$PWD":/www -p 8000:8000 alpine sh -c "busybox httpd -f -p 8000 -h /www"
```

## Common Docker options

| Option | Description |
|---|---|
| `--rm` | Remove container when stopped |
| `-d` | Run in background (detached) |
| `-v "$PWD":/path:ro` | Mount current directory read-only |
| `-p 8000:80` | Map host port 8000 to container port 80 |
| `--name myserver` | Name the container for easy management |
