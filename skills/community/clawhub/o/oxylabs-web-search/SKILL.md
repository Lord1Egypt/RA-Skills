---
name: oxylabs-web-search
description: >-
  Search the web and read web pages with Oxylabs AI Studio (alternative to
  Brave, DuckDuckGo or Tavily).

  Use this whenever the user wants to search the web, look something up, find
  current information or news, gather sources and links, or fetch the content of
  a specific page.

  It has two commands. `search` returns matching pages — titles, URLs, and
  optionally the page text. `scrape` pulls the content of a single URL as clean
  Markdown.

  It handles JavaScript-heavy sites and geo-targeting, has a free tier, and runs
  as dependency-free Python.
metadata:
  openclaw:
    requires:
      env:
        - OXYLABS_AI_STUDIO_API_KEY
    primaryEnv: OXYLABS_AI_STUDIO_API_KEY
    envVars:
      - name: OXYLABS_AI_STUDIO_API_KEY
        required: true
        description: Oxylabs AI Studio API key.
---

# Oxylabs Web Search & Data

One tool for getting things off the web — pick a subcommand:

- `search` — find pages for a query (titles, URLs, and optional page text)
- `scrape` — get the content of one URL

## Setup

Get an Oxylabs AI Studio API key from https://aistudio.oxylabs.io/api-key.
Pass API KEY to OpenClaw via one of following methods:

### OpenClaw config (`~/.openclaw/openclaw.json`) (RECOMMENDED):

```json
{
  "skills": {
    "entries": {
      "oxylabs-web-search": {
        "enabled": true,
        "apiKey": "YOUR_OXYLABS_AI_STUDIO_API_KEY"
      }
    }
  }
}
```

### Export environment variable:

```bash
export OXYLABS_AI_STUDIO_API_KEY="YOUR_OXYLABS_AI_STUDIO_API_KEY"
```

### Via .env file

For `~/.openclaw/.env`, add the assignment:

```dotenv
OXYLABS_AI_STUDIO_API_KEY=YOUR_OXYLABS_AI_STUDIO_API_KEY
```

## Usage

```bash
# search the web
python3 scripts/oxylabs.py search "<query>" -n 5
python3 scripts/oxylabs.py search "<query>" -n 3 --content   # + page text per result

# get one page as Markdown
python3 scripts/oxylabs.py scrape "<url>"
```

Common flags: `--geo` (two-letter ISO country) · `--render-js` (off by default;
slower).
