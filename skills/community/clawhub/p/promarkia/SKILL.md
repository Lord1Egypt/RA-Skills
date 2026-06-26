---
name: promarkia
description: "Run Promarkia AI squads via the Promarkia API — social media posts, copywriting, SEO, ads, lead generation, image/video creation, campaign planning, and more. Use when asked to run a Promarkia task, submit a squad job, or schedule recurring marketing automation via the Promarkia platform."
homepage: https://www.promarkia.com
metadata:
  clawdbot:
    emoji: "🚀"
    requires:
      env: ["PROMARKIA_API_KEY"]
      primaryEnv: "PROMARKIA_API_KEY"
    files: ["scripts/*"]
---

# Promarkia

Thin API client for [Promarkia](https://www.promarkia.com) — run any Promarkia squad from OpenClaw.

## Setup

1. Sign up at [promarkia.com](https://www.promarkia.com) and buy credits or subscribe
2. Connect your accounts (LinkedIn, X, Reddit, etc.) via the **Connect Integrations** panel
3. Generate an API key from **API Keys** in the sidebar
4. Set the environment variable: `PROMARKIA_API_KEY=pmk_your_key_here`

## Available Squads

| Squad ID | Name | What it does |
|----------|------|-------------|
| `1` | Assistant | Email, calendar, productivity tasks |
| `9` | Image Creator | Generate/edit images with AI |
| `10` | Video | Create short/long-form video content |
| `11` | Social Media | Post to LinkedIn, X, Reddit, Facebook, Instagram |
| `12` | Copywriting | Research, write, publish articles and blog posts |
| `16` | SEO Expert | Keyword research, SERP analysis, on-page audits |
| `17` | Campaign Planner | Marketing plans, media plans, budget allocations |
| `18` | Digital Ads | Ad copy for Google, LinkedIn, X, TikTok |
| `19` | Coders | AI-assisted coding and debugging |
| `20` | Data Scientist | Analyze data, create charts, generate insights |
| `21` | Lead Generation | Find prospects via Apollo/ZoomInfo, draft outreach |

## Usage

### Run a task

```bash
python scripts/promarkia_run.py --squad 11 --prompt "Post about our new AI feature on LinkedIn and X"
```

### From OpenClaw (agent usage)

The agent calls `scripts/promarkia_run.py` with `--squad` and `--prompt` arguments.

### List available squads

```bash
python scripts/promarkia_run.py --list-squads
```

### Check a previous run

```bash
python scripts/promarkia_run.py --get-run RUN_ID
```

## Scheduling with OpenClaw Cron

Schedule recurring tasks using OpenClaw's built-in cron system:

**Daily LinkedIn post at 9 AM ET:**
```
/cron add --name "Daily LinkedIn Post" --schedule "0 9 * * *" --tz "America/New_York" --payload "Run Promarkia social squad: Post a LinkedIn article about our latest blog post"
```

**Weekly SEO audit every Monday:**
```
/cron add --name "Weekly SEO Audit" --schedule "0 10 * * 1" --tz "America/New_York" --payload "Run Promarkia SEO squad: Audit the top 5 pages on our website for SEO issues"
```

## Credentials / Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `PROMARKIA_API_KEY` | Yes | Your Promarkia API key (starts with `pmk_`) |
| `PROMARKIA_API_BASE` | No | API base URL (default: `https://www.promarkia.com`). Do not use `apis.promarkia.com`. |

## Notes

- Each task execution deducts credits from your Promarkia account
- Connected accounts (LinkedIn, X, Reddit, etc.) must be set up via the Promarkia web UI
- Task timeout defaults to 1200 seconds (20 minutes); override with `--timeout`
- Results are stored in your Promarkia account and can be retrieved later by run ID
