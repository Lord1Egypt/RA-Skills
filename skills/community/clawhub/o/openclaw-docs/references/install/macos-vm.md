# macOS VMs

Source: https://docs.openclaw.ai/install/macos-vm

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationHosting and deploymentmacOS VMsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
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
- [OpenClaw on macOS VMs (Sandboxing)](#openclaw-on-macos-vms-sandboxing)
- [Recommended default (most users)](#recommended-default-most-users)
- [macOS VM options](#macos-vm-options)
- [Local VM on your Apple Silicon Mac (Lume)](#local-vm-on-your-apple-silicon-mac-lume)
- [Hosted Mac providers (cloud)](#hosted-mac-providers-cloud)
- [Quick path (Lume, experienced users)](#quick-path-lume-experienced-users)
- [What you need (Lume)](#what-you-need-lume)
- [1) Install Lume](#1-install-lume)
- [2) Create the macOS VM](#2-create-the-macos-vm)
- [3) Complete Setup Assistant](#3-complete-setup-assistant)
- [4) Get the VM’s IP address](#4-get-the-vm%E2%80%99s-ip-address)
- [5) SSH into the VM](#5-ssh-into-the-vm)
- [6) Install OpenClaw](#6-install-openclaw)
- [7) Configure channels](#7-configure-channels)
- [8) Run the VM headlessly](#8-run-the-vm-headlessly)
- [Bonus: iMessage integration](#bonus-imessage-integration)
- [Save a golden image](#save-a-golden-image)
- [Running 24/7](#running-24%2F7)
- [Troubleshooting](#troubleshooting)
- [Related docs](#related-docs)

​OpenClaw on macOS VMs (Sandboxing)
​Recommended default (most users)

- **Small Linux VPS** for an always-on Gateway and low cost. See [VPS hosting](/vps).

- **Dedicated hardware** (Mac mini or Linux box) if you want full control and a **residential IP** for browser automation. Many sites block data center IPs, so local browsing often works better.

- **Hybrid:** keep the Gateway on a cheap VPS, and connect your Mac as a **node** when you need browser/UI automation. See [Nodes](/nodes) and [Gateway remote](/gateway/remote).

Use a macOS VM when you specifically need macOS-only capabilities (iMessage/BlueBubbles) or want strict isolation from your daily Mac.
​macOS VM options
​Local VM on your Apple Silicon Mac (Lume)
Run OpenClaw in a sandboxed macOS VM on your existing Apple Silicon Mac using [Lume](https://cua.ai/docs/lume).
This gives you:

- Full macOS environment in isolation (your host stays clean)

- iMessage support via BlueBubbles (impossible on Linux/Windows)

- Instant reset by cloning VMs

- No extra hardware or cloud costs

​Hosted Mac providers (cloud)
If you want macOS in the cloud, hosted Mac providers work too:

- [MacStadium](https://www.macstadium.com/) (hosted Macs)

- Other hosted Mac vendors also work; follow their VM + SSH docs

Once you have SSH access to a macOS VM, continue at step 6 below.

​Quick path (Lume, experienced users)

- Install Lume

- `lume create openclaw --os macos --ipsw latest`

- Complete Setup Assistant, enable Remote Login (SSH)

- `lume run openclaw --no-display`

- SSH in, install OpenClaw, configure channels

- Done

​What you need (Lume)

- Apple Silicon Mac (M1/M2/M3/M4)

- macOS Sequoia or later on the host

- ~60 GB free disk space per VM

- ~20 minutes

​1) Install Lume
Copy```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"

```

If `~/.local/bin` isn’t in your PATH:
Copy```
echo &#x27;export PATH="$PATH:$HOME/.local/bin"&#x27; >> ~/.zshrc && source ~/.zshrc

```

Verify:
Copy```
lume --version

```

Docs: [Lume Installation](https://cua.ai/docs/lume/guide/getting-started/installation)

​2) Create the macOS VM
Copy```
lume create openclaw --os macos --ipsw latest

```

This downloads macOS and creates the VM. A VNC window opens automatically.
Note: The download can take a while depending on your connection.

​3) Complete Setup Assistant
In the VNC window:

- Select language and region

- Skip Apple ID (or sign in if you want iMessage later)

- Create a user account (remember the username and password)

- Skip all optional features

After setup completes, enable SSH:

- Open System Settings → General → Sharing

- Enable “Remote Login”

​4) Get the VM’s IP address
Copy```
lume get openclaw

```

Look for the IP address (usually `192.168.64.x`).

​5) SSH into the VM
Copy```
ssh youruser@192.168.64.X

```

Replace `youruser` with the account you created, and the IP with your VM’s IP.

​6) Install OpenClaw
Inside the VM:
Copy```
npm install -g openclaw@latest
openclaw onboard --install-daemon

```

Follow the onboarding prompts to set up your model provider (Anthropic, OpenAI, etc.).

​7) Configure channels
Edit the config file:
Copy```
nano ~/.openclaw/openclaw.json

```

Add your channels:
Copy```
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
Copy```
openclaw channels login

```

​8) Run the VM headlessly
Stop the VM and restart without display:
Copy```
lume stop openclaw
lume run openclaw --no-display

```

The VM runs in the background. OpenClaw’s daemon keeps the gateway running.
To check status:
Copy```
ssh youruser@192.168.64.X "openclaw status"

```

​Bonus: iMessage integration
This is the killer feature of running on macOS. Use [BlueBubbles](https://bluebubbles.app) to add iMessage to OpenClaw.
Inside the VM:

- Download BlueBubbles from bluebubbles.app

- Sign in with your Apple ID

- Enable the Web API and set a password

- Point BlueBubbles webhooks at your gateway (example: `https://your-gateway-host:3000/bluebubbles-webhook?password=<password>`)

Add to your OpenClaw config:
Copy```
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

Restart the gateway. Now your agent can send and receive iMessages.
Full setup details: [BlueBubbles channel](/channels/bluebubbles)

​Save a golden image
Before customizing further, snapshot your clean state:
Copy```
lume stop openclaw
lume clone openclaw openclaw-golden

```

Reset anytime:
Copy```
lume stop openclaw && lume delete openclaw
lume clone openclaw-golden openclaw
lume run openclaw --no-display

```

​Running 24/7
Keep the VM running by:

- Keeping your Mac plugged in

- Disabling sleep in System Settings → Energy Saver

- Using `caffeinate` if needed

For true always-on, consider a dedicated Mac mini or a small VPS. See [VPS hosting](/vps).

​Troubleshooting
ProblemSolutionCan’t SSH into VMCheck “Remote Login” is enabled in VM’s System SettingsVM IP not showingWait for VM to fully boot, run `lume get openclaw` againLume command not foundAdd `~/.local/bin` to your PATHWhatsApp QR not scanningEnsure you’re logged into the VM (not host) when running `openclaw channels login`

​Related docs

- [VPS hosting](/vps)

- [Nodes](/nodes)

- [Gateway remote](/gateway/remote)

- [BlueBubbles channel](/channels/bluebubbles)

- [Lume Quickstart](https://cua.ai/docs/lume/guide/getting-started/quickstart)

- [Lume CLI Reference](https://cua.ai/docs/lume/reference/cli-reference)

- [Unattended VM Setup](https://cua.ai/docs/lume/guide/fundamentals/unattended-setup) (advanced)

- [Docker Sandboxing](/install/docker) (alternative isolation approach)

GCPexe.dev⌘I