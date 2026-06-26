# Ansible

Source: https://docs.openclaw.ai/install/ansible

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationOther install methodsAnsibleGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
InstallInstaller Internals
Other install methods
DockerPodmanNixAnsibleBun (Experimental)
Maintenance
UpdatingMigration GuideUninstall
Hosting and deployment
Fly.ioHetznerGCPmacOS VMsexe.devDeploy on RailwayDeploy on RenderDeploy on Northflank
Advanced
Development Channels
On this page
- [Ansible Installation](#ansible-installation)
- [Quick Start](#quick-start)
- [What You Get](#what-you-get)
- [Requirements](#requirements)
- [What Gets Installed](#what-gets-installed)
- [Post-Install Setup](#post-install-setup)
- [Quick commands](#quick-commands)
- [Security Architecture](#security-architecture)
- [4-Layer Defense](#4-layer-defense)
- [Verification](#verification)
- [Docker Availability](#docker-availability)
- [Manual Installation](#manual-installation)
- [Updating OpenClaw](#updating-openclaw)
- [Troubleshooting](#troubleshooting)
- [Firewall blocks my connection](#firewall-blocks-my-connection)
- [Service won’t start](#service-won%E2%80%99t-start)
- [Docker sandbox issues](#docker-sandbox-issues)
- [Provider login fails](#provider-login-fails)
- [Advanced Configuration](#advanced-configuration)
- [Related](#related)

​Ansible Installation
The recommended way to deploy OpenClaw to production servers is via **[openclaw-ansible](https://github.com/openclaw/openclaw-ansible)** — an automated installer with security-first architecture.
​Quick Start
One-command install:
Copy```
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw-ansible/main/install.sh | bash

```

**📦 Full guide: [github.com/openclaw/openclaw-ansible](https://github.com/openclaw/openclaw-ansible)**
The openclaw-ansible repo is the source of truth for Ansible deployment. This page is a quick overview.

​What You Get

- 🔒 **Firewall-first security**: UFW + Docker isolation (only SSH + Tailscale accessible)

- 🔐 **Tailscale VPN**: Secure remote access without exposing services publicly

- 🐳 **Docker**: Isolated sandbox containers, localhost-only bindings

- 🛡️ **Defense in depth**: 4-layer security architecture

- 🚀 **One-command setup**: Complete deployment in minutes

- 🔧 **Systemd integration**: Auto-start on boot with hardening

​Requirements

- **OS**: Debian 11+ or Ubuntu 20.04+

- **Access**: Root or sudo privileges

- **Network**: Internet connection for package installation

- **Ansible**: 2.14+ (installed automatically by quick-start script)

​What Gets Installed
The Ansible playbook installs and configures:

- **Tailscale** (mesh VPN for secure remote access)

- **UFW firewall** (SSH + Tailscale ports only)

- **Docker CE + Compose V2** (for agent sandboxes)

- **Node.js 22.x + pnpm** (runtime dependencies)

- **OpenClaw** (host-based, not containerized)

- **Systemd service** (auto-start with security hardening)

Note: The gateway runs **directly on the host** (not in Docker), but agent sandboxes use Docker for isolation. See [Sandboxing](/gateway/sandboxing) for details.
​Post-Install Setup
After installation completes, switch to the openclaw user:
Copy```
sudo -i -u openclaw

```

The post-install script will guide you through:

- **Onboarding wizard**: Configure OpenClaw settings

- **Provider login**: Connect WhatsApp/Telegram/Discord/Signal

- **Gateway testing**: Verify the installation

- **Tailscale setup**: Connect to your VPN mesh

​Quick commands
Copy```
# Check service status
sudo systemctl status openclaw

# View live logs
sudo journalctl -u openclaw -f

# Restart gateway
sudo systemctl restart openclaw

# Provider login (run as openclaw user)
sudo -i -u openclaw
openclaw channels login

```

​Security Architecture
​4-Layer Defense

- **Firewall (UFW)**: Only SSH (22) + Tailscale (41641/udp) exposed publicly

- **VPN (Tailscale)**: Gateway accessible only via VPN mesh

- **Docker Isolation**: DOCKER-USER iptables chain prevents external port exposure

- **Systemd Hardening**: NoNewPrivileges, PrivateTmp, unprivileged user

​Verification
Test external attack surface:
Copy```
nmap -p- YOUR_SERVER_IP

```

Should show **only port 22** (SSH) open. All other services (gateway, Docker) are locked down.
​Docker Availability
Docker is installed for **agent sandboxes** (isolated tool execution), not for running the gateway itself. The gateway binds to localhost only and is accessible via Tailscale VPN.
See [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) for sandbox configuration.
​Manual Installation
If you prefer manual control over the automation:
Copy```
# 1. Install prerequisites
sudo apt update && sudo apt install -y ansible git

# 2. Clone repository
git clone https://github.com/openclaw/openclaw-ansible.git
cd openclaw-ansible

# 3. Install Ansible collections
ansible-galaxy collection install -r requirements.yml

# 4. Run playbook
./run-playbook.sh

# Or run directly (then manually execute /tmp/openclaw-setup.sh after)
# ansible-playbook playbook.yml --ask-become-pass

```

​Updating OpenClaw
The Ansible installer sets up OpenClaw for manual updates. See [Updating](/install/updating) for the standard update flow.
To re-run the Ansible playbook (e.g., for configuration changes):
Copy```
cd openclaw-ansible
./run-playbook.sh

```

Note: This is idempotent and safe to run multiple times.
​Troubleshooting
​Firewall blocks my connection
If you’re locked out:

- Ensure you can access via Tailscale VPN first

- SSH access (port 22) is always allowed

- The gateway is **only** accessible via Tailscale by design

​Service won’t start
Copy```
# Check logs
sudo journalctl -u openclaw -n 100

# Verify permissions
sudo ls -la /opt/openclaw

# Test manual start
sudo -i -u openclaw
cd ~/openclaw
pnpm start

```

​Docker sandbox issues
Copy```
# Verify Docker is running
sudo systemctl status docker

# Check sandbox image
sudo docker images | grep openclaw-sandbox

# Build sandbox image if missing
cd /opt/openclaw/openclaw
sudo -u openclaw ./scripts/sandbox-setup.sh

```

​Provider login fails
Make sure you’re running as the `openclaw` user:
Copy```
sudo -i -u openclaw
openclaw channels login

```

​Advanced Configuration
For detailed security architecture and troubleshooting:

- [Security Architecture](https://github.com/openclaw/openclaw-ansible/blob/main/docs/security.md)

- [Technical Details](https://github.com/openclaw/openclaw-ansible/blob/main/docs/architecture.md)

- [Troubleshooting Guide](https://github.com/openclaw/openclaw-ansible/blob/main/docs/troubleshooting.md)

​Related

- [openclaw-ansible](https://github.com/openclaw/openclaw-ansible) — full deployment guide

- [Docker](/install/docker) — containerized gateway setup

- [Sandboxing](/gateway/sandboxing) — agent sandbox configuration

- [Multi-Agent Sandbox & Tools](/tools/multi-agent-sandbox-tools) — per-agent isolation

NixBun (Experimental)⌘I