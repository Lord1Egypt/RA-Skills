---
name: osop
description: OSOP workflow authoring, validation, risk analysis, and self-optimization for AI agents
version: 1.2.0
emoji: "\U0001F4CB"
homepage: https://osop.ai
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
      config:
        - ~/.osop/config.yaml
    primaryEnv: OSOP_MCP_URL
    install:
      - kind: uv
        package: pyyaml
    always: false
user-invocable: true
disable-model-invocation: false
---

# OSOP — Open Standard Operating Procedures

Universal protocol for defining, validating, risk-assessing, and executing process workflows. Works with any AI coding agent.

## Capabilities

When this skill is active, the agent can:

- **Create** OSOP workflow definitions from natural language
- **Validate** workflow YAML against the OSOP schema
- **Risk Assess** workflows for security issues, permission gaps, destructive commands
- **Execute** workflows with dry-run mode for safety
- **Render** workflows as Mermaid diagrams
- **Optimize** workflows using execution history — detect slow steps, failure hotspots
- **Convert** between OSOP and external formats (GitHub Actions, BPMN, Airflow)
- **Report** on workflow executions as standalone HTML

## Sub-Skills

This pack includes 4 specialized skills:

| Skill | Command | What it does |
|-------|---------|-------------|
| `osop-log` | `/osop-log` | Record a structured session log after completing work |
| `osop-report` | `/osop-report` | Convert .osop + .osoplog.yaml to HTML report |
| `osop-review` | `/osop-review` | Security & risk analysis of workflows |
| `osop-optimize` | `/osop-optimize` | Improve workflows from execution history |

## OSOP Node Types (v1.0)

16 supported node types in 4 categories:

**Actors:** `human`, `agent`, `company`, `department`
**Technical:** `api`, `cli`, `db`, `git`, `docker`, `cicd`, `infra`, `mcp`
**Flow Control:** `system`, `event`, `gateway`, `data`

Use `subtype` for domain specialization (e.g., `type: agent, subtype: llm`).

## Edge Modes

13 modes: `sequential`, `conditional`, `parallel`, `loop`, `event`, `fallback`, `error`, `timeout`, `compensation`, `message`, `dataflow`, `signal`, `weighted`, `spawn`.

## Quick Start

### 1. Define a workflow

```yaml
osop_version: "1.0"
id: "deploy-staging"
name: "Deploy to Staging"
description: "Build, test, and deploy to staging environment."
version: "1.0.0"
tags: [deploy, staging]

nodes:
  - id: "build"
    type: "cli"
    name: "Build Project"
    description: "Run the build command"
  - id: "test"
    type: "cicd"
    subtype: "test"
    name: "Run Tests"
    description: "Execute test suite"
  - id: "deploy"
    type: "infra"
    name: "Deploy to Staging"
    description: "Push to staging environment"
    security:
      risk_level: "medium"
      approval_gate: true

edges:
  - from: "build"
    to: "test"
    mode: "sequential"
  - from: "test"
    to: "deploy"
    mode: "conditional"
    when: "tests.passed == true"
```

### 2. Review for risks

Run `/osop-review deploy-staging.osop` to check for security issues before execution.

### 3. Execute and log

After running, use `/osop-log` to record what happened as a structured `.osoplog.yaml`.

### 4. Generate report

Run `/osop-report` to create a standalone HTML report with dark mode and expandable nodes.

## Session Logging

After completing multi-step tasks, this skill produces:
- **`.osop`** — workflow definition (what should happen)
- **`.osoplog.yaml`** — execution record (what actually happened)

These files can be visualized at https://osop-editor.vercel.app or converted to HTML.

## Security Metadata

Nodes can declare `security.risk_level` (low/medium/high/critical), `security.permissions`, `security.secrets`, and `approval_gate` for risk analysis.

## Self-Optimization Loop

1. Execute workflow → produce `.osoplog`
2. Aggregate stats from past runs
3. Run `/osop-optimize` → get improvement suggestions
4. Apply approved changes → execute improved workflow
5. Repeat — the SOP gets better each iteration

## Links

- **Spec:** https://github.com/Archie0125/osop-spec
- **Visual Editor:** https://osop-editor.vercel.app
- **Examples:** https://github.com/Archie0125/osop-examples
- **Website:** https://osop.ai
