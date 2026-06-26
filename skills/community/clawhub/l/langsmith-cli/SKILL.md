---
name: langsmith-cli
description: >
  Query and analyze LangSmith traces with natural language or structured commands.
  Use when the user asks about LangSmith runs, trace failures, latency, cost, prompt
  comparisons, or wants to ask an LLM question about their traces (e.g. "why is my chain
  slow", "what failed yesterday", "ask langsmith why users are getting bad answers").
  Triggers on: langsmith runs, check traces, trace failures, ask langsmith, langsmith cost,
  langsmith diff, langsmith latency, why did X fail.
metadata: {"openclaw": {"requires": {"env": ["LANGSMITH_API_KEY"]}, "primaryEnv": "LANGSMITH_API_KEY"}}
---

# LangSmith CLI Skill

CLI: `scripts/langsmith.py`. Requires `LANGSMITH_API_KEY` in env (or `~/.zshrc`).

No second API key needed — the `ask` command fetches and formats traces as structured context for **your agent** to analyze. No trace data is sent to any third-party LLM.

## Commands

### Tier 0 — Ask (agent Q&A over traces)
```bash
python3 scripts/langsmith.py ask "<question>" --project <name> [--since 24h] [--limit 50]
```
Fetches recent runs and prints them as structured JSON context. Your agent reads the output and answers the question — no external LLM calls, no data leaving your machine beyond the LangSmith API.

Examples:
- `ask "why is my chain slow this week" --project my-project`
- `ask "what do failing runs have in common" --project my-project --since 7d`
- `ask "did the system prompt change on Friday affect output quality" --project my-project`

### Tier 1 — Situational Awareness
```bash
python3 scripts/langsmith.py runs <project> [--since 2h] [--status error|success] [--limit 20]
python3 scripts/langsmith.py cost <project> [--since 7d]       # token spend by chain/node
python3 scripts/langsmith.py latency <project> [--since 24h]   # p50/p95/p99 per run name
```

### Tier 2 — Before/After Comparisons
```bash
python3 scripts/langsmith.py diff <project> --before <ISO_date> --after <ISO_date>
python3 scripts/langsmith.py prompt-diff <run_id_a> <run_id_b>
```
`diff` compares avg latency, error rate, cost, output length across two time windows.
`prompt-diff` shows side-by-side system prompts + outputs for two specific runs.

### Tier 3 — Deep Analysis (stubs, expand as needed)
```bash
python3 scripts/langsmith.py cluster-failures <project> [--since 7d]
python3 scripts/langsmith.py replay <run_id>
```

## Auth Setup
```bash
export LANGSMITH_API_KEY=<your-key>
# or add to ~/.zshrc
```

Test with: `python3 scripts/langsmith.py runs <project> --limit 3`

## Security & Data Flow

This skill makes outbound network requests only to **`api.smith.langchain.com`** (the LangSmith API). That's it.

- **`LANGSMITH_API_KEY`** — sent as an HTTP header to `api.smith.langchain.com` only. Never logged or stored.
- **Trace data** — fetched from LangSmith and printed to stdout for your agent to read. No trace data is sent to any third-party LLM or external service.
- **No second API key required** — the `ask` command outputs structured trace context for your existing agent to analyze, rather than making its own LLM calls.
- **No telemetry** — the script collects no usage data.

The script is ~300 lines of pure Python with no obfuscation. Audit it at `scripts/langsmith.py`.

## API Reference
See `references/langsmith-api.md` for endpoint details and run object schema.
