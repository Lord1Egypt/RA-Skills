---
name: agent-forum
version: 1.0.0
description: Run a structured multi-perspective debate in a single LLM call. Five hardcoded viewpoints argue across three rounds to eliminate confirmation bias and produce a verdict. Use for Monday Leverage Audit, Friday Weekly Retro, any strategic decision where bias is a risk, or when evaluating opportunities from OUTSTANDING.md. Triggers on "run a forum", "debate this", "leverage audit", "weekly retro", or when delegation skill needs a second opinion on opportunity framing.
---

# Agent Forum

One prompt. Five simulated agents. Three rounds. One verdict. Runs as a single `sessions_spawn` call (~8-12k tokens).

## The 5 Agents

| Agent | Perspective |
|-------|-------------|
| **Revenue Realist** | No revenue signal = not working. Show me the money. |
| **Builder** | Ship more, measure later. Momentum matters. |
| **Skeptic** | Prove it. What's the null hypothesis? Assumes failure until evidence. |
| **Operator** | Systems, reliability, cost. What breaks at 10x scale? |
| **Customer Voice** | Would I open this email? Pay for this? Care about this? |

## Prompt Template

Inject `{DATA}` and `{QUESTION}` into this template:

```
You are running a strategic forum with 5 agents. Each agent has a hardcoded perspective.
They debate the data in 3 rounds, then produce a joint verdict.

RULES:
- 2-3 sentences per agent per round. No fluff.
- Agents MUST disagree where perspectives conflict.
- Round 3: CONSENSUS, CONTESTED, VERDICT.
- Brutally honest. No cheerleading.
- Total output under 3,000 tokens.

THE 5 AGENTS:
1. Revenue Realist — Only money. No revenue signal = not working.
2. Builder — Ship more, iterate. Momentum > perfection.
3. Skeptic — Prove it. Assumes failure until evidence.
4. Operator — Systems, reliability, cost. What breaks at scale?
5. Customer Voice — Would I buy/open/care about this?

DATA PAYLOAD:
{DATA}

QUESTION:
{QUESTION}

FORMAT:
## Round 1: Initial Positions
## Round 2: Challenges & Rebuttals
## Round 3: Verdict
### Consensus
### Contested
### Verdict
### Controllable Assessment
[Each item: ✅ Controllable / ⚠️ Partial / ❌ Uncontrollable]
```

## Spawn Config

```
sessions_spawn:
  task: [formatted prompt]
  model: "github-copilot/claude-opus-4.6"
  mode: "run"
  runTimeoutSeconds: 120
```

## Data Collection Before Forum

**Leverage Audit (Monday):** Resend analytics, lead pipeline counts, revenue/signups, error logs, outreach totals, cron health, cost burn.

**Weekly Retro (Friday):** Sprint target vs actual, emails sent, leads sourced, revenue events, things shipped/broke, blockers hit.

## Cron

- Monday 9 AM ET: `0 13 * * 1` (leverage audit)
- Friday 9 AM ET: `0 13 * * 5` (retro)

Use OpenClaw cron (needs LLM access), not crontab.
