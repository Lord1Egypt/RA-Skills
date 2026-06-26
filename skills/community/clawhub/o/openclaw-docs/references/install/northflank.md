# Deploy on Northflank

Source: https://docs.openclaw.ai/install/northflank

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationHosting and deploymentDeploy on NorthflankGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
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
- [How to get started](#how-to-get-started)
- [What you get](#what-you-get)
- [Setup flow](#setup-flow)
- [Getting chat tokens](#getting-chat-tokens)
- [Telegram bot token](#telegram-bot-token)
- [Discord bot token](#discord-bot-token)

Deploy OpenClaw on Northflank with a one-click template and finish setup in your browser.
This is the easiest “no terminal on the server” path: Northflank runs the Gateway for you,
and you configure everything via the `/setup` web wizard.
​How to get started

- Click [Deploy OpenClaw](https://northflank.com/stacks/deploy-openclaw) to open the template.

- Create an [account on Northflank](https://app.northflank.com/signup) if you don’t already have one.

- Click **Deploy OpenClaw now**.

- Set the required environment variable: `SETUP_PASSWORD`.

- Click **Deploy stack** to build and run the OpenClaw template.

- Wait for the deployment to complete, then click **View resources**.

- Open the OpenClaw service.

- Open the public OpenClaw URL and complete setup at `/setup`.

- Open the Control UI at `/openclaw`.

​What you get

- Hosted OpenClaw Gateway + Control UI

- Web setup wizard at `/setup` (no terminal commands)

- Persistent storage via Northflank Volume (`/data`) so config/credentials/workspace survive redeploys

​Setup flow

- Visit `https://<your-northflank-domain>/setup` and enter your `SETUP_PASSWORD`.

- Choose a model/auth provider and paste your key.

- (Optional) Add Telegram/Discord/Slack tokens.

- Click **Run setup**.

- Open the Control UI at `https://<your-northflank-domain>/openclaw`

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

Deploy on RenderDevelopment Channels⌘I