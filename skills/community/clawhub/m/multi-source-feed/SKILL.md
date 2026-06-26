---
name: multi-source-feed
description: Set up and manage an AI-curated daily tech brief from customizable sources. Use when user says "set up multi-source-feed", "configure my daily brief", or "msf setup".
version: 1.0.0
metadata: {"openclaw":{"emoji":"📡","requires":{"bins":["python3"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY","homepage":"https://github.com/zidooong/multi-source-feed"}}
---

# Multi-Source Feed

AI-curated daily tech brief aggregated from customizable sources (X, HN, GitHub Trending, RSS blogs, Reddit, Product Hunt, Tavily, and more). Deduplicates, filters by your interests, and delivers a structured memo.

## Setup

When the user asks to set up Multi-Source Feed, follow these steps **in order**. Execute each step automatically. If any step fails, print the manual command and continue.

### Step 1: Clone & Install

```bash
cd ~ && git clone https://github.com/zidooong/multi-source-feed.git
cd ~/multi-source-feed
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

If clone already exists, skip to `pip install`.

### Step 2: API Keys

Some sources require API keys that the user must register themselves. Ask the user for:

1. **Tavily** (free): powers web search to catch trending topics not covered by RSS feeds. Sign up at https://tavily.com
2. **Product Hunt** (free): required for the Product Hunt GraphQL API. Get a token at https://api.producthunt.com/v2/docs

Once the user provides both keys, write them to `~/multi-source-feed/.env`:

```
TAVILY_API_KEY=<user's key>
PRODUCTHUNT_API_TOKEN=<user's key>
```

### Step 3: X/Twitter Login

Tell the user:
> "To save your X/Twitter session, you need to:
> 1. Open Chrome with remote debugging enabled by running:
>    `open -a 'Google Chrome' --args --remote-debugging-port=9222`
> 2. Log in to X/Twitter in that Chrome window
> 3. Once logged in, I'll run a script that connects to that browser and saves your session cookies."

After the user confirms they are logged in to X in Chrome, run:

```bash
cd ~/multi-source-feed && source .venv/bin/activate && python login_save_session.py
```

This script connects to the already-open Chrome instance via CDP (Chrome DevTools Protocol) on port 9222, extracts the session/cookies, and saves them to `x_session.json` in the project root. It does **not** open a new browser window — it requires Chrome to already be running with `--remote-debugging-port=9222`.

### Step 4: Customize

**This step directly affects the quality of the daily brief.** Strongly encourage the user to customize before proceeding.

Ask the user:
> "The default profile is a generic template. I strongly recommend customizing these files to match your interests — this directly determines the quality of your daily brief. What topics do you care about? What should be filtered out?"

Based on their response:
- Edit `config/user_profile.md` — set their interests, non-interests, and Key Players to track
- Adjust `config/sources.yaml` if needed (enable/disable sources, add their own RSS feeds)
- Adjust `config/preferences.md` if they want different memo sections or format

If they insist on skipping, move on — but remind them they can customize later.

### Step 5: Test Run

```bash
cd ~/multi-source-feed && source .venv/bin/activate && python -m src.pipeline
```

Show the user the output summary (number of sources, items fetched, any errors). If successful, show 5-10 sample titles from `feed_slim.json`.

### Step 6: Schedule

The system runs in two phases. Phase 1 (scraping) must complete before Phase 2 (memo generation) starts.

**Phase 1: Scrape (crontab)** — Pure Python job that fetches all sources, deduplicates, and writes `feed_slim.json`. Set up a daily cron job:
```bash
(crontab -l 2>/dev/null; echo "0 9 * * * cd ~/multi-source-feed && .venv/bin/python3 -m src.pipeline >> /tmp/msf-scrape.log 2>&1") | crontab -
```

**Phase 2: Memo (OpenClaw cron)** — LLM-powered job that generates the daily brief and sends it to the user. Must run ~20 min after Phase 1 to ensure scraping is complete.

Create an OpenClaw cron job that:
1. Checks if `feed_slim.json` exists and is from today
2. Reads `config/user_profile.md` and `config/preferences.md`
3. Reads `feed_slim.json` (the scrape output)
4. Generates the daily brief following preferences.md format
5. Sends the brief to the user via their configured channel
6. Saves the brief to `memo/YYYY-MM-DD.md` (used for cross-day dedup)

Tell the user:
> "Setup complete! Your daily brief will be generated every morning. You'll receive it through your configured messaging channel."

## Manual Setup Fallback

If automated setup fails, provide the user with these commands to run manually:

```bash
# 1. Clone
git clone https://github.com/zidooong/multi-source-feed.git && cd multi-source-feed

# 2. Install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && playwright install chromium

# 3. Configure
cp .env.example .env
# Edit .env with your API keys

# 4. X Login
python login_save_session.py

# 5. Test
python -m src.pipeline

# 6. Schedule scraping
crontab -e
# Add: 0 9 * * * cd ~/multi-source-feed && .venv/bin/python3 -m src.pipeline >> /tmp/msf-scrape.log 2>&1
```

## Customization

All user-customizable files are in `config/`:

| File | Purpose |
|------|---------|
| `config/user_profile.md` | Your interests, Key Players to track |
| `config/sources.yaml` | Enable/disable sources, add RSS feeds |
| `config/preferences.md` | Memo format, sections, filtering rules |

### Adding a new RSS source

Add 4 lines to `config/sources.yaml`:
```yaml
- name: my-blog
  type: rss
  enabled: true
  url: https://example.com/feed.xml
  tags: [blog]
```

## X-Push (Optional)

If the user wants real-time X/Twitter highlights every 2 hours (in addition to the daily brief):

1. Ask the user if they want to customize `push/preferences.md` (filtering rules and output format)
2. Create an OpenClaw cron job (every 2 hours) with this prompt:

```
Execute these steps in order:

1. Run: bash ~/multi-source-feed/push/run.sh
   (Wait for it to finish, usually 2-3 minutes)

2. If exit code is non-zero, notify the user that X Push scraping failed, then stop.

3. Read push/new_posts.json. If the posts array is empty, stop silently.

4. Read push/preferences.md for filtering rules and output format.

5. Read config/user_profile.md to understand what the reader cares about.

6. Filter and send noteworthy posts following the format in push/preferences.md.

7. End.
```

The push module shares `x_session.json` and `.venv` with the main pipeline — no extra setup needed.
