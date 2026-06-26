---
name: opportunity-scout
description: "Hunt for real, expressed user pain points and unmet demand across Reddit, HN, and configurable sources. Finds demand signals like frustration posts, feature requests, workaround descriptions, and willingness-to-pay sentiment. Compiles findings into a prioritized digest with signal strength scoring, competition analysis, and trend tracking. Use when: opportunity scan, find opportunities, business ideas, market gaps, what are people asking for, niche research, demand signals, pain points, product ideas, gap analysis, what should I build, unmet needs."
---

# Opportunity Scout

Hunt for real demand signals — not news, not trends, but people expressing pain,
frustration, and unmet needs that represent building opportunities.

## Skill Directory

All paths below are relative to this skill's directory.

- `scripts/configure.py` — manage niches, keywords, sources, schedule
- `scripts/scan_sources.py` — generate search queries and process results
- `scripts/score_signals.py` — score and rank findings
- `scripts/digest.py` — generate prioritized markdown digest
- `scripts/history.py` — track signals over time, detect trends
- `references/signal-types.md` — what counts as a demand signal (read when scoring)
- `references/source-guide.md` — how to configure sources effectively
- `assets/config.example.json` — example niche configurations

## Data Files

All state lives in the skill directory:

- `config.json` — active configuration (created by configure.py)
- `history.json` — signal history log (created by history.py)
- `findings/` — raw and scored finding files per scan

## Workflow

### First-Time Setup

1. Run `configure.py --init` to create config.json from the example, or:
   - `configure.py --add-niche "AI tools for small business" --keywords "wish,need,looking for,alternative to,frustrated"`
   - `configure.py --add-source reddit:r/SaaS,reddit:r/smallbusiness,hackernews`
   - `configure.py --set-schedule daily`

### Running a Scan

Execute these steps in order:

1. **Generate queries**: Run `scan_sources.py --generate-queries` to get optimized
   search queries. It prints JSON with query strings.

2. **Execute searches**: For each query, call the `web_search` tool. Collect all
   results into a JSON array and save to a temp file.

3. **Ingest results**: Run `scan_sources.py --ingest <results.json>` to parse raw
   search results into standardized findings. Outputs findings JSON.

4. **Score findings**: Run `score_signals.py <findings.json>` to score each finding
   on signal strength, engagement, freshness, competition, and recurrence. Outputs
   scored JSON.

5. **Update history**: Run `history.py --update <scored.json>` to log findings and
   detect trend patterns (persistent, emerging, fading).

6. **Generate digest**: Run `digest.py <scored.json>` to produce the markdown report.
   Use `--output <path>` to save to a specific location (e.g., Obsidian vault).
   Use `--max-results 20` to limit output.

### Quick Scan (Single Command Summary)

For a rapid scan of a single niche without full config:

1. Run `scan_sources.py --quick "developer tools for AI agents"` to get queries
2. Execute web_search for each query
3. Pipe results through score and digest

### Reading References

- Before scoring or evaluating signals manually, read `references/signal-types.md`
  for the taxonomy of demand signals and how to distinguish real demand from noise.
- When helping users configure sources, read `references/source-guide.md`.

## Cron Integration

Set schedule in config.json via `configure.py --set-schedule daily|weekly`.
When triggered by cron, run the full scan workflow above. Save digest to the
user's preferred output location (default: skill directory `findings/`).

## Key Design Principles

- **Demand, not news**: Every finding should express unmet need, frustration, or a gap.
  Filter aggressively — 10 strong signals beat 100 weak ones.
- **Batch queries**: Combine niche + keywords into fewer, broader queries rather than
  one query per keyword. Respect rate limits.
- **Track over time**: Signals that persist across scans are more valuable than one-offs.
  Use history.py to surface persistent demand and fading trends.
- **Score honestly**: High engagement + low competition + recurring = strong opportunity.
  Don't inflate scores — the user needs signal, not noise.
