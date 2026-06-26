---
name: standalone-setup
description: Deploy a self-hosted Mobazha store on any Linux VPS using Docker. Use when the user wants to set up a standalone store on a server.
requires_credentials: true
credential_types:
  - SSH credentials (IP address and password/key for VPS access, user-provided)
---

# Standalone Store Setup

Deploy a fully independent Mobazha store on any Linux VPS with a single command. Docker-based with automatic updates.

**Official guide**: <https://mobazha.org/self-host>

## Prerequisites

- A Linux VPS (Ubuntu 22.04+ or Debian 12+) with 2+ CPU cores, 2+ GB RAM, 20+ GB SSD
- Root or sudo access
- (Optional) A domain name pointed to the VPS IP

### Recommended VPS Providers

| Provider | Spec | Price |
|----------|------|-------|
| Hetzner | 2 vCPU / 4 GB / 40 GB SSD | ~€4.5/mo |
| Contabo | 4 vCPU / 8 GB / 50 GB SSD | ~€6/mo |
| DigitalOcean | 2 vCPU / 4 GB / 80 GB SSD | ~$24/mo |
| Vultr | 2 vCPU / 4 GB / 80 GB SSD | ~$24/mo |

## Step-by-Step Deployment

### Step 1: Connect to Your VPS

If the user provides an IP and password, connect via SSH:

```bash
ssh root@<IP_ADDRESS>
```

If the user provides an SSH key, use:

```bash
ssh -i <KEY_PATH> root@<IP_ADDRESS>
```

### Step 2: Install the Standalone Store

For a full list of installer flags and post-install file locations, see `references/install-flags.md`.

> **Security note**: The commands below download and execute a shell script from `get.mobazha.org`. Before running, you can review the script by opening the URL in a browser or running `curl -sSL https://get.mobazha.org/standalone | less`. Only proceed if the user confirms they trust the source.

**Zero-config (most common)**:

```bash
curl -sSL https://get.mobazha.org/standalone | sudo bash
```

**With a pre-configured domain** (enables auto-TLS via Let's Encrypt):

```bash
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --domain shop.example.com
```

**Privacy mode with Tor**:

```bash
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --overlay tor
```

**Using testnets** (for trying things out without real money):

```bash
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --testnet
```

Flags can be combined:

```bash
curl -sSL https://get.mobazha.org/standalone | sudo bash -s -- --domain shop.example.com --overlay tor --testnet
```

### Step 3: What Happens During Installation

The installer automatically:

1. Installs Docker if not already present
2. Downloads the Docker Compose configuration to `/opt/mobazha/`
3. Generates a unique API key
4. Starts the Mobazha services (node, frontend, reverse proxy)
5. Sets up a systemd timer for hourly auto-updates
6. Installs the `mobazha-ctl` management CLI to `/usr/local/bin/`

### Step 4: Complete the Store Onboarding

Open the store admin panel in a browser:

- **With domain**: `https://shop.example.com/admin`
- **Without domain**: `http://<VPS_IP>/admin`

On first visit, a **Setup Wizard** appears with 4 steps:

1. **Set admin password** — required before anything else
2. **Store profile** — name, description, avatar
3. **Region and currency** — country and display currency
4. **Done** — dashboard unlocked, next steps suggested

For the full onboarding walkthrough (including API-based setup by AI agents), see the `store-onboarding` skill.

After onboarding, consider connecting your AI agent to the store for hands-free management — see the `store-mcp-connect` skill.

### Step 5: Verify the Installation

```bash
mobazha-ctl status
```

Or check the health endpoint:

```bash
curl -sS http://localhost/healthz
```

## Management Commands

| Command | Description |
|---------|-------------|
| `mobazha-ctl status` | Show service status |
| `mobazha-ctl logs` | View service logs |
| `mobazha-ctl set-domain <domain>` | Add or change the store domain |
| `cd /opt/mobazha && docker compose down` | Stop all services |
| `cd /opt/mobazha && docker compose up -d` | Start all services |
| `cd /opt/mobazha && docker compose pull && docker compose up -d` | Manual update |

## Adding a Domain Later

If you installed without a domain and want to add one:

1. Point your domain's DNS A record to the VPS IP
2. Run: `mobazha-ctl set-domain shop.example.com`
3. The store will automatically obtain a TLS certificate

## Enabling Privacy Overlay Later

You can enable Tor or Lokinet after installation from **Admin → System → Network** in the store dashboard, without re-installing.

## Backup and Restore

Store data lives in `/opt/mobazha/data/`. To back up:

```bash
cd /opt/mobazha && docker compose down
tar czf ~/mobazha-backup-$(date +%Y%m%d).tar.gz data/
docker compose up -d
```

## Troubleshooting

### Port 80/443 already in use

Stop existing web servers (Apache, Nginx) before installing:

```bash
systemctl stop nginx apache2 2>/dev/null; true
```

### Firewall blocking ports

Allow HTTP/HTTPS traffic:

```bash
ufw allow 80/tcp && ufw allow 443/tcp
```

Or with firewalld:

```bash
firewall-cmd --permanent --add-service=http --add-service=https && firewall-cmd --reload
```

### Check container logs

```bash
cd /opt/mobazha && docker compose logs -f
```

## Credential Handling

If the user provides a VPS IP and root password:

1. **Ask for explicit confirmation** before connecting to the VPS via SSH
2. Use SSH to connect to the VPS
3. Run the installation command
4. Report the store URL back to the user
5. Remind the user to change the default SSH password for security

**Never store or log credentials.** After the session, credentials are not retained. The agent must not transmit credentials to any third party or persist them beyond the immediate command execution.
