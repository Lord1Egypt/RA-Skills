---
name: nex-life-logger
description: Track computer activity (browser history, active windows, YouTube videos) locally and query it with AI. All activity data stays on your machine. LLM features require explicit user configuration. Ask your agent what you were doing at any time.
version: 1.1.0
metadata:
  clawdbot:
    emoji: "\U0001F9E0"
    requires:
      bins:
        - python3
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "lib/*"
      - "setup.sh"
---

# Nex Life Logger

AI-powered local activity tracker. Your agent remembers everything you did on your computer. All activity data stays on your machine. LLM features require explicit configuration.

## When to Use

Use this skill when the user asks about:

- Their browsing history, what websites they visited
- What they were working on yesterday, last week, this month
- Their computer activity or screen time
- Time spent on specific topics, websites, or applications
- YouTube videos they watched and what was discussed in them
- Their productivity patterns or how they spent their time
- Searching their personal history for anything (tools, topics, projects)
- Generating summaries of their activity (daily, weekly, monthly)
- Keywords, topics, or tools they've been using
- Exporting their activity data

Trigger phrases: "what was I doing", "browsing history", "computer activity", "what did I work on", "time spent", "YouTube watch history", "productivity", "what I did yesterday", "last week", "search my history"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs dependencies in a virtual environment, initializes the database, and starts the background collector service.

## Available Commands

The CLI tool is `nex-life-logger`. All commands output plain text.

### Search

FTS5-powered full-text search across all tracked data with filters and relevance ranking:

```bash
nex-life-logger search "docker containers"
nex-life-logger search "machine learning" --since 2026-03-01 --until 2026-04-01
nex-life-logger search "react" --kind url --source chrome --limit 50
nex-life-logger search "python" --kind app_focus
nex-life-logger search "kubernetes" --category tool
nex-life-logger search "AI agents" --output json
```

Search filters:
- `--kind`: Filter activities by type (url, search, youtube, app_focus)
- `--source`: Filter activities by browser/source (chrome, edge, brave, firefox, window)
- `--category`: Filter keywords by category (topic, tool, language, project, domain, search)
- `--limit`: Max results per section (default: 30)
- `--since` / `--until`: Date range (ISO format)
- `--output json`: Machine-readable JSON output for programmatic use

### Summaries

View AI-generated summaries:

```bash
nex-life-logger summary daily
nex-life-logger summary daily --date 2026-04-03
nex-life-logger summary weekly
nex-life-logger summary monthly
nex-life-logger summary yearly
```

### Activities

View recent raw activities:

```bash
nex-life-logger activities --last 2h
nex-life-logger activities --last 1d
nex-life-logger activities --since 2026-04-03 --until 2026-04-04
nex-life-logger activities --kind youtube
nex-life-logger activities --kind search
nex-life-logger activities --kind app_focus
```

### Keywords

View extracted keywords and topics:

```bash
nex-life-logger keywords --top 20
nex-life-logger keywords --category tool
nex-life-logger keywords --since 2026-04-01
```

### Transcripts

View YouTube video transcripts:

```bash
nex-life-logger transcript <video_id>
nex-life-logger transcripts --last 7d
```

### Statistics

```bash
nex-life-logger stats
nex-life-logger stats --date 2026-04-03
```

### Generate Summaries

Generate AI summaries on demand (requires LLM configuration):

```bash
nex-life-logger generate daily
nex-life-logger generate weekly
nex-life-logger generate monthly --date 2026-03-01
```

### Export

```bash
nex-life-logger export json --output export.json
nex-life-logger export csv --output activities.csv
nex-life-logger export html --output report.html
```

### Service Management

```bash
nex-life-logger service status
nex-life-logger service start
nex-life-logger service stop
nex-life-logger service logs
```

### Configuration

```bash
nex-life-logger config show
nex-life-logger config set-api-key
nex-life-logger config set-provider openai
nex-life-logger config set-model gpt-4o
nex-life-logger config set-api-base https://api.openai.com/v1
nex-life-logger config set-poll-interval 60
nex-life-logger config rebuild-fts
```

The `rebuild-fts` command rebuilds the FTS5 search indexes from scratch. Run this after importing data, syncing the database from another machine, or if search results seem incomplete.

## Example Interactions

**User:** "What was I working on yesterday afternoon?"
**Agent runs:** `nex-life-logger activities --last 1d --kind url` and `nex-life-logger activities --last 1d --kind app_focus`
**Agent:** Presents the activities naturally, grouping by topic.

**User:** "How much time did I spend on YouTube this week?"
**Agent runs:** `nex-life-logger activities --last 7d --kind youtube`
**Agent:** Counts the YouTube entries and presents a summary.

**User:** "Show me my productivity summary for last week"
**Agent runs:** `nex-life-logger summary weekly`
**Agent:** Presents the weekly summary if it exists, or runs `nex-life-logger generate weekly` first.

**User:** "What were the main topics I researched in March?"
**Agent runs:** `nex-life-logger keywords --since 2026-03-01 --top 20`
**Agent:** Lists the top keywords and topics.

**User:** "Search my history for anything related to Docker"
**Agent runs:** `nex-life-logger search "docker"`
**Agent:** Presents matching activities, summaries, and transcripts ranked by relevance.

**User:** "What Docker stuff did I look at in Chrome specifically?"
**Agent runs:** `nex-life-logger search "docker" --kind url --source chrome`
**Agent:** Shows only Chrome browsing results related to Docker.

**User:** "What YouTube videos did I watch about machine learning?"
**Agent runs:** `nex-life-logger search "machine learning" --kind youtube`
**Agent:** Lists the videos and summarizes what was discussed based on transcript snippets.

**User:** "Give me a JSON dump of all Python-related activity from last week"
**Agent runs:** `nex-life-logger search "python" --since 2026-03-29 --output json`
**Agent:** Returns structured JSON for further processing.

**User:** "Generate a daily summary for today"
**Agent runs:** `nex-life-logger generate daily`
**Agent:** Shows the generated summary.

**User:** "Give me overall stats about my tracked data"
**Agent runs:** `nex-life-logger stats`
**Agent:** Presents the statistics in a readable format.

**User:** "What tools and languages have I been using the most?"
**Agent runs:** `nex-life-logger keywords --category tool --top 15` and `nex-life-logger keywords --category language --top 10`
**Agent:** Combines the results into a clear overview.

**User:** "Export all my data to JSON"
**Agent runs:** `nex-life-logger export json --output ~/life-logger-backup.json`
**Agent:** Confirms the export location.

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Section headers followed by `---` separators
- List items prefixed with `- `
- Timestamps in ISO-8601 format
- Every command output ends with `[Nex Life Logger by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally. Do not show raw database paths or internal details.

## Important Notes

- All activity data is stored locally at `~/.life-logger/`. No telemetry, no analytics.
- No external API calls are made unless the user has explicitly configured an LLM provider. There are no default API endpoints.
- The background collector must be running for new data to be collected. If the user asks about tracking and the collector is not running, suggest `nex-life-logger service start`.
- LLM configuration is required for AI-powered features (summary generation). The `activities`, `keywords`, `stats`, `search`, and `transcripts` commands work without LLM.
- The collector fetches YouTube transcripts from YouTube (network access) when productive videos are detected.
- The collector tracks: browser history (Chrome, Edge, Brave, Firefox), active window focus, and YouTube transcripts.
- Chat/messaging apps and sensitive windows (password managers, banking) are automatically filtered out.
- Only productive content is tracked (AI, programming, design, building, learning). Entertainment, politics, and news are filtered.

## Troubleshooting

- **"Search returns no results but data exists"**: Run `nex-life-logger config rebuild-fts` to rebuild the search indexes.
- **"Database not found"**: Run `nex-life-logger service start` or `bash setup.sh` to initialize.
- **"LLM not configured"**: Run `nex-life-logger config set-api-key` then `nex-life-logger config set-provider <name>`.
- **No recent data**: Check if the collector is running with `nex-life-logger service status`. Start it with `nex-life-logger service start`.
- **Empty search results**: The collector may not have been running during that time period. Check `nex-life-logger stats` to see the data range.

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
