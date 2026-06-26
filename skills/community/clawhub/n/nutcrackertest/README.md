# UXR Observer

**Ethnographic UX research for OpenClaw — understand how you actually use your AI agent.**

UXR Observer is an OpenClaw skill that passively analyzes your interaction history and produces research-grade ethnographic reports. It goes beyond session counts and token usage to surface *why* you interact the way you do: friction points, delight moments, behavioral patterns, and actionable recommendations.

## What It Does

- **Passive observation** — Reads your session transcripts (`.jsonl` files) without modifying anything
- **PII redaction** — All data is stripped of emails, phone numbers, API keys, file paths, and names before storage
- **Ethnographic analysis** — Classifies tasks, detects friction and delight signals, identifies desire paths and workarounds
- **Daily reports** — Structured Markdown reports with executive summaries, friction logs, verbatim quotes, and recommendations
- **Longitudinal trends** — Track how your usage evolves over weeks and months
- **Behavioral archetypes** — Characterizes your relationship with the agent (power delegator, cautious verifier, efficient querier, etc.)

## Installation

```bash
# Clone or copy to your skills directory
cp -r uxr-observer ~/.openclaw/workspace/skills/

# Refresh skills in OpenClaw
# Ask your agent: "refresh skills"
```

### Requirements

- `python3` (3.8+)
- `jq`

## Usage

| Command | Description |
|---------|-------------|
| `/uxr` | Generate today's report |
| `/uxr report 2025-01-15` | Report for a specific date |
| `/uxr trends` | Longitudinal trend analysis |
| `/uxr friction` | Focused friction analysis (last 7 days) |
| `/uxr quotes` | Notable verbatim quotes |
| `/uxr status` | Data collection status |

## Automated Daily Reports

Set up a cron job to generate reports automatically:

```bash
openclaw cron add \
  --id "daily-uxr-report" \
  --schedule "0 22 * * *" \
  --message "Run /uxr report for today. Save to the reports directory."
```

## What's in a Report?

Each daily report includes:

1. **Executive Summary** — 2-3 sentence overview
2. **Session Statistics** — Counts, durations, costs, peak hours
3. **Task Breakdown** — Categorized activity distribution (coding, research, writing, automation, etc.)
4. **Top Findings** — 3-5 key ethnographic observations ranked by significance
5. **Friction Log** — Moments of difficulty with context and severity ratings
6. **Delight Log** — Moments of success and satisfaction
7. **Verbatim Quotes** — Redacted user quotes annotated with sentiment
8. **Tool/Skill Usage** — Frequency and success rates
9. **Behavioral Archetype** — Your evolving usage personality
10. **Behavioral Trends** — Comparison against recent history
11. **Recommendations** — Actionable suggestions for improving your setup

## Privacy

- **100% local** — All data stays on your machine. Nothing is transmitted anywhere.
- **PII redacted** — Raw messages are never stored. Emails, phones, API keys, paths, and names are replaced with `[EMAIL]`, `[PHONE]`, `[API_KEY]`, `[PATH]`, `[NAME]` placeholders.
- **User-controlled** — Inspect or delete any stored data at any time in the skill's `data/` and `reports/` directories.

## File Structure

```
uxr-observer/
├── SKILL.md              # Skill definition
├── scripts/
│   ├── collect.sh        # Session data extraction
│   ├── redact.py         # PII redaction
│   ├── analyze.py        # Ethnographic analysis engine
│   └── report.py         # Report generator
├── templates/
│   └── daily-report.md   # Report template
├── data/                 # Stored analysis data (created at runtime)
├── reports/              # Generated reports (created at runtime)
└── README.md
```

## Design Philosophy

Traditional analytics tell you *what* happened. Ethnographic analysis tells you *why*. UXR Observer produces the kind of output a Staff UX Researcher would use to inform product decisions: friction logs, verbatim quotes, desire paths, and behavioral archetypes.

## Publishing to ClawHub

```bash
cd ~/.openclaw/workspace/skills
clawhub login
clawhub publish uxr-observer --tag latest
```

## License

MIT
