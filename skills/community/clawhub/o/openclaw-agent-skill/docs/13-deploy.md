# Deploy & Cloud Hosting

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 12

---

<!-- SOURCE: https://docs.openclaw.ai/install/hetzner -->

# Hetzner - OpenClaw

## OpenClaw on Hetzner (Docker, Production VPS Guide)

## Goal

Run a persistent OpenClaw Gateway on a Hetzner VPS using Docker, with durable state, baked-in binaries, and safe restart behavior. If you want “OpenClaw 24/7 for ~$5”, this is the simplest reliable setup. Hetzner pricing changes; pick the smallest Debian/Ubuntu VPS and scale up if you hit OOMs. Security model reminder:

*   Company-shared agents are fine when everyone is in the same trust boundary and the runtime is business-only.
*   Keep strict separation: dedicated VPS/runtime + dedicated accounts; no personal Apple/Google/browser/password-manager profiles on that host.
*   If users are adversarial to each other, split by gateway/host/OS user.

See [Security](https://docs.openclaw.ai/gateway/security) and [VPS hosting](https://docs.openclaw.ai/vps).

## What are we doing (simple terms)?

*   Rent a small Linux server (Hetzner VPS)
*   Install Docker (isolated app runtime)
*   Start the OpenClaw Gateway in Docker
*   Persist `~/.openclaw` + `~/.openclaw/workspace` on the host (survives restarts/rebuilds)
*   Access the Control UI from your laptop via an SSH tunnel

The Gateway can be accessed via:

*   SSH port forwarding from your laptop
*   Direct port exposure if you manage firewalling and tokens yourself

This guide assumes Ubuntu or Debian on Hetzner.  
If you are on another Linux VPS, map packages accordingly. For the generic Docker flow, see [Docker](https://docs.openclaw.ai/install/docker).

* * *

## Quick path (experienced operators)

1.  Provision Hetzner VPS
2.  Install Docker
3.  Clone OpenClaw repository
4.  Create persistent host directories
5.  Configure `.env` and `docker-compose.yml`
6.  Bake required binaries into the image
7.  `docker compose up -d`
8.  Verify persistence and Gateway access

* * *

## What you need

*   Hetzner VPS with root access
*   SSH access from your laptop
*   Basic comfort with SSH + copy/paste
*   ~20 minutes
*   Docker and Docker Compose
*   Model auth credentials
*   Optional provider credentials
    *   WhatsApp QR
    *   Telegram bot token
    *   Gmail OAuth

* * *

## 1) Provision the VPS

Create an Ubuntu or Debian VPS in Hetzner. Connect as root:

This guide assumes the VPS is stateful. Do not treat it as disposable infrastructure.

* * *

## 2) Install Docker (on the VPS)

```
apt-get update
apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sh
```

Verify:

```
docker --version
docker compose version
```

* * *

## 3) Clone the OpenClaw repository

```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

This guide assumes you will build a custom image to guarantee binary persistence.

* * *

## 4) Create persistent host directories

Docker containers are ephemeral. All long-lived state must live on the host.

```
mkdir -p /root/.openclaw/workspace

# Set ownership to the container user (uid 1000):
chown -R 1000:1000 /root/.openclaw
```

* * *

## 5) Configure environment variables

Create `.env` in the repository root.

```
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/root/.openclaw
OPENCLAW_WORKSPACE_DIR=/root/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

Generate strong secrets:

**Do not commit this file.**

* * *

## 6) Docker Compose configuration

Create or update `docker-compose.yml`.

```
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE}
    build: .
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - HOME=/home/node
      - NODE_ENV=production
      - TERM=xterm-256color
      - OPENCLAW_GATEWAY_BIND=${OPENCLAW_GATEWAY_BIND}
      - OPENCLAW_GATEWAY_PORT=${OPENCLAW_GATEWAY_PORT}
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - GOG_KEYRING_PASSWORD=${GOG_KEYRING_PASSWORD}
      - XDG_CONFIG_HOME=${XDG_CONFIG_HOME}
      - PATH=/home/linuxbrew/.linuxbrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    volumes:
      - ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace
    ports:
      # Recommended: keep the Gateway loopback-only on the VPS; access via SSH tunnel.
      # To expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"
    command:
      [
        "node",
        "dist/index.js",
        "gateway",
        "--bind",
        "${OPENCLAW_GATEWAY_BIND}",
        "--port",
        "${OPENCLAW_GATEWAY_PORT}",
        "--allow-unconfigured",
      ]
```

`--allow-unconfigured` is only for bootstrap convenience, it is not a replacement for a proper gateway configuration. Still set auth (`gateway.auth.token` or password) and use safe bind settings for your deployment.

* * *

## 7) Bake required binaries into the image (critical)

Installing binaries inside a running container is a trap. Anything installed at runtime will be lost on restart. All external binaries required by skills must be installed at image build time. The examples below show three common binaries only:

*   `gog` for Gmail access
*   `goplaces` for Google Places
*   `wacli` for WhatsApp

These are examples, not a complete list. You may install as many binaries as needed using the same pattern. If you add new skills later that depend on additional binaries, you must:

1.  Update the Dockerfile
2.  Rebuild the image
3.  Restart the containers

**Example Dockerfile**

```
FROM node:22-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Example binary 1: Gmail CLI
RUN curl -L https://github.com/steipete/gog/releases/latest/download/gog_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/gog

# Example binary 2: Google Places CLI
RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/goplaces

# Example binary 3: WhatsApp CLI
RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/wacli

# Add more binaries below using the same pattern

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

* * *

## 8) Build and launch

```
docker compose build
docker compose up -d openclaw-gateway
```

Verify binaries:

```
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

Expected output:

```
/usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli
```

* * *

## 9) Verify Gateway

```
docker compose logs -f openclaw-gateway
```

Success:

```
[gateway] listening on ws://0.0.0.0:18789
```

From your laptop:

```
ssh -N -L 18789:127.0.0.1:18789 root@YOUR_VPS_IP
```

Open: `http://127.0.0.1:18789/` Paste your gateway token.

* * *

## What persists where (source of truth)

OpenClaw runs in Docker, but Docker is not the source of truth. All long-lived state must survive restarts, rebuilds, and reboots.

| Component | Location | Persistence mechanism | Notes |
| --- | --- | --- | --- |
| Gateway config | `/home/node/.openclaw/` | Host volume mount | Includes `openclaw.json`, tokens |
| Model auth profiles | `/home/node/.openclaw/` | Host volume mount | OAuth tokens, API keys |
| Skill configs | `/home/node/.openclaw/skills/` | Host volume mount | Skill-level state |
| Agent workspace | `/home/node/.openclaw/workspace/` | Host volume mount | Code and agent artifacts |
| WhatsApp session | `/home/node/.openclaw/` | Host volume mount | Preserves QR login |
| Gmail keyring | `/home/node/.openclaw/` | Host volume + password | Requires `GOG_KEYRING_PASSWORD` |
| External binaries | `/usr/local/bin/` | Docker image | Must be baked at build time |
| Node runtime | Container filesystem | Docker image | Rebuilt every image build |
| OS packages | Container filesystem | Docker image | Do not install at runtime |
| Docker container | Ephemeral | Restartable | Safe to destroy |

* * *

## Infrastructure as Code (Terraform)

For teams preferring infrastructure-as-code workflows, a community-maintained Terraform setup provides:

*   Modular Terraform configuration with remote state management
*   Automated provisioning via cloud-init
*   Deployment scripts (bootstrap, deploy, backup/restore)
*   Security hardening (firewall, UFW, SSH-only access)
*   SSH tunnel configuration for gateway access

**Repositories:**

*   Infrastructure: [openclaw-terraform-hetzner](https://github.com/andreesg/openclaw-terraform-hetzner)
*   Docker config: [openclaw-docker-config](https://github.com/andreesg/openclaw-docker-config)

This approach complements the Docker setup above with reproducible deployments, version-controlled infrastructure, and automated disaster recovery.

> **Note:** Community-maintained. For issues or contributions, see the repository links above.

---

<!-- SOURCE: https://docs.openclaw.ai/install/gcp -->

# GCP - OpenClaw

## OpenClaw on GCP Compute Engine (Docker, Production VPS Guide)

## Goal

Run a persistent OpenClaw Gateway on a GCP Compute Engine VM using Docker, with durable state, baked-in binaries, and safe restart behavior. If you want “OpenClaw 24/7 for ~$5-12/mo”, this is a reliable setup on Google Cloud. Pricing varies by machine type and region; pick the smallest VM that fits your workload and scale up if you hit OOMs.

## What are we doing (simple terms)?

*   Create a GCP project and enable billing
*   Create a Compute Engine VM
*   Install Docker (isolated app runtime)
*   Start the OpenClaw Gateway in Docker
*   Persist `~/.openclaw` + `~/.openclaw/workspace` on the host (survives restarts/rebuilds)
*   Access the Control UI from your laptop via an SSH tunnel

The Gateway can be accessed via:

*   SSH port forwarding from your laptop
*   Direct port exposure if you manage firewalling and tokens yourself

This guide uses Debian on GCP Compute Engine. Ubuntu also works; map packages accordingly. For the generic Docker flow, see [Docker](https://docs.openclaw.ai/install/docker).

* * *

## Quick path (experienced operators)

1.  Create GCP project + enable Compute Engine API
2.  Create Compute Engine VM (e2-small, Debian 12, 20GB)
3.  SSH into the VM
4.  Install Docker
5.  Clone OpenClaw repository
6.  Create persistent host directories
7.  Configure `.env` and `docker-compose.yml`
8.  Bake required binaries, build, and launch

* * *

## What you need

*   GCP account (free tier eligible for e2-micro)
*   gcloud CLI installed (or use Cloud Console)
*   SSH access from your laptop
*   Basic comfort with SSH + copy/paste
*   ~20-30 minutes
*   Docker and Docker Compose
*   Model auth credentials
*   Optional provider credentials
    *   WhatsApp QR
    *   Telegram bot token
    *   Gmail OAuth

* * *

## 1) Install gcloud CLI (or use Console)

**Option A: gcloud CLI** (recommended for automation) Install from [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install) Initialize and authenticate:

```
gcloud init
gcloud auth login
```

**Option B: Cloud Console** All steps can be done via the web UI at [https://console.cloud.google.com](https://console.cloud.google.com/)

* * *

## 2) Create a GCP project

**CLI:**

```
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project
```

Enable billing at [https://console.cloud.google.com/billing](https://console.cloud.google.com/billing) (required for Compute Engine). Enable the Compute Engine API:

```
gcloud services enable compute.googleapis.com
```

**Console:**

1.  Go to IAM & Admin > Create Project
2.  Name it and create
3.  Enable billing for the project
4.  Navigate to APIs & Services > Enable APIs > search “Compute Engine API” > Enable

* * *

## 3) Create the VM

**Machine types:**

| Type | Specs | Cost | Notes |
| --- | --- | --- | --- |
| e2-medium | 2 vCPU, 4GB RAM | ~$25/mo | Most reliable for local Docker builds |
| e2-small | 2 vCPU, 2GB RAM | ~$12/mo | Minimum recommended for Docker build |
| e2-micro | 2 vCPU (shared), 1GB RAM | Free tier eligible | Often fails with Docker build OOM (exit 137) |

**CLI:**

```
gcloud compute instances create openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud
```

**Console:**

1.  Go to Compute Engine > VM instances > Create instance
2.  Name: `openclaw-gateway`
3.  Region: `us-central1`, Zone: `us-central1-a`
4.  Machine type: `e2-small`
5.  Boot disk: Debian 12, 20GB
6.  Create

* * *

## 4) SSH into the VM

**CLI:**

```
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

**Console:** Click the “SSH” button next to your VM in the Compute Engine dashboard. Note: SSH key propagation can take 1-2 minutes after VM creation. If connection is refused, wait and retry.

* * *

## 5) Install Docker (on the VM)

```
sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

Log out and back in for the group change to take effect:

Then SSH back in:

```
gcloud compute ssh openclaw-gateway --zone=us-central1-a
```

Verify:

```
docker --version
docker compose version
```

* * *

## 6) Clone the OpenClaw repository

```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

This guide assumes you will build a custom image to guarantee binary persistence.

* * *

## 7) Create persistent host directories

Docker containers are ephemeral. All long-lived state must live on the host.

```
mkdir -p ~/.openclaw
mkdir -p ~/.openclaw/workspace
```

* * *

## 8) Configure environment variables

Create `.env` in the repository root.

```
OPENCLAW_IMAGE=openclaw:latest
OPENCLAW_GATEWAY_TOKEN=change-me-now
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_PORT=18789

OPENCLAW_CONFIG_DIR=/home/$USER/.openclaw
OPENCLAW_WORKSPACE_DIR=/home/$USER/.openclaw/workspace

GOG_KEYRING_PASSWORD=change-me-now
XDG_CONFIG_HOME=/home/node/.openclaw
```

Generate strong secrets:

**Do not commit this file.**

* * *

## 9) Docker Compose configuration

Create or update `docker-compose.yml`.

```
services:
  openclaw-gateway:
    image: ${OPENCLAW_IMAGE}
    build: .
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - HOME=/home/node
      - NODE_ENV=production
      - TERM=xterm-256color
      - OPENCLAW_GATEWAY_BIND=${OPENCLAW_GATEWAY_BIND}
      - OPENCLAW_GATEWAY_PORT=${OPENCLAW_GATEWAY_PORT}
      - OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN}
      - GOG_KEYRING_PASSWORD=${GOG_KEYRING_PASSWORD}
      - XDG_CONFIG_HOME=${XDG_CONFIG_HOME}
      - PATH=/home/linuxbrew/.linuxbrew/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    volumes:
      - ${OPENCLAW_CONFIG_DIR}:/home/node/.openclaw
      - ${OPENCLAW_WORKSPACE_DIR}:/home/node/.openclaw/workspace
    ports:
      # Recommended: keep the Gateway loopback-only on the VM; access via SSH tunnel.
      # To expose it publicly, remove the `127.0.0.1:` prefix and firewall accordingly.
      - "127.0.0.1:${OPENCLAW_GATEWAY_PORT}:18789"
    command:
      [
        "node",
        "dist/index.js",
        "gateway",
        "--bind",
        "${OPENCLAW_GATEWAY_BIND}",
        "--port",
        "${OPENCLAW_GATEWAY_PORT}",
      ]
```

* * *

## 10) Bake required binaries into the image (critical)

Installing binaries inside a running container is a trap. Anything installed at runtime will be lost on restart. All external binaries required by skills must be installed at image build time. The examples below show three common binaries only:

*   `gog` for Gmail access
*   `goplaces` for Google Places
*   `wacli` for WhatsApp

These are examples, not a complete list. You may install as many binaries as needed using the same pattern. If you add new skills later that depend on additional binaries, you must:

1.  Update the Dockerfile
2.  Rebuild the image
3.  Restart the containers

**Example Dockerfile**

```
FROM node:22-bookworm

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

# Example binary 1: Gmail CLI
RUN curl -L https://github.com/steipete/gog/releases/latest/download/gog_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/gog

# Example binary 2: Google Places CLI
RUN curl -L https://github.com/steipete/goplaces/releases/latest/download/goplaces_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/goplaces

# Example binary 3: WhatsApp CLI
RUN curl -L https://github.com/steipete/wacli/releases/latest/download/wacli_Linux_x86_64.tar.gz \
  | tar -xz -C /usr/local/bin && chmod +x /usr/local/bin/wacli

# Add more binaries below using the same pattern

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY scripts ./scripts

RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build
RUN pnpm ui:install
RUN pnpm ui:build

ENV NODE_ENV=production

CMD ["node","dist/index.js"]
```

* * *

## 11) Build and launch

```
docker compose build
docker compose up -d openclaw-gateway
```

If build fails with `Killed` / `exit code 137` during `pnpm install --frozen-lockfile`, the VM is out of memory. Use `e2-small` minimum, or `e2-medium` for more reliable first builds. When binding to LAN (`OPENCLAW_GATEWAY_BIND=lan`), configure a trusted browser origin before continuing:

```
docker compose run --rm openclaw-cli config set gateway.controlUi.allowedOrigins '["http://127.0.0.1:18789"]' --strict-json
```

If you changed the gateway port, replace `18789` with your configured port. Verify binaries:

```
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli
```

Expected output:

```
/usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli
```

* * *

## 12) Verify Gateway

```
docker compose logs -f openclaw-gateway
```

Success:

```
[gateway] listening on ws://0.0.0.0:18789
```

* * *

## 13) Access from your laptop

Create an SSH tunnel to forward the Gateway port:

```
gcloud compute ssh openclaw-gateway --zone=us-central1-a -- -L 18789:127.0.0.1:18789
```

Open in your browser: `http://127.0.0.1:18789/` Fetch a fresh tokenized dashboard link:

```
docker compose run --rm openclaw-cli dashboard --no-open
```

Paste the token from that URL. If Control UI shows `unauthorized` or `disconnected (1008): pairing required`, approve the browser device:

```
docker compose run --rm openclaw-cli devices list
docker compose run --rm openclaw-cli devices approve <requestId>
```

* * *

## What persists where (source of truth)

OpenClaw runs in Docker, but Docker is not the source of truth. All long-lived state must survive restarts, rebuilds, and reboots.

| Component | Location | Persistence mechanism | Notes |
| --- | --- | --- | --- |
| Gateway config | `/home/node/.openclaw/` | Host volume mount | Includes `openclaw.json`, tokens |
| Model auth profiles | `/home/node/.openclaw/` | Host volume mount | OAuth tokens, API keys |
| Skill configs | `/home/node/.openclaw/skills/` | Host volume mount | Skill-level state |
| Agent workspace | `/home/node/.openclaw/workspace/` | Host volume mount | Code and agent artifacts |
| WhatsApp session | `/home/node/.openclaw/` | Host volume mount | Preserves QR login |
| Gmail keyring | `/home/node/.openclaw/` | Host volume + password | Requires `GOG_KEYRING_PASSWORD` |
| External binaries | `/usr/local/bin/` | Docker image | Must be baked at build time |
| Node runtime | Container filesystem | Docker image | Rebuilt every image build |
| OS packages | Container filesystem | Docker image | Do not install at runtime |
| Docker container | Ephemeral | Restartable | Safe to destroy |

* * *

## Updates

To update OpenClaw on the VM:

```
cd ~/openclaw
git pull
docker compose build
docker compose up -d
```

* * *

## Troubleshooting

**SSH connection refused** SSH key propagation can take 1-2 minutes after VM creation. Wait and retry. **OS Login issues** Check your OS Login profile:

```
gcloud compute os-login describe-profile
```

Ensure your account has the required IAM permissions (Compute OS Login or Compute OS Admin Login). **Out of memory (OOM)** If Docker build fails with `Killed` and `exit code 137`, the VM was OOM-killed. Upgrade to e2-small (minimum) or e2-medium (recommended for reliable local builds):

```
# Stop the VM first
gcloud compute instances stop openclaw-gateway --zone=us-central1-a

# Change machine type
gcloud compute instances set-machine-type openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small

# Start the VM
gcloud compute instances start openclaw-gateway --zone=us-central1-a
```

* * *

## Service accounts (security best practice)

For personal use, your default user account works fine. For automation or CI/CD pipelines, create a dedicated service account with minimal permissions:

1.  Create a service account:
    
    ```
    gcloud iam service-accounts create openclaw-deploy \
      --display-name="OpenClaw Deployment"
    ```
    
2.  Grant Compute Instance Admin role (or narrower custom role):
    
    ```
    gcloud projects add-iam-policy-binding my-openclaw-project \
      --member="serviceAccount:openclaw-deploy@my-openclaw-project.iam.gserviceaccount.com" \
      --role="roles/compute.instanceAdmin.v1"
    ```
    

Avoid using the Owner role for automation. Use the principle of least privilege. See [https://cloud.google.com/iam/docs/understanding-roles](https://cloud.google.com/iam/docs/understanding-roles) for IAM role details.

* * *

## Next steps

*   Set up messaging channels: [Channels](https://docs.openclaw.ai/channels)
*   Pair local devices as nodes: [Nodes](https://docs.openclaw.ai/nodes)
*   Configure the Gateway: [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)

---

<!-- SOURCE: https://docs.openclaw.ai/install/fly -->

# Fly.io - OpenClaw

## Fly.io Deployment

**Goal:** OpenClaw Gateway running on a [Fly.io](https://fly.io/) machine with persistent storage, automatic HTTPS, and Discord/channel access.

## What you need

*   [flyctl CLI](https://fly.io/docs/hands-on/install-flyctl/) installed
*   Fly.io account (free tier works)
*   Model auth: API key for your chosen model provider
*   Channel credentials: Discord bot token, Telegram token, etc.

## Beginner quick path

1.  Clone repo → customize `fly.toml`
2.  Create app + volume → set secrets
3.  Deploy with `fly deploy`
4.  SSH in to create config or use Control UI

## 1) Create the Fly app

```
# Clone the repo
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Create a new Fly app (pick your own name)
fly apps create my-openclaw

# Create a persistent volume (1GB is usually enough)
fly volumes create openclaw_data --size 1 --region iad
```

**Tip:** Choose a region close to you. Common options: `lhr` (London), `iad` (Virginia), `sjc` (San Jose).

## 2) Configure fly.toml

Edit `fly.toml` to match your app name and requirements. **Security note:** The default config exposes a public URL. For a hardened deployment with no public IP, see [Private Deployment](https://docs.openclaw.ai/install/fly#private-deployment-hardened) or use `fly.private.toml`.

```
app = "my-openclaw"  # Your app name
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  OPENCLAW_PREFER_PNPM = "1"
  OPENCLAW_STATE_DIR = "/data"
  NODE_OPTIONS = "--max-old-space-size=1536"

[processes]
  app = "node dist/index.js gateway --allow-unconfigured --port 3000 --bind lan"

[http_service]
  internal_port = 3000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[vm]]
  size = "shared-cpu-2x"
  memory = "2048mb"

[mounts]
  source = "openclaw_data"
  destination = "/data"
```

**Key settings:**

| Setting | Why |
| --- | --- |
| `--bind lan` | Binds to `0.0.0.0` so Fly’s proxy can reach the gateway |
| `--allow-unconfigured` | Starts without a config file (you’ll create one after) |
| `internal_port = 3000` | Must match `--port 3000` (or `OPENCLAW_GATEWAY_PORT`) for Fly health checks |
| `memory = "2048mb"` | 512MB is too small; 2GB recommended |
| `OPENCLAW_STATE_DIR = "/data"` | Persists state on the volume |

## 3) Set secrets

```
# Required: Gateway token (for non-loopback binding)
fly secrets set OPENCLAW_GATEWAY_TOKEN=$(openssl rand -hex 32)

# Model provider API keys
fly secrets set ANTHROPIC_API_KEY=sk-ant-...

# Optional: Other providers
fly secrets set OPENAI_API_KEY=sk-...
fly secrets set GOOGLE_API_KEY=...

# Channel tokens
fly secrets set DISCORD_BOT_TOKEN=MTQ...
```

**Notes:**

*   Non-loopback binds (`--bind lan`) require `OPENCLAW_GATEWAY_TOKEN` for security.
*   Treat these tokens like passwords.
*   **Prefer env vars over config file** for all API keys and tokens. This keeps secrets out of `openclaw.json` where they could be accidentally exposed or logged.

## 4) Deploy

First deploy builds the Docker image (~2-3 minutes). Subsequent deploys are faster. After deployment, verify:

You should see:

```
[gateway] listening on ws://0.0.0.0:3000 (PID xxx)
[discord] logged in to discord as xxx
```

## 5) Create config file

SSH into the machine to create a proper config:

Create the config directory and file:

```
mkdir -p /data
cat > /data/openclaw.json << 'EOF'
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["anthropic/claude-sonnet-4-5", "openai/gpt-4o"]
      },
      "maxConcurrent": 4
    },
    "list": [
      {
        "id": "main",
        "default": true
      }
    ]
  },
  "auth": {
    "profiles": {
      "anthropic:default": { "mode": "token", "provider": "anthropic" },
      "openai:default": { "mode": "token", "provider": "openai" }
    }
  },
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "discord" }
    }
  ],
  "channels": {
    "discord": {
      "enabled": true,
      "groupPolicy": "allowlist",
      "guilds": {
        "YOUR_GUILD_ID": {
          "channels": { "general": { "allow": true } },
          "requireMention": false
        }
      }
    }
  },
  "gateway": {
    "mode": "local",
    "bind": "auto"
  },
  "meta": {
    "lastTouchedVersion": "2026.1.29"
  }
}
EOF
```

**Note:** With `OPENCLAW_STATE_DIR=/data`, the config path is `/data/openclaw.json`. **Note:** The Discord token can come from either:

*   Environment variable: `DISCORD_BOT_TOKEN` (recommended for secrets)
*   Config file: `channels.discord.token`

If using env var, no need to add token to config. The gateway reads `DISCORD_BOT_TOKEN` automatically. Restart to apply:

```
exit
fly machine restart <machine-id>
```

## 6) Access the Gateway

### Control UI

Open in browser:

Or visit `https://my-openclaw.fly.dev/` Paste your gateway token (the one from `OPENCLAW_GATEWAY_TOKEN`) to authenticate.

### Logs

```
fly logs              # Live logs
fly logs --no-tail    # Recent logs
```

### SSH Console

## Troubleshooting

### ”App is not listening on expected address”

The gateway is binding to `127.0.0.1` instead of `0.0.0.0`. **Fix:** Add `--bind lan` to your process command in `fly.toml`.

### Health checks failing / connection refused

Fly can’t reach the gateway on the configured port. **Fix:** Ensure `internal_port` matches the gateway port (set `--port 3000` or `OPENCLAW_GATEWAY_PORT=3000`).

### OOM / Memory Issues

Container keeps restarting or getting killed. Signs: `SIGABRT`, `v8::internal::Runtime_AllocateInYoungGeneration`, or silent restarts. **Fix:** Increase memory in `fly.toml`:

Or update an existing machine:

```
fly machine update <machine-id> --vm-memory 2048 -y
```

**Note:** 512MB is too small. 1GB may work but can OOM under load or with verbose logging. **2GB is recommended.**

### Gateway Lock Issues

Gateway refuses to start with “already running” errors. This happens when the container restarts but the PID lock file persists on the volume. **Fix:** Delete the lock file:

```
fly ssh console --command "rm -f /data/gateway.*.lock"
fly machine restart <machine-id>
```

The lock file is at `/data/gateway.*.lock` (not in a subdirectory).

### Config Not Being Read

If using `--allow-unconfigured`, the gateway creates a minimal config. Your custom config at `/data/openclaw.json` should be read on restart. Verify the config exists:

```
fly ssh console --command "cat /data/openclaw.json"
```

### Writing Config via SSH

The `fly ssh console -C` command doesn’t support shell redirection. To write a config file:

```
# Use echo + tee (pipe from local to remote)
echo '{"your":"config"}' | fly ssh console -C "tee /data/openclaw.json"

# Or use sftp
fly sftp shell
> put /local/path/config.json /data/openclaw.json
```

**Note:** `fly sftp` may fail if the file already exists. Delete first:

```
fly ssh console --command "rm /data/openclaw.json"
```

### State Not Persisting

If you lose credentials or sessions after a restart, the state dir is writing to the container filesystem. **Fix:** Ensure `OPENCLAW_STATE_DIR=/data` is set in `fly.toml` and redeploy.

## Updates

```
# Pull latest changes
git pull

# Redeploy
fly deploy

# Check health
fly status
fly logs
```

### Updating Machine Command

If you need to change the startup command without a full redeploy:

```
# Get machine ID
fly machines list

# Update command
fly machine update <machine-id> --command "node dist/index.js gateway --port 3000 --bind lan" -y

# Or with memory increase
fly machine update <machine-id> --vm-memory 2048 --command "node dist/index.js gateway --port 3000 --bind lan" -y
```

**Note:** After `fly deploy`, the machine command may reset to what’s in `fly.toml`. If you made manual changes, re-apply them after deploy.

## Private Deployment (Hardened)

By default, Fly allocates public IPs, making your gateway accessible at `https://your-app.fly.dev`. This is convenient but means your deployment is discoverable by internet scanners (Shodan, Censys, etc.). For a hardened deployment with **no public exposure**, use the private template.

### When to use private deployment

*   You only make **outbound** calls/messages (no inbound webhooks)
*   You use **ngrok or Tailscale** tunnels for any webhook callbacks
*   You access the gateway via **SSH, proxy, or WireGuard** instead of browser
*   You want the deployment **hidden from internet scanners**

### Setup

Use `fly.private.toml` instead of the standard config:

```
# Deploy with private config
fly deploy -c fly.private.toml
```

Or convert an existing deployment:

```
# List current IPs
fly ips list -a my-openclaw

# Release public IPs
fly ips release <public-ipv4> -a my-openclaw
fly ips release <public-ipv6> -a my-openclaw

# Switch to private config so future deploys don't re-allocate public IPs
# (remove [http_service] or deploy with the private template)
fly deploy -c fly.private.toml

# Allocate private-only IPv6
fly ips allocate-v6 --private -a my-openclaw
```

After this, `fly ips list` should show only a `private` type IP:

```
VERSION  IP                   TYPE             REGION
v6       fdaa:x:x:x:x::x      private          global
```

### Accessing a private deployment

Since there’s no public URL, use one of these methods: **Option 1: Local proxy (simplest)**

```
# Forward local port 3000 to the app
fly proxy 3000:3000 -a my-openclaw

# Then open http://localhost:3000 in browser
```

**Option 2: WireGuard VPN**

```
# Create WireGuard config (one-time)
fly wireguard create

# Import to WireGuard client, then access via internal IPv6
# Example: http://[fdaa:x:x:x:x::x]:3000
```

**Option 3: SSH only**

```
fly ssh console -a my-openclaw
```

### Webhooks with private deployment

If you need webhook callbacks (Twilio, Telnyx, etc.) without public exposure:

1.  **ngrok tunnel** - Run ngrok inside the container or as a sidecar
2.  **Tailscale Funnel** - Expose specific paths via Tailscale
3.  **Outbound-only** - Some providers (Twilio) work fine for outbound calls without webhooks

Example voice-call config with ngrok:

```
{
  "plugins": {
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "tunnel": { "provider": "ngrok" },
          "webhookSecurity": {
            "allowedHosts": ["example.ngrok.app"]
          }
        }
      }
    }
  }
}
```

The ngrok tunnel runs inside the container and provides a public webhook URL without exposing the Fly app itself. Set `webhookSecurity.allowedHosts` to the public tunnel hostname so forwarded host headers are accepted.

### Security benefits

| Aspect | Public | Private |
| --- | --- | --- |
| Internet scanners | Discoverable | Hidden |
| Direct attacks | Possible | Blocked |
| Control UI access | Browser | Proxy/VPN |
| Webhook delivery | Direct | Via tunnel |

## Notes

*   Fly.io uses **x86 architecture** (not ARM)
*   The Dockerfile is compatible with both architectures
*   For WhatsApp/Telegram onboarding, use `fly ssh console`
*   Persistent data lives on the volume at `/data`
*   Signal requires Java + signal-cli; use a custom image and keep memory at 2GB+.

## Cost

With the recommended config (`shared-cpu-2x`, 2GB RAM):

*   ~$10-15/month depending on usage
*   Free tier includes some allowance

See [Fly.io pricing](https://fly.io/docs/about/pricing/) for details.

---

<!-- SOURCE: https://docs.openclaw.ai/install/exe-dev -->

# exe.dev - OpenClaw

Goal: OpenClaw Gateway running on an exe.dev VM, reachable from your laptop via: `https://<vm-name>.exe.xyz` This page assumes exe.dev’s default **exeuntu** image. If you picked a different distro, map packages accordingly.

## Beginner quick path

1.  [https://exe.new/openclaw](https://exe.new/openclaw)
2.  Fill in your auth key/token as needed
3.  Click on “Agent” next to your VM, and wait…
4.  ???
5.  Profit

## What you need

*   exe.dev account
*   `ssh exe.dev` access to [exe.dev](https://exe.dev/) virtual machines (optional)

## Automated Install with Shelley

Shelley, [exe.dev](https://exe.dev/)’s agent, can install OpenClaw instantly with our prompt. The prompt used is as below:

```
Set up OpenClaw (https://docs.openclaw.ai/install) on this VM. Use the non-interactive and accept-risk flags for openclaw onboarding. Add the supplied auth or token as needed. Configure nginx to forward from the default port 18789 to the root location on the default enabled site config, making sure to enable Websocket support. Pairing is done by "openclaw devices list" and "openclaw devices approve <request id>". Make sure the dashboard shows that OpenClaw's health is OK. exe.dev handles forwarding from port 8000 to port 80/443 and HTTPS for us, so the final "reachable" should be <vm-name>.exe.xyz, without port specification.
```

## Manual installation

## 1) Create the VM

From your device:

Then connect:

Tip: keep this VM **stateful**. OpenClaw stores state under `~/.openclaw/` and `~/.openclaw/workspace/`.

## 2) Install prerequisites (on the VM)

```
sudo apt-get update
sudo apt-get install -y git curl jq ca-certificates openssl
```

## 3) Install OpenClaw

Run the OpenClaw install script:

```
curl -fsSL https://openclaw.ai/install.sh | bash
```

## 4) Setup nginx to proxy OpenClaw to port 8000

Edit `/etc/nginx/sites-enabled/default` with

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 8000;
    listen [::]:8000;

    server_name _;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Standard proxy headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout settings for long-lived connections
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

## 5) Access OpenClaw and grant privileges

Access `https://<vm-name>.exe.xyz/` (see the Control UI output from onboarding). If it prompts for auth, paste the token from `gateway.auth.token` on the VM (retrieve with `openclaw config get gateway.auth.token`, or generate one with `openclaw doctor --generate-gateway-token`). Approve devices with `openclaw devices list` and `openclaw devices approve <requestId>`. When in doubt, use Shelley from your browser!

## Remote Access

Remote access is handled by [exe.dev](https://exe.dev/)’s authentication. By default, HTTP traffic from port 8000 is forwarded to `https://<vm-name>.exe.xyz` with email auth.

## Updating

```
npm i -g openclaw@latest
openclaw doctor
openclaw gateway restart
openclaw health
```

Guide: [Updating](https://docs.openclaw.ai/install/updating)

---

<!-- SOURCE: https://docs.openclaw.ai/install/northflank -->

# Deploy on Northflank - OpenClaw

Deploy OpenClaw on Northflank with a one-click template and finish setup in your browser. This is the easiest “no terminal on the server” path: Northflank runs the Gateway for you, and you configure everything via the `/setup` web wizard.

## How to get started

1.  Click [Deploy OpenClaw](https://northflank.com/stacks/deploy-openclaw) to open the template.
2.  Create an [account on Northflank](https://app.northflank.com/signup) if you don’t already have one.
3.  Click **Deploy OpenClaw now**.
4.  Set the required environment variable: `SETUP_PASSWORD`.
5.  Click **Deploy stack** to build and run the OpenClaw template.
6.  Wait for the deployment to complete, then click **View resources**.
7.  Open the OpenClaw service.
8.  Open the public OpenClaw URL and complete setup at `/setup`.
9.  Open the Control UI at `/openclaw`.

## What you get

*   Hosted OpenClaw Gateway + Control UI
*   Web setup wizard at `/setup` (no terminal commands)
*   Persistent storage via Northflank Volume (`/data`) so config/credentials/workspace survive redeploys

## Setup flow

1.  Visit `https://<your-northflank-domain>/setup` and enter your `SETUP_PASSWORD`.
2.  Choose a model/auth provider and paste your key.
3.  (Optional) Add Telegram/Discord/Slack tokens.
4.  Click **Run setup**.
5.  Open the Control UI at `https://<your-northflank-domain>/openclaw`

If Telegram DMs are set to pairing, the setup wizard can approve the pairing code.

## Getting chat tokens

### Telegram bot token

1.  Message `@BotFather` in Telegram
2.  Run `/newbot`
3.  Copy the token (looks like `123456789:AA...`)
4.  Paste it into `/setup`

### Discord bot token

1.  Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)
2.  **New Application** → choose a name
3.  **Bot** → **Add Bot**
4.  **Enable MESSAGE CONTENT INTENT** under Bot → Privileged Gateway Intents (required or the bot will crash on startup)
5.  Copy the **Bot Token** and paste into `/setup`
6.  Invite the bot to your server (OAuth2 URL Generator; scopes: `bot`, `applications.commands`)

---

<!-- SOURCE: https://docs.openclaw.ai/install/render -->

# Deploy on Render - OpenClaw

Deploy OpenClaw on Render using Infrastructure as Code. The included `render.yaml` Blueprint defines your entire stack declaratively, service, disk, environment variables, so you can deploy with a single click and version your infrastructure alongside your code.

## Prerequisites

*   A [Render account](https://render.com/) (free tier available)
*   An API key from your preferred [model provider](https://docs.openclaw.ai/providers)

## Deploy with a Render Blueprint

[Deploy to Render](https://render.com/deploy?repo=https://github.com/openclaw/openclaw) Clicking this link will:

1.  Create a new Render service from the `render.yaml` Blueprint at the root of this repo.
2.  Prompt you to set `SETUP_PASSWORD`
3.  Build the Docker image and deploy

Once deployed, your service URL follows the pattern `https://<service-name>.onrender.com`.

## Understanding the Blueprint

Render Blueprints are YAML files that define your infrastructure. The `render.yaml` in this repository configures everything needed to run OpenClaw:

```
services:
  - type: web
    name: openclaw
    runtime: docker
    plan: starter
    healthCheckPath: /health
    envVars:
      - key: PORT
        value: "8080"
      - key: SETUP_PASSWORD
        sync: false # prompts during deploy
      - key: OPENCLAW_STATE_DIR
        value: /data/.openclaw
      - key: OPENCLAW_WORKSPACE_DIR
        value: /data/workspace
      - key: OPENCLAW_GATEWAY_TOKEN
        generateValue: true # auto-generates a secure token
    disk:
      name: openclaw-data
      mountPath: /data
      sizeGB: 1
```

Key Blueprint features used:

| Feature | Purpose |
| --- | --- |
| `runtime: docker` | Builds from the repo’s Dockerfile |
| `healthCheckPath` | Render monitors `/health` and restarts unhealthy instances |
| `sync: false` | Prompts for value during deploy (secrets) |
| `generateValue: true` | Auto-generates a cryptographically secure value |
| `disk` | Persistent storage that survives redeploys |

## Choosing a plan

| Plan | Spin-down | Disk | Best for |
| --- | --- | --- | --- |
| Free | After 15 min idle | Not available | Testing, demos |
| Starter | Never | 1GB+ | Personal use, small teams |
| Standard+ | Never | 1GB+ | Production, multiple channels |

The Blueprint defaults to `starter`. To use free tier, change `plan: free` in your fork’s `render.yaml` (but note: no persistent disk means config resets on each deploy).

## After deployment

### Complete the setup wizard

1.  Navigate to `https://<your-service>.onrender.com/setup`
2.  Enter your `SETUP_PASSWORD`
3.  Select a model provider and paste your API key
4.  Optionally configure messaging channels (Telegram, Discord, Slack)
5.  Click **Run setup**

### Access the Control UI

The web dashboard is available at `https://<your-service>.onrender.com/openclaw`.

## Render Dashboard features

### Logs

View real-time logs in **Dashboard → your service → Logs**. Filter by:

*   Build logs (Docker image creation)
*   Deploy logs (service startup)
*   Runtime logs (application output)

### Shell access

For debugging, open a shell session via **Dashboard → your service → Shell**. The persistent disk is mounted at `/data`.

### Environment variables

Modify variables in **Dashboard → your service → Environment**. Changes trigger an automatic redeploy.

### Auto-deploy

If you use the original OpenClaw repository, Render will not auto-deploy your OpenClaw. To update it, run a manual Blueprint sync from the dashboard.

## Custom domain

1.  Go to **Dashboard → your service → Settings → Custom Domains**
2.  Add your domain
3.  Configure DNS as instructed (CNAME to `*.onrender.com`)
4.  Render provisions a TLS certificate automatically

## Scaling

Render supports horizontal and vertical scaling:

*   **Vertical**: Change the plan to get more CPU/RAM
*   **Horizontal**: Increase instance count (Standard plan and above)

For OpenClaw, vertical scaling is usually sufficient. Horizontal scaling requires sticky sessions or external state management.

## Backups and migration

Export your configuration and workspace at any time:

```
https://<your-service>.onrender.com/setup/export
```

This downloads a portable backup you can restore on any OpenClaw host.

## Troubleshooting

### Service won’t start

Check the deploy logs in the Render Dashboard. Common issues:

*   Missing `SETUP_PASSWORD` — the Blueprint prompts for this, but verify it’s set
*   Port mismatch — ensure `PORT=8080` matches the Dockerfile’s exposed port

### Slow cold starts (free tier)

Free tier services spin down after 15 minutes of inactivity. The first request after spin-down takes a few seconds while the container starts. Upgrade to Starter plan for always-on.

### Data loss after redeploy

This happens on free tier (no persistent disk). Upgrade to a paid plan, or regularly export your config via `/setup/export`.

### Health check failures

Render expects a 200 response from `/health` within 30 seconds. If builds succeed but deploys fail, the service may be taking too long to start. Check:

*   Build logs for errors
*   Whether the container runs locally with `docker build && docker run`

---

<!-- SOURCE: https://docs.openclaw.ai/install/macos-vm -->

# macOS VMs - OpenClaw

## OpenClaw on macOS VMs (Sandboxing)

## Recommended default (most users)

*   **Small Linux VPS** for an always-on Gateway and low cost. See [VPS hosting](https://docs.openclaw.ai/vps).
*   **Dedicated hardware** (Mac mini or Linux box) if you want full control and a **residential IP** for browser automation. Many sites block data center IPs, so local browsing often works better.
*   **Hybrid:** keep the Gateway on a cheap VPS, and connect your Mac as a **node** when you need browser/UI automation. See [Nodes](https://docs.openclaw.ai/nodes) and [Gateway remote](https://docs.openclaw.ai/gateway/remote).

Use a macOS VM when you specifically need macOS-only capabilities (iMessage/BlueBubbles) or want strict isolation from your daily Mac.

## macOS VM options

### Local VM on your Apple Silicon Mac (Lume)

Run OpenClaw in a sandboxed macOS VM on your existing Apple Silicon Mac using [Lume](https://cua.ai/docs/lume). This gives you:

*   Full macOS environment in isolation (your host stays clean)
*   iMessage support via BlueBubbles (impossible on Linux/Windows)
*   Instant reset by cloning VMs
*   No extra hardware or cloud costs

### Hosted Mac providers (cloud)

If you want macOS in the cloud, hosted Mac providers work too:

*   [MacStadium](https://www.macstadium.com/) (hosted Macs)
*   Other hosted Mac vendors also work; follow their VM + SSH docs

Once you have SSH access to a macOS VM, continue at step 6 below.

* * *

## Quick path (Lume, experienced users)

1.  Install Lume
2.  `lume create openclaw --os macos --ipsw latest`
3.  Complete Setup Assistant, enable Remote Login (SSH)
4.  `lume run openclaw --no-display`
5.  SSH in, install OpenClaw, configure channels
6.  Done

* * *

## What you need (Lume)

*   Apple Silicon Mac (M1/M2/M3/M4)
*   macOS Sequoia or later on the host
*   ~60 GB free disk space per VM
*   ~20 minutes

* * *

## 1) Install Lume

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"
```

If `~/.local/bin` isn’t in your PATH:

```
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc && source ~/.zshrc
```

Verify:

Docs: [Lume Installation](https://cua.ai/docs/lume/guide/getting-started/installation)

* * *

## 2) Create the macOS VM

```
lume create openclaw --os macos --ipsw latest
```

This downloads macOS and creates the VM. A VNC window opens automatically. Note: The download can take a while depending on your connection.

* * *

## 3) Complete Setup Assistant

In the VNC window:

1.  Select language and region
2.  Skip Apple ID (or sign in if you want iMessage later)
3.  Create a user account (remember the username and password)
4.  Skip all optional features

After setup completes, enable SSH:

1.  Open System Settings → General → Sharing
2.  Enable “Remote Login”

* * *

## 4) Get the VM’s IP address

Look for the IP address (usually `192.168.64.x`).

* * *

## 5) SSH into the VM

```
ssh youruser@192.168.64.X
```

Replace `youruser` with the account you created, and the IP with your VM’s IP.

* * *

## 6) Install OpenClaw

Inside the VM:

```
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Follow the onboarding prompts to set up your model provider (Anthropic, OpenAI, etc.).

* * *

## 7) Configure channels

Edit the config file:

```
nano ~/.openclaw/openclaw.json
```

Add your channels:

```
{
  "channels": {
    "whatsapp": {
      "dmPolicy": "allowlist",
      "allowFrom": ["+15551234567"]
    },
    "telegram": {
      "botToken": "YOUR_BOT_TOKEN"
    }
  }
}
```

Then login to WhatsApp (scan QR):

* * *

## 8) Run the VM headlessly

Stop the VM and restart without display:

```
lume stop openclaw
lume run openclaw --no-display
```

The VM runs in the background. OpenClaw’s daemon keeps the gateway running. To check status:

```
ssh youruser@192.168.64.X "openclaw status"
```

* * *

## Bonus: iMessage integration

This is the killer feature of running on macOS. Use [BlueBubbles](https://bluebubbles.app/) to add iMessage to OpenClaw. Inside the VM:

1.  Download BlueBubbles from bluebubbles.app
2.  Sign in with your Apple ID
3.  Enable the Web API and set a password
4.  Point BlueBubbles webhooks at your gateway (example: `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`)

Add to your OpenClaw config:

```
{
  "channels": {
    "bluebubbles": {
      "serverUrl": "http://localhost:1234",
      "password": "your-api-password",
      "webhookPath": "/bluebubbles-webhook"
    }
  }
}
```

Restart the gateway. Now your agent can send and receive iMessages. Full setup details: [BlueBubbles channel](https://docs.openclaw.ai/channels/bluebubbles)

* * *

## Save a golden image

Before customizing further, snapshot your clean state:

```
lume stop openclaw
lume clone openclaw openclaw-golden
```

Reset anytime:

```
lume stop openclaw && lume delete openclaw
lume clone openclaw-golden openclaw
lume run openclaw --no-display
```

* * *

## Running 24/7

Keep the VM running by:

*   Keeping your Mac plugged in
*   Disabling sleep in System Settings → Energy Saver
*   Using `caffeinate` if needed

For true always-on, consider a dedicated Mac mini or a small VPS. See [VPS hosting](https://docs.openclaw.ai/vps).

* * *

## Troubleshooting

| Problem | Solution |
| --- | --- |
| Can’t SSH into VM | Check “Remote Login” is enabled in VM’s System Settings |
| VM IP not showing | Wait for VM to fully boot, run `lume get openclaw` again |
| Lume command not found | Add `~/.local/bin` to your PATH |
| WhatsApp QR not scanning | Ensure you’re logged into the VM (not host) when running `openclaw channels login` |

* * *

*   [VPS hosting](https://docs.openclaw.ai/vps)
*   [Nodes](https://docs.openclaw.ai/nodes)
*   [Gateway remote](https://docs.openclaw.ai/gateway/remote)
*   [BlueBubbles channel](https://docs.openclaw.ai/channels/bluebubbles)
*   [Lume Quickstart](https://cua.ai/docs/lume/guide/getting-started/quickstart)
*   [Lume CLI Reference](https://cua.ai/docs/lume/reference/cli-reference)
*   [Unattended VM Setup](https://cua.ai/docs/lume/guide/fundamentals/unattended-setup) (advanced)
*   [Docker Sandboxing](https://docs.openclaw.ai/install/docker) (alternative isolation approach)

---

<!-- SOURCE: https://docs.openclaw.ai/install/railway -->

# Deploy on Railway - OpenClaw

Deploy OpenClaw on Railway with a one-click template and finish setup in your browser. This is the easiest “no terminal on the server” path: Railway runs the Gateway for you, and you configure everything via the `/setup` web wizard.

## Quick checklist (new users)

1.  Click **Deploy on Railway** (below).
2.  Add a **Volume** mounted at `/data`.
3.  Set the required **Variables** (at least `SETUP_PASSWORD`).
4.  Enable **HTTP Proxy** on port `8080`.
5.  Open `https://<your-railway-domain>/setup` and finish the wizard.

## One-click deploy

[Deploy on Railway](https://railway.com/deploy/clawdbot-railway-template) After deploy, find your public URL in **Railway → your service → Settings → Domains**. Railway will either:

*   give you a generated domain (often `https://<something>.up.railway.app`), or
*   use your custom domain if you attached one.

Then open:

*   `https://<your-railway-domain>/setup` — setup wizard (password protected)
*   `https://<your-railway-domain>/openclaw` — Control UI

## What you get

*   Hosted OpenClaw Gateway + Control UI
*   Web setup wizard at `/setup` (no terminal commands)
*   Persistent storage via Railway Volume (`/data`) so config/credentials/workspace survive redeploys
*   Backup export at `/setup/export` to migrate off Railway later

## Required Railway settings

### Public Networking

Enable **HTTP Proxy** for the service.

*   Port: `8080`

### Volume (required)

Attach a volume mounted at:

*   `/data`

### Variables

Set these variables on the service:

*   `SETUP_PASSWORD` (required)
*   `PORT=8080` (required — must match the port in Public Networking)
*   `OPENCLAW_STATE_DIR=/data/.openclaw` (recommended)
*   `OPENCLAW_WORKSPACE_DIR=/data/workspace` (recommended)
*   `OPENCLAW_GATEWAY_TOKEN` (recommended; treat as an admin secret)

## Setup flow

1.  Visit `https://<your-railway-domain>/setup` and enter your `SETUP_PASSWORD`.
2.  Choose a model/auth provider and paste your key.
3.  (Optional) Add Telegram/Discord/Slack tokens.
4.  Click **Run setup**.

If Telegram DMs are set to pairing, the setup wizard can approve the pairing code.

## Getting chat tokens

### Telegram bot token

1.  Message `@BotFather` in Telegram
2.  Run `/newbot`
3.  Copy the token (looks like `123456789:AA...`)
4.  Paste it into `/setup`

### Discord bot token

1.  Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)
2.  **New Application** → choose a name
3.  **Bot** → **Add Bot**
4.  **Enable MESSAGE CONTENT INTENT** under Bot → Privileged Gateway Intents (required or the bot will crash on startup)
5.  Copy the **Bot Token** and paste into `/setup`
6.  Invite the bot to your server (OAuth2 URL Generator; scopes: `bot`, `applications.commands`)

## Backups & migration

Download a backup at:

*   `https://<your-railway-domain>/setup/export`

This exports your OpenClaw state + workspace so you can migrate to another host without losing config or memory.

---

<!-- SOURCE: https://docs.openclaw.ai/vps -->

# VPS Hosting - OpenClaw

This hub links to the supported VPS/hosting guides and explains how cloud deployments work at a high level.

## Pick a provider

*   **Railway** (one‑click + browser setup): [Railway](https://docs.openclaw.ai/install/railway)
*   **Northflank** (one‑click + browser setup): [Northflank](https://docs.openclaw.ai/install/northflank)
*   **Oracle Cloud (Always Free)**: [Oracle](https://docs.openclaw.ai/platforms/oracle) — $0/month (Always Free, ARM; capacity/signup can be finicky)
*   **Fly.io**: [Fly.io](https://docs.openclaw.ai/install/fly)
*   **Hetzner (Docker)**: [Hetzner](https://docs.openclaw.ai/install/hetzner)
*   **GCP (Compute Engine)**: [GCP](https://docs.openclaw.ai/install/gcp)
*   **exe.dev** (VM + HTTPS proxy): [exe.dev](https://docs.openclaw.ai/install/exe-dev)
*   **AWS (EC2/Lightsail/free tier)**: works well too. Video guide: [https://x.com/techfrenAJ/status/2014934471095812547](https://x.com/techfrenAJ/status/2014934471095812547)

## How cloud setups work

*   The **Gateway runs on the VPS** and owns state + workspace.
*   You connect from your laptop/phone via the **Control UI** or **Tailscale/SSH**.
*   Treat the VPS as the source of truth and **back up** the state + workspace.
*   Secure default: keep the Gateway on loopback and access it via SSH tunnel or Tailscale Serve. If you bind to `lan`/`tailnet`, require `gateway.auth.token` or `gateway.auth.password`.

Remote access: [Gateway remote](https://docs.openclaw.ai/gateway/remote)  
Platforms hub: [Platforms](https://docs.openclaw.ai/platforms)

This is a valid setup when the users are in one trust boundary (for example one company team), and the agent is business-only.

*   Keep it on a dedicated runtime (VPS/VM/container + dedicated OS user/accounts).
*   Do not sign that runtime into personal Apple/Google accounts or personal browser/password-manager profiles.
*   If users are adversarial to each other, split by gateway/host/OS user.

Security model details: [Security](https://docs.openclaw.ai/gateway/security)

## Using nodes with a VPS

You can keep the Gateway in the cloud and pair **nodes** on your local devices (Mac/iOS/Android/headless). Nodes provide local screen/camera/canvas and `system.run` capabilities while the Gateway stays in the cloud. Docs: [Nodes](https://docs.openclaw.ai/nodes), [Nodes CLI](https://docs.openclaw.ai/cli/nodes)

## Startup tuning for small VMs and ARM hosts

If CLI commands feel slow on low-power VMs (or ARM hosts), enable Node’s module compile cache:

```
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF'
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

*   `NODE_COMPILE_CACHE` improves repeated command startup times.
*   `OPENCLAW_NO_RESPAWN=1` avoids extra startup overhead from a self-respawn path.
*   First command run warms cache; subsequent runs are faster.
*   For Raspberry Pi specifics, see [Raspberry Pi](https://docs.openclaw.ai/platforms/raspberry-pi).

### systemd tuning checklist (optional)

For VM hosts using `systemd`, consider:

*   Add service env for stable startup path:
    *   `OPENCLAW_NO_RESPAWN=1`
    *   `NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache`
*   Keep restart behavior explicit:
    *   `Restart=always`
    *   `RestartSec=2`
    *   `TimeoutStartSec=90`
*   Prefer SSD-backed disks for state/cache paths to reduce random-I/O cold-start penalties.

Example:

```
sudo systemctl edit openclaw
```

```
[Service]
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Restart=always
RestartSec=2
TimeoutStartSec=90
```

How `Restart=` policies help automated recovery: [systemd can automate service recovery](https://www.redhat.com/en/blog/systemd-automate-recovery).

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/oracle -->

# Oracle Cloud - OpenClaw

## Goal

Run a persistent OpenClaw Gateway on Oracle Cloud’s **Always Free** ARM tier. Oracle’s free tier can be a great fit for OpenClaw (especially if you already have an OCI account), but it comes with tradeoffs:

*   ARM architecture (most things work, but some binaries may be x86-only)
*   Capacity and signup can be finicky

## Cost Comparison (2026)

| Provider | Plan | Specs | Price/mo | Notes |
| --- | --- | --- | --- | --- |
| Oracle Cloud | Always Free ARM | up to 4 OCPU, 24GB RAM | $0  | ARM, limited capacity |
| Hetzner | CX22 | 2 vCPU, 4GB RAM | ~ $4 | Cheapest paid option |
| DigitalOcean | Basic | 1 vCPU, 1GB RAM | $6  | Easy UI, good docs |
| Vultr | Cloud Compute | 1 vCPU, 1GB RAM | $6  | Many locations |
| Linode | Nanode | 1 vCPU, 1GB RAM | $5  | Now part of Akamai |

* * *

## Prerequisites

*   Oracle Cloud account ([signup](https://www.oracle.com/cloud/free/)) — see [community signup guide](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd) if you hit issues
*   Tailscale account (free at [tailscale.com](https://tailscale.com/))
*   ~30 minutes

## 1) Create an OCI Instance

1.  Log into [Oracle Cloud Console](https://cloud.oracle.com/)
2.  Navigate to **Compute → Instances → Create Instance**
3.  Configure:
    *   **Name:** `openclaw`
    *   **Image:** Ubuntu 24.04 (aarch64)
    *   **Shape:** `VM.Standard.A1.Flex` (Ampere ARM)
    *   **OCPUs:** 2 (or up to 4)
    *   **Memory:** 12 GB (or up to 24 GB)
    *   **Boot volume:** 50 GB (up to 200 GB free)
    *   **SSH key:** Add your public key
4.  Click **Create**
5.  Note the public IP address

**Tip:** If instance creation fails with “Out of capacity”, try a different availability domain or retry later. Free tier capacity is limited.

## 2) Connect and Update

```
# Connect via public IP
ssh ubuntu@YOUR_PUBLIC_IP

# Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential
```

**Note:** `build-essential` is required for ARM compilation of some dependencies.

## 3) Configure User and Hostname

```
# Set hostname
sudo hostnamectl set-hostname openclaw

# Set password for ubuntu user
sudo passwd ubuntu

# Enable lingering (keeps user services running after logout)
sudo loginctl enable-linger ubuntu
```

## 4) Install Tailscale

```
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --ssh --hostname=openclaw
```

This enables Tailscale SSH, so you can connect via `ssh openclaw` from any device on your tailnet — no public IP needed. Verify:

**From now on, connect via Tailscale:** `ssh ubuntu@openclaw` (or use the Tailscale IP).

## 5) Install OpenClaw

```
curl -fsSL https://openclaw.ai/install.sh | bash
source ~/.bashrc
```

When prompted “How do you want to hatch your bot?”, select **“Do this later”**.

> Note: If you hit ARM-native build issues, start with system packages (e.g. `sudo apt install -y build-essential`) before reaching for Homebrew.

## 6) Configure Gateway (loopback + token auth) and enable Tailscale Serve

Use token auth as the default. It’s predictable and avoids needing any “insecure auth” Control UI flags.

```
# Keep the Gateway private on the VM
openclaw config set gateway.bind loopback

# Require auth for the Gateway + Control UI
openclaw config set gateway.auth.mode token
openclaw doctor --generate-gateway-token

# Expose over Tailscale Serve (HTTPS + tailnet access)
openclaw config set gateway.tailscale.mode serve
openclaw config set gateway.trustedProxies '["127.0.0.1"]'

systemctl --user restart openclaw-gateway
```

## 7) Verify

```
# Check version
openclaw --version

# Check daemon status
systemctl --user status openclaw-gateway

# Check Tailscale Serve
tailscale serve status

# Test local response
curl http://localhost:18789
```

## 8) Lock Down VCN Security

Now that everything is working, lock down the VCN to block all traffic except Tailscale. OCI’s Virtual Cloud Network acts as a firewall at the network edge — traffic is blocked before it reaches your instance.

1.  Go to **Networking → Virtual Cloud Networks** in the OCI Console
2.  Click your VCN → **Security Lists** → Default Security List
3.  **Remove** all ingress rules except:
    *   `0.0.0.0/0 UDP 41641` (Tailscale)
4.  Keep default egress rules (allow all outbound)

This blocks SSH on port 22, HTTP, HTTPS, and everything else at the network edge. From now on, you can only connect via Tailscale.

* * *

## Access the Control UI

From any device on your Tailscale network:

```
https://openclaw.<tailnet-name>.ts.net/
```

Replace `<tailnet-name>` with your tailnet name (visible in `tailscale status`). No SSH tunnel needed. Tailscale provides:

*   HTTPS encryption (automatic certs)
*   Authentication via Tailscale identity
*   Access from any device on your tailnet (laptop, phone, etc.)

* * *

## Security: VCN + Tailscale (recommended baseline)

With the VCN locked down (only UDP 41641 open) and the Gateway bound to loopback, you get strong defense-in-depth: public traffic is blocked at the network edge, and admin access happens over your tailnet. This setup often removes the _need_ for extra host-based firewall rules purely to stop Internet-wide SSH brute force — but you should still keep the OS updated, run `openclaw security audit`, and verify you aren’t accidentally listening on public interfaces.

### What’s Already Protected

| Traditional Step | Needed? | Why |
| --- | --- | --- |
| UFW firewall | No  | VCN blocks before traffic reaches instance |
| fail2ban | No  | No brute force if port 22 blocked at VCN |
| sshd hardening | No  | Tailscale SSH doesn’t use sshd |
| Disable root login | No  | Tailscale uses Tailscale identity, not system users |
| SSH key-only auth | No  | Tailscale authenticates via your tailnet |
| IPv6 hardening | Usually not | Depends on your VCN/subnet settings; verify what’s actually assigned/exposed |

### Still Recommended

*   **Credential permissions:** `chmod 700 ~/.openclaw`
*   **Security audit:** `openclaw security audit`
*   **System updates:** `sudo apt update && sudo apt upgrade` regularly
*   **Monitor Tailscale:** Review devices in [Tailscale admin console](https://login.tailscale.com/admin)

### Verify Security Posture

```
# Confirm no public ports listening
sudo ss -tlnp | grep -v '127.0.0.1\|::1'

# Verify Tailscale SSH is active
tailscale status | grep -q 'offers: ssh' && echo "Tailscale SSH active"

# Optional: disable sshd entirely
sudo systemctl disable --now ssh
```

* * *

## Fallback: SSH Tunnel

If Tailscale Serve isn’t working, use an SSH tunnel:

```
# From your local machine (via Tailscale)
ssh -L 18789:127.0.0.1:18789 ubuntu@openclaw
```

Then open `http://localhost:18789`.

* * *

## Troubleshooting

### Instance creation fails (“Out of capacity”)

Free tier ARM instances are popular. Try:

*   Different availability domain
*   Retry during off-peak hours (early morning)
*   Use the “Always Free” filter when selecting shape

### Tailscale won’t connect

```
# Check status
sudo tailscale status

# Re-authenticate
sudo tailscale up --ssh --hostname=openclaw --reset
```

### Gateway won’t start

```
openclaw gateway status
openclaw doctor --non-interactive
journalctl --user -u openclaw-gateway -n 50
```

### Can’t reach Control UI

```
# Verify Tailscale Serve is running
tailscale serve status

# Check gateway is listening
curl http://localhost:18789

# Restart if needed
systemctl --user restart openclaw-gateway
```

### ARM binary issues

Some tools may not have ARM builds. Check:

```
uname -m  # Should show aarch64
```

Most npm packages work fine. For binaries, look for `linux-arm64` or `aarch64` releases.

* * *

## Persistence

All state lives in:

*   `~/.openclaw/` — config, credentials, session data
*   `~/.openclaw/workspace/` — workspace (SOUL.md, memory, artifacts)

Back up periodically:

```
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

* * *

## See Also

*   [Gateway remote access](https://docs.openclaw.ai/gateway/remote) — other remote access patterns
*   [Tailscale integration](https://docs.openclaw.ai/gateway/tailscale) — full Tailscale docs
*   [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) — all config options
*   [DigitalOcean guide](https://docs.openclaw.ai/platforms/digitalocean) — if you want paid + easier signup
*   [Hetzner guide](https://docs.openclaw.ai/install/hetzner) — Docker-based alternative

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/raspberry-pi -->

# Raspberry Pi - OpenClaw

## Goal

Run a persistent, always-on OpenClaw Gateway on a Raspberry Pi for **~$35-80** one-time cost (no monthly fees). Perfect for:

*   24/7 personal AI assistant
*   Home automation hub
*   Low-power, always-available Telegram/WhatsApp bot

## Hardware Requirements

| Pi Model | RAM | Works? | Notes |
| --- | --- | --- | --- |
| **Pi 5** | 4GB/8GB | ✅ Best | Fastest, recommended |
| **Pi 4** | 4GB | ✅ Good | Sweet spot for most users |
| **Pi 4** | 2GB | ✅ OK | Works, add swap |
| **Pi 4** | 1GB | ⚠️ Tight | Possible with swap, minimal config |
| **Pi 3B+** | 1GB | ⚠️ Slow | Works but sluggish |
| **Pi Zero 2 W** | 512MB | ❌   | Not recommended |

**Minimum specs:** 1GB RAM, 1 core, 500MB disk  
**Recommended:** 2GB+ RAM, 64-bit OS, 16GB+ SD card (or USB SSD)

## What You’ll Need

*   Raspberry Pi 4 or 5 (2GB+ recommended)
*   MicroSD card (16GB+) or USB SSD (better performance)
*   Power supply (official Pi PSU recommended)
*   Network connection (Ethernet or WiFi)
*   ~30 minutes

## 1) Flash the OS

Use **Raspberry Pi OS Lite (64-bit)** — no desktop needed for a headless server.

1.  Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2.  Choose OS: **Raspberry Pi OS Lite (64-bit)**
3.  Click the gear icon (⚙️) to pre-configure:
    *   Set hostname: `gateway-host`
    *   Enable SSH
    *   Set username/password
    *   Configure WiFi (if not using Ethernet)
4.  Flash to your SD card / USB drive
5.  Insert and boot the Pi

## 2) Connect via SSH

```
ssh user@gateway-host
# or use the IP address
ssh user@192.168.x.x
```

## 3) System Setup

```
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y git curl build-essential

# Set timezone (important for cron/reminders)
sudo timedatectl set-timezone America/Chicago  # Change to your timezone
```

## 4) Install Node.js 22 (ARM64)

```
# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version  # Should show v22.x.x
npm --version
```

## 5) Add Swap (Important for 2GB or less)

Swap prevents out-of-memory crashes:

```
# Create 2GB swap file
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Optimize for low RAM (reduce swappiness)
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 6) Install OpenClaw

### Option A: Standard Install (Recommended)

```
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Option B: Hackable Install (For tinkering)

```
git clone https://github.com/openclaw/openclaw.git
cd openclaw
npm install
npm run build
npm link
```

The hackable install gives you direct access to logs and code — useful for debugging ARM-specific issues.

## 7) Run Onboarding

```
openclaw onboard --install-daemon
```

Follow the wizard:

1.  **Gateway mode:** Local
2.  **Auth:** API keys recommended (OAuth can be finicky on headless Pi)
3.  **Channels:** Telegram is easiest to start with
4.  **Daemon:** Yes (systemd)

## 8) Verify Installation

```
# Check status
openclaw status

# Check service
sudo systemctl status openclaw

# View logs
journalctl -u openclaw -f
```

## 9) Access the Dashboard

Since the Pi is headless, use an SSH tunnel:

```
# From your laptop/desktop
ssh -L 18789:localhost:18789 user@gateway-host

# Then open in browser
open http://localhost:18789
```

Or use Tailscale for always-on access:

```
# On the Pi
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Update config
openclaw config set gateway.bind tailnet
sudo systemctl restart openclaw
```

* * *

## Performance Optimizations

### Use a USB SSD (Huge Improvement)

SD cards are slow and wear out. A USB SSD dramatically improves performance:

```
# Check if booting from USB
lsblk
```

See [Pi USB boot guide](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#usb-mass-storage-boot) for setup.

### Speed up CLI startup (module compile cache)

On lower-power Pi hosts, enable Node’s module compile cache so repeated CLI runs are faster:

```
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF' # pragma: allowlist secret
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

Notes:

*   `NODE_COMPILE_CACHE` speeds up subsequent runs (`status`, `health`, `--help`).
*   `/var/tmp` survives reboots better than `/tmp`.
*   `OPENCLAW_NO_RESPAWN=1` avoids extra startup cost from CLI self-respawn.
*   First run warms the cache; later runs benefit most.

### systemd startup tuning (optional)

If this Pi is mostly running OpenClaw, add a service drop-in to reduce restart jitter and keep startup env stable:

```
sudo systemctl edit openclaw
```

```
[Service]
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Restart=always
RestartSec=2
TimeoutStartSec=90
```

Then apply:

```
sudo systemctl daemon-reload
sudo systemctl restart openclaw
```

If possible, keep OpenClaw state/cache on SSD-backed storage to avoid SD-card random-I/O bottlenecks during cold starts. How `Restart=` policies help automated recovery: [systemd can automate service recovery](https://www.redhat.com/en/blog/systemd-automate-recovery).

### Reduce Memory Usage

```
# Disable GPU memory allocation (headless)
echo 'gpu_mem=16' | sudo tee -a /boot/config.txt

# Disable Bluetooth if not needed
sudo systemctl disable bluetooth
```

### Monitor Resources

```
# Check memory
free -h

# Check CPU temperature
vcgencmd measure_temp

# Live monitoring
htop
```

* * *

## ARM-Specific Notes

### Binary Compatibility

Most OpenClaw features work on ARM64, but some external binaries may need ARM builds:

| Tool | ARM64 Status | Notes |
| --- | --- | --- |
| Node.js | ✅   | Works great |
| WhatsApp (Baileys) | ✅   | Pure JS, no issues |
| Telegram | ✅   | Pure JS, no issues |
| gog (Gmail CLI) | ⚠️  | Check for ARM release |
| Chromium (browser) | ✅   | `sudo apt install chromium-browser` |

If a skill fails, check if its binary has an ARM build. Many Go/Rust tools do; some don’t.

### 32-bit vs 64-bit

**Always use 64-bit OS.** Node.js and many modern tools require it. Check with:

```
uname -m
# Should show: aarch64 (64-bit) not armv7l (32-bit)
```

* * *

## Recommended Model Setup

Since the Pi is just the Gateway (models run in the cloud), use API-based models:

```
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-20250514",
        "fallbacks": ["openai/gpt-4o-mini"]
      }
    }
  }
}
```

**Don’t try to run local LLMs on a Pi** — even small models are too slow. Let Claude/GPT do the heavy lifting.

* * *

## Auto-Start on Boot

The onboarding wizard sets this up, but to verify:

```
# Check service is enabled
sudo systemctl is-enabled openclaw

# Enable if not
sudo systemctl enable openclaw

# Start on boot
sudo systemctl start openclaw
```

* * *

## Troubleshooting

### Out of Memory (OOM)

```
# Check memory
free -h

# Add more swap (see Step 5)
# Or reduce services running on the Pi
```

### Slow Performance

*   Use USB SSD instead of SD card
*   Disable unused services: `sudo systemctl disable cups bluetooth avahi-daemon`
*   Check CPU throttling: `vcgencmd get_throttled` (should return `0x0`)

### Service Won’t Start

```
# Check logs
journalctl -u openclaw --no-pager -n 100

# Common fix: rebuild
cd ~/openclaw  # if using hackable install
npm run build
sudo systemctl restart openclaw
```

### ARM Binary Issues

If a skill fails with “exec format error”:

1.  Check if the binary has an ARM64 build
2.  Try building from source
3.  Or use a Docker container with ARM support

### WiFi Drops

For headless Pis on WiFi:

```
# Disable WiFi power management
sudo iwconfig wlan0 power off

# Make permanent
echo 'wireless-power off' | sudo tee -a /etc/network/interfaces
```

* * *

## Cost Comparison

| Setup | One-Time Cost | Monthly Cost | Notes |
| --- | --- | --- | --- |
| **Pi 4 (2GB)** | ~$45 | $0  | \+ power (~$5/yr) |
| **Pi 4 (4GB)** | ~$55 | $0  | Recommended |
| **Pi 5 (4GB)** | ~$60 | $0  | Best performance |
| **Pi 5 (8GB)** | ~$80 | $0  | Overkill but future-proof |
| DigitalOcean | $0  | $6/mo | $72/year |
| Hetzner | $0  | €3.79/mo | ~$50/year |

**Break-even:** A Pi pays for itself in ~6-12 months vs cloud VPS.

* * *

## See Also

*   [Linux guide](https://docs.openclaw.ai/platforms/linux) — general Linux setup
*   [DigitalOcean guide](https://docs.openclaw.ai/platforms/digitalocean) — cloud alternative
*   [Hetzner guide](https://docs.openclaw.ai/install/hetzner) — Docker setup
*   [Tailscale](https://docs.openclaw.ai/gateway/tailscale) — remote access
*   [Nodes](https://docs.openclaw.ai/nodes) — pair your laptop/phone with the Pi gateway

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/digitalocean -->

# DigitalOcean - OpenClaw

## Goal

Run a persistent OpenClaw Gateway on DigitalOcean for \*\*6/month∗∗(or6/month\*\* (or 4/mo with reserved pricing). If you want a $0/month option and don’t mind ARM + provider-specific setup, see the [Oracle Cloud guide](https://docs.openclaw.ai/platforms/oracle).

## Cost Comparison (2026)

| Provider | Plan | Specs | Price/mo | Notes |
| --- | --- | --- | --- | --- |
| Oracle Cloud | Always Free ARM | up to 4 OCPU, 24GB RAM | $0  | ARM, limited capacity / signup quirks |
| Hetzner | CX22 | 2 vCPU, 4GB RAM | €3.79 (~$4) | Cheapest paid option |
| DigitalOcean | Basic | 1 vCPU, 1GB RAM | $6  | Easy UI, good docs |
| Vultr | Cloud Compute | 1 vCPU, 1GB RAM | $6  | Many locations |
| Linode | Nanode | 1 vCPU, 1GB RAM | $5  | Now part of Akamai |

**Picking a provider:**

*   DigitalOcean: simplest UX + predictable setup (this guide)
*   Hetzner: good price/perf (see [Hetzner guide](https://docs.openclaw.ai/install/hetzner))
*   Oracle Cloud: can be $0/month, but is more finicky and ARM-only (see [Oracle guide](https://docs.openclaw.ai/platforms/oracle))

* * *

## Prerequisites

*   DigitalOcean account ([signup with $200 free credit](https://m.do.co/c/signup))
*   SSH key pair (or willingness to use password auth)
*   ~20 minutes

## 1) Create a Droplet

1.  Log into [DigitalOcean](https://cloud.digitalocean.com/)
2.  Click **Create → Droplets**
3.  Choose:
    *   **Region:** Closest to you (or your users)
    *   **Image:** Ubuntu 24.04 LTS
    *   **Size:** Basic → Regular → **$6/mo** (1 vCPU, 1GB RAM, 25GB SSD)
    *   **Authentication:** SSH key (recommended) or password
4.  Click **Create Droplet**
5.  Note the IP address

## 2) Connect via SSH

## 3) Install OpenClaw

```
# Update system
apt update && apt upgrade -y

# Install Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# Verify
openclaw --version
```

## 4) Run Onboarding

```
openclaw onboard --install-daemon
```

The wizard will walk you through:

*   Model auth (API keys or OAuth)
*   Channel setup (Telegram, WhatsApp, Discord, etc.)
*   Gateway token (auto-generated)
*   Daemon installation (systemd)

## 5) Verify the Gateway

```
# Check status
openclaw status

# Check service
systemctl --user status openclaw-gateway.service

# View logs
journalctl --user -u openclaw-gateway.service -f
```

## 6) Access the Dashboard

The gateway binds to loopback by default. To access the Control UI: **Option A: SSH Tunnel (recommended)**

```
# From your local machine
ssh -L 18789:localhost:18789 root@YOUR_DROPLET_IP

# Then open: http://localhost:18789
```

**Option B: Tailscale Serve (HTTPS, loopback-only)**

```
# On the droplet
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# Configure Gateway to use Tailscale Serve
openclaw config set gateway.tailscale.mode serve
openclaw gateway restart
```

Open: `https://<magicdns>/` Notes:

*   Serve keeps the Gateway loopback-only and authenticates Control UI/WebSocket traffic via Tailscale identity headers (tokenless auth assumes trusted gateway host; HTTP APIs still require token/password).
*   To require token/password instead, set `gateway.auth.allowTailscale: false` or use `gateway.auth.mode: "password"`.

**Option C: Tailnet bind (no Serve)**

```
openclaw config set gateway.bind tailnet
openclaw gateway restart
```

Open: `http://<tailscale-ip>:18789` (token required).

## 7) Connect Your Channels

### Telegram

```
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

### WhatsApp

```
openclaw channels login whatsapp
# Scan QR code
```

See [Channels](https://docs.openclaw.ai/channels) for other providers.

* * *

## Optimizations for 1GB RAM

The $6 droplet only has 1GB RAM. To keep things running smoothly:

### Add swap (recommended)

```
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Use a lighter model

If you’re hitting OOMs, consider:

*   Using API-based models (Claude, GPT) instead of local models
*   Setting `agents.defaults.model.primary` to a smaller model

### Monitor memory

* * *

## Persistence

All state lives in:

*   `~/.openclaw/` — config, credentials, session data
*   `~/.openclaw/workspace/` — workspace (SOUL.md, memory, etc.)

These survive reboots. Back them up periodically:

```
tar -czvf openclaw-backup.tar.gz ~/.openclaw ~/.openclaw/workspace
```

* * *

## Oracle Cloud Free Alternative

Oracle Cloud offers **Always Free** ARM instances that are significantly more powerful than any paid option here — for $0/month.

| What you get | Specs |
| --- | --- |
| **4 OCPUs** | ARM Ampere A1 |
| **24GB RAM** | More than enough |
| **200GB storage** | Block volume |
| **Forever free** | No credit card charges |

**Caveats:**

*   Signup can be finicky (retry if it fails)
*   ARM architecture — most things work, but some binaries need ARM builds

For the full setup guide, see [Oracle Cloud](https://docs.openclaw.ai/platforms/oracle). For signup tips and troubleshooting the enrollment process, see this [community guide](https://gist.github.com/rssnyder/51e3cfedd730e7dd5f4a816143b25dbd).

* * *

## Troubleshooting

### Gateway won’t start

```
openclaw gateway status
openclaw doctor --non-interactive
journalctl -u openclaw --no-pager -n 50
```

### Port already in use

```
lsof -i :18789
kill <PID>
```

### Out of memory

```
# Check memory
free -h

# Add more swap
# Or upgrade to $12/mo droplet (2GB RAM)
```

* * *

## See Also

*   [Hetzner guide](https://docs.openclaw.ai/install/hetzner) — cheaper, more powerful
*   [Docker install](https://docs.openclaw.ai/install/docker) — containerized setup
*   [Tailscale](https://docs.openclaw.ai/gateway/tailscale) — secure remote access
*   [Configuration](https://docs.openclaw.ai/gateway/configuration) — full config reference

