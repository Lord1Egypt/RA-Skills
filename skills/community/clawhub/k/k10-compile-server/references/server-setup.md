# Server Setup Guide

Deploy your own K10 Compile Server.

## Requirements

| Component | Version / Notes |
|-----------|----------------|
| Python | 3.10+ |
| PlatformIO Core | `pip install platformio` |
| DFRobot UniHiker K10 Arduino | `pio platform install https://github.com/DFRobot/platform-unihiker.git` |
| OpenSSL | For self-signed HTTPS cert (Web Serial requires HTTPS) |
| Docker + Compose | Optional, for containerized deployment |
| curl, zip, unzip | Optional, for CLI usage |
| esptool | `pip install esptool` — only needed for server-side flashing |

## Quick Start (Docker — Recommended)

```bash
cd server/

# Generate self-signed certificate (first time only)
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem \
  -days 3650 -nodes -subj "/CN=K10 Compile Server"

# Start server
docker compose up -d --build

# Verify
curl -sk https://localhost:8900/api/health
```

## Quick Start (Native / systemd)

```bash
cd server/
bash install.sh
# Select option [1] systemd
```

The script will:
1. Check Python 3.10+
2. Install PlatformIO + UniHiker K10 platform
3. Install Python dependencies
4. Generate self-signed HTTPS cert
5. Install systemd service and start it

## Post-Installation

Verify the server is working:

```bash
# Health check
curl -sk https://localhost:8900/api/health

# Compile Blink example
bash k10-compile-server/scripts/compile-project.sh \
  --server https://localhost:8900 \
  --dir examples/Blink \
  --wait

# Open Web Serial flash page
bash k10-compile-server/scripts/compile-project.sh \
  --server https://localhost:8900 \
  --dir examples/Blink \
  --wait --web-serial
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `K10_COMPILE_HOST` | `0.0.0.0` | Bind address |
| `K10_COMPILE_PORT` | `8900` | Server port |
| `K10_STATIC_DIR` | `./static` | Web Serial JS files |
| `K10_SSL_CERT` | `./cert.pem` | HTTPS cert path |
| `K10_SSL_KEY` | `./key.pem` | HTTPS key path |
| `K10_REDIRECT_PORT` | `8080` | HTTP→HTTPS redirect port |
| `K10_COMPILE_TIMEOUT` | `300` | Compile timeout (seconds) |
| `K10_MAX_CONCURRENT` | `2` | Max parallel compilations |
| `K10_BUILD_TTL` | `1800` | How long build results are kept (seconds) |

### PlatformIO Cache

PlatformIO downloads toolchains to `~/.platformio`. Docker persists this
directory in the named volume `pio-data`, so `docker compose down && docker
compose up -d` keeps the downloaded K10 toolchain. A brand-new volume may need
to download toolchains on the first compile.

For native installs, PlatformIO manages this automatically.

## Docker Production Tips

```bash
# Map PlatformIO cache from a host directory (faster than docker volume)
docker compose run -d --build \
  -v /opt/platformio:/root/.platformio \
  ...

# Use a real certificate instead of self-signed
# Mount cert.pem and key.pem, or use a reverse proxy (nginx/caddy)
```

## HTTPS Without a Real Certificate

Web Serial **requires HTTPS**. For LAN use, self-signed is fine:

1. Visit `https://<server-ip>:8900` in Chrome/Edge
2. Click **Advanced → Proceed to site** (or type `thisisunsafe` on the error page)

For a trusted cert on LAN, consider:
- [mkcert](https://github.com/FiloSottile/mkcert) — create locally-trusted CAs
- [Caddy](https://caddyserver.com/) — automatic HTTPS via reverse proxy
- Let's Encrypt with a real domain + DNS

## Security

> ⚠️ **This server has no authentication. Do not expose to the public internet.**

Safe access methods:
- **LAN**: Direct connection within your local network
- **VPN**: Tailscale, WireGuard, or ZeroTier
- **SSH tunnel**: `ssh -L 8900:localhost:8900 user@server`
- **Reverse proxy**: Add nginx + HTTP Basic Auth / OAuth

If you must expose it publicly, put it behind a reverse proxy with:
- Authentication (OAuth2, Basic Auth, or SSO)
- Rate limiting
- HTTPS with a real certificate (Let's Encrypt)
