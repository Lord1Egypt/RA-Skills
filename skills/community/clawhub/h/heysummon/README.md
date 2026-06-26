# 🦞 HeySummon Consumer Skill

> Get help from human experts when your AI agent gets stuck.

HeySummon is a Human-in-the-Loop (HITL) service that connects AI agents with human experts in real-time. This skill provides a secure, encrypted communication channel between OpenClaw agents and HeySummon providers.

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Scripts Reference](#scripts-reference)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

---

## ✨ Features

- 🔐 **End-to-end encryption** (E2E) via X25519 + Ed25519
- 📡 **Real-time notifications** via Server-Sent Events (SSE)
- 🏷️ **Multi-provider support** with friendly name routing
- 🔄 **Auto-sync** to GitHub (optional cron job)
- 🛡️ **Secure by default** — no credentials in code or commits
- 🚀 **pm2 integration** for production reliability

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  OpenClaw Agent (You)                    │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │ HeySummon Consumer Skill                        │   │
│  │                                                   │   │
│  │  1. Submit Request ──> Platform API              │   │
│  │  2. Platform Watcher ←── SSE Stream              │   │
│  │  3. Notification ──────> OpenClaw                │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────┐
│              HeySummon Platform (Server)                 │
│                                                           │
│  • POST /api/v1/help        (submit request)            │
│  • GET  /api/v1/events/stream (SSE notifications)       │
│  • GET  /api/v1/whoami      (provider info)             │
│  • GET  /api/v1/messages/:id (fetch messages)           │
│                                                           │
│  🔒 E2E Encryption Server-Side                           │
│  📡 Real-time Event Streaming                            │
└─────────────────────────────────────────────────────────┘
                           │
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              HeySummon Provider (Expert)                 │
│                                                           │
│  • Receives requests via provider dashboard              │
│  • Responds with expert advice                           │
│  • Uses same E2E encryption                              │
└─────────────────────────────────────────────────────────┘
```

**Key Points:**
- All communication goes through the **HeySummon Platform API** (no direct P2P)
- **E2E encryption** is handled **server-side** by the platform
- **SSE stream** delivers real-time events (key exchange, messages, status)
- **OpenClaw** receives notifications and routes them to your chat

---

## 📦 Installation

### Prerequisites

- **Node.js** (for crypto.mjs)
- **curl** (for API calls)
- **jq** (for JSON parsing)
- **pm2** (optional, for production watcher)
- **OpenClaw** (for notifications)

### Setup

1. **Clone or install the skill:**
   ```bash
   # Already installed in your OpenClaw workspace
   cd ~/clawd-sonny/skills/heysummon
   ```

2. **Create `.env` file:**
   ```bash
   cp .env.example .env
   # Edit .env with your API key and platform URL
   ```

3. **Register your first provider:**
   ```bash
   bash scripts/add-provider.sh "hs_cli_your_key_here" "ProviderName"
   ```

4. **Start the event watcher:**
   ```bash
   bash scripts/setup.sh
   ```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

Create a `.env` file in the skill directory:

```env
# HeySummon Platform URL
HEYSUMMON_BASE_URL=http://localhost:3445

# Your client API key (get this from platform dashboard)
HEYSUMMON_API_KEY=hs_cli_your_key_here

# Notification settings (for OpenClaw routing)
HEYSUMMON_NOTIFY_MODE=message
HEYSUMMON_NOTIFY_TARGET=telegram_target_chat_id_here

# Optional: custom paths (defaults shown)
# HEYSUMMON_KEY_DIR=.keys
# HEYSUMMON_REQUESTS_DIR=.requests
# HEYSUMMON_PROVIDERS_FILE=providers.json
```

### Platform URL Options

- **Self-hosted:** `http://localhost:3445` (default)
- **Cloud:** `https://cloud.heysummon.ai`
- **Custom server:** `https://heysummon.yourdomain.com`

### API Key Format

- ✅ **Client key:** `hs_cli_...` or `htl_cli_...`
- ❌ **Provider key:** `hs_prov_...` (will be rejected)

Get your client key from the HeySummon dashboard:
1. Go to **Users** → Create user profile
2. Click **Create Client Key**
3. Copy the `hs_cli_...` key

---

## 🚀 Usage

### 1. Submit a Help Request

**To a specific provider:**
```bash
bash scripts/submit-request.sh \
  "How do I configure Nginx reverse proxy?" \
  '[{"role":"user","content":"I am stuck on SSL setup"}]' \
  "DevOpsExpert"
```

**To default provider (from `.env`):**
```bash
bash scripts/submit-request.sh \
  "How do I fix this error?" \
  '[]'
```

**Output:**
```
📡 Provider: DevOpsExpert
✅ Request submitted
📨 Request ID: cmm123abc...
🔖 Ref Code: HS-A1B2
⏳ Status: pending
📡 Consumer watcher already running
```

### 2. Wait for Notifications

The platform watcher will automatically notify you when:
- 🔑 Provider connects (key exchange)
- 📩 Provider responds
- 🔒 Conversation is closed

Notifications appear in your configured OpenClaw chat.

### 3. Check Request Status (Optional)

```bash
bash scripts/check-status.sh cmm123abc...
```

---

## 📚 Scripts Reference

### Core Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup.sh` | Start platform watcher | `bash scripts/setup.sh` |
| `teardown.sh` | Stop platform watcher | `bash scripts/teardown.sh` |
| `submit-request.sh` | Submit help request | See [Usage](#usage) |
| `add-provider.sh` | Register provider | `bash scripts/add-provider.sh <key> <name>` |
| `list-providers.sh` | List providers | `bash scripts/list-providers.sh` |
| `check-status.sh` | Check request status | `bash scripts/check-status.sh <request-id>` |

### Background Scripts

| Script | Purpose | When Used |
|--------|---------|-----------|
| `platform-watcher.sh` | SSE event listener | Started by `setup.sh` |
| `crypto.mjs` | E2E encryption | Auto-called by setup/submit |
| `auto-sync.sh` | Git auto-sync | Cron job (optional) |

### Script Details

#### `setup.sh`

Starts the platform event watcher as a background process.

**Behavior:**
- Generates keypairs if they don't exist
- Uses `pm2` if available, otherwise `nohup`
- Creates `.requests/` directory for tracking active requests

**Output:**
```
⚠️ No keypairs found. Generating in .keys...
✅ Keypairs generated in .keys
✅ Consumer watcher started via pm2 (name: heysummon-watcher)
```

#### `submit-request.sh`

Submits a help request to the HeySummon platform.

**Arguments:**
1. **Question** (required): The question to ask the expert
2. **Messages** (optional): JSON array of conversation context (default: `[]`)
3. **Provider** (optional): Provider name from `providers.json` (default: uses `HEYSUMMON_API_KEY`)

**Example:**
```bash
bash scripts/submit-request.sh \
  "How do I set up GitHub Actions?" \
  '[{"role":"user","content":"I need CI/CD help"}]' \
  "CIExpert"
```

#### `add-provider.sh`

Registers a provider by fetching their name from the platform.

**Arguments:**
1. **API Key** (required): Client API key (`hs_cli_...`)
2. **Friendly Name** (optional): Override name (default: uses platform name)

**Example:**
```bash
bash scripts/add-provider.sh "hs_cli_abc123..." "MyExpert"
```

**Output:**
```
✅ Provider added: MyExpert (John Doe)
📋 Providers registered: 2
```

#### `platform-watcher.sh`

Background process that listens to the platform's SSE event stream.

**Events handled:**
- `keys_exchanged` — Provider connected
- `new_message` — Provider sent a message
- `responded` — Provider responded
- `closed` — Conversation closed

**Notifications sent via:**
- OpenClaw `message` tool (if `NOTIFY_MODE=message`)
- JSONL file (if `NOTIFY_MODE=file`)

---

## 🔒 Security

### What's Protected

✅ **Gitignored (never committed):**
- `.env` (API keys)
- `providers.json` (contains API keys)
- `.keys/` (encryption keypairs)
- `.requests/` (active request tracking)
- `*.jsonl` (event logs)

✅ **Path Security:**
- All paths are **relative** to skill directory
- No hardcoded user paths (no `~` or `/home/user/...`)
- Configurable via environment variables

✅ **API Key Security:**
- Only stored in `.env` (gitignored)
- Never passed as CLI arguments (except in `add-provider.sh`, which writes to gitignored file)
- Validated format (`hs_cli_...` or `htl_cli_...`)

✅ **Encryption:**
- E2E encryption handled by platform (server-side)
- Client keypairs generated locally (Ed25519 + X25519)
- Keys stored in `.keys/` (gitignored)

### Security Best Practices

1. **Never commit credentials:**
   ```bash
   # Already in .gitignore:
   .env
   providers.json
   .keys/
   .requests/
   *.pem
   ```

2. **Use environment variables:**
   - Don't hardcode API keys
   - Don't hardcode platform URLs

3. **Rotate API keys regularly:**
   - Generate new client key in platform dashboard
   - Update `.env`
   - Re-register providers

4. **Restrict file permissions:**
   ```bash
   chmod 600 .env
   chmod 700 .keys/
   ```

---

## 🐛 Troubleshooting

### Watcher Not Starting

**Problem:** `setup.sh` fails or watcher exits immediately

**Solutions:**
1. Check if `.env` exists and has valid `HEYSUMMON_API_KEY`
2. Verify platform is reachable: `curl -s ${HEYSUMMON_BASE_URL}/health`
3. Check pm2 logs: `pm2 logs heysummon-watcher`
4. Check nohup logs: `tail scripts/watcher.log`

### No Notifications Received

**Problem:** Provider responded but you didn't get notified

**Solutions:**
1. Check watcher status: `pm2 status` or `ps aux | grep platform-watcher`
2. Verify `HEYSUMMON_NOTIFY_TARGET` is correct chat ID
3. Check OpenClaw is running: `curl http://localhost:18789/health`
4. Restart watcher: `bash scripts/teardown.sh && bash scripts/setup.sh`

### Invalid API Key Error

**Problem:** `{"error":"Invalid or inactive API key"}`

**Solutions:**
1. Verify key format starts with `hs_cli_` (not `hs_prov_`)
2. Check key is active in platform dashboard
3. Ensure `.env` has correct `HEYSUMMON_BASE_URL`
4. Test with: `curl -s ${BASE_URL}/api/v1/whoami -H "x-api-key: ${KEY}"`

### Provider Not Found

**Problem:** `Provider 'XYZ' not found in providers.json`

**Solutions:**
1. List providers: `bash scripts/list-providers.sh`
2. Add provider: `bash scripts/add-provider.sh <key> <name>`
3. Check `providers.json` exists and has valid JSON

---

## 🔧 Development

### Directory Structure

```
heysummon/
├── .env                    # Config (gitignored)
├── .gitignore             # Excludes secrets
├── SKILL.md               # Skill documentation (for OpenClaw)
├── README.md              # This file
├── providers.json         # Provider registry (gitignored)
├── .keys/                 # Encryption keypairs (gitignored)
├── .requests/             # Active request tracking (gitignored)
└── scripts/
    ├── setup.sh           # Start watcher
    ├── teardown.sh        # Stop watcher
    ├── platform-watcher.sh # SSE event listener
    ├── submit-request.sh  # Submit help request
    ├── add-provider.sh    # Register provider
    ├── list-providers.sh  # List providers
    ├── check-status.sh    # Check request status
    ├── crypto.mjs         # E2E encryption
    └── auto-sync.sh       # Git auto-sync
```

### Adding a New Provider

```bash
# Get client key from platform dashboard
CLIENT_KEY="hs_cli_abc123..."

# Register provider
bash scripts/add-provider.sh "$CLIENT_KEY" "ExpertName"

# Verify
bash scripts/list-providers.sh
```

### Testing a Request

```bash
# Submit test request
bash scripts/submit-request.sh \
  "Test question" \
  '[]' \
  "YourProvider"

# Check watcher logs
pm2 logs heysummon-watcher --lines 50

# Check request status
bash scripts/check-status.sh <request-id-from-output>
```

### Auto-Sync Setup (Optional)

Sync skill to GitHub every hour:

```bash
# Already configured in cron:
0 * * * * /path/to/skills/heysummon/scripts/auto-sync.sh >> /tmp/heysummon-skill-sync.log 2>&1
```

Manually trigger sync:
```bash
bash scripts/auto-sync.sh
```

---

## 📝 License

This skill is part of the OpenClaw ecosystem.

---

## 🤝 Support

- **Issues:** Open an issue on the GitHub repo
- **Questions:** Ask via HeySummon (meta! 🦞)
- **Docs:** See [SKILL.md](SKILL.md) for OpenClaw-specific usage

---

**Made with ⭐ by Patrick the Starfish**
