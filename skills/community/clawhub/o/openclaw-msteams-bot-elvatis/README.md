# openclaw-teams-elvatis

Microsoft Teams connector plugin for [OpenClaw Gateway](https://github.com/openclaw/openclaw). Bridges Teams channels to OpenClaw AI sessions with per-channel system prompts, model configuration, and full Azure Bot Framework authentication.

## Features

- **Per-channel sessions** - each Teams channel maps to its own OpenClaw session
- **Per-channel system prompts** - configure different AI personas per channel (Accounting, Marketing, HR, General)
- **Per-channel model selection** - override the default model per channel
- **Single-tenant & multi-tenant** - supports both Azure AD configurations
- **Typing indicators** - shows typing activity while waiting for a response
- **1:1, group chat, and channel support** - works everywhere in Teams
- **Bot Framework authentication** - all requests verified via Azure JWT tokens

---

## Step-by-Step Deployment Guide

### Prerequisites

- A server with Node.js 18+ and OpenClaw Gateway installed
- A domain with HTTPS (e.g. `teams-bot.yourdomain.com`)
- A Microsoft Azure account with permission to create Bot registrations
- An OpenClaw API key (Anthropic or other provider)

---

### Step 1: Create Azure Bot Registration

1. Open the [Azure Portal](https://portal.azure.com)
2. Search for **"Azure Bot"** → click **Create**
3. Fill in:
   - **Bot handle**: e.g. `your-company-bot`
   - **Subscription + Resource Group**: select existing or create new
   - **Pricing tier**: F0 (free) is fine for getting started
   - **Microsoft App ID**: choose **"Create new Microsoft App ID"**
   - **Type**: Single Tenant (recommended for internal org bots)
4. Click **Review + Create** → **Create**
5. Once deployed, open the Bot resource → **Configuration**
6. Note the **Microsoft App ID** (you need this later)
7. Click **"Manage Password"** → **"New client secret"**
   - Give it a name and expiry (e.g. 24 months)
   - **Copy the secret value immediately** - you cannot see it again

---

### Step 2: Enable the Teams Channel

1. In your Azure Bot resource → **Channels**
2. Click **Microsoft Teams**
3. Accept the terms of service → **Save**
4. The bot is now registered as a Teams app

---

### Step 3: Set Up the Server

On your server, install OpenClaw if not already done:

```bash
npm install -g openclaw
openclaw gateway install
systemctl --user enable openclaw-gateway
systemctl --user start openclaw-gateway
```

Create the plugin directory:

```bash
mkdir -p ~/.openclaw/workspace/plugins/openclaw-teams-elvatis
cd ~/.openclaw/workspace/plugins/openclaw-teams-elvatis
```

Clone this repo and build:

```bash
git clone https://github.com/elvatis/openclaw-teams-elvatis.git .
npm install
npm run build
# Copy compiled JS files to plugin root
cp dist/src/index.js dist/src/bot.js dist/src/session.js dist/src/types.js ./
```

---

### Step 4: Configure OpenClaw

Add the plugin to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "allow": ["openclaw-teams-elvatis"],
    "load": {
      "paths": ["/home/YOUR_USER/.openclaw/workspace/plugins/openclaw-teams-elvatis"]
    },
    "entries": {
      "openclaw-teams-elvatis": {
        "enabled": true,
        "config": {
          "appId": "YOUR_MICROSOFT_APP_ID",
          "appPassword": "YOUR_MICROSOFT_APP_PASSWORD",
          "appTenantId": "YOUR_AZURE_TENANT_ID",
          "port": 3978,
          "channels": {
            "General": {
              "label": "teams-general",
              "systemPrompt": "You are the company AI assistant. Answer questions and help with work tasks.",
              "model": "anthropic/claude-sonnet-4-6"
            },
            "Accounting": {
              "label": "teams-accounting",
              "systemPrompt": "You are the accounting assistant. Help with invoices, expenses, and bookkeeping.",
              "model": "anthropic/claude-sonnet-4-6"
            }
          }
        }
      }
    }
  }
}
```

> **Note:** `appTenantId` is only required for single-tenant bots. Find it in Azure Portal → Azure Active Directory → Overview → "Directory (tenant) ID".

Restart the gateway:

```bash
systemctl restart elvatis-agent-openclaw
# Or for user services:
systemctl --user restart openclaw-gateway
```

---

### Step 5: Set Up Apache Reverse Proxy with SSL

Install Certbot and get a certificate:

```bash
apt install certbot python3-certbot-apache
certbot --apache -d teams-bot.yourdomain.com
```

Apache vHost config (e.g. via ISPConfig or manually):

```apache
<VirtualHost *:443>
    ServerName teams-bot.yourdomain.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/teams-bot.yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/teams-bot.yourdomain.com/privkey.pem

    ProxyPreserveHost On
    RewriteEngine On

    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule /(.*) ws://127.0.0.1:3978/$1 [P,L]

    RewriteRule ^/(.*)$ http://127.0.0.1:3978/$1 [P,L]
    ProxyPassReverse / http://127.0.0.1:3978/

    # Disable ModSecurity for Bot Framework endpoint
    <Location /api/messages>
        SecRuleEngine Off
    </Location>
</VirtualHost>
```

Reload Apache:

```bash
apache2ctl configtest && apache2ctl graceful
```

---

### Step 6: Set the Messaging Endpoint in Azure

1. Azure Portal → your Bot resource → **Configuration**
2. Set **Messaging endpoint**:
   ```
   https://teams-bot.yourdomain.com/api/messages
   ```
3. Click **Save**

Test with the built-in **Web Chat** in Azure Portal → Channels → Web Chat → **"Test in Web Chat"**.
If the bot responds there, the endpoint is working correctly.

---

### Step 7: Create the Teams App Manifest

Create a `manifest.json`:

```json
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.17/MicrosoftTeams.schema.json",
  "manifestVersion": "1.17",
  "version": "1.0.0",
  "id": "YOUR_MICROSOFT_APP_ID",
  "developer": {
    "name": "Your Company",
    "websiteUrl": "https://yourcompany.com",
    "privacyUrl": "https://yourcompany.com/privacy",
    "termsOfUseUrl": "https://yourcompany.com/terms"
  },
  "name": {
    "short": "Akido",
    "full": "Akido – Company AI Assistant"
  },
  "description": {
    "short": "Internal AI assistant for your team.",
    "full": "AI assistant powered by OpenClaw. Helps with research, writing, strategy, and knowledge questions."
  },
  "icons": {
    "color": "color.png",
    "outline": "outline.png"
  },
  "accentColor": "#1a1a2e",
  "bots": [
    {
      "botId": "YOUR_MICROSOFT_APP_ID",
      "scopes": ["personal", "team", "groupchat"],
      "supportsFiles": true,
      "isNotificationOnly": false,
      "commandLists": [
        {
          "scopes": ["personal", "team", "groupchat"],
          "commands": [
            { "title": "Help", "description": "Shows available commands" },
            { "title": "Status", "description": "Shows the current status" }
          ]
        }
      ]
    }
  ],
  "permissions": ["identity", "messageTeamMembers"],
  "validDomains": ["yourcompany.com", "teams-bot.yourcompany.com"]
}
```

Pack the zip (files must be in the **root**, not in a subfolder):

```bash
# Correct:
zip manifest.zip manifest.json color.png outline.png

# Wrong (don't do this):
zip -r manifest.zip manifest-folder/
```

---

### Step 8: Deploy the App in Microsoft Teams

**As an admin (recommended for org-wide deployment):**

1. Open [admin.teams.microsoft.com](https://admin.teams.microsoft.com)
2. **Teams apps → Manage apps** → **Upload new app** → upload your `manifest.zip`
3. Find the app → set status to **Allowed**
4. **Teams apps → Setup policies** → Global policy → **Add apps** → add your bot
5. This makes the bot available to all users (can take up to 24h to propagate)

**For personal testing (sideloading):**

1. In Teams → Apps (left sidebar) → **Manage your apps**
2. **Upload an app** → **Upload a custom app** → select your `manifest.zip`
3. The bot is now available for you personally

---

### Step 9: Add the Bot to a Channel

1. Open the Teams channel → click **+** (Add a tab) or **...** → **Apps**
2. Search for your bot name → **"Add to a team"**
3. Select the channel → **Set up**

Or simply type `@YourBotName` in the channel message box - Teams will prompt you to add the bot.

**Using the bot:**
- In channels: `@Akido What are our current projects?`
- In direct messages: Just write normally, no `@` needed
- In group chats: `@Akido Summarize this conversation`

---

## Image & File Support

The bot supports file attachments sent via the paperclip icon in Teams.

**Supported types:**
- Images (PNG, JPG, GIF, WebP) - analysed by the AI vision model
- Text files (.txt, .md, .csv, .json, .ts, .js, .py, etc.) - content included inline
- SharePoint/OneDrive files - fetched automatically via download URL

**How to send a file:**
1. Click the paperclip icon in the Teams message box
2. Select your file
3. Send - the bot will analyse and respond

**Note:** Inline images (Ctrl+V / paste) have limited support due to Teams CDN authentication. For best results, use the paperclip attachment method.

**Chat history** is automatically persisted per channel as JSONL session files. The bot remembers previous conversations within each channel session.

---

### Smoke Tests

After deployment, run these checks:

```bash
# 1. Health check
curl https://teams-bot.yourdomain.com/health
# Expected: {"status":"ok","plugin":"openclaw-teams-elvatis"}

# 2. Bot Framework endpoint (should return 401 Unauthorized - correct!)
curl -X POST https://teams-bot.yourdomain.com/api/messages
# Expected: HTTP 401

# 3. Gateway status
systemctl status elvatis-agent-openclaw
# Expected: active (running)

# 4. Port check
ss -tlnp | grep 3978
# Expected: LISTEN on *:3978
```

---

### Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` from external POST | Bot Framework auth working correctly | Normal - only Azure can send valid JWTs |
| `503 Service Unavailable` | Apache proxy can't reach port 3978 | Check `ss -tlnp \| grep 3978`, restart gateway |
| `Invalid session ID` error in logs | Teams channel ID contains special chars | Fixed in v0.1.1+ (session ID is sanitized) |
| Bot responds `{"ok":true}` instead of text | Wrong JSON path parsing | Fixed in v0.1.1+ (`result.payloads[0].text`) |
| `Missing register/activate export` | Old plugin build in wrong directory | Copy `dist/src/*.js` files to plugin root |
| Bot doesn't respond in channels | Bot not added to channel | Type `@BotName` in channel, confirm add |
| App not visible in Teams admin center | Manifest zip structure wrong | Files must be in zip root, not in a subfolder |
| Inline image (paste) not analysed | Teams CDN auth restriction | Attach as file via paperclip instead |
| Long response truncated in Teams | Teams 28KB message limit | Response is automatically split into multiple messages |

---

### Architecture

```
Microsoft Teams
      │
      │ HTTPS POST /api/messages (JWT signed by Azure)
      ▼
Apache Reverse Proxy (teams-bot.yourdomain.com)
      │
      │ HTTP → 127.0.0.1:3978
      ▼
openclaw-teams-elvatis plugin (Bot Framework Express server)
      │
      │ openclaw agent --message "..." --session-id "..." --json
      ▼
OpenClaw Gateway (ws://127.0.0.1:18789)
      │
      │ Anthropic API / other model provider
      ▼
AI Response → back through the chain → Teams channel
```

---

### Configuration Reference

| Property | Type | Required | Description |
|---|---|---|---|
| `appId` | string | ✅ | Microsoft App ID from Azure Bot |
| `appPassword` | string | ✅ | Azure App client secret |
| `appTenantId` | string | Single-tenant only | Azure AD Tenant/Directory ID |
| `port` | number | | Bot server port (default: 3978) |
| `channels` | object | | Per-channel config (key = channel name) |

**Per-channel options:**

| Property | Type | Description |
|---|---|---|
| `label` | string | OpenClaw session label |
| `systemPrompt` | string | AI system prompt for this channel |
| `model` | string | Model override (e.g. `anthropic/claude-sonnet-4-6`) |

---

## Development

```bash
npm install
npm run build      # compile TypeScript
npm run dev        # watch mode
```

Plugin entry point: `src/index.ts`
Bot Framework server: `src/bot.ts`
Session management: `src/session.ts`

## License

Apache-2.0 - Copyright 2026 Elvatis - Emre Kohler
