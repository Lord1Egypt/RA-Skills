--- 
name: openclaw-quickstart-setup
description: Complete OpenClaw setup automation skill. Installs gateway, hardens security (localhost binding, auth), routes to cost-effective models (DeepSeek/Kimi for simple tasks, Claude/Opus for complex), connects channels (Telegram/WhatsApp/Discord), and deploys useful starter workflows (daily brief, email triage, heartbeat). Born from real production experience — every step tested and debugged. Zero to running in under 30 minutes.
---

# OpenClaw Quickstart Setup

Production-tested setup flow for OpenClaw/Moltbot. Every step comes from real deployments — not theory.

## Prerequisites Check

```bash
node --version  # Needs 22.16+ (24 recommended)
npm --version
```

If Node is too old: `nvm install 24`

## Step 1: Install & Initialize

```bash
npm i -g openclaw
openclaw init
```

## Step 2: Security Hardening (DO THIS FIRST)

### Bind to localhost (prevent public exposure)
```json
// openclaw.json
{
  "gateway": {
    "bind": "127.0.0.1"
  }
}
```

**Why:** CVE-2026-25253 ("Clawbleed") exploited default 0.0.0.0 binding. 63% of 42K+ exposed instances had zero auth. This is literally 30 seconds of work.

### Enable authentication
```json
{
  "gateway": {
    "auth": true
  }
}
```

For remote access: Use Tailscale. Never expose directly.

## Step 3: Cost-Effective Model Routing

The biggest money-saver. Route simple tasks to cheap models, reserve expensive ones for complex reasoning:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-chat",
        "fallbacks": ["nvidia/nemotron-nano-12b-v2"]
      },
      "imageModel": {
        "primary": "moonshotai/kimi-k2.5"
      }
    }
  }
}
```

**Cost comparison (monthly for moderate use):**
- All Claude Opus: ~$420/month
- All GPT-5.4: ~$300/month  
- Routed (DeepSeek + Kimi + fallback): ~$15-30/month
- **Savings: 70-90%**

### Task-based routing in prompts
```
For simple tasks (formatting, lists, translations): use default model
For complex reasoning (debugging, architecture, analysis): use /model command to switch
For vision/image tasks: uses imageModel automatically
```

## Step 4: Channel Connection

### Telegram (most popular)
1. Message @BotFather on Telegram
2. `/newbot` → get API token
3. Configure:
```json
{
  "channels": {
    "telegram": {
      "adapter": "telegram",
      "token": "YOUR_BOT_TOKEN"
    }
  }
}
```

### WhatsApp (via WA CLI)
```bash
openclaw skills install wacli
```
Follow WA CLI skill instructions for QR code pairing.

### Discord
```json
{
  "channels": {
    "discord": {
      "adapter": "discord",
      "token": "YOUR_BOT_TOKEN"
    }
  }
}
```

## Step 5: Starter Workflows

### Daily Brief (cron)
```json
{
  "cron": [{
    "name": "daily-brief",
    "schedule": {"kind": "cron", "expr": "0 8 * * *", "tz": "UTC"},
    "sessionTarget": "main",
    "payload": {"kind": "systemEvent", "text": "DAILY BRIEF: Check email, calendar, weather. Summarize priorities."}
  }]
}
```

### Email Triage (via Maton)
```bash
# Install Maton skill for Gmail/Outlook access
openclaw skills install maton
```

### Heartbeat (periodic self-check)
```json
{
  "cron": [{
    "name": "heartbeat",
    "schedule": {"kind": "every", "everyMs": 1800000},
    "sessionTarget": "main",
    "payload": {"kind": "systemEvent", "text": "HEARTBEAT: Read HEARTBEAT.md. Execute priority tasks."}
  }]
}
```

## Step 6: Memory Setup

### MEMORY.md (long-term memory)
- Keep under 20K chars (silently truncated above that)
- Distilled wisdom, not raw logs

### Daily notes (raw logs)
```
memory/YYYY-MM-DD.md
```

### Compaction warning
Default compaction mode "safeguard" silently fails above 180K tokens. Enable active memory if you want automatic context pulls.

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| SyntaxError on startup | Node.js too old. `nvm install 24` |
| Telegram breaks after update | Pin version: `npm i -g openclaw@4.15` |
| MEMORY.md content disappears | Keep under 20K chars |
| Gateway binds 0.0.0.0 | Change to 127.0.0.1 immediately |
| API costs too high | Route simple tasks to DeepSeek/Kimi |
| Cron jobs 403 errors | Use sessionTarget "main" with systemEvent, not "isolated" |
| Dreams cron breaks in 4.12 | Disable dreams, use regular cron |

## ClawHub Safety

> ⚠️ 20%+ of ClawHub skills are malicious (per the founder). 1,184+ confirmed malicious skills since January 2026. Snyk found 36% have prompt injection patterns.

**Protection:**
```json
{
  "skills": {
    "allowListOnly": true
  }
}
```
Only install skills you've verified. Check publisher GitHub repos. Never paste install commands from SKILL.md without reading them first.

## Verification

After setup, confirm everything works:

```bash
openclaw gateway status    # Should show "running"
openclaw skills list       # Should show installed skills
```

Send a test message through your connected channel. If the agent responds — you're live.
