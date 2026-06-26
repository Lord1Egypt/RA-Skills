---
name: lock-me-in
description: "Remote browser login and session persistence for headless servers. Start an interactive browser session via a temporary public URL (cloudflared tunnel), let the user log in visually, then persist cookies/localStorage for future automated use. Use when: (1) a website requires login before the agent can interact with it, (2) the user says 'log me in' or 'I need to log in to X', (3) automated browsing needs saved credentials, (4) the agent needs to access authenticated pages (LinkedIn, job boards, dashboards). Requires: Playwright-compatible Chromium, cloudflared."
---

# lock-me-in

Remote browser login via temporary public URL. The user logs in visually; cookies persist for future automation.

## How It Works

1. Agent launches headless Chromium with Playwright
2. A web UI streams live screenshots of the browser
3. Cloudflared creates a temporary public tunnel URL
4. User opens the link, clicks/types to log in
5. Session (cookies + localStorage) saved to disk
6. Future Playwright sessions load the saved state

## Quick Start

```bash
# Start a login session
node <skill-dir>/scripts/browser-login.mjs <url> <session-name>

# Examples
node <skill-dir>/scripts/browser-login.mjs https://linkedin.com/login linkedin
node <skill-dir>/scripts/browser-login.mjs https://github.com/login github
node <skill-dir>/scripts/browser-login.mjs https://mail.google.com gmail
```

Run in background with nohup, capture the tunnel URL from stdout:
```bash
nohup node <skill-dir>/scripts/browser-login.mjs <url> <name> > /tmp/lock-me-in.log 2>&1 &
# Wait for URL:
grep -m1 'LOGIN URL' /tmp/lock-me-in.log
```

Send the tunnel URL to the user via their messaging channel.

## Loading Saved Sessions

To use a saved session in Playwright automation:

```javascript
import { chromium } from 'playwright-core';

const browser = await chromium.launch({ executablePath: CHROME_PATH, headless: true, args: ['--no-sandbox'] });
const context = await browser.newContext({
  storageState: '/data/home/.browser-sessions/<session-name>/storage.json'
});
const page = await context.newPage();
await page.goto('https://linkedin.com/feed'); // Already logged in!
```

## Session Storage

Sessions persist at `/data/home/.browser-sessions/<name>/`:
- `storage.json` — Cookies + localStorage (Playwright format)
- `meta.json` — Session metadata (last URL, timestamp, cookie count)

List saved sessions: `ls /data/home/.browser-sessions/`

## Configuration

Environment variables:
- `LOCK_ME_IN_SESSIONS_DIR` — Override sessions dir (default: `/data/home/.browser-sessions`)
- `LOCK_ME_IN_CHROME_PATH` — Override Chrome path (auto-detected from Playwright)
- `LOCK_ME_IN_PORT` — Override local proxy port (default: 18850)
- `OPENCLAW_PROXY_URL` — HTTP proxy for browser traffic (auto-parsed for auth)

Script flags:
- `--port=N` — Local proxy port
- `--timeout=N` — Auto-close after N seconds (default: 900 = 15 min)

## Requirements

- Playwright-compatible Chromium (installed via `npx playwright install chromium`)
- `cloudflared` binary for tunneling (install: `curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared`)
- Node.js 18+

## Web UI Controls

- **Click** on screenshot to click that position
- **Send** types text into the focused element
- **Tab / Enter** for keyboard navigation
- **← Back** browser back button
- **↓ Scroll** scroll down
- **Navigate** go to a specific URL
- **💾 Save** persist session without closing
- **✅ Done** save and close everything

## Security Notes

- Tunnel URLs are random and short-lived (valid only while the process runs)
- No authentication on the tunnel by default — share the URL only with the intended user
- Sessions contain auth cookies — treat `storage.json` as sensitive
- Auto-closes after 15 minutes by default to limit exposure
