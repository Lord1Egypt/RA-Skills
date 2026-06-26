# Oto Sessions Skill for OpenClaw

**Platform-agnostic browser session management for AI automation agents.**

Oto solves the hardest part of browser-based automation: staying logged in. It manages authenticated sessions for any website, with full multi-user and multi-account support.

## Quick Install

```bash
# 1. Install Oto framework
git clone https://github.com/mbahar/oto.git ~/oto
cd ~/oto && npm install

# 2. Install this skill
cp -r oto-sessions ~/.openclaw/skills/
```

## Quick Start

```bash
# Save a session (opens browser for manual login)
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work

# List saved sessions
node ~/oto/scripts/list-sessions.js

# Use in automation code
const { launchSession } = require('~/oto/lib/session-manager');
const { page, save } = await launchSession('amazon', 'work');
// Already authenticated — no login wall!
```

## What's Included

- **SKILL.md** — Complete documentation and API reference
- **scripts/** — CLI wrappers and utilities
  - `list-sessions.sh` — Show all saved sessions
  - `save-session.sh` — Create a new session
  - `delete-session.sh` — Remove a session
  - `launch-session.js` — Start automation with a session
  - `check-session.js` — Verify session exists
- **references/** — Detailed guides
  - `SETUP.md` — Installation and configuration
  - `INTEGRATION.md` — Using Oto in agents and scripts

## Common Use Cases

### Save a Session

```bash
node ~/oto/scripts/save-session.js amazon https://www.amazon.com work
```

### Use in Automation

```js
const { launchSession } = require('~/oto/lib/session-manager');

const { page, save, browser } = await launchSession('amazon', 'work');
await page.goto('https://www.amazon.com/orders');
// Fully authenticated — no login required

await save();
await browser.close();
```

### Multiple Accounts

```js
const personal = await launchSession('amazon', 'personal');
const business = await launchSession('amazon', 'work');

// Each runs independently
await personal.page.goto('https://www.amazon.com');
await business.page.goto('https://sellercentral.amazon.com');
```

## Documentation

- [SKILL.md](./SKILL.md) — Full skill documentation
- [references/SETUP.md](./references/SETUP.md) — Installation guide
- [references/INTEGRATION.md](./references/INTEGRATION.md) — Integration patterns
- [Oto GitHub](https://github.com/mbahar/oto) — Main repository

## Features

- ✅ **Any Website** — Platform-agnostic session management
- ✅ **Multiple Accounts** — Personal, business, work accounts on same site
- ✅ **Persistent Login** — Save once, reuse forever
- ✅ **Secure** — Local storage, never committed to git, chmod 600
- ✅ **Multi-Agent** — Share sessions across agents and scripts

## Requirements

- Node.js 18+
- npm
- A machine with a display (for login automation)

## License

MIT — Built by Personal Bahar

---

**Next:** Read [references/SETUP.md](./references/SETUP.md) for detailed installation instructions.
