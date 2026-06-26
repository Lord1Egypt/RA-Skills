# Oto Skill Setup Guide

## Prerequisites

- Node.js 18 or higher
- npm
- A machine with a display (for manual login flows)
- Playwright (automatically installed)

## Installation Steps

### 1. Install Oto Framework

```bash
# Clone Oto repository
git clone https://github.com/mbahar/oto.git ~/oto

# Install dependencies
cd ~/oto
npm install
```

This creates:
- `~/oto/lib/` — Core session manager
- `~/oto/scripts/` — CLI tools
- `~/oto/sessions/` — Local session storage (git-ignored)

### 2. Install OpenClaw Skill

```bash
# Copy the skill to OpenClaw skills directory
cp -r oto-sessions ~/.openclaw/skills/
```

Or if you have a `.skill` package:

```bash
openclaw skill install oto-sessions.skill
```

### 3. Verify Installation

```bash
# List installed skills
openclaw skills list | grep oto

# Test the Oto installation
node ~/oto/scripts/list-sessions.js
```

## Directory Structure

After setup, you'll have:

```
~/oto/
├── lib/
│   ├── session-manager.js   # Core APIs (launchSession, hasSession, etc.)
│   ├── browser.js           # Low-level browser utilities
│   └── secrets.js           # API key management
├── scripts/
│   ├── save-session.js      # Interactive login + capture
│   ├── list-sessions.js     # Show all saved sessions
│   └── delete-session.js    # Remove a session
├── sessions/                # Local storage (NEVER committed)
│   ├── registry.json        # Metadata index
│   └── amazon--work.json   # Example session
└── node_modules/            # Playwright, etc.

~/.openclaw/skills/
└── oto-sessions/            # This skill
    ├── SKILL.md
    ├── scripts/
    │   ├── list-sessions.sh
    │   ├── save-session.sh
    │   ├── delete-session.sh
    │   ├── launch-session.js
    │   └── check-session.js
    └── references/
        └── SETUP.md (you are here)
```

## Quick Start

### Save Your First Session

```bash
# Save an Amazon session
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work

# Browser opens → you log in → press ENTER when done
# Session saved as amazon:work
```

### List Sessions

```bash
node ~/oto/scripts/list-sessions.js

# Output:
# 📦 Saved Sessions
# 
#   Platform         Account          Saved
#   ───────────────────────────────────────────
#   amazon           work            Apr 3, 9:00 AM
```

### Use in Automation

```js
const { launchSession } = require('~/oto/lib/session-manager');

// Launch with saved session
const { page, save, browser } = await launchSession('amazon', 'work');

// Fully authenticated — no login wall
await page.goto('https://www.amazon.com/orders');

// Do your automation...

// Save updated session
await save();
await browser.close();
```

## Common Platforms

### E-Commerce

```bash
# Amazon
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work
node ~/oto/scripts/save-session.js amazon https://www.amazon.com personal

# eBay
node ~/oto/scripts/save-session.js ebay https://signin.ebay.com work

# Poshmark (Resale)
node ~/oto/scripts/save-session.js poshmark https://poshmark.com/login personal

# Shopify (Admin)
node ~/oto/scripts/save-session.js shopify https://accounts.shopify.com work
```

### Social & Creator Platforms

```bash
# TikTok Shop
node ~/oto/scripts/save-session.js tiktok https://www.tiktok.com/login work

# Instagram (Creator/Business)
node ~/oto/scripts/save-session.js instagram https://instagram.com/accounts/login/ work
```

### Services & Tools

```bash
# PayPal
node ~/oto/scripts/save-session.js paypal https://www.paypal.com/signin work

# Twilio Console
node ~/oto/scripts/save-session.js twilio https://console.twilio.com work

# Indeed (Employer)
node ~/oto/scripts/save-session.js indeed https://employers.indeed.com personal
```

## Session File Format

Sessions are stored as JSON with encrypted credentials:

```json
{
  "platform": "amazon",
  "account": "work",
  "url": "https://www.amazon.com",
  "savedAt": "2025-04-03T12:00:00Z",
  "cookies": [ /* encrypted */ ],
  "localStorage": { /* encrypted */ },
  "sessionStorage": { /* encrypted */ }
}
```

**Files are chmod 600** — only owner can read.

## Troubleshooting

### "Oto not found"

```bash
# Install Oto if missing
git clone https://github.com/mbahar/oto.git ~/oto
cd ~/oto && npm install
```

### "Session not found: amazon:work"

```bash
# Create the session
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work

# Or list what you have
node ~/oto/scripts/list-sessions.js
```

### Browser hangs during login

Some sites block headless browsers. Try:

```js
// In your automation code, use headless=false
const { page } = await launchSession('amazon', 'work', false);
// Browser now shows in a window
```

### Session expires

Many sites invalidate cookies after inactivity. Save a fresh session:

```bash
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work
```

### Playwright not installed

```bash
cd ~/oto && npm install
```

## Environment Variables

You can override paths with environment variables:

```bash
# Custom Oto location
export OTO_PATH=/custom/path/to/oto
node ~/oto/scripts/list-sessions.js

# In your code:
process.env.OTO_PATH = '/custom/path/to/oto';
const { launchSession } = require(`${process.env.OTO_PATH}/lib/session-manager`);
```

## Security Notes

- Sessions are stored **locally only** — never synced to cloud
- Files are **chmod 600** — only readable by owner
- `.gitignore` blocks all `sessions/` and `secrets/` directories
- **Safe to fork** — clone Oto, bring your own sessions
- No API keys embedded — you control all credentials

## Next Steps

- [Integration Guide](./INTEGRATION.md) — Use Oto in agents
- [Oto GitHub](https://github.com/mbahar/oto) — Main repository
- [Playwright Docs](https://playwright.dev) — Browser automation details
