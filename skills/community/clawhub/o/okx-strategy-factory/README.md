# OKX Strategy Factory

[中文](./README_CN.md)

A meta-skill that coordinates 5 specialized AI agents to handle the full lifecycle of on-chain trading strategies on OKX OnchainOS: development, backtesting, deployment, publishing, and iteration.

## What is this?

Strategy Factory is an **Agent Team pipeline** — instead of a single AI agent doing everything, a Lead coordinator spawns purpose-built expert agents for each phase. Each agent has strict input/output contracts and quality gates that must pass before the pipeline advances.

Built for developers who want AI agents to develop, validate, deploy, and continuously improve on-chain trading strategies via OKX DEX API.

## Architecture

```
User Request
     │
     ▼
┌─────────┐     ┌───────────┐     ┌─────────┐     ┌──────────┐     ┌───────────┐
│ Strategy │────▶│ Backtest  │────▶│  Infra   │────▶│ Publish  │     │ Iteration │
│  Agent   │     │  Agent    │     │  Agent   │     │  Agent   │     │   Agent   │
│          │     │           │     │          │     │(parallel)│     │(post-LIVE)│
│ Develop  │     │ Validate  │     │ Deploy   │     │ Package  │     │  Review   │
│ strategy │     │ backtest  │     │ to VPS   │     │ as Skill │     │ & propose │
└─────────┘     └───────────┘     └─────────┘     └──────────┘     └───────────┘
     ▲               │ FAIL            │                                  │
     └───────────────┘                 │ FAIL → auto-rollback             │
     ▲                                                                    │
     └────────────────────── user approves optimization ──────────────────┘

                    Lead Agent (coordinator, never writes code)
```

## Platform Compatibility

> **Recommended**: Claude Code, Cursor, Gemini CLI — AI coding IDEs with subagent/teammate spawning.
>
> **Not recommended**: OpenClaw — OpenClaw is a runtime for executing strategies, not for multi-agent development pipelines. Use the individual strategy skills (e.g. `grid-trading`) on OpenClaw instead.

## Installation

**Claude Code** (recommended):
```bash
npx clawhub install okx-strategy-factory
# Or manual:
cp -r okx-strategy-factory ~/.claude/skills/
```

**Cursor**:
```bash
cp -r okx-strategy-factory /path/to/project/.cursor/skills/
```

**Gemini CLI**:
```bash
cp -r okx-strategy-factory /path/to/project/.gemini/skills/
```

## Quick Start

After installation, ask your AI agent:

```
Use the okx-strategy-factory skill to develop a grid trading strategy for ETH/USDC on Base.
```

Or trigger a specific phase:

```
Use okx-strategy-factory to backtest the grid-trading strategy in Strategy/grid-trading/Script/v1.0.0/.
```

```
Use okx-strategy-factory to iterate on the live ETH grid strategy — review the last 7 days.
```

The Lead agent will coordinate the appropriate expert agents automatically.

## Directory Structure

```
okx-strategy-factory/
├── SKILL.md              # Main document: pipeline definition + state machine
├── roles/                # Agent role definitions
│   ├── lead.md           #   Coordinator — spawns agents, enforces gates
│   ├── strategy.md       #   Writes strategy code + config + risk profile
│   ├── backtest.md       #   Validates strategy against historical data
│   ├── infra.md          #   Deploys to VPS via SSH
│   ├── publish.md        #   Packages strategy as cross-platform Skill
│   └── iteration.md      #   Post-LIVE review and optimization proposals
├── templates/            # Structured templates
│   └── requirements.md   #   Strategy requirements template (Lead fills before spawning Strategy agent)
├── references/           # Shared technical references
│   ├── api-interfaces.md #   Adapter interface spec (wallet, dex, position)
│   ├── risk-schema.json  #   JSON Schema for risk-profile.json validation
│   └── strategy-lessons.md # Strategy lessons learned (risk, MTF, cost, pitfalls)
├── assets/               # Templates and tools
│   ├── product-skill-template/  # Strategy-specific packaging templates (.tmpl)
│   ├── skill-templates/         # Skill design pattern templates (pipeline, tool-wrapper, etc.)
│   └── publish.sh               # Skill validation and publishing script
└── hooks/                # Pipeline automation
    ├── task-completed-gate.sh   # Quality gate checks between steps
    └── teammate-idle-reassign.sh # Reassign idle agents
```

## Agent Roles

| Role | Responsibility | Input | Output |
|------|---------------|-------|--------|
| **Lead** | Coordinate pipeline, enforce quality gates, manage state | User request | Spawn prompts, state.json updates |
| **Strategy** | Write strategy logic + config + risk profile | `Strategy/{strategy}/requirements.md` (structured requirements distilled by Lead) | `Strategy/{strategy}/Script/v{ver}/` (strategy.js, config.json, risk-profile.json, README.md) |
| **Backtest** | Validate strategy against historical data | Strategy script directory | `Strategy/{strategy}/Backtest/v{ver}/` (backtest-report.json, equity-curve.csv) |
| **Infra** | Deploy to VPS (SSH, pm2, health check, rollback) | Backtest-passed strategy version | Running process on VPS, VERSION file |
| **Publish** | Package strategy as cross-platform Skill + GitHub release | Backtest-passed strategy + deploy confirmation | `{strategy}/` (manifest.json, install.sh, SKILL.md) |
| **Iteration** | Analyze live performance, propose optimizations | On-chain trade history + market data | `Strategy/{strategy}/Iteration/v{ver}-review-{date}.md` |

## Pipeline

```
Step 1: Strategy Development
  Lead distills discussion into Strategy/{strategy}/requirements.md → user confirms → spawn Strategy agent
  Gate: strategy.js + config.json + risk-profile.json + README.md all present
    │
    ▼
Step 2: Backtest Validation
  Gate: Compliance PASS + Sharpe > 1.0 + Win Rate > 40%
  FAIL → back to Step 1 with failure details
    │
    ▼
Step 3: Deploy to VPS ──────────────────── Step 4: Publish as Skill (parallel start)
  Gate: pm2 online + no errors in 30s       Gate: manifest.json + install.sh + adapters
  FAIL → auto-rollback to previous version   GitHub release waits for Step 3 success
    │
    ▼
Step 5: Iteration (post-LIVE, on-demand)
  Gate: user confirms optimization proposal
  Approved → new version starts at Step 1 (must re-backtest)
```

Steps execute strictly in order. No skipping. Iteration always triggers a full re-run from Step 1.

## Prerequisites

- **onchainos CLI** — `npx skills add okx/onchainos-skills`
- **OKX API Key** — with DEX trading permissions
- **OnchainOS Agentic Wallet** — with TEE signing enabled
- **Python 3.10+** — for backtest engine and trading scripts
- **VPS** (optional) — for live deployment
- **1Password CLI** (optional) — for secure credential management (`op`)

## License

Apache-2.0
