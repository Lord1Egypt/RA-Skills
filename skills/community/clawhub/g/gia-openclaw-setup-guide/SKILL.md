# OpenClaw Setup Guide Skill

Help users install and configure OpenClaw from scratch. Covers installation, channel connection, skill setup, and first automation workflow.

## What This Skill Does

Guides a new OpenClaw user through:
1. Installing OpenClaw on their machine (Mac/Linux/Windows WSL)
2. Running the onboarding wizard
3. Connecting messaging channels (Telegram, Discord, WhatsApp, Slack)
4. Installing and configuring skills
5. Setting up their first automation workflow
6. Configuring heartbeats and cron jobs
7. Setting up memory and identity files

## Usage

When a user asks for help setting up OpenClaw, follow these steps in order:

### Step 1: System Check
```bash
# Check OS and prerequisites
uname -a
node --version  # Need Node.js 18+
git --version
```

### Step 2: Install OpenClaw
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

### Step 3: Connect a Channel
```bash
# For Telegram (most common)
openclaw channels add telegram
# Follow prompts for bot token from @BotFather

# For Discord
openclaw channels add discord
# Provide bot token from Discord Developer Portal
```

### Step 4: Configure Identity
Create these files in the workspace:
- `SOUL.md` — Agent personality and behavior
- `USER.md` — Information about the human
- `AGENTS.md` — Operating procedures
- `IDENTITY.md` — Name, emoji, avatar

### Step 5: Install Skills
```bash
# Browse available skills
openclaw skills search <keyword>

# Install a skill
openclaw skills install <skill-name>
```

### Step 6: Set Up Automation
- Configure heartbeat interval in openclaw config
- Set up cron jobs for recurring tasks
- Create HEARTBEAT.md for proactive behaviors

### Step 7: First Workflow Test
Send a message to your agent on the connected channel. Try:
- "Search the web for [topic]"
- "Read and summarize [file]"
- "Set a reminder for [time]"

## Troubleshooting

### Common Issues
- **Node.js version too old**: `nvm install 22 && nvm use 22`
- **Permission denied**: `sudo chown -R $USER ~/.openclaw`
- **Bot not responding**: Check `openclaw status` and `openclaw gateway logs`
- **Channel connection failed**: Verify token, check firewall/proxy settings

## Requirements
- Node.js 18+ (22 recommended)
- 2GB RAM minimum
- macOS, Linux, or Windows with WSL2
- Internet connection for API calls

## Cost
- OpenClaw itself: Free (open source)
- AI model API: ~$5-50/month depending on usage
- Hosting (optional): $5-20/month for always-on
