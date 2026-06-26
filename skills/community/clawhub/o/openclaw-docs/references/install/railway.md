# Deploy on Railway

Source: https://docs.openclaw.ai/install/railway

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationHosting and deploymentDeploy on RailwayGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
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
- [Quick checklist (new users)](#quick-checklist-new-users)
- [One-click deploy](#one-click-deploy)
- [What you get](#what-you-get)
- [Required Railway settings](#required-railway-settings)
- [Public Networking](#public-networking)
- [Volume (required)](#volume-required)
- [Variables](#variables)
- [Setup flow](#setup-flow)
- [Getting chat tokens](#getting-chat-tokens)
- [Telegram bot token](#telegram-bot-token)
- [Discord bot token](#discord-bot-token)
- [Backups & migration](#backups-%26-migration)

Deploy OpenClaw on Railway with a one-click template and finish setup in your browser.
This is the easiest “no terminal on the server” path: Railway runs the Gateway for you,
and you configure everything via the `/setup` web wizard.
​Quick checklist (new users)

- Click **Deploy on Railway** (below).

- Add a **Volume** mounted at `/data`.

- Set the required **Variables** (at least `SETUP_PASSWORD`).

- Enable **HTTP Proxy** on port `8080`.

- Open `https://<your-railway-domain>/setup` and finish the wizard.

​One-click deploy
Deploy on Railway
After deploy, find your public URL in **Railway → your service → Settings → Domains**.
Railway will either:

- give you a generated domain (often `https://<something>.up.railway.app`), or

- use your custom domain if you attached one.

Then open:

- `https://<your-railway-domain>/setup` — setup wizard (password protected)

- `https://<your-railway-domain>/openclaw` — Control UI

​What you get

- Hosted OpenClaw Gateway + Control UI

- Web setup wizard at `/setup` (no terminal commands)

- Persistent storage via Railway Volume (`/data`) so config/credentials/workspace survive redeploys

- Backup export at `/setup/export` to migrate off Railway later

​Required Railway settings
​Public Networking
Enable **HTTP Proxy** for the service.

- Port: `8080`

​Volume (required)
Attach a volume mounted at:

- `/data`

​Variables
Set these variables on the service:

- `SETUP_PASSWORD` (required)

- `PORT=8080` (required — must match the port in Public Networking)

- `OPENCLAW_STATE_DIR=/data/.openclaw` (recommended)

- `OPENCLAW_WORKSPACE_DIR=/data/workspace` (recommended)

- `OPENCLAW_GATEWAY_TOKEN` (recommended; treat as an admin secret)

​Setup flow

- Visit `https://<your-railway-domain>/setup` and enter your `SETUP_PASSWORD`.

- Choose a model/auth provider and paste your key.

- (Optional) Add Telegram/Discord/Slack tokens.

- Click **Run setup**.

If Telegram DMs are set to pairing, the setup wizard can approve the pairing code.
​Getting chat tokens
​Telegram bot token

- Message `@BotFather` in Telegram

- Run `/newbot`

- Copy the token (looks like `123456789:AA...`)

- Paste it into `/setup`

​Discord bot token

- Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)

- **New Application** → choose a name

- **Bot** → **Add Bot**

- **Enable MESSAGE CONTENT INTENT** under Bot → Privileged Gateway Intents (required or the bot will crash on startup)

- Copy the **Bot Token** and paste into `/setup`

- Invite the bot to your server (OAuth2 URL Generator; scopes: `bot`, `applications.commands`)

​Backups & migration
Download a backup at:

- `https://<your-railway-domain>/setup/export`

This exports your OpenClaw state + workspace so you can migrate to another host without losing config or memory.exe.devDeploy on Render⌘I