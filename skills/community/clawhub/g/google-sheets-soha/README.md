# google-sheets-soha

An OpenClaw skill for reading and analyzing data from Google Sheets. Supports both public and private sheets, with on-disk caching to avoid redundant API calls.

## Features

- Automatically extracts Sheet ID from URLs or accepts it directly from the user
- Supports **public sheets** (API Key) and **private sheets** (Service Account)
- On-disk cache with 5-minute TTL — skips API calls when data is still fresh
- Remembers Sheet ID throughout the conversation — never asks twice
- Replies in the same language as the user

## Requirements

- `python3` available in PATH
- `curl` available in PATH
- One of: `GOOGLE_API_KEY` (public sheet) or `GOOGLE_SERVICE_ACCOUNT_JSON` (private sheet)

## Installation

```bash
clawhub install google-sheets-soha
```

Restart OpenClaw after installation for the skill to be loaded.

## Configuration

Add to `~/.openclaw/openclaw.json` at the top level (alongside `agents`, not inside it):

### Public sheet (Anyone with the link)

```json
{
  "skills": {
    "entries": {
      "google-sheets-soha": {
        "enabled": true,
        "env": {
          "GOOGLE_API_KEY": "AIza..."
        }
      }
    }
  }
}
```

### Private sheet (Service Account)

```json
{
  "skills": {
    "entries": {
      "google-sheets-soha": {
        "enabled": true,
        "env": {
          "GOOGLE_SERVICE_ACCOUNT_JSON": "/home/node/.openclaw/google-sa.json"
        }
      }
    }
  }
}
```

## Getting Credentials

### Google API Key (public sheet)
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project → **APIs & Services → Library** → enable **Google Sheets API**
3. **APIs & Services → Credentials → Create Credentials → API Key**
4. Copy the key into your config

### Service Account (private sheet)
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project → enable **Google Sheets API**
3. **IAM & Admin → Service Accounts → Create Service Account**
4. Go to the **Keys** tab → **Add Key → JSON** → download the file
5. Copy the file to `~/.openclaw/google-sa.json`
6. Fix permissions: `sudo chown 1000:1000 ~/.openclaw/google-sa.json`
7. Open your Google Sheet → **Share** → paste the `client_email` from the JSON file → Viewer

## Usage

Just ask naturally — the skill activates automatically when it detects a Google Sheets-related request:

```
"Read this sheet: https://docs.google.com/spreadsheets/d/abc123/edit"
"What is the total revenue this month?"
"List all incomplete tasks"
"Compare January and February sales"
"Refresh the sheet"
```

## Cache

Data is cached at:
```
~/.openclaw/workspace/.cache/sheets/{spreadsheetId}/{tabName}.json
```

Default TTL is **5 minutes**. To clear the cache and force a fresh fetch, say:
- `"refresh"` / `"reload"` / `"get latest data"`

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| 403 Forbidden | Sheet not shared | Share the sheet with the service account email |
| 404 Not Found | Wrong Sheet ID | Double-check the URL |
| `python3` not found | Python not installed | Run `apt-get install -y python3` in the container |
| Permission denied (cache) | Wrong file ownership | Run `sudo chown -R 1000:1000 ~/.openclaw` |

## Security

This skill has been reviewed and is safe to use. Here is exactly what it does and does not do:

**What it accesses:**
- `sheets.googleapis.com` — to fetch spreadsheet data via Google Sheets API v4
- `oauth2.googleapis.com` — to authenticate your Service Account credentials

**What it does NOT do:**
- Does not send your data to any third-party service
- Does not store credentials anywhere other than your local machine
- Does not execute arbitrary remote code
- Does not write to your Google Sheet (read-only access)

**Env vars used:**

| Variable | Purpose | Required |
|---|---|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Path to Service Account JSON for private sheets | If using private sheets |
| `GOOGLE_API_KEY` | API key for public sheets | If using public sheets |

**Local execution:** The skill runs `python3` scripts locally inside your OpenClaw container to fetch and cache data. No Python code is sent to external servers.

**Cache:** Data is cached locally at `~/.openclaw/workspace/.cache/sheets/` with a 5-minute TTL. Cache files never leave your machine.

> If ClawHub flags this skill as suspicious, it is due to a [known platform issue](https://github.com/openclaw/clawhub/issues/522) where the security scanner does not always read env var declarations from SKILL.md frontmatter correctly. The declarations are present in the frontmatter — the scanner metadata mismatch is a false positive.

## License

MIT-0