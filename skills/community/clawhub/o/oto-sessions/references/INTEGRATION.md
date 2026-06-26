# Oto Skill Integration Guide

How to use Oto sessions in your OpenClaw agents and automation scripts.

## For Agent Developers

### Pattern 1: Check → Prompt → Launch

When your agent needs a session, always check first:

```js
const { execSync } = require('child_process');
const { hasSession } = require('~/oto/lib/session-manager');

// In your agent task:
if (!hasSession('amazon', 'work')) {
  console.log('Creating Amazon session...');
  
  // Prompt user to save a session
  return {
    type: 'user-action',
    message: 'Need to create a session first. Run:',
    command: 'node ~/oto/scripts/save-session.js amazon https://www.amazon.com work'
  };
}

// Safe to use now
const { launchSession } = require('~/oto/lib/session-manager');
const { page, save, browser } = await launchSession('amazon', 'work');

// Automate...
await page.goto('https://www.amazon.com/orders');

// Save updated session when done
await save();
await browser.close();
```

### Pattern 2: Multi-Account Automation

Run the same task across multiple accounts:

```js
const { launchSession, listSessions } = require('~/oto/lib/session-manager');

// Find all Amazon accounts
const sessions = listSessions().filter(s => s.platform === 'amazon');

for (const session of sessions) {
  const { page, save, browser } = await launchSession(
    session.platform, 
    session.account
  );

  console.log(`Processing ${session.account}...`);
  await page.goto('https://www.amazon.com/orders');
  // Do work...

  await save();
  await browser.close();
}
```

### Pattern 3: Parallel Sessions

Handle multiple accounts simultaneously:

```js
const { launchSession } = require('~/oto/lib/session-manager');

// Load both accounts
const [personal, business] = await Promise.all([
  launchSession('amazon', 'personal'),
  launchSession('amazon', 'work')
]);

// Work in parallel
const [personalOrders, businessOrders] = await Promise.all([
  personal.page.goto('https://www.amazon.com/orders'),
  business.page.goto('https://sellercentral.amazon.com')
]);

// Save both
await Promise.all([
  personal.save(),
  business.save()
]);

await Promise.all([
  personal.browser.close(),
  business.browser.close()
]);
```

### Pattern 4: Session Health Check

Verify a session is still valid:

```js
const { launchSession } = require('~/oto/lib/session-manager');

async function isSessionValid(platform, account) {
  try {
    const { page, browser } = await launchSession(platform, account);
    const title = await page.title();
    await browser.close();
    
    // If we got here, session works
    return true;
  } catch (err) {
    // Session expired or browser error
    return false;
  }
}

// Use it
if (!await isSessionValid('amazon', 'work')) {
  console.log('Session expired — recreate with:');
  console.log('  node ~/oto/scripts/save-session.js amazon https://www.amazon.com work');
}
```

### Pattern 5: Error Handling with Fallback

Gracefully handle missing sessions:

```js
const { launchSession, hasSession } = require('~/oto/lib/session-manager');

async function automateAmazon(accountName) {
  if (!hasSession('amazon', accountName)) {
    return {
      success: false,
      error: 'Session missing',
      action: `node ~/oto/scripts/save-session.js amazon https://www.amazon.com ${accountName}`
    };
  }

  try {
    const { page, save, browser } = await launchSession('amazon', accountName);
    
    // Automate
    await page.goto('https://www.amazon.com/orders');
    const count = await page.locator('[data-test="OrderCard"]').count();
    
    await save();
    await browser.close();
    
    return { success: true, ordersFound: count };
  } catch (err) {
    return {
      success: false,
      error: err.message
    };
  }
}
```

## For OpenClaw Skills

If you're building a skill that needs sessions, import this skill as a dependency:

```yaml
# In your skill manifest
name: my-amazon-skill
description: Manage Amazon orders
dependencies:
  - oto-sessions
```

Then in your code:

```js
const skill = require('~/.openclaw/skills/oto-sessions');
const { launchSession } = require('~/oto/lib/session-manager');

// Use it
const { page, save } = await launchSession('amazon', 'work');
```

## For Standalone Scripts

Use Oto directly without agents:

```js
// standalone-script.js
const { launchSession } = require('~/oto/lib/session-manager');

(async () => {
  const { page, save, browser } = await launchSession('amazon', 'work');
  
  await page.goto('https://www.amazon.com/orders');
  await page.screenshot({ path: 'orders.png' });
  
  await save();
  await browser.close();
})();
```

Run it:

```bash
node standalone-script.js
```

## Session Lifecycle

### 1. Create (Interactive)

```bash
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work
# User logs in manually
# Session saved to ~/oto/sessions/amazon--work.json
```

### 2. Use (Automation)

```js
const { launchSession } = require('~/oto/lib/session-manager');
const { page, browser, save } = await launchSession('amazon', 'work');
// page is fully authenticated
```

### 3. Update (After changes)

```js
await save();  // Persist new cookies/storage
```

### 4. Delete (Cleanup)

```bash
node ~/oto/scripts/delete-session.js amazon work
# Session removed from disk
```

## API Reference

### `launchSession(platform, account = 'default', headless = true)`

Launch a browser context with saved session.

**Returns:**
```js
{
  browser,        // Playwright Browser instance
  context,        // BrowserContext
  page,           // Page (initial blank page)
  platform,       // String: platform name
  account,        // String: account name
  isAuthenticated, // Boolean: was session found?
  save()          // Async: save updated session
}
```

**Example:**
```js
const { page, save, browser } = await launchSession('amazon', 'work');
await page.goto('https://www.amazon.com');
// ... automation ...
await save();
await browser.close();
```

### `hasSession(platform, account = 'default')`

Check if a session exists without launching.

**Returns:** Boolean

**Example:**
```js
if (!hasSession('tiktok', 'work')) {
  console.log('Session missing!');
}
```

### `listSessions()`

Get all saved sessions with metadata.

**Returns:**
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
  // ... more sessions
]
```

**Example:**
```js
const sessions = listSessions();
console.log(`You have ${sessions.length} saved sessions`);

// Filter by platform
const amazonSessions = sessions.filter(s => s.platform === 'amazon');
```

### `deleteSession(platform, account = 'default')`

Permanently remove a session (requires confirmation).

**Returns:** Promise

**Example:**
```js
await deleteSession('amazon', 'old-account');
```

### `connectDebugBrowser(wsEndpoint = 'ws://localhost:3000')`

Connect to a running Chromium instance for debugging.

**Use when:** You want to manually control a browser in Chrome DevTools while your script runs.

**Example:**
```js
// In a separate terminal, start Chrome:
// google-chrome --remote-debugging-port=9222

const { browser, page } = await connectDebugBrowser('ws://localhost:9222');
// Now you can control it manually while script runs
```

## Debugging

### Enable Oto debug logs

```bash
DEBUG=oto node your-script.js
```

### Run browser in visible window

```js
// headless: false shows the browser
const { page } = await launchSession('amazon', 'work', false);
```

### Inspect saved session file

```bash
# See session metadata
cat ~/oto/sessions/amazon--work.json | jq . | head -20
```

### Record video during automation

```js
const { launchSession } = require('~/oto/lib/session-manager');

const { page, save, browser, context } = await launchSession(
  'amazon', 
  'work',
  false // visible
);

// If recording was enabled, check context._connection
// Or use headless recording in Playwright
```

## Best Practices

1. **Always check before using:**
   ```js
   if (!hasSession(platform, account)) { /* handle */ }
   ```

2. **Save after changes:**
   ```js
   await save();  // Don't forget this!
   ```

3. **Close browser cleanly:**
   ```js
   await browser.close();
   ```

4. **Use try/catch:**
   ```js
   try {
     const { page, save, browser } = await launchSession(...);
     // work...
   } finally {
     await browser.close();
   }
   ```

5. **Handle multiple accounts safely:**
   ```js
   // Use Promise.all for parallel work
   const results = await Promise.all([
     launchSession('amazon', 'personal'),
     launchSession('amazon', 'work')
   ]);
   ```

6. **Respect rate limits:**
   - Add delays between requests
   - Don't hammer sites
   - Use headless automation responsibly

## Troubleshooting

**Q: "Session not found"**

A: Create it first:
```bash
node ~/oto/scripts/save-session.js <platform> <url> <account>
```

**Q: Browser hangs/times out**

A: Try with visible window:
```js
const { page } = await launchSession('amazon', 'work', false);
```

**Q: Session expires after a few days**

A: Save a fresh one:
```bash
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work
```

**Q: Cookie rejected / "Not authenticated"**

A: The site might have updated auth. Try:
```bash
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work
```

## Related

- [Setup Guide](./SETUP.md) — Installation & first steps
- [Oto GitHub](https://github.com/mbahar/oto) — Main repo
- [Playwright API](https://playwright.dev/docs/api/class-browser) — Browser control details
