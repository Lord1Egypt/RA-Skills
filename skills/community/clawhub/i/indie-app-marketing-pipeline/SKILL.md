---
name: indie-app-marketing-pipeline
description: >
  Template-driven multi-platform content pipeline for indie iOS developers. Generates
  and schedules a full week of social posts (TikTok, YouTube Shorts, X/Twitter, Facebook)
  from a content bank with zero LLM calls per day. Use this skill when asked about:
  marketing pipeline, content pipeline, social media automation, indie app marketing,
  automated posting, content scheduling.
license: MIT
metadata:
  openclaw:
    emoji: 📲
    requires:
      bins: [node]
      env: [POSTIZ_API_KEY]
---

# Indie App Marketing Pipeline

A zero-LLM daily marketing system for indie iOS developers. Write your angles once, then
a weekly planner + daily publisher handle the rest — generating platform-native copy and
scheduling posts to [Postiz](https://postiz.com) automatically.

## What the Pipeline Does

1. **Weekly Planner** — reads your content bank, picks unused angles, applies
   platform-specific templates, and writes a `weekly-plan-YYYY-MM-DD.json` file.
   No LLM required. Run once per week (or whenever you add new angles).

2. **Daily Publisher** — runs each morning (cron at 7 AM), reads that day's entries
   from the weekly plan, and schedules them to Postiz via its public API.
   - Text posts (X, Facebook) are scheduled directly.
   - TikTok/YouTube Shorts trigger your video-gen script (or skip with `--text-only`).

The only time you need an LLM is to write new content bank angles when the bank runs dry.

## Supported Platforms

| Platform | Post type | Volume |
|---|---|---|
| TikTok | Video (requires separate video-gen script) | 3/day |
| YouTube Shorts | Video (reuses TikTok video) | 3/day |
| X / Twitter | Text tweet, 280-char trimmed | 2/day |
| Facebook | Text brand post | Mon/Wed/Fri |

## Architecture

```
content-bank.json         ← your angles (hook + texts + caption per angle)
       │
       ▼
weekly-planner.js         ← picks angles, renders templates → weekly-plan.json
       │
       ▼
weekly-plan-YYYY-MM-DD.json
       │
       ▼
daily-publisher.js        ← reads today's posts → Postiz API → live schedule
       │
       ▼
Postiz (postiz.com)       ← buffers + publishes to each platform on schedule
```

**Template system** — `content-templates.json` defines patterns per platform (hot-take,
question-hook, relatable-meme, etc.). The planner cycles through patterns to avoid
repetition. Variables: `{hook}`, `{insight}`, `{cta}`, `{appName}`, `{appHandle}`,
`{hashtags}`.

**Posting history** — `posting-history.json` tracks which angles have been posted so
the planner never repeats content until the bank is exhausted.

## Setup

### 1. Accounts Needed

- **Postiz** — self-hosted or cloud ([postiz.com](https://postiz.com)). Free tier works.
  Connect your TikTok, YouTube, X, and Facebook accounts in the Postiz UI.
  Note the integration IDs for each platform.

- **Social accounts** — TikTok creator, YouTube channel, X account, Facebook page.

### 2. Run the Setup Script

```bash
cd /path/to/your-app-marketing/
bash skills/indie-app-marketing-pipeline/scripts/setup.sh
```

The script will:
- Create the directory structure (`plans/`, `logs/`, `content-bank.json`, etc.)
- Prompt for your Postiz URL, API key, and platform integration IDs
- Create a sample content bank with 10 starter angles
- Create a `.env` file

### 3. Configure Your App

Edit `config.json` (created by setup.sh):

```json
{
  "app": {
    "name": "YourAppName",
    "handle": "@YourHandle",
    "appStoreUrl": "https://apps.apple.com/app/yourapp",
    "websiteUrl": "https://yourwebsite.com",
    "topicCategory": "productivity"
  },
  "postiz": {
    "apiKey": "$POSTIZ_API_KEY",
    "integrationIds": {
      "tiktok": "your-tiktok-integration-id",
      "youtube": "your-youtube-integration-id",
      "x": "your-x-integration-id",
      "facebook": "your-facebook-integration-id"
    }
  }
}
```

### 4. Edit Your Content Bank

Fill `content-bank.json` with angles for your app. See `assets/sample-content-bank.json`
for the format and `references/content-bank-guide.md` for strategy.

Each angle needs:

```json
{
  "id": "unique-kebab-case-id",
  "hook": "One punchy sentence that is the hook",
  "texts": [
    "Opening line for the video script",
    "Second beat",
    "Third beat / insight",
    "Close"
  ],
  "caption": "TikTok/YouTube caption with hashtags"
}
```

### 5. Run the Weekly Planner

```bash
node scripts/weekly-planner.js --dry-run          # preview
node scripts/weekly-planner.js                    # write plan
node scripts/weekly-planner.js --week 2026-04-07  # specific start date
node scripts/weekly-planner.js --days 3           # plan just 3 days
```

### 6. Run the Daily Publisher

```bash
node scripts/daily-publisher.js --dry-run         # preview today
node scripts/daily-publisher.js                   # go live
node scripts/daily-publisher.js --text-only       # skip video, schedule text only
node scripts/daily-publisher.js --skip-past       # skip posts whose time has passed
```

### 7. Schedule the Daily Publisher (macOS cron)

```bash
# Open crontab
crontab -e

# Add line (runs at 7:00 AM daily):
0 7 * * * cd /path/to/your-app-marketing && node scripts/daily-publisher.js >> logs/cron.log 2>&1
```

Or use a launchd plist for more control.

## Customization

### Posting Schedule

Edit the `VISUAL_SCHEDULE`, `X_SCHEDULE`, and `FB_SCHEDULE` arrays in `weekly-planner.js`.
Times are in EST by default — change `toISOEst()` to use your timezone offset.

Default schedule:

| Slot | Platform | Time (EST) |
|---|---|---|
| tiktok-1 | TikTok | 08:00 |
| youtube-short-1 | YouTube | 08:15 |
| tiktok-2 | TikTok | 13:00 |
| youtube-short-2 | YouTube | 13:15 |
| tiktok-3 | TikTok | 18:00 |
| youtube-short-3 | YouTube | 18:15 |
| x-1 | X | 10:30 |
| x-2 | X | 16:00 |
| fb-text-1 | Facebook | 12:00 (Mon/Wed/Fri) |

### Content Templates

Edit `assets/content-templates.json` to customize the copy patterns. The planner
rotates through all patterns for each platform. See the template variable reference
in `references/platform-strategy.md`.

### Facebook Posts

Facebook posts come from a separate `fb-brand-content-bank.json` (richer, longer-form
content). The weekly planner picks from this bank for Mon/Wed/Fri slots.
See `references/content-bank-guide.md` for how to structure these.

### Angles Per Day

Change `ANGLES_PER_DAY` (default: 3) in `weekly-planner.js` to post more or fewer
video angles per day.

## Files Reference

```
scripts/
  weekly-planner.js        ← generate weekly plan
  daily-publisher.js       ← schedule today's posts to Postiz
  setup.sh                 ← first-time setup

assets/
  content-templates.json   ← platform copy patterns
  sample-content-bank.json ← 10 starter angles

references/
  content-bank-guide.md    ← how to write & maintain your angle bank
  platform-strategy.md     ← platform-specific best practices
```

## References

- [content-bank-guide.md](references/content-bank-guide.md) — writing angles that work
- [platform-strategy.md](references/platform-strategy.md) — platform-specific tactics
- [Postiz docs](https://docs.postiz.com) — API reference
