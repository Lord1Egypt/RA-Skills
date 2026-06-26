---
name: openclaw-token-usage
description: Inspect token usage from local OpenClaw transcripts across a specified time range. Use when the user asks how many tokens were consumed in OpenClaw, GitHub Copilot model usage inside OpenClaw, or wants usage broken down by day, agent, provider, model, session, rankings, CSV exports, or markdown reports.
---

# OpenClaw Token Usage

Use the bundled script to aggregate token usage recorded in local OpenClaw transcript files under `~/.openclaw/agents/*/sessions/`.

## Quick start

Run:

```bash
python3 ~/.openclaw/workspace/skills/openclaw-token-usage/scripts/report_openclaw_token_usage.py \
  --from '2026-03-14' \
  --to '2026-03-16' \
  --tz 'UTC+8'
```

Default output includes:
- total usage
- daily × agent breakdown
- agent totals
- model totals

Optional additions:
- `--top-sessions 10` for Top N session ranking
- `--csv-dir ~/.openclaw/workspace/output/token-usage-csv` for CSV exports
- `--format json` for structured output including session totals
- `--format markdown` for a ready-to-share report

## Workflow

1. Confirm the time range.
   - Accept natural ranges from the user, but convert them to explicit timestamps before running the script.
   - Default timezone should match the user's expectation; use `UTC+8` unless they ask otherwise.
2. Decide the scope.
   - All agents by default.
   - Narrow with `--agents` when the user asks for specific agents.
   - Narrow with `--providers` or `--models` when the user wants only some models.
3. Decide the output shape.
   - Human summary by default.
   - JSON when another tool/script will consume the result.
   - CSV when the user wants spreadsheet/report-friendly output.
   - Markdown when the user wants a report for docs, messages, or status updates.
   - `--top-sessions` when the user wants ranking or hotspot analysis.
4. Run the script.
5. Report the result in plain language.
   - Call out timezone assumptions.
   - Mention that counts are transcript-based and deduplicated across `.reset` / `.deleted` transcript copies.
   - Clarify that local transcript usage does not cover IDE-side GitHub Copilot usage outside OpenClaw.

## Recommended commands

All agents, human-readable summary:

```bash
python3 ~/.openclaw/workspace/skills/openclaw-token-usage/scripts/report_openclaw_token_usage.py \
  --from '2026-03-14' \
  --to '2026-03-16' \
  --tz 'UTC+8'
```

Only GitHub Copilot provider:

```bash
python3 ~/.openclaw/workspace/skills/openclaw-token-usage/scripts/report_openclaw_token_usage.py \
  --from '2026-03-14' \
  --to '2026-03-16' \
  --tz 'UTC+8' \
  --providers github-copilot
```

Specific agents:

```bash
python3 ~/.openclaw/workspace/skills/openclaw-token-usage/scripts/report_openclaw_token_usage.py \
  --from '2026-03-14' \
  --to '2026-03-16' \
  --tz 'UTC+8' \
  --agents main,xiaocheng,xiaowen
```

Top sessions ranking:

```bash
python3 ~/.openclaw/workspace/skills/openclaw-token-usage/scripts/report_openclaw_token_usage.py \
  --from '2026-03-14' \
  --to '2026-03-16' \
  --tz 'UTC+8' \
  --top-sessions 10
```

JSON export:

```bash
python3 ~/.openclaw/workspace/skills/openclaw-token-usage/scripts/report_openclaw_token_usage.py \
  --from '2026-03-14' \
  --to '2026-03-16' \
  --tz 'UTC+8' \
  --format json \
  --output ~/.openclaw/workspace/output/token-usage.json
```

CSV exports:

```bash
python3 ~/.openclaw/workspace/skills/openclaw-token-usage/scripts/report_openclaw_token_usage.py \
  --from '2026-03-14' \
  --to '2026-03-16' \
  --tz 'UTC+8' \
  --csv-dir ~/.openclaw/workspace/output/token-usage-csv
```

Markdown report:

```bash
python3 ~/.openclaw/workspace/skills/openclaw-token-usage/scripts/report_openclaw_token_usage.py \
  --from '2026-03-14' \
  --to '2026-03-16' \
  --tz 'UTC+8' \
  --format markdown \
  --output ~/.openclaw/workspace/output/token-usage-report.md
```

## Output notes

The script reports these metrics when present in transcripts:
- `input`
- `output`
- `cacheRead`
- `cacheWrite`
- `totalTokens`
- `messages`

Session notes:
- Session totals are inferred from transcript files and `sessions.json` indexes when available.
- If a transcript file cannot be mapped back to a session key, the script falls back to `file:<filename>`.

Markdown report notes:
- Includes scope, summary, by-day table, by-agent table, by-model table, Top sessions, and auto-generated findings.
- Suitable for sharing in docs or pasting into chat after light editing.

Important:
- Some transcript entries may show a model/provider but still have zero token usage recorded.
- This skill measures usage visible in local OpenClaw transcripts. It does not cover IDE-side GitHub Copilot usage outside OpenClaw.
- If the user asks specifically for GitHub Copilot usage inside OpenClaw, prefer `--providers github-copilot`.
