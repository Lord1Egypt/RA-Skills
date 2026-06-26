---
name: openclaw-model-usage
description: Inspect local OpenClaw model usage directly from session logs. Use when asked for the current model, recent model usage, usage breakdown by model, token totals, cost summaries, per-agent usage, or daily model usage summaries.
---

# OpenClaw Model Usage

Use this skill to inspect local OpenClaw model usage directly from session JSONL files.

## When to use

Use this skill when the user asks for:
- the current / most recent model in use
- recent model usage
- usage summaries by provider/model
- token totals by model
- cost summaries by model when available
- per-agent or per-session usage
- session/subagent rollups
- daily model usage summaries
- a compact summary plus an optional HTML dashboard

## What it does

This skill provides a local-first replacement for external model-usage workflows.

It reads OpenClaw session logs directly and does not depend on CodexBar.

## Preferred usage

Start with a short human-readable summary:

```bash
python {baseDir}/scripts/model_usage.py
python {baseDir}/scripts/model_usage.py overview
python {baseDir}/scripts/model_usage.py top-agents
python {baseDir}/scripts/model_usage.py top-sessions
```

Generate the HTML dashboard from **real local logs** when the user wants a richer artifact:

```bash
python {baseDir}/scripts/model_usage.py dashboard --root ~/.openclaw/agents --out dist/dashboard.html --title "OpenClaw Usage Dashboard"
```

Recommended response pattern:
- return a short human-readable summary first
- optionally generate and attach the HTML dashboard for richer inspection on phone/desktop

## JSON output

```bash
python {baseDir}/scripts/model_usage.py overview --json --pretty
python {baseDir}/scripts/model_usage.py sessions --json --pretty
python {baseDir}/scripts/model_usage.py subagents --json --pretty
python {baseDir}/scripts/model_usage.py rows --limit 20 --json --pretty
```

## Inputs

Default real source:

```bash
~/.openclaw/agents
```

Important:
- use the real local OpenClaw log root for user-facing summaries and dashboards
- do **not** use `tests/fixtures_root` unless you are intentionally running development tests
- fixture roots generate sample/test output, not the user's real usage report

## References

If you need field-level sourcing details, read:

- `references/discovery.md`
