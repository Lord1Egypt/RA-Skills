---
name: osop-log
description: Generate OSOP session log — creates .osop workflow and .osoplog.yaml execution record
version: 1.2.0
emoji: "\U0001F4DD"
homepage: https://osop.ai
argument-hint: [short description of what was done]
metadata:
  openclaw:
    requires:
      bins:
        - bash
      config:
        - ~/.osop/config.yaml
    install: []
    always: false
user-invocable: true
disable-model-invocation: false
---

# OSOP Session Logger

You just completed a task. Now produce a structured session log.

## What to create

1. **`sessions/YYYY-MM-DD-<short-desc>.osop`** — workflow definition
2. **`sessions/YYYY-MM-DD-<short-desc>.osoplog.yaml`** — execution record

Create the `sessions/` directory if it doesn't exist.

## Task description

$ARGUMENTS

## .osop format

```yaml
osop_version: "1.0"
id: "session-<short-description>"
name: "<What you did>"
description: "<1-2 sentence summary>"
version: "1.0.0"
tags: [claude-code, <relevant-tags>]

nodes:
  - id: "<step-id>"
    type: "<node-type>"   # human, agent, mcp, cli, api, cicd, git, db, docker, infra, system, event, gateway, data, company, department
    subtype: "<subtype>"  # Optional: llm, explore, plan, worker, tool, test, commit, rest, etc.
    name: "<Step Name>"
    description: "<What this step does>"
    security:
      risk_level: "<low|medium|high|critical>"

edges:
  - from: "<step-a>"
    to: "<step-b>"
    mode: "sequential"    # sequential, parallel, conditional, fallback, error, spawn, etc.
```

## .osoplog.yaml format

```yaml
osoplog_version: "1.0"
run_id: "<generate-uuid>"
workflow_id: "<matches .osop id>"
mode: "live"
status: "COMPLETED"

trigger:
  type: "manual"
  actor: "user"
  timestamp: "<ISO timestamp>"

started_at: "<ISO timestamp>"
ended_at: "<ISO timestamp>"
duration_ms: <total ms>

runtime:
  agent: "claude-code"
  model: "<current model>"

node_records:
  - node_id: "<step-id>"
    node_type: "<type>"
    attempt: 1
    status: "COMPLETED"
    started_at: "<ISO>"
    ended_at: "<ISO>"
    duration_ms: <ms>
    outputs:
      <what you produced>
    tools_used:
      - { tool: "<tool-name>", calls: <n> }
    reasoning:
      question: "<what was decided>"
      selected: "<chosen approach>"
      confidence: <0.0-1.0>

result_summary: "<1-2 sentence summary>"
```

## Node type mapping

| Action | type | subtype |
|---|---|---|
| Read/explore files | `mcp` | `tool` |
| Edit/write files | `mcp` | `tool` |
| Shell commands | `cli` | `script` |
| Run tests | `cicd` | `test` |
| Git operations | `git` | `commit` / `branch` / `pr` |
| Analyze/reason | `agent` | `llm` |
| Search codebase | `mcp` | `tool` |
| Ask user | `human` | `input` |
| User reviews | `human` | `review` |
| Spawn sub-agent | `agent` | `explore` / `plan` / `worker` |
| API calls | `api` | `rest` |

## Sub-agent tracking

If you spawned sub-agents, use `parent` on child nodes and `spawn` edge:

```yaml
nodes:
  - id: "coordinator"
    type: "agent"
    subtype: "coordinator"
  - id: "explore_1"
    type: "agent"
    subtype: "explore"
    parent: "coordinator"
edges:
  - from: "coordinator"
    to: "explore_1"
    mode: "spawn"
```

## Important

- Be accurate about what tools were used and how many calls
- Include reasoning for non-obvious decisions
- Estimate durations based on tool call timing
- If the task failed, set status to FAILED and include error details
- View logs at https://osop-editor.vercel.app
