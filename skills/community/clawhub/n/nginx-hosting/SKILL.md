---
name: nginx-hosting
description: >
  Zero-auth static game hosting via the server's local nginx instance.
  Primary deployment method for all browser games. No login, no token,
  no user action required. Serves games at a permanent public HTTPS URL.
---

# nginx-hosting

**Primary deployment method for all games.**

Serves static files directly from the host nginx at:
`https://roger-us02.clawln.net/games/{game-name}/`

## How It Works

nginx is already running on this host with a valid SSL cert for `roger-us02.clawln.net`.
The `/games/` location block is configured to serve files from `/data/games/`.
Deploying a game = copying files + reloading nginx. No external service needed.

## nginx config (already applied)

Location block in `/etc/nginx/conf.d/roger-us02.clawln.net.conf`:

```nginx
location /games/ {
    alias /data/games/;
    index index.html;
    try_files $uri $uri/ $uri/index.html =404;
}
```

## Deploy a game

```bash
# 1. Copy build files
mkdir -p /data/games/{game-name}
cp -r /path/to/build/* /data/games/{game-name}/

# 2. Reload nginx (no downtime)
/usr/sbin/nginx -s reload

# 3. Verify
curl -sk https://roger-us02.clawln.net/games/{game-name}/ | head -3
```

## Update an existing game

Same as deploy — just overwrite the files and reload:

```bash
cp -r /path/to/new-build/* /data/games/{game-name}/
/usr/sbin/nginx -s reload
```

## List deployed games

```bash
ls /data/games/
```

## Base URL

```
https://roger-us02.clawln.net/games/
```

Each game lives at `https://roger-us02.clawln.net/games/{game-name}/`.

## Constraints

- Static files only (HTML, JS, CSS, images, audio)
- No server-side logic or databases
- All games share the same domain and SSL cert
- nginx binary: `/usr/sbin/nginx`
- Games root: `/data/games/`
