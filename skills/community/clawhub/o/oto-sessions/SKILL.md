---
name: oto-sessions
description: Manage authenticated browser sessions for any website using the Oto framework. Save, reuse, and switch between multiple accounts across any platform without re-authenticating. Use when: (1) saving a new session after manual login, (2) listing available sessions, (3) deleting a session, (4) launching automation on a saved session, (5) connecting to a debug browser. Triggers on phrases like "save session", "list sessions", "delete session", "launch browser", "automate with [platform]", or any task requiring authenticated browser access.
keywords:
  - session management
  - browser automation
  - authentication
  - multi-account
  - web scraping
  - bot automation
---

# Oto Sessions Skill

**Platform-agnostic browser session management for AI automation agents.**

Oto solves the hardest part of browser-based automation: staying logged in. It manages authenticated sessions for any website, with full multi-user and multi-account support — so AI agents and scripts can access any platform without re-authenticating.

## What This Skill Does

This skill wraps the Oto CLI tools to provide a seamless workflow for:

- **Saving sessions** — Log in once manually, then reuse forever
- **Listing sessions** — See all your saved platform:account pairs
- **Deleting sessions** — Remove sessions you no longer need
- **Launching automation** — Start fully authenticated browser sessions
- **Multi-account support** — Switch between personal, business, or multiple accounts on the same platform

## Installation

### 1. Clone and install Oto

```bash
git clone https://github.com/mbahar/oto.git ~/oto
cd ~/oto && npm install
```

Oto will create `~/oto/sessions/` (local, git-ignored) to store encrypted sessions.

### 2. Install this skill

```bash
cp -r oto-sessions ~/.openclaw/skills/
```

Once installed, your agent will automatically:
- Prompt you to save sessions when needed
- Reuse saved sessions for all automation tasks
- Switch between accounts seamlessly

### Requirements

- Node.js 18+
- Playwright (installed by `npm install`)
- A machine with a display (browser automation needs a screen for login flows)

## Usage Patterns

### Pattern 1: Save a New Session

When you need to authenticate on a website:

```bash
# Opens browser for manual login, saves session when you press Enter
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work

# Session saved as amazon:work — ready to reuse
```

**In automation code:**

```js
const { launchSession } = require('~/oto/lib/session-manager');

// Launch with saved session — already authenticated, no login wall
const { page, save } = await launchSession('amazon', 'work');

// Go straight to authenticated pages
await page.goto('https://www.amazon.com/orders');

// Do stuff...

// Save updated session back
await save();
```

### Pattern 2: List All Sessions

```bash
node ~/oto/scripts/list-sessions.js

# Output:
# 📦 Saved Sessions
# 
#   Platform         Account          Saved
#   ─────────────────────────────────────────
#   amazon           work            Apr 3, 9:00 AM
#   amazon           personal         Apr 3, 9:05 AM
#   tiktok           work            Apr 3, 9:10 AM
```

### Pattern 3: Delete a Session

```bash
# Delete specific account on a platform
node ~/oto/scripts/delete-session.js amazon work

# Delete default account
node ~/oto/scripts/delete-session.js tiktok
```

### Pattern 4: Multi-Account Automation

Run against multiple accounts simultaneously:

```js
const { launchSession } = require('~/oto/lib/session-manager');

// Load both accounts
const personal  = await launchSession('amazon', 'personal');
const business  = await launchSession('amazon', 'work');

// Each runs independently
await personal.page.goto('https://www.amazon.com/orders');
await business.page.goto('https://sellercentral.amazon.com');

// Work with both...

await personal.save();
await business.save();
```

### Pattern 5: Check Before Using

```js
const { launchSession, hasSession } = require('~/oto/lib/session-manager');

if (!hasSession('tiktok', 'work')) {
  console.log('Session missing. Run:');
  console.log('  node ~/oto/scripts/save-session.js tiktok https://tiktok.com/login work');
  process.exit(1);
}

// Safe to use
const { page } = await launchSession('tiktok', 'work');
```

### Pattern 6: Debug Mode (Connect to Running Browser)

```js
const { connectDebugBrowser } = require('~/oto/lib/session-manager');

// Connect to Chrome running with --remote-debugging-port=9222
const { browser, page } = await connectDebugBrowser();

// Control it — already logged into whatever you have open
await page.goto('https://some-authenticated-page.com');
```

## Session ID Format

Sessions are stored as `platform:account`:

| ID | Meaning |
|----|---------|
| `amazon:work` | Amazon, work account |
| `amazon:personal` | Amazon, personal account |
| `tiktok:work` | TikTok, work account |
| `indeed:personal` | Indeed, Personal's employer account |
| `poshmark:personal` | Poshmark, personal account |
| `shopify:work` | Shopify, business account |
| `myapp:alice` | Any app, Alice's account |

**You define the names.** Oto doesn't know or care what the platform actually is — it's purely for your organization.

## Common Examples

### Amazon (Personal & Business)

```bash
# Save personal account
node ~/oto/scripts/save-session.js amazon https://www.amazon.com personal

# Save business account (Work)
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work

# Use in code
const personal = await launchSession('amazon', 'personal');
const business = await launchSession('amazon', 'work');
```

### TikTok Shop

```bash
node ~/oto/scripts/save-session.js tiktok https://www.tiktok.com/login work
node ~/oto/scripts/save-session.js tiktok https://www.tiktok.com/login personal

# List what we have
node ~/oto/scripts/list-sessions.js
```

### eBay (Multi-Seller)

```bash
node ~/oto/scripts/save-session.js ebay https://signin.ebay.com work
node ~/oto/scripts/save-session.js ebay https://signin.ebay.com personal

# Automate on both
const workSession = await launchSession('ebay', 'work');
const personalSession = await launchSession('ebay', 'personal');
```

### Shopify Admin

```bash
node ~/oto/scripts/save-session.js shopify https://accounts.shopify.com work

# Use
const { page } = await launchSession('shopify', 'work');
await page.goto('https://admin.shopify.com/');
```

## APIs

### Session Manager Exports

**`launchSession(platform, account = 'default', headless = true)`**

Launches a browser context with saved session cookies/storage. Returns:

```js
{
  browser,        // Playwright browser instance
  context,        // Browser context
  page,           // Current page
  platform,       // Platform name
  account,        // Account name
  isAuthenticated, // Boolean: was session found?
  save()          // Async function to save updated session
}
```

**`hasSession(platform, account = 'default')`**

Boolean check if session exists.

**`listSessions()`**

Returns array of all saved sessions with metadata:

```js
[
  {
    key: 'amazon:work',
    platform: 'amazon',
    account: 'work',
    url: 'https://www.amazon.com',
    savedAt: '2025-04-03T12:00:00Z',
    label: 'amazon:work'
  },
  // ...
]
```

**`deleteSession(platform, account = 'default')`**

Permanently delete a session (requires confirmation).

**`connectDebugBrowser()`**

Connect to a running Chrome instance for manual debugging/testing.

## Security

- **Sessions are local-only** — stored in `~/oto/sessions/`
- **Never committed to git** — `.gitignore` blocks all session files
- **File permissions** — each session is `chmod 600` (owner only)
- **Safe to fork** — clone the code, bring your own sessions
- **No API keys embedded** — you control all credentials

## Architecture

```
Oto Framework
├── lib/session-manager.js    # Core session APIs
├── scripts/
│   ├── save-session.js       # Interactive login + capture
│   ├── list-sessions.js      # Show all sessions
│   └── delete-session.js     # Remove a session
└── sessions/                 # Local storage (git-ignored)
    ├── amazon--work.json
    ├── amazon--personal.json
    └── registry.json
```

## Workflow for Agents

1. **Check if session exists:**
   ```js
   const { hasSession } = require('~/oto/lib/session-manager');
   if (!hasSession('amazon', 'work')) { /* prompt */ }
   ```

2. **If missing, prompt user:**
   ```
   You'll need to create a session first:
   node ~/oto/scripts/save-session.js amazon https://www.amazon.com work
   ```

3. **If exists, launch and automate:**
   ```js
   const { launchSession } = require('~/oto/lib/session-manager');
   const { page, save } = await launchSession('amazon', 'work');
   // Automate...
   await save();
   ```

4. **After task, save updated session:**
   ```js
   await save();  // Persist any new cookies/storage
   await browser.close();
   ```

## Troubleshooting

**Q: Browser launches but login doesn't work**

A: Some sites block headless browsers. Try:
```js
const { page } = await launchSession('amazon', 'work', headless=false);
```

**Q: Session expires after a few days**

A: Many sites invalidate cookies after inactivity. Save a fresh session when needed:
```bash
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work
```

**Q: Can't find my sessions**

A: List them:
```bash
node ~/oto/scripts/list-sessions.js
```

Sessions are in `~/oto/sessions/` with filenames like `platform--account.json`.

**Q: How do I use multiple accounts simultaneously?**

A: Load them both:
```js
const a = await launchSession('amazon', 'work');
const b = await launchSession('amazon', 'personal');
// Both run independently
```

## Related

- [Oto GitHub](https://github.com/mbahar/oto) — Main repository
- [Playwright Docs](https://playwright.dev) — Browser automation
- [OpenClaw Skills](https://docs.openclaw.ai/skills) — Skill framework

---

Built and maintained by the Oto community (@mbahar).
