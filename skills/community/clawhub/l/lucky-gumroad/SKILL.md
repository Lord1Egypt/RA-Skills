---
name: gumroad
description: Gumroad store automation — product creation, uploads, profile editing, data pulls. Use when any task involves Gumroad (creating products, managing listings, pulling sales data, updating profile). Requires authenticated Chrome profile at /home/openclaw/gumroad-profile. Never log in manually — session is pre-authenticated.
---

# Gumroad Automation Skill

## Authentication

Session is pre-authenticated. **Never log in manually.** Always reuse the saved Chrome profile.

## Chrome Profile

**Path:** `/home/openclaw/gumroad-profile`

**Rules (non-negotiable):**
- Always use `--user-data-dir=/home/openclaw/gumroad-profile`
- Never clear cookies
- Never use incognito/guest mode
- Never run as root

## Quick Session Test

```bash
timeout 20 google-chrome \
  --user-data-dir=/home/openclaw/gumroad-profile \
  --headless=new --no-sandbox --disable-gpu \
  --disable-dev-shm-usage \
  --dump-dom https://gumroad.com/dashboard \
  > /tmp/gumroad-test.html 2>/dev/null

grep -E "Dashboard/Index|logged_in_user|current_seller" /tmp/gumroad-test.html | head
```

- If grep returns lines → session valid ✅
- If URL is `/login?next=%2Fdashboard` → session expired ❌ (tell Ray)

## Headless Chrome Launch (for automation)

```bash
google-chrome \
  --user-data-dir=/home/openclaw/gumroad-profile \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port=9222 \
  "https://gumroad.com/dashboard" &
```

## Puppeteer / Playwright

```javascript
// Puppeteer
const browser = await puppeteer.launch({
  headless: 'new',
  userDataDir: '/home/openclaw/gumroad-profile',
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
});

// Playwright
const context = await chromium.launchPersistentContext('/home/openclaw/gumroad-profile', {
  headless: true,
  args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
});
```

## Account Info

- Seller: `qcautonomous`
- Display name: `RayChod`
- Subdomain: `qcautonomous.gumroad.com`
- User ID: `3256469230239`

## Important

- If session ever expires, **tell Ray** — don't try to log in
- Kill any leftover Chrome before launching: `pkill -f "chrome.*gumroad-profile" 2>/dev/null`
- Always wait 2 seconds after kill before relaunching
