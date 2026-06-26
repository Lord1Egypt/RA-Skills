# GCP

Source: https://docs.openclaw.ai/install/gcp

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationHosting and deploymentGCPGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
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
- [OpenClaw on GCP Compute Engine (Docker, Production VPS Guide)](#openclaw-on-gcp-compute-engine-docker-production-vps-guide)
- [Goal](#goal)
- [What are we doing (simple terms)?](#what-are-we-doing-simple-terms-)
- [Quick path (experienced operators)](#quick-path-experienced-operators)
- [What you need](#what-you-need)
- [1) Install gcloud CLI (or use Console)](#1-install-gcloud-cli-or-use-console)
- [2) Create a GCP project](#2-create-a-gcp-project)
- [3) Create the VM](#3-create-the-vm)
- [4) SSH into the VM](#4-ssh-into-the-vm)
- [5) Install Docker (on the VM)](#5-install-docker-on-the-vm)
- [6) Clone the OpenClaw repository](#6-clone-the-openclaw-repository)
- [7) Create persistent host directories](#7-create-persistent-host-directories)
- [8) Configure environment variables](#8-configure-environment-variables)
- [9) Docker Compose configuration](#9-docker-compose-configuration)
- [10) Bake required binaries into the image (critical)](#10-bake-required-binaries-into-the-image-critical)
- [11) Build and launch](#11-build-and-launch)
- [12) Verify Gateway](#12-verify-gateway)
- [13) Access from your laptop](#13-access-from-your-laptop)
- [What persists where (source of truth)](#what-persists-where-source-of-truth)
- [Updates](#updates)
- [Troubleshooting](#troubleshooting)
- [Service accounts (security best practice)](#service-accounts-security-best-practice)
- [Next steps](#next-steps)

​OpenClaw on GCP Compute Engine (Docker, Production VPS Guide)
​Goal
Run a persistent OpenClaw Gateway on a GCP Compute Engine VM using Docker, with durable state, baked-in binaries, and safe restart behavior.
If you want “OpenClaw 24/7 for ~$5-12/mo”, this is a reliable setup on Google Cloud.
Pricing varies by machine type and region; pick the smallest VM that fits your workload and scale up if you hit OOMs.
​What are we doing (simple terms)?

- Create a GCP project and enable billing

- Create a Compute Engine VM

- Install Docker (isolated app runtime)

- Start the OpenClaw Gateway in Docker

- Persist `~/.openclaw` + `~/.openclaw/workspace` on the host (survives restarts/rebuilds)

- Access the Control UI from your laptop via an SSH tunnel

The Gateway can be accessed via:

- SSH port forwarding from your laptop

- Direct port exposure if you manage firewalling and tokens yourself

This guide uses Debian on GCP Compute Engine.
Ubuntu also works; map packages accordingly.
For the generic Docker flow, see [Docker](/install/docker).

​Quick path (experienced operators)

- Create GCP project + enable Compute Engine API

- Create Compute Engine VM (e2-small, Debian 12, 20GB)

- SSH into the VM

- Install Docker

- Clone OpenClaw repository

- Create persistent host directories

- Configure `.env` and `docker-compose.yml`

- Bake required binaries, build, and launch

​What you need

- GCP account (free tier eligible for e2-micro)

- gcloud CLI installed (or use Cloud Console)

- SSH access from your laptop

- Basic comfort with SSH + copy/paste

- ~20-30 minutes

- Docker and Docker Compose

- Model auth credentials

Optional provider credentials

- WhatsApp QR

- Telegram bot token

- Gmail OAuth

​1) Install gcloud CLI (or use Console)
**Option A: gcloud CLI** (recommended for automation)
Install from [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
Initialize and authenticate:
Copy```
gcloud init
gcloud auth login

```

**Option B: Cloud Console**
All steps can be done via the web UI at [https://console.cloud.google.com](https://console.cloud.google.com)

​2) Create a GCP project
**CLI:**
Copy```
gcloud projects create my-openclaw-project --name="OpenClaw Gateway"
gcloud config set project my-openclaw-project

```

Enable billing at [https://console.cloud.google.com/billing](https://console.cloud.google.com/billing) (required for Compute Engine).
Enable the Compute Engine API:
Copy```
gcloud services enable compute.googleapis.com

```

**Console:**

- Go to IAM & Admin > Create Project

- Name it and create

- Enable billing for the project

- Navigate to APIs & Services > Enable APIs > search “Compute Engine API” > Enable

​3) Create the VM
**Machine types:**
TypeSpecsCostNotese2-small2 vCPU, 2GB RAM~$12/moRecommendede2-micro2 vCPU (shared), 1GB RAMFree tier eligibleMay OOM under load
**CLI:**
Copy```
gcloud compute instances create openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud

```

**Console:**

- Go to Compute Engine > VM instances > Create instance

- Name: `openclaw-gateway`

- Region: `us-central1`, Zone: `us-central1-a`

- Machine type: `e2-small`

- Boot disk: Debian 12, 20GB

- Create

​4) SSH into the VM
**CLI:**
Copy```
gcloud compute ssh openclaw-gateway --zone=us-central1-a

```

**Console:**
Click the “SSH” button next to your VM in the Compute Engine dashboard.
Note: SSH key propagation can take 1-2 minutes after VM creation. If connection is refused, wait and retry.

​5) Install Docker (on the VM)
Copy```
sudo apt-get update
sudo apt-get install -y git curl ca-certificates
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER

```

Log out and back in for the group change to take effect:
Copy```
exit

```

Then SSH back in:
Copy```
gcloud compute ssh openclaw-gateway --zone=us-central1-a

```

Verify:
Copy```
docker --version
docker compose version

```

​6) Clone the OpenClaw repository
Copy```
git clone https://github.com/openclaw/openclaw.git
cd openclaw

```

This guide assumes you will build a custom image to guarantee binary persistence.

​7) Create persistent host directories
Docker containers are ephemeral.
All long-lived state must live on the host.
Copy```
mkdir -p ~/.openclaw
mkdir -p ~/.openclaw/workspace

```

​8) Configure environment variables
Create `.env` in the repository root.
Copy```
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
Copy```
openssl rand -hex 32

```

**Do not commit this file.**

​9) Docker Compose configuration
Create or update `docker-compose.yml`.
Copy```
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

​10) Bake required binaries into the image (critical)
Installing binaries inside a running container is a trap.
Anything installed at runtime will be lost on restart.
All external binaries required by skills must be installed at image build time.
The examples below show three common binaries only:

- `gog` for Gmail access

- `goplaces` for Google Places

- `wacli` for WhatsApp

These are examples, not a complete list.
You may install as many binaries as needed using the same pattern.
If you add new skills later that depend on additional binaries, you must:

- Update the Dockerfile

- Rebuild the image

- Restart the containers

**Example Dockerfile**
Copy```
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

​11) Build and launch
Copy```
docker compose build
docker compose up -d openclaw-gateway

```

Verify binaries:
Copy```
docker compose exec openclaw-gateway which gog
docker compose exec openclaw-gateway which goplaces
docker compose exec openclaw-gateway which wacli

```

Expected output:
Copy```
/usr/local/bin/gog
/usr/local/bin/goplaces
/usr/local/bin/wacli

```

​12) Verify Gateway
Copy```
docker compose logs -f openclaw-gateway

```

Success:
Copy```
[gateway] listening on ws://0.0.0.0:18789

```

​13) Access from your laptop
Create an SSH tunnel to forward the Gateway port:
Copy```
gcloud compute ssh openclaw-gateway --zone=us-central1-a -- -L 18789:127.0.0.1:18789

```

Open in your browser:
`http://127.0.0.1:18789/`
Paste your gateway token.

​What persists where (source of truth)
OpenClaw runs in Docker, but Docker is not the source of truth.
All long-lived state must survive restarts, rebuilds, and reboots.
ComponentLocationPersistence mechanismNotesGateway config`/home/node/.openclaw/`Host volume mountIncludes `openclaw.json`, tokensModel auth profiles`/home/node/.openclaw/`Host volume mountOAuth tokens, API keysSkill configs`/home/node/.openclaw/skills/`Host volume mountSkill-level stateAgent workspace`/home/node/.openclaw/workspace/`Host volume mountCode and agent artifactsWhatsApp session`/home/node/.openclaw/`Host volume mountPreserves QR loginGmail keyring`/home/node/.openclaw/`Host volume + passwordRequires `GOG_KEYRING_PASSWORD`External binaries`/usr/local/bin/`Docker imageMust be baked at build timeNode runtimeContainer filesystemDocker imageRebuilt every image buildOS packagesContainer filesystemDocker imageDo not install at runtimeDocker containerEphemeralRestartableSafe to destroy

​Updates
To update OpenClaw on the VM:
Copy```
cd ~/openclaw
git pull
docker compose build
docker compose up -d

```

​Troubleshooting
**SSH connection refused**
SSH key propagation can take 1-2 minutes after VM creation. Wait and retry.
**OS Login issues**
Check your OS Login profile:
Copy```
gcloud compute os-login describe-profile

```

Ensure your account has the required IAM permissions (Compute OS Login or Compute OS Admin Login).
**Out of memory (OOM)**
If using e2-micro and hitting OOM, upgrade to e2-small or e2-medium:
Copy```
# Stop the VM first
gcloud compute instances stop openclaw-gateway --zone=us-central1-a

# Change machine type
gcloud compute instances set-machine-type openclaw-gateway \
  --zone=us-central1-a \
  --machine-type=e2-small

# Start the VM
gcloud compute instances start openclaw-gateway --zone=us-central1-a

```

​Service accounts (security best practice)
For personal use, your default user account works fine.
For automation or CI/CD pipelines, create a dedicated service account with minimal permissions:

Create a service account:
Copy```
gcloud iam service-accounts create openclaw-deploy \
  --display-name="OpenClaw Deployment"

```

Grant Compute Instance Admin role (or narrower custom role):
Copy```
gcloud projects add-iam-policy-binding my-openclaw-project \
  --member="serviceAccount:openclaw-deploy@my-openclaw-project.iam.gserviceaccount.com" \
  --role="roles/compute.instanceAdmin.v1"

```

Avoid using the Owner role for automation. Use the principle of least privilege.
See [https://cloud.google.com/iam/docs/understanding-roles](https://cloud.google.com/iam/docs/understanding-roles) for IAM role details.

​Next steps

- Set up messaging channels: [Channels](/channels)

- Pair local devices as nodes: [Nodes](/nodes)

- Configure the Gateway: [Gateway configuration](/gateway/configuration)

HetznermacOS VMs⌘I