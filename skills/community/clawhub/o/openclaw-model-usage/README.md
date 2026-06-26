# openclaw-model-usage

[![CI](https://github.com/ranasalalali/openclaw-model-usage/actions/workflows/ci.yml/badge.svg)](https://github.com/ranasalalali/openclaw-model-usage/actions/workflows/ci.yml)

A portable AgentSkill and Python CLI for inspecting local OpenClaw model usage directly from session logs.

## Overview

`openclaw-model-usage` summarizes local model usage from OpenClaw session JSONL files and joins those usage rows with pragmatic session metadata from local OpenClaw session indexes.

It answers questions like:
- what model is active right now?
- how much token and cost usage happened recently?
- which agents and sessions are driving usage?
- which subagents rolled up under a parent session?
- what does usage look like by day, model, or session tree?

## Quick start

```bash
uv run --project . openclaw-model-usage
uv run --project . openclaw-model-usage overview
uv run --project . openclaw-model-usage top-agents
uv run --project . openclaw-model-usage top-sessions
uv run --project . openclaw-model-usage current
uv run --project . openclaw-model-usage dashboard
uv run --project . openclaw-model-usage overview --json --pretty
```

Default command: `overview`

## Human-friendly commands

These are aimed at chat/operator use with compact non-JSON output:

- `overview` — one-screen summary with totals, current model, top agents, top sessions, top models
- `top-agents` — ranked agents by cost
- `top-sessions` — ranked sessions by cost
- `current` — most recent model/call context

The existing detailed/raw views remain available:

- `agents`
- `sessions`
- `subagents`
- `session-tree`
- `daily`
- `recent`
- `rows`
- `dashboard` — writes a responsive self-contained HTML report locally

## Example output

```text
Usage overview — $0.0119, 3,700 tok, 4 calls
Agents 1 | Sessions 3 | Models 1
Current: openai-codex/gpt-5.4 | sample-agent | child-from-prompt | prompt-only-subagent

Top agents
1. sample-agent — $0.0119, 3,700 tok, 3 sessions

Top sessions
1. parent-session — $0.0099, 2,500 tok, 2 calls
2. child-from-prompt | prompt-only-subagent | parent parent-session | depth 1 — $0.0020, 600 tok, 1 calls
3. child-session | sample-subagent-task | parent parent-session | depth 1 — $0.0000, 600 tok, 1 calls

Top models
1. openai-codex/gpt-5.4 — $0.0119, 3,100 tok, 3 calls
```

## Detailed and JSON usage

```bash
uv run --project . openclaw-model-usage overview --json --pretty
uv run --project . openclaw-model-usage top-agents --json --pretty
uv run --project . openclaw-model-usage top-sessions --json --pretty
uv run --project . openclaw-model-usage sessions --json --pretty
uv run --project . openclaw-model-usage rows --session-id 8ce56106-1712-45c7-a2b4-93fcafe86315 --json --pretty
```

## Bundled script

Run the bundled script directly:

```bash
python3 scripts/model_usage.py
python3 scripts/model_usage.py overview
python3 scripts/model_usage.py top-agents
python3 scripts/model_usage.py top-sessions
python3 scripts/model_usage.py session-tree
python3 scripts/model_usage.py dashboard --out dist/dashboard.html
```

## HTML dashboard

Generate a local static dashboard from your **real local OpenClaw logs**:

```bash
uv run --project . openclaw-model-usage dashboard
uv run --project . openclaw-model-usage dashboard --root ~/.openclaw/agents --out dist/dashboard.html --title "OpenClaw Usage"
python3 scripts/model_usage.py dashboard --root ~/.openclaw/agents --out dist/dashboard.html --title "OpenClaw Usage Dashboard"
```

Important:
- the intended/default source is your real local log root: `~/.openclaw/agents`
- do **not** use `tests/fixtures_root` for normal/operator usage
- fixture roots are for development/testing only and will generate a sample/test dashboard, not your real usage dashboard

Default output path:

```text
dist/dashboard.html
```

The report is self-contained and includes:
- headline totals for cost, tokens, calls, sessions, agents, and models
- current/latest activity
- top agents
- top models
- top sessions with friendlier session names when metadata exists
- recent daily cost trend with a simple mobile-friendly daily cost bar chart, with calls/tokens kept as supporting detail
- recent assistant usage rows with better session labels

## Useful filters

```bash
uv run --project . openclaw-model-usage overview --agent tars-code --since-days 7
uv run --project . openclaw-model-usage top-sessions --channel discord --limit 10
uv run --project . openclaw-model-usage subagents --channel discord --json --pretty
uv run --project . openclaw-model-usage dashboard --channel discord --since-days 7 --out dist/discord-dashboard.html
```

## Data sources

Primary usage source:

```bash
~/.openclaw/agents/*/sessions/*.jsonl
```

Session metadata source:

```bash
~/.openclaw/agents/*/sessions/sessions.json
```

The tool joins assistant usage rows from JSONL files with available session metadata from `sessions.json` plus the JSONL session header line.

See `references/discovery.md` for field inventory and reliability notes.

## Repo structure

- `SKILL.md` — instructions for agent use
- `scripts/model_usage.py` — bundled script used by the skill
- `src/openclaw_model_usage/cli.py` — packaged CLI implementation
- `references/discovery.md` — local data source notes
- `tests/smoke_test.py` — fixture-based smoke test covering session attribution and human-friendly views

## Testing

```bash
python3 tests/smoke_test.py
uv run --project . openclaw-model-usage --help
```

Development note:
- test fixtures under `tests/fixtures_root` are only for smoke tests and development validation
- user-facing commands should point at real logs under `~/.openclaw/agents` unless you are intentionally testing against fixtures

CI also checks:
- CLI help
- smoke test execution
- package build

## Design goals

- portable
- local-first
- small and pragmatic
- no CodexBar dependency
- compact operator-friendly default output
- JSON still available for scripting and inspection
- reliable session/subagent attribution from observed local metadata

## Current limitations

- attribution is only as good as local metadata written by OpenClaw
- parent-child rollups rely on `sessions.json` `spawnedBy` linkage; missing index data means no tree link
- repo/project attribution is intentionally out of scope unless the logs say it explicitly
- only assistant message usage rows are counted, matching the existing tool design
