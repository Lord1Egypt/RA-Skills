---
name: weekly-retro
description: "Weekly retrospective that analyzes memory logs to identify accomplishments, recurring patterns, friction points, and forward-looking recommendations. More strategic than a daily recap — answers 'what should change next week?' Use when: weekly retro, weekly review, what should change, how was this week, retrospective, week in review."
---

# Weekly Retro

Generate a strategic weekly retrospective from memory log files.

## Quick Start

Run the full pipeline:

```
python3 scripts/gather_week.py --memory-dir PATH | \
python3 scripts/analyze.py | \
python3 scripts/retrospective.py --output vault/weekly-retro/YYYY-MM-DD.md
```

## Pipeline

| Step | Script | Input | Output |
|------|--------|-------|--------|
| 1. Gather | `gather_week.py` | memory/*.md files | Structured JSON (per-day + aggregated) |
| 2. Analyze | `analyze.py` | Gathered JSON | Pattern analysis JSON |
| 3. Report | `retrospective.py` | Analysis JSON | Markdown retrospective |

## Scripts

### gather_week.py

Read memory files for the past N days and extract structured data.

```
python3 scripts/gather_week.py --memory-dir ~/.openclaw/workspace/memory --days 7
```

Options:
- `--memory-dir PATH` — Path to memory directory (default: ~/.openclaw/workspace/memory)
- `--days N` — Number of days to look back (default: 7)
- `--end-date YYYY-MM-DD` — End date (default: today)
- `--config PATH` — Config JSON file

### analyze.py

Detect patterns from gathered data. Reads JSON from stdin.

Identifies:
- Accomplishments (shipped, published, fixed, built)
- Recurring themes (topics appearing 3+ days)
- Repeated failures and friction points
- Time sinks (disproportionate attention)
- Unfinished threads (started but not completed)
- Work schedule patterns (time-of-day distribution)

```
python3 scripts/gather_week.py ... | python3 scripts/analyze.py
```

Options:
- `--history-file PATH` — Path to retro history for longitudinal comparison

### retrospective.py

Generate the markdown retrospective. Reads analysis JSON from stdin.

Sections:
- Week at a Glance (3-sentence summary)
- Wins (with evidence)
- Patterns (recurring topics, toolchain, work schedule, attention distribution)
- Friction Points (with recurrence flags)
- Unfinished Business (carry-forward items)
- Recommendations (2-3 actionable changes for next week)
- Week Score (1-10 with justification)

```
python3 scripts/analyze.py ... | python3 scripts/retrospective.py --output PATH
```

Options:
- `--output PATH` — Write to file instead of stdout
- `--no-frontmatter` — Skip YAML frontmatter

### history.py

Track retrospective history for longitudinal patterns.

```
python3 scripts/history.py --record --analysis analysis.json
python3 scripts/history.py --show
python3 scripts/history.py --trends
```

Options:
- `--record` — Record this week's analysis
- `--analysis PATH` — Analysis JSON to record
- `--show` — Show past retro summaries
- `--trends` — Show longitudinal trends
- `--data-dir PATH` — Storage directory

## Cron Integration

Schedule a Sunday evening retrospective:

```json
{
  "name": "Weekly Retrospective",
  "schedule": {"kind": "cron", "expr": "0 20 * * 0", "tz": "America/New_York"},
  "payload": {
    "kind": "agentTurn",
    "message": "Run the weekly-retro skill. Gather the past 7 days of memory logs, analyze patterns, generate the retrospective, and save to vault/weekly-retro/."
  }
}
```

## Output

The retrospective is Obsidian-compatible markdown with YAML frontmatter including date range, week score, and auto-detected tags. Designed for vault storage and long-term pattern review.

## Dependencies

Python standard library only. No external packages required.
