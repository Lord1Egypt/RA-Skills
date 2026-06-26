[中文](README.zh-TW.md) | English

# NotebookLM Studio Skill

AI agent skill for Google NotebookLM — import sources (URLs, YouTube, files, text) and generate podcasts, videos, reports, quizzes, flashcards, mind maps, slides, infographics, and data tables.

Works with **Claude Code**, **OpenClaw**, **Codex**, and any agent that supports the [Agent Skills](https://agentskills.io) specification.

![Full Flow Demo](assets/demo-full-flow.png)

## Features

- **9 artifact types**: audio, video, report, quiz, flashcards, mind-map, slide-deck, infographic, data-table
- **All source types**: URLs, YouTube, text notes, PDF, Word, audio, images, Google Drive
- **Multi-language output**: generates content in 30+ languages (default: Traditional Chinese)
- **Cross-platform**: works with any AI agent that reads SKILL.md
- **Telegram delivery**: two-round delivery with real-time status tracking (via OpenClaw)
- **Audio compression**: ffmpeg post-processing for Telegram's 50MB file size limit
- **CLI-driven**: uses `notebooklm` CLI directly — no custom Python wrappers

## Usage

Just tell your AI agent what you want. No CLI knowledge needed.

**Generate a study package from a URL:**
> Generate a report, quiz, and flashcards from this article
> https://example.com/deep-learning-intro

**Turn a YouTube video into a podcast and slides:**
> Make a podcast and slide deck from this video, use debate format
> https://youtube.com/watch?v=dQw4w9WgXcQ

**Create an infographic from a PDF:**
> Create a sketch-note style infographic from this paper
> *(attach file.pdf)*

**Full package via Telegram (OpenClaw):**
> 幫我用這篇文章做一份完整的學習包，包含 report、quiz、flashcards、podcast 和簡報
> https://example.com/article

The agent handles everything: creating the notebook, adding sources, generating artifacts, and delivering results back to you.

## How It Works

```
You ──────── "Generate a report and slides from this URL"
                │
                ▼
        AI Agent (Claude Code / OpenClaw / Codex)
                │  reads SKILL.md → 9-step workflow
                ▼
        notebooklm CLI
                │  create notebook → add sources → generate → download
                ▼
        ./output/<topic>/
            ├── report.md
            ├── slides.pdf
            ├── podcast.mp3
            └── ...
                │
                ▼  (optional, OpenClaw)
        Telegram ── delivers each artifact as it completes
```

## Artifact Types

| Type | CLI Command | Est. Time | Output |
|------|-------------|-----------|--------|
| Audio (Podcast) | `generate audio` | 5-30 min | MP3 |
| Video | `generate video` | 5-30 min | MP4 |
| Report | `generate report` | 1-2 min | Markdown |
| Quiz | `generate quiz` | 1-2 min | JSON/MD/HTML |
| Flashcards | `generate flashcards` | 1-2 min | JSON/MD/HTML |
| Mind Map | `generate mind-map` | Instant | JSON |
| Slide Deck | `generate slide-deck` | 2-10 min | PDF/PPTX |
| Infographic | `generate infographic` | 2-5 min | PNG |
| Data Table | `generate data-table` | 1-2 min | CSV |

See `references/artifacts.md` for full CLI options per artifact type.

## Setup

### Prerequisites

- **Python 3.10+**
- **ffmpeg** (for audio compression)
- **OS**: macOS, Linux (Ubuntu 20.04+), or Windows

### 1. Install the skill

**Option A — ClawHub (recommended):**
```bash
npm i -g clawhub        # install ClawHub CLI (one-time)
clawhub install notebooklm-studio
```

**Option B — Git clone:**
```bash
git clone --recurse-submodules https://github.com/jasontsaicc/notebooklm-studio-skill.git
cd notebooklm-studio-skill
```

### 2. Install notebooklm CLI

> **Both Option A and B require steps 2–5 below.**

The skill requires the `notebooklm` CLI tool. This is a separate dependency regardless of how you installed the skill.

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
```

**Ubuntu/Debian** — also install system dependencies for Chromium:
```bash
playwright install-deps chromium
```

### 3. Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install -y ffmpeg
```

### 4. Authenticate

**On a machine with a browser (Mac/Windows/Linux desktop):**
```bash
notebooklm login
```

**On a headless server (e.g. Ubuntu VPS):**

Run login on your local machine first, then transfer the credential:
```bash
# Local machine — login and verify
notebooklm login
notebooklm auth check

# Transfer to server
ssh user@server "mkdir -p ~/.notebooklm"
scp ~/.notebooklm/storage_state.json user@server:~/.notebooklm/storage_state.json
ssh user@server "chmod 600 ~/.notebooklm/storage_state.json"
```

### 5. Verify

```bash
notebooklm auth check --test
```

Expected: all checks pass, token fetch succeeds.

### 6. Install as agent skill (Option B only)

Skip this step if you used ClawHub. For Git clone:

**Claude Code:**
```bash
ln -s "$(pwd)" ~/.claude/skills/notebooklm-studio
```

**OpenClaw:**
```bash
ln -s "$(pwd)" /path/to/openclaw/skills/notebooklm-studio
```

**Other agents:** Place or symlink this directory where your agent discovers skills.

## Quick Demo (CLI)

After setup, try a quick end-to-end test without an AI agent:

```bash
# Create a notebook
notebooklm create "Test Notebook $(date +%Y%m%d)"
notebooklm use <notebook_id>    # use the ID from output above

# Add a source
notebooklm source add "https://en.wikipedia.org/wiki/Feynman_technique"

# Generate a report (fastest artifact, ~1 min)
notebooklm generate report --format study-guide --wait

# Download
mkdir -p output/feynman-technique
notebooklm download report ./output/feynman-technique/report.md

# Check result
cat ./output/feynman-technique/report.md
```

If this works, your setup is complete. The AI agent will follow the same workflow automatically via SKILL.md.

## Repository Structure

```
notebooklm-studio-skill/
├── SKILL.md                         # Agent skill definition (9-step workflow)
├── README.md
├── LICENSE
├── notebooklm-py/                   # git submodule (notebooklm CLI)
├── references/
│   ├── artifacts.md                 # 9 artifact types + CLI options
│   ├── artifact-options.md          # ASK/OFFER/SILENT option priorities
│   ├── source-types.md              # Source types & detection rules
│   ├── output-contracts.md          # Output format specifications
│   └── telegram-delivery.md         # Telegram delivery contract
├── scripts/
│   ├── compress_audio.sh            # ffmpeg audio compression
│   └── recover_tier2_delivery.sh    # Cron recovery for Tier 2 artifacts
└── assets/                          # Screenshots and demo media
```

## OpenClaw Timeout & Recovery Setup

Tier 2 artifacts (podcast, video, slides) take 5–40 minutes to generate. If the agent times out before they finish, they'll be generated on NotebookLM's server but never downloaded or delivered. This section sets up automatic recovery.

### 1. Agent Timeout

Set `timeoutSeconds: 1800` (30 min) for the notebooklm agent in your OpenClaw config:

```json
{
  "agents": {
    "list": [
      {
        "id": "notebooklm",
        "timeoutSeconds": 1800
      }
    ]
  }
}
```

This covers most Tier 2 artifacts. For cinematic video (Veo 3, ~40 min), consider `2400`.

### 2. Tier 2 Recovery Cron (every 5 min)

If the agent times out mid-delivery, `delivery-status.json` tracks what's still pending. The recovery script polls, downloads, and updates status automatically.

```bash
# crontab -e
*/5 * * * * cd /path/to/notebooklm-studio-skill && bash scripts/recover_tier2_delivery.sh ./output >> /var/log/notebooklm-recovery.log 2>&1
```

What it does:
- Scans `output/*/delivery-status.json` for `"status": "pending"` artifacts
- Polls each via `notebooklm artifact poll <task_id>`
- If `completed` → downloads, compresses audio, updates status
- If `failed` → marks as failed
- If `processing` → skips (next run will retry)

### 3. Health Check Cron (every 30 min)

Catch expired sessions before they block recovery:

```bash
# crontab -e
*/30 * * * * notebooklm auth check --test --json | python3 -c "import json,sys; d=json.load(sys.stdin); exit(0 if d['status']=='ok' else 1)" || echo "$(date): AUTH EXPIRED — run notebooklm login" >> /var/log/notebooklm-health.log
```

### Troubleshooting

**"Tier 2 artifacts generated but never delivered"**

This happens when the agent times out during `artifact wait`. Check and recover:

```bash
# See what's pending
python3 -c "
import json, glob
for f in glob.glob('output/*/delivery-status.json'):
    data = json.load(open(f))
    pending = [a for a in data['artifacts'] if a['status'] == 'pending']
    if pending:
        print(f'{f}: {len(pending)} pending')
        for a in pending:
            print(f'  {a[\"type\"]} — task_id: {a[\"task_id\"]}')
"

# Manual recovery
bash scripts/recover_tier2_delivery.sh ./output
```

**"Auth check failed" in recovery log**

Session expired. Re-login and recovery will resume on the next cron cycle:

```bash
notebooklm login
notebooklm auth check --test   # verify
```

**"Recovery runs but artifacts stay pending"**

The artifact may still be generating. Check manually:

```bash
notebooklm artifact poll <task_id> --json
```

If `processing` → wait. If stuck for 60+ minutes → check the [NotebookLM web UI](https://notebooklm.google.com) directly.

## Updating notebooklm-py

```bash
cd notebooklm-py && git pull origin main && cd ..
pip install -e "notebooklm-py[browser]"
```

## Powered By

- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) — Unofficial Python API & CLI for Google NotebookLM

## License

MIT
