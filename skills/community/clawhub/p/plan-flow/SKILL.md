---
name: plan-flow
version: 1.0.8
description: Structured AI-assisted development workflows - discovery, planning, execution, code reviews, and testing
metadata: {"openclaw":{"requires":{"bins":["git","gh"]}},"clawhub":{"requires":{"bins":["git","gh"]},"emoji":"🗺️","homepage":"https://github.com/brunoscardoso/plan-flow"}}
homepage: https://github.com/brunoscardoso/plan-flow
user-invocable: true
---

# Plan-Flow: Structured AI-Assisted Development

A comprehensive skill set for AI-assisted software development with structured workflows and persistent project memory.

## Available Commands

| Command | Description |
|---------|-------------|
| `/setup` | Analyze project and generate pattern files |
| `/discovery` | Create discovery document for requirements gathering |
| `/create-plan` | Create implementation plan with phases and complexity scores |
| `/execute-plan` | Execute plan phases with verification |
| `/create-contract` | Create integration contract from API docs |
| `/review-code` | Review local uncommitted changes |
| `/review-pr` | Review a Pull Request |
| `/write-tests` | Write tests to achieve coverage target |
| `/flow` | Toggle autopilot mode (auto-chains the full workflow) |

## Always-Active Features

| Feature | Description |
|---------|-------------|
| Project Ledger | Persistent learning journal at `flow/ledger.md` - silently captures mistakes, corrections, and project-specific knowledge across sessions |

## Recommended Workflow

**Automated - runs without asking permission:**

```
1. /setup           → Index project patterns (run once)
2. /discovery       → Gather requirements for a feature
3. /create-plan     → Create structured implementation plan (auto-runs after discovery)
4. /execute-plan    → Execute the plan phase by phase (auto-runs after plan)
5. /review-code     → Review changes before committing
6. Archive          → Move discovery + plan to flow/archive/
```

**Only stop to ask the user when:**
- Missing critical information (device type, browser, etc.)
- Need to reproduce an issue
- Ambiguous requirements
- Need approval for destructive actions

**Never ask "Ready to create plan?" or "Proceed with execution?" - just do it.**

## Core Concepts

### Complexity Scoring

Every plan phase has a complexity score (0-10):

| Score | Level | Description |
|-------|-------|-------------|
| 0-2 | Trivial | Simple, mechanical changes |
| 3-4 | Low | Straightforward implementation |
| 5-6 | Medium | Moderate complexity, some decisions |
| 7-8 | High | Complex, multiple considerations |
| 9-10 | Very High | Significant complexity/risk |

### Flow Directory Structure

All artifacts are stored in `flow/`:

```
flow/
├── archive/           # Completed/abandoned plans
├── contracts/         # Integration contracts
├── discovery/         # Discovery documents
├── plans/             # Active implementation plans
├── references/        # Reference materials
├── reviewed-code/     # Code review documents
├── reviewed-pr/       # PR review documents
└── ledger.md          # Persistent project learning journal
```

## Critical Rules

1. **Automated Workflow**: Run discovery → plan → execute automatically. Only stop to ask when you need information from the user.
2. **Discovery First (Hard Block)**: `/discovery` is **required** before `/create-plan`. Plans cannot be created without a discovery document. No exceptions. If no discovery exists, run discovery first.
3. **Tests Last**: Tests are always the last phase of any implementation plan.
4. **Build at End Only**: Run build verification only after ALL phases complete.
5. **Archive When Done**: Move completed discovery and plans to `flow/archive/`.

## Configuration

Create `.plan-flow.yml` in your project root:

```yaml
ai:
  provider: claude
  anthropic_api_key: sk-ant-api03-your-key-here
```

## Requirements

- `git` - For version control operations
- `gh` - GitHub CLI for PR reviews

## Installation

```bash
clawhub install plan-flow
```

Or add to your workspace skills folder:

```bash
git clone https://github.com/brunoscardoso/plan-flow.git ~/.openclaw/skills/plan-flow
```
