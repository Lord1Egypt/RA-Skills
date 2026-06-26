---
name: Token Usage
description: Multi-agent token burn analysis across all registered OpenClaw agents
version: 0.2.2 # x-release-please-version
author: panthrocorp
license: MIT-0
metadata:
  openclaw:
    emoji: "🔥"
    homepage: https://github.com/PanthroCorp-Limited/openclaw-skills
    os: ["linux"]
---

# Token Usage

Analyse token usage and estimated costs across all registered OpenClaw agents. Dynamically discovers agents, groups sessions by channel category, flags anomalies, and presents a per-agent breakdown with combined totals.

## Step 1: Discover agents

List the contents of `~/.openclaw/agents/`. Each subdirectory is an agent.

For each agent directory, attempt to read `sessions/sessions.json`. If the file does not exist, is empty, or is not valid JSON, skip that agent and note it as "(no session data)" in the output.

## Step 2: Parse session entries

Each `sessions.json` is a JSON object. The keys are session key strings with the format:

```
agent:<agentId>:<channel>:<subtype>[:<identifier>]
```

For each session entry, extract these fields (all may be absent):

| Field | Type | Description |
|-------|------|-------------|
| `totalTokens` | integer | Total tokens consumed in this session |
| `inputTokens` | integer | Input/prompt tokens |
| `outputTokens` | integer | Output/completion tokens |
| `estimatedCostUsd` | float | Estimated cost in USD |
| `model` | string | Model identifier (e.g. `provider/model-name`) |
| `updatedAt` | integer | Last update timestamp in epoch milliseconds |

The **category** is the third segment of the session key (index 2 when splitting on `:`).

Examples:
- `agent:alice:discord:channel:123456789` -> category = `discord`
- `agent:alice:telegram:direct:987654321` -> category = `telegram`
- `agent:bob:cron:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` -> category = `cron`
- `agent:alice:main` -> category = `main`

## Step 3: Apply time window filter

The user specifies a time window. If not specified, default to **"this week"**.

| Window | Behaviour |
|--------|-----------|
| "this week" | Include sessions where `updatedAt` is within the last 7 days |
| "all time" | No filter; include all sessions |
| "last N days" | Include sessions where `updatedAt` is within the last N days |

If `updatedAt` is absent or `0`, include the session **only** when the window is "all time". For all other windows, exclude it.

Convert `updatedAt` from epoch milliseconds to a date for comparison.

## Step 4: Aggregate per agent, per category

For each agent, group the filtered sessions by category. Within each group, compute:

- **Total tokens**: sum of `totalTokens` (skip entries where the field is absent)
- **Input tokens**: sum of `inputTokens` (skip entries where the field is absent)
- **Output tokens**: sum of `outputTokens` (skip entries where the field is absent)
- **Estimated cost**: sum of `estimatedCostUsd` (skip entries where the field is absent)
- **Session count**: number of sessions in the group
- **Models**: the set of distinct `model` values (skip entries where the field is absent)

## Step 5: Flag anomalies

Apply two flags to each category group:

**SINKHOLE**: `totalTokens` > 10,000 AND (`estimatedCostUsd` is absent across all entries in the group, or the summed cost is less than $0.01).
This indicates high token volume on free or untracked models and may signal wasted computation.

**EXPENSIVE**: summed `estimatedCostUsd` > $5.00.
This indicates a high-spend category. Review whether the spend is justified.

A single category can have both flags (high tokens on a mix of free and paid models).

## Step 6: Present results

### Per-agent sections

For each agent that has session data, print a heading with the agent name and total session count, then a table with one row per category:

```
## alice (120 sessions)

| Category | Sessions | Tokens | Input | Output | Est. Cost | Models | Flags |
|----------|----------|--------|-------|--------|-----------|--------|-------|
| discord  | 80       | 1.2M   | 800K  | 400K   | $42.50    | model-a | EXPENSIVE |
| telegram | 25       | 120K   | 80K   | 40K    | $3.20     | model-a | |
| cron     | 10       | 95K    | 60K   | 35K    | $0.00     | model-b | SINKHOLE |
| main     | 5        | 20K    | 15K   | 5K     | $0.32     | model-a | |
```

Sort rows by estimated cost descending within each agent.

For agents skipped in Step 1, print: `## <agent> (no session data)`

### Combined summary

After all agent sections, print:

```
## Combined Totals

- **Total sessions**: <count>
- **Total tokens**: <sum> (input: <sum>, output: <sum>)
- **Total estimated cost**: $<sum>

### Top 3 by cost
1. <agent>/<category>: $<cost> (<tokens> tokens)
2. ...
3. ...

### Top 3 by token volume
1. <agent>/<category>: <tokens> tokens ($<cost>)
2. ...
3. ...
```

### Formatting rules

- Token counts: use human-readable format (e.g. `1.2M`, `45K`, `320`)
- Costs: round to 2 decimal places, prefix with `$`
- If a summed value is zero because all entries were absent, display as `-` not `0`

## Step 7: Persist structured history

Append exactly one JSON line to:

`~/.openclaw/workspace/memory/token-usage-history.ndjson`

Create the file if it does not exist. Never modify existing lines.

This step always runs. It does not require explicit user request.

### Record structure

The line is a compact JSON object (no newlines within the record):

```json
{"date":"YYYY-MM-DD","window":"<time window>","runAt":<epoch ms>,"agents":[...],"combined":{...}}
```

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | UTC date of this run (`YYYY-MM-DD`) |
| `window` | string | Time window used (e.g. `"last 1 day"`, `"this week"`) |
| `runAt` | integer | Epoch milliseconds when the skill ran |
| `agents` | array | One entry per agent that has session data |
| `combined` | object | Aggregated totals across all agents |

Each agent entry:

```json
{
  "id": "<agentId>",
  "categories": [
    {
      "category": "<category>",
      "sessions": 80,
      "totalTokens": 1200000,
      "inputTokens": 800000,
      "outputTokens": 400000,
      "estimatedCostUsd": 42.50,
      "models": ["model-a"],
      "flags": ["EXPENSIVE"]
    }
  ],
  "totals": {
    "sessions": 120,
    "totalTokens": 1435000,
    "inputTokens": 955000,
    "outputTokens": 480000,
    "estimatedCostUsd": 46.02
  }
}
```

The `combined` object mirrors the `totals` shape without an `id` field.

Use `null` for any numeric field where all entries in the group had the field absent. Use `[]` for `flags` when no flags apply. Agents with no session data are omitted from the record entirely.

## Step 8: Optional log write

**Only if the user explicitly requests logging**, append a timestamped summary to:

`~/.openclaw/workspace/memory/token-diet-log.md`

Create the file if it does not exist.

Append in this format:

```markdown
## YYYY-MM-DD -- Token Usage Report (window: <time window>)

- Total: <tokens> tokens, $<cost> estimated
- <agent>: <tokens> tokens, $<cost> (<flags if any>)
- ...
- Anomalies: <comma-separated list of flagged agent/category pairs with flag name>
```

Do not write to this file unless the user explicitly asks.

## Permissions

| Access | Path | Required |
|--------|------|----------|
| Read | `~/.openclaw/agents/*/sessions/sessions.json` | Always |
| Write | `~/.openclaw/workspace/memory/token-usage-history.ndjson` | Always |
| Write | `~/.openclaw/workspace/memory/token-diet-log.md` | Only when user requests logging |

No environment variables. No network access. No credentials.
