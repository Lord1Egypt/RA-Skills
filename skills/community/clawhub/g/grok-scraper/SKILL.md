---
name: grok-scraper
description: Execute queries to Grok AI via Playwright browser automation without requiring an X API KEY. Use when the user wants to "ask Grok", search X for real-time info, or specifically requests to use Grok for free without API billing.
---

# Grok Scraper

## Preview

[<video src="./assets/grok-2026-03-15T10-01-45.webm" controls width="100%"></video>](https://github.com/user-attachments/assets/d48c7948-11d5-4606-baf8-db0a0b0a095f)

**Agent Context**: This is a zero-cost alternative to official X APIs. It uses a real browser session (Playwright) via an X Premium account. ALWAYS use this skill when the user wants to query Grok but does not have or want to use an X API KEY.

## Prerequisites

- **OpenClaw** must be installed on the host machine.
- **A display/GUI environment is required.** This skill launches a real browser window for login. It **cannot run on headless cloud servers** (no screen). It must be used on a local machine or a remote desktop with a display.
- The user must be logged in to **x.com** via the browser session saved by `npm run login`. Without a valid session, all queries will fail.

## First-Time Setup

Run these commands once after cloning the repo, before doing anything else:

```bash
cd scripts
npm install
npx playwright install chromium
```

Then log in to x.com to create a session:

```bash
npm run login
# A browser window will open — log in to x.com manually, then return to the terminal and press Enter
```

The `session/` directory will be created automatically after a successful login.

## Workflow

**Step 1: Check Login State**
- If `session/` directory does not exist: stop and ask the user to run `cd scripts && npm run login`.
- If it exists: proceed.

**Step 2: Execute Query**
```bash
scripts/run.sh "The user's detailed prompt"
```

`run.sh` handles logging, automatic retry on Grok service errors, and login-expiry detection. It is the canonical entry point for all queries.

**Step 3: Read Output**
- Exit Code 0 → read `output/latest.md` and present the result.
- Other exit codes → see Error Handling below.

## Error Handling

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Read `output/latest.md` |
| 2 | Session expired | Ask user to run `cd scripts && npm run login` |
| 3 | Grok service error | `run.sh` already retried once; report failure to user |
| 1 | Extraction failed | Check if `output/debug-dom.json` was written → if yes, DOM selectors may have broken — see [dom-selector-fix.md](dom-selector-fix.md) |

## DOM Selectors Breaking

Twitter/X redeploys its front-end regularly, which changes the CSS class names this scraper relies on. If extraction fails with `Method: none`, follow the fix guide:

→ **[dom-selector-fix.md](dom-selector-fix.md)**

## Examples

**Standard query**
```bash
scripts/run.sh "Search for the latest AI news and format as markdown"
# → read output/latest.md
```

**Session expired**
1. Run `scripts/run.sh` → Exit Code 2
2. Tell user: "Session expired, please run `cd scripts && npm run login`"

**DOM selectors broken**
1. Run `scripts/run.sh` → Exit Code 1, `output/debug-dom.json` exists
2. Follow [dom-selector-fix.md](dom-selector-fix.md) to identify new classes and update `SELECTORS` in `scripts/scrape.js`

---

## Debugging

When diagnosing scraper issues directly, use the bare command — it skips logging and retry logic, making failures easier to inspect.

| Flag | Example | Description |
|------|---------|-------------|
| _(none)_ | `npm run scrape` | Run with default prompt |
| `"prompt"` | `npm run scrape -- "Your question"` | Custom prompt |
| `--record` | `npm run scrape -- --record` | Record video to `output/grok-<timestamp>.webm` |
| `--record <path>` | `npm run scrape -- --record out.webm` | Record video to custom path (relative → `output/`) |
| `--size WxH` | `npm run scrape -- --record --size 1920x1080` | Set recording resolution (default: `1280x800`) |

All flags can be combined:
```bash
cd scripts
npm run scrape -- "Your prompt" --record --size 1920x1080
```

When `--record` is active, the browser runs in **headed mode** (visible window) with `slowMo: 50ms`; without it, headless mode is used.

