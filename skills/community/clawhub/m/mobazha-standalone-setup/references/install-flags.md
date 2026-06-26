# Standalone Installer Flags Reference

Source: `curl -sSL https://get.mobazha.org/standalone | sudo bash [options]`

## Available Flags

| Flag | Value | Default | Description |
|------|-------|---------|-------------|
| `--domain` | `<domain>` | (none) | Pre-configure domain for auto-TLS via Let's Encrypt |
| `--overlay` | `tor` or `lokinet` | (none) | Enable privacy overlay network |
| `--saas-url` | `<url>` | `https://app.mobazha.org` | Override SaaS API URL |
| `--testnet` | (flag) | disabled | Use cryptocurrency testnets |
| `--help` | (flag) | — | Show help message |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `INSTALL_DIR` | `/opt/mobazha` | Installation directory |
| `SAAS_API_URL` | `https://app.mobazha.org` | SaaS API URL |

## Examples

```bash
# Basic install — HTTP on IP
curl -sSL https://get.mobazha.org/standalone | sudo bash

# With domain — HTTPS auto-TLS
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --domain shop.example.com

# Privacy mode
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --overlay tor

# Combined
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --domain shop.example.com --overlay tor --testnet

# Custom install directory
INSTALL_DIR=/srv/mobazha curl -sSL https://get.mobazha.org/standalone | sudo bash
```

## Post-Install Locations

| Path | Purpose |
|------|---------|
| `/opt/mobazha/` | Main install directory |
| `/opt/mobazha/.env` | Configuration (chmod 600) |
| `/opt/mobazha/docker-compose.yml` | Docker Compose config |
| `/opt/mobazha/data/` | Persistent store data |
| `/usr/local/bin/mobazha-ctl` | Management CLI |
| `/etc/systemd/system/mobazha-update.timer` | Auto-update timer |
