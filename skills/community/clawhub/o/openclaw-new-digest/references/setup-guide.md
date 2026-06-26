# News Digest Setup Guide

## Prerequisites

- **Node.js** >= 18 (for built-in `fetch` support)
- **OpenClaw** installed and configured

## Installation

### Via ClawdHub (recommended)

```bash
clawdhub install news-digest
```

### Manual

```bash
git clone <repo-url> ~/.openclaw/skills/news-digest
```

Or copy the `news-digest-1.0.0/` directory to `~/.openclaw/skills/news-digest/`.

## Environment Variables

### Create a `.env` File

Create a `.env` file in your OpenClaw workspace (this is the preferred location for cron compatibility):

```bash
# ~/.openclaw/workspace/.env
TAVILY_API_KEY=tvly-xxxxxxxxxxxxx
XPOZ_API_KEY=your-xpoz-key
```

The `cron-trigger.sh` script automatically searches for `.env` in this order:
1. `~/.openclaw/workspace/.env` (recommended)
2. `{skill-root}/.env`
3. `~/.env`

### Required

#### `TAVILY_API_KEY`

Get your API key from [https://tavily.com](https://tavily.com). Required for Tavily Search and Extract.

### Recommended

#### `XPOZ_API_KEY`

Configure the Xpoz MCP service in OpenClaw for Twitter access. If not configured, the skill degrades gracefully — Twitter data is skipped and the agent relies on Tavily + Hacker News.

### Optional

#### `NEWS_DIGEST_DATA_DIR`

Override the default data storage directory. Default: `{skill-root}/data/`.

## Quick Environment Check

Verify everything is configured correctly:

```bash
node scripts/env-check.mjs
```

## First-Time Configuration

After installing, the agent will automatically detect that no `config.json` exists and prompt the user to set up their push schedule and topics.

You can also configure manually:

### Quick Setup (Defaults)

Create the standard 3-slot schedule (08:00 Finance, 12:00 AI, 18:00 General):

```bash
node scripts/manage-config.mjs init
```

### Custom Setup

Add slots one by one:

```bash
node scripts/manage-config.mjs set-slot \
  --name morning \
  --time 08:00 \
  --topic "Finance" \
  --label "金融早报" \
  --keywords "crypto,bitcoin,ethereum,finance,stock" \
  --priority "crypto > financial events > US stocks" \
  --sources "twitter,tavily,hackernews"

node scripts/manage-config.mjs set-slot \
  --name noon \
  --time 12:00 \
  --topic "AI / Agent" \
  --label "AI午报" \
  --keywords "AI,LLM,GPT,agent,machine learning" \
  --sources "twitter,tavily,hackernews"
```

### Verify Config

```bash
node scripts/manage-config.mjs show
```

### Modify Later

```bash
# Change time
node scripts/manage-config.mjs set-slot --name morning --time 07:30

# Change keywords
node scripts/manage-config.mjs set-slot --name morning --keywords "crypto,defi,bitcoin"

# Add a new slot
node scripts/manage-config.mjs set-slot --name afternoon --time 15:00 --topic "Markets" --label "盘后速递" --keywords "stocks,earnings"

# Remove a slot
node scripts/manage-config.mjs remove-slot --name evening

# Reset everything
node scripts/manage-config.mjs reset
```

## Enable the Bootstrap Hook

The hook reads `config.json` to inject a time-aware reminder at session start. If no config exists, it reminds the agent to run first-time setup.

```bash
# Step 1: Copy hook files to OpenClaw hooks directory
cp -r hooks/openclaw ~/.openclaw/hooks/news-digest

# Step 2: Enable the hook
openclaw hooks enable news-digest

# Step 3: Verify it's registered
openclaw hooks list
```

If `news-digest` appears in the list, the hook is active. It will fire on every `agent:bootstrap` event.

## Scheduling (Cron)

This skill is an **AI-assisted workflow** — the agent executes the push when triggered. Use cron to trigger it automatically at scheduled times.

### Important: Configure Before Scheduling

Cron entries should match the slots in your `config.json`. After changing your schedule via `manage-config.mjs`, update your crontab accordingly.

### Setup

The `cron-trigger.sh` script reads `config.json` for slot definitions, loads `.env`, and spawns an OpenClaw session.

**Step 1: Test the script first**

```bash
# Dry run — shows slot info from config without triggering
bash /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot morning --dry-run
```

Expected output:
```
[2026-03-06T10:00:00+08:00] slot=morning env=/home/user/.openclaw/workspace/.env [DRY RUN]
  Config: /path/to/news-digest-1.0.0/data/config.json
  Slot: morning (金融早报)
  Topic: Finance
  Would run: openclaw run --message "Execute news digest push for slot ..."
  TAVILY_API_KEY: set
  XPOZ_API_KEY: set
```

**Step 2: Add cron entries**

```bash
crontab -e
```

Add entries for each slot in your config. The times should match:

```cron
# Example for default 3-slot config — adjust to your config.json!
0 8 * * *  /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot morning >> /tmp/news-digest-cron.log 2>&1
0 12 * * * /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot noon >> /tmp/news-digest-cron.log 2>&1
0 18 * * * /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot evening >> /tmp/news-digest-cron.log 2>&1
```

If you added a custom slot (e.g. `afternoon` at 15:00), add:
```cron
0 15 * * * /path/to/news-digest-1.0.0/scripts/cron-trigger.sh --slot afternoon >> /tmp/news-digest-cron.log 2>&1
```

**Step 3: Verify cron is running**

```bash
crontab -l
```

### Auto-Detection

If you omit `--slot`, the script reads `config.json` and auto-detects the active slot based on the current hour and each slot's `window` field:

```bash
# Will auto-detect based on config.json
bash /path/to/news-digest-1.0.0/scripts/cron-trigger.sh
```

### Why cron-trigger.sh?

Cron runs in a minimal shell environment — it does **not** load `.bashrc`, `.zshrc`, or `.env` files. The `cron-trigger.sh` script solves this by:
1. Sourcing the `.env` file before doing anything
2. Reading slot definitions from `config.json`
3. Logging every trigger to `data/logs/cron.log` for traceability
4. Providing `--dry-run` for safe testing

### Logs

Cron execution logs are written to:
- `{dataDir}/logs/cron.log` — internal trigger log (written by the script)
- `/tmp/news-digest-cron.log` — stdout/stderr capture (from the crontab redirect)

## Verify Installation

Test each script individually:

```bash
# Check environment
node scripts/env-check.mjs

# View config
node scripts/manage-config.mjs show

# Test Hacker News fetch
node scripts/fetch-hackernews.mjs "AI" --min-score 30 --hours 48 -n 5

# Test Tavily search (requires TAVILY_API_KEY)
node scripts/fetch-tavily.mjs "AI news today" --topic news --days 1 -n 3

# Test storage
echo '{"slot":"morning","topic":"test","items":[{"title":"Test","source":"manual"}],"usage":{"tavily_search":1,"hackernews":1}}' | node scripts/store-push.mjs

# Test query
node scripts/query.mjs pushes --date $(date +%Y-%m-%d)

# Test feedback
node scripts/add-feedback.mjs --slot morning "测试反馈"

# Test usage tracking
node scripts/track-usage.mjs today
node scripts/track-usage.mjs forecast
```

## Data Directory Structure

After running, the data directory will look like:

```
data/
├── config.json          ← User-defined schedule & topics
├── pushes/
│   └── 2026-03-06/
│       ├── morning.json
│       ├── noon.json
│       └── evening.json
├── feedback/
│   └── 2026-03-06/
│       ├── morning.json
│       └── noon.json
├── usage/
│   └── 2026-03.json
└── logs/
    └── cron.log
```

## Troubleshooting

### "Config file not found"

The schedule hasn't been configured yet. Either:
- Tell the agent to help you set up: "Help me configure my news digest schedule"
- Or run: `node scripts/manage-config.mjs init` for defaults

### "Missing TAVILY_API_KEY"

1. Check the variable is set: `echo $TAVILY_API_KEY`
2. Check your `.env` file exists: `cat ~/.openclaw/workspace/.env`
3. If running via cron, verify `cron-trigger.sh --dry-run` shows the key as "set"

### Cron not triggering

1. Verify cron is running: `crontab -l`
2. Check cron daemon: `pgrep cron` (Linux) or `launchctl list | grep cron` (macOS)
3. Check logs: `cat /tmp/news-digest-cron.log`
4. Check internal logs: `cat data/logs/cron.log`
5. Test manually: `bash scripts/cron-trigger.sh --slot morning --dry-run`

### Cron triggers but slot not found

The slot name in your crontab must match a slot name in `config.json`. Run:
```bash
node scripts/manage-config.mjs show
```
to see available slot names, then update your crontab.

### Cron triggers but API keys are missing

The `.env` file must be in one of these locations:
- `~/.openclaw/workspace/.env` (preferred)
- `{skill-root}/.env`
- `~/.env`

Format (no `export`, no quotes around values):
```
TAVILY_API_KEY=tvly-xxxxxxxxxxxxx
XPOZ_API_KEY=your-key-here
```

### No Hacker News results

- Try broader keywords or lower `--min-score`
- HN API is public but rate-limited; if you see errors, wait and retry
- Use `--hours 48` to expand the time window

### Empty push results

- Check that sources are returning data by running fetch scripts individually
- Lower the influence thresholds in your config
- Use a broader topic slot for testing

### Hook not firing

1. Verify hook is enabled: `openclaw hooks list`
2. Check hook file location: `ls ~/.openclaw/hooks/news-digest/`
3. Both `HOOK.md` and `handler.js` must be present
4. The hook only fires on `agent:bootstrap` — it won't fire for subagent sessions
