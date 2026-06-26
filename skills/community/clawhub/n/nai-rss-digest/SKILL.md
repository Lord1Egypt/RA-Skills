---
name: rss-digest
description: Generate a structured daily or weekly digest from an OPML file of RSS/Atom feeds. Fetches articles from a configurable time window (last 24h or 7 days), optionally filters by keywords/topics, and outputs a formatted markdown file suitable for Obsidian or Discord. Use when the user asks to: generate an RSS digest, summarize their feeds, build a news roundup, read their OPML feeds, or schedule a daily/weekly newsletter from RSS. Triggers on phrases like "rss digest", "feed digest", "summarize my feeds", "daily news roundup", "weekly digest from OPML", or "what's in my feeds today".
---

# RSS Digest

Generate a markdown digest from an OPML feed list. No API keys required. Uses only Python stdlib.

## Scripts

| Script | Purpose | Input | Output |
|---|---|---|---|
| `scripts/parse_opml.py` | Parse OPML → feed list | OPML file path | JSON array (stdout) |
| `scripts/fetch_feeds.py` | Fetch feeds → articles | JSON feed list (stdin or `--feeds`) | JSON array (stdout) |
| `scripts/build_digest.py` | Articles → markdown | JSON articles (stdin) | Markdown (stdout or `--output`) |

Reference OPML: `references/opml-example.opml`

All scripts write progress/errors to stderr, data to stdout — safe to pipe.

## Setup

Make scripts executable once:

```bash
chmod +x ~/.openclaw/workspace/skills/rss-digest/scripts/*.py
```

Set a variable for convenience:

```bash
SKILL=~/.openclaw/workspace/skills/rss-digest
```

## One-Time Digest

Run the full pipeline:

```bash
python3 $SKILL/scripts/parse_opml.py ~/feeds.opml \
  | python3 $SKILL/scripts/fetch_feeds.py --hours 24 \
  | python3 $SKILL/scripts/build_digest.py --period Daily --output ~/digest.md
```

Open `~/digest.md` in Obsidian or cat to terminal.

## Weekly Digest

```bash
python3 $SKILL/scripts/parse_opml.py ~/feeds.opml \
  | python3 $SKILL/scripts/fetch_feeds.py --hours 168 \
  | python3 $SKILL/scripts/build_digest.py --period Weekly --group-by category --output ~/weekly-digest.md
```

## Keyword Filtering

Only include articles matching specific topics:

```bash
python3 $SKILL/scripts/parse_opml.py ~/feeds.opml \
  | python3 $SKILL/scripts/fetch_feeds.py --hours 24 --keywords "AI,machine learning,LLM" \
  | python3 $SKILL/scripts/build_digest.py --title "AI Digest"
```

`--keywords` is comma-separated, case-insensitive. Matches title or summary.

## Cron Schedule

Add to crontab (`crontab -e`) for a daily digest at 7 AM ET:

```cron
0 7 * * * python3 /Users/openclaw/.openclaw/workspace/skills/rss-digest/scripts/parse_opml.py ~/feeds.opml | python3 /Users/openclaw/.openclaw/workspace/skills/rss-digest/scripts/fetch_feeds.py --hours 24 | python3 /Users/openclaw/.openclaw/workspace/skills/rss-digest/scripts/build_digest.py --period Daily --output /Users/openclaw/.openclaw/workspace/vault/daily-recap/rss-$(date +\%Y-\%m-\%d).md
```

Weekly digest every Monday at 8 AM:

```cron
0 8 * * 1 python3 /Users/openclaw/.openclaw/workspace/skills/rss-digest/scripts/parse_opml.py ~/feeds.opml | python3 /Users/openclaw/.openclaw/workspace/skills/rss-digest/scripts/fetch_feeds.py --hours 168 | python3 /Users/openclaw/.openclaw/workspace/skills/rss-digest/scripts/build_digest.py --period Weekly --group-by category --output /Users/openclaw/.openclaw/workspace/vault/daily-recap/rss-weekly-$(date +\%Y-\%m-\%d).md
```

## Options Reference

### fetch_feeds.py

| Flag | Default | Description |
|---|---|---|
| `--hours N` | 24 | Articles from last N hours |
| `--keywords K` | (none) | Comma-separated filter keywords |
| `--feeds FILE` | stdin | JSON feed list file (alternative to piping) |
| `--timeout N` | 10 | HTTP timeout per feed in seconds |

### build_digest.py

| Flag | Default | Description |
|---|---|---|
| `--title STR` | "RSS Digest" | Digest heading title |
| `--period STR` | "Daily" | Period label (Daily / Weekly) |
| `--output FILE` | stdout | Write to file instead of stdout |
| `--group-by STR` | "feed" | Group by: `feed`, `category`, or `none` |
| `--max-summary N` | 300 | Max chars of article summary (0 = omit) |
| `--date STR` | today | Override the date label |

## OPML File

Export your OPML from any RSS reader (Feedly, NetNewsWire, Reeder, Inoreader, etc.) via their export settings. See `references/opml-example.opml` for the expected format. Feeds can be flat or nested inside category folders.

## Output Format

The digest is clean markdown with:
- H1 title with article count
- H2 sections per feed/category
- Linked article titles, publication time, and truncated summary
- Footer with generation timestamp

Suitable for pasting into Discord (plain markdown), saving to Obsidian, or emailing.

## Error Handling

- Unreachable feeds are skipped with a stderr warning — the rest continue.
- Articles with no publish date are included (can't apply time filter to them).
- Malformed XML feeds are skipped gracefully.
- Empty result sets produce a "No articles found" digest rather than crashing.
