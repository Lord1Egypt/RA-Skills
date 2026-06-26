# Promarkia Skill for OpenClaw

Run [Promarkia](https://www.promarkia.com) AI squads directly from OpenClaw — automate social media posts, copywriting, SEO audits, ad creation, lead generation, and more.

## Quick Start

### 1. Get a Promarkia Account

1. Go to [promarkia.com](https://www.promarkia.com) and sign in with Google
2. Purchase credits or subscribe to a plan

### 2. Connect Your Accounts

Before running squads that publish content, connect the platforms you want to use:

1. Log in to Promarkia
2. Click **Connect Integrations** in the sidebar
3. Connect the platforms you need:
   - **Social Media Squad:** LinkedIn, X/Twitter, Reddit, Facebook, Instagram
   - **Copywriting Squad:** WordPress, Google Docs, Notion
   - **Lead Generation Squad:** Apollo, ZoomInfo, Salesforce, HubSpot
   - **Video Squad:** YouTube, TikTok
   - Other squads may require Google Sheets, Google Drive, etc.

Each platform uses OAuth — you'll be redirected to authorize Promarkia to post on your behalf.

### 3. Generate an API Key

1. Log in to Promarkia
2. Click **API Keys** in the sidebar
3. Click **Generate** and give your key a name (e.g., "OpenClaw")
4. **Copy the key immediately** — it's only shown once
5. Set it as an environment variable:

```bash
# Linux/macOS
export PROMARKIA_API_KEY=pmk_your_key_here

# Windows (PowerShell)
$env:PROMARKIA_API_KEY = "pmk_your_key_here"

# Or add to your OpenClaw config under skills.entries.promarkia.env
```

### 4. Install the Skill

Copy this folder to your OpenClaw skills directory:

```
~/.openclaw/workspace/skills/promarkia/
```

Or add the parent directory to `skills.load.extraDirs` in your OpenClaw config.

## Usage

### Chat with OpenClaw

Just ask naturally:

> "Run the Promarkia social squad to post about our new product launch on LinkedIn and X"

> "Use Promarkia to write a blog post about AI in marketing"

> "Run a Promarkia SEO audit on our homepage"

### Command Line

```bash
# List available squads
python scripts/promarkia_run.py --list-squads

# Run a task
python scripts/promarkia_run.py --squad 11 --prompt "Post about our AI feature on LinkedIn"

# Check a previous run
python scripts/promarkia_run.py --get-run 123456
```

### Schedule Recurring Tasks

Use OpenClaw's cron system to schedule automated runs:

```
/cron add --name "Daily LinkedIn Post" \
  --schedule "0 9 * * *" \
  --tz "America/New_York" \
  --payload "Run Promarkia social squad: Post a LinkedIn article highlighting our latest blog post"
```

## Available Squads

| ID | Squad | Integrations Needed |
|----|-------|-------------------|
| 1 | Assistant | Gmail, Outlook, Calendar |
| 9 | Image Creator | Google Drive |
| 10 | Video | YouTube, TikTok |
| 11 | Social Media | LinkedIn, X, Reddit, Facebook, Instagram |
| 12 | Copywriting | Google Docs, Notion, WordPress |
| 16 | SEO Expert | Google |
| 17 | Campaign Planner | Google Docs, Notion, Sheets |
| 18 | Digital Ads | Google, LinkedIn, X, TikTok |
| 19 | Coders | (none) |
| 20 | Data Scientist | Google Sheets |
| 21 | Lead Generation | Apollo, ZoomInfo, Salesforce, HubSpot |

## How It Works

1. Your OpenClaw agent calls `scripts/promarkia_run.py` with a squad ID and prompt
2. The script authenticates with your API key against `www.promarkia.com`
3. Promarkia creates a session, connects to your linked accounts, and executes the squad
4. Results are returned and credits are deducted from your Promarkia balance
5. Run history is stored in your Promarkia account for later retrieval

## Configuration

| Environment Variable | Required | Default | Description |
|---------------------|----------|---------|-------------|
| `PROMARKIA_API_KEY` | Yes | — | Your API key (starts with `pmk_`) |
| `PROMARKIA_API_BASE` | No | `https://www.promarkia.com` | API endpoint |

## Troubleshooting

**"Insufficient credits"** — Purchase more credits or upgrade your plan at promarkia.com.

**"Invalid API key"** — Check that `PROMARKIA_API_KEY` is set correctly. Keys start with `pmk_`.

**"Task execution timed out"** — Some squads (video, complex copywriting) can take up to 20 minutes. Try increasing `--timeout`.

**"User account not found"** — Make sure the API key belongs to an active Promarkia account.

**Squad returns empty result** — Ensure the required integrations are connected in Promarkia (e.g., LinkedIn for Social Media Squad).

## Support

- Website: [promarkia.com](https://www.promarkia.com)
- Documentation: [blog.promarkia.com](https://blog.promarkia.com)
